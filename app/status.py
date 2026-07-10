from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from threading import Lock


@dataclass(slots=True)
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
                ping=round(ping, 2),
                packet_loss=round(packet_loss, 2),
                timestamp=datetime.now(UTC).isoformat(),
                version=version,
            )

    def get(self) -> Status:

        with self._lock:
            return self._status


status_store = StatusStore()


def status_as_dict() -> dict:
    return asdict(status_store.get())