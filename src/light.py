#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time

import numpy as np
from neopixel import *

import utils


class Light(object):
    def __init__(self, strip, top_offset=29, top_strip_length=27, top_center_length=4):
        super(Light, self).__init__()

        self.strip = strip
        self.top_offset = top_offset
        self.top_strip_length = top_strip_length
        self.top_center_length = top_center_length
        self.powered = True

    def set_powered(self, powered):
        logging.info("Light power set to : %s", powered)
        if self.powered == powered:
            return

        if not powered  :
            self.clear()

        self.powered = powered

    def show_color(self, color=Color(220, 200, 255)):
        if not self.powered:
            return

        logging.debug("Changing top color")
        for i in range(self.top_offset, self.top_offset + self.top_strip_length + self.top_center_length):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def clear(self):
        logging.info("Cleaning top")
        for i in range(self.top_offset, self.top_offset + self.top_strip_length + self.top_center_length):
            utils.led_off(self.strip, i)

        self.strip.show()

    def loading(self, times=5, queue=10):
        if not self.powered:
            return

        for i in range(0, self.top_strip_length * times):

            for q in range(0, queue):
                if (i < q):
                    continue
                self.strip.setPixelColor(self.top_offset + ((i - q) % self.top_strip_length), utils.hsv_to_Color(
                    ((i - q) % self.top_strip_length) / float(self.top_strip_length), 0.8, (queue - q) / float(queue)))

            utils.led_off(self.strip, self.top_offset + ((i - queue) % self.top_strip_length))

            time.sleep(0.05)
            self.strip.show()

        for q in range(0, queue):
            utils.led_off(self.strip, self.top_offset + self.top_strip_length - (queue - q))

    def center_dot(self, color=Color(255, 0, 0)):
        if not self.powered:
            return

        for i in range(self.top_offset + self.top_strip_length,
                       self.top_offset + self.top_strip_length + self.top_center_length):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def luminosity_gradient(self, hue, sat, value_from, value_target, duration=1., frequency=60):
        if not self.powered:
            return

        min_val = min(value_from, value_target)
        max_val = max(value_from, value_target)

        steps = np.arange(0., 1., 1 / float(frequency * duration))
        if value_target < value_from:
            steps = np.flip(steps, 0)

        for step in steps:
            current_value = min_val + utils.tr_sig(step) * (max_val - min_val)
            self.show_color(utils.hsv_to_Color(hue, sat, current_value))
            time.sleep(1 / float(frequency))


if __name__ == '__main__':

    # LED strip configuration:
    LED_COUNT = 60  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 5  # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 240  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
                              LED_STRIP)
    strip.begin()

    t = Light(strip=strip)

    # t.loading(times=5)
    # t.show_color(Color(90,90,255))
    # time.sleep(0.5)
    # t.center_dot()
    # time.sleep(1)
    t.clear()

    # Réveil naturel
    l = 0.06
    m = 0.99

    hue = 0.08
    sat = 0.9

    t.luminosity_gradient(hue, sat, .0, .10, duration=0.5)
    for i in range(0, 5):
        t.luminosity_gradient(hue, sat, l, m, duration=3.)
        time.sleep(0.05)
        t.luminosity_gradient(hue, sat, m, l, duration=2.)
        time.sleep(0.2)

    t.clear()
