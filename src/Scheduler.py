import time

import logging

from strategies.core.PausableThread import PausableThread


class Scheduler(PausableThread):
    def __init__(self):
        PausableThread.__init__(self)

        self._screen_th = None
        self._light_th = None

        self._paused_screen_th = None

    def set_screen_thread(self, thread):
        logging.info("Setting a new Screen thread")
        if self._screen_th is not None:
            self._screen_th.stop()
            self._screen_th.join(1)

        self._screen_th = thread
        self._screen_th.start()



    def set_light_thread(self, thread):
        logging.info("Setting a new Light thread")
        if self._light_th is not None:
            self._light_th.stop()
            self._light_th.join(1)

        self._light_th = thread
        self._light_th.start()

    def temporary_switch_screen_thread(self, thread):
        logging.info("Temporary switching Screen Thread")
        if self._paused_screen_th is not None:
            logging.warning("A thread is already here temporary")
            return

        if self._screen_th is not None:
            self._screen_th.pause()
            self._paused_screen_th = self._screen_th

        self._screen_th = thread
        if self._screen_th is not None:
            self._screen_th.start()
            self._screen_th.join()

        self._screen_th = self._paused_screen_th
        self._paused_screen_th = None

        if self._screen_th is not None:
            self._screen_th.resume()



    def stop(self):
        logging.info("Stopping scheduler")

        threads = [self._screen_th, self._light_th, self._paused_screen_th]

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
            if self._screen_th is not None and self._screen_th.isAlive():
                self._screen_th.join(1)
            if self._light_th is not None and self._light_th.isAlive():
                self._light_th.join(1)

            time.sleep(0.5)
        logging.info("Exiting Scheduler Thread")