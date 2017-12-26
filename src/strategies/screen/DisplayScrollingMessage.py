import logging
import time

import config
import utils
from StoppablePausableThread import StoppablePausableThread
from strategies.colors.OneCyclePerHour import OneCyclePerHour
from strategies.time.RealTime import RealTime


class DisplayScrollingMessage(StoppablePausableThread, RealTime):
    def __init__(self, screen, message, duration=1,
                 screen_color_strategy=OneCyclePerHour(luminosity_coeff=0.2, value_min_light=0.1)):
        super(DisplayScrollingMessage, self).__init__()

        self.screen = screen

        self.screen_color_strategy = screen_color_strategy

        self.message = "    "+message+"    "
        self.duration = duration

        self.step = 0

    def run(self):
        logging.info("SCREEN : Displaying %s at a speed of   %d s", self.message, self.duration)
        with config.strip_lock:
            self.screen.clear()
        super(DisplayScrollingMessage, self).run()

    def work(self):

        minutes_of_day = self.compute_minutes_of_day()

        with config.strip_lock:
            self.screen.display(self.message[self.step:self.step+4], color=utils.convert_rgb_to_Color(
                self.screen_color_strategy.get_current_color(minutes_of_day)))

        self.step = self.step + 1

        if self.step * self.duration == (len(self.message)-3) * self.duration:
            self.stop()

        time.sleep(self.duration / len(self.message))
