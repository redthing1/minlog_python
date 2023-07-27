from . import logger, Verbosity, Backend

def all_prints():
    logger.log("hello", Verbosity.DEBUG)
    logger.log("hello", Verbosity.TRACE)
    logger.log("hello", Verbosity.INFO)
    logger.log("hello", Verbosity.WARN)
    logger.log("hello", Verbosity.ERROR)
    logger.log("hello", Verbosity.CRITICAL)

if __name__ == "__main__":
    logger.backend = Backend.RICH
    all_prints()
    logger.backend = Backend.COLORAMA
    all_prints()
