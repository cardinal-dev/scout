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

import re
import scout.ssh
import scout.env
import time

def getArp(ip, username, password):
    '''
    Function that opens a SSH connection to the AP
    and runs show ip arp to gather ARP table.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip,username=username,password=password)
    stdin, stdout, stderr = scoutSshClient.exec_command("show ip arp\n")
    sshOut = stdout.read()
    getArpTable = sshOut.decode('ascii').strip("\n").lstrip()
    scoutSshClient.close()
    return getArpTable

def getSpeed(ip, username, password):
    '''
    Function that reports speed of Gi0/0 in Mbps.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    stdin, stdout, stderr = scoutSshClient.exec_command("sho int gi0\n")
    sshOut = stdout.read()
    sshBandwidth = sshOut.decode('ascii').strip("\n").split(",")
    getBandwidth = sshBandwidth[9].strip("Mbps")
    scoutSshClient.close()
    return getBandwidth

def getMac(ip, username, password):
    '''
    Function that reports back the MAC address of AP.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    macAddrRegex = re.compile(r'\w\w\w\w.\w\w\w\w.\w\w\w\w')
    stdin, stdout, stderr = scoutSshClient.exec_command("show int gi0\n")
    sshOut = stdout.read()
    intList = sshOut.decode('ascii').strip("\n").split(",")
    getMac = macAddrRegex.search(intList[2]).group(0)
    scoutSshClient.close()
    return getMac

def getClientCount(ip, username, password):
    '''
    Function that reports the number of active clients on
    AP via show dot11 associations.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    stdin, stdout, stderr = scoutSshClient.exec_command("show dot11 associations\n")
    sshOut = stdout.read()
    scoutSshClient.close()
    countClient = sshOut.decode('ascii').strip("\n")
    macAddrRegex = re.compile(r'\w\w\w\w\.\w\w\w\w\.\w\w\w\w')
    searchMacAddr = macAddrRegex.findall(countClient)
    totalClients = len(searchMacAddr)
    return totalClients

def getModel(ip, username, password):
    '''
    Function that reports the model ID of AP.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    stdin, stdout, stderr = scoutSshClient.exec_command("show version\n")
    sshOut = stdout.read()
    getModelString = sshOut.decode('ascii').strip("\n")
    apModelRegex = re.compile(r'\w\w\w\-\w\w\w\w\w\w\w\w\-\w-\w\w')
    getApModel = apModelRegex.search(getModelString).group(0)
    scoutSshClient.close()
    return getApModel

def getHostname(ip, username, password):
    '''
    Function that retrieves AP hostname via show version.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    jinjaEnv = scout.env.scoutJinjaEnv()
    cmdTemplate = jinjaEnv.get_template("scout_get_hostname")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSshClient.invoke_shell()
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    getHostname = channel.recv(65535).decode('ascii').strip("\n").strip(">").lstrip()
    scoutSshClient.close()
    return getHostname

def getLocation(ip, username, password):
    '''
    Function that retrieves AP location via show snmp location.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    jinjaEnv = scout.env.scoutJinjaEnv()
    cmdTemplate = jinjaEnv.get_template("scout_get_location")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSshClient.invoke_shell()
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    if channel.recv_ready():
        sshReturn = channel.recv(65535)
        location = sshReturn.decode('ascii').splitlines()
    scoutSshClient.close()
    return location[4]

def getUsers(ip, username, password):
    '''
    Function that retrieves AP users via show users.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    jinjaEnv = scout.env.scoutJinjaEnv()
    cmdTemplate = jinjaEnv.get_template("scout_get_users")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSshClient.invoke_shell()
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    if channel.recv_ready():
        sshReturn = channel.recv(65535)
        userLines = sshReturn.splitlines()
        scoutSshClient.close()
        getUsers = []
        for line in userLines[4:-1]:
            getUsers.append(line.decode('ascii').strip("\n"))
    return "\n".join(getUsers)

