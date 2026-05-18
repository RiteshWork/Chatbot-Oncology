"""
scripts/create_sample_data.py
Create sample data for the complete 7-state Calm flow.

Flow: Intro → Classify → Breathing → Observation → Countdown → Guided Imagery → Close

This creates the database templates that will be used for all sessions.
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from states.models import State
from processes.models import Process
from library.models import LibraryItem


def create_sample_data():
    """Create all sample data for the Calm flow."""

    with get_session() as db:
        print("=" * 80)
        print("CREATING CALM FLOW PROCESS TEMPLATE (7 STATES)")
        print("=" * 80)

        # Create States for Guided Imagery Flow (Steps 1-5, 7)
        print("\n[1] Creating States...")

        state_intro = State(
            id=uuid.uuid4(),
            code="guided_intro",
            name="Step 1: Introduction",
            description="Introduction to Guided Imagery VR experience"
        )

        state_breathing = State(
            id=uuid.uuid4(),
            code="guided_breathing",
            name="Step 2: Deep Breathing",
            description="Deep breathing to relax body and mind"
        )

        state_observation = State(
            id=uuid.uuid4(),
            code="guided_observation",
            name="Step 3: Observe Your Breath",
            description="Natural breathing with So/In and Hum/Out technique"
        )

        state_countdown = State(
            id=uuid.uuid4(),
            code="guided_countdown",
            name="Step 4: Countdown",
            description="Countdown visualization from 10 to 1"
        )

        state_imagery = State(
            id=uuid.uuid4(),
            code="guided_imagery",
            name="Step 5: Inner World - Safe Place",
            description="Visualization of safe, healing place"
        )

        state_hindsight = State(
            id=uuid.uuid4(),
            code="guided_hindsight",
            name="Step 7: Hindsight & Closing",
            description="Recollect experience and return to awareness"
        )

        states = [state_intro, state_breathing, state_observation,
                  state_countdown, state_imagery, state_hindsight]
        db.add_all(states)
        db.flush()

        for state in states:
            print(f"  Created state: {state.name}")

        # Create Process Definition with all transitions
        print("\n[2] Creating Process Definition...")

        process_definition = {
            "initial_state": str(state_intro.id),
            "states": {
                # Step 1: Intro → Step 2: Breathing (when patient is calm)
                str(state_intro.id): {
                    "transitions": [
                        {"condition": "emotion == 'calm'", "target": str(state_breathing.id)}
                    ]
                },
                # Step 2: Breathing → Step 3: Observation (when patient is calm)
                # If anxious, stays in breathing for more support
                str(state_breathing.id): {
                    "transitions": [
                        {"condition": "emotion == 'calm'", "target": str(state_observation.id)}
                    ]
                },
                # Step 3: Observation → Step 4: Countdown (when patient is calm)
                # If anxious, stays in observation for more support
                str(state_observation.id): {
                    "transitions": [
                        {"condition": "emotion == 'calm'", "target": str(state_countdown.id)}
                    ]
                },
                # Step 4: Countdown → Step 5: Imagery (when patient is calm)
                # If anxious, stays in countdown for more support
                str(state_countdown.id): {
                    "transitions": [
                        {"condition": "emotion == 'calm'", "target": str(state_imagery.id)}
                    ]
                },
                # Step 5: Imagery → Step 7: Hindsight (when patient is calm)
                # If anxious, stays in imagery for more healing time
                str(state_imagery.id): {
                    "transitions": [
                        {"condition": "emotion == 'calm'", "target": str(state_hindsight.id)}
                    ]
                },
                # Step 7: Hindsight is the end state
                str(state_hindsight.id): {
                    "transitions": []
                }
            },
            "end_states": [str(state_hindsight.id)]
        }

        process = Process(
            id=uuid.uuid4(),
            code="guided_imagery_v1",
            name="Guided Imagery - Therapeutic Visualization",
            description="6-step guided imagery session: Intro → Breathing → Observation → Countdown → Safe Place → Hindsight",
            definition=process_definition,
            is_active=True
        )

        process.validate_definition()
        db.add(process)
        db.flush()

        print(f"  Created process: {process.name}")
        print(f"    Flow: Intro → Breathing → Observation → Countdown → Safe Place → Hindsight")

        # Create Library Items (scripts for each state)
        print("\n[3] Creating Library Items...")

        lib_items = [
            LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title="Step 1: Introduction",
                body="Hello, I'm RelaxBot, your therapeutic companion. I'm here to help you find moments of peace and relaxation through guided imagery. Before we begin this therapeutic journey, I'd like to understand your current state. How are you feeling right now?",
                item_metadata={"step": "1", "state": "intro"}
            ),
            LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title="Step 2: Deep Breathing",
                body="Be in a comfortable position with your eyes closed. As per your capacity let your breathing get a little deeper and fuller. With every breath in, notice that you bring in fresh air, fresh oxygen and fresh energy to your body. And with every breath out, imagine that you can release a bit of tension, discomfort and worry. Allowing your body and mind to relax fully. Repeat this inhalation and exhalation 4 more times allowing body and mind to relax. Inhale... Exhale... Inhale... Exhale... Continue.",
                item_metadata={"step": "2", "state": "breathing", "technique": "deep_breathing"}
            ),
            LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title="Step 3: Observe Your Breath",
                body="Now become aware of your breathing and let your body inhale and exhale naturally. As you inhale, mentally say 'In or So (for Hindus)' and while you exhale, mentally say 'Out or Hum (for Hindus)'. Repeat this for 5 minutes. Inhale... So or In... Exhale... Hum or Out... Continue at your own pace.",
                item_metadata={"step": "3", "state": "observation", "technique": "so_hum"}
            ),
            LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title="Step 4: Countdown",
                body="Now visualize numbers on a screen counting down from 10 to 1. With each count down go into deeper and calmer state. 10... 9... 8... 7... 6... 5... 4... 3... 2... 1. With each number, feel yourself descending into a more profound state of relaxation and inner peace.",
                item_metadata={"step": "4", "state": "countdown"}
            ),
            LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title="Step 5: Inner World and Safe Place",
                body="Now shift your attention to your inner world, the world where your memories, dreams, feelings, plans reside. Visualize a beautiful place where you feel safe, comfortable, and relaxed. Take some time to explore this place, notice what you see there, any sounds you hear. Notice if there is any fragrance, or special quality of air. Notice what time of the day it is, what is the temperature. If your mind wanders, just take another breath or two and gently return your attention to this beautiful and healing place. Allow yourself to become aware of anything in this place that feels like it will heal you. Experience whatever healing is there for you and relax. Know that while you relax, your body's natural healing systems operate at their highest efficiency.",
                item_metadata={"step": "5", "state": "imagery", "technique": "safe_place_visualization"}
            ),
            LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title="Step 7: Hindsight & Closing",
                body="Try to recollect your experience and how the session has been therapeutic, with profound healing effect. Feel the peace within and be happy for this very moment. Give yourself a mental pat on the back for participating in your recovery. See yourself doing this mental imagery exercise three times a day. Associate yourself with an image that represents your strength, bravery, and courage. Whenever you feel the need to reconnect with yourself breathe deeply, relax, and think of this image. With a few gentle blinks, gently move your eyes and become aware of your surroundings.",
                item_metadata={"step": "7", "state": "hindsight", "type": "closing_affirmation"}
            ),
        ]

        db.add_all(lib_items)
        print(f"  Created {len(lib_items)} library items")

        # Commit all changes
        db.commit()

        print("\n" + "=" * 80)
        print("SUCCESS! CALM FLOW PROCESS CREATED")
        print("=" * 80)
        print(f"States: 7")
        print(f"Process: 1 (calm_v1)")
        print(f"Library Items: {len(lib_items)}")
        print("\nThis is the PROCESS TEMPLATE. Sessions will be created at runtime.")
        print("=" * 80)


if __name__ == "__main__":
    create_sample_data()
