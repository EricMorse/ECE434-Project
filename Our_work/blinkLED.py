#!/usr/bin/env python3
import GPIOmay as GPIO
import time

LED="P9_14"
#LED = "GPMC_A2"
GPIO.setup(LED, GPIO.OUT)

while True:
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(0.5)
