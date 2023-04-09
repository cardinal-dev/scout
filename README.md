[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

<h1>scout</h1>
<h3>Managing Autonomous Cisco APs</h3>

`scout` is the underlying logic that communicates with autonomous Cisco APs via SSH. The main component of `scout`
is `paramiko`. `scout` is built on and requires Python3. `scout` and all other Cardinal components are tested
against Python 3.6, 3.7, and 3.8.

<h2>Deprecation Notice</h2>
Starting April 9th, 2023, Cardinal development will no longer continue. If anyone wants to continue development, please feel free to fork this repo, along with the repo for scout. I'm going to merge all of the latest dependency PRs before archiving. The latest source code is essentially v3.0, with some things missing. Thank you to everyone who contributed over the years! Overall, I think I accomplished my goal of creating an open source Cisco access point controller.

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
