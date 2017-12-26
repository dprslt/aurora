from neopixel import *

import colorsys, math


def led_off(strip, address):
    strip.setPixelColor(address, Color(0, 0, 0))
    strip.show()


def convert_rgb_to_Color(rgb):
    return Color(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def hsv_to_Color(h, s, v):
    rgb = [int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v)]
    return convert_rgb_to_Color(rgb)


def tr_sig(x):
    if x <= 0.001:
        return 0.
    if x >= 0.999:
        return 1.
    return 1 / (1 + math.exp(-12 * (x - 0.45)))

def tr_cos(x):
    if x <= 0.001:
        return 0.
    if x >= 0.999:
        return 1
    return  0.5 * math.cos(math.pi * (x + 1)) + 0.5
