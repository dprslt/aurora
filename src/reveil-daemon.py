#!/usr/bin/python
# -*- coding: utf-8 -*-

import getopt
import logging
import signal
import sys
import time

from neopixel import *
import RPi.GPIO as GPIO

import config
import display
import light

from strategies.core import get_display_strategy
from strategies.buttons import ToogleLight

# LED strip configuration:
LED_COUNT = 60  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering


def init_leds_strip():
    return Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
                             LED_STRIP)


"""
from : https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""


def args_parse(argv):
    hlp = "reveil-daemon.py [-vqa]"
    try:
        opts, args = getopt.getopt(argv, "hvqa")
    except getopt.GetoptError:
        print hlp
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print hlp
            sys.exit()
        elif opt == "-v":
            config.log_level = logging.DEBUG
        elif opt == "-q":
            config.display_strategy_name = "quick"
        elif opt == "-a":
            config.display_strategy_name = "anim"


def exit_handler(signum, frame):
    global disp, strip

    logging.info("Exiting on SIGTERM ..")
    disp.clear()
    top_light.clear()
    exit()


if __name__ == '__main__':
    args_parse(sys.argv[1:])
    logging.basicConfig(format='%(asctime)s %(filename)s->%(funcName)s():%(lineno)d %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=config.log_level,  # filename="log.txt"
                        )

    ####################################################################
    #                             Code                                 #
    ####################################################################

    logging.info("Starting configuration")
    ## LEDs Configuration
    strip = init_leds_strip()
    strip.begin()

    disp = display.Screen(strip)
    top_light = light.Light(strip, top_offset=29)

    logging.info("Pulling display strategy for name %s", config.display_strategy_name)
    config.core_strategy = get_display_strategy(config.display_strategy_name, strip, disp, top_light)

    ## Buttons configuration

    but1 = ToogleLight(top_light)
    but1.register(23, pull_up_down=GPIO.PUD_UP)


    logging.info("Installing handlers")
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)


    disp.display("dodo")
    time.sleep(1)
    disp.clear()

    config.core_strategy.play()
