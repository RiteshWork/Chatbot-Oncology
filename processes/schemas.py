"""
processes/schemas.py
Pydantic shapes for Process.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProcessBase(BaseModel):
    code: str = Field(..., max_length=64)
    name: str = Field(..., max_length=255)
    description: str | None = None
    definition: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class ProcessCreate(ProcessBase):
    """Payload to create a new process. No id, no timestamps."""
    pass


class ProcessRead(ProcessBase):
    """Shape returned when reading a process back."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)