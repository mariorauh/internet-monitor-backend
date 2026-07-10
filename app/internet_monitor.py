from datetime import datetime
import socket

import requests
from ping3 import ping

import app.config as config
from app.models import Measurement


class InternetMonitor:

    def measure(self) -> Measurement:

        dns_ok = self._check_dns()

        ping_ms, packet_loss = self._measure_ping()

        http_ok = self._check_http()

        internet_ok = (
            dns_ok
            and http_ok
            and ping_ms is not None
        )

        return Measurement(
            timestamp=datetime.now(),
            internet_ok=internet_ok,
            dns_ok=dns_ok,
            ping_ms=ping_ms,
            packet_loss=packet_loss,
        )

    # -------------------------------------------------------------------------

    def _check_dns(self) -> bool:

        try:

            socket.gethostbyname(
                config.DNS_TARGET
            )

            return True

        except Exception:

            return False

    # -------------------------------------------------------------------------

    def _check_http(self) -> bool:

        try:

            response = requests.get(
                config.HTTP_TARGET,
                timeout=config.HTTP_TIMEOUT,
            )

            return response.status_code < 400

        except Exception:

            return False

    # -------------------------------------------------------------------------

    def _measure_ping(
        self,
    ) -> tuple[float | None, float]:

        successful_pings = []

        for _ in range(config.PING_COUNT):

            response = ping(
                config.PING_TARGET,
                timeout=config.PING_TIMEOUT,
            )

            if response is not None:

                successful_pings.append(
                    response * 1000
                )

        packet_loss = (
            (
                config.PING_COUNT
                - len(successful_pings)
            )
            / config.PING_COUNT
        ) * 100

        if successful_pings:

            average_ping = round(
                sum(successful_pings)
                / len(successful_pings),
                2,
            )

        else:

            average_ping = None
            
        

        return (
            average_ping,
            packet_loss,
        )