#!/usr/bin/env

from twisted.internet import reactor
import aprs

import sys, re

class Core:
  def __init__(self):
    self.version = "PyAPRSd (aprs::core v1.0)"
    self.clients = {}
    self.managers = {}

  def add_client(self, server, port, callsign, passcode, receive_filter):
    client_name = server + ":" + str(port)
    client = aprs.Client(self, client_name)
    self.clients[client_name] = client
    client.connect(server, port, callsign, passcode, receive_filter)

  def add_manager(self, port, username, password):
    manager = aprs.Manager(self)
    manager.create(port, username, password)
    
  def start(self):
    reactor.run()

  def stop(self):
    reactor.stop()
