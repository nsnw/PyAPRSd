#!/usr/bin/env python

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import sys, re

# Connector class
class Client:
  class APRSClient(LineReceiver):

    def connectionMade(self):
      #self.sendLine("user " + callsign + " pass " + passcode + " vers PyAPRSd 0.1 filter " + receive_filter)
      pass

    def lineReceived(self, line):
      print line
      pass

    def sendPacket(self, packet):
      pass

  class APRSClientFactory(ClientFactory):
    def __init__(self, protocol):
      self.protocol = protocol

    def clientConnectionFailed(self, connector, reason):
      print 'connection failed:', reason.getErrorMessage()
      reactor.stop()

    def clientConnectionLost(self, connector, reason):
      print 'connection lost:', reason.getErrorMessage()
      reactor.stop()

  class APRSClientException(Exception):
    def __init__(self, value):
      self.value = value
    def __str__(self):
      return repr(self.value)
  
  def tick(self):
    print "tick"

  def connect(self, server, port):
    try:
      factory = self.APRSClientFactory(self.APRSClient)
      print "Hello"
      print factory
      #reactor.connectTCP(server, port, factory)
      lc = LoopingCall(self.tick)
      lc.start(1)
      reactor.run()
    except self.APRSClientException, e:
      print e.value

