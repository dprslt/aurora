import logging
import signal
import time
from datetime import datetime

import config
from strategies.colors.OneCyclePerHour import OneCyclePerHour
from strategies.screen.AbstractClock import AbstractClock
from strategies.time.RealTime import RealTime


class RealClockTime(AbstractClock, RealTime):
    def __init__(self, screen, screen_color_strategy=OneCyclePerHour(luminosity_coeff=0.15, value_min_light=0.05)):
        AbstractClock.__init__(self, screen, screen_color_strategy)

        self.separator_state = False
        self.step_counter = 0
        self.sleeping_time = 0.5

    def run(self):
        logging.info("SCREEN : Clock Real Time mode")

        super(RealClockTime, self).run()

    def work(self):
        self.time_str = self.get_str_time()

        with config.strip_lock:
            self.refresh()

        if self.step_counter == 1 / self.sleeping_time:
            with config.strip_lock:
                self.screen.set_separator_state(self.separator_state, color=self.color_digit)
            self.separator_state = not self.separator_state
            self.step_counter = 0
        else:
            self.step_counter = self.step_counter + 1

        time.sleep(self.sleeping_time)


if __name__ == '__main__':
    t1 = RealClockTime("t1")
    t2 = RealClockTime("t2")
    t3 = RealClockTime("t3")


    def stop_all(signum, frame):
        print("SIGNAL")
        t1.stop()
        t2.stop()
        t3.stop()

        print("JOING")
        t2.join()
        t3.join()

        print("EXITING")

        exit()


    signal.signal(signal.SIGTERM, stop_all)
    signal.signal(signal.SIGINT, stop_all)

    t1.start()
    t2.start()
    t3.start()

    time.sleep(2)
    print("Stoping thread 1")
    t1.stop()

    t1.join()
    print("Okay, thread 1 stopped")

    print("Pausing thread 2")
    t2.pause()
    time.sleep(6)
    print("Resuming thread 2")
    t2.resume()
    t2.join()

    print ("Tread 2 done")
    t3.join()

    print("Joining all done")
