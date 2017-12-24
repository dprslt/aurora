from strategies.colors import OneCyclePerHour


class AbstractCore(object):

    def __init__(self, strip, display, light):
        super(AbstractCore, self).__init__()
        self.strip = strip
        self.display = display
        self.light = light
        self.light_color_strategy = OneCyclePerHour(luminosity_coeff=1)

    def play(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()