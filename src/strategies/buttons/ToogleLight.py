import logging
from threading import Lock

import config
from strategies.buttons.AbstractButtonAction import AbstractButtonAction


class ToogleLight(AbstractButtonAction):
    def __init__(self, light):
        super(ToogleLight, self).__init__()
        self.light = light
        self.running = False
        self.lock = Lock()

    def action(self, channel):
        logging.info("Button pushed %d pushed : Light toogle asked", self.bcm_port)

        with self.lock:
            if self.running:
                return

        with self.lock:
            self.running = True
        config.scheduler.toogle_light(self.light)
        with self.lock:
            self.running = False
