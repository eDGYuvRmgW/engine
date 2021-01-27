import logging

import pretty_logs
import colorama
from termcolor import colored

colorama.init()

RED     = '\033[0;31m'
BRIGHT_CYAN    = '\033[1;36m'
BRIGHT_GREEN   = '\033[1;32m'
BRIGHT_YELLOW  = '\033[1;33m'
WHITE   = '\033[0;37m'
BRIGHT_RED     = '\033[1;31m'
BRIGHT_MAGENTA = '\033[1;35m'
BRIGHT_GREEN   = '\033[1;32m'
BRIGHT_BLACK   = GREY = '\033[1;30m'
BLUE    = '\033[0;34m'
BRIGHT_BLUE    = '\033[1;34m'
YELLOW  = '\033[0;33m'

import sys

class Formatter(logging.Formatter):

    dbg_fmt  = BRIGHT_MAGENTA
    info_fmt = WHITE
    warn_fmt  = BRIGHT_YELLOW
    err_fmt  = BRIGHT_RED

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):
        format_orig = self._style._fmt
        base_fmt = '%(levelname)s' + BRIGHT_GREEN + ' %(lineno)d' + BRIGHT_CYAN +' %(name)s' + BRIGHT_BLUE + ' %(relativeCreated)dms' + GREY + '\n%(message)s\n'

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = Formatter.dbg_fmt + base_fmt
        elif record.levelno == logging.INFO:
            self._style._fmt = Formatter.info_fmt + base_fmt

        elif record.levelno == logging.WARNING:
            self._style._fmt = Formatter.warn_fmt + base_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = Formatter.err_fmt + base_fmt

        result = logging.Formatter.format(self, record)
        self._style._fmt = format_orig
        return result



formatter = Formatter()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logging.root.addHandler(handler)
