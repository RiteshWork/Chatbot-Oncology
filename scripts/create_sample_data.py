"""
scripts/create_sample_data.py
Create sample data for testing the chatbot flow.
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from states.models import State
from processes.models import Process
from library.models import LibraryItem
from sessions.models import Session


def create_sample_data():
    """Create all sample data for testing."""

    with get_session() as db:
        print("=" * 80)
        print("CREATING SAMPLE DATA FOR CALM FLOW")
        print("=" * 80)

        # Create States
        print("\n[1] Creating States...")

        state_welcome = State(
            id=uuid.uuid4(),
            code="calm_welcome",
            name="Welcome - Comfortable & Ready",
            description="Patient acknowledges they are comfortable and ready for guided imagery"
        )

        state_breath = State(
            id=uuid.uuid4(),
            code="calm_breath_observation",
            name="Observe Your Breath",
            description="Guided breath observation with anchor word technique (calm/release)"
        )

        state_closing = State(
            id=uuid.uuid4(),
            code="calm_closing",
            name="Closing & Affirmation",
            description="Gentle return to awareness and closing affirmation"
        )

        db.add_all([state_welcome, state_breath, state_closing])
        db.flush()

        print(f"  Created state: {state_welcome.name}")
        print(f"  Created state: {state_breath.name}")
        print(f"  Created state: {state_closing.name}")

        # Create Process
        print("\n[2] Creating Process...")

        process_definition = {
            "initial_state": str(state_welcome.id),
            "states": {
                str(state_welcome.id): {
                    "transitions": [
                        {
                            "condition": "True",
                            "target": str(state_breath.id)
                        }
                    ]
                },
                str(state_breath.id): {
                    "transitions": [
                        {
                            "condition": "True",
                            "target": str(state_closing.id)
                        }
                    ]
                },
                str(state_closing.id): {
                    "transitions": []
                }
            },
            "end_states": [str(state_closing.id)]
        }

        process = Process(
            id=uuid.uuid4(),
            code="calm_v1",
            name="Calm - Guided Breath Observation",
            description="A complete calming experience using guided breath observation",
            definition=process_definition,
            is_active=True
        )

        process.validate_definition()
        db.add(process)
        db.flush()

        print(f"  Created process: {process.name}")
        print(f"    Flow: Welcome -> Breath -> Closing")

        # Create Library Items
        print("\n[3] Creating Library Items...")

        lib_welcome = LibraryItem(
            id=uuid.uuid4(),
            kind="script",
            title="Welcome Script",
            body="I'm glad you're feeling ready. That's great to hear. We'll move at a calm, comfortable pace. You're in control throughout the process. Let's begin with some slow, steady breathing.",
            item_metadata={"intent": "calm", "state": "welcome"}
        )

        lib_breath = LibraryItem(
            id=uuid.uuid4(),
            kind="script",
            title="Observe Your Breath - Guided Script",
            body="Take a comfortable position and gently bring your attention to your breath. No need to change it, just noticing it as it flows in and out. If it helps, you can silently say 'calm' as you breathe in and 'release' as you breathe out. Continue for a few moments, just breathing and observing.",
            item_metadata={"intent": "calm", "technique": "anchor_word_breathing"}
        )

        lib_closing = LibraryItem(
            id=uuid.uuid4(),
            kind="script",
            title="Closing & Return to Awareness",
            body="And when you're ready, begin to slowly expand your awareness. Noticing your body again, the space around you. You did wonderful work here today. Remember, you can return to this calm breathing anytime you need it.",
            item_metadata={"intent": "calm", "state": "closing"}
        )

        db.add_all([lib_welcome, lib_breath, lib_closing])

        print(f"  Created library item: Welcome Script")
        print(f"  Created library item: Observe Your Breath")
        print(f"  Created library item: Closing & Return")

        # Create Test Session
        print("\n[4] Creating Test Session...")

        test_session = Session(
            id=uuid.uuid4(),
            patient_id="test_patient",
            process_id=process.id,
            current_state_id=state_welcome.id,
            session_metadata={"messages": [], "created_by": "seed_script"}
        )

        db.add(test_session)

        print(f"  Created session: {test_session.id}")
        print(f"    Patient: {test_session.patient_id}")
        print(f"    Starting state: {state_welcome.name}")

        # Commit
        db.commit()

        print("\n" + "=" * 80)
        print("SUCCESS! SAMPLE DATA CREATED")
        print("=" * 80)
        print(f"States: 3")
        print(f"Process: 1")
        print(f"Library Items: 3")
        print(f"Test Session: 1")
        print(f"Session ID: {test_session.id}")
        print("=" * 80)


if __name__ == "__main__":
    create_sample_data()
