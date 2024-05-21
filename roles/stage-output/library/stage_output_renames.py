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


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: stage_output_renames

short_description: Rename file extensions for stage-output

description:
    - "Renames file extensions for stage-output quickly."

options:
    extensions:
        description:
            - Dict of file extensions to be replaced with .txt when staging.
              key is extension and value is boolean determining if it should
              be replaced.
        required: true
    rename_dir:
        description:
            - The base dir to rename files in.
        required: true

author:
    - Clark Boylan
'''


EXAMPLES = '''
- name: Stage output rename extensions
  stage_output_renames:
    extensions:
      conf: true
      log: true
      py: false
    rename_dir: '/home/zuul/logs'
'''


RETURN = '''
msg:
    description: The output message from the module.
renamed:
    description: Dict of old: new file names.
errors:
    description: Dict of old: error strings.
'''


from ansible.module_utils.basic import AnsibleModule  # noqa

import os
import os.path


def rename_file(old_path):
    # Only rename the file if it is a normal file
    if os.path.isfile(old_path) and not os.path.islink(old_path):
        path, ext = old_path.rsplit('.', 1)
        new_path = path + '_' + ext + '.txt'
        # Only rename if the target doesn't already exist
        if not os.path.isfile(new_path) and \
                not os.path.isdir(new_path) and \
                not os.path.islink(new_path):
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                # TODO Do we need to distinguish between these cases?
                return None, str(e)
            return new_path, None
        return None, "Target path exists."
    return None, "Source path does not exist."


def rename_exts(path, exts):
    results = dict(
        renamed=dict(),
        errors=dict(),
    )
    for root, dirs, files in os.walk(path):
        for f in files:
            for e in exts:
                if f.endswith(e):
                    full_path = os.path.join(root, f)
                    new_path, error = rename_file(full_path)
                    if error:
                        results["errors"][full_path] = error
                    elif new_path:
                        results["renamed"][full_path] = new_path
                    break
    return results


def run_module():
    module_args = dict(
        extensions=dict(type='dict', required=True),
        rename_dir=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    rename_dir = module.params['rename_dir']

    if not os.path.isdir(rename_dir):
        module.fail_json(msg='Rename dir %s is not a dir or does not exist' %
                         rename_dir, **result)

    extensions_dict = module.params['extensions']
    extensions_list = ['.' + k for k, v in extensions_dict.items()
                       if module.boolean(v)]

    rename_result = rename_exts(rename_dir, extensions_list)
    result.update(rename_result)

    if result['renamed']:
        result['changed'] = True
    if result['errors']:
        module.fail_json(msg='Failed to rename all requested files', **result)
    else:
        module.exit_json(msg='Renamed files for staging.', **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
