from enum import Enum
import colorama
from colorama import Fore, Back, Style

IS_COMPILED = "__compiled__" in globals()


def mprint(*args, **kwargs):
    # nuitka has issues with rich
    if IS_COMPILED:
        # do standard print
        print(*args, **kwargs)
    else:
        from rich import print as rprint

        rprint(*args, **kwargs)


class Backend(Enum):
    RICH = 0
    COLORAMA = 1


class Verbosity(Enum):
    CRITICAL = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    TRACE = 4
    DEBUG = 5


class Logger(object):
    def __init__(
        self, verbosity: Verbosity = Verbosity.INFO, backend: Backend = Backend.RICH
    ):
        # maximum verbosity of messages to print
        self.verbosity = verbosity

        self.backend = backend

        if self.backend == Backend.COLORAMA:
            # initialize colorama
            colorama.init()

    def short_verbosity(self, message_verbosity: Verbosity):
        if message_verbosity == Verbosity.DEBUG:
            return "dbg"
        elif message_verbosity == Verbosity.TRACE:
            return "trc"
        elif message_verbosity == Verbosity.INFO:
            return "inf"
        elif message_verbosity == Verbosity.WARN:
            return "wrn"
        elif message_verbosity == Verbosity.ERROR:
            return "err"
        elif message_verbosity == Verbosity.CRITICAL:
            return "crt"

    def log(self, message: str, message_verbosity: Verbosity):
        # if the message verbosity is within the configured maximum verbosity
        if message_verbosity.value > self.verbosity.value:
            return

        # then print the message

        if self.backend == Backend.RICH:
            mprint(message)
        elif self.backend == Backend.COLORAMA:
            meta_str = f"[{self.short_verbosity(message_verbosity)}]"
            message_str = message

            meta_bg = self.get_bg_color_colorama(message_verbosity)
            meta_fg = self.get_fg_color_colorama(message_verbosity)
            message_bg = Back.RESET
            message_fg = Fore.RESET

            meta_frm = f"{meta_bg}{meta_fg}{meta_str}{Style.RESET_ALL}"
            message_frm = f"{message_bg}{message_fg}{message_str}{Style.RESET_ALL}"

            print(f"{meta_frm} {message_frm}")

    def debug(self, message: str):
        self.log(message, Verbosity.DEBUG)

    def trace(self, message: str):
        self.log(message, Verbosity.TRACE)

    def info(self, message: str):
        self.log(message, Verbosity.INFO)

    def warn(self, message: str):
        self.log(message, Verbosity.WARN)

    def error(self, message: str):
        self.log(message, Verbosity.ERROR)

    def crit(self, message: str):
        self.log(message, Verbosity.CRITICAL)

    def force_log(self, message: str):
        self.crit(message)

    def log_only_when_quieter_than(self, message: str, compare_verbosity: Verbosity):
        if self.verbosity.value <= compare_verbosity.value:
            mprint(message)

    def is_quiet(self):
        return self.verbosity.value == Verbosity.ERROR.value

    def is_verbose(self):
        return self.verbosity.value == Verbosity.TRACE.value

    def be_quiet(self):
        self.verbosity = Verbosity.ERROR

    def be_verbose(self):
        self.verbosity = Verbosity.TRACE

    def get_bg_color_colorama(self, message_verbosity: Verbosity):
        return Back.BLACK

    def get_fg_color_colorama(self, message_verbosity: Verbosity):
        if message_verbosity == Verbosity.DEBUG:
            return Fore.LIGHTBLACK_EX
        elif message_verbosity == Verbosity.TRACE:
            return Fore.LIGHTBLACK_EX
        elif message_verbosity == Verbosity.INFO:
            return Fore.GREEN
        elif message_verbosity == Verbosity.WARN:
            return Fore.YELLOW
        elif message_verbosity == Verbosity.ERROR:
            return Fore.RED
        elif message_verbosity == Verbosity.CRITICAL:
            return Fore.RED


logger = Logger()
