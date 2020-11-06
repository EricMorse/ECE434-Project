#!/usr/bin/env python3
"""gpiod-based GPIO functionality of a BeagleBone using Python."""
import gpiod
import sys
import multiprocessing
import select
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
parent_conn = None

def run(channel, edge, callback=None, debounce=0, child_conn=None):
        thread_go = True
        while thread_go:
            event_detected = None
            wait_for_edge(channel, edge, child_conn)
            callback(channel)
            thread_go = not child_conn.poll()
            if not thread_go:
                    child_conn.close()

def setup(channel, direction):
    """Set up the GPIO channel, direction and (optional) pull/up down control.
    
    channel        - channel can be in the form of 'P8_10', or 'EHRPWM2A'
    direction      - INPUT or OUTPUT
    [pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN
    [initial]      - Initial value for an output channel
    [delay]        - Time in milliseconds to wait after exporting gpio pin"""


    found=0
# Searh for channel in either name or consumer
    for chip in gpiod.ChipIter():
        # print('{} - {} lines:'.format(chip.name(), chip.num_lines()))

        for line in gpiod.LineIter(chip):
            offset = line.offset()
            name = line.name()
            consumer = line.consumer()
            linedirection = line.direction()
            active_state = line.active_state()
            
            if name == channel or consumer == channel:

                # print('{}\tline {:>3}: {:>18} {:>12} {:>8} {:>10}'.format(
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
    # print(channel)
    ret = ports[channel][0].set_values(vals)
    if ret:
        print(ret)

def input(channel):
    """Input from a GPIO channel.  Returns HIGH=1=True or LOW=0=False
    gpio - gpio channel"""
    # print("input()")
    # print(channel)
    return ports[channel][0].get_values()

def wait_for_edge(channel, edge, child_conn, timeout = -1):
    """Wait for an edge.
    
    channel - gpio channel
    edge - RISING, FALLING or BOTH
    timeout (optional) - time to wait in miliseconds. -1 will wait forever (default)"""
    # print("wait_for_edge()")
    # print(ports)
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
       x = line.event_wait(sec = 1)
    return line.event_wait()

def add_event_detect(channel, edge, callback=None, debounce=0):
    """Enable edge detection events for a particular GPIO channel.
  
    channel      - board pin number.
    edge         - RISING, FALLING or BOTH
    [callback]   - A callback function for the event (optional)
    [bouncetime] - Switch bounce timeout in ms for callback"""
    global threads
    global parent_conn
    parent_conn, child_conn  = multiprocessing.Pipe()
    process2 = multiprocessing.Process(target = run, args = (channel, edge, callback, debounce, child_conn))
    threads.append(process2)
    process2.start()
    return
       
def cleanup():
    """Clean up by resetting all GPIO channels that have been used by 
    this program to INPUT with no pullup/pulldown and no event detection."""
    global ports
    global threads
    for thread in threads:
        parent_conn.send(False)
        parent_conn.close()
        thread.join()
        thread.close()
    for channel, val in ports.items():
        ret = val[0].release()
        if ret:
            print(ret)
        ret = val[1].close()
        if ret:
            print(ret)
        ports={}
