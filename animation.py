
#    4        9            17        26
# 0     5  8    13      16    21  22     27
#    3       10     14     18        25
# 1     6  7    12      15    20  23     28
#    2       11            19        24

import logging, time

from neopixel import *
import utils

def loop_chenillard(strip, color=Color(255,0,0)):
    delay_chenillard = 0.10
    for i in range(0,20):
        chenillard(strip, Color(0,128,255), delay_chenillard)
        delay_chenillard *= 0.6

def loop_chenillard_digits(strip, color=Color(255,0,0)):
    delay_chenillard = 0.10
    for i in range(0,50):
        chenillard_digit(strip, Color(0,128,50), delay_chenillard)
        delay_chenillard *= 0.90

def chenillard(strip, color=Color(255,0,0), delay=0.2):
    logging.info("Animation chenillard is running !")
    offset = 0
    segments = [0, 1, 2, 11, 19, 24, 28, 27, 26, 17, 9, 4]

    old_seg = -1

    for i in range(0,29):
        utils.led_off(strip, offset + i)

    strip.show()


    for seg in segments:
        if old_seg >= 0:
            utils.led_off(strip, offset + old_seg)

        strip.setPixelColor(offset + seg, color)
        old_seg = seg

        strip.show()

        time.sleep(delay)

    utils.led_off(strip, offset + old_seg)

def chenillard_digit(strip, color=Color(255,0,0), delay=0.2):
    logging.info("Animation chenillard_digit is running !")
    offset = 0
    digits_segments = [
        [0, 1, 2, 6, 5, 4],
        [8, 7, 11, 12, 13, 9],
        [16, 15, 19, 20, 21, 17],
        [22, 23, 24, 28, 27, 26],
    ]

    olds = [-1, -1, -1, -1]
    for i in range(0,len(digits_segments[0])):
        for d in range(0,4):
            if olds[d] >= 0:
                strip.setPixelColor(offset + olds[d], Color(0,0,0))

            strip.setPixelColor(offset + digits_segments[d][i], color)
            olds[d] = digits_segments[d][i]

        strip.show()
        time.sleep(delay)

    for d in range(0,4):
        strip.setPixelColor(offset + olds[d], Color(0,0,0))
    strip.show()
