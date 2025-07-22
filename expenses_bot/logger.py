import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")


def setup_logger() -> logging.Logger:
    log = logging.getLogger("expenses_bot")
    log.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setLevel(LOG_LEVEL)
    console.setFormatter(formatter)

    file = TimedRotatingFileHandler(
        LOG_FILE,
        when="midnight",
        backupCount=14,
        encoding="utf-8",
    )
    file.setLevel(LOG_LEVEL)
    file.setFormatter(formatter)

    log.addHandler(console)
    log.addHandler(file)
    log.propagate = False

    return log
