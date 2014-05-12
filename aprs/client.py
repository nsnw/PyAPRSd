#!/usr/bin/env python

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import sys, re

# Connector class
class Client:
  def __init__(self, core, name):
    self.version = "PyAPRSd (aprs::client v1.0)"
    self.core = core
    self.connection = None
    self.name = name

  class APRSClient(LineReceiver):
    def __init__(self, client, core, callsign, passcode, receive_filter):
      self.client = client
      self.core = core
      self.callsign = callsign
      self.passcode = passcode
      self.receive_filter = receive_filter
      print self.core.version
      print self.client.version
      print self.client.name

    def connectionMade(self):
      self.sendLine("user " + self.callsign + " pass " + self.passcode + " vers PyAPRSd 0.1 filter " + self.receive_filter)
      pass

    def lineReceived(self, line):
      print line
      pass

    def sendPacket(self, packet):
      pass

  class APRSClientFactory(ClientFactory):
    def __init__(self, client, core, protocol, callsign, passcode, receive_filter):
      self.client = client
      self.core = core
      self.protocol = protocol
      self.callsign = callsign
      self.passcode = passcode
      self.receive_filter = receive_filter

    def clientConnectionFailed(self, connector, reason):
      print 'connection failed:', reason.getErrorMessage()
      self.client.disconnect()

    def clientConnectionLost(self, connector, reason):
      print 'connection lost:', reason.getErrorMessage()
      reactor.stop()

    def buildProtocol(self, addr):
      return self.protocol(self.client, self.core, self.callsign, self.passcode, self.receive_filter)

  class APRSClientException(Exception):
    def __init__(self, value):
      self.value = value
    def __str__(self):
      return repr(self.value)
  
  def tick(self, server):
    pass

  def connect(self, server, port, callsign, passcode, receive_filter):
    try:
      factory = self.APRSClientFactory(self, self.core, self.APRSClient, callsign, passcode, receive_filter)
      self.connection = reactor.connectTCP(server, port, factory)
      lc = LoopingCall(self.tick, server)
      lc.start(1)
    except self.APRSClientException, e:
      print e.value

