#!/usr/bin/env python3
"""gpiod-based Pinmux functionality of a BeagleBone using Python."""
import gpiod
import sys


# function to set pin mode
def set_pin_mode(key, mode):
	# pin mode can not be set for built-in USR LEDs
	if USR in key:
		return BBIO_OK
	if len(key)==4:
		print("{}{}{}{}".format(pin, sys.getsizeof(pin), key, key[3]))
	else:
		print("{}{}{}".format(pin, sys.getsizeof(pin), key))
