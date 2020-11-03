import GPIOmay as GPIO
channel = 'GPMC_A2'
GPIO.setup(channel, GPIO.OUT)
GPIO.wait_for_event(channel)
GPIO.event_detected(channel)
