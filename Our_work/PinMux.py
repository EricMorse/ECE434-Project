#!/usr/bin/env python3
"""gpiod-based Pinmux functionality of a BeagleBone using Python."""
import gpiod
import sys
from collections import defaultdict

def def_value():
	return "<INVALID>"

BBIO_ERR = defaultdict(def_value)

BBIO_ERR = {
	"BBIO_OK" : "OK",
	"BBIO_ACCESS" : "ACCESS",
	"BBIO_SYSFS" : "SYSFS",
	"BBIO_CAPE" : "CAPE",
	"BBIO_INVARG": "INVARG",
	"BBIO_MEM": "MEMORY",
	"BBIO_GEN": "GENERAL"
}

# function to set pin mode
def set_pin_mode(channel, mode):
	path = '/sys/devices/platform/ocp/ocp:' + channel + '_pinmux/state'
	fd = open(path, 'w')
	fd.write(mode)
	fd.close()

	return path
