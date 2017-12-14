#!/usr/bin/python
# -*- coding: utf-8 -*-

from neopixel import *

import logging, time

import utils



class Top(object):

    def __init__(self,strip, top_offset=29, top_length=27):
        super(Top, self).__init__()

        self.strip = strip
        self.top_offset = top_offset
        self.top_length = top_length



    def show_color(self, color=Color(220,200,255)):
        logging.debug("Changing top color")
        for i in range(self.top_offset, self.top_offset + self.top_length):
            self.strip.setPixelColor(i,color)

        self.strip.show()

    def clear(self):
        logging.info("Cleaning top")
        for i in range(self.top_offset, self.top_offset + self.top_length):
            utils.led_off(self.strip, i)

        self.strip.show()

    def loading(self, times=5):
        queue = 10

        for i in range(0, self.top_length * times):



            for q in range(0, queue):

                if (i < q):
                    continue

                self.strip.setPixelColor(self.top_offset + ((i - q) % self.top_length), utils.hsv_to_Color( ((i-q)  % self.top_length)/float(self.top_length ), 0.8, (queue-q)/float(queue) ))

            utils.led_off(self.strip, self.top_offset + ((i - queue) % self.top_length))


            time.sleep(0.05)
            self.strip.show()

        for q in range(0, queue):
            utils.led_off(self.strip, self.top_offset + self.top_length - (queue - q) )




if __name__ == '__main__':

    # LED strip configuration:
    LED_COUNT      = 56      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()

    t = Top(strip=strip)

    t.loading(10)
