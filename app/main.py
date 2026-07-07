import time
import signal
import sys

import app.config as config
from app.database import Database
from app.internet_monitor import InternetMonitor
from app.logger import logger
from app.outage_detector import OutageDetector
from app.version import APP_NAME, APP_VERSION


running = True


def shutdown(signum, frame) -> None:
    global running

    logger.info("Shutdown signal received.")

    running = False


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


def main() -> None:

    logger.info("%s %s", APP_NAME, APP_VERSION)
    logger.info("Starting monitoring...")

    database = Database()
    monitor = InternetMonitor()
    outage_detector = OutageDetector(database)

    logger.info("Database initialized")
    logger.info("Monitoring interval: %s seconds", config.CHECK_INTERVAL)

    while running:

        try:

            measurement = monitor.measure()

            database.save_measurement(measurement)

            outage_detector.process(measurement)

            logger.info(
                "Internet=%s | DNS=%s | Ping=%s ms | Packet Loss=%.0f%%",
                "OK" if measurement.internet_ok else "DOWN",
                "OK" if measurement.dns_ok else "FAILED",
                measurement.ping_ms if measurement.ping_ms is not None else "-",
                measurement.packet_loss,
            )

        except Exception:

            logger.exception("Unexpected error during monitoring.")

        time.sleep(config.CHECK_INTERVAL)

    logger.info("Internet Monitor stopped.")

    sys.exit(0) 


if __name__ == "__main__":

    main()