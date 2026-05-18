"""
scripts/add_therapy_states.py
Add therapy states from the therapy agent logic document.

Adds:
- STATE 2.1: GROUNDING (if anxious)
- STATE 2.2: REASSURANCE (if resistant)
- STATE 6: SAFE_PLACE_VISUALIZATION
- STATE 9: CLOSING
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from states.models import State
from processes.models import Process
from library.models import LibraryItem


THERAPY_STATES = {
    "2.1": {
        "code": "grounding",
        "name": "Step 2.1: Grounding (Anxiety Handler)",
        "description": "Stabilize user when anxious - 5 senses grounding"
    },
    "2.2": {
        "code": "reassurance",
        "name": "Step 2.2: Reassurance (Resistance Handler)",
        "description": "Provide reassurance when user is resistant"
    },
    "6": {
        "code": "guided_safe_place",
        "name": "Step 6: Safe Place Visualization",
        "description": "Visualization of safe, healing place"
    },
    "9": {
        "code": "guided_closing",
        "name": "Step 9: Closing",
        "description": "Close session and return to awareness"
    }
}

LIBRARY_CONTENT = {
    "2.1": {
        "title": "Step 2.1: Grounding (Anxiety Handler)",
        "base": "Let's slow things down... Look around you... notice one thing you can see... Now take a slow breath in... and out...",
        "responses": {
            "anxious": "You're safe. Let's ground ourselves together. Look around - what's one thing you can see right now? One thing you can hear? One thing you can feel? Good. Now let's breathe together.",
            "emotional": "I'm here with you. Let's take a moment to feel present. Notice your feet on the ground. Notice the space around you. You're safe right now.",
            "hesitant": "Sometimes slowing down helps. Just notice what's around you. There's no rush. This grounding helps your nervous system settle.",
            "uncertain": "Grounding helps when we're uncertain. Let's anchor to the present moment. What do you see? What do you feel?",
            "needs_reassurance": "You're completely safe right now. Let's ground ourselves. Feel your body in the chair. Feel your feet on the ground. You're here, you're safe.",
            "unwilling": "Sometimes this simple grounding can help shift things. Just notice your surroundings. No pressure. Just observing what's here.",
            "physically_uncomfortable": "Let's adjust and ground you. Notice where your body contacts the chair or floor. That grounding can help ease tension."
        }
    },
    "2.2": {
        "title": "Step 2.2: Reassurance (Resistance Handler)",
        "base": "You are okay. What you're feeling right now... it's uncomfortable, but it is not dangerous. Your body is reacting... and it will pass. You've gotten through moments like this before... and you can get through this one too.",
        "responses": {
            "resistant": "That's completely okay. You don't have to force anything. What you're feeling right now - it's uncomfortable, but it's not dangerous. Your body is just reacting. And it will pass. You've been through challenging moments before, and you can get through this too. You're safe, and I'm here with you.",
            "anxious": "I hear your anxiety. It's real, and it's okay. What you're feeling won't harm you. Your body is protecting itself, and that protective response will ease. You're safe right now.",
            "emotional": "It's okay to feel whatever you're feeling. These feelings are temporary. You have the strength to sit with this. I'm here with you.",
            "hesitant": "I appreciate you trying, even with doubt. Sometimes the most powerful thing is to try despite uncertainty. You might surprise yourself.",
            "uncertain": "It's okay to be unsure. You don't have to be certain to take the next step. Just try one small thing with me.",
            "unwilling": "I respect that this doesn't feel right for you right now. And you don't have to. But maybe we could try just one small step together? No commitment beyond that.",
            "needs_reassurance": "You're completely safe with me. I'm not here to force anything on you. You're in control. We can go at your pace, and you can stop anytime."
        }
    },
    "6": {
        "title": "Step 6: Safe Place Visualization",
        "base": "Now shift your attention to your inner world, the world where your memories, dreams, feelings, plans reside. Visualize a beautiful place where you feel safe, comfortable, and relaxed. Take some time to explore this place, notice what you see there, any sounds you hear. Notice if there is any fragrance, or special quality of air. Notice what time of the day it is, what is the temperature. If your mind wanders, just take another breath or two and gently return your attention to this beautiful and healing place.",
        "responses": {
            "comfortable": "Beautiful. Your safe place is becoming clearer. Explore it. Feel the peace. What do you see? What sounds surround you? This is your healing sanctuary. Enjoy this moment of peace.",
            "emotional": "Imagine your perfect safe place. A place where all worry melts away. What is it? A beach? A forest? Mountains? A quiet room? Let it form naturally. You're safe here. Feel the peace.",
            "hesitant": "Your safe place doesn't need to be perfect or crystal clear. Just the feeling of it matters. Safety. Comfort. Relaxation. What comes to mind? Go with it.",
            "uncertain": "Trust your imagination. Your safe place is forming. It's uniquely yours. What does it feel like? Look around. You're beginning to heal here.",
            "needs_reassurance": "This is your safe place. Completely under your control. You create it. What would make you feel safe? Build that here. I'm with you.",
            "unwilling": "Imagine somewhere that feels good to you. Even a memory of a comfortable moment. That's your safe place. Feel the peace there.",
            "physically_uncomfortable": "Your safe place can ease physical discomfort. Imagine perfect temperature, comfortable support, gentle surroundings. What feels healing to your body?"
        }
    },
    "9": {
        "title": "Step 9: Closing",
        "base": "Slowly bring your attention back... Take one deep breath... When you're ready... gently open your eyes... You did well today.",
        "responses": {
            "comfortable": "Slowly... bring your awareness back to the room. Notice your body. Take one more deep breath. When you're ready... gently open your eyes. You did beautiful work today. Well done.",
            "emotional": "You showed courage today. Slowly come back. Bring your awareness to your body. To the room around you. When ready, gently open your eyes. You did well. That took strength.",
            "hesitant": "You gave this a genuine try. That matters. Slowly come back. Gently open your eyes when ready. You showed up for yourself today.",
            "uncertain": "You took the step. That's what matters. Slowly return. Gently bring your awareness back. Open your eyes when you're ready. You did it.",
            "needs_reassurance": "You're safe. You made it through. You did wonderfully. Slowly return. Gently open your eyes. You're okay. You're safe.",
            "unwilling": "Thank you for trying. Even in resistance, you found moments of peace. That matters. Gently return. Open your eyes. You're welcome back anytime.",
            "physically_uncomfortable": "Your body showed up today. You honored its needs. That's wisdom. Slowly return. Gently open your eyes. You're doing okay."
        }
    }
}


def add_therapy_states():
    """Add therapy states from logic document."""

    with get_session() as db:
        print("=" * 80)
        print("ADDING THERAPY HANDLER STATES")
        print("=" * 80)

        # Get existing process
        process = db.query(Process).filter(Process.code == "guided_imagery_v2").first()
        if not process:
            print("ERROR: Process 'guided_imagery_v2' not found!")
            return

        # Create new states
        print("\n[1] Creating new states...")
        new_states = {}
        for step, info in THERAPY_STATES.items():
            state = State(
                id=uuid.uuid4(),
                code=info["code"],
                name=info["name"],
                description=info["description"]
            )
            new_states[step] = state
            db.add(state)
            print(f"  ✓ {info['name']}")

        db.flush()

        # Update process definition with new transitions
        print("\n[2] Updating process transitions...")
        definition = process.definition

        # Get the state ID for CHECK_USER_READINESS (should be in existing states)
        existing_states = db.query(State).all()
        state_map = {state.code: str(state.id) for state in existing_states}
        state_map.update({f"step_{step}": str(new_states[step].id)
                         for step in new_states})

        # Add new state transitions
        # STATE 2 (check_readiness) → 2.1 (grounding) if anxious, 2.2 (reassurance) if resistant
        check_readiness_state = [s for s in existing_states if "check" in s.code.lower() or s.name == "Step 2: Check User Readiness"]
        breathing_state = [s for s in existing_states if "breathing" in s.code.lower()]

        if check_readiness_state and breathing_state:
            check_id = str(check_readiness_state[0].id)
            breathing_id = str(breathing_state[0].id)

            # Update CHECK_READINESS transitions
            definition["states"][check_id] = {
                "transitions": [
                    {"condition": "emotion in ['calm', 'comfortable']", "target": breathing_id},
                    {"condition": "emotion == 'anxious'", "target": str(new_states["2.1"].id)},
                    {"condition": "emotion == 'resistant'", "target": str(new_states["2.2"].id)},
                ]
            }

            # Add GROUNDING (2.1) → back to BREATHING
            definition["states"][str(new_states["2.1"].id)] = {
                "transitions": [
                    {"condition": "emotion in ['calm', 'comfortable', 'anxious']", "target": breathing_id}
                ]
            }

            # Add REASSURANCE (2.2) → back to CHECK_READINESS
            definition["states"][str(new_states["2.2"].id)] = {
                "transitions": [
                    {"condition": "emotion in ['calm', 'comfortable', 'resistant']", "target": check_id}
                ]
            }

        # Add SAFE_PLACE state (Step 6)
        safe_place_id = str(new_states["6"].id)
        imagery_state = [s for s in existing_states if "imagery" in s.code.lower()]
        closing_id = str(new_states["9"].id)

        if imagery_state:
            imagery_id = str(imagery_state[0].id)
            # Update IMAGERY (Step 5) → SAFE_PLACE (Step 6)
            definition["states"][imagery_id]["transitions"] = [
                {"condition": "emotion in ['calm', 'comfortable']", "target": safe_place_id}
            ]

            # Add SAFE_PLACE (Step 6) → CLOSING (Step 9)
            definition["states"][safe_place_id] = {
                "transitions": [
                    {"condition": "emotion in ['calm', 'comfortable', 'anxious', 'emotional', 'hesitant', 'uncertain', 'resistant', 'needs_reassurance', 'unwilling', 'physically_uncomfortable']",
                     "target": closing_id}
                ]
            }

        # Add CLOSING state (Step 9)
        definition["states"][closing_id] = {
            "transitions": []  # Final state
        }

        # Update end states
        if closing_id not in definition.get("end_states", []):
            definition["end_states"].append(closing_id)

        process.definition = definition
        db.flush()
        print(f"  ✓ Updated transition flows")

        # Create library items
        print("\n[3] Creating library content...")
        lib_items = []

        for step in ["2.1", "2.2", "6", "9"]:
            content = LIBRARY_CONTENT[step]
            state_code = THERAPY_STATES[step]["code"]

            # Base script
            base_item = LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title=content["title"],
                body=content["base"],
                item_metadata={
                    "step": step,
                    "state_code": state_code,
                    "type": "base_script",
                    "emotional_state": "universal"
                }
            )
            lib_items.append(base_item)

            # Emotional responses
            for emotion, response in content["responses"].items():
                response_item = LibraryItem(
                    id=uuid.uuid4(),
                    kind="response",
                    title=f"{content['title']} - {emotion}",
                    body=response,
                    item_metadata={
                        "step": step,
                        "state_code": state_code,
                        "type": "emotional_response",
                        "emotional_state": emotion
                    }
                )
                lib_items.append(response_item)

        db.add_all(lib_items)
        print(f"  ✓ Created {len(lib_items)} library items")

        # Commit
        db.commit()

        print("\n" + "=" * 80)
        print("SUCCESS! THERAPY STATES ADDED")
        print("=" * 80)
        print(f"\nNew States: 4")
        print(f"  - Step 2.1: Grounding (Anxiety Handler)")
        print(f"  - Step 2.2: Reassurance (Resistance Handler)")
        print(f"  - Step 6: Safe Place Visualization")
        print(f"  - Step 9: Closing")
        print(f"\nLibrary Items: {len(lib_items)}")
        print(f"\nNew State Flow:")
        print(f"  Step 1 → Step 2 →")
        print(f"    ├ (anxious) → Step 2.1: Grounding → Step 3")
        print(f"    ├ (resistant) → Step 2.2: Reassurance → Step 2")
        print(f"    └ (calm) → Step 3")
        print(f"  Step 3 → Step 4 → Step 5 → Step 6 → Step 9")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        add_therapy_states()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
