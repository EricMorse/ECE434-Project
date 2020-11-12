# Creators
Mark A Yoder, Eric Morse, and Joshua Key
# License
GPL
# Executive Summary
Picture that summarizes the project
BBIO are a group of library files for gpio that are written in C that is wrapped into Python.  Our project is to rewrite the library fully in Python rather than using wrappers.
What works: The GPIO, UART, and ADC capabilities will now run the same way they normally would, expect the Python does not use a Python wrapper.
What isn't working: The programs have only been tested on the BeagleBone Black with kernel 4.19.  The BBIO programs may not function correctly on other kernels or BeagleBones.
Conclusion: The BBIO library no longer requires a Python wrapper as all of the functions interact with the BeagleBone directly from Python.

# Packaging (N/A)
hardware information (we have only software)
# Installation Instructions (N/A)
how to install the project
# User Instructions
The programmer has to import the library into the code that they write and call the gpiod functions from that library.
# Highlights
We created a full drop-in replacement of gpiod's pywrapper in C to a full python implementation of gpiod for python programmers.  It has full gpiod functionality with gpio pin event detection and setting outputs on gpio pins.  It supports setting directions during setup.  It also supports setting up multiple gpio pins at the same time, which is how gpiod differs from regular gpio.  It has full support for UART functionality as well as ADC conversions.
# Theory of Operation
The library is a drop-in replacement of the py-wrapper version of BBIO gpiod.  A programmer would import the library files into the code they write and call the functions.  
.setup() to setup a gpio pin.  
.output() to configure the output of a gpio pin that has been setup already.  
.add_event_detect() to detect a change in the value of a gpio pin, and go to a callback function when it changes.  
.cleanup() to close all memory allocations and remove all pins.  

# Work Breakdown
Joshua Key and Eric Morse did pair-programming.  
We worked the entire project and all modules together.  
We completed all GPIO functionality of GPIOD, including event detection.  
We completed all UART functionality of GPIOD.  
We also completed all Pinmux and ADC (Analog to Digital Conversion) of GPIOD.  
Mark Yoder did initial work on GPIOmay.py and worked most of it, except event detection.  

# Future Work
The columns are being changed in an update to BBIO, which will mean that the columns of our table will need to be changed to reflact that.  The code should work fine, but maintenance of the code will need to happen if it does not work under any new update.  
# Conclusions
In the near future, there will be a new image for the 4.19 Black kernel that will switch the Consumer and the Name for gpioinfo.  This will remove an error that we had to work around, which will require an update to implement.  Additional functionality will need to be implemented to both the C and the Python library.  

