from neopixel import *


def led_off(strip,address):
    strip.setPixelColor(address, Color(0,0,0))
    strip.show()
