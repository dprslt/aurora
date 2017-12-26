import config
import utils
from StoppablePausableThread import StoppablePausableThread
from strategies.colors import OneCyclePerHour
from strategies.time import AbstractTime


class AbstractClock(StoppablePausableThread, AbstractTime):
    def __init__(self, screen, screen_color_strategy=OneCyclePerHour(luminosity_coeff=0.2, value_min_light=0.1)):
        super(AbstractClock, self).__init__()
        self.screen = screen

        self.time_str = ""
        self.color_digit = None

        self.screen_color_strategy = screen_color_strategy

    def refresh(self):
        minutes_of_day = self.compute_minutes_of_day()

        self.color_digit = self.screen_color_strategy.get_current_color(minutes_of_day)
        self.color_digit = utils.convert_rgb_to_Color(self.color_digit)

        with config.strip_lock:
            self.screen.display(self.time_str, color=self.color_digit)

    def work(self):
        raise NotImplementedError()
