#!/usr/bin/env python
import sys
import ipaddress  # pip install ipaddress
import SoftLayer  # pip install softlayer

# Your SoftLayer account credentials
USERNAME=''
API_KEY=''
# A list of IP addresses that you need to be able to connect to
CONNECT = [
  '10.1.1.1',
  '10.2.2.2'
]

# Connect to SoftLayer
client = SoftLayer.Client(username = USERNAME, api_key = API_KEY, endpoint_url = SoftLayer.API_PUBLIC_ENDPOINT)

# Locate my user object; loop if needed to set account flags
for try_count in [1, 2] :
  users = client['SoftLayer_Account'].getUsers()
  user = [x for x in users if x['username'] == USERNAME][0]

  # Check for SSL VPN and manual VPN override
  if not user['sslVpnAllowedFlag'] :
    if try_count == 1 :
      print "SSL VPN is not enabled for your account, enabling"
      client['SoftLayer_User_Customer'].editObject({ 'sslVpnAllowedFlag': True }, id = user['id'])
    else :
      print "Unable to enable SSL VPN"
      sys.exit(1)
  if not user['vpnManualConfig'] :
    if try_count == 1 :
      print "Manual VPN subnet configuration is not set for your account, enabling"
      client['SoftLayer_User_Customer'].editObject({ 'vpnManualConfig': True }, id = user['id'])
    else :
      print "Unable to enable manual subnet configuration"
      sys.exit(1)

# Discover currently associated subnets
print "Your currently selected subnets:"
subnets = client['SoftLayer_User_Customer'].getOverrides(id=user['id'])
for subnet in subnets :
  details = client['SoftLayer_Network_Subnet'].getObject(id=subnet['subnetId'])
  print "  %s/%s" % (details['networkIdentifier'], details['cidr'])
  client['SoftLayer_Network_Service_Vpn_Overrides'].deleteObject(id=subnet['id'])

# Locate the subnets that contain all of the IP addresses we are interested in
all_subnets = client['SoftLayer_Account'].getPrivateSubnets()
addresses = [ipaddress.ip_address(unicode(x)) for x in CONNECT]
new_subnets = []
new_overrides = []
for subnet in all_subnets :
  network = ipaddress.ip_network(u"%s/%s" % (subnet['networkIdentifier'], subnet['cidr']))
  for address in addresses :
    if address in network :
      new_subnets.append(subnet)
      new_overrides.append({'subnetId': subnet['id'], 'userId': user['id']})
      break

print "New subnets:"
for subnet in new_subnets :
  print "  %s/%s" % (subnet['networkIdentifier'], subnet['cidr'])

# Apply these new subnets to the user
client['SoftLayer_Network_Service_Vpn_Overrides'].createObjects(new_overrides)

# SL says that we must "commit" our changes with this call
client['SoftLayer_User_Customer'].updateVpnUser(id=user['id'])

print "You may have to wait several minutes for the changes to propagate to your VPN"

