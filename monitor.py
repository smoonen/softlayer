import SoftLayer

# Your SoftLayer account credentials
USERNAME=''
API_KEY=''

# Connect to SoftLayer
client = SoftLayer.Client(username = USERNAME, api_key = API_KEY, endpoint_url = SoftLayer.API_PUBLIC_ENDPOINT)

# Search for bare metal servers that are reported to be down by the SL monitor
down_hardware = client['SoftLayer_Account'].getNetworkMonitorDownHardware()
for hw_obj in down_hardware :
  monitors = client['SoftLayer_Hardware'].getNetworkMonitors(id = hw_obj['id'])

  # Test whether this server's monitor is monitoring its public or private IP
  private_monitor = None
  public_monitor = None
  for monitor in monitors :
    if monitor['ipAddress'] == hw_obj['primaryIpAddress'] :
      public_monitor = monitor.copy()
    elif monitor['ipAddress'] == hw_obj['privateIpAddress'] :
      private_monitor = monitor.copy()

  # Reconfigure the monitor to use the private IP if necessary
  if private_monitor is None :
    if public_monitor is None :
      print "Host %s is flagged down by SL, has no public or private monitor!" % hw_obj['fullyQualifiedDomainName']
    else :
      print "Host %s is flagged down by SL, has no private monitor; will fix" % hw_obj['fullyQualifiedDomainName']
      new_monitor = public_monitor.copy()
      del new_monitor['id']
      del new_monitor['status']
      del new_monitor['guestId']
      new_monitor['ipAddress'] = hw_obj['privateIpAddress']
      client['SoftLayer_Network_Monitor_Version1_Query_Host'].createObject(new_monitor)
      client['SoftLayer_Network_Monitor_Version1_Query_Host'].deleteObject(id = public_monitor['id'])
  else :
    print "Host %s is flagged down by SL, although it has a private monitor!" % hw_obj['fullyQualifiedDomainName']

