#!/usr/bin/python
import os, sys, requests
from ansible.module_utils.basic import *

def keyvault_present(data):
	server = data['server']
	name = data['name']
	MSI_ENDPOINT = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net"
	r = requests.get(MSI_ENDPOINT, headers = {"Metadata" : "true"}) 
	data = r.json() 

	KeyVaultURL = "https://%s.vault.azure.net/secrets/%s?api-version=2016-10-01" % (server, name)
	kvSecret = requests.get(url = KeyVaultURL, headers = {"Authorization": "Bearer " + data["access_token"]})

	return True, True, kvSecret.json()["value"]

def keyvault_exists(data):
	server = data['server']
	name = data['name']
        result = "incorrect key"
	MSI_ENDPOINT = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net"
	r = requests.get(MSI_ENDPOINT, headers = {"Metadata" : "true"}) 
	data = r.json() 

	KeyVaultURL = "https://%s.vault.azure.net/secrets/%s?api-version=2016-10-01" % (server, name)
	kvSecret = requests.get(url = KeyVaultURL, headers = {"Authorization": "Bearer " + data["access_token"]})

	return True, True, kvSecret.json()["value"]

# https://blog.toast38coza.me/custom-ansible-module-hello-world/
def main():
        fields = {
                "name": {"required": True, "type": "str" },
                "server": {"required": True, "type": "str"},
                "description": {"required": False, "type": "str"},
                "timeout": {"default": 10, "type": "int" },
                "state": {
                        "default": "present",
                        "choices": ['present', 'exists'],
                        "type": 'str'
                },
        }

        choice_map = {
                "present": keyvault_present,
                "exists": keyvault_exists,
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

