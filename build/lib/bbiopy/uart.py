#!/usr/bin/env python3

"""
Copyright (c) 2013 Adafruit
Author of Py-Wrapper version: Justin Cooper
Authors of Full Python version: Mark Yoder, Eric Morse, and Joshua Key

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


"uart functionality of the BeagleBone"
# import importlib

# common = input('common')
# importlib.import_module(common)
import os

uart_table = [
  [ "UART1", "/dev/ttyO1", "ADAFRUIT-UART1", "P9_26", "P9_24"],
  [ "UART2", "/dev/ttyO2", "ADAFRUIT-UART2", "P9_22", "P9_21"],
  [ "UART3", "/dev/ttyO3", "ADAFRUIT-UART3", "P9_42", ""],
  [ "UART4", "/dev/ttyO4", "ADAFRUIT-UART4", "P9_11", "P9_13"],
  [ "UART5", "/dev/ttyO5", "ADAFRUIT-UART5", "P8_38", "P8_37"],
  [ "PB-UART0", "/dev/ttyO0", "ADAFRUIT-UART0", "P1_30", "P1_32"],
  [ "PB-UART1", "/dev/ttyO1", "ADAFRUIT-UART1", "P2_11", "P2_09"],
  [ "PB-UART2", "/dev/ttyO2", "ADAFRUIT-UART2", "P1_08", "P1_10"],
  [ "PB-UART4", "/dev/ttyO4", "ADAFRUIT-UART4", "P2_05", "P2_07"],
  [ None, None, 0, 0, 0 ]
]

# uboot overlay
"""def uboot_overlay_enabled():
	cmd = "/bin/grep -c bone_capemgr.uboot_capemgr_enabled=1 /proc/cmdline"
	
	file = os.popen(cmd, mode="r")
	if file == None:
			print("error: uboot_overlay_enabled() failed to run cmd = {}".format(cmd))
			return -1
	uboot_overlay = file.read(1)
	file.close()
	
	if uboot_overlay == '1':
		print("Adafruit_BBIO: uboot_overlay_enabled() is true")
		return 1
	else:
		print("Adafruit_BBIO: uboot_overlay_enabled() is false")
		return 0
"""

	
def uart_setup(name):
	for k in range(0,5):
		if name == uart_table[k][2]:
			if k == 2:
				file_dir= "/sys/devices/platform/ocp/ocp:" + uart_table[2][3] + "_pinmux/state"
				state = open(file_dir, mode='w')
				state.write("uart")
				state.close()
			else:
				for i in range(0, 2):
					file_dir = "/sys/devices/platform/ocp/ocp:" + uart_table[k][3+i] + "_pinmux/state"
					state = open(file_dir, mode='w')
					state.write("uart")
					state.close()

def uart_cleanup():
	for k in range(0,5):
		if k == 2:
			file_dir = "/sys/devices/platform/ocp/ocp:" + uart_table[2][3] + "_pinmux/state"
			state = open(file_dir, mode='w')
			state.write("default")
			state.close()
		else:
			for i in range(0, 2):
				file_dir = "/sys/devices/platform/ocp/ocp:" + uart_table[k][3+i] + "_pinmux/state"
				state = open(file_dir, mode='w')
				state.write("default")
				state.close()
	# e1 = unload_device_tree("ADAFRUIT-UART1")
	# e2 = unload_device_tree("ADAFRUIT-UART2")
	# e3 = unload_device_tree("ADAFRUIT-UART3")
	# e4 = unload_device_tree("ADAFRUIT-UART4")
	# e5 = unload_device_tree("ADAFRUIT-UART5")
	# if e1 is not "OK":
	#	return e1
	# if e2 is not "OK":
	#	return e2
	# if e3 is not "OK":
	#	return e3
	# if e4 is not "OK":
	#	return e4
	#if e5 is not "OK":
	#	return e5

	#return "OK"

