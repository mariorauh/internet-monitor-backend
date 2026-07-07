from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Measurement:

    timestamp: datetime

    internet_ok: bool

    dns_ok: bool

    ping_ms: float | None

    packet_loss: float