import logging, time
from datetime import datetime

import utils

from strategies.core.AbstractTimeCore import AbstractTimeCore


class RealTime(AbstractTimeCore):
    def __init__(self, strip, display, light):
        super(RealTime, self).__init__(strip, display, light)
        self.sleeping_time = 0.2



    def play(self):
        ## Infinite Loop
        separator_state = False
        rgb_color_digit = None

        logging.info("Running in real time mode")
        i = 0
        while True:
            self.time_str = datetime.now().strftime("%H%M")

            self.refresh()

            if i == 1/self.sleeping_time:
                self.display.set_separator_state(separator_state, color=self.color_digit)
                separator_state = not separator_state
                i = 0
            else:
                i = i + 1

            time.sleep(self.sleeping_time)
