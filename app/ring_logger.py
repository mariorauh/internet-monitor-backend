from __future__ import annotations

import logging
from collections import deque
from pathlib import Path


class RingFileHandler(logging.Handler):
    """
    Logging handler with a maximum number of log lines.

    The newest log entries are always kept.
    Older entries are automatically discarded.
    """

    def __init__(self, filename: str, max_lines: int = 100000) -> None:
        super().__init__()

        self.file = Path(filename)
        self.max_lines = max_lines

        self.file.parent.mkdir(parents=True, exist_ok=True)

        if self.file.exists():
            with self.file.open("r", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            lines = []

        self.buffer = deque(lines, maxlen=max_lines)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record) + "\n"

            self.buffer.append(message)

            with self.file.open("w", encoding="utf-8") as f:
                f.writelines(self.buffer)

        except Exception:
            self.handleError(record)