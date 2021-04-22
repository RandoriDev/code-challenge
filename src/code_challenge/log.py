"""
Randori Code Challenge server module.
"""

import logging
import os
import sys

from code_challenge import constants


class ExcludeLogLevelFilter(logging.Filter):
    """Exclude log level filter.

    Filters out any log messages that do match the given level.
    """

    def __init__(self, level: int):
        """Constructor.

        :param level: Exclude log level
        """

        logging.Filter.__init__(self)
        self.level = level

    def filter(self, record) -> bool:  # noqa: A003
        """Filter method.

        :param record: Log record
        :return: Whether the log record level is not equal to the exclude log level for this instance
        """

        return record.levelno != self.level


class ExclusiveLogLevelFilter(logging.Filter):
    """Exclusive log level filter.

    Filters out any log messages that do not match the given level.
    """

    def __init__(self, level: int):
        """Constructor.

        :param level: Exclusive log level
        """

        logging.Filter.__init__(self)
        self.level = level

    def filter(self, record) -> bool:  # noqa: A003
        """Filter method.

        :param record: Log record
        :return: Whether the log record level is equal to the exclude log level for this instance
        """

        return record.levelno == self.level


def initialize_app_logger(name: str):
    """This function initializes the app logger for the application.

    :param name: Logger name
    """

    # get the app logger
    logger = logging.getLogger(name)

    # set logger level
    logger.setLevel(logging.DEBUG)

    # create stdout console handler and set level to debug
    stdout_console_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_console_handler.setLevel(logging.DEBUG)

    # create stderr console handler and set level to error
    stderr_console_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_console_handler.setLevel(logging.ERROR)

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")

    # add formatter to handlers
    stdout_console_handler.setFormatter(formatter)
    stderr_console_handler.setFormatter(formatter)

    # create a new exclude log level filter for stdout handler
    stdout_console_handler.addFilter(ExcludeLogLevelFilter(level=logging.ERROR))

    # create a new exclusive log level filter for stderr handler
    stderr_console_handler.addFilter(ExclusiveLogLevelFilter(level=logging.ERROR))

    # add handlers to the logger
    logger.addHandler(stdout_console_handler)
    logger.addHandler(stderr_console_handler)

    # do not propagate the log messages to the root logger
    logger.propagate = False

    return logger
