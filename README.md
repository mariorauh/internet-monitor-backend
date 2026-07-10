# Internet Monitor

A lightweight Home Assistant add-on for monitoring Internet connectivity, detecting outages and providing a REST API for automations and dashboards.

---

# Features

- Continuous Internet connectivity monitoring
- HTTP availability monitoring
- DNS availability monitoring
- ICMP ping monitoring
- Packet loss detection
- Automatic outage detection
- SQLite database
- REST API
- Home Assistant Add-on
- Multi-architecture Docker images (amd64 / aarch64)
- Local Docker test environment
- Automated release process

---

# REST API

The Internet Monitor exposes the current monitoring status via HTTP.

## GET /status

Example response

```json
{
    "internet": true,
    "dns": true,
    "ping": 23.61,
    "packet_loss": 0.0,
    "timestamp": "2026-07-10T08:35:14Z",
    "version": "0.3.1"
}
```

---

# Home Assistant Configuration

The following settings can be configured directly from the Home Assistant Add-on configuration page.

| Option | Description | Default |
|---------|-------------|---------|
| HTTP Target | URL used for HTTP availability check | https://www.google.com |
| HTTP Timeout | HTTP request timeout (seconds) | 5 |
| DNS Target | DNS server used for DNS lookup | 8.8.8.8 |
| Ping Target | Host used for ICMP ping | 1.1.1.1 |
| Ping Count | Number of ICMP packets | 4 |
| Ping Timeout | Timeout per ICMP packet (seconds) | 2 |
| Check Interval | Monitoring interval (seconds) | 5 |

The effective configuration is logged automatically during application startup.

---

# Docker

Build

```bash
docker build -t internet-monitor .
```

Run

```bash
docker run \
    --rm \
    -p 8080:8080 \
    internet-monitor
```

REST API

```
http://localhost:8080/status
```

---

# Home Assistant Add-on

Repository

```
https://github.com/mariorauh/internet-monitor-addon
```

After installation the REST API is available via

```
http://<HOME_ASSISTANT_IP>:8080/status
```

---

# Local Docker Test

A complete local Docker test environment is included.

## Windows

```
test\test-docker.bat
```

## Linux / macOS

```bash
./test/test-docker.sh
```

The test environment automatically

- creates a dedicated Python virtual environment
- installs or updates required Python packages
- builds the Docker image
- starts the Docker container
- waits for the Docker Healthcheck
- validates the REST API
- continuously displays the current monitoring status

---

# Development

Clone the repository

```bash
git clone https://github.com/mariorauh/internet-monitor-backend.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run locally

```bash
python -m app.main
```

---

# Release

The repository contains an automated release tool.

Run

```bash
python release.py
```

The release tool automatically

- updates the backend version
- updates the Home Assistant Add-on version
- creates the Git commit
- creates the Git tag
- pushes the repository
- triggers the GitHub Actions Docker build

---

# Project Structure

```
internet-monitor-backend/

├── app/
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── internet_monitor.py
│   ├── logger.py
│   ├── models.py
│   ├── outage_detector.py
│   ├── ring_logger.py
│   ├── status.py
│   └── main.py
│
├── docker/
│   └── compose.yaml
│
├── test/
│   ├── .venv/
│   ├── requirements.txt
│   ├── test.py
│   ├── test-docker.bat
│   └── test-docker.sh
│
├── Dockerfile
├── requirements.txt
├── release.py
└── README.md
```

---

# Roadmap

## Version 0.3.x

- ✅ REST API
- ✅ Home Assistant configuration
- ✅ Local Docker test environment

## Version 0.4.x

- Home Assistant REST entities
- Internet status sensor
- DNS status sensor
- Ping sensor
- Packet loss sensor
- Availability sensor

## Version 0.5.x

- Historical REST endpoint
- Statistics endpoint
- Uptime calculation
- Outage history

## Version 1.0

- Stable public API
- Long-term statistics
- Dashboard support
- Grafana integration

---

# License

MIT License