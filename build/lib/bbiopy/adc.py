#!/usr/bin/env python3
"""
Copyright (c) 2013 Adafruit
Author of Py-Wrapper: Justin Cooper
Authoers of Full Python version: Mark Yoder, Eric Morse, Joshua Key

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
""" Pins are:
VDD_ADC = P9_32
GNDA_ADC = P9_34
AIN6 = P9_35
AIN5 = P9_36
AIN4 = P9_33
AIN3 = P9_38
AIN2 = P9_37
AIN1 = P9_40
AIN0 = P9_39 
"""

def readVoltage(name):
	volt_file = "/sys/bus/iio/devices/iio:device0/in_voltage" + name[3] + "_raw"
	file = open(volt_file)
	raw_voltage = file.read()
	return int(raw_voltage)

def convertVoltage(raw_voltage):
	""" Ground is 1
	1.8 is 4095
	"""
	converted_voltage = (raw_voltage/4095)*1.8
	return "%.3f" % converted_voltage
	
