from enum import Enum
from rich.console import Console
from typing import Optional


class Verbosity(Enum):
    """defines logging verbosity levels from most severe to most detailed"""

    CRITICAL = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    TRACE = 4
    DEBUG = 5


class Logger:
    # mapping of verbosity levels to their short forms
    VERBOSITY_SHORTCUTS = {
        Verbosity.DEBUG: "dbg",
        Verbosity.TRACE: "trc",
        Verbosity.INFO: "inf",
        Verbosity.WARN: "wrn",
        Verbosity.ERROR: "err",
        Verbosity.CRITICAL: "crt",
    }

    # rich styling for different verbosity levels
    VERBOSITY_STYLES = {
        Verbosity.DEBUG: "bright_black on black",
        Verbosity.TRACE: "white on black",
        Verbosity.INFO: "green on black",
        Verbosity.WARN: "yellow on black",
        Verbosity.ERROR: "red on black",
        Verbosity.CRITICAL: "bright_red on black",
    }

    def __init__(
        self, verbosity: Verbosity = Verbosity.INFO, log_source: Optional[str] = None
    ):
        """initialize logger with given verbosity and optional source tag"""
        self.verbosity = verbosity
        self.log_source = log_source
        self.console = Console()

    def logger_for(self, log_source: str) -> "Logger":
        """create a new logger instance with the same verbosity but different source"""
        return Logger(self.verbosity, log_source=log_source)

    def _format_message(self, message: str, level: Verbosity) -> tuple[str, str, str]:
        """format the message components with proper escaping"""
        # escape brackets to prevent rich interpretation
        meta = f"[{self.VERBOSITY_SHORTCUTS[level]}]".replace("[", "\\[")
        source = f"[{self.log_source}]".replace("[", "\\[") if self.log_source else ""
        content = message.replace("[", "\\[")
        return meta, source, content

    def log(self, message: str, level: Verbosity) -> None:
        """log a message with the specified verbosity level"""
        if level.value > self.verbosity.value:
            return

        meta, source, content = self._format_message(message, level)

        # print components with appropriate styling
        self.console.print(meta, style=self.VERBOSITY_STYLES[level], end="")
        self.console.print(" ", end="")

        if source:
            self.console.print(source, style="bright_black", end=" ")

        self.console.print(content)

    # convenience methods for different log levels
    def debug(self, message: str) -> None:
        """log debug message"""
        self.log(message, Verbosity.DEBUG)

    def trace(self, message: str) -> None:
        """log trace message"""
        self.log(message, Verbosity.TRACE)

    def info(self, message: str) -> None:
        """log info message"""
        self.log(message, Verbosity.INFO)

    def warn(self, message: str) -> None:
        """log warning message"""
        self.log(message, Verbosity.WARN)

    def error(self, message: str) -> None:
        """log error message"""
        self.log(message, Verbosity.ERROR)

    def crit(self, message: str) -> None:
        """log critical message"""
        self.log(message, Verbosity.CRITICAL)

    def force_log(self, message: str) -> None:
        """force log a message at critical level"""
        self.crit(message)

    # verbosity control methods
    def is_quiet(self) -> bool:
        """check if logger is in quiet mode (error level)"""
        return self.verbosity == Verbosity.ERROR

    def is_verbose(self) -> bool:
        """check if logger is in verbose mode (trace level)"""
        return self.verbosity == Verbosity.TRACE

    def be_quiet(self) -> None:
        """set logger to quiet mode"""
        self.verbosity = Verbosity.ERROR

    def be_verbose(self) -> None:
        """set logger to verbose mode"""
        self.verbosity = Verbosity.TRACE

    def be_debug(self) -> None:
        """set logger to debug mode"""
        self.verbosity = Verbosity.DEBUG

    def log_only_when_quieter_than(
        self, message: str, compare_verbosity: Verbosity
    ) -> None:
        """log message only if current verbosity is lower than specified level"""
        if self.verbosity.value <= compare_verbosity.value:
            print(message)  # using standard print for this specific case


# create default logger instance
logger = Logger()
