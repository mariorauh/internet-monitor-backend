from __future__ import annotations

import logging
import sys

from app.ring_logger import RingFileHandler

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"

logger = logging.getLogger("internet-monitor")
logger.setLevel(logging.INFO)

# Verhindert doppelte Handler nach einem Neustart
logger.handlers.clear()

formatter = logging.Formatter(LOG_FORMAT)

#
# Home Assistant / Docker Log
#
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

#
# Persistente Logdatei
#
file_handler = RingFileHandler(
    "/data/internet_monitor.log",
    max_lines=10000,
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.propagate = False