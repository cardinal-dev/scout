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

    def __init__(self):

        # Ingest values from config file at SCOUTCONFIG
        scoutConfigFile = os.environ['SCOUTCONFIG']
        scoutConfig = ConfigParser()
        scoutConfig.read("{0}".format(scoutConfigFile))

        self.tunings = {}

        # Establish default behavior. If values are not defined
        # in SCOUTCONFIG, we'll try to handle accordingly.
        if scoutConfig.has_option('scout', 'commandDir'):
            self.tunings['commandDir'] = scoutConfig.get('scout', 'commandDir')
        else:
            self.tunings['commandDir'] = '/opt/scout/templates'

        if scoutConfig.has_option('scout', 'commandDebug'):
            self.tunings['commandDebug'] = scoutConfig.get('scout', 'commandDebug')
        else:
            self.tunings['commandDebug'] = 'off'

        fileLoader = jinja2.FileSystemLoader("{0}".format(self.tunings['commandDir']))
        # See: https://bandit.readthedocs.io/en/latest/plugins/b701_jinja2_autoescape_false.html
        jinjaEnv = jinja2.Environment(loader=fileLoader, autoescape=True)

        # Embed Jinja2 object into tunings dict()
        self.tunings['jinjaEnv'] = jinjaEnv

    def ssh(self, host, username, password, port, **kwargs):
        '''
        Build SSH client using paramiko.
        '''
        # Invoke paramiko to start building SSH client
        scoutSshClient = paramiko.SSHClient()

        scoutSshClient.connect(host, port=port, username=username, password=password, **kwargs)
        return scoutSshClient

    def list(self):
        '''
        Return current configuration of scoutEnv
        '''
        return self.tunings