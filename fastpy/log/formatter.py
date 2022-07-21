import logging
import colorama
from .config import *

colorama.init()


class CustomFormatter(logging.Formatter):
    green = colorama.Fore.GREEN
    white = colorama.Fore.WHITE
    blue = colorama.Fore.BLUE
    yellow = colorama.Fore.YELLOW
    red = colorama.Fore.RED
    bold_red = colorama.Fore.RED + colorama.Style.BRIGHT
    reset = colorama.Style.RESET_ALL

    FORMATS = {
        logging.DEBUG: blue + FORMAT + reset,
        logging.INFO: green + FORMAT + reset,
        logging.WARNING: yellow + FORMAT + reset,
        logging.ERROR: red + FORMAT + reset,
        logging.CRITICAL: bold_red + FORMAT + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
