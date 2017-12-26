import time

import config
import utils
from StoppablePausableThread import StoppablePausableThread


class Loading(StoppablePausableThread):
    def __init__(self, light, queue=10):
        super(Loading, self).__init__()
        self.light = light

        self.step = 0

        self.queue = queue

    def work(self):

        for q in range(0, self.queue):
            if (self.step < q):
                continue
            with config.strip_lock:
                self.light.strip.setPixelColor(self.light.top_offset + ((self.step - q) % self.light.top_strip_length),
                                           utils.hsv_to_Color(
                                               ((self.step - q) % self.light.top_strip_length) / float(
                                                   self.light.top_strip_length), 0.8,
                                               (self.queue - q) / float(self.queue)))

        with config.strip_lock:
            utils.led_off(self.light.strip,
                      self.light.top_offset + ((self.step - self.queue) % self.light.top_strip_length))

            self.light.strip.show()

        time.sleep(0.01)
        self.step = self.step + 1

    def run(self):
        super(Loading, self).run()

        for q in range(self.queue+1, 0, -1):
            with config.strip_lock:
                utils.led_off(self.light.strip, self.light.top_offset + ((self.step - q) % self.light.top_strip_length))
            time.sleep(0.01)




