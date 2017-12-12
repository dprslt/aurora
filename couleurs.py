#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import time,math, colorsys

DAY_LENTGH = 1440.0


def compute_color(minute_of_the_day, saturation_min = 0.25, value_min_light = 0.25, value_phase=0.33 ):

    h = (2 * step / DAY_LENTGH) % 1
    s = saturation_min + (0.5 * (1 - saturation_min) * (math.cos((step / (DAY_LENTGH / 2.)) * 2 *math.pi)+1))
    v = value_min_light + (0.5 * (1 - value_min_light) * (math.cos( ((step + DAY_LENTGH * value_phase)/(DAY_LENTGH)) * 2 * math.pi)+1))

    return [ int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v) ]


if __name__ == '__main__':
    from PIL import Image

    data = np.zeros((64,64,3), dtype=np.uint8)
    step = 0
    while True:

        r, g, b = compute_color(step)

        hour = step / 60
        minutes = step % 60

        print step, " - ", hour,"h",minutes," : ",(r,g,b)

        data[:,:,0] = int(r)
        data[:,:,1] = int(g)
        data[:,:,2] = int(b)

        img = Image.fromarray(data,'RGB')
        img.save('render.png')

        step = (step + 1) % 1440

        time.sleep(0.01)
