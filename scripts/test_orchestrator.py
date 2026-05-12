"""
scripts/test_orchestrator.py
Test the Orchestrator with the sample data we created.
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.engine import OrchestratorEngine
from orchestrator.schemas import OrchestratorRequest

def test_orchestrator():
    """Test the full Calm flow."""

    print("=" * 80)
    print("TESTING ORCHESTRATOR WITH CALM FLOW")
    print("=" * 80)

    orchestrator = OrchestratorEngine()

    # Use the session ID from create_sample_data.py output
    session_id = uuid.UUID("1b85aec8-73d9-4a9b-aa62-44225cd55a1f")

    # Test Step 1: Welcome → Breathing
    print("\n[Step 1] Welcome state → Breathing state")
    print("-" * 80)

    response1 = orchestrator.process(
        OrchestratorRequest(
            session_id=session_id,
            message="I'm ready to begin",
            classifier_output=None
        )
    )

    print(f"Response: {response1}")
    print()

    # Test Step 2: Breathing → Closing
    print("[Step 2] Breathing state → Closing state")
    print("-" * 80)

    response2 = orchestrator.process(
        OrchestratorRequest(
            session_id=session_id,
            message="Done breathing",
            classifier_output=None
        )
    )

    print(f"Response: {response2}")
    print()

    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_orchestrator()