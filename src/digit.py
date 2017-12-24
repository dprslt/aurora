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
    "0": [True, True, True, False, True, True, True],
    "1": [False, False, False, False, False, True, True],
    "2": [False, True, True, True, True, True, False],
    "3": [False, False, True, True, True, True, True],
    "4": [True, False, False, True, False, True, True],
    "5": [True, False, True, True, True, False, True],
    "6": [True, True, True, True, True, False, True],
    "7": [False, False, False, False, True, True, True],
    "8": [True, True, True, True, True, True, True],
    "9": [True, False, True, True, True, True, True],
    "c": [False, True, True, True, False, False, False],
    "o": [False, True, True, True, False, False, True],
    "i": [False, False, False, False, False, False, True],
    "I": [False, False, False, False, False, True, True],
    "b": [True, True, True, True, False, False, True],
    "d": [False, True, True, True, False, True, True],
    "O": [True, True, True, False, True, True, True],
    "-": [False, False, False, True, False, False, False],
    "J": [False, True, True, False, False, True, True],
    "u": [False, True, True, False, False, False, True],
    "U": [True, True, True, False, False, True, True],
    "P": [True, True, False, True, True, True, False],

}

"""Ce masque permet de permuter les positions entre les digits pairs et impairs"""
mask_permutation = [1, 0, 4, 3, 2, 6, 5]

from neopixel import *
import logging

import utils


class Digit(object):
    """docstring for Digit."""

    def __init__(self, index, offset_addr, strip):
        super(Digit, self).__init__()
        self.index = index
        self.offset_addr = offset_addr
        self.strip = strip

        logging.info("New Digit created, index: %d, offset_addr: %d", self.index, self.offset_addr)

    def write(self, char, color=(255, 0, 0)):
        if char not in characters_map:
            logging.warning(
                "Error displaying : %s not found in dictionnay, it's probably not possible to print it on a 7 segments display",
                char)
            return

        self._led_output(char, color)

    def clear(self):
        logging.debug("Digit %d : clear", self.index)
        for i in range(0, 7):
            self.strip.setPixelColor(self.offset_addr + i, Color(0, 0, 0))
        self.strip.show()

    def _compute_permut(self, matrix):
        arr = [False, False, False, False, False, False, False]

        if self.index == 0 or self.index == 3:
            return matrix

        for i, c in enumerate(matrix):
            arr[mask_permutation[i]] = c

        return arr

    def _led_output(self, char, color=Color(255, 0, 0)):

        matrix_display = characters_map[char]
        logging.debug(matrix_display)
        matrix_display = self._compute_permut(matrix_display)
        logging.debug(matrix_display)

        for index, value in enumerate(matrix_display):
            if not value:
                self.strip.setPixelColor(self.offset_addr + index, Color(0, 0, 0))
            else:
                self.strip.setPixelColor(self.offset_addr + index, color)

        self.strip.show()
