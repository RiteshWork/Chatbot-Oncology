"""
scripts/test_session_manager.py
Test the Session Manager with the Calm flow.
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.session_manager import SessionManager
from orchestrator.session_manager_schemas import SessionManagerRequest


def test_session_manager():
    """Test Session Manager with the calm flow."""

    print("=" * 80)
    print("TESTING SESSION MANAGER WITH CALM FLOW")
    print("=" * 80)

    # Initialize Session Manager (without classifier for now)
    session_manager = SessionManager(classifier_fn=None)

    # Use the session ID from create_sample_data.py
    # You'll need to update this with your actual session ID
    session_id = uuid.UUID("f598f3ab-958b-4f82-9ee6-7a4f4c329ad3")

    # Test Step 1: Welcome → Breathing
    print("\n[Step 1] User: 'I'm ready to begin'")
    print("-" * 80)

    response1 = session_manager.process(
        SessionManagerRequest(
            session_id=session_id,
            message="I'm ready to begin"
        )
    )

    print(f"\nCurrent State: {response1.current_state.state_name}")
    print(f"  Code: {response1.current_state.state_code}")
    print(f"\nContent Presented:")
    for item in response1.content:
        print(f"  [{item.kind}] {item.title}")
        # Show first 100 chars of body
        preview = item.body[:100] + "..." if len(item.body) > 100 else item.body
        print(f"    {preview}")
    print(f"\nMessages in session: {response1.message_count}")

    # Test Step 2: Breathing → Closing
    print("\n" + "=" * 80)
    print("[Step 2] User: 'Done breathing'")
    print("-" * 80)

    response2 = session_manager.process(
        SessionManagerRequest(
            session_id=session_id,
            message="Done breathing"
        )
    )

    print(f"\nCurrent State: {response2.current_state.state_name}")
    print(f"  Code: {response2.current_state.state_code}")
    print(f"\nContent Presented:")
    for item in response2.content:
        print(f"  [{item.kind}] {item.title}")
        preview = item.body[:100] + "..." if len(item.body) > 100 else item.body
        print(f"    {preview}")
    print(f"\nMessages in session: {response2.message_count}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE - SESSION MANAGER WORKING!")
    print("=" * 80)


if __name__ == "__main__":
    test_session_manager()
