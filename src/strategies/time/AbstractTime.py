class AbstractTime(object):

    def __init__(self):
        super(AbstractTime, self).__init__()

    def compute_minutes_of_day(self):
        raise NotImplementedError()

    def get_str_time(self):
        raise NotImplementedError()