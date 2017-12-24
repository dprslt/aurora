from threading import Thread, Event

import logging


class PausableThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.paused = Event()
        self.paused.set()

    def run(self):
        while self.running:
            while not self.paused.wait(timeout=0.5):
                if not self.running:
                    logging.info("Exiting paused thread")
                    return

            self.work()

        logging.info("Exiting thread")

    def work(self):
        raise NotImplementedError()

    def stop(self):
        self.running = False

    def pause(self):
        self.paused.clear()

    def resume(self):
        self.paused.set()
