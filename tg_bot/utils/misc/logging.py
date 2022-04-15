import sys

from loguru import logger

from data import config
import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )


def allow_logging_levels(func):
    def check(record):
        return func(record) and record["level"].name in config.LOGGING_LEVEL
    return check


@allow_logging_levels
def logging_info_only(record):
    return record["level"].name == 'INFO'


@allow_logging_levels
def logging_debug_only(record):
    return record["level"].name == 'DEBUG'


# noinspection PyArgumentList
def setup():
    BASE_FORMAT = "{time:YYYY-MM-DD at HH:mm:ss} | {level} \t| "
    INFO_FORMAT = BASE_FORMAT + "{message}"
    DEBUG_FORMAT = BASE_FORMAT +"{file}:{function}:{line} | {message}"

    logger.remove()

    logger.add(sys.stderr, filter=logging_info_only, format=INFO_FORMAT)
    logger.add(sys.stderr, filter=logging_debug_only, format=DEBUG_FORMAT)

    logger.add(config.LOGS_BASE_PATH + "/file_{time}.log")