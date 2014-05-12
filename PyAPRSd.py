#!/usr/bin/env python

import sys, re, ConfigParser
import aprs

config = ConfigParser.ConfigParser()
config.read('PyAPRSd.cfg')

#client = aprs.Client()
#client.connect('vancouver.aprs2.net', 14580)
core = aprs.Core()
core.add_client('vancouver.aprs2.net', 14580, 'VE7CXZ', '19134', 'r/48.45/-123.4/20')
core.add_client('noam.aprs2.net', 14580, 'VE7CXZ', '19134', 'r/48.45/-123.4/20')
core.add_manager(54321, "admin", "password")
print "stuff"
core.start()
