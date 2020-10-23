#!/usr/bin/env python3

import PWMmay as PWM
import PinMux as PinMux

channel = "P9_14"

# print(PWM.get_pwm_key(channel))

# print(PWM.get_pwm_path(channel))

err = PWM.start(channel, 50, freq=10)
if err == None:
    exit()

print(PWM.set_frequency(channel, 10))

print(PWM.set_duty_cycle(channel, 10))

print(PinMux.set_pin_mode(channel, "gpio"))
# print(PWM.stop(channel))
