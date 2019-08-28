# The MIT License (MIT)
#
# Copyright (c) 2019 Tom Greasley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`ncd_pr33_15`
================================================================================

Driver for the ncd.io PR33-15 4-20ma receiver

* Author(s): Tom Greasley

Implementation Notes
--------------------

**Hardware:**

   `NCD.io PR33-15 <https://store.ncd.io/product/4-channel-i2c-4-20ma-current-receiver-with-i2c-interface/>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards: https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

import sys
from adafruit_bus_device.i2c_device import I2CDevice

#pylint: disable=wrong-import-position
try:
    lib_index = sys.path.index("/lib")  # pylint: disable=invalid-name
    if lib_index < sys.path.index(".frozen"):
        # Prefer frozen modules over those in /lib.
        sys.path.insert(lib_index, ".frozen")
except ValueError:
    # Don't change sys.path if it doesn't contain "lib" or ".frozen".
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/schlafsack/CircuitPython_NCD_PR33_15.git"

DEVICE_ADDRESS = 0x68  # default address of PR33-15 board

GAIN_1X = 0x00
GAIN_2X = 0x01
GAIN_4X = 0x02
GAIN_8X = 0x03

SAMPLE_RATE_12_BIT = 0x00
SAMPLE_RATE_14_BIT = 0x01
SAMPLE_RATE_16_BIT = 0x02

CHANNEL_1 = 0x00
CHANNEL_2 = 0x01
CHANNEL_3 = 0x02
CHANNEL_4 = 0x03

class ConfigBits:

    def __init__(self, num_bits, lowest_bit):
        self.bit_mask = ((1 << num_bits)-1) << lowest_bit
        if self.bit_mask >= 1 << 8:
            raise ValueError("Cannot have more than 8 bits")
        self.lowest_bit = lowest_bit
        self.buffer = bytearray(3)

    def __get__(self, obj, objtype=None):
        with obj.i2c_device as i2c:
            i2c.readinto(self.buffer)
        return (self.buffer[2] & self.bit_mask) >> self.lowest_bit

    def __set__(self, obj, value):
        value <<= self.lowest_bit    # shift the value over to the right spot
        with obj.i2c_device as i2c:
            i2c.readinto(self.buffer)
            reg = self.buffer[2]
            reg &= ~self.bit_mask  # mask off the bits we're about to change
            reg |= value           # then or in our new value
            self.buffer[2] = reg & 0xFF
            i2c.write(self.buffer[2:3])

class Receiver:

    def __init__(self, i2c, range_from = 0, range_to=20, device_address=DEVICE_ADDRESS):
        self.i2c_device = I2CDevice(i2c, device_address)
        self.buffer = bytearray(2)
        self.range_from = range_from
        self.range_to = range_to

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):

        bits_less = int((4-(self.sample_rate/2)))
        resolution = float(self.range_to - self.range_from) / float(65535 >> (bits_less + 1))

        with self.i2c_device as i2c:
            i2c.readinto(self.buffer)

        raw_data = ((self.buffer[0] << 8) + self.buffer[1]) & (65535 >> bits_less)
        if raw_data > (1 << (16-(bits_less+1)))-1:
            raw_data -= ((1 << (16-(2+2)))-1)
        return float(raw_data) * float(resolution)


    # configuration properties
    gain = ConfigBits(2, 0)  # 2 bits: bits 0 & 1
    sample_rate = ConfigBits(2, 2)  # 2 bits: bits 2 & 3
    continuous = ConfigBits(1, 4)  # 1 bit: bit 4
    channel = ConfigBits(2, 5)  # 2 bits: bit 5 & 6
    ready = ConfigBits(1, 7)  # 1 bit: bit 7

