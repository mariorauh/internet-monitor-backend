from pathlib import Path
import json

## HAOS specific

OPTIONS_FILE = Path("/data/options.json")

DEFAULT_OPTIONS = {
    "http_target": "https://www.google.com",
    "http_timeout": 5,
    "dns_target": "8.8.8.8",
    "ping_target": "1.1.1.1",
    "ping_count": 4,
    "ping_timeout": 2,
    "check_interval": 5,
}

OPTIONS = DEFAULT_OPTIONS.copy()

if OPTIONS_FILE.exists():

    try:

        with OPTIONS_FILE.open(
            "r",
            encoding="utf-8",
        ) as fp:

            OPTIONS.update(json.load(fp))

    except Exception:

        pass

    

# =============================================================================
# Application
# =============================================================================

APP_NAME = "Internet Monitor"

APP_VERSION = "0.3.1"

LOG_LEVEL = "INFO"

# =============================================================================
# Monitoring
# =============================================================================

HTTP_TARGET = OPTIONS["http_target"]
HTTP_TIMEOUT = OPTIONS["http_timeout"]

DNS_TARGET = OPTIONS["dns_target"]

PING_TARGET = OPTIONS["ping_target"]
PING_COUNT = OPTIONS["ping_count"]
PING_TIMEOUT = OPTIONS["ping_timeout"]

CHECK_INTERVAL = OPTIONS["check_interval"]

# =============================================================================
# Database
# =============================================================================

DATA_DIRECTORY = Path("/data")

DATABASE_FILE = DATA_DIRECTORY / "internet_monitor.db"

KEEP_RAW_MEASUREMENTS_DAYS = 90

KEEP_OUTAGES_DAYS = 3650

# =============================================================================
# API
# =============================================================================

API_ENABLED = True

API_HOST = "0.0.0.0"

API_PORT = 8080

# =============================================================================
# Home Assistant
# =============================================================================

MQTT_ENABLED = False

MQTT_HOST = ""

MQTT_PORT = 1883

MQTT_USERNAME = ""

MQTT_PASSWORD = ""


    
def log_configuration(logger) -> None:
    """Log the effective application configuration."""

    logger.info("")
    logger.info("Configuration")
    logger.info("-------------")
    logger.info("HTTP Target     : %s", HTTP_TARGET)
    logger.info("HTTP Timeout    : %d s", HTTP_TIMEOUT)
    logger.info("DNS Target      : %s", DNS_TARGET)
    logger.info("Ping Target     : %s", PING_TARGET)
    logger.info("Ping Count      : %d", PING_COUNT)
    logger.info("Ping Timeout    : %d s", PING_TIMEOUT)
    logger.info("Check Interval  : %d s", CHECK_INTERVAL)
    logger.info("")