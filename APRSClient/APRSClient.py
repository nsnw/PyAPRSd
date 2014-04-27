#!/usr/bin/env python

import re

# Packet class
class APRSPacket(object):

  def __init__(self):
    # These data types are taken directly from the APRS spec at http://aprs.org/doc/APRS101.PDF
    # This is not an exhaustive list. These are the most common ones, and were added during
    # testing.
    self._data_type_list = {'!' : 'Position without timestamp',
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

    self._date_type_list = {'z' : 'D/H/M format, zulu time',
                            '/' : 'D/H/M format, local time',
                            'h' : 'H/M/S format, zulu time'
                           }

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
    # Comment
    self._comment = None
    # PHG (Power-Height-Gain)
    self._phg = None
    # Data extension
    self._data_extension = None
    # Altitude
    self._altitude = None
    # Date
    self._date = None
    # Date type
    self._date_type = None
    # Month
    self._month = None
    # Day
    self._day = None
    # Hour
    self._hour = None
    # Minute
    self._minute = None
    # Second
    self._second = None

    # Parsed, read-only values of the above, populated by parse()
    self._parsed_source = None
    self._parsed_destination = None
    self._parsed_path = None
    self._parsed_information = None

    # Internal class variables
    # X1J flag
    self._x1j = False

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

  # Path
  @property
  def path(self):
    return self._path

  @path.setter
  def path(self, value):
    self._path = value
    self._build()

  # Information field
  @property
  def information(self):
    return self._information

  @information.setter
  def information(self, value):
    self._information = value
    self._build()

  # Data type (usually first character of the Information field - not always)
  @property
  def data_type(self):
    return self._data_type

  @data_type.setter
  def data_type(self, value):
    self._data_type = value
    self._build()

  # Latitude
  @property
  def latitude(self):
    return self._latitude

  @latitude.setter
  def latitude(self, value):
    self._latitude = value
    self._build()

  # Longitude
  @property
  def longitude(self):
    return self._longitude

  @longitude.setter
  def longitude(self, value):
    self._longitude = value
    self._build()

  # Symbol
  @property
  def symbol(self):
    return self._symbol

  @symbol.setter
  def symbol(self, value):
    self._symbol = value
    self._build()

  # Comment (at the end of the Information field in status packets)
  @property
  def comment(self):
    return self._comment

  @comment.setter
  def comment(self, value):
    self._comment = value
    self._build()

  # Data extension (PHG, course/speed, radio range, etc.)
  @property
  def data_extension(self):
    return self._data_extension

  @data_extension.setter
  def data_extension(self, value):
    self._data_extension = value
    self._build()

  # Altitude
  @property
  def altitude(self):
    return self._altitude

  @altitude.setter
  def altitude(self, value):
    self._altitude = value
    self._build()

  # Power-Height-Gain
  @property
  def phg(self):
    return self._phg

  @phg.setter
  def phg(self, value):
    self._phg = value
    self._build()

  # Raw date
  @property
  def date(self):
    return self._date

  @date.setter
  def date(self, value):
    self._date = value
    self._build()

  # Date type
  @property
  def date_type(self):
    return self._date_type

  @date_type.setter
  def date_type(self, value):
    self._date_type = value
    self._build()

  # Month
  @property
  def month(self):
    return self._month

  @month.setter
  def month(self, value):
    self._month = value
    self._build()

  # Day
  @property
  def day(self):
    return self._day

  @day.setter
  def day(self, value):
    self._day = value
    self._build()

  # Hour
  @property
  def hour(self):
    return self._hour

  @hour.setter
  def hour(self, value):
    self._hour = value
    self._build()

  # Minute
  @property
  def minute(self):
    return self._minute

  @minute.setter
  def minute(self, value):
    self._minute = value
    self._build()

  # Second
  @property
  def second(self):
    return self._second

  @second.setter
  def second(self, value):
    self._second = value
    self._build()

  # Read-only attributes
  # Friendly name for the data type
  @property
  def data_type_name(self):
    return self._data_type_list.get(self._data_type)

  # Friendly name for the date type
  @property
  def date_type_name(self):
    return self._date_type_list.get(self._date_type)

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
    if first_char in self._data_type_list:
      # Assign it to _data_type
      self._data_type = first_char
    else:
      # No valid data type found so far. However, the spec allows '!' (and
      # *only* '!' to appear anywhere in the first 40 characters of the
      # information field
      if re.search(r"!", data[0:40]):
        self._data_type = "!"
        # Set the X1J flag to assist with parsing
        self._x1j = True
      else:
        # Since we don't know the data type, we can't parse the information
        # field any further
        return

    # Parse the information field
    if self._data_type in [ '!', '=' ]:
      # position reports - without timestamps (!, =)
      # Check if the 
      (self._latitude, symbol_table, self._longitude, symbol_code, comment) = re.search(r"^[\!\=]([\d\s\.]+[NS])(\S)([\d\s\.]+[EW])(\S)(.*)$", self._information).groups()
      # Join the two symbol characters together
      self._symbol = symbol_table + symbol_code
    elif self._data_type in [ '/', '@' ]:
      # position reports - with timestamps (/, @)
      (self._date, self._date_type, self._latitude, symbol_table, self._longitude, symbol_code, comment) = re.search(r"^[\/\@](\d{6})([zh\/])([\d\s\.]+[NS])(\S)([\d\s\.]+[EW])(\S)(.*)$", self._information).groups()
      if self._date_type in [ "z", "/" ]:
        self._day = self._date[0:2]
        self._hour = self._date[2:2]
        self._minute = self._date[4:2]
      elif self._date_type == "/":
        self._hour = self._date[0:2]
        self._minute = self._date[2:2]
        self._seconds = self._date[4:2]
      
  # parse
  def _parse(self):
    # Split packet into segments
    print "Packet: " + self._packet
    packet_segments = re.search(r"([\w\-]+)>([\w\-]+),([\w\-\*\,]+):(.*)$", self._packet)
    # Assign segments to variables
    (self._source, self._destination, self._path, self._information) = packet_segments.groups()
    # Set the read-only parse time versions of the above
    (self._parsed_source, self._parsed_destination, self._parsed_path, self._parsed_information) = packet_segments.groups()
    self._parse_information()

  # build information
  def _build_information(self):
    pass

  # build
  def _build(self):
    if self._source is not None and self._destination is not None and self._path is not None and self._information is not None:
      packet = self._source + ">" + self._destination + "," + self._path + ":" + self._information
      self._packet = packet
