#!/usr/bin/env python3

#   floatdata.py
#   Copyright (C) 2017 Zhang Wenjie (wenjiez696@gmail.com)

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
floatdata.py
"""

import struct
from enum import Enum

class FloatData:
    FloatDataType = Enum("FloatDataType", "float double")
    _floatpacktype = {FloatDataType.float: '<f', FloatDataType.double: '<d'}
    _typelength = {FloatDataType.float: 4, FloatDataType.double: 8}

    _data = None
    _type = None

    def __init__(self):
        self._data = bytearray(4)
        self._type = FloatData.FloatDataType.float

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value != FloatData.FloatDataType.float and value != FloatData.FloatDataType.double:
            raise ValueError("type must be either FloatData.FloatDataType.float or FloatData.FloatDataType.double")
        if self._type != value:
            val = self.floatValue
            self._type = value
            self.floatValue = val
        self.updateWidget()

    @property
    def floatValue(self):
        return struct.unpack(FloatData._floatpacktype[self._type], self._data)[0]

    @floatValue.setter
    def floatValue(self, value):
        self._data = bytearray(struct.pack(FloatData._floatpacktype[self._type], value))
        self.updateWidget()

    @property
    def hexString(self):
        return self._data.hex()

    @hexString.setter
    def hexString(self, value):
        lenstr = FloatData._typelength[self._type] * 2
        if len(value) < lenstr:
            value = "0"*(lenstr - len(value)) + value
        if len(value) > lenstr:
            raise ValueError("value is too long.")
        self._data = bytearray.fromhex(value)
        self.updateWidget()

    def _index(self, bit):
        index = bit // 8
        b = bit % 8
        return index, b

    def getBit(self, bit):
        index, b = self._index(bit)
        return bool((self._data[index] >> b) & 1)

    def setBit(self, bit, value):
        index, b = self._index(bit)
        if value:
            self._data[index] |= 1 << b
        else:
            self._data[index] &= ~(1<<b)
        self.updateWidget()

    def updateWidget(self):
        pass