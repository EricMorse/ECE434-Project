import adc as adc
voltage = adc.readVoltage("AIN0")
print(adc.convertVoltage(voltage))
