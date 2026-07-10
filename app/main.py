import time
import signal
import sys

import app.config as config
from app.database import Database
from app.internet_monitor import InternetMonitor
from app.logger import logger
from app.outage_detector import OutageDetector
import app.config as config
from app.status import status_store
from threading import Thread

from app.api import start_api




running = True


def shutdown(signum, frame) -> None:
    global running

    logger.info("Shutdown signal received.")

    running = False


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


def main() -> None:

    logger.info(
        "%s %s",
        config.APP_NAME,
        config.APP_VERSION,
    )
    logger.info("Starting monitoring...")
    
    logger.info(
        "%s %s",
        config.APP_NAME,
        config.APP_VERSION,
    )

    config.log_configuration(logger)

    database = Database()
    monitor = InternetMonitor()
    outage_detector = OutageDetector(database)

    logger.info("Database initialized")
    logger.info("Monitoring interval: %s seconds", config.CHECK_INTERVAL)
    
    if config.API_ENABLED:

        Thread(
            target=start_api,
            daemon=True,
            name="REST API",
        ).start()

        logger.info(
            "REST API started on %s:%d",
            config.API_HOST,
            config.API_PORT,
        )

    while running:

        try:

            measurement = monitor.measure()

            database.save_measurement(measurement)

            outage_detector.process(measurement)
            
            status_store.update(
                internet=measurement.internet_ok,
                dns=measurement.dns_ok,
                ping=measurement.ping_ms or 0.0,
                packet_loss=measurement.packet_loss,
                version=config.APP_VERSION,
            )

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