"""
sessions/schemas.py
Pydantic shapes for Session.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SessionBase(BaseModel):
    patient_id: str = Field(..., max_length=128)
    process_id: uuid.UUID
    current_state_id: uuid.UUID | None = None
    session_metadata: dict[str, Any] = Field(default_factory=dict)


class SessionCreate(SessionBase):
    """Payload to start a new session. patient_id and process_id are
    required; everything else has sensible defaults."""
    pass


class SessionRead(SessionBase):
    """Shape returned when reading a session back."""
    id: uuid.UUID
    started_at: datetime
    ended_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)