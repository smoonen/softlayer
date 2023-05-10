import pprint
import requests
import SoftLayer

# SoftLayer API requests can be authenticated with a classic API key but also with an IAM token.

# First, exchange an IAM API key (not a classic API key) for an IAM token.

APIKEY = '...'

hdrs = { 'Accept'       : 'application/json',
         'Content-Type' : 'application/x-www-form-urlencoded' }
params = { 'grant_type' : 'urn:ibm:params:oauth:grant-type:apikey',
           'apikey'     : APIKEY }
resp = requests.post('https://iam.cloud.ibm.com/identity/token', data = params, headers = hdrs)
assert resp.status_code in (200, 202)
json = resp.json()

# Authenticate with the SoftLayer API using the IAM token we obtained

auth = SoftLayer.auth.BearerAuthentication('', json['access_token'])
client = SoftLayer.API.IAMClient(auth = auth)

# Make a SoftLayer API call

result = client['SoftLayer_Account'].getObject()
pprint.pprint(result)

