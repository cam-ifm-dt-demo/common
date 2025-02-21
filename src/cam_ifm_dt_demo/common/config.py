"""Configuration settings for the DT demo."""

import pathlib
from enum import IntEnum
from typing import Annotated

import pydantic as pyd
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingLevel(IntEnum):
    """Logging levels from the `logging` module."""
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


def convert_level(l: int | str) -> LoggingLevel:
    """Return a LoggingLevel by name or value."""
    if isinstance(l, int):
        return LoggingLevel(int)

    # l is a str, try matching
    for member in LoggingLevel:
        if member.name == l:
            return member

    raise ValueError('Invalid value for LoggingLevel.')


MyEnum = Annotated[LoggingLevel, pyd.BeforeValidator(convert_level)]


class Config(BaseSettings):
    """Configuration settings for the DT demo."""

    # See https://docs.pydantic.dev/latest/concepts/pydantic_settings/#field-value-priority

    if pathlib.Path('/run/secrets').exists():
        model_config = SettingsConfigDict(
            secrets_dir='/run/secrets'
        )

    api_url: pyd.HttpUrl = 'http://localhost:8000/'
    """URL used by modules to access the API."""

    db_url: pyd.AnyUrl = 'sqlite:////appdata/dt_demo_test.db'
    """URL for the shared database."""

    # LOGGING

    sql_echo: bool = False
    """Sets the echo parameter for the SQLAlchemy/SQLModel engine."""

    log_level_uvicorn: MyEnum = 'INFO'
    """Sets the logging level for Uvicorn (used by FastAPI).

    Since FastAPI somtimes bypasses the `logging` module, it is best not to change this level."""

    log_level_mine: MyEnum = 'DEBUG'
    """Sets the logging level for our own code."""

    log_level_root: MyEnum = 'INFO'
    """Sets the logging level for the root logger."""


config = Config()
