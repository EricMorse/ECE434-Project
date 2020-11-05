#!/usr/bin/env python3
"""gpiod-based GPIO functionality of a BeagleBone using Python."""
import gpiod
import sys
from multiprocessing import Process

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

#class myThread(threading.Thread):
#    def __init__(self, threadID, channel, edge, callback, debounce):
#        threading.Thread.__init__(self)
#        self.threadID = threadID
#        self.channel = channel
#        self.old_value = input(channel)[0]
#        self.edge = edge
#        self.callback = callback
#        self.debounce = debounce
#        # self.run()
#    def run(self):
#       # print("Run the thread")
#        # Get lock to synchronize threads
#        #threadLock.acquire()
#        event_detected = None
#        print("waiting for edge")
#        wait_for_edge(self.channel, self.edge)
#        print("Event detected")
#        print(self.old_value)
#        if self.edge == BOTH:
#                #print("Both triggered!")
#                self.callback()
#                self.old_value = input(self.channel)
#        else:
#                if self.old_value == 0 and self.edge == RISING:
#                        print("we got high!")
#                        event_detected = RISING
#                elif self.old_value == 1 and self.edge == FALLING:
#                        print("We got low!")
#                        event_detected = FALLING#
#
#                if self.edge == event_detected:
#                        print("Callback called!")
#                        self.callback(self.channel)
#                self.old_value = input(self.channel)[0]
#        self.run()

def run(channel, edge, callback=None, debounce=0):
        # print("Run the thread")
        # Get lock to synchronize threads
        #threadLock.acquire()
        x = True
        while x:
            recv(x)
            event_detected = None
            print("waiting for edge")
            old_value = input(channel)[0]
            wait_for_edge(channel, edge)
            print("Event detected")
            if edge == BOTH:
                    print("Both triggered!")
                    callback(channel)
                    old_value = input(channel)[0]
            else:
                    if old_value == 0:
                            print("we got high!")
                            event_detected = RISING
                    else:
                            print("We got low!")
                            event_detected = FALLING
                    print("edge = {}".format(edge))
                    print("event_detected = {}".format(event_detected))
                    if edge is event_detected:
                            print("Callback called!")
                            callback(channel)
                    old_value = input(channel)[0]	
        

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

    if found: 
        print('{}: {}: {}, {}'.format(chip.name(), offset, name, consumer))
    else:
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

def wait_for_edge(channel, edge, timeout = -1):
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
    print("Initialize the thread")
    process2 = Process(target = run, args = (channel, edge, callback, debounce))
    threads.append(process2)
    process2.start()
    # thread2.run()
    print("The rest of the function gets to run")
    #line=ports[channel][0]
    #print(line.to_list())
    #print(line.to_list()[0].event_read())
    #if edge == RISING:
    #    print("RISING Edge")
    #    ev_edge = gpiod.LINE_REQ_EV_RISING_EDGE
    #elif edge == FALLING:
    #    print("Falling Edge")
    #    ev_edge = gpiod.LINE_REQ_EV_FALLING_EDGE
    #elif edge == BOTH:
    #    print("BOTH Edges")
    #    ev_edge = gpiod.LINE_REQ_EV_BOTH_EDGES
    #else:
    #    #print("Unknown edge type: " + str(edge))
    #    ev_edge = gpiod.LINE_REQ_EV_FALLING_EDGE
    return
    #line.to_list()[0].add_event_detect(channel, ev_edge)
    

#def event_detected(channel):
#    """Returns True if an edge has occured on a given GPIO.  
#   
#    You need to enable edge detection using add_event_detect() first.
#    channel - gpio channel"""
#    line=ports[channel][0]
#    return line.event_detected(channel)
       
def cleanup():
    """Clean up by resetting all GPIO channels that have been used by 
    this program to INPUT with no pullup/pulldown and no event detection."""
    global ports
    global threads
    for thread in threads:
        thread.send(False)
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
