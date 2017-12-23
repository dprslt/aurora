import logging, time


from strategies.core.AbstractTimeCore import AbstractTimeCore


class QuickTime(AbstractTimeCore):

    def __init__(self, strip, display, light):
        super(QuickTime, self).__init__(strip, display, light)
        self.st = 0


    def refresh(self):
        super(QuickTime, self).refresh()

    def compute_minutes_of_day(self):
        return self.st


    def play(self):
        ## Infinite Loop

        logging.info("Running in quick time mode")

        while True:
            old_time_str = self.time_str
            hours = self.st / 60
            minutes = self.st % 60

            self.time_str = "{h:02d}{m:02d}".format(h=hours, m=minutes)

            if not old_time_str == self.time_str:
                self.refresh()

            self.st = (self.st + 1) % 1440

            time.sleep(0.02)

