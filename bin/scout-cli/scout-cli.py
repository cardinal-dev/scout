#!/usr/bin/env python3

''' scout - Managing Autonomous Cisco APs

MIT License

Copyright © 2019 Cardinal Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import argparse
import sys
import scout.sys
import scout.info
import scout.ssid

parser = argparse.ArgumentParser(description="scout-cli: CLI for Managing Cisco Autonomous Access Points")
parser.add_argument('--getArp', help="Print an access point's ARP table", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getSpeed', help="Show access point's link speed", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getName', help="Show access point's hostname", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getUsers', help="Show connected users", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getMac', help="Show access point's MAC address", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getModel', help="Show access point's model information", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getSerial', help="Show access point's serial number", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getLocation', help="Show access point's location", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getIosInfo', help="Show access point's IOS information", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getUptime', help="Show access point's system uptime", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--getClientCount', help="Show access point's client count", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--ping', help="Ping an access point via SSH", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--runFetcher', help="Fetch access point information via fetcher()", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--led', help="Trigger LED function for 30 seconds", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--changeIp', help="Change an access point's IP address", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<NEW_IP>", "<SUBNET_MASK>"), type=str, nargs=5)
parser.add_argument('--changeName', help="Change an access point's hostname", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<NEW_AP_NAME>"), type=str, nargs=4)
parser.add_argument('--createSsid24', help="Create a 2.4GHz SSID", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<SSID_NAME>", "<WPA2_PASSWORD>", "<VLAN_ID>", "<BRIDGE_GROUP_ID>", "<RADIO_ID>", "<INTERFACE_ID>"), type=str, nargs=9)
parser.add_argument('--createSsid5', help="Create a 5GHz SSID", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<SSID_NAME>", "<WPA2_PASSWORD>", "<VLAN_ID>", "<BRIDGE_GROUP_ID>", "<RADIO_ID>", "<INTERFACE_ID>"), type=str, nargs=9)
parser.add_argument('--createSsidRadius24', help="Create a 2.4GHz 802.1x SSID", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<SSID_NAME>", "<VLAN_ID>", "<BRIDGE_GROUP_ID>", "<RADIO_ID>", "<INTERFACE_ID>", "<RADIUS_IP>", "<SHARED_SECRET>", "<AUTH_PORT>", "<ACCT_PORT>", "<RADIUS_TIMEOUT>", "<RADIUS_GROUP>", "<METHOD_LIST>"), type=str, nargs=15)
parser.add_argument('--createSsidRadius5', help="Create a 5GHz 802.1x SSID", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<SSID_NAME>", "<VLAN_ID>", "<BRIDGE_GROUP_ID>", "<RADIO_ID>", "<INTERFACE_ID>", "<RADIUS_IP>", "<SHARED_SECRET>", "<AUTH_PORT>", "<ACCT_PORT>", "<RADIUS_TIMEOUT>", "<RADIUS_GROUP>", "<METHOD_LIST>"), type=str, nargs=15)
parser.add_argument('--deleteSsid24', help="Delete a 2.4GHz SSID", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<SSID_NAME>", "<VLAN_ID>", "<RADIO_ID>", "<INTERFACE_ID>"), type=str, nargs=7)
parser.add_argument('--deleteSsid5', help="Delete a 5GHz SSID", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<SSID_NAME>", "<VLAN_ID>", "<RADIO_ID>", "<INTERFACE_ID>"), type=str, nargs=7)
parser.add_argument('--enableHttp', help="Enable an access point's HTTP server", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--disableHttp', help="Disable an access point's HTTP server", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--enableSnmp', help="Enable access point's SNMP server", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--disableSnmp', help="Disable access point's SNMP server", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--wr', help="Write configuration to access point", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--erase', help="Erase an access point's configuration", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--reboot', help="Reboot an access point", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>"), type=str, nargs=3)
parser.add_argument('--tftpBackup', help="Backup an access point's configuration via TFTP", metavar=("<IP_ADDRESS>", "<USERNAME>", "<PASSWORD>", "<TFTP_SERVER>"), type=str, nargs=4)

args = parser.parse_args()

def scoutArgs():
    ip = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    return ip, username, password

# scout.info
if args.getArp:
    ip, username, password = scoutArgs()
    getArp = scout.info.getArp(ip=ip, username=username, password=password)
    print(getArp)
elif args.getSpeed:
    ip, username, password = scoutArgs()
    getSpeed = scout.info.getSpeed(ip=ip, username=username, password=password)
    print(getSpeed + 'Mbps')
elif args.getClientCount:
    ip, username, password = scoutArgs()
    countClients = scout.info.getClientCount(ip=ip, username=username, password=password)
    print(countClients)
elif args.getMac:
    ip, username, password = scoutArgs()
    getMacAddr = scout.info.getMac(ip=ip, username=username, password=password)
    print(getMacAddr)
elif args.getModel:
    ip, username, password = scoutArgs()
    getApModel = scout.info.getModel(ip=ip, username=username, password=password)
    print(getApModel)
elif args.getName:
    ip, username, password = scoutArgs()
    getApName = scout.info.getHostname(ip=ip, username=username, password=password)
    print(getApName)
elif args.getSerial:
    ip, username, password = scoutArgs()
    getApSerial = scout.info.getSerial(ip=ip, username=username, password=password)
    print(getApSerial)
elif args.getIosInfo:
    ip, username, password = scoutArgs()
    getApIosInfo = scout.info.getIosInfo(ip=ip, username=username, password=password)
    print(getApIosInfo)
elif args.getLocation:
    ip, username, password = scoutArgs()
    getApLocation = scout.info.getLocation(ip=ip, username=username, password=password)
    print(getApLocation)
elif args.getUptime:
    ip, username, password = scoutArgs()
    getApUptime = scout.info.getUptime(ip=ip, username=username, password=password)
    print(getApUptime)
elif args.getUsers:
    ip, username, password = scoutArgs()
    getApUsers = scout.info.getUsers(ip=ip, username=username, password=password)
    print(getApUsers)
elif args.runFetcher:
    ip, username, password = scoutArgs()
    apInfo = scout.info.fetcher(ip=ip, username=username, password=password)
    print(apInfo)
elif args.ping:
    ip, username, password = scoutArgs()
    apPing = scout.info.ping(ip=ip, username=username, password=password)
    print(apPing)

# scout.sys
elif args.led:
    ip, username, password = scoutArgs()
    scout.sys.scoutLed(ip=ip, username=username, password=password)
elif args.changeIp:
    ip, username, password = scoutArgs()
    newIp = sys.argv[5]
    subnetMask = sys.argv[6]
    scout.sys.scoutChangeIp(ip=ip, username=username, password=password, newIp=newIp, subnetMask=subnetMask)
elif args.disableHttp:
    ip, username, password = scoutArgs()
    scout.sys.scoutDisableHttp(ip=ip, username=username, password=password)
elif args.disableSnmp:
    ip, username, password = scoutArgs()
    scout.sys.scoutDisableSnmp(ip=ip, username=username, password=password)
elif args.enableHttp:
    ip, username, password = scoutArgs()
    scout.sys.scoutEnableHttp(ip=ip, username=username, password=password)
elif args.enableSnmp:
    ip, username, password = scoutArgs()
    snmp = sys.argv[5]
    scout.sys.scoutEnableSnmp(ip=ip, username=username, password=password, snmp=snmp)
elif args.tftpBackup:
    ip, username, password = scoutArgs()
    tftpIp = sys.argv[5]
    tftpBackup = scout.sys.scoutTftpBackup(ip=ip, username=username, password=password, tftpIp=tftpIp)
elif args.wr:
    ip, username, password = scoutArgs()
    scout.sys.scoutDoWr(ip=ip, username=username, password=password)
elif args.erase:
    ip, username, password = scoutArgs()
    scout.sys.scoutWriteDefault(ip=ip, username=username, password=password)
elif args.reboot:
    ip, username, password = scoutArgs()
    scout.sys.scoutDoReboot(ip=ip, username=username, password=password)
elif args.changeName:
    ip, username, password = scoutArgs()
    apName = sys.argv[5]
    scout.sys.scoutChangeName(ip=ip, username=username, password=password, apName=apName)

# scout.ssid
elif args.createSsid24:
    ip, username, password = scoutArgs()
    ssid = sys.argv[5]
    wpa2Pass = sys.argv[6]
    vlan = sys.argv[7]
    bridgeGroup = sys.argv[8]
    radioSub = sys.argv[9]
    gigaSub = sys.argv[10]
    scout.ssid.scoutCreateSsid24(ip=ip, username=username, password=password, ssid=ssid, wpa2Pass=wpa2Pass, vlan=vlan, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub)
elif args.createSsid5:
    ip, username, password = scoutArgs()
    ssid = sys.argv[5]
    wpa2Pass = sys.argv[6]
    vlan = sys.argv[7]
    bridgeGroup = sys.argv[8]
    radioSub = sys.argv[9]
    gigaSub = sys.argv[10]
    scout.ssid.scoutCreateSsid5(ip=ip, username=username, password=password, ssid=ssid, wpa2Pass=wpa2Pass, vlan=vlan, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub)
elif args.createSsidRadius24:
    ip, username, password = scoutArgs()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    bridgeGroup = sys.argv[7]
    radioSub = sys.argv[8]
    gigaSub = sys.argv[9]
    radiusIp = sys.argv[10]
    sharedSecret = sys.argv[11]
    authPort = sys.argv[12]
    acctPort = sys.argv[13]
    radiusTimeout = sys.argv[14]
    radiusGroup = sys.argv[15]
    methodList = sys.argv[16]
    scout.ssid.scoutCreateSsid24Radius(ip=ip, username=username, password=password, ssid=ssid, vlan=vlan, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub, radiusIp=radiusIp, sharedSecret=sharedSecret, authPort=authPort, acctPort=acctPort, radiusTimeout=radiusTimeout, radiusGroup=radiusGroup, methodList=methodList)
elif args.createSsidRadius5:
    ip, username, password = scoutArgs()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    bridgeGroup = sys.argv[7]
    radioSub = sys.argv[8]
    gigaSub = sys.argv[9]
    radiusIp = sys.argv[10]
    sharedSecret = sys.argv[11]
    authPort = sys.argv[12]
    acctPort = sys.argv[13]
    radiusTimeout = sys.argv[14]
    radiusGroup = sys.argv[15]
    methodList = sys.argv[16]
    scout.ssid.scoutCreateSsid5Radius(ip=ip, username=username, password=password, ssid=ssid, vlan=vlan, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub, radiusIp=radiusIp, sharedSecret=sharedSecret, authPort=authPort, acctPort=acctPort, radiusTimeout=radiusTimeout, radiusGroup=radiusGroup, methodList=methodList)
elif args.deleteSsid24:
    ip, username, password = scoutArgs()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    radioSub = sys.argv[7]
    gigaSub = sys.argv[8]
    scout.ssid.scoutDeleteSsid24(ip=ip, username=username, password=password, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
elif args.deleteSsid5:
    ip, username, password = scoutArgs()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    radioSub = sys.argv[7]
    gigaSub = sys.argv[8]
    scout.ssid.scoutDeleteSsid5(ip=ip, username=username, password=password, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
else:
    print("ERROR: Please specify a valid scout-cli command.")
    sys.exit(1)
