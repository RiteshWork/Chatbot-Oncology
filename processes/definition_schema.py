"""
processes/definition_schema.py
Pydantic schema to validate Process.definition structure.

This ensures that whenever a Process is created or updated,
its definition matches the expected workflow structure.

DESIGN CHOICES:
- condition & target: REQUIRED (transitions need both to work)
- transitions: Defaults to [] (empty = end state, no further transitions)
- end_states: Defaults to [] (process can rely on states with no transitions)
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Dict


class StateTransition(BaseModel):
    """
    A single transition rule in a state.

    Defines: IF condition is true, THEN go to target state.

    Both condition and target are REQUIRED because:
    - condition: Tells orchestrator WHEN to transition
    - target: Tells orchestrator WHERE to go
    """
    condition: str = Field(..., description="Condition to evaluate (e.g., 'true', 'stress_level > 8')")
    target: str = Field(..., description="UUID of target state as string")


class StateConfig(BaseModel):
    """
    Configuration for a single state in the workflow.

    transitions defaults to [] (empty list) because:
    - Empty transitions = this is an END state
    - Patient cannot move further from this state
    - Session effectively ends here
    """
    transitions: List[StateTransition] = Field(
        default_factory=list,
        description="List of transitions from this state (empty list = end state)"
    )


class ProcessDefinition(BaseModel):
    """
    Complete process workflow definition.

    This is the state machine that defines how a process flows
    from initial state through various states and transitions.

    end_states defaults to [] (empty list) because:
    - Process can rely on states with no transitions instead
    - Not all processes need explicit end_states list
    - Provides flexibility in process design
    """
    initial_state: str = Field(..., description="UUID of initial state as string")
    states: Dict[str, StateConfig] = Field(..., description="Map of state_uuid -> StateConfig")
    end_states: List[str] = Field(
        default_factory=list,
        description="List of state UUIDs that end the process (optional)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "initial_state": "550e8400-e29b-41d4-a716-446655440001",
                "states": {
                    "550e8400-e29b-41d4-a716-446655440001": {
                        "transitions": [
                            {
                                "condition": "true",
                                "target": "550e8400-e29b-41d4-a716-446655440002"
                            }
                        ]
                    },
                    "550e8400-e29b-41d4-a716-446655440002": {
                        "transitions": []
                    }
                },
                "end_states": ["550e8400-e29b-41d4-a716-446655440002"]
            }
        }
