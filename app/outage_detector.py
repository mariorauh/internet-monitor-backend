from datetime import datetime

from app.database import Database
from app.models import Measurement


class OutageDetector:

    def __init__(self, database: Database):

        self.database = database

        self.outage_active = False

        self.start_time: datetime | None = None

    # -------------------------------------------------------------------------

    def process(
        self,
        measurement: Measurement,
    ) -> None:

        # ------------------------------------------------------------
        # Internet failed
        # ------------------------------------------------------------

        if (
            not measurement.internet_ok
            and not self.outage_active
        ):

            self.outage_active = True

            self.start_time = measurement.timestamp

            return

        # ------------------------------------------------------------
        # Internet restored
        # ------------------------------------------------------------

        if (
            measurement.internet_ok
            and self.outage_active
        ):

            end_time = measurement.timestamp

            duration = int(
                (
                    end_time
                    - self.start_time
                ).total_seconds()
            )

            self.database.save_outage(
                start_time=self.start_time,
                end_time=end_time,
                duration_seconds=duration,
                reason="Internet unavailable",
            )

            self.outage_active = False

            self.start_time = None