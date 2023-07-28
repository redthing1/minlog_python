from . import logger, Verbosity, Backend


def log_all_levels(my_logger):
    my_logger.log("hello", Verbosity.DEBUG)
    my_logger.log("hello", Verbosity.TRACE)
    my_logger.log("hello", Verbosity.INFO)
    my_logger.log("hello", Verbosity.WARN)
    my_logger.log("hello", Verbosity.ERROR)
    my_logger.log("hello", Verbosity.CRITICAL)


if __name__ == "__main__":
    print("=" * 10, "RICH", "=" * 10)
    logger.backend = Backend.RICH
    log_all_levels(logger)
    print("=" * 10, "COLORAMA", "=" * 10)
    logger.backend = Backend.COLORAMA
    log_all_levels(logger)

    # test with a log source
    print("=" * 10, "LOG SOURCE (RICH)", "=" * 10)
    apple_logger = logger.logger_for("apple")
    log_all_levels(apple_logger)

    print("=" * 10, "LOG SOURCE (COLORAMA)", "=" * 10)
    banana_logger = logger.logger_for("banana")
    banana_logger.backend = Backend.COLORAMA
    log_all_levels(banana_logger)
