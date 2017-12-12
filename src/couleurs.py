#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import time, math, colorsys, logging

DAY_LENTGH = 1440.0


def compute_color(minute_of_the_day, saturation_min = 0.25, value_min_light = 0.25, full_night_hour=4, luminosity_coeff=1):

    full_night_hour = max(min(full_night_hour,24),0)
    # Calcul de la position de l'heure la plus basse
    # 0.25 correspond au delta pour placer le min de la courbe à 0
    value_phase = (full_night_hour/24.0 + 0.25)

    # Vérification et correction de la valeur des coefficients
    luminosity_coeff = max(min(luminosity_coeff, 1),0)
    saturation_min = max(min(saturation_min, 1),0)
    value_min_light = max(min(value_min_light, 1),0)

    h = (2 * minute_of_the_day / DAY_LENTGH) % 1
    s = saturation_min + (0.5 * (1 - saturation_min) * (math.cos((minute_of_the_day / (DAY_LENTGH / 2.)) * 2 *math.pi)+1))
    v = value_min_light + (0.5 * (1 - value_min_light) * (math.sin( ((minute_of_the_day - DAY_LENTGH * value_phase)/(DAY_LENTGH)) * 2 * math.pi)+1))
    v *= luminosity_coeff

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
