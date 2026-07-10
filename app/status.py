from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from threading import Lock


@dataclass
class Status:

    internet: bool = False
    dns: bool = False
    ping: float = 0.0
    packet_loss: float = 0.0
    timestamp: str = ""
    version: str = ""


class StatusStore:

    def __init__(self) -> None:

        self._lock = Lock()

        self._status = Status()

    def update(
        self,
        internet: bool,
        dns: bool,
        ping: float,
        packet_loss: float,
        version: str,
    ) -> None:

        with self._lock:

            self._status = Status(
                internet=internet,
                dns=dns,
                ping=ping,
                packet_loss=packet_loss,
                timestamp=datetime.now(UTC).isoformat(),
                version=version,
            )

    def get(self) -> dict:

        with self._lock:
            return asdict(self._status)


status_store = StatusStore()