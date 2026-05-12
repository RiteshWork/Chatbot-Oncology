"""
orchestrator/engine.py
Core Orchestrator engine - stateless business logic for session routing.

The Orchestrator:
1. Loads Session from database
2. Loads Process definition
3. Evaluates transition conditions
4. Updates Session in database
5. Fetches State details
6. Fetches Library content
7. Returns all fetched data to Session Manager
"""

from __future__ import annotations

import uuid
import logging
from typing import Any
from datetime import datetime, timezone

from sqlalchemy.orm import Session as DBSession

from db import get_session
from processes.models import Process
from sessions.models import Session
from states.models import State
from library.models import LibraryItem
from processes.schemas import ProcessRead
from sessions.schemas import SessionRead
from states.schemas import StateRead
from library.schemas import LibraryItemRead

from .schemas import (
    OrchestratorRequest,
    OrchestratorResponse,
    ClassifierOutput,
)

logger = logging.getLogger(__name__)


class OrchestratorEngine:
    """
    Orchestrator engine - handles all business logic for session routing.

    Stateless: Can be instantiated once and reused across requests.
    """

    def process(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """
        Main orchestration flow.

        Args:
            request: OrchestratorRequest with session_id, message, classifier_output

        Returns:
            OrchestratorResponse with all fetched data

        Raises:
            ValueError: If session or process not found
        """
        with get_session() as db:
            # Step 1: Load Session
            session = self._load_session(db, request.session_id)

            # Step 2: Load Process
            process = self._load_process(db, session.process_id)

            # Step 3: Evaluate transitions and select next state
            next_state_id = self._evaluate_and_select_next_state(
                db=db,
                process=process,
                session=session,
                classifier_output=request.classifier_output,
            )

            # Step 4: Update Session in database
            self._update_session(
                db=db,
                session=session,
                next_state_id=next_state_id,
                message=request.message,
                classifier_output=request.classifier_output,
            )

            # Step 5: Fetch State details
            state = self._fetch_state(db, next_state_id)

            # Step 6: Fetch Library content
            content = self._fetch_library_content(db, next_state_id)

            # Step 7: Build and return response
            return OrchestratorResponse(
                session=SessionRead.model_validate(session).model_dump(),
                process=ProcessRead.model_validate(process).model_dump(),
                state=StateRead.model_validate(state).model_dump(),
                content=[LibraryItemRead.model_validate(item).model_dump() for item in content],
                next_state_id=next_state_id,
                transition_taken=None,
            )

    def _load_session(self, db: DBSession, session_id: uuid.UUID) -> Session:
        """Step 1: Load session from database."""
        logger.info(f"Loading session: {session_id}")
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        return session

    def _load_process(self, db: DBSession, process_id: uuid.UUID) -> Process:
        """Step 2: Load process definition from database."""
        logger.info(f"Loading process: {process_id}")
        process = db.query(Process).filter(Process.id == process_id).first()
        if not process:
            raise ValueError(f"Process not found: {process_id}")
        return process

    def _evaluate_and_select_next_state(
        self,
        db: DBSession,
        process: Process,
        session: Session,
        classifier_output: ClassifierOutput | None,
    ) -> uuid.UUID:
        """Step 3: Evaluate transitions and select next state."""
        current_state_id = session.current_state_id
        logger.info(f"Evaluating transitions from state: {current_state_id}")

        definition = process.definition
        if not definition or "states" not in definition:
            return current_state_id

        state_config = definition["states"].get(str(current_state_id))
        if not state_config:
            return current_state_id

        transitions = state_config.get("transitions", [])
        if not transitions:
            return current_state_id

        for transition in transitions:
            condition = transition.get("condition")
            target = transition.get("target")

            if not condition or not target:
                continue

            if self._evaluate_condition(condition, session.session_metadata, classifier_output):
                logger.info(f"Condition matched: '{condition}' → {target}")
                return uuid.UUID(target)

        return current_state_id

    def _evaluate_condition(
        self,
        condition: str,
        session_metadata: dict,
        classifier_output: ClassifierOutput | None = None,
    ) -> bool:
        """Evaluate a single transition condition."""
        logger.debug(f"Evaluating condition: {condition}")
        context = self._build_evaluation_context(session_metadata, classifier_output)

        try:
            result = eval(condition, {"__builtins__": {}}, context)
            return bool(result)
        except Exception as e:
            logger.error(f"Error evaluating condition '{condition}': {e}")
            return False

    def _build_evaluation_context(
        self,
        session_metadata: dict,
        classifier_output: ClassifierOutput | None = None,
    ) -> dict[str, Any]:
        """Build context dict for condition evaluation."""
        context = {}

        if classifier_output:
            context["intent"] = classifier_output.intent
            context["emotion"] = classifier_output.emotion
            context["stress_level"] = classifier_output.stress_level or 0
            context["confidence"] = classifier_output.confidence
        else:
            context["intent"] = None
            context["emotion"] = None
            context["stress_level"] = 0
            context["confidence"] = 0

        if "user_responses" in session_metadata:
            context.update(session_metadata["user_responses"])

        for key, value in session_metadata.items():
            if key not in ["messages", "classifier_output"] and not key.startswith("_"):
                context[key] = value

        return context

    def _update_session(
        self,
        db: DBSession,
        session: Session,
        next_state_id: uuid.UUID,
        message: str,
        classifier_output: ClassifierOutput | None = None,
    ) -> None:
        """Step 4: Update session in database with new state and metadata."""
        logger.info(f"Updating session: {session.id}")

        session.current_state_id = next_state_id

        if not session.session_metadata:
            session.session_metadata = {}

        if "messages" not in session.session_metadata:
            session.session_metadata["messages"] = []

        session.session_metadata["messages"].append({
            "role": "user",
            "content": message,
        })

        if classifier_output:
            session.session_metadata["classifier_output"] = classifier_output.model_dump()

        session.session_metadata["last_updated"] = datetime.now(timezone.utc).isoformat()

    def _fetch_state(self, db: DBSession, state_id: uuid.UUID) -> State:
        """Step 5: Fetch state details from database."""
        logger.info(f"Fetching state: {state_id}")
        state = db.query(State).filter(State.id == state_id).first()
        if not state:
            raise ValueError(f"State not found: {state_id}")
        return state

    def _fetch_library_content(self, db: DBSession, state_id: uuid.UUID) -> list[LibraryItem]:
        """Step 6: Fetch library items for a state."""
        logger.info(f"Fetching library content for state: {state_id}")
        items = db.query(LibraryItem).all()
        logger.debug(f"Fetched {len(items)} library items")
        return items
