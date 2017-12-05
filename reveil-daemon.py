#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, sys, getopt,time
from datetime import datetime

import display



"""
from : https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""
def args_parse(argv):
    global log_level
    global emulated

    hlp = "reveil-daemon.py [-v|e]"
    try:
        opts, args = getopt.getopt(argv,"hve")
    except getopt.GetoptError:
        print hlp
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print hlp
            sys.exit()
        elif opt == "-v":
            log_level=logging.DEBUG
        elif opt == "-e":
            emulated=True


def init_leds_strip():
    # LED strip configuration:
    LED_COUNT      = 31      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

    return Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)



log_level = logging.INFO
emulated = False


try:
    from neopixel import *
    logging.info("NeoPixel is installed !")
except ImportError:
    pass


    args_parse(sys.argv[1:])
    logging.basicConfig(format='%(asctime)s %(filename)s->%(funcName)s():%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=log_level, filename="log.txt")

    ####################################################################
    #                             Code                                 #
    ####################################################################

    logging.info("Starting configuration")

    ## LEDs Configuration
    if not emulated:
        strip = init_leds_strip()
        strip.begin()
    else:
        strip = 0

    disp = display.Screen(strip, emulated=emulated)

    disp.display("dodo", dots=False)
    time.sleep(2)

    ## Infinite Loop
    time_str=""
    while True:
        old_time_str = time_str
        time_str = datetime.now().strftime("%H%M")

        disp.display(time_str)

        time.sleep(1)
