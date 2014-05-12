#!/usr/bin/env python

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import sys, re

# Connector class
class Manager:
  def __init__(self, core):
    self.core = core

  class APRSManager(LineReceiver):
    def __init__(self, core, username, password):
      self.core = core
      self.username = username
      self.password = password

      print "Manager with username of ", self.username, " and password of ", self.password
      print "Core is", self.core.version

    def connectionMade(self):
      self.sendLine("PyAPRSd v1.0")
      self.sendLine("Core " + self.core.version)

    def lineReceived(self, line):
      self.sendLine("Got: " + line)
      if line == "stop":
        self.core.stop()
      elif line == "clients":
        for (key, client) in self.core.clients.items():
          self.sendLine(key)
      elif line == "kill":
        self.core.clients.get("vancouver.aprs2.net:14580").disconnect()

  class APRSManagerFactory(Factory):
    def __init__(self, core, protocol, username, password):
      self.core = core
      self.protocol = protocol
      self.username = username
      self.password = password

    def buildProtocol(self, addr):
      return self.protocol(self.core, self.username, self.password)

  def create(self, port, username, password):
    reactor.listenTCP(port, self.APRSManagerFactory(self.core, self.APRSManager, username, password))
