import logging

from .client import *

logging.getLogger(__name__).addHandler(logging.NullHandler())
