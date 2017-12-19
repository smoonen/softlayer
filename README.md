# softlayer
SoftLayer related tooling

## vpn_subnets.py

SoftLayer limits a VPN connection to 64 subnets. If you have more than 64 subnets in
your SoftLayer account, you need to switch your VPN subnet management from Automatic
to Manual and specifically select the subnets you want to connect to.

This script simplifies the process of managing these subnets. By providing your
SoftLayer username, API key, and a list of private IP addresses to which you need to
connect, the tool sets your account's VPN access to manual, and connects to the
set of subnets that encompass the IP addresses you selected.

*Nota bene:* VPN configuration changes seem to take several minutes to take effect.

## empty_vlans.py

This script helps to identify VLANs in your SoftLayer account that have no attached hardware or virtual guests. These VLANs are not in use and are candidates for cancellation together with their subnets.

## monitor.py

This script searches for bare metal servers in your SoftLayer account for which the SoftLayer monitor reports that the server is down and for which the monitor is configured to monitor the public IP address rather than the private IP address. For these servers, the monitor configuration is replaced with a new configuration that monitors the private IP address instead. This is useful for vSphere (ESXi) hosts that have a public interface but whose public IP address is shut down.

