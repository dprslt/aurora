import logging
import numpy as np
import time

import config
import utils

from StoppablePausableThread import StoppablePausableThread


class Breath(StoppablePausableThread):
    def __init__(self, light, hue, sat, value_from, value_target, duration, pauses , frequency=60):
        super(Breath, self).__init__()

        self.light = light

        self.hue = hue
        self.sat = sat

        self.duration = duration
        self.pauses = pauses
        self.frequency = frequency

        self.reverse = False

        self.min_val = min(value_from, value_target)
        self.max_val = max(value_from, value_target)

        self.steps = np.arange(0., 1., 1 / float(self.frequency * self.duration[int(self.reverse)]))
        if value_target < value_from:
            self.steps = np.flip(self.steps, 0)

        self.step_count = 0

    def run(self):
        logging.info("LIGHT : Warm Breath mode")

        super(Breath, self).run()

    def work(self):

        if self.step_count == len(self.steps):
            time.sleep(self.pauses[int(self.reverse)])
            self.reverse = not self.reverse
            self.step_count = 0
            self.steps = np.arange(0., 1., 1 / float(self.frequency * self.duration[int(self.reverse)]))
            if self.reverse :
                self.steps = np.flip(self.steps, 0)

        step = self.steps[self.step_count]

        #current_value = self.min_val + utils.tr_sig(step) * (self.max_val - self.min_val)
        current_value = self.min_val + utils.tr_cos(step) * (self.max_val - self.min_val)
        with config.strip_lock:
            self.light.show_color(utils.hsv_to_Color(self.hue, self.sat, current_value))
        time.sleep(1 / float(self.frequency))

        self.step_count = self.step_count + 1


