[![Build Status](https://api.travis-ci.com/cardinal-dev/scout.svg?branch=main)](https://travis-ci.com/cardinal-dev/scout)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

<h1>scout</h1>
<h3>Managing Autonomous Cisco APs</h3>

`scout` is the underlying logic that communicates with autonomous Cisco APs via SSH. The main component of `scout`
is `paramiko`. `scout` is built on and requires Python3. `scout` and all other Cardinal components are tested
against Python 3.6, 3.7, and 3.8.

<h3>Example Usage:</h3>

~~~
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from scout import info
>>> users = info.getUsers("192.168.2.5", "Cisco", "Cisco")
>>> print(users)
    Line       User       Host(s)              Idle       Location
*  1 vty 0     Cisco      idle                 00:00:00 test-sys-1

  Interface    User               Mode         Idle     Peer Address
~~~

`scout` is a Python package that contains five modules:

`ssh` builds the `paramiko` client based on information passed into `buildSshClient()`. `buildSshClient()` accepts
three positional arguments: `ip`, `username`, and `password`.

`env` contains the Jinja2 logic for building/running `scout` templates. Currently, all default `scout` templates can
be found in `templates/`. `scout` can read a text file that has one IOS command per line. If desired, 
the user can pass Jinja2 values to the templates in order to build complex command runs.

`info` contains command functions that gather Cisco AP information, much like the commands a sysadmin
would type at the Terminal.

`sys` contains command functions that manipulate system settings.

`ssid` contains command functions that create/delete SSIDs.
