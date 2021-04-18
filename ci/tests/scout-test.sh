#!/bin/bash

# scout - Managing Autonomous Cisco APs

# MIT License

# Copyright © 2019 Cardinal Contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# REQUIRES: ping, nc, snmpwalk, tftpd-hpa (or TFTP equivalent), sleep

# STATIC VARIABLES

option="$1"

checkConfigFile=$(ls ci.config)

if [ "$checkConfigFile" = "ci.config" ]; then
    . ci.config
else
    apIp="$2"
    apUsername="$3"
    apPassword="$4"
    changeIp="$5"
    subnetMask="$6"
    # CI assumes tftpServer is on the execution machine
    tftpServer="$7"
    radiusServer="$8"
    sharedSecret="$9"
    authPort="$10"
    acctPort="$11"
    radiusTimeout="$12"
fi

# Test scout operations

scoutTestUsage() {
    echo "scout-test: CI testing for Scout"
    echo "Usage:"
    echo "    --help: Display scout-test options."
    echo "    --run-all-tests: Run all tests included in scout-test.sh."
    echo "    --run-test: Run specific test function."
}

testScoutGetArp() {
    # Test --get-arp
    echo "INFO: Running testScoutGetArp()..."
    scout-cli --get-arp "$apIp" "$apUsername" "$apPassword"
    return=$(echo $?)
    if [ "$return" = 0 ]; then
        echo "INFO: testScoutGetArp() test passed!"
        echo "$testGetArp"
    else
        echo "ERROR: testScoutGetArp() test failed!"
        exit 1
    fi
}

testScoutLed() {
    # Test --led
    echo "INFO: Running testScoutLed()..."
    scout-cli --led "$apIp" "$apUsername" "$apPassword"
    return=$(echo $?)
    if [ "$return" = 0 ]; then
        echo "INFO: testScoutLed() test passed!"
        echo "$testLed"
    else
        echo "ERROR: testScoutLed() test failed!"
        exit 1
    fi
}

testScoutChangeIp() {
    # Test --change-ip
    echo "INFO: Running testScoutChangeIp()..."
    scout-cli --change-ip "$apIp" "$apUsername" "$apPassword" "$changeIp" "$subnetMask"
    ping -c 4 "$changeIp"
    pingReturn=$(echo $?)
    scout-cli --change-ip "$changeIp" "$apUsername" "$apPassword" "$apIp" "$subnetMask"
    revertReturn=$(echo $?)
    if [ "$pingReturn" = 0 ] && [ "$revertReturn" = 0 ]; then
        echo "INFO: testScoutChangeIp() test passed!"
    else
        echo "ERROR: testScoutChangeIp() test failed!"
        exit 1
    fi
}

testScoutCreateSsid24() {
    # Test --create-ssid-24
    echo "INFO: Running testScoutCreateSsid24()..."
    scout-cli --create-ssid-24 "$apIp" "$apUsername" "$apPassword" ScoutTest test1234 1 1 1 1
    return=$(echo $?)

    if [ "$return" = 0 ]; then
        sleep 25
        iw dev wlan0 scan | grep ScoutTest
        broadcastTest=$(echo $?)
        if [ "$broadcastTest" = 0 ]; then
            echo "INFO: testScoutCreateSsid24() test passed!"
            scout-cli --delete-ssid-24 "$apIp" "$apUsername" "$apPassword" ScoutTest 1 1 1
        else
            scout-cli --delete-ssid-24 "$apIp" "$apUsername" "$apPassword" ScoutTest 1 1 1
            echo "ERROR: testScoutCreateSsid24() test failed!"
            exit 1
        fi
    else
        echo "ERROR: testScoutCreateSsid24() test failed!"
        exit 1
    fi
}

testScoutCreateSsid5() {
    # Test --create-ssid-5
    echo "INFO: Running testScoutCreateSsid5()..."
    scout-cli --create-ssid-5 "$apIp" "$apUsername" "$apPassword" ScoutTest5 test1234 1 1 1 1
    return=$(echo $?)

    if [ "$return" = 0 ]; then
        sleep 25
        iw dev wlan0 scan | grep ScoutTest5
        broadcastTest=$(echo $?)
        if [ "$broadcastTest" = 0 ]; then
            echo "INFO: testScoutCreateSsid5() test passed!"
            scout-cli --delete-ssid-5 "$apIp" "$apUsername" "$apPassword" ScoutTest5 1 1 1
        else
            scout-cli --delete-ssid-5 "$apIp" "$apUsername" "$apPassword" ScoutTest5 1 1 1
            echo "ERROR: testScoutCreateSsid5() test failed!"
            exit 1
        fi
    else
        echo "ERROR: testScoutCreateSsid5() test failed!"
        exit 1
    fi
}

