import loguru
import sys
import os

DEFAULT_LOG_LEVEL="WARNING"
if "LOG_LEVEL" in os.environ:
    DEFAULT_LOG_LEVEL=os.environ["LOG_LEVEL"]

DEFAULT_APP_NAME="UNKNOWN_APP"
if "APP_NAME" in os.environ:
    DEFAULT_APP_NAME=os.environ["APP_NAME"]


def setup_logging(level=DEFAULT_LOG_LEVEL, version=DEFAULT_APP_NAME):
    format_string = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{version}:{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'.replace(
        "{version}", version)
    loguru.logger.remove()
    loguru.logger.add(sys.stderr, level=level, format=format_string)
    # Only send file-based logs at the 'error' level, all other levels are stderr only
    # loguru.logger.add("/python/stuckLog.log", level="ERROR", format=format_string, rotation="100 MB", compression="zip")
    return loguru.logger

log = setup_logging()