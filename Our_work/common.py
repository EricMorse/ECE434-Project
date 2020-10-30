import os

uart_table = [
  [ "UART1", "/dev/ttyO1", "ADAFRUIT-UART1", "P9_26", "P9_24"],
  [ "UART2", "/dev/ttyO2", "ADAFRUIT-UART2", "P9_22", "P9_21"],
  [ "UART3", "/dev/ttyO3", "ADAFRUIT-UART3", "P9_42", ""],
  [ "UART4", "/dev/ttyO4", "ADAFRUIT-UART4", "P9_11", "P9_13"],
  [ "UART5", "/dev/ttyO5", "ADAFRUIT-UART5", "P8_38", "P8_37"],
  [ "PB-UART0", "/dev/ttyO0", "ADAFRUIT-UART0", "P1_30", "P1_32"],
  [ "PB-UART1", "/dev/ttyO1", "ADAFRUIT-UART1", "P2_11", "P2_09"],
  [ "PB-UART2", "/dev/ttyO2", "ADAFRUIT-UART2", "P1_08", "P1_10"],
  [ "PB-UART4", "/dev/ttyO4", "ADAFRUIT-UART4", "P2_05", "P2_07"],
  [ None, None, 0, 0, 0 ]
]


# uboot overlay
def uboot_overlay_enabled():
	cmd = "/bin/grep -c bone_capemgr.uboot_capemgr_enabled=1 /proc/cmdline"
	file = os.popen(cmd, mode="r")
	if file == None:
			print("error: uboot_overlay_enabled() failed to run cmd = {}".format(cmd))
			return -1
	uboot_overlay = file.read(1)
	file.close()
	
	if uboot_overlay == '1':
		print("Adafruit_BBIO: uboot_overlay_enabled() is true")
		return 1
	else:
		print("Adafruit_BBIO: uboot_overlay_enabled() is false")
		return 0

# Need load_device_tree function
def load_device_tree(name):
	if uboot_overlay_enabled():
		return "OK"
	if name == "UART":
	# We are attempting to use config-pin setups instead of slot file alterations (Eric Morse and Joshua Key)
	#	os.system("config-pin
	# print("{}{}{}".format(ctrl_dir, sizeof(ctrl_dir), "/sys/devices/platform/bone_capemgr"))
	# file = open(slots, mode = 'r')
	# if not file:
	# 	return "CAPE"
	# while file.read(line, sizeof(line, file)):
	#	pos =  line.find(name)
	#	if pos >= 0:
	#		if line[pos:]:
	#			close(file)
	#			return "OK"
	#print("{}".format(name), end='', file = file)
	#close(file)
	sleep(0.2)
	return "OK"

# Don't really need device_tree_loaded function
def device_tree_loaded(name):
	if uboot_overlay_enabled():
		return 1
	# print("{}{}{}".format(ctrl_dir, sizeof(ctrl_dir), "/sys/devices/platform/bone_capemgr"))
	if not file:
		return -1
	file = open(slots, mode = 'r')
	while file.read(line, sizeof(line, file)):
		pos = line.find(name)
		if pos >= 0:
			if line[pos:]:
				close(file)
				return 1
	close(file)
	return 0

# Need unload_device_tree function
def unload_device_tree(name):
	file = open(slots, mode='r')
	if not file:
		return "SYSFS"
	while file.read(line, sizeof(line, file)):
		pos = line.find(name)
		if pos >= 0:
			if line[pos:]:
				slot_line =  [string(x) for x in line.split(":") is x.strip()]
				print("{}".format(slot_line), end='', file = file)
				close(file)
				return "OK"
	close(file)
	return "OK"
