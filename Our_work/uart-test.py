import uart as uart

# uart.uboot_overlay_enabled()
uart.uart_setup("ADAFRUIT-UART3")
uart.uart_cleanup()