testScoutCreateSsid24Radius() {
    # Test --create-ssid-radius-24
    echo "INFO: Running testScoutCreateSsid24Radius()..."
    scout-cli --create-ssid-radius-24 "$apIp" "$apUsername" "$apPassword" ScoutTestRadius 1 1 1 1 "$radiusServer" "$sharedSecret" "$authPort" "$acctPort" "$radiusTimeout" EAP_GRP EAP_MTD
    return=$(echo $?)

    if [ "$return" = 0 ]; then
        sleep 25
        iw dev wlan0 scan | grep ScoutTestRadius
        broadcastTest=$(echo $?)
        if [ "$broadcastTest" = 0 ]; then
            echo "INFO: testScoutCreateSsid24Radius() test passed!"
            scout-cli --delete-ssid-24 "$apIp" "$apUsername" "$apPassword" ScoutTestRadius 1 1 1
        else
            scout-cli --delete-ssid-24 "$apIp" "$apUsername" "$apPassword" ScoutTestRadius 1 1 1
            echo "ERROR: testScoutCreateSsid24Radius() test failed!"
            exit 1
        fi
    else
        echo "ERROR: testScoutCreateSsid24Radius() test failed!"
        exit 1
    fi
}

testScoutCreateSsid5Radius() {
    # Test --create-ssid-radius-5
    echo "INFO: Running testScoutCreateSsid5Radius()..."
    scout-cli --create-ssid-radius-5 "$apIp" "$apUsername" "$apPassword" ScoutTestRadius5 1 1 1 1 "$radiusServer" "$sharedSecret" "$authPort" "$acctPort" "$radiusTimeout" EAP_GRP EAP_MTD
    return=$(echo $?)

    if [ "$return" = 0 ]; then
        sleep 25
        iw dev wlan0 scan | grep ScoutTestRadius5
        broadcastTest=$(echo $?)
        if [ "$broadcastTest" = 0 ]; then
            echo "INFO: testScoutCreateSsid5Radius() test passed!"
            scout-cli --delete-ssid-5 "$apIp" "$apUsername" "$apPassword" ScoutTestRadius5 1 1 1
        else
            scout-cli --delete-ssid-5 "$apIp" "$apUsername" "$apPassword" ScoutTestRadius5 1 1 1
            echo "ERROR: testScoutCreateSsid5Radius() test failed!"
            exit 1
        fi
    else
        echo "ERROR: testScoutCreateSsid5Radius() test failed!"
        exit 1
    fi
}

testScoutHttp() {
    # Test --disable-http
    echo "INFO: Running testScoutHttp()..."
    scout-cli --enable-http "$apIp" "$apUsername" "$apPassword"
    testEnableHttp=$(nc -vz "$apIp" 80)
    enableHttpRc=$(echo $?)
    if [ "$enableHttpRc" = 0 ]; then
        echo "INFO: --enable-http test passed!"
        scout-cli --disable-http "$apIp" "$apUsername" "$apPassword"
        testDisableHttp=$(nc -vz "$apIp" 80)
        disableHttpRc=$(echo $?)
        if [ "$disableHttpRc" = 1 ]; then
            echo "INFO: --disable-http test passed!"
        fi

        if [ "$enableHttpRc" = 0 ] && [ "$disableHttpRc" = 1 ]; then
            echo "INFO: testScoutHttp() test passed!"
        else
            echo "ERROR: testScoutHttp() test failed!"
            exit 1
        fi

    fi
}

testScoutSnmp() {
    # Test --disable-snmp
    echo "INFO: Running testScoutSnmp()..."
    scout-cli --enable-snmp "$apIp" "$apUsername" "$apPassword" public
    snmpwalk -v2c -c public "$apIp"
    enableSnmpRc=$(echo $?)
    if [ "$enableSnmpRc" = 0 ]; then
        echo "INFO: --enable-snmp test passed!"
        scout-cli --disable-snmp "$apIp" "$apUsername" "$apPassword"
        snmpwalk -v2c -c public "$apIp"
        disableSnmpRc=$(echo $?)
        if [ "$disableSnmpRc" = 1 ]; then
            echo "INFO: --disable-snmp test passed!"
        fi

        if [ "$enableSnmpRc" = 0 ] && [ "$disableSnmpRc" = 1 ]; then
            echo "INFO: testScoutSnmp() test passed!"
        else
            echo "ERROR: testScoutSnmp() test failed!"
            exit 1
        fi

    fi
}

