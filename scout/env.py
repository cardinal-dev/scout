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

import os
import paramiko
import jinja2
from configparser import ConfigParser

class scoutEnv():
    '''
    Object that defines how scout ultimately behaves.
    scoutEnv() will return a dict() with configuration
    options, which will be ingested on execution.
    '''

    def __init__(self, **kwargs):

        # Ingest values from config file at SCOUTCONFIG
        scoutConfigFile = os.environ['SCOUTCONFIG']
        scoutConfig = ConfigParser()
        scoutConfig.read("{0}".format(scoutConfigFile))

        self.tunings = {}

        # By default, let's look at config file at SCOUTCONFIG first
        commandDebug = scoutConfig.get('scout', 'commandDebug')
        commandDir = scoutConfig.get('scout', 'commandDir')

        fileLoader = jinja2.FileSystemLoader("{0}".format(commandDir))
        # autoescape is set to True for security purposes
        jinjaEnv = jinja2.Environment(loader=fileLoader, autoescape=True)

        # Establish default behavior. If values are not defined
        # in SCOUTCONFIG, we'll try to handle accordingly.
        if len(commandDebug) <= 0:
            self.tunings['commandDebug'] = 'off'
        else:
            self.tunings['commandDebug'] = commandDebug

        if len(commandDir) <= 0:
            self.tunings['commandDir'] = '/opt/scout/templates'
        else:
            self.tunings['commandDir'] = commandDir

        # Embed Jinja2 object into tunings dict()
        self.tunings['jinjaEnv'] = jinjaEnv

        # Accommodate for a wide array of key/value pairs
        for d in kwargs.items():
            self.tunings[d[0]] = d[1]

    def ssh(self, ip, username, password, port, **kwargs):
        '''
        Build SSH client using paramiko.
        '''
        # Invoke paramiko to start building SSH client
        scoutSshClient = paramiko.SSHClient()

        # Read in customizations from scout.ini
        scoutSshClient.connect(ip, port=port, username=username, password=password, look_for_keys=False, allow_agent=False)
        return scoutSshClient

    def list(self):
        '''
        Return current configuration of scoutEnv
        '''
        return self.tunings