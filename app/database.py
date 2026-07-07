from datetime import datetime, timedelta

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
    select,
    delete,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)

import app.config as config
from app.models import Measurement


# =============================================================================
# Base
# =============================================================================

class Base(DeclarativeBase):
    pass


# =============================================================================
# Measurement Table
# =============================================================================

class MeasurementEntity(Base):

    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    timestamp: Mapped[datetime] = mapped_column(DateTime)

    internet_ok: Mapped[bool] = mapped_column(Boolean)

    dns_ok: Mapped[bool] = mapped_column(Boolean)

    ping_ms: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    packet_loss: Mapped[float] = mapped_column(Float)


# =============================================================================
# Outage Table
# =============================================================================

class OutageEntity(Base):

    __tablename__ = "outages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    start_time: Mapped[datetime] = mapped_column(DateTime)

    end_time: Mapped[datetime] = mapped_column(DateTime)

    duration_seconds: Mapped[int] = mapped_column(Integer)

    reason: Mapped[str] = mapped_column(String)


# =============================================================================
# Database
# =============================================================================

class Database:

    def __init__(self):

        config.DATA_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.engine = create_engine(
            f"sqlite:///{config.DATABASE_FILE}",
            echo=False,
        )

        Base.metadata.create_all(self.engine)

    # -------------------------------------------------------------------------
    # Measurements
    # -------------------------------------------------------------------------

    def save_measurement(
        self,
        measurement: Measurement,
    ) -> None:

        with Session(self.engine) as session:

            entity = MeasurementEntity(
                timestamp=measurement.timestamp,
                internet_ok=measurement.internet_ok,
                dns_ok=measurement.dns_ok,
                ping_ms=measurement.ping_ms,
                packet_loss=measurement.packet_loss,
            )

            session.add(entity)
            session.commit()

    # -------------------------------------------------------------------------

    def get_last_measurements(
        self,
        limit: int = 100,
    ) -> list[MeasurementEntity]:

        with Session(self.engine) as session:

            stmt = (
                select(MeasurementEntity)
                .order_by(MeasurementEntity.id.desc())
                .limit(limit)
            )

            return list(session.scalars(stmt))

    # -------------------------------------------------------------------------
    # Outages
    # -------------------------------------------------------------------------

    def save_outage(
        self,
        start_time: datetime,
        end_time: datetime,
        duration_seconds: int,
        reason: str,
    ) -> None:

        with Session(self.engine) as session:

            outage = OutageEntity(
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration_seconds,
                reason=reason,
            )

            session.add(outage)
            session.commit()

    # -------------------------------------------------------------------------

    def get_outages(self) -> list[OutageEntity]:

        with Session(self.engine) as session:

            stmt = (
                select(OutageEntity)
                .order_by(
                    OutageEntity.start_time.desc()
                )
            )

            return list(session.scalars(stmt))

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------

    def cleanup_measurements(
        self,
        keep_days: int,
    ) -> None:

        cutoff = (
            datetime.now()
            - timedelta(days=keep_days)
        )

        with Session(self.engine) as session:

            stmt = delete(
                MeasurementEntity
            ).where(
                MeasurementEntity.timestamp < cutoff
            )

            session.execute(stmt)

            session.commit()