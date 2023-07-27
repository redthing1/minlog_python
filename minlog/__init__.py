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
    def __init__(self, verbosity: Verbosity = Verbosity.INFO):
        # maximum verbosity of messages to print
        self.verbosity = verbosity

        # default to rich
        self.backend = Backend.RICH
        # but if compiled, default to colorama
        if IS_COMPILED:
            self.backend = Backend.COLORAMA

        if self.backend == Backend.RICH:
            from rich.console import Console

            self.rich_console = Console()

        elif self.backend == Backend.COLORAMA:
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
        meta_str = f"{self.short_verbosity(message_verbosity)}"
        message_str = message

        if self.backend == Backend.RICH:
            # mprint(message)
            meta_style_rich = self.get_style_rich(message_verbosity)
            self.rich_console.print(f"\[{meta_str}]", style=meta_style_rich, end="")
            message_str_escaped = message_str.replace("[", "\[")
            self.rich_console.print(f" {message_str_escaped}")
        elif self.backend == Backend.COLORAMA:
            meta_bg = Back.BLACK
            meta_fg = self.get_fg_color_colorama(message_verbosity)
            message_bg = Back.RESET
            message_fg = Fore.RESET

            meta_frm = f"{meta_bg}{meta_fg}[{meta_str}]{Style.RESET_ALL}"
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

    def get_style_rich(self, message_verbosity: Verbosity):
        if message_verbosity == Verbosity.DEBUG:
            return "bright_black on black"
        elif message_verbosity == Verbosity.TRACE:
            return "bright_black on black"
        elif message_verbosity == Verbosity.INFO:
            return "green on black"
        elif message_verbosity == Verbosity.WARN:
            return "yellow on black"
        elif message_verbosity == Verbosity.ERROR:
            return "red on black"
        elif message_verbosity == Verbosity.CRITICAL:
            return "red on black"


logger = Logger()
