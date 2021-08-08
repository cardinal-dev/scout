<h1>scout-cli</h1>
<h3>CLI for Managing Cisco Autonomous APs</h3>

`scout-cli` depends on `scout` logic in order to manage Cisco APs via the CLI. Instead of passing positional arguments
directly into the functions, `scout-cli` uses the `sys` module in order to gather the values needed.

<h3>Usage:</h3>

~~~
usage: scout-cli [-h] [--getArp <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getSpeed <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getName <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getUsers <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getMac <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getModel <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getSerial <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getLocation <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getIosInfo <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getUptime <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--getClientCount <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--ping <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--runFetcher <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--led <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--changeIp <IP_ADDRESS> <USERNAME> <PASSWORD> <NEW_IP> <SUBNET_MASK>]
                 [--changeName <IP_ADDRESS> <USERNAME> <PASSWORD> <NEW_AP_NAME>]
                 [--createSsid24 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <WPA2_PASSWORD> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID>]
                 [--createSsid5 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <WPA2_PASSWORD> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID>]
                 [--createSsidRadius24 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID> <RADIUS_IP> <SHARED_SECRET> <AUTH_PORT> <ACCT_PORT> <RADIUS_TIMEOUT> <RADIUS_GROUP> <METHOD_LIST>]
                 [--createSsidRadius5 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID> <RADIUS_IP> <SHARED_SECRET> <AUTH_PORT> <ACCT_PORT> <RADIUS_TIMEOUT> <RADIUS_GROUP> <METHOD_LIST>]
                 [--deleteSsid24 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <RADIO_ID> <INTERFACE_ID>]
                 [--deleteSsid5 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <RADIO_ID> <INTERFACE_ID>]
                 [--enableHttp <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--disableHttp <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--enableSnmp <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--disableSnmp <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--wr <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--erase <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--reboot <IP_ADDRESS> <USERNAME> <PASSWORD>]
                 [--tftpBackup <IP_ADDRESS> <USERNAME> <PASSWORD> <TFTP_SERVER>]

scout-cli: CLI for Managing Cisco Autonomous Access Points

optional arguments:
  -h, --help            show this help message and exit
  --getArp <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Print an access point's ARP table
  --getSpeed <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's link speed
  --getName <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's hostname
  --getUsers <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show connected users
  --getMac <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's MAC address
  --getModel <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's model information
  --getSerial <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's serial number
  --getLocation <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's location
  --getIosInfo <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's IOS information
  --getUptime <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's system uptime
  --getClientCount <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Show access point's client count
  --ping <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Ping an access point via SSH
  --runFetcher <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Fetch access point information via fetcher()
  --led <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Trigger LED function for 30 seconds
  --changeIp <IP_ADDRESS> <USERNAME> <PASSWORD> <NEW_IP> <SUBNET_MASK>
                        Change an access point's IP address
  --changeName <IP_ADDRESS> <USERNAME> <PASSWORD> <NEW_AP_NAME>
                        Change an access point's hostname
  --createSsid24 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <WPA2_PASSWORD> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID>
                        Create a 2.4GHz SSID
  --createSsid5 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <WPA2_PASSWORD> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID>
                        Create a 5GHz SSID
  --createSsidRadius24 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID> <RADIUS_IP> <SHARED_SECRET> <AUTH_PORT> <ACCT_PORT> <RADIUS_TIMEOUT> <RADIUS_GROUP> <METHOD_LIST>
                        Create a 2.4GHz 802.1x SSID
  --createSsidRadius5 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <BRIDGE_GROUP_ID> <RADIO_ID> <INTERFACE_ID> <RADIUS_IP> <SHARED_SECRET> <AUTH_PORT> <ACCT_PORT> <RADIUS_TIMEOUT> <RADIUS_GROUP> <METHOD_LIST>
                        Create a 5GHz 802.1x SSID
  --deleteSsid24 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <RADIO_ID> <INTERFACE_ID>
                        Delete a 2.4GHz SSID
  --deleteSsid5 <IP_ADDRESS> <USERNAME> <PASSWORD> <SSID_NAME> <VLAN_ID> <RADIO_ID> <INTERFACE_ID>
                        Delete a 5GHz SSID
  --enableHttp <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Enable an access point's HTTP server
  --disableHttp <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Disable an access point's HTTP server
  --enableSnmp <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Enable access point's SNMP server
  --disableSnmp <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Disable access point's SNMP server
  --wr <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Write configuration to access point
  --erase <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Erase an access point's configuration
  --reboot <IP_ADDRESS> <USERNAME> <PASSWORD>
                        Reboot an access point
  --tftpBackup <IP_ADDRESS> <USERNAME> <PASSWORD> <TFTP_SERVER>
                        Backup an access point's configuration via TFTP
~~~

Every parameter in `scout-cli` requires three arguments: `ip`, `username`, and `password`.
After providing the connection information, you can add additional values, depending
on the option specified.

<h3>Example</h3>

~~~
scout-cli --getArp <IP_ADDRESS> <USERNAME> <PASSWORD>
~~~

~~~
scout-cli --getArp 192.168.2.100 cisco1 mysecretpass
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.2.1             0   ec1a.5986.2510  ARPA   BVI1
Internet  192.168.2.3             1   7ce9.d306.090c  ARPA   BVI1
Internet  192.168.2.9             -   f866.f292.a65d  ARPA   BVI1
~~~
