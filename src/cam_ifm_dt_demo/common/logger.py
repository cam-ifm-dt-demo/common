"""Classes and functions for prettier logging.

The primary purpose of this module is so that different loggers can match the output formatting
used by FastAPI.
"""

import logging
import re

import colorama as c
from fastapi_cli.utils.cli import CustomFormatter

from .config import config


class MyFormatter(CustomFormatter):
    """Custom logging formatter."""

    @staticmethod
    def clean_len(s: str):
        """Determine string length after stripping ANSI control sequences."""
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return len(ansi_escape.sub('', s))

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Set colors and formatting for messages.

        See: https://rich.readthedocs.io/en/stable/appendix/colors.html"""
        tag_color = (
            c.Back.RED if record.levelno >= logging.ERROR
            else c.Back.YELLOW + c.Fore.BLACK if record.levelno >= logging.WARNING
            else c.Back.GREEN + c.Fore.BLACK if record.levelno >= logging.INFO
            else c.Back.LIGHTBLACK_EX
        )
        msg_color = (
            c.Fore.RED if record.levelno >= logging.ERROR
            else c.Fore.YELLOW if record.levelno >= logging.WARNING
            else c.Fore.RESET if record.levelno >= logging.INFO
            else c.Fore.BLACK
        )

        s1 = f"{tag_color} {record.levelname} {c.Fore.RESET}{c.Back.RESET}"
        s2 = f"{c.Fore.BLUE}{record.name}{c.Fore.RESET}"
        s3 = f"{msg_color}{record.getMessage()}{c.Fore.RESET}"
        pad_left = max(0, 11 - __class__.clean_len(s1))
        return f"{'': <{pad_left}}{s1} {s2}: {s3}"


STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(MyFormatter())


def setup_logging():
    """Set up logger formatting for the various loggers used by FastAPI and SQLModel,
    as well as the root logger."""

    # Let these loggers propagate, but turn off any output at the current logger hierarchy level
    for logger_name in [
        'sqlalchemy.engine', 'sqlalchemy.engine.Engine', 'sqlalchemy.pool', 'sqlalchemy.orm'
    ]:
        logger = logging.getLogger(logger_name)
        logger.handlers = []

    # Uvicorn logger, used by FastAPI -- set logging level and do not propagate
    uvicorn_logger = logging.getLogger('uvicorn.error')
    uvicorn_logger.handlers = [STREAM_HANDLER]
    uvicorn_logger.setLevel(config.log_level_uvicorn)
    uvicorn_logger.propagate = False

    # Root logger
    if not hasattr(__builtins__, '__IPYTHON__'):
        root_logger = logging.getLogger()
        root_logger.handlers = [STREAM_HANDLER]
        root_logger.setLevel(config.log_level_root)


def add_logger(name: str):
    """Adds a new logger, or perform setup on the logger if it already exists."""
    if hasattr(__builtins__, '__IPYTHON__'):
        return logging.getLogger()

    logger = logging.getLogger(name)
    logger.handlers = [STREAM_HANDLER]
    logger.setLevel(config.log_level_mine)
    logger.propagate = False
    return logger
