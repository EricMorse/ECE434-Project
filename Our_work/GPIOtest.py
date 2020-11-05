#!/usr/bin/env python3
# From: https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/gpio
# From: https://adafruit-beaglebone-io-python.readthedocs.io/en/latest/GPIO.html

# To setup a digital pin as an output, set the output value HIGH, and then cleanup after you're done:
# import Adafruit_BBIO.GPIO as GPIO
import GPIOmay as GPIO
import time

# CHANNEL='P9_14'
CHANNEL='GPMC_A2'       # P9_14
INPUT="GPMC_AD10"       # P8_14

GPIO.setup(CHANNEL, GPIO.OUT)
# while True:
GPIO.output(CHANNEL, [GPIO.HIGH])     # You can also write 1 instead.
time.sleep(0.1)
GPIO.output(CHANNEL, [GPIO.LOW])     # You can also write 1 instead.
time.sleep(0.1)
GPIO.output(CHANNEL, [GPIO.HIGH])     # You can also write 1 instead.
    
# GPIO.cleanup()

# You can also refer to the pin names:
# GPIO.setup("P9_14", GPIO.OUT)

# In the first example, you can see we used the "P8_10" key to designate which 
# pin we'd like to set as the output, and the same pin in the second example,
# but using it's name "GPMC_A0".


# You can also set pins as inputs as follows:
GPIO.setup(INPUT, GPIO.IN)

# Once you've done that, you can access the input value in a few different ways. 
# The first, and easiest way is just polling the inputs, such as in a loop that keeps checking them:
if GPIO.input(INPUT)[0]:  # P8_14
    print("HIGH")
else:
    print("LOW")

# You can also wait for an edge. This means that if the value is falling 
# (going from 3.3V down to 0V), rising (going from 0V up to 3.3V), 
# or both (that is it changes from 3.3V to 0V or vice-versa), 
# the GPIO library will trigger, and continue execution of your program.

# The wait_for_edge method is blocking, and will wait until something happens:
# print("waiting for edge...", end='')
# GPIO.wait_for_edge(INPUT, GPIO.HIGH, timeout=5000)


# Another option, that is non-blocking is to add an event to detect. 
# First, you setup your event to watch for, then you can do whatever else your 
# program will do, and later on, you can check if that event was detected.

def my_callback(channel):
    print("callback called")
    #print('Edge detected on channel {}'.format(channel))

# # A simple example of this is as follows:
GPIO.add_event_detect(INPUT, GPIO.FALLING, callback = my_callback)
#your amazing code here
#detect wherever: 
#time.sleep(5)
#if GPIO.event_detected(INPUT):
#   print("event detected again!")
    
# # Or if you want you can define a callback function.

# Then have it called when the event occurs
#GPIO.remove_event_detect("P8_14")
#GPIO.add_event_detect("P8_14", GPIO.BOTH, callback=my_callback) 

#while True:             # Do something while waiting for event
#   time.sleep(100)
 
GPIO.cleanup()
print("all done!")
