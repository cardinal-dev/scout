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

import sys
import scout.sys
import scout.info
import scout.ssid

# SCOUT USAGE

def scoutUsage():
    print("scout-cli: Cardinal CLI for Managing Cisco Access Points")
    print("Usage:")
    print("   scout-cli --get-arp: print access point ARP table")
    print("   scout-cli --led: trigger LED function for 30 seconds")
    print("   scout-cli --change-ip: change access point IP")
    print("   scout-cli --create-ssid-24: create a 2.4GHz SSID")
    print("   scout-cli --create-ssid-5: create a 5GHz SSID")
    print("   scout-cli --create-ssid-radius-24: create a 2.4GHz RADIUS SSID")
    print("   scout-cli --create-ssid-radius-5: create a 5GHz RADIUS SSID")
    print("   scout-cli --delete-ssid-24: delete a 2.4GHz SSID/RADIUS SSID")
    print("   scout-cli --delete-ssid-5: delete a 5GHz SSID/RADIUS SSID")
    print("   scout-cli --disable-http: disable access point HTTP server")
    print("   scout-cli --disable-snmp: disable access point SNMP function")
    print("   scout-cli --enable-http: enable access point HTTP function")
    print("   scout-cli --enable-snmp: enable access point SNMP function")
    print("   scout-cli --get-speed: show access point link speed")
    print("   scout-cli --tftp-backup: backup access point config via TFTP")
    print("   scout-cli --wr: write configuration to access point")
    print("   scout-cli --erase: erase configuration on access point")
    print("   scout-cli --count-clients: fetch client associations on access point")
    print("   scout-cli --get-name: fetch access point hostname")
    print("   scout-cli --get-users: fetch access point users")
    print("   scout-cli --get-mac: fetch access point MAC address")
    print("   scout-cli --get-model: fetch access point model info")
    print("   scout-cli --get-serial: fetch access point serial number")
    print("   scout-cli --get-location: fetch access point location")
    print("   scout-cli --get-ios-info: fetch access point IOS info")
    print("   scout-cli --get-uptime: fetch access point uptime info")
    print("   scout-cli --reboot: reboot access point")
    print("   scout-cli --change-name: change access point hostname")
    print("   scout-cli --run-fetcher: run scoutFetcher() from scout-cli")
    print("   scout-cli --ping: ping an AP via SSH")


# Let's start handling the logic for scout-cli

