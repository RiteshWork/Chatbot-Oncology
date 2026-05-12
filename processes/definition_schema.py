"""
processes/definition_schema.py
Pydantic schema to validate Process.definition structure.
"""

from pydantic import BaseModel

# Class 1: StateTransition
# - Fields: condition (str), target (str)
# - Both required

# Class 2: StateConfig
# - Fields: transitions (list of StateTransition)
# - transitions can be empty list (optional/default to [])

# Class 3: ProcessDefinition
# - Fields: initial_state (str), states (dict), end_states (list)
# - All required
# - states is dict where key=state_uuid, value=StateConfig

from pydantic import BaseModel
from typing import List, Dict

class StateTransition(BaseModel):
    condition: str = #???  # What goes here?
    target: str = #???     # What goes here?

    class StateConfig(BaseModel):
        transitions: List[StateTransition] = #???  # What's the default?

        class ProcessDefinition(BaseModel):
            initial_state: str
            states: Dict[str, StateConfig]
            end_states: List[str] = #???  # What's the default?