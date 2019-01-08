#!/usr/bin/env python

import requests 

server = "dackeyvault"
name = "dac-prod-autokey"
# name = "npdac-infraautomation"

MSI_ENDPOINT = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net"
r = requests.get(MSI_ENDPOINT, headers = {"Metadata" : "true"}) 
data = r.json() 

KeyVaultURL = "https://%s.vault.azure.net/secrets/%s?api-version=2016-10-01" % (server,name)
kvSecret = requests.get(url = KeyVaultURL, headers = {"Authorization": "Bearer " + data["access_token"]})

print kvSecret.json()["value"]