if len(sys.argv) > 1:
    scoutCommand = sys.argv[1]

    def scoutArgs():
        ip = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
        return ip, username, password

    # scout.info
    if scoutCommand == "--help":
        scoutUsage()
    elif scoutCommand == "--get-arp":
        ip, username, password = scoutArgs()
        getArp = scout.info.scoutGetArp(ip=ip, username=username, password=password)
        print(getArp)
    elif scoutCommand == "--get-speed":
        ip, username, password = scoutArgs()
        getSpeed = scout.info.scoutGetSpeed(ip=ip, username=username, password=password)
        print(getSpeed + 'Mbps')
    elif scoutCommand == "--count-clients":
        ip, username, password = scoutArgs()
        countClients = scout.info.scoutCountClients(ip=ip, username=username, password=password)
        print(countClients)
    elif scoutCommand == "--get-mac":
        ip, username, password = scoutArgs()
        getMacAddr = scout.info.scoutGetMac(ip=ip, username=username, password=password)
        print(getMacAddr)
    elif scoutCommand == "--get-model":
        ip, username, password = scoutArgs()
        getApModel = scout.info.scoutGetModel(ip=ip, username=username, password=password)
        print(getApModel)
    elif scoutCommand == "--get-name":
        ip, username, password = scoutArgs()
        getApName = scout.info.scoutGetHostname(ip=ip, username=username, password=password)
        print(getApName)
    elif scoutCommand == "--get-serial":
        ip, username, password = scoutArgs()
        getApSerial = scout.info.scoutGetSerial(ip=ip, username=username, password=password)
        print(getApSerial)
    elif scoutCommand == "--get-ios-info":
        ip, username, password = scoutArgs()
        getApIosInfo = scout.info.scoutGetIosInfo(ip=ip, username=username, password=password)
        print(getApIosInfo)
    elif scoutCommand == "--get-location":
        ip, username, password = scoutArgs()
        getApLocation = scout.info.scoutGetLocation(ip=ip, username=username, password=password)
        print(getApLocation)
    elif scoutCommand == "--get-uptime":
        ip, username, password = scoutArgs()
        getApUptime = scout.info.scoutGetUptime(ip=ip, username=username, password=password)
        print(getApUptime)
    elif scoutCommand == "--get-users":
        ip, username, password = scoutArgs()
        getApUsers = scout.info.scoutGetUsers(ip=ip, username=username, password=password)
        print(getApUsers)
    elif scoutCommand == "--run-fetcher":
        ip, username, password = scoutArgs()
        apInfo = scout.info.scoutFetcher(ip=ip, username=username, password=password)
        print(apInfo)
    elif scoutCommand == "--ping":
        ip, username, password = scoutArgs()
        apPing = scout.info.scoutPing(ip=ip, username=username, password=password)
        print(apPing)

    # scout.sys
    elif scoutCommand == "--led":
        ip, username, password = scoutArgs()
        scout.sys.scoutLed(ip=ip, username=username, password=password)
    elif scoutCommand == "--change-ip":
        ip, username, password = scoutArgs()
        newIp = sys.argv[5]
        subnetMask = sys.argv[6]
        scout.sys.scoutChangeIp(ip=ip, username=username, password=password, newIp=newIp, subnetMask=subnetMask)
    elif scoutCommand == "--disable-http":
        ip, username, password = scoutArgs()
        scout.sys.scoutDisableHttp(ip=ip, username=username, password=password)
    elif scoutCommand == "--disable-snmp":
        ip, username, password = scoutArgs()
        scout.sys.scoutDisableSnmp(ip=ip, username=username, password=password)
    elif scoutCommand == "--enable-http":
        ip, username, password = scoutArgs()
        scout.sys.scoutEnableHttp(ip=ip, username=username, password=password)
    elif scoutCommand == "--enable-snmp":
        ip, username, password = scoutArgs()
        snmp = sys.argv[5]
        scout.sys.scoutEnableSnmp(ip=ip, username=username, password=password, snmp=snmp)
    elif scoutCommand == "--tftp-backup":
        ip, username, password = scoutArgs()
        tftpIp = sys.argv[5]
        tftpBackup = scout.sys.scoutTftpBackup(ip=ip, username=username, password=password, tftpIp=tftpIp)
    elif scoutCommand == "--wr":
        ip, username, password = scoutArgs()
        scout.sys.scoutDoWr(ip=ip, username=username, password=password)
    elif scoutCommand == "--erase":
        ip, username, password = scoutArgs()
        scout.sys.scoutWriteDefault(ip=ip, username=username, password=password)
    elif scoutCommand == "--reboot":
        ip, username, password = scoutArgs()
        scout.sys.scoutDoReboot(ip=ip, username=username, password=password)
    elif scoutCommand == "--change-name":
        ip, username, password = scoutArgs()
        apName = sys.argv[5]
        scout.sys.scoutChangeName(ip=ip, username=username, password=password, apName=apName)

    # scout.ssid
    elif scoutCommand == "--create-ssid-24":
        ip, username, password = scoutArgs()
        ssid = sys.argv[5]
        wpa2Pass = sys.argv[6]
        vlan = sys.argv[7]
        bridgeGroup = sys.argv[8]
        radioSub = sys.argv[9]
        gigaSub = sys.argv[10]
        scout.ssid.scoutCreateSsid24(ip=ip, username=username, password=password, ssid=ssid, wpa2Pass=wpa2Pass, vlan=vlan, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub)
    elif scoutCommand == "--create-ssid-5":
        ip, username, password = scoutArgs()
        ssid = sys.argv[5]
        wpa2Pass = sys.argv[6]
        vlan = sys.argv[7]
        bridgeGroup = sys.argv[8]
        radioSub = sys.argv[9]
        gigaSub = sys.argv[10]
        scout.ssid.scoutCreateSsid5(ip=ip, username=username, password=password, ssid=ssid, wpa2Pass=wpa2Pass, vlan=vlan, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub)
    elif scoutCommand == "--create-ssid-radius-24":
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
    elif scoutCommand == "--create-ssid-radius-5":
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
    elif scoutCommand == "--delete-ssid-24":
        ip, username, password = scoutArgs()
        ssid = sys.argv[5]
        vlan = sys.argv[6]
        radioSub = sys.argv[7]
        gigaSub = sys.argv[8]
        scout.ssid.scoutDeleteSsid24(ip=ip, username=username, password=password, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
    elif scoutCommand == "--delete-ssid-5":
        ip, username, password = scoutArgs()
        ssid = sys.argv[5]
        vlan = sys.argv[6]
        radioSub = sys.argv[7]
        gigaSub = sys.argv[8]
        scout.ssid.scoutDeleteSsid5(ip=ip, username=username, password=password, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
    else:
        print("ERROR: Please specify a valid scout-cli command.")
        sys.exit(1)

else:
    print("ERROR: No valid options detected. Please use --help for a list of valid options.")
