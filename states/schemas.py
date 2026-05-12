"""
states/schemas.py
Pydantic shapes for State.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StateBase(BaseModel):
    code: str = Field(..., max_length=64)
    name: str = Field(..., max_length=255)
    description: str | None = None


class StateCreate(StateBase):
    """Payload to create a new state. No id, no timestamps."""
    pass


class StateRead(StateBase):
    """Shape returned when reading a state back."""
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)