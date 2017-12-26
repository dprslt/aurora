import colorsys

from strategies.colors.AbstractColor import AbstractColor


class FixedColor(AbstractColor):
    def __init__(self, rgb_color, luminosity=1.0):
        super(FixedColor, self).__init__()
        self.rgb_color = [ int(i * luminosity) for i in rgb_color ]

    def get_current_color(self, minutes_of_day):
        return self.rgb_color

    def get_current_color_hsv(self, minutes_of_day):
        rgb= [i / 255 for i in self.rgb_color]
        return colorsys.hsv_to_rgb(rgb[0], rgb[1], rgb[2])
