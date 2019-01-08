#!/usr/bin/python
import os, sys
from subprocess import call
from ansible.module_utils.basic import *

def pretask_present(data):
        result = "task set"
	call("/etc/az/.az", shell=True)
        return True, True, result

def pretask_absent(data):
        result = "task unset"
        envs = [
                'AZURE_CLIENT_ID',
                'AZURE_SECRET',
                'AZURE_SUBSCRIPTION_ID',
                'AZURE_TENANT'
        ]
        for env in envs:
                if hasattr(os, 'unsetenv'):
                        os.unsetenv(env)
                else:
                        # os.putenv(env, '')
                        os.environ[env] = ''
	call("/etc/az/.unaz", shell=True)
        os.environ['AZURE_CLIENT_ID'] = 'foo'
        return True, True, result

# https://blog.toast38coza.me/custom-ansible-module-hello-world/
def main():
        fields = {
                "task": {"required": True, "type": "str" },
                "description": {"required": False, "type": "str"},
                "private": {"default": False, "type": "bool" },
                "real": {"default": True, "type": "bool" },
                "timeout": {"default": 10, "type": "int" },
                "state": {
                        "default": "present",
                        "choices": ['present', 'absent'],
                        "type": 'str'
                },
        }

        choice_map = {
                "present": pretask_present,
                "absent": pretask_absent,
        }

        module = AnsibleModule(argument_spec=fields)
        is_error, has_changed, result = choice_map.get(module.params['state'])(module.params)
        module.exit_json(changed=has_changed, meta=result)

        if not is_error:
                module.exit_json(changed=has_changed, meta=result)
        else:
                module.fail_json(msg="preload filed", meta=result)

if __name__ == '__main__':
    main()