testScoutGetSpeed() {
    # Test --get-speed
    echo "INFO: Running testScoutGetSpeed()..."
    scout-cli --get-speed "$apIp" "$apUsername" "$apPassword"
    getSpeedRc=$(echo $?)
    if [ "$getSpeedRc" = 0 ]; then
        echo "INFO: --get-speed test passed!"
    else
        echo "INFO: --get-speed test failed!"
        exit 1
    fi
}

testScoutTftpBackup() {
    # Test --tftp-backup
    echo "INFO: Running testScoutTftpBackup()..."
    apName=$(scout-cli --get-name "$apIp" "$apUsername" "$apPassword")
    scout-cli --tftp-backup "$apIp" "$apUsername" "$apPassword" "$tftpServer"
    checkTftpBackup=$(ls -lah /var/lib/tftpboot/*-confg | grep --ignore-case "$apName")
    tftpBackupRc=$(echo $?)
    if [ "$tftpBackupRc" = 0 ]; then
        echo "INFO: --tftp-backup test passed!"
    else
        echo "INFO: --tftp-backup test failed!"
        exit 1
    fi
}

testScoutWr() {
    # Test --wr
    echo "INFO: Running testScoutWr()..."
    scout-cli --wr "$apIp" "$apUsername" "$apPassword"
    doWrRc=$(echo $?)
    if [ "$doWrRc" = 0 ]; then
        echo "INFO: --wr test passed!"
    else
        echo "INFO: --wr test failed!"
        exit 1
    fi
}

testScoutCountClients() {
    # Test --count-clients
    echo "INFO: Running testScoutCountClients()..."
    scout-cli --count-clients "$apIp" "$apUsername" "$apPassword"
    countClientsRc=$(echo $?)
    if [ "$countClientsRc" = 0 ]; then
        echo "INFO: --count-clients test passed!"
    else
        echo "INFO: --count-clients test failed!"
        exit 1
    fi
}

testScoutGetName() {
    # Test --get-name
    echo "INFO: Running testScoutGetName()..."
    scout-cli --get-name "$apIp" "$apUsername" "$apPassword"
    getNameRc=$(echo $?)
    if [ "$getNameRc" = 0 ]; then
        echo "INFO: --get-name test passed!"
    else
        echo "INFO: --get-name test failed!"
        exit 1
    fi
}

testScoutGetUsers() {
    # Test --get-users
    echo "INFO: Running testScoutGetUsers()..."
    scout-cli --get-users "$apIp" "$apUsername" "$apPassword"
    getUsersRc=$(echo $?)
    if [ "$getUsersRc" = 0 ]; then
        echo "INFO: --get-users test passed!"
    else
        echo "INFO: --get-users test failed!"
        exit 1
    fi
}

testScoutGetMac() {
    # Test --get-mac
    echo "INFO: Running testScoutGetMac()..."
    scout-cli --get-mac "$apIp" "$apUsername" "$apPassword"
    getMacRc=$(echo $?)
    if [ "$getMacRc" = 0 ]; then
        echo "INFO: --get-mac test passed!"
    else
        echo "INFO: --get-mac test failed!"
        exit 1
    fi
}

testScoutGetModel() {
    # Test --get-model
    echo "INFO: Running testScoutGetModel()..."
    scout-cli --get-model "$apIp" "$apUsername" "$apPassword"
    getModelRc=$(echo $?)
    if [ "$getModelRc" = 0 ]; then
        echo "INFO: --get-model test passed!"
    else
        echo "INFO: --get-model test failed!"
        exit 1
    fi
}

testScoutGetSerial() {
    # Test --get-serial
    echo "INFO: Running testScoutGetSerial()..."
    scout-cli --get-serial "$apIp" "$apUsername" "$apPassword"
    getSerialRc=$(echo $?)
    if [ "$getSerialRc" = 0 ]; then
        echo "INFO: --get-serial test passed!"
    else
        echo "INFO: --get-serial test failed!"
        exit 1
    fi
}

testScoutGetLocation() {
    # Test --get-location
    echo "INFO: Running testScoutGetLocation()..."
    scout-cli --get-location "$apIp" "$apUsername" "$apPassword"
    getLocationRc=$(echo $?)
    if [ "$getLocationRc" = 0 ]; then
        echo "INFO: --get-location test passed!"
    else
        echo "INFO: --get-location test failed!"
        exit 1
    fi
}

testScoutGetIosInfo() {
    # Test --get-ios-info
    echo "INFO: Running testScoutIosInfo()..."
    scout-cli --get-ios-info "$apIp" "$apUsername" "$apPassword"
    getIosInfoRc=$(echo $?)
    if [ "$getIosInfoRc" = 0 ]; then
        echo "INFO: --get-ios-info test passed!"
    else
        echo "INFO: --get-ios-info test failed!"
        exit 1
    fi
}

testScoutGetUptime() {
    # Test --get-uptime
    echo "INFO: Running testScoutGetUptime()..."
    scout-cli --get-uptime "$apIp" "$apUsername" "$apPassword"
    getUptimeRc=$(echo $?)
    if [ "$getUptimeRc" = 0 ]; then
        echo "INFO: --get-uptime test passed!"
    else
        echo "INFO: --get-uptime test failed!"
        exit 1
    fi
}

testScoutReboot() {
    # Test --reboot
    echo "INFO: Running testScoutReboot()..."
    scout-cli --reboot "$apIp" "$apUsername" "$apPassword"
    sleep 300
    scout-cli --ping "$apIp" "$apUsername" "$apPassword"
    rebootRc=$(echo $?)
    if [ "$rebootRc" = 0 ]; then
        echo "INFO: --reboot test passed!"
    else
        echo "INFO: --reboot test failed!"
        exit 1
    fi
}

testScoutChangeName() {
    # Test --change-name
    echo "INFO: Running testScoutChangeName()..."
    oldHostname=$(scout-cli --get-name "$apIp" "$apUsername" "$apPassword")
    scout-cli --change-name "$apIp" "$apUsername" "$apPassword" scoutTest
    newHostname=$(scout-cli --get-name "$apIp" "$apUsername" "$apPassword")
    if [ "$newHostname" = "scoutTest" ]; then
        echo "INFO: --change-name test passed!"
    else
        echo "INFO: --change-name test failed!"
        exit 1
    fi
    scout-cli --change-name "$apIp" "$apUsername" "$apPassword" "$oldHostname"
}

testScoutRunFetcher() {
    # Test --run-fetcher
    echo "INFO: Running testScoutRunFetcher()..."
    for i in {1..5}; do
        scout-cli --run-fetcher "$apIp" "$apUsername" "$apPassword"
        fetcherRc=$(echo $?)
        if [ "$fetcherRc" = 0 ]; then
            echo "INFO: --run-fetcher test passed!"
        else
            echo "INFO: --run-fetcher test failed!"
            exit 1
        fi;
    done
}

testScoutPing() {
    # Test --ping
    echo "INFO: Running testScoutPing()..."
    scout-cli --ping "$apIp" "$apUsername" "$apPassword"
    pingRc=$(echo $?)
    if [ "$pingRc" = 0 ]; then
        echo "INFO: --ping test passed!"
    else
        echo "INFO: --ping test failed!"
        exit 1
    fi
}

if [ "$option" == "--help" ]; then
    scoutTestUsage
elif [ "$option" == "--run-all-tests" ]; then
    testScoutGetArp
    testScoutLed
    testScoutChangeIp
    testScoutCreateSsid24
    testScoutCreateSsid5
    testScoutCreateSsid24Radius
    testScoutCreateSsid5Radius
    testScoutHttp
    testScoutSnmp
    testScoutGetSpeed
    testScoutTftpBackup
    testScoutWr
    testScoutCountClients
    testScoutGetName
    testScoutGetUsers
    testScoutGetMac
    testScoutGetModel
    testScoutGetSerial
    testScoutGetLocation
    testScoutGetIosInfo
    testScoutGetUptime
    testScoutReboot
    testScoutChangeName
    testScoutRunFetcher
    testScoutPing
    echo "ALL TESTS PASSED"
elif [ "$option" == "--run-test" ]; then
    test="$2"
    apIp="$3"
    apUsername="$4"
    apPassword="$5"
    "$2"
else
    echo "ERROR: Please specify a valid option for scout-test."
    exit 1
fi
