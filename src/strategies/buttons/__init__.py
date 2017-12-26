from strategies.buttons.ToogleLight import *
from strategies.buttons.NavigateModes import *

import RPi.GPIO as GPIO

# GPIO Pin using BCM format
PORT_1 = 23
PORT_2 = 24

button_1 = None
button_2 = None


def register_buttons(top_light, disp):
    button_1 = ToogleLight(top_light)
    button_1.register(PORT_1, pull_up_down=GPIO.PUD_UP, event=GPIO.FALLING)

    button_2 = NavigateModes(top_light, disp)
    button_2.register(PORT_2, pull_up_down=GPIO.PUD_UP, event=GPIO.FALLING)


def unregister_buttons():
    GPIO.remove_event_detect(PORT_1)
    GPIO.remove_event_detect(PORT_2)


__all__ = [ToogleLight, NavigateModes, register_buttons, unregister_buttons]
