# -*- coding: utf-8 -*-

"""
Liste des digits affichables
Les segments sont numérotés comme suit :

- 4 -
0   5
| 3 |
1   6
- 2 -

Attention un pixel sur deux est mappé dans l'autre sens :

- 2 -
1   6
| 3 |
0   5
- 4 -

"""
characters_map = {
	"0" : [True, True, True, False, True, True, True],
	"1" : [False, False, False, False, False, True, True],
	"2" : [False, True, True, True, True, True, False],
	"3" : [False, False, True, True, True, True, True],
	"4" : [True, False, False, True, False, True, True],
	"5" : [True, False, True, True, True, False, True],
	"6" : [True, True, True, True, True, False, True],
	"7" : [False, False, False, False, True, True, True],
	"8" : [True, True, True, True, True, True, True],
	"9" : [True, False, True, True, True, True, True],
	"c" : [False, True, True, True, False, False, False],
	"o" : [False, True, True, True, False, False, True],
	"i" : [False, False, False, False, False, False, True],
	"I" : [False, False, False, False, False, True, True],
	"b" : [True, True, True, True, False, False, True],
	"d" : [False, True, True, True, False, True, True],
	"O" : [True, True, True, False, True, True, True],

    }

"""Ce masque permet de permuter les positions entre les digits pairs et impairs"""
mask_permutation = [1,0,4,3,2,6,5]


import logging

try:
    from neopixel import *
except ImportError:
    pass

class Digit(object):

    """docstring for Digit."""
    def __init__(self, index, offset_addr, strip, emulated=False):
        super(Digit, self).__init__()
        self.index = index
        self.offset_addr = offset_addr
        self.strip = strip
        self.emulated = emulated

        logging.info("New Digit created, index: %d, offset_addr: %d, emulated:%s", self.index, self.offset_addr, self.emulated)

    def write(self, char, color=(255,0,0)):
        if char not in characters_map:
            logging.warning("Error displaying : %s not found in dictionnay, it's probably not possible to print if on a 7 segments display",char)
            return

        if self.emulated:
            self._console_output(char)
        else:
            self._led_output(char,color)

    def _compute_permut(self, matrix):
        arr = [False,False,False,False,False,False,False]

        if self.index % 2 == 0 :
            return matrix

        for i, c in enumerate(matrix):
            arr[mask_permutation[i]] = c

        return arr

    def _console_output(self, char, color=(255,0,0)):

        matrix_display = characters_map[char]
        logging.debug(matrix_display)

        s = list(map(lambda x: 'X' if x else ' ' , matrix_display))
        logging.debug(s)

        print ' ',s[4],' '
        print s[0],' ',s[5]
        print ' ',s[3],' '
        print s[1],' ',s[6]
        print ' ',s[2],' '


    def _led_output(self, char, color=(255,0,0)):

        # Import neo pixel

        matrix_display = characters_map[char]
        logging.debug(matrix_display)
        matrix_display = self._compute_permut(matrix_display)
        logging.debug(matrix_display)

        for index, value in enumerate(matrix_display):
            if value :
                neo_color = Color(0,0,0)
            else :
                neo_color = Color(color[0], color[1], color[2])

            self.strip.setPixelColor(self.offset_addr + index, neo_color)

        self.strip.show()
