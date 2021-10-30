#!/usr/bin/python
# -*- coding: utf-8 -*-

import getopt
import logging
import signal
import sys

import RPi.GPIO as GPIO
import time
from neopixel import *

import config
import display
import light
from Scheduler import Scheduler
from strategies.buttons import ToogleLight, register_buttons
from strategies.buttons.NavigateModes import NavigateModes
from strategies.core import get_display_strategy
# LED strip configuration:
from strategies.light.Breath import Breath
from strategies.light.Loading import Loading
from strategies.light.SimpleRealTimeColor import SimpleRealTimeColor
from strategies.light.TurnedOff import TurnedOff
from strategies.screen.DisplayMessage import DisplayMessage
from strategies.screen.DisplayScrollingMessage import DisplayScrollingMessage
from strategies.screen.RealClockTime import RealClockTime
import rest_api


LED_COUNT = 60  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 5)
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
        print (hlp)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(hlp)
            sys.exit()
        elif opt == "-v":
            config.log_level = logging.DEBUG
        elif opt == "-q":
            config.display_strategy_name = "quick"
        elif opt == "-a":
            config.display_strategy_name = "anim"


def exit_handler(signum, frame):
    global disp, strip, rest_server_thread

    logging.info("Exiting on SIGTERM ..")

    config.scheduler.stop()

    with config.strip_lock:
        disp.clear()
        top_light.clear()

    rest_server_thread.shutdown()
    # rest_server.kill()
    # rest_server.join()


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

    ## Buttons configuration

    register_buttons(top_light, disp)

    logging.info("Installing handlers")
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    config.scheduler = Scheduler()
    # Starting boot routine
    config.scheduler.set_screen_thread(DisplayScrollingMessage(screen=disp, message="BOOOOOOOE",duration=2))
    config.scheduler.set_light_thread(Loading(top_light))
    time.sleep(1)
    config.scheduler.set_screen_thread(DisplayMessage(screen=disp, message="v1-3"))
    time.sleep(1)


    config.scheduler.set_screen_thread(RealClockTime(disp))
    time.sleep(0.5)
    config.scheduler.set_light_thread(SimpleRealTimeColor(top_light, paused=True))
    config.scheduler.toogle_light(top_light)
    
    rest_server_thread = rest_api.start_rest_server(light=top_light, disp=disp)
    # rest_server = rest_api.start_rest_server(light=top_light, disp=disp)

    config.scheduler.start()

    # time.sleep(3)

    # config.scheduler.temporary_switch_screen_thread(DisplayMessage(disp, "6666", 10, FixedColor([255, 0, 0], 0.1)))

    config.scheduler.join(1)
