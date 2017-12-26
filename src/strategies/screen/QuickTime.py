import logging
import time

import config
from strategies.colors.OneCyclePerHour import OneCyclePerHour
from strategies.screen.AbstractClock import AbstractClock


class QuickTime(AbstractClock):
    def __init__(self, screen, screen_color_strategy=OneCyclePerHour(luminosity_coeff=0.2, value_min_light=0.1)):
        AbstractClock.__init__(self, screen, screen_color_strategy)

        self.separator_state = False
        self.step_counter = 0
        self.sleeping_time = 0.02


    def run(self):
        logging.info("SCREEN : Clock Quick Time mode")

        super(QuickTime, self).run()

    def work(self):
        hours = int(self.step_counter / 60)
        minutes = int(self.step_counter % 60)

        self.time_str = "{h:02d}{m:02d}".format(h=hours, m=minutes)

        with config.strip_lock:
            self.refresh()

        self.step_counter = (self.step_counter + 1) % 1440

        time.sleep(self.sleeping_time)

    def compute_minutes_of_day(self):
        return self.step_counter
