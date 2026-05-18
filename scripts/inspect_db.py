"""
scripts/inspect_db.py
Inspect what's currently in the database.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from processes.models import Process
from states.models import State
from library.models import LibraryItem
from sessions.models import Session


def inspect_db():
    """Inspect database contents."""

    with get_session() as db:
        print("\n" + "=" * 80)
        print("DATABASE INSPECTION")
        print("=" * 80)

        # 1. Processes
        print("\n[1] PROCESSES")
        print("-" * 80)
        processes = db.query(Process).all()
        if processes:
            for proc in processes:
                print(f"\n  ID: {proc.id}")
                print(f"  Code: {proc.code}")
                print(f"  Name: {proc.name}")
                print(f"  Description: {proc.description}")
                print(f"  Active: {proc.is_active}")
                if proc.definition:
                    print(f"  Initial State: {proc.definition.get('initial_state', 'N/A')}")
                    num_states = len(proc.definition.get('states', {}))
                    print(f"  Total States in Process: {num_states}")
        else:
            print("  No processes found")

        # 2. States
        print("\n[2] STATES")
        print("-" * 80)
        states = db.query(State).all()
        if states:
            for state in states:
                print(f"\n  ID: {state.id}")
                print(f"  Code: {state.code}")
                print(f"  Name: {state.name}")
        else:
            print("  No states found")

        # 3. Library Items Summary
        print("\n[3] LIBRARY ITEMS")
        print("-" * 80)
        library_items = db.query(LibraryItem).all()

        if library_items:
            print(f"\n  Total Items: {len(library_items)}")

            # Group by step
            items_by_step = {}
            items_by_type = {}
            items_by_emotion = {}

            for item in library_items:
                metadata = item.item_metadata or {}
                step = metadata.get("step", "unknown")
                item_type = metadata.get("type", "unknown")
                emotion = metadata.get("emotional_state", "unknown")

                if step not in items_by_step:
                    items_by_step[step] = []
                items_by_step[step].append(item)

                if item_type not in items_by_type:
                    items_by_type[item_type] = 0
                items_by_type[item_type] += 1

                if emotion not in items_by_emotion:
                    items_by_emotion[emotion] = 0
                items_by_emotion[emotion] += 1

            print("\n  By Step:")
            for step in sorted(items_by_step.keys()):
                print(f"    Step {step}: {len(items_by_step[step])} items")

            print("\n  By Type:")
            for item_type, count in sorted(items_by_type.items()):
                print(f"    {item_type}: {count} items")

            print("\n  By Emotional State:")
            for emotion, count in sorted(items_by_emotion.items()):
                print(f"    {emotion}: {count} items")

            print("\n  First 5 Library Items:")
            for i, item in enumerate(library_items[:5]):
                metadata = item.item_metadata or {}
                print(f"\n    [{i+1}] {item.title}")
                print(f"        Kind: {item.kind}")
                print(f"        Step: {metadata.get('step', 'N/A')}")
                print(f"        Type: {metadata.get('type', 'N/A')}")
                print(f"        Emotion: {metadata.get('emotional_state', 'N/A')}")
                print(f"        Body Preview: {item.body[:80]}...")
        else:
            print("  No library items found")

        # 4. Sessions
        print("\n[4] SESSIONS")
        print("-" * 80)
        sessions = db.query(Session).all()
        if sessions:
            print(f"\n  Total Sessions: {len(sessions)}")
            for session in sessions[-5:]:  # Show last 5
                print(f"\n  ID: {session.id}")
                print(f"  Patient: {session.patient_id}")
                print(f"  Process: {session.process_id}")
                print(f"  Current State: {session.current_state_id}")
                print(f"  Started: {session.started_at}")
        else:
            print("  No sessions found")

        print("\n" + "=" * 80)
        print("END OF INSPECTION")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        inspect_db()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
