"""
scripts/cleanup_db.py
Clean up database before recreating sample data.

This script removes:
1. All sessions
2. All processes
3. All states
4. All library items
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from sessions.models import Session
from processes.models import Process
from states.models import State
from library.models import LibraryItem


def cleanup_db():
    """Clean up all database records."""

    with get_session() as db:
        print("=" * 80)
        print("CLEANING UP DATABASE")
        print("=" * 80)

        # Delete in order of dependencies
        print("\n[1] Deleting sessions...")
        session_count = db.query(Session).delete()
        print(f"  Deleted {session_count} sessions")

        print("\n[2] Deleting processes...")
        process_count = db.query(Process).delete()
        print(f"  Deleted {process_count} processes")

        print("\n[3] Deleting states...")
        state_count = db.query(State).delete()
        print(f"  Deleted {state_count} states")

        print("\n[4] Deleting library items...")
        lib_count = db.query(LibraryItem).delete()
        print(f"  Deleted {lib_count} library items")

        # Commit all deletions
        db.commit()

        print("\n" + "=" * 80)
        print("DATABASE CLEANUP COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    try:
        cleanup_db()
    except Exception as e:
        print(f"Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
