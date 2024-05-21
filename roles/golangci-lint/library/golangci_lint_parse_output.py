# Copyright 2020 VEXXHOST, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: golangci_lint_parse_output
short_description: Parse the output of golangci-lint and return comments
author: Mohammed Naser (@mnaser)
description:
  - Parse the output of golangci-lint and return content for inline comments.
requirements:
  - "python >= 3.5"
options:
  workdir:
    description:
      - Path for the project to strip for comments
    required: true
    type: str
  output:
    description:
      - Output from the golangci-lint command run
    required: true
    type: str
'''

import re

from ansible.module_utils.basic import AnsibleModule

BUILD_RE = re.compile(r'^.*\[(.*)\]"$')
RE = re.compile(r"^(.*):(\d+):\d+: (.*)$")


def parse_output(output, workdir):
    comments = {}
    for line in output.split('\n'):
        # If we have a build failure, we need to match that first and extract
        # the error message.  We'll also need to remove 'workdir' as it
        # contains the full path.
        m = BUILD_RE.match(line)
        if m:
            line = re.sub(r'\\(.)', r'\1', m.group(1))
            # We find everything up until workdir, strip the length of workdir
            # and then remove one extra character to remove leading slash.
            index = line.find(workdir) + len(workdir) + 1
            line = line[index:].replace(workdir, '')
        m = RE.match(line)
        if m:
            file_path = m.group(1)
            start_line = m.group(2)
            message = m.group(3)

            comments.setdefault(file_path, [])
            comments[file_path].append(dict(line=int(start_line),
                                            message=message))
    return comments


def main():
    module = AnsibleModule(
        argument_spec=dict(
            output=dict(required=True, type='str', no_log=True),
            workdir=dict(required=True, str='str'),
        )
    )

    comments = parse_output(module.params['output'], module.params['workdir'])
    module.exit_json(changed=False, comments=comments)


if __name__ == '__main__':
    main()
