import loguru
import sys


def setup_logging(level='DEBUG', version="UNKNOWN_VERSION"):
    format_string = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{version}:{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'.replace(
        "{version}", version)
    loguru.logger.remove()
    loguru.logger.add(sys.stderr, level=level, format=format_string)
    # Only send file-based logs at the 'error' level, all other levels are stderr only
    # loguru.logger.add("/python/stuckLog.log", level="ERROR", format=format_string, rotation="100 MB", compression="zip")
    return loguru.logger


log = setup_logging()  # Setup Default Logger with formats / etc
