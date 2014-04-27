#!/usr/bin/env python

import re

# Packet class
class APRSPacket(object):

  # These data types are taken directly from the APRS spec at http://aprs.org/doc/APRS101.PDF
  # This is not an exhaustive list. These are the most common ones, and were added during
  # testing.
  data_types = {'!' : 'Position without timestamp',
                '_' : 'Weather Report (without position)',
                '@' : 'Position with timestamp (with APRS messaging)',
                '/' : 'Position with timestamp (no APRS messaging)',
                '=' : 'Position without timestamp (with APRS messaging)',
                'T' : 'Telemetry data',
                ';' : 'Object',
                '<' : 'Station Capabilities',
                '>' : 'Status',
                '`' : 'Current Mic-E Data (not used in TM-D700)',
                '?' : 'Query',
                '\'' : 'Old Mic-E Data (but Current data for TM-D700)',
                ':' : 'Message',
                '$' : 'Raw GPS data or Ultimeter 2000',
               }

  def __init__(self):
    # Raw packet
    self._packet = None
    # Station the packet originated from
    self._source = None
    # Destination of the packet
    self._destination = None
    # Packet path
    self._path = None
    # Information field
    self._information = None
    # Data type identifier
    self._data_type = None
    # Latitude
    self._latitude = None
    # Longitude
    self._longitude = None
    # Symbol
    self._symbol = None

    # Parsed, read-only values of the above, populated by parse()
    self._parsed_source = None
    self._parsed_destination = None
    self._parsed_path = None
    self._parsed_information = None

  # packet
  @property
  def packet(self):
    return self._packet

  @packet.setter
  def packet(self, value):
    self._packet = value
    self._parse()

  # source
  @property
  def source(self):
    return self._source

  @source.setter
  def source(self, value):
    self._source = value
    self._build()

  # destination
  @property
  def destination(self):
    return self._destination

  @destination.setter
  def destination(self, value):
    self._destination = value
    self._build()

  @property
  def path(self):
    return self._path

  @path.setter
  def path(self, value):
    self._path = value
    self._build()

  @property
  def information(self):
    return self._information

  @information.setter
  def information(self, value):
    self._information = value
    self._build()

  @property
  def data_type(self):
    return self._data_type

  @data_type.setter
  def data_type(self, value):
    self._data_type = value
    self._build()

  # Read-only attributes
  @property
  def data_type_name(self):
    return data_types.get(self._data_type)

  # reset packet
  def _reset(self):
    self._source = self._parsed_source
    self._destination = self._parsed_destination
    self._path = self._parsed_path
    self._information = self._parsed_information
    self._parse()

  # parse information
  def _parse_information(self):
    # Get the data type
    first_char = self._information[0]

    # Look to see if it is a valid data type.
    if first_char in data_types:
      # Assign it to _data_type
      self._data_type = first_char
    else:
      # No valid data type found so far. However, the spec allows '!' (and
      # *only* '!' to appear anywhere in the first 40 characters of the
      # information field
      if re.search(r"!", data[0:40]):
        self._data_type = "!"
    
  # parse
  def _parse(self):
    # Split packet into segments
    print "Packet: " + self._packet
    packet_segments = re.search(r"([\w\-]+)>([\w\-]+),([\w\-\*\,]+):(.*)$", self._packet)
    # Assign segments to variables
    (self._source, self._destination, self._path, self._information) = packet_segments.groups()
    # Set the read-only parse time versions of the above
    (self._parsed_source, self._parsed_destination, self._parsed_path, self._parsed_information) = packet_segments.groups()

  # build information
  def _build_information(self):
    pass

  # build
  def _build(self):
    if self._source is not None and self._destination is not None and self._path is not None and self._information is not None:
      packet = self._source + ">" + self._destination + "," + self._path + ":" + self._information
      self._packet = packet
