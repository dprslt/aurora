from strategies.colors import TwoCyclePerDay


class AbstractCore(object):

    def __init__(self, strip, display, light):
        super(AbstractCore, self).__init__()
        self.strip = strip
        self.display = display
        self.light = light
        self.light_color_strategy = TwoCyclePerDay(luminosity_coeff=1)
        self.screen_color_strategy = TwoCyclePerDay(luminosity_coeff=0.2, value_min_light=0.1)

    def play(self):
        raise NotImplementedError()

    def refresh(self):
        raise NotImplementedError()