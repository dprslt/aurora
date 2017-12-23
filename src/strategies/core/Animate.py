# -*- coding: utf-8 -*-

import logging

import time
from threading import Thread

import animation
import config
from strategies.core.AbstractCore import AbstractCore

from neopixel import *


class Screen(Thread):
    def __init__(self, strip, display):
        Thread.__init__(self)
        self.display = display
        self.strip = strip

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        i = 0

        while True:
            animation.loop_chenillard(self.strip, color=Color(95, 90, 255))
            time.sleep(0.5)
            animation.loop_chenillard_digits(self.strip)
            time.sleep(0.5)


class Top(Thread):
    def __init__(self, strip, top):
        Thread.__init__(self)
        self.top = top
        self.strip = strip

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""

        # Réveil naturel
        l = 0.06
        m = 0.99

        hue = 0.08
        sat = 0.9
        while True:
            self.top.loading()
            self.top.luminosity_gradient(hue, sat, .0, .10, duration=0.5)
            for i in range(0, 5):
                self.top.luminosity_gradient(hue, sat, l, m, duration=3.)
                time.sleep(0.05)
                self.top.luminosity_gradient(hue, sat, m, l, duration=2.)
                time.sleep(0.2)


class AnimateCore(AbstractCore):

    def __init__(self, strip, display, light):
        super(AnimateCore, self).__init__(strip, display, light)


    def play(self):
        ## Infinite Loop
        time_str = ""
        separator_state = False
        rgb_color_digit = None

        logging.info("Running in real time mode")

        # Création des threads
        thread_1 = Screen(self.strip,self.display)
        config.thread_2 = Top(self.strip, self.light)

        # Lancement des threads
        thread_1.start()
        config.thread_2.start()

        # Attend que les threads se terminent
        thread_1.join()
        config.thread_2.join()
