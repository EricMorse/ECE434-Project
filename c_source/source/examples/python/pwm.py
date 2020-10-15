#!/usr/bin/env python3
import Adafruit_BBIO.PWM as PWM

#set polarity to 1 on start:
#PWM.start("P9_14", 50, 2000, 1)

#PWM.start(channel, duty, freq=2000, polarity=0)
#duty values are valid 0 (off) to 100 (on)

SERVO="P9_14"
PWM.start(SERVO, 50)
PWM.set_duty_cycle(SERVO, 25.5)
PWM.set_frequency(SERVO, 10)

PWM.stop(SERVO)
PWM.cleanup()
