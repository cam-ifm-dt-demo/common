"""Utility functions for the API."""

import logging
from typing import Type

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from sqlmodel import Session


class MyAPIError(BaseModel):
    """Generic error class for the API."""
    message: str = Field(examples=['Error message'])


class ErrorResponse(JSONResponse):
    """A JSON response corresponding to an HTTP error."""


def validate(obj, cls: Type[BaseModel], logger: logging.Logger | None = None):
    """Manually validate a Pydantic/SQLModel model, throwing an HTTPException if invalid.

    This is required as Try It Out on the automatic Swagger documentation page does not
    properly check for missing model fields."""
    if logger is None:
        logger = logging.getLogger()
    try:
        cls.model_validate(obj)
    except ValidationError as e:
        logger.error(str(e))
        raise HTTPException(422, str(e)) from e


def ensure_exists(cls: Type[BaseModel], _id, session: Session,
                  logger: logging.Logger | None = None):
    """Check that a SQLModel instance of the specified type `cls` exists
    with primary key `id`, and return the instance if found."""
    if logger is None:
        logger = logging.getLogger()
    existing = session.get(cls, _id)
    if not existing:
        err_msg = f'{cls.__name__} with ID `{_id}` not found.'
        logger.error(err_msg)
        raise HTTPException(404, err_msg)
    return existing


def ensure_not_exists(cls: Type[BaseModel], _id, session: Session,
                      logger: logging.Logger | None = None):
    """Check that no SQLModel instance of the specifed type `cls` exists
    with primary key`id`."""
    if logger is None:
        logger = logging.getLogger()
    existing = session.get(cls, _id)
    if existing:
        err_msg = f'{cls.__name__} with ID `{_id}` already exists.'
        logger.error(err_msg)
        raise HTTPException(404, err_msg)
