from datetime import datetime

from strategies.time.AbstractTime import AbstractTime


class RealTime(AbstractTime):

    def __init__(self):
        super(RealTime, self).__init__()

    def compute_minutes_of_day(self):
        time_str = self.get_str_time()
        hours = int(time_str[0:2])
        minutes = int(time_str[2:4])
        return hours * 60 + minutes

    def get_str_time(self):
        return datetime.now().strftime("%H%M")

