import utils
from strategies.core.AbstractCore import AbstractCore


class AbstractTimeCore(AbstractCore):

    def __init__(self, strip, display, light):
        super(AbstractTimeCore, self).__init__(strip, display, light)
        self.need_refresh=False
        self.time_str=""
        self.color_digit = None

    def refresh(self):
        if self.need_refresh:
            self.need_refresh = False

        minutes_of_day = self.compute_minutes_of_day()

        self.color_digit = self.screen_color_strategy.get_current_color(minutes_of_day)
        self.color_digit = utils.convert_rgb_to_Color(self.color_digit)
        color_top = self.light_color_strategy.get_current_color(minutes_of_day)
        color_top = utils.convert_rgb_to_Color(color_top)

        self.display.display(self.time_str, color=self.color_digit)
        self.light.show_color(color_top)

    def compute_minutes_of_day(self):
        raise NotImplementedError()

