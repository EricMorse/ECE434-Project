#!/usr/bin/env python3
"""
Copyright (c) 2013 Adafruit

Original RPi.GPIO Py-Wrapper Author Ben Croston
Modified for BBIO Py-Wrapper Author Justin Cooper
Authors of Full Python Implementation: Mark Yoder, Joshua Key, and Eric Morse

This file incorporates work covered by the following copyright and 
permission notice, all modified code adopts the original license:

Copyright (c) 2013 Ben Croston

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
"""gpiod-based GPIO functionality of a BeagleBone using Python."""
import gpiod
import sys
#import multiprocessing
from multiprocessing import Pipe, Process
# import select
import time

ALT0 = 4
BOTH = 3
FALLING = 2
HIGH = 1
IN = 0
LOW = 0
OUT = 1
PUD_DOWN = 1
PUD_OFF = 0
PUD_UP = 2
RISING = 1
VERSION = '0.0.0'
threads=[]
ports={}        # Dictionary of channel/line pairs that are open
CONSUMER='GPIOmay'
parent_conn = []
gChannel = []
gChannelNames = []

# Table generated based on https://github.com/jadonk/bonescript/blob/master/src/bone.js
table = [
  [ "USR0", "USR0", 53, -1, -1, "GPMC_A5"],
  [ "USR1", "USR1", 54, -1, -1, "GPMC_A6"],
  [ "USR2", "USR2", 55, -1, -1, "GPMC_A7"],
  [ "USR3", "USR3", 56, -1, -1, "GPMC_A8"],
  [ "DGND", "P8_1", 0, -1, -1, "unused"],
  [ "DGND", "P8_2", 0, -1, -1, "unused"],
  [ "GPIO1_6", "P8_3", 38, -1, -1, "GPMC_AD6"],
  [ "GPIO1_7", "P8_4", 39, -1, -1, "GPMC_AD7"],
  [ "GPIO1_2", "P8_5", 34, -1, -1, "GPMC_AD2"],
  [ "GPIO1_3", "P8_6", 35, -1, -1, "GPMC_AD3"],
  [ "TIMER4", "P8_7", 66, 2, -1, "GPMC_ADVN_ALE"],
  [ "TIMER7", "P8_8", 67, 2, -1, "GPMC_OEN_REN"],
  [ "TIMER5", "P8_9", 69, 2, -1, "GPMC_BEON_CLE"],
  [ "TIMER6", "P8_10", 68, 2, -1, "GPMC_WEN"],
  [ "GPIO1_13", "P8_11", 45, -1, -1, "GPMC_AD13"],
  [ "GPIO1_12", "P8_12", 44, -1, -1, "GPMC_AD12"],
  [ "EHRPWM2B", "P8_13", 23, 4, -1, "GPMC_AD9"],
  [ "GPIO0_26", "P8_14", 26, -1, -1, "GPMC_AD10"],
  [ "GPIO1_15", "P8_15", 47, -1, -1, "GPMC_AD15"],
  [ "GPIO1_14", "P8_16", 46, -1, -1, "GPMC_AD14"],
  [ "GPIO0_27", "P8_17", 27, -1, -1, "GPMC_AD11"],
  [ "GPIO2_1", "P8_18", 65, -1, -1, "GPMC_DK_MUX0"],
  [ "EHRPWM2A", "P8_19", 22, 4, -1, "GPMC_AD8"],
  [ "GPIO1_31", "P8_20", 63, -1, -1, "GPMC_CSN2"],
  [ "GPIO1_30", "P8_21", 62, -1, -1, "GPMC_CSN1"],
  [ "GPIO1_5", "P8_22", 37, -1, -1, "GPMC_AD5"],
  [ "GPIO1_4", "P8_23", 36, -1, -1, "GPMC_AD4"],
  [ "GPIO1_1", "P8_24", 33, -1, -1, "GPMC_AD1"],
  [ "GPIO1_0", "P8_25", 32, -1, -1, "GPMC_AD0"],
  [ "GPIO1_29", "P8_26", 61, -1, -1, "GPMC_CSN0"],
  [ "GPIO2_22", "P8_27", 86, -1, -1, "LCD_VSYNC"],
  [ "GPIO2_24", "P8_28", 88, -1, -1, "LCD_PCLK"],
  [ "GPIO2_23", "P8_29", 87, -1, -1, "LCD_HSYNC"],
  [ "GPIO2_25", "P8_30", 89, -1, -1, "LCD_AC_BIAS_EN"],
  [ "UART5_CTSN", "P8_31", 10, -1, -1, "LCD_DATA14"],
  [ "UART5_RTSN", "P8_32", 11, -1, -1, "LCD_DATA15"],
  [ "UART4_RTSN", "P8_33", 9, -1, -1, "LCD_DATA13"],
  [ "UART3_RTSN", "P8_34", 81, 2, -1, "LCD_DATA11"],
  [ "UART4_CTSN", "P8_35", 8, -1, -1, "LCD_DATA12"],
  [ "UART3_CTSN", "P8_36", 80, 2, -1, "LCD_DATA10"],
  [ "UART5_TXD", "P8_37", 78, -1, -1, "LCD_DATA8"],
  [ "UART5_RXD", "P8_38", 79, -1, -1, "LCD_DATA9"],
  [ "GPIO2_12", "P8_39", 76, -1, -1, "LCD_DATA6"],
  [ "GPIO2_13", "P8_40", 77, -1, -1, "LCD_DATA7"],
  [ "GPIO2_10", "P8_41", 74, -1, -1, "LCD_DATA4"],
  [ "GPIO2_11", "P8_42", 75, -1, -1, "LCD_DATA5"],
  [ "GPIO2_8", "P8_43", 72, -1, -1, "LCD_DATA2"],
  [ "GPIO2_9", "P8_44", 73, -1, -1, "LCD_DATA3"],
  [ "GPIO2_6", "P8_45", 70, 3, -1, "LCD_DATA0"],
  [ "GPIO2_7", "P8_46", 71, 3, -1, "LCD_DATA1"],
  [ "DGND", "P9_1", 0, -1, -1, "unused"],
  [ "DGND", "P9_2", 0, -1, -1, "unused"],
  [ "VDD_3V3", "P9_3", 0, -1, -1, "unused"],
  [ "VDD_3V3", "P9_4", 0, -1, -1, "unused"],
  [ "VDD_5V", "P9_5", 0, -1, -1, "unused"],
  [ "VDD_5V", "P9_6", 0, -1, -1, "unused"],
  [ "SYS_5V", "P9_7", 0, -1, -1, "unused"],
  [ "SYS_5V", "P9_8", 0, -1, -1, "unused"],
  [ "PWR_BUT", "P9_9", 0, -1, -1, "unused"],
  [ "SYS_RESETn", "P9_10", 0, -1, -1, "unused"],
  [ "UART4_RXD", "P9_11", 30, -1, -1, "GPMC_WAIT0"],
  [ "GPIO1_28", "P9_12", 60, -1, -1, "GPMC_BEN1"],
  [ "UART4_TXD", "P9_13", 31, -1, -1, "GPMC_WPN"],
  [ "EHRPWM1A", "P9_14", 50, 6, -1, "GPMC_A2"],
  [ "GPIO1_16", "P9_15", 48, -1, -1, "GPMC_A0"],
  [ "EHRPWM1B", "P9_16", 51, 6, -1, "GPMC_A3"],
  [ "I2C1_SCL", "P9_17", 5, -1, -1, "SPI0_CS0"],
  [ "I2C1_SDA", "P9_18", 4, -1, -1, "SPI0_D1"],
  [ "I2C2_SCL", "P9_19", 13, -1, -1, "UART1_RTSN"],
  [ "I2C2_SDA", "P9_20", 12, -1, -1, "UART1_CTSN"],
  [ "UART2_TXD", "P9_21", 3, 3, -1, "SPI0_D0"],
  [ "UART2_RXD", "P9_22", 2, 3, -1, "SPI0_SCLK"],
  [ "GPIO1_17", "P9_23", 49, -1, -1, "GPMC_A1"],
  [ "UART1_TXD", "P9_24", 15, -1, -1, "UART1_TXD"],
  [ "GPIO3_21", "P9_25", 117, -1, -1, "MCASP0_AHCLKX"],
  [ "UART1_RXD", "P9_26", 14, -1, -1, "UART1_RXD"],
  [ "GPIO3_19", "P9_27", 115, -1, -1, "MCASP0_FSR"],
  [ "SPI1_CS0", "P9_28", 113, 4, -1, "MCASP0_AHCLKR"],
  [ "SPI1_D0", "P9_29", 111, 1, -1, "MCASP0_FSX"],
  [ "SPI1_D1", "P9_30", 112, -1, -1, "MCASP0_AXR0"],
  [ "SPI1_SCLK", "P9_31", 110, 1, -1, "MCASP0_ACLKX"],
  [ "VDD_ADC", "P9_32", 0, -1, -1, "unused"],
  [ "AIN4", "P9_33", 0, -1, 4, "unused"],
  [ "GNDA_ADC", "P9_34", 0, -1, -1, "uused"],
  [ "AIN6", "P9_35", 0, -1, 6, "unused"],
  [ "AIN5", "P9_36", 0, -1, 5, "unused"],
  [ "AIN2", "P9_37", 0, -1, 2, "unused"],
  [ "AIN3", "P9_38", 0, -1, 3, "unused"],
  [ "AIN0", "P9_39", 0, -1, 0, "unused"],
  [ "AIN1", "P9_40", 0, -1, 1, "unused"],
  [ "CLKOUT2", "P9_41", 20, -1, -1, "XDMA_EVENT_INTR1"],
  [ "GPIO0_7", "P9_42", 7, 0, -1, "ECAP0_IN_PWM0_OUT"],
  [ "DGND", "P9_43", 0, -1, -1, "unused"],
  [ "DGND", "P9_44", 0, -1, -1, "unused"],
  [ "DGND", "P9_45", 0, -1, -1, "unused"],
  [ "DGND", "P9_46", 0, -1, -1, "unused"],
  
  # Commented out Blue and PocketBeagle since our project doesn't use them
  #  These are for the Blue
  #[ "GP0_3", "GP0_3",  57, -1, -1, "blue"],
  #[ "GP0_4", "GP0_4",  49, -1, -1, "blue"],
  #[ "GP0_5", "GP0_5", 116, -1, -1, "blue"],
  #[ "GP0_6", "GP0_6", 113, -1, -1, "blue"],
  #[ "GP1_3", "GP1_3",  98, -1, -1],
  #[ "GP1_4", "GP1_4",  97, -1, -1],
  #[ "RED_LED",   "RED",    66, -1, -1],   # LEDs
  #[ "GREEN_LED", "GREEN",  67, -1, -1],
  #[ "BAT25", "BAT25",  27, -1, -1],
  #[ "BAT50", "BAT50",  11, -1, -1],
  #[ "BAT75", "BAT75",  61, -1, -1],
  #[ "BAT100", "BAT100",  10000, -1, -1], # Placeholder
  #[ "WIFI", "WIFI",  10001, -1, -1], # Placeholder
  
  #[ "PAUSE", "P8_9",  69, 1, -1],
  #[ "MODE",  "P8_10", 68, 1, -1],
  
  # These are for the PocketBeagle
  #[ "VIN_AC", "P1_1", 0, -1, -1],
  #[ "GPIO2_23", "P1_2", 87, -1, -1],
  #[ "USB1_DRVVBUS", "P1_3", 0, -1, -1],
  #[ "GPIO2_25", "P1_4", 89, -1, -1],
  #[ "USB1_VBUS_IN", "P1_5", 0, -1, -1],
  #[ "SPI0_CS0", "P1_6", 5, -1, -1],
  #[ "VIN-USB", "P1_7", 0, -1, -1],
  #[ "SPI0_SCLK", "P1_8", 2, 3, -1],
  #[ "USB1-DN", "P1_9", 0, -1, -1],
  #[ "SPI0_D0", "P1_10", 3, 3, -1],
  #[ "USB1-DP", "P1_11", 0, -1, -1],
  #[ "SPI0_D1", "P1_12", 4, -1, -1],
  #[ "USB1-ID", "P1_13", 0, -1, -1],
  #[ "VOUT-3.3V", "P1_14", 0, -1, -1],
  #[ "GND", "P1_15", 0, -1, -1],
  #[ "GND", "P1_16", 0, -1, -1],
  #[ "VREFN", "P1_17", 0, -1, -1],
  #[ "VREFP", "P1_18", 0, -1, -1],
  #[ "AIN0", "P1_19", 0, -1, 0],
  #[ "GPIO0_20", "P1_20", 20, 4, -1],
  #[ "AIN1", "P1_21", 0, -1, 1],
  #[ "GND", "P1_22", 0, -1, -1],
  #[ "AIN2", "P1_23", 0, -1, 2],
  #[ "VOUT-5V", "P1_24", 0, -1, -1],
  #[ "AIN3", "P1_25", 0, -1, 3],
  #[ "I2C2_SDA", "P1_26", 12, 1, -1],
  #[ "AIN4", "P1_27", 0, -1, 4],
  #[ "I2C2_SCL", "P1_28", 13, 1, -1],
  #[ "GPIO3_21", "P1_29", 117, -1, -1],
  #[ "UART0_TXD", "P1_30", 43, -1, -1],
  #[ "GPIO3_18", "P1_31", 114, -1, -1],
  #[ "UART0_RXD", "P1_32", 42, -1, -1],
  #[ "GPIO3_15", "P1_33", 111, 1, -1],
  #[ "GPIO0_26", "P1_34", 26, -1, -1],
  #[ "GPIO2_24", "P1_35", 88, -1, -1],
  #[ "EHRPWM0A", "P1_36", 110, 1, -1],
  #[ "EHRPWM1A", "P2_1", 50, 6, -1],
  #[ "GPIO1_27", "P2_2", 59, -1, -1],
  #[ "GPIO0_23", "P2_3", 23, 4, -1],
  #[ "GPIO1_26", "P2_4", 58, -1, -1],
  #[ "UART4_RXD", "P2_5", 30, -1, -1],
  #[ "GPIO1_25", "P2_6", 57, -1, -1],
  #[ "UART4_TXD", "P2_7", 31, -1, -1],
  #[ "GPIO1_28", "P2_8", 60, -1, -1],
  #[ "I2C1_SCL", "P2_9", 15, -1, -1],
  #[ "GPIO1_20", "P2_10", 52, -1, -1],
  #[ "I2C1_SDA", "P2_11", 14, -1, -1],
  #[ "POWER_BUTTON", "P2_12", 0, -1, -1],
  #[ "VOUT-5V", "P2_13", 0, -1, -1],
  #[ "BAT-VIN", "P2_14", 0, -1, -1],
  #[ "GND", "P2_15", 0, -1, -1],
  #[ "BAT-TEMP", "P2_16", 0, -1, -1],
  #[ "GPIO2_1", "P2_17", 65, -1, -1],
  #[ "GPIO1_15", "P2_18", 47, -1, -1],
  #[ "GPIO0_27", "P2_19", 27, -1, -1],
  #[ "GPIO2_0", "P2_20", 64, -1, -1],
  #[ "GND", "P2_21", 0, -1, -1],
  #[ "GPIO1_14", "P2_22", 46, -1, -1],
  #[ "VOUT-3.3V", "P2_23", 0, -1, -1],
  #[ "GPIO1_12", "P2_24", 44, -1, -1],
  #[ "SPI1_CS0", "P2_25", 41, -1, -1],
  #[ "RESET#", "P2_26", 0, -1, -1],
  #[ "SPI1_D0", "P2_27", 40, 5, -1],
  #[ "GPIO3_20", "P2_28", 116, -1, -1],
  #[ "SPI1_SCLK", "P2_29", 7, -1, -1],
  #[ "GPIO3_17", "P2_30", 113, -1, -1],
  #[ "SPI1_CS1", "P2_31", 19, 2, -1],
  #[ "GPIO3_16", "P2_32", 112, -1, -1],
  #[ "GPIO1_13", "P2_33", 45, -1, -1],
  #[ "GPIO3_19", "P2_34", 115, -1, -1],
  #[ "GPIO2_22", "P2_35", 86, -1, -1],
  #[ "AIN7", "P2_36", 0, -1, 7],
  
  [ None, None, 0, 0, 0, "unused" ]
]
def channelNameConvert(channel):
    global gChannel
    global gChannelNames
    for i in range(0, len(gChannel)):
        if channel == gChannelNames[i]:
            return gChannel[i]
    print("Error: name not found")
    return "error"

def run(channel, edge, callback=None, debounce=0, child_conn=None):
    channel = channelNameConvert(channel)
    thread_go = True
    while thread_go:
        event_detected = None
        thread_go = wait_for_edge(channel, edge, child_conn)
        if thread_go:
            time.sleep(debounce/1000000.0)
            callback(channel)
        #thread_go = not child_conn.poll()
        #if not thread_go:
        #    child_conn.close()

def setup(channel, direction):
    """Set up the GPIO channel, direction and (optional) pull/up down control.
    
    channel        - channel can be in the form of 'P8_10', or 'EHRPWM2A'
    direction      - INPUT or OUTPUT
    [pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN
    [initial]      - Initial value for an output channel
    [delay]        - Time in milliseconds to wait after exporting gpio pin"""
    global gChannel
    global gChannelNames
    for index in table:
       if index[1] == channel:
           channel = index[5]
           gChannel.append(index[5])
           gChannelNames.append(index[1])
           break
       elif index[0] == channel:
           channel = index[5]
           gChannel.append(index[5])
           gChannelNames.append(index[0])
           break
       elif index[5] == channel:
           gChannel.append(index[5])
           gChannelNames.append(index[5])
    found=0
# Searh for channel in either name or consumer
    for chip in gpiod.ChipIter():
        # print('[] - [] lines:'.format(chip.name(), chip.num_lines()))

        for line in gpiod.LineIter(chip):
            offset = line.offset()
            name = line.name()
            consumer = line.consumer()
            linedirection = line.direction()
            active_state = line.active_state()
            
            if name == channel or consumer == channel:

                # print('[]\tline [:>3]: [:>18] [:>12] [:>8] [:>10]'.format(
                #         chip.name(),
                #         offset,
                #         'unnamed' if name is None else name,
                #         'unused' if consumer is None else consumer,
                #         'input' if linedirection == gpiod.Line.DIRECTION_INPUT else 'output',
                #         'active-low' if active_state == gpiod.Line.ACTIVE_LOW else 'active-high'))
                found=1
                break
        if found:
            break

        chip.close()

    if not found: 
        print(channel + ': Not found')
        sys.exit(1)
    
    # print(chip)
    
    lines = chip.get_lines([offset])
    # print(lines)
    if direction == IN:
        ret = lines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_IN)
    elif direction == OUT:
        ret = lines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)
    else:
        print("Unknown direction: " + str(direction))
        sys.exit(1)
    
    if ret:
        print(ret)
        
    ports[channel] = [lines, chip]
    # print(ports)

def output(channel, vals):
    """Output to a GPIO channel
    
    channel  - gpio channel
    value - 0/1 or False/True or LOW/HIGH"""
    # print("output()")
    print(channel)
    channel = channelNameConvert(channel)
    print(channel)
    if type(vals) is not type([]):
       vals = [vals]
    ret = ports[channel][0].set_values(vals)
    if ret:
        print(ret)

def input(channel):
    """Input from a GPIO channel.  Returns HIGH=1=True or LOW=0=False
    gpio - gpio channel"""
    # print("input()")
    # print(channel)
    channel = channelNameConvert(channel)
    return ports[channel][0].get_values()

def wait_for_edge(channel, edge, child_conn, timeout = -1):
    """Wait for an edge.
    
    channel - gpio channel
    edge - RISING, FALLING or BOTH
    timeout (optional) - time to wait in miliseconds. -1 will wait forever (default)"""
    # print("wait_for_edge()")
    # print(ports)
    channel = channelNameConvert(channel)
    line=ports[channel][0]
    chip=ports[channel][1]
    
    if edge == RISING:
        ev_edge = gpiod.LINE_REQ_EV_RISING_EDGE
    elif edge == FALLING:
        ev_edge = gpiod.LINE_REQ_EV_FALLING_EDGE
    elif edge == BOTH:
        ev_edge = gpiod.LINE_REQ_EV_BOTH_EDGES
    else:
        print("Unknown edge type: " + str(edge))
    
    # Try releasing the line and requesting again
    
    offset = line.to_list()[0].offset()
    line.release()
    line = chip.get_lines([offset])
    
    line.request(consumer=CONSUMER, type=ev_edge)
    x = None
    while not x:
        thread_go = not child_conn.poll()
        if not thread_go:
            return False 
        x = line.event_wait(sec = 1)
    return True

def add_event_detect(channel, edge, callback=None, debounce=0):
    """Enable edge detection events for a particular GPIO channel.
  
    channel      - board pin number.
    edge         - RISING, FALLING or BOTH
    [callback]   - A callback function for the event (optional)
    [bouncetime] - Switch bounce timeout in ms for callback"""
    global threads
    global parent_conn
    channel = channelNameConvert(channel)
    parent_conn_temp, child_conn  = Pipe()
    parent_conn.append(parent_conn_temp)
    process2 = Process(target = run, args = (channel, edge, callback, debounce, child_conn))
    threads.append(process2)
    process2.start()
    return
       
def cleanup():
    """Clean up by resetting all GPIO channels that have been used by 
    this program to INPUT with no pullup/pulldown and no event detection."""
    global ports
    global threads
    i = 0
    for thread in threads:
        parent_conn[i].send(False)
        parent_conn[i].close()
        thread.join()
        thread.close()
        i = i + 1
    for channel, val in ports.items():
        ret = val[0].release()
        if ret:
            print(ret)
        ret = val[1].close()
        if ret:
            print(ret)
        ports={}
