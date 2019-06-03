#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import time, math, colorsys, logging

from strategies.colors.AbstractColor import AbstractColor

DAY_LENTGH = 1440.0


class OneCyclePerHourNightMode(AbstractColor):


    def __init__(self, saturation_min=0.95, value_min_light=0.10, night_from=22, night_to=9, luminosity_coeff=1,
                 color_offset=0.5, full_night_hour=4):
        super(OneCyclePerHourNightMode, self).__init__()
        self.color_offset = color_offset
        self.luminosity_coeff = luminosity_coeff
        self.night_from = night_from
        self.night_to = night_to
        self.full_night_hour = full_night_hour
        self.value_min_light = value_min_light
        self.saturation_min = saturation_min

    def get_current_color(self, minutes_of_day):
        hsv = self.get_current_color_hsv(minutes_of_day)

        # Convertion en RGB sur base 255
        return [int(i * 255) for i in colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])]

    def get_current_color_hsv(self, minutes_of_day):
        full_night_hour = max(min(self.full_night_hour, 24), 0)
        # Calcul de la position de l'heure la plus basse
        # 0.25 correspond au delta pour placer le min de la courbe à 0
        value_phase = (full_night_hour / 24.0 + 0.25)

        # Vérification et correction de la valeur des coefficients
        luminosity_coeff = max(min(self.luminosity_coeff, 1), 0)
        saturation_min = max(min(self.saturation_min, 1), 0)
        value_min_light = max(min(self.value_min_light, 1), 0)

        # Ecriture des valeurs hsv
        h = (15 * minutes_of_day / DAY_LENTGH) + self.color_offset % 1
        s = saturation_min + (
            0.5 * (1 - saturation_min) * (math.cos((minutes_of_day / (DAY_LENTGH / 15.)) * 2 * math.pi) + 1))
        if minutes_of_day > (self.night_from * 60) or minutes_of_day < (self.night_to * 60) :
            h = 0
            v = value_min_light
        else :
            v = 1 * luminosity_coeff

        return [h, s, v]


if __name__ == '__main__':
    from PIL import Image

    data = np.zeros((64, 64, 3), dtype=np.uint8)
    step = 0

    color = OneCyclePerHour()

    while True:
        r, g, b = color.get_current_color(step)

        hour = step / 60
        minutes = step % 60

        print (step, " - ", hour, "h", minutes, " : ", (r, g, b))

        data[:, :, 0] = int(r)
        data[:, :, 1] = int(g)
        data[:, :, 2] = int(b)

        img = Image.fromarray(data, 'RGB')
        img.save('render.png')

        step = (step + 1) % 1440

        time.sleep(0.01)
