from threading import Thread, RLock, Event

import time

import signal

import logging

from datetime import datetime

import config
import utils
from strategies.colors.OneCyclePerHour import OneCyclePerHour
from strategies.core.PausableThread import PausableThread
from strategies.screen.AbstractClock import AbstractClock

lock = RLock()


class DisplayMessage(PausableThread):
    def __init__(self, strip, screen, message, duration=1,
                 screen_color_strategy=OneCyclePerHour(luminosity_coeff=0.2, value_min_light=0.1)):
        super(DisplayMessage, self).__init__()

        self.strip = strip
        self.screen = screen

        self.screen_color_strategy = screen_color_strategy

        self.message = message
        self.duration = duration

        self.step = 0

        self.pause_time = 0.2
        self.time_str = ""

    def run(self):
        logging.info("SCREEN : Displaying %s for %d s", self.message, self.duration)
        with config.strip_lock:
            self.screen.clear()
        super(DisplayMessage, self).run()

    def work(self):

        self.time_str = datetime.now().strftime("%H%M")
        hours = int(self.time_str[0:2])
        minutes = int(self.time_str[2:4])
        minutes_of_day = hours * 60 + minutes
        with config.strip_lock:
            self.screen.display(self.message, color=utils.convert_rgb_to_Color(
                self.screen_color_strategy.get_current_color(minutes_of_day)))

        self.step = self.step + 1

        if self.step * self.pause_time == self.duration:
            self.stop()

        time.sleep(self.pause_time)
