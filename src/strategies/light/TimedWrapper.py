import logging

from StoppablePausableThread import StoppablePausableThread
import time

class TimedWrapper(StoppablePausableThread):
    def __init__(self, childThread, duration):
        super(TimedWrapper, self).__init__()
        self.duration = duration
        self.childThread = childThread

    def run(self):
        logging.info("Wrapped Timer of a child Thread")

        # super(TimedWrapper, self).run()
        self.childThread.start()
        logging.info("Wrapped Timer : Child will be running for "+str(self.duration))
        time.sleep(self.duration)
        self.childThread.stop()
        self.childThread.join()
        logging.info("Wrapped Timer : my child finnaly died *cry* *cry*, i can't live here anymore")
        self.stop()

    def work(self):
        # Do nothing
        time.sleep(1)

    def stop(self):
        self.childThread.stop()
        self.childThread.join(1)
        super(TimedWrapper, self).stop()

    def pause(self):
        self.childThread.pause()
        super(TimedWrapper, self).pause()

    def resume(self):
        self.childThread.resume()
        super(TimedWrapper, self).resume()