def getSerial(ip, username, password):
    '''
    Function that reports the serial number of AP.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    stdin, stdout, stderr = scoutSshClient.exec_command("show inventory\n")
    sshOut = stdout.read()
    getSerialString = sshOut.decode('ascii').strip("\n")
    apSerialRegex = re.compile(r'\w\w\w\w\w\w\w\w\w\w\w')
    getApSerial = apSerialRegex.search(getSerialString).group(0)
    scoutSshClient.close()
    return getApSerial

def getIosInfo(ip, username, password):
    '''
    Function that retrieves AP IOS info via show version.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    stdin, stdout, stderr = scoutSshClient.exec_command("show version\n")
    sshOut = stdout.read().splitlines()
    getIosInfo = sshOut[0].decode('ascii').strip("\n")
    scoutSshClient.close()
    return getIosInfo

def getUptime(ip, username, password):
    '''
    Function that retrieves AP uptime via show version.
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    stdin, stdout, stderr = scoutSshClient.exec_command("show version\n")
    sshOut = stdout.read().splitlines()
    getApUptime = sshOut[8].decode('ascii').strip("\n")
    scoutSshClient.close()
    return getApUptime

def fetcher(ip, username, password):
    '''
    Function that fetches AP information over single SSH channel
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    jinjaEnv = scout.env.scoutJinjaEnv()
    cmdTemplate = jinjaEnv.get_template("scout_fetcher")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSshClient.invoke_shell()
    sshData = []
    apInfo = []
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.75)
        if channel.recv_ready():
            sshReturn = channel.recv(65535)
            dataLines = sshReturn.decode('ascii')
            sshData.append(dataLines)
    scoutSshClient.close()
    macAddrRegex = re.compile(r'\w\w\w\w.\w\w\w\w.\w\w\w\w')
    apModelRegex = re.compile(r'\w\w\w\-\w\w\w\w\w\w\w\w\-\w-\w\w')
    apSerialRegex = re.compile(r'\w\w\w\w\w\w\w\w\w\w\w')
    apBandwidthRegex = re.compile(r'(1|10|100|1000)(Gbps|Mbps)')
    # Append info to apInfo[]
    apMacAddr = macAddrRegex.search(sshData[4].split(',')[1]).group(0)
    apInfo.append(apMacAddr)
    apBandwidth = apBandwidthRegex.search(sshData[3]).group(0)
    apInfo.append(apBandwidth)
    apIosInfo = sshData[5].replace("\r", '').split("\n")[1]
    apInfo.append(apIosInfo)
    apUptime = sshData[6].replace("\r", '').split("\n")[1]
    apInfo.append(apUptime)
    apSerial = apSerialRegex.search(sshData[7].split("\n")[2]).group(0)
    apInfo.append(apSerial)
    apModel = apModelRegex.search(sshData[7].split("\n")[2]).group(0)
    apInfo.append(apModel)
    calcClientCount = sshData[8].split('\n')[4:]
    apClientCount = len(macAddrRegex.findall(str(calcClientCount)))
    apInfo.append(apClientCount)
    apLocation = sshData[9].replace("\r", '').split("\n")[1]
    apInfo.append(apLocation)
    return apInfo

def ping(ip, username, password):
    '''
    Function that performs a simple SSH session similar to ping
    '''
    scoutSshClient = scout.ssh.buildSshClient(ip=ip, username=username, password=password)
    jinjaEnv = scout.env.scoutJinjaEnv()
    cmdTemplate = jinjaEnv.get_template("scout_ssh_ping")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSshClient.invoke_shell()
    sshData = []
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.75)
        if channel.recv_ready():
            sshReturn = channel.recv(65535)
            dataLines = sshReturn.decode('ascii')
            sshData.append(dataLines)
    scoutSshClient.close()
    apPing = sshData[0].split("\n")[2:3]
    return apPing
