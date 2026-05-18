"""
scripts/interactive_chat.py
Interactive chatbot conversation for testing the full RAG + LLM pipeline.

Shows the complete conversation flow step-by-step.
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.session_manager import SessionManager
from orchestrator.session_manager_schemas import SessionManagerRequest
from services.session_service import SessionService
from classifier.simple_classifier import classifier
from db import get_session
from library.models import LibraryItem


def print_divider(title=""):
    """Print a nice divider."""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"{'-'*80}\n")


def interactive_chat():
    """Run interactive chatbot conversation."""

    print_divider("RELAXBOT INTERACTIVE CONVERSATION")
    print("This demonstrates the complete flow:")
    print("1. Create session")
    print("2. Bot presents intro")
    print("3. You respond")
    print("4. Classifier analyzes your emotion")
    print("5. LLM generates personalized response")
    print("6. Continue through therapeutic states")
    print()

    # Step 1: Create session
    print("STEP 1: Creating session...")
    print("-" * 80)
    try:
        session = SessionService.create_session(
            patient_id="interactive_user",
            process_code="guided_imagery_v1"
        )
        session_id = session.id
        print(f"✓ Session created: {session_id}")
        print(f"  Patient: interactive_user")
        print(f"  Process: Guided Imagery - Therapeutic Visualization (6-state therapeutic flow)")
    except Exception as e:
        print(f"✗ Error creating session: {e}")
        return

    print_divider()

    # Initialize Session Manager
    session_manager = SessionManager(classifier_fn=classifier.classify)

    # Step 2: Bot sends first message (Step 1: Introduction)
    print("STEP 2: Bot sends first message...\n")

    try:
        # Get Step 1 introduction from library
        with get_session() as db:
            # Get all library items and filter by step=1
            all_items = db.query(LibraryItem).all()
            step1_intro = None
            for item in all_items:
                if item.item_metadata and item.item_metadata.get("step") == "1":
                    step1_intro = item
                    break

            if step1_intro:
                intro_text = step1_intro.body
            else:
                intro_text = "Hello, I'm RelaxBot, your therapeutic companion. How are you feeling right now?"

        print(f"Bot: {intro_text}\n")
        print(f"[Current State: Step 1: Introduction]")

    except Exception as e:
        print(f"✗ Error getting bot intro: {e}")
        import traceback
        traceback.print_exc()
        return

    print_divider()

    # Step 3: Start conversation loop
    print("STEP 3: Your turn - respond to the bot...\n")

    exchange = 1
    while True:
        print(f"\n{'='*80}")
        print(f"EXCHANGE {exchange} - Your Turn")
        print(f"{'='*80}\n")

        # Get user input
        user_message = input("You: ").strip()

        if not user_message:
            print("Please enter a message.")
            continue

        if user_message.lower() in ["exit", "quit", "bye"]:
            print("\nBot: Thank you for this session. Take care of yourself!")
            break

        print_divider()

        # Process the message through the full pipeline
        print("Processing your message...\n")

        try:
            # Step 1: Classify emotion
            classifier_output = classifier.classify(user_message)
            print(f"[Classifier]")
            print(f"  Intent: {classifier_output.intent}")
            print(f"  Emotion: {classifier_output.emotion}")
            print(f"  Confidence: {classifier_output.confidence:.0%}")

            # Step 2: Run through Session Manager (Orchestrator + RAG + LLM)
            print(f"\n[Orchestrator]")
            response = session_manager.process(
                SessionManagerRequest(
                    session_id=session_id,
                    message=user_message
                )
            )

            print(f"  Current State: {response.current_state.state_name}")
            print(f"  State Code: {response.current_state.state_code}")

            # Step 3: Show the response
            print(f"\n[LLM Generated Response]")
            print(f"\nBot: {response.llm_response}\n")

            # Show context (optional)
            if response.content:
                print(f"[Context Available]")
                print(f"  Available resources: {len(response.content)} items")
                for item in response.content[:2]:  # Show first 2
                    print(f"    - [{item.kind}] {item.title}")

            exchange += 1

        except Exception as e:
            print(f"✗ Error processing message: {e}")
            import traceback
            traceback.print_exc()

    print_divider()
    print(f"✓ Session ended: {session_id}")
    print(f"  Total exchanges: {exchange - 1}")


if __name__ == "__main__":
    try:
        interactive_chat()
    except KeyboardInterrupt:
        print("\n\nChat interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
