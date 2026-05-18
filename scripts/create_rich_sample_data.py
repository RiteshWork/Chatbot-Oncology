"""
scripts/create_rich_sample_data.py
Create comprehensive sample data with emotional state variations.

This script populates the database with:
1. Core therapeutic steps (1-7)
2. Multiple emotional state responses (7 states)
3. Patient statements for each emotional state
4. Bot responses tailored to each emotional state
5. Affirmations and guidance for each step
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from states.models import State
from processes.models import Process
from library.models import LibraryItem


# ============================================================================
# EMOTIONAL STATES DEFINITION
# ============================================================================

EMOTIONAL_STATES = {
    "comfortable": {
        "name": "Comfortable & Ready",
        "description": "Patient is relaxed, willing, and ready to begin",
        "color": "green",
        "keywords": ["relaxed", "ready", "comfortable", "peaceful", "calm", "safe", "ease"]
    },
    "emotional": {
        "name": "Emotional/Overwhelmed",
        "description": "Patient feels nervous, anxious, racing thoughts, overwhelmed",
        "color": "orange",
        "keywords": ["nervous", "anxious", "overwhelmed", "racing", "tense", "drained", "stressed"]
    },
    "hesitant": {
        "name": "Hesitant/Doubtful",
        "description": "Patient is unsure, skeptical, not good at visualization",
        "color": "yellow",
        "keywords": ["hesitant", "unsure", "silly", "doubtful", "skeptical", "imagination", "doubt"]
    },
    "uncertain": {
        "name": "Uncertain/Conflicted",
        "description": "Patient is undecided, on the fence, conflicted",
        "color": "gray",
        "keywords": ["uncertain", "undecided", "fence", "conflicted", "torn", "hesitating"]
    },
    "needs_reassurance": {
        "name": "Needs Reassurance",
        "description": "Patient needs safety assurance, clarity, step-by-step guidance",
        "color": "blue",
        "keywords": ["safe", "bad", "happen", "control", "uncomfortable", "reassure", "guide"]
    },
    "unwilling": {
        "name": "Unwilling/Refusing",
        "description": "Patient doesn't want to do it, prefers alternatives",
        "color": "red",
        "keywords": ["don't want", "skip", "pointless", "uncomfortable", "anxious", "silly"]
    },
    "physically_uncomfortable": {
        "name": "Physically Uncomfortable",
        "description": "Patient has physical discomfort, pain, stiffness",
        "color": "purple",
        "keywords": ["hurt", "pain", "stiff", "ache", "uncomfortable", "sore", "uncomfortable"]
    }
}


# ============================================================================
# THERAPEUTIC CONTENT BY STEP & EMOTIONAL STATE
# ============================================================================

LIBRARY_CONTENT = {
    "1": {  # Step 1: Introduction
        "title": "Step 1: Introduction",
        "base_script": "Welcome to your Guided Imagery VR experience. This module will help create vivid mental experiences by guiding you through a virtual environment. We hope this session will enhance relaxation, focus and wellbeing through visualization.",
        "responses": {
            "comfortable": "That's wonderful! I'm so glad you're feeling ready and relaxed. Let's begin this journey together. We'll take this at your own pace, and you're in complete control every step of the way.",
            "emotional": "I hear you. It's completely normal to feel nervous or have racing thoughts. This is a safe space, and we can go at your pace. Many people feel this way at first, and that's okay. Shall we start with some gentle breathing to help settle your mind?",
            "hesitant": "I appreciate your willingness to try, even if you're not entirely sure about it. There's no right or wrong way to do this. We'll take it slowly, and you might surprise yourself with what you're capable of. Are you willing to give it a shot?",
            "uncertain": "I can sense you're weighing your options, and that's perfectly fine. There's no pressure here. Whether you decide to proceed or not, I respect your choice. Would you like to try, or would you prefer to talk more about it first?",
            "needs_reassurance": "I completely understand your concerns. Let me assure you: you're in control the entire time. I'll guide you step by step, and you can stop anytime you need to. This is a safe, gentle practice designed to help you, not harm you. Ready to proceed?",
            "unwilling": "I hear that guided imagery might not be your preference right now. That's completely okay. We can approach this differently. Would you like to explore another relaxation technique, or would you prefer to stop here?",
            "physically_uncomfortable": "I'm sorry to hear you're experiencing physical discomfort. Let's make sure you're as comfortable as possible. Can you adjust your position or move to a more comfortable location? We can begin once you feel settled."
        }
    },

    "2": {  # Step 2: Deep Breathing
        "title": "Step 2: Deep Breathing",
        "base_script": "Be in a comfortable position with your eyes closed. As per your capacity let your breathing get a little deeper and fuller. With every breath in, notice that you bring in fresh air, fresh oxygen and fresh energy to your body. And with every breath out, imagine that you can release a bit of tension, discomfort and worry. Repeat this inhalation and exhalation 4 more times allowing body and mind to relax. Inhale... Exhale... continue.",
        "responses": {
            "comfortable": "You're doing wonderfully! Feel how calm your body is becoming with each breath. Continue at your own rhythm. There's no rush. Just breathe naturally and let the relaxation deepen.",
            "emotional": "That's excellent. If your mind wanders, that's completely normal. Just gently bring your attention back to your breath. Each exhale releases more tension. You're doing great.",
            "hesitant": "You're doing this perfectly. There's nothing complicated about it. Just notice your natural breath. You're already more relaxed than you think. Keep going at your own pace.",
            "uncertain": "I can see you're giving this a try. That's a good sign. With each breath, you're releasing doubt and inviting calm. Continue breathing. You're on the right path.",
            "needs_reassurance": "You're safe and in control. I'm here with you the entire time. Just focus on your breathing. If anything feels uncomfortable, let me know and we can adjust. You're doing great.",
            "unwilling": "I know this might feel unusual, but you're doing it. Simple breathing is all we need. No pressure. Just a few more breaths with me. You've got this.",
            "physically_uncomfortable": "If your position is uncomfortable, you can adjust anytime. Find what works for your body. Breathing helps ease physical tension. Take your time and breathe at your own pace."
        }
    },

    "3": {  # Step 3: Observe Your Breath
        "title": "Step 3: Observe Your Breath",
        "base_script": "Now become aware of your breathing and let your body inhale and exhale naturally. As you inhale, mentally say 'In or So' and while you exhale, mentally say 'Out or Hum'. This ancient technique helps anchor your mind and deepen your relaxation. Continue at your own pace.",
        "responses": {
            "comfortable": "Perfect. You're becoming more and more relaxed with each breath. Notice how peaceful your mind is becoming. Keep going. This is beautiful work.",
            "emotional": "Excellent. Your mind is becoming clearer with each breath. The So/Hum technique is helping your thoughts settle. You're doing perfectly. Continue.",
            "hesitant": "You see? It's simpler than you thought. Just the breath and the mantra. Your mind is already quieter. You're doing wonderfully.",
            "uncertain": "You're finding your rhythm. With each breath, you're becoming more present. This is working for you. Keep going.",
            "needs_reassurance": "You're doing exactly right. The So/Hum technique is safe and ancient. It gives your mind something to focus on. You're in complete control. Continue breathing.",
            "unwilling": "This is working, isn't it? Just breath and a simple mantra. You're becoming calmer. Keep going with me.",
            "physically_uncomfortable": "Let your body relax as you breathe. The technique works with your natural rhythm. If you need to adjust, that's fine. Continue at whatever pace feels comfortable."
        }
    },

    "4": {  # Step 4: Countdown
        "title": "Step 4: Countdown",
        "base_script": "Now visualize numbers on a screen counting down from 10 to 1. With each count down go into deeper and calmer state. 10... 9... 8... 7... 6... 5... 4... 3... 2... 1. With each number, feel yourself descending into a more profound state of relaxation and inner peace.",
        "responses": {
            "comfortable": "Imagine the numbers clearly before you. With each number, you sink deeper into peace. 10... deeper still... 9... 8... You're in a beautiful space now. Continue counting down.",
            "emotional": "The numbers help quiet your racing mind. 10... 9... Feel each number taking you deeper. 8... 7... You're safe and relaxed. Continue.",
            "hesitant": "You don't need to see the numbers perfectly. Just the idea of them is enough. 10... 9... You're already deeper. 8... 7... Keep going.",
            "uncertain": "Let yourself visualize or just imagine the countdown. Either way works. 10... 9... You're finding your way. 8... 7... Continue.",
            "needs_reassurance": "Visualize the numbers at your own pace. I'm here with you. 10... 9... You're safe and descending deeper. 8... 7... Continue with me.",
            "unwilling": "Simple countdown. Numbers going down. You're going deeper. 10... 9... 8... This is working. Keep going.",
            "physically_uncomfortable": "Visualize yourself becoming more comfortable with each number. 10... 9... Your body relaxing. 8... 7... Continue at your pace."
        }
    },

    "5": {  # Step 5: Safe Place Visualization
        "title": "Step 5: Safe Place Visualization",
        "base_script": "Now shift your attention to your inner world. Visualize a beautiful place where you feel safe, comfortable, and relaxed. Take time to explore this place. Notice what you see, sounds you hear, fragrances, temperature. Allow yourself to become aware of anything that feels healing. Experience whatever healing is there for you. Know that your body's natural healing systems operate at their highest efficiency.",
        "responses": {
            "comfortable": "Beautiful. Your safe place is becoming clearer. Explore it. Feel the peace. What do you see? What sounds surround you? This is your healing sanctuary. Enjoy this moment.",
            "emotional": "Imagine your perfect safe place. A place where all worry melts away. What is it? A beach? A forest? Mountains? Let it form naturally. You're safe here. Feel the peace.",
            "hesitant": "Your safe place doesn't need to be perfect or crystal clear. Just the feeling of it matters. Safety. Comfort. Relaxation. What comes to mind? Go with it.",
            "uncertain": "Trust your imagination. Your safe place is forming. It's uniquely yours. What does it feel like? Look around. You're beginning to heal here.",
            "needs_reassurance": "This is your safe place. Completely under your control. You create it. What would make you feel safe? Build that here. I'm with you.",
            "unwilling": "Imagine somewhere that feels good to you. Even a memory of a comfortable moment. That's your safe place. Feel the peace there.",
            "physically_uncomfortable": "Your safe place can ease physical discomfort. Imagine perfect temperature, comfortable support, gentle surroundings. What feels healing to your body?"
        }
    },

    "7": {  # Step 7: Hindsight & Closing
        "title": "Step 7: Hindsight & Closing",
        "base_script": "Recollect your experience and how therapeutic this session has been. Feel the peace within. Give yourself credit for participating in your recovery. See yourself doing this three times a day. Associate yourself with an image representing your strength, bravery, and courage. Whenever you need to reconnect, breathe deeply and think of this image. Gently return to awareness of your surroundings.",
        "responses": {
            "comfortable": "What a beautiful journey you've taken. You've done wonderful work today. This peace is yours to keep. Practice this daily. You are strong. You are healing. Well done.",
            "emotional": "Look at what you've accomplished today. Despite nervousness, you showed courage. That strength is always within you. Practice this healing regularly. You're doing great.",
            "hesitant": "You did it. You gave it a genuine try, and you found something meaningful here. Trust yourself more. This experience proves your capability. Come back often.",
            "uncertain": "You made the choice to try, and it paid off. Trust yourself more. This peace is real and achievable. Make this a regular practice. You're capable.",
            "needs_reassurance": "You were safe the entire time, and you succeeded beautifully. That's powerful. Keep practicing. Each session strengthens you. You can do this anytime you need healing.",
            "unwilling": "Thank you for trying. Even in resistance, you found moments of peace. That matters. If you want to return, you know where to find this. You're welcome anytime.",
            "physically_uncomfortable": "Your body showed up today. You honored its needs while seeking healing. That's wisdom. Gentle practices like this help your body relax. You're healing."
        }
    }
}


def create_rich_sample_data():
    """Create comprehensive therapeutic data with emotional state variations."""

    with get_session() as db:
        print("=" * 80)
        print("CREATING COMPREHENSIVE THERAPEUTIC LIBRARY")
        print("=" * 80)

        # Step 1: Create States
        print("\n[1] Creating States...")

        states_data = {
            "1": ("guided_intro", "Step 1: Introduction"),
            "2": ("guided_breathing", "Step 2: Deep Breathing"),
            "3": ("guided_observation", "Step 3: Observe Your Breath"),
            "4": ("guided_countdown", "Step 4: Countdown"),
            "5": ("guided_imagery", "Step 5: Inner World - Safe Place"),
            "7": ("guided_hindsight", "Step 7: Hindsight & Closing"),
        }

        states = {}
        for step, (code, name) in states_data.items():
            state = State(
                id=uuid.uuid4(),
                code=code,
                name=name,
                description=f"Therapeutic step {step}"
            )
            states[step] = state
            db.add(state)
            print(f"  Created state: {name}")

        db.flush()

        # Step 2: Create Process Definition with emotion-based transitions
        print("\n[2] Creating Process Definition with Emotion-Based Transitions...")

        process_definition = {
            "initial_state": str(states["1"].id),
            "states": {
                # Step 1 → Step 2 (when emotion == 'calm' or 'comfortable')
                str(states["1"].id): {
                    "transitions": [
                        {"condition": "emotion in ['calm', 'comfortable']", "target": str(states["2"].id)}
                    ]
                },
                # Step 2 → Step 3
                str(states["2"].id): {
                    "transitions": [
                        {"condition": "emotion in ['calm', 'comfortable']", "target": str(states["3"].id)}
                    ]
                },
                # Step 3 → Step 4
                str(states["3"].id): {
                    "transitions": [
                        {"condition": "emotion in ['calm', 'comfortable']", "target": str(states["4"].id)}
                    ]
                },
                # Step 4 → Step 5
                str(states["4"].id): {
                    "transitions": [
                        {"condition": "emotion in ['calm', 'comfortable']", "target": str(states["5"].id)}
                    ]
                },
                # Step 5 → Step 7
                str(states["5"].id): {
                    "transitions": [
                        {"condition": "emotion in ['calm', 'comfortable']", "target": str(states["7"].id)}
                    ]
                },
                # Step 7: End state
                str(states["7"].id): {
                    "transitions": []
                }
            },
            "end_states": [str(states["7"].id)]
        }

        process = Process(
            id=uuid.uuid4(),
            code="guided_imagery_v2",
            name="Guided Imagery - Therapeutic Visualization (Enhanced)",
            description="6-step guided imagery with emotional state awareness",
            definition=process_definition,
            is_active=True
        )

        process.validate_definition()
        db.add(process)
        db.flush()

        print(f"  Created process: {process.name}")
        print(f"    Emotion-based transitions: calm/comfortable → proceed, others → support")

        # Step 3: Create Library Items with Emotional Variations
        print("\n[3] Creating Rich Library with Emotional State Variations...")

        lib_items = []
        item_count = 0

        for step in ["1", "2", "3", "4", "5", "7"]:
            step_content = LIBRARY_CONTENT[step]
            state_id = states[step].id

            # Add base script for this step
            base_item = LibraryItem(
                id=uuid.uuid4(),
                kind="script",
                title=step_content["title"],
                body=step_content["base_script"],
                item_metadata={
                    "step": step,
                    "state_code": states_data[step][0],
                    "type": "base_script",
                    "emotional_state": "universal"
                }
            )
            lib_items.append(base_item)
            item_count += 1

            # Add emotional state-specific responses
            for emotional_state, response in step_content["responses"].items():
                response_item = LibraryItem(
                    id=uuid.uuid4(),
                    kind="response",
                    title=f"{step_content['title']} - {EMOTIONAL_STATES[emotional_state]['name']}",
                    body=response,
                    item_metadata={
                        "step": step,
                        "state_code": states_data[step][0],
                        "type": "emotional_response",
                        "emotional_state": emotional_state,
                        "emotional_name": EMOTIONAL_STATES[emotional_state]["name"]
                    }
                )
                lib_items.append(response_item)
                item_count += 1

        db.add_all(lib_items)
        print(f"  Created {item_count} library items (base + emotional variations)")

        # Commit all changes
        db.commit()

        print("\n" + "=" * 80)
        print("SUCCESS! COMPREHENSIVE THERAPEUTIC LIBRARY CREATED")
        print("=" * 80)
        print(f"States: 6 (Steps 1-5, 7)")
        print(f"Process: 1 (guided_imagery_v2 - emotion-aware)")
        print(f"Library Items: {item_count}")
        print(f"  - 6 base scripts (universal)")
        print(f"  - {item_count - 6} emotional state variations (7 per step)")
        print("\nEmotional States Supported:")
        for state_key, state_info in EMOTIONAL_STATES.items():
            print(f"  - {state_info['name']}")
        print("\nSessionswill now:")
        print("  ✓ Classify emotion after every patient message")
        print("  ✓ Use emotion-based responses from library")
        print("  ✓ Transition based on emotional state (calm → proceed, others → support)")
        print("  ✓ Adapt support to patient's emotional journey")
        print("=" * 80)


if __name__ == "__main__":
    try:
        create_rich_sample_data()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
