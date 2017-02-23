import SoftLayer

# Your SoftLayer account credentials
USERNAME=''
API_KEY=''

# Connect to SoftLayer
client = SoftLayer.Client(username = USERNAME, api_key = API_KEY, endpoint_url = SoftLayer.API_PUBLIC_ENDPOINT)

print "VLANs containing no hardware or guests:"

# Find all our VLANs
vlans = client['SoftLayer_Account'].getNetworkVlans()
for vlan in vlans :
  hardware = client['SoftLayer_Network_Vlan'].getHardware(id = vlan['id'])
  guests = client['SoftLayer_Network_Vlan'].getVirtualGuests(id = vlan['id'])
  gnc = client['SoftLayer_Network_Vlan'].getGuestNetworkComponents(id = vlan['id'])

  if len(hardware) == 0 and len(guests) == 0 and len(gnc) == 0 :
    print vlan['id']

