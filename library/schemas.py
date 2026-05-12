"""
library/schemas.py
pydantic shapes for LibraryItem - used at the API boundary.
"""

from __future__ import  annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class LibraryItemBase(BaseModel):
    kind: str = Field(..., max_length=64)
    title: str = Field(..., max_length=255)
    body: str
    item_metadata: dict[str, Any] = Field(default_factory=dict)

class LibraryItemCreate(LibraryItemBase):
    """Payload to create a new library item, no id, no timestamps."""
    pass
class LibraryItemRead(LibraryItemBase):
    """Shape returned when reading a library item back."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
