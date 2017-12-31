import logging

import time

import config
import utils
from StoppablePausableThread import StoppablePausableThread
from strategies.time.RealTime import RealTime


class SimpleColor(StoppablePausableThread, RealTime):
    def __init__(self, light, color_strategy, paused = False):

        super(SimpleColor, self).__init__()
        self.light = light
        self.color_strategy = color_strategy

        self.step_counter = 0
        self.sleeping_time = 0.2

        if paused:
            self.paused.clear()

    def run(self):
        logging.info("LIGHT : Simple Color mode")
        super(SimpleColor, self).run()

    def work(self):
        minutes_of_day = self.compute_minutes_of_day()
        light_color = self.color_strategy.get_current_color(minutes_of_day)
        light_color = utils.convert_rgb_to_Color(light_color)
        with config.strip_lock:
            self.light.show_color(light_color)

        time.sleep(self.sleeping_time)
