"""
sessions/models.py
The Session table — one patient running one process, in real time.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    patient_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    process_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("processes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    current_state_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("states.id", ondelete="SET NULL"),
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    session_metadata: Mapped[dict] = mapped_column(
        "metadata", JSON, nullable=False, default=dict,
    )

    def __repr__(self) -> str:
        return (
            f"<Session id={self.id} patient={self.patient_id!r} "
            f"process={self.process_id} ended={self.ended_at is not None}>"
        )