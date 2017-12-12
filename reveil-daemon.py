#!/usr/bin/python
# -*- coding: utf-8 -*-

from neopixel import *

import logging, sys, getopt,time

from datetime import datetime

import display, animation, utils, couleurs



"""
from : https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""
def args_parse(argv):
    global log_level

    hlp = "reveil-daemon.py [-v]"
    try:
        opts, args = getopt.getopt(argv,"hv")
    except getopt.GetoptError:
        print hlp
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print hlp
            sys.exit()
        elif opt == "-v":
            log_level=logging.DEBUG



def init_leds_strip():
    # LED strip configuration:
    LED_COUNT      = 31      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 25     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

    return Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)



log_level = logging.INFO



if __name__ == '__main__':

    args_parse(sys.argv[1:])
    logging.basicConfig(format='%(asctime)s %(filename)s->%(funcName)s():%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=log_level, filename="log.txt")

    ####################################################################
    #                             Code                                 #
    ####################################################################

    logging.info("Starting configuration")

    ## LEDs Configuration
    strip = init_leds_strip()
    strip.begin()

    disp = display.Screen(strip)

    disp.display("dodo")
    time.sleep(1)
    disp.clear()

    # animation.loop_chenillard_digits(strip, Color(50,130,255))

    ## Infinite Loop
    time_str = ""
    separator_state = False
    while True:
        old_time_str = time_str
        time_str = datetime.now().strftime("%H%M")


        # TODO tester

        hours = int(time_str[0:2])
        minutes = int(time_str[2:4])

        minutes_of_day = hours * 60 + minutes
        rgb_color = couleurs.compute_color(minutes_of_day)
        color = utils.convert_rgb_to_Color(rgb_color)


        if not old_time_str == time_str:
            disp.display(time_str, color=color)


        disp.set_separator_state(separator_state, color)
        separator_state = not separator_state

        time.sleep(1)
