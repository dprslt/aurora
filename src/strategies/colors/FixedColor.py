from strategies.colors.AbstractColor import AbstractColor


class FixedColor(AbstractColor):
    def __init__(self, rgb_color):
        super(FixedColor, self).__init__()
        self.rgb_color = rgb_color

    def get_current_color(self, minutes_of_day):
        return self.rgb_color
