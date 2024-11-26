from . import logger, Verbosity
from typing import Callable

"""
minlog test suite
run: poetry run python -m minlog._test
"""


def run_tests() -> None:
    """execute test suite with elegant formatting"""
    logger.be_debug()  # ensure full logging visibility

    # core logging functionality
    print("\n■ core logging")
    logger.debug("→ debug message")
    logger.trace("→ trace message")
    logger.info("→ info message")
    logger.warn("→ warning message")
    logger.error("→ error message")
    logger.crit("→ critical message")

    # verbosity controls
    print("\n■ verbosity handling")
    print("→ quiet mode (errors only)")
    logger.be_quiet()
    logger.info("• this should not appear")
    logger.error("• this error should appear")

    print("\n→ verbose mode (all messages)")
    logger.be_verbose()
    logger.debug("• debug should now appear")
    logger.info("• info should now appear")

    # source logging
    print("\n■ source loggers")
    app_logger = logger.logger_for("app")
    db_logger = logger.logger_for("db")
    app_logger.info("→ message from app context")
    db_logger.warn("→ warning from db context")

    # special cases
    print("\n■ special cases")
    print("→ rich formatting characters")
    logger.info("• message with [brackets]")
    logger.info("• message with [red]color[/red]")

    print("\n→ multi-line content")
    logger.info("• line one\n• line two")

    # message filtering
    print("\n■ message filtering")
    logger.be_quiet()
    logger.force_log("→ forced message in quiet mode")
    logger.log_only_when_quieter_than("→ conditional message", Verbosity.DEBUG)

    print("\n✓ all tests completed")


if __name__ == "__main__":
    run_tests()
