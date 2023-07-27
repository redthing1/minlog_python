from . import logger, Verbosity, Backend


def all_prints():
    logger.log("hello", Verbosity.DEBUG)
    logger.log("hello", Verbosity.TRACE)
    logger.log("hello", Verbosity.INFO)
    logger.log("hello", Verbosity.WARN)
    logger.log("hello", Verbosity.ERROR)
    logger.log("hello", Verbosity.CRITICAL)


if __name__ == "__main__":
    print("=" * 10, "RICH", "=" * 10)
    logger.backend = Backend.RICH
    all_prints()
    print("=" * 10, "COLORAMA", "=" * 10)
    logger.backend = Backend.COLORAMA
    all_prints()
