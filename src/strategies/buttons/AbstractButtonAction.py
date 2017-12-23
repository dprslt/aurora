import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)

class AbstractButtonAction(object):

    def __init__(self):
        super(AbstractButtonAction, self).__init__()

    def action(self, channel):
        raise NotImplementedError()

    '''
        pull_up_down : GPIO.PUD_UP | GPIO.PUD_DOWN
        event :  GPIO.FALLING | GPIO.RISING
    '''
    def register(self, bcm_port, pull_up_down, event=GPIO.FALLING, bouncetime=300):
        self.bcm_port = bcm_port
        self.pull_up_down = pull_up_down
        self.event = event
        logging.info("Register GPIO button on port %d, event : %s, mode : %s", self.bcm_port, self.event, self.pull_up_down)
        GPIO.setup(bcm_port, GPIO.IN, pull_up_down=pull_up_down)

        GPIO.add_event_detect(bcm_port, event, callback=self.action, bouncetime=bouncetime)
