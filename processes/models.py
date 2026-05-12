"""
processes/models.py
The Process table — a named flow the bot can run with a patient.
"""

from __future__ import annotations

import uuid
import logging
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from .definition_schema import ProcessDefinition

logger = logging.getLogger(__name__)


class Process(Base):
    __tablename__ = "processes"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    code: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    definition: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def validate_definition(self) -> bool:
        """
        Validate that definition matches ProcessDefinition schema.

        This ensures the definition has:
        - initial_state (UUID of starting state)
        - states (dict of state configs with transitions)
        - end_states (list of final states, optional)

        Raises:
            ValueError: If definition is invalid

        Returns:
            True if valid
        """
        try:
            ProcessDefinition(**self.definition)
            logger.info(f"Process {self.code} definition is valid")
            return True
        except Exception as e:
            logger.error(f"Process {self.code} definition is invalid: {e}")
            raise ValueError(f"Invalid process definition: {e}")

    def __repr__(self) -> str:
        return f"<Process code={self.code!r} active={self.is_active}>"