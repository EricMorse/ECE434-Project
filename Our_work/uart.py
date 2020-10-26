import importlib

common = input('common')
importlib.import_module(common)

def uart_setup(dt):
	return load_device_tree(dt)

def uart_cleanup():
	e1 = unload_device_tree("ADAFRUIT-UART1")
	e2 = unload_device_tree("ADAFRUIT-UART2")
	e3 = unload_device_tree("ADAFRUIT-UART3")
	e4 = unload_device_tree("ADAFRUIT-UART4")
	e5 = unload_device_tree("ADAFRUIT-UART5")
	if e1 is not "OK":
		return e1
	if e2 is not "OK":
		return e2
	if e3 is not "OK":
		return e3
	if e4 is not "OK":
		return e4
	if e5 is not "OK":
		return e5

	return "OK"

