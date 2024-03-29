import logging
from threading import Lock

import config
from strategies.buttons.AbstractButtonAction import AbstractButtonAction
from strategies.light.Breath import Breath
from strategies.light.SimpleRealTimeColor import SimpleRealTimeColor
from strategies.light.SimpleColor import SimpleColor
from strategies.colors.FixedColor import FixedColor

from strategies.screen import DisplayMessage
from strategies.screen import DisplayScrollingMessage


from datetime import datetime



class NavigateModes(AbstractButtonAction):
    def __init__(self, light, disp):
        super(NavigateModes, self).__init__()
        self.light = light
        self.disp = disp
        self.running = False

        self.i = 1

        self.running = False
        self.lock = Lock()

        self.modes = [
            self.one_cycle_per_hour,
            self.breathing_warm,
            self.full_light,
        ]

    def action(self, channel):
        logging.info("Button pushed %d pushed : Mode change asked", self.bcm_port)

        with self.lock:
            if self.running:
                return

        with self.lock:
            self.running = True

        self.modes[self.i]()

        self.i = (self.i + 1) % len(self.modes)

        with self.lock:
            self.running = False

    def breathing_warm(self):
        config.scheduler.set_light_thread(
            Breath(self.light, 0.08, 0.9, value_target=0.99, value_from=0.1, duration=[2.5, 2.5], pauses=[0.05, 0.8],
                   frequency=40))
        config.scheduler.temporary_switch_screen_thread(DisplayMessage(screen=self.disp, message="rESP", duration=0.5))

    def one_cycle_per_hour(self):
        config.scheduler.set_light_thread(SimpleRealTimeColor(self.light))
        config.scheduler.temporary_switch_screen_thread(DisplayMessage(screen=self.disp, message="rEAL", duration=0.5))

    def full_light(self):
        config.scheduler.set_light_thread(SimpleColor(self.light,FixedColor([255,172,68])))
        config.scheduler.temporary_switch_screen_thread(DisplayMessage(screen=self.disp, message="hot", duration=0.5))

    def days_left(self):
        delta = datetime.strptime("04/08/2018","%d/%m/%Y") - datetime.now()

        config.scheduler.temporary_switch_screen_thread(DisplayMessage(screen=self.disp, message="J"+str(delta.days), duration=2, screen_color_strategy=FixedColor([255,11,11]) ))
