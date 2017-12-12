from neopixel import *


def led_off(strip,address):
    strip.setPixelColor(address, Color(0,0,0))
    strip.show()


def convert_rgb_to_Color(rgb):
    return Color(rgb[0], rgb[1], rgb[2])
