# -*- coding: utf-8 -*-

from neopixel import *
import logging

import digit, utils

import sys,time



DIGIT_OFFSET_1 = 0
DIGIT_OFFSET_2 = 7
SEPARATOR_OFFSET = 14
DIGIT_OFFSET_3 = 15
DIGIT_OFFSET_4 = 22



class Screen(object):

    """docstring for Screen."""
    def __init__(self,strip, display_offset=0):
        super(Screen, self).__init__()

        self.strip = strip
        self.display_offset = display_offset


        self.digits = []
        self.digits.append(digit.Digit(0,display_offset + DIGIT_OFFSET_1, strip))
        self.digits.append(digit.Digit(1,display_offset + DIGIT_OFFSET_2, strip))
        # Position du point
        self.digits.append(digit.Digit(2,display_offset + DIGIT_OFFSET_3, strip))
        self.digits.append(digit.Digit(3,display_offset + DIGIT_OFFSET_4, strip))

        logging.info("Display created with 4 digits, offset : %d ", display_offset)
        logging.debug(self.digits)

    def set_separator_state(self,state, color=Color(255,0,0)):
        if state:
            self.strip.setPixelColor(self.display_offset + SEPARATOR_OFFSET, color)
        else:
            self.strip.setPixelColor(self.display_offset + SEPARATOR_OFFSET, Color(0,0,0))
        self.strip.show()

    def clear(self):
        logging.info("Clearing display.")
        for d in self.digits:
            d.clear()
        self.set_separator_state(False)


    def display(self, string, color=Color(255,0,0)):
        if len(string) > 4:
            logging.warning("The given string (%s) is wider than the screen, it will be truncated.", string)

        logging.info("Displaying : %s",string[0:4] )

        for i in range(0,4):
            logging.debug("Digit %d set to : %s",i, string[i])
            self.digits[i].write(string[i], color)
