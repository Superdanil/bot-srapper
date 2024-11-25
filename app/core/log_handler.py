import sys

from loguru import logger

from core.settings import settings

logger.remove()

logger.add(
    sink=settings.LOGFILE,
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    rotation=settings.ROTATION,
    compression=settings.COMPRESSION,
)

logger.add(sys.stderr, level="DEBUG")
