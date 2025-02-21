import logging

from cam_ifm_dt_demo.common import logger

logger.setup_logging()

LOGGER = logger.add_logger('test')

LOGGER.error('This is an error message.')
LOGGER.warning('This is an warning message.')
LOGGER.info('This is an info message.')
LOGGER.debug('This is an debug message.')

logging.debug("This shouldn't show.")
