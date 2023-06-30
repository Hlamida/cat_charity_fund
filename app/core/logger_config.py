import logging
import sys

logger = logging.getLogger(__name__)
logging_format = logging.Formatter(
    fmt='[%(asctime)s: %(levelname)s] %(message)s'
)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = logging.FileHandler(f'{__name__}.log', mode='w')
stream_handler.setFormatter(logging_format)
file_handler.setFormatter(logging_format)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
