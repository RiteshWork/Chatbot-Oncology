"""
orchestrator/schemas.py
Pydantic schemas for Orchestrator input and output.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# INPUT SCHEMAS
# ============================================================================

class ClassifierOutput(BaseModel):
    """Output from the Classifier component."""
    intent: str = Field(..., description="User's intent (e.g., 'request_breathing')")
    emotion: str | None = Field(None, description="Detected emotion (e.g., 'anxious')")
    stress_level: float | None = Field(None, ge=0, le=10, description="Stress level 0-10")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Confidence of classification")


class OrchestratorRequest(BaseModel):
    """Input to Orchestrator.process()"""
    session_id: uuid.UUID = Field(..., description="Session ID")
    message: str = Field(..., description="User message")
    classifier_output: ClassifierOutput | None = Field(
        None,
        description="Output from classifier (optional)"
    )


# ============================================================================
# OUTPUT SCHEMAS
# ============================================================================

class OrchestratorResponse(BaseModel):
    """Output from Orchestrator.process() - all fetched data."""

    session: dict = Field(..., description="Session record from database")
    process: dict = Field(..., description="Process record with definition")
    state: dict = Field(..., description="Current state record")
    content: list[dict] = Field(default_factory=list, description="Library items for state")
    next_state_id: uuid.UUID = Field(..., description="ID of next state")
    transition_taken: str | None = Field(None, description="Condition that matched")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TransitionConditionEvaluation(BaseModel):
    """Result of evaluating a single transition condition."""
    condition: str = Field(..., description="The condition string")
    matched: bool = Field(..., description="Whether condition evaluated to true")
    target_state_id: uuid.UUID | None = Field(None, description="Target if matched")


class StateTransitionResult(BaseModel):
    """Result of evaluating all transitions for a state."""
    current_state_id: uuid.UUID = Field(..., description="Current state")
    next_state_id: uuid.UUID = Field(..., description="Selected next state")
    transitions_evaluated: list[TransitionConditionEvaluation] = Field(
        default_factory=list,
        description="All transitions that were evaluated"
    )
    matched_condition: str | None = Field(None, description="Condition that matched")
