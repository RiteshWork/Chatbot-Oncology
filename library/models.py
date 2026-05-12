"""
library/models.py
The libraryItem table -  content th bot can present (scripts, prompt, audio refs).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from db import Base

class LibraryItem(Base):
    __tablename__ = "library_items"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    kind: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    item_metadata: Mapped[dict] = mapped_column(
        "metadata", JSON, nullable=False, default=dict,
    )

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


    def __repr__(self) -> str:
        return f"<LibraryItem id={self.id} kind={self.kind!r} title={self.title!r} >"