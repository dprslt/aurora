import logging

import time

import config
import utils
from StoppablePausableThread import StoppablePausableThread
from strategies.colors.OneCyclePerHour import OneCyclePerHour
from strategies.time.RealTime import RealTime



class TurnedOff(StoppablePausableThread):
    def __init__(self, light):
        super(TurnedOff, self).__init__()
        self.light = light

        self.sleeping_time = 0.5

    def run(self):
        logging.info("LIGHT : Turned off")
        with config.strip_lock:
            self.light.clear()
        super(TurnedOff, self).run()

    def work(self):
        time.sleep(self.sleeping_time)
