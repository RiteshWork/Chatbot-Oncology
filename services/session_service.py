"""
services/session_service.py
Service for creating and managing sessions.

Handles:
- Auto-creating sessions with a process
- Retrieving existing sessions
- Session initialization
"""

from __future__ import annotations

import uuid
import logging
from datetime import datetime, timezone

from db import get_session
from sessions.models import Session
from processes.models import Process

logger = logging.getLogger(__name__)


class SessionService:
    """Service for session creation and management."""

    @staticmethod
    def create_session(patient_id: str, process_code: str = "calm_v1") -> Session:
        """
        Auto-create a new session with a process.

        Finds the process by code (e.g., "calm_v1") and creates a session
        that starts at the process's initial state.

        Args:
            patient_id: Identifier for the patient
            process_code: Code of the process to use (default: calm_v1)

        Returns:
            Created Session object

        Raises:
            ValueError: If process not found
        """
        with get_session() as db:
            logger.info(f"[SessionService] Creating session for patient {patient_id} with process {process_code}")

            # Find process by code
            process = db.query(Process).filter(Process.code == process_code).first()
            if not process:
                raise ValueError(f"Process {process_code} not found")

            # Get initial state from process definition
            initial_state_id = process.definition.get("initial_state")
            if not initial_state_id:
                raise ValueError(f"Process {process_code} has no initial state")

            # Create session at initial state
            new_session = Session(
                id=uuid.uuid4(),
                patient_id=patient_id,
                process_id=process.id,
                current_state_id=uuid.UUID(initial_state_id),
                session_metadata={
                    "messages": [],
                    "created_by": "api",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
            )

            db.add(new_session)
            db.commit()

            logger.info(f"[SessionService] Session created: {new_session.id}")
            return new_session

    @staticmethod
    def get_session(session_id: uuid.UUID) -> Session | None:
        """
        Retrieve a session by ID.

        Args:
            session_id: UUID of the session

        Returns:
            Session object or None if not found
        """
        with get_session() as db:
            session = db.query(Session).filter(Session.id == session_id).first()
            return session
