#!/usr/bin/env python

import sys
sys.path.append('../APRS')
from APRS import APRSPacket

packet = APRSPacket()

raw_packet = "VE7CXZ-10>APU25N,TCPIP*:=4826.48NS12331.90W#Langford Digi - http://digi.ve7cxz.net/"
packet.packet = raw_packet
print "Input packet: " + packet.packet
print "-----------------"
print "Source     : " + packet.source
print "Destination: " + packet.destination
print "Path       : " + packet.path
print "Information: " + packet.information
print "Type       : " + packet.data_type + " (" + packet.data_type_name + ")"
print "Position   : " + packet.latitude + ", " + packet.longitude
print "Symbol     : " + packet.symbol
print "-----------------"
print ""
print "Modifying packet..."
packet.source = "M0VKG-9"
packet.destination = "APK102"
packet.path = "WIDE1-1"
print packet.packet

raw_packet = "VE7CXZ-10>APU25N,TCPIP*:/092345z4903.50N/07201.75W>Test1234"
packet.packet = raw_packet
print "Input packet: " + packet.packet
print "-----------------"
print "Source     : " + packet.source
print "Destination: " + packet.destination
print "Path       : " + packet.path
print "Information: " + packet.information
print "Type       : " + packet.data_type + " (" + packet.data_type_name + ")"
print "Position   : " + packet.latitude + ", " + packet.longitude
print "Symbol     : " + packet.symbol
print "Date       : " + packet.date
print "Date type  : " + packet.date_type + " (" + packet.date_type_name + ")"
print "-----------------"
print ""
print "Modifying packet..."
packet.source = "M0VKG-9"
packet.destination = "APK102"
packet.path = "WIDE1-1"
print packet.packet

new_packet = APRSPacket()
new_packet.source = "VE7QQQ-1"
print new_packet.packet
new_packet.destination = "APU25N"
print new_packet.packet
new_packet.path = "WIDE1-1,WIDE2-1"
print new_packet.packet
new_packet.information = "=48  .  NT123  .  W#Test APRS message"
print new_packet.packet
