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

