from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from cam_ifm_dt_demo.common.logger import setup_logging, add_logger

LOGGER = add_logger('api')

@asynccontextmanager
async def lifespan(_):
    """Add FastAPI startup and cleanup tasks."""
    setup_logging()

    print('')
    print('')
    LOGGER.info('-----FASTAPI APPLICATION STARTUP------')
    LOGGER.info('')

    yield  # Start the FastAPI main loop
    # cleanup tasks go here
    LOGGER.critical('Shutting down now!')

app = FastAPI(lifespan=lifespan)

@app.get('/')
def root():
    LOGGER.debug('Hello World')
    return PlainTextResponse('Hello World')
