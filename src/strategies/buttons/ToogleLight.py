import logging

import config
from strategies.buttons.AbstractButtonAction import AbstractButtonAction


class ToogleLight(AbstractButtonAction):

    def __init__(self, light):
        super(ToogleLight, self).__init__()
        self.light = light

    def action(self, channel):
        logging.info("Button pushed %d pushed : Light toogle asked", self.bcm_port)
        previous_state = self.light.powered
        self.light.set_powered(not previous_state)
        if not previous_state:
            config.core_strategy.refresh()

