#!/usr/bin/python
# -*- coding: utf-8 -*-

from neopixel import *

import logging, sys, getopt, time, signal

from datetime import datetime

import display, animation, utils, couleurs


def init_leds_strip():
    # LED strip configuration:
    LED_COUNT      = 31      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

    return Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)



def quick_time():
    ## Infinite Loop
    time_str = ""

    logging.info("Running in quick time mode")

    st = 0
    while True:
        old_time_str = time_str


        hours = st / 60
        minutes = st % 60

        time_str = "{h:02d}{m:02d}".format(h=hours, m=minutes)


        if not old_time_str == time_str:
            minutes_of_day = hours * 60 + minutes
            rgb_color = couleurs.compute_color(minutes_of_day,value_min_light = 0.10)
            color = utils.convert_rgb_to_Color(rgb_color)

            disp.display(time_str, color=color)

        st = (st+10)%1440

        time.sleep(0.1)

def real_time():
    ## Infinite Loop
    time_str = ""
    separator_state = False

    logging.info("Running in real time mode")

    while True:
        old_time_str = time_str
        time_str = datetime.now().strftime("%H%M")

        if not old_time_str == time_str:
            hours = int(time_str[0:2])
            minutes = int(time_str[2:4])

            minutes_of_day = hours * 60 + minutes
            rgb_color = couleurs.compute_color(minutes_of_day)
            color = utils.convert_rgb_to_Color(rgb_color)

            disp.display(time_str, color=color)


        disp.set_separator_state(separator_state, color)
        separator_state = not separator_state

        time.sleep(1)

log_level = logging.INFO
time_function = real_time

"""
from : https://www.tutorialspoint.com/python/python_command_line_arguments.htm
"""
def args_parse(argv):
    global log_level, time_function

    hlp = "reveil-daemon.py [-vq]"
    try:
        opts, args = getopt.getopt(argv,"hvq")
    except getopt.GetoptError:
        print hlp
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print hlp
            sys.exit()
        elif opt == "-v":
            log_level=logging.DEBUG
        elif opt == "-q":
            time_function = quick_time


disp = None
strip = None

def exit_handler(signum, frame):
    global disp, strip

    logging.info("Exiting on SIGTERM ..")
    disp.clear()
    exit()


if __name__ == '__main__':


    args_parse(sys.argv[1:])
    logging.basicConfig(format='%(asctime)s %(filename)s->%(funcName)s():%(lineno)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=log_level, #filename="log.txt"
                    )

    # log_stdout = logging.StreamHandler()
    # log_stdout.setLevel(log_level)
    # log_stdout.setFormatter(logging.Formatter('%(asctime)s %(filename)s->%(funcName)s():%(lineno)d %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S'))
    # logging.getLogger().addHandler(log_stdout)

    ####################################################################
    #                             Code                                 #
    ####################################################################

    logging.info("Starting configuration")

    ## LEDs Configuration
    strip = init_leds_strip()
    strip.begin()

    disp = display.Screen(strip)

    logging.info("Installing handlers")
    signal.signal(signal.SIGTERM, exit_handler)

    disp.display("dodo")
    time.sleep(1)
    disp.clear()

    # animation.loop_chenillard_digits(strip, Color(50,130,255))

    # TODO A testersh
    time_function()
