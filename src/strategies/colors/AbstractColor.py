

class AbstractColor(object):

    def __init__(self):
        super(AbstractColor, self).__init__()

    def get_current_color(self, minutes_of_day):
        raise NotImplementedError()

    def get_current_color_hsv(self,minutes_of_day):
        raise NotImplementedError()