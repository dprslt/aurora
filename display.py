# -*- coding: utf-8 -*-

import logging
import digit

import sys

try:
    from neopixel import *
except ImportError:
    pass



DIGIT_OFFSET_1 = 0
DIGIT_OFFSET_2 = 7
SEPARATOR_OFFSET = 14
DIGIT_OFFSET_3 = 15
DIGIT_OFFSET_4 = 22



class Screen(object):

    """docstring for Screen."""
    def __init__(self,strip, emulated=False, display_offset=0):
        super(Screen, self).__init__()

        self.strip = strip
        self.emulated = emulated
        self.display_offset = display_offset


        self.digits = []
        self.digits.append(digit.Digit(0,display_offset + DIGIT_OFFSET_1, strip, emulated=emulated))
        self.digits.append(digit.Digit(1,display_offset + DIGIT_OFFSET_2, strip, emulated=emulated))
        # Position du point
        self.digits.append(digit.Digit(2,display_offset + DIGIT_OFFSET_3, strip, emulated=emulated))
        self.digits.append(digit.Digit(3,display_offset + DIGIT_OFFSET_4, strip, emulated=emulated))

        logging.info("Display created with 4 digits, emulated:%s ", emulated)
        logging.debug(self.digits)

    def set_separator_state(state):
        if self.emulated:
            return

        if state:
            self.strip.setPixelColor(self.display_offset + SEPARATOR_OFFSET, Color(255,0,0)) # TODO Deal with color
        else:
            self.strip.setPixelColor(self.display_offset + SEPARATOR_OFFSET, Color(0,0,0))




    def display(self, string, dots=True):
        if len(string) > 4:
            logging.warning("The given string (%s) is wider than the screen, it will be truncated.", string)

        logging.info("Displaying : %s%s%s",string[0:2],":" if dots else "",string[2:4] )

        if self.emulated:
            matrix_displays = []
            s = []
            for i in range(0,4):
                matrix_displays.append(digit.characters_map[string[i]])
                s.append(list(map(lambda x: 'X' if x else ' ' , matrix_displays[i])))

            dots_full= "     "
            dots_empty="     "
            if dots:
                dots_full="  -  "

            print ' ' , s[0][4] , ' ', '  ', ' ' , s[1][4] , ' ', dots_empty , ' ' , s[2][4] , ' ', '  ', ' ' , s[3][4] , ' '
            print s[0][0],' ',s[0][5], '  ', s[1][0],' ',s[1][5], dots_full , s[2][0],' ',s[2][5], '  ', s[3][0],' ',s[3][5]
            print ' ' , s[0][3] , ' ', '  ', ' ' , s[1][3] , ' ', dots_empty , ' ' , s[2][3] , ' ', '  ', ' ' , s[3][3] , ' '
            print s[0][1],' ',s[0][6], '  ', s[1][1],' ',s[1][6], dots_full , s[2][1],' ',s[2][6], '  ', s[3][1],' ',s[3][6]
            print ' ' , s[0][2] , ' ', '  ', ' ' , s[1][2] , ' ', dots_empty , ' ' , s[2][2] , ' ', '  ', ' ' , s[3][2] , ' '

            sys.stdout.write("\033[F\033[F\033[F\033[F\033[F") # Cursor up five line

        else:
            # Todo dots

            for i in range(0,4):
                logging.debug("Digit %d set to : %s",i, string[i])
                self.digits[i].write(string[i])
