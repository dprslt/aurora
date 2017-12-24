import logging
from threading import RLock

log_level = logging.INFO
display_strategy_name = "real"

disp = None
top_light = None
strip = None

core_strategy = None

strip_lock = RLock()

scheduler = None