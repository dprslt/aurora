from strategies.core.QuickTime import *
from strategies.core.RealTime import *
from strategies.core.Animate import *




def get_display_strategy(type, strip, display, light):
    if type == "real" or type == "realtime":
        return RealTime(strip, display, light)
    elif type == "quick" or type == "quicktime":
        return QuickTime(strip, display, light)
    elif type == "anim" or type == "animate":
        return AnimateCore(strip, display, light)

__all__ = [QuickTime, RealTime, AnimateCore, get_display_strategy]
