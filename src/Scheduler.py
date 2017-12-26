import logging
import time
from threading import Lock

from StoppablePausableThread import StoppablePausableThread
from strategies.light.TurnedOff import TurnedOff


class Scheduler(StoppablePausableThread):
    def __init__(self):
        StoppablePausableThread.__init__(self)

        self.screen_th = None
        self.light_th = None

        self._paused_screen_th = None

        self.last_active_light = None

        self.lock = Lock()

    def set_screen_thread(self, thread):
        logging.info("Setting a new Screen thread")
        if self.screen_th is not None:
            self.screen_th.stop()
            self.screen_th.join(1)

        self.screen_th = thread
        self.screen_th.start()

    def set_light_thread(self, thread):
        logging.info("Setting a new Light thread")
        if self.light_th is not None:
            self.light_th.stop()
            self.light_th.join(1)

        if self.last_active_light is not None:
            self.last_active_light.stop()
            self.last_active_light = None

        self.light_th = thread
        self.light_th.start()

    def toogle_light(self, ligth):
        with self.lock:
            if self.last_active_light is None:
                self.light_th.pause()
                time.sleep(0.2)
                self.last_active_light = self.light_th
                self.light_th = TurnedOff(ligth)
                self.light_th.start()
            else:
                self.light_th.stop()
                self.light_th.join(1)
                self.light_th = self.last_active_light
                self.light_th.resume()
                self.last_active_light = None



    def temporary_switch_screen_thread(self, thread):
        logging.info("Temporary switching Screen Thread")
        if self._paused_screen_th is not None:
            logging.warning("A thread is already here temporary")
            return

        if self.screen_th is not None:
            self.screen_th.pause()
            self._paused_screen_th = self.screen_th

        self.screen_th = thread
        self.screen_th.start()
        self.screen_th.join()

        self.screen_th = self._paused_screen_th
        self._paused_screen_th = None

        self.screen_th.resume()

    def stop(self):
        logging.info("Stopping scheduler")

        threads = [self.screen_th, self.light_th, self._paused_screen_th, self.last_active_light]

        for th in threads:
            if th is not None and th.isAlive():
                logging.info("Stoping a thread %s", th)
                th.stop()
                th.join(1)

        super(Scheduler, self).stop()

    def work(self):
        pass

    def run(self):
        logging.info("Launching scheduler")
        while self.running:
            if self.screen_th is not None and self.screen_th.isAlive():
                self.screen_th.join(1)
            if self.light_th is not None and self.light_th.isAlive():
                self.light_th.join(1)

            time.sleep(0.5)
        logging.info("Exiting Scheduler Thread")
