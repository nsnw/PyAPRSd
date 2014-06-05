#!/usr/bin/env python

import sys, re, ConfigParser
import aprs

config = ConfigParser.ConfigParser()
config.read('PyAPRSd.cfg')

#client = aprs.Client()
#client.connect('vancouver.aprs2.net', 14580)
core = aprs.Core()
core.add_manager(54321, "admin", "password")
core.start()
