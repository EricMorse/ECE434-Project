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
	
