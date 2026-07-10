# Internet Monitor

A lightweight Home Assistant add-on for monitoring Internet connectivity,
detecting outages and providing a REST API for automation and dashboards.

---

## Features

- Continuous Internet connectivity monitoring
- DNS availability monitoring
- ICMP latency measurement
- Packet loss detection
- Outage detection
- SQLite database
- REST API
- Docker support
- Home Assistant Add-on
- Multi-architecture Docker images
- Automated GitHub releases

---

## REST API

The Internet Monitor exposes the current monitoring status via HTTP.

### GET /status

Example response

```json
{
    "internet": true,
    "dns": true,
    "ping": 23.61,
    "packet_loss": 0.0,
    "timestamp": "2026-07-10T08:35:14Z",
    "version": "0.3.0"
}
```

---

## Docker

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

## Home Assistant Add-on

Install the repository

```
https://github.com/mariorauh/internet-monitor-addon
```

After installation the add-on exposes

```
http://<HA-IP>:8080/status
```

---

## Development

Clone

```bash
git clone https://github.com/mariorauh/internet-monitor-backend.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python -m app.main
```

---

## Local Docker Test

The repository contains a complete local Docker test environment.

Windows

```text
test\test-docker.bat
```

Linux / macOS

```bash
./test/test-docker.sh
```

The test automatically

- creates a virtual environment
- installs required Python packages
- builds the Docker image
- starts the container
- waits for the Docker health check
- validates the REST API
- continuously displays the current monitoring status

---

## Release

A release is created using

```bash
python release.py
```

The release tool automatically

- updates the application version
- updates the Home Assistant add-on version
- creates the Git commit
- creates the Git tag
- pushes the repository
- publishes the Docker image via GitHub Actions

---

## Project Structure

```
internet-monitor-backend/

├── app/
├── test/
├── Dockerfile
├── release.py
└── requirements.txt
```

---

## Roadmap

### Version 0.3.x

- REST API
- Home Assistant REST sensors
- Local Docker testing

### Version 0.4.x

- Statistics endpoint
- Historical data endpoint

### Version 0.5.x

- Grafana support
- Long-term statistics

---

## License

MIT License