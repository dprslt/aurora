from neopixel import *

import colorsys

def led_off(strip,address):
    strip.setPixelColor(address, Color(0,0,0))
    strip.show()


def convert_rgb_to_Color(rgb):
    return Color(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def hsv_to_Color(h,s,v):
    rgb =  [ int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v) ]
    return convert_rgb_to_Color(rgb)
