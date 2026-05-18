"""
scripts/add_physically_uncomfortable_content.py
Load Physically Uncomfortable therapeutic content into database

This script extracts content from the uploaded DOCX and structures it
as library items with proper metadata for RAG retrieval and LLM synthesis.
"""

import sys
import os
import uuid
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from library.models import LibraryItem

# ============================================================================
# PHYSICALLY UNCOMFORTABLE CONTENT
# Extracted and structured from: Physically uncomfortable Version2 (Ado).docx
# ============================================================================

PHYSICALLY_UNCOMFORTABLE_LIBRARY = {
    # ========== INTRODUCTION ==========
    "intro_check": {
        "kind": "script",
        "title": "Step 1: Introduction - Physically Uncomfortable Check-In",
        "body": """Welcome to your Guided Imagery experience.

Guided imagery is a gentle relaxation technique that uses your imagination to help your mind and body feel calmer and more at ease. There's no right or wrong way to experience it—just allow yourself to follow along in a way that feels comfortable for you.

You may begin to notice a sense of relaxation, clarity, or calm as we continue.

Before we start, I just want to check—are you feeling comfortable right now? If you need to adjust your position or have any questions, please feel free to tell me.""",
        "metadata": {
            "step": "1",
            "state_code": "introduction",
            "emotional_state": "physically_uncomfortable",
            "type": "base_script",
            "severity": "all"
        }
    },

    # ========== OPENING SCRIPTS BY INTENSITY ==========
    "mild_opening": {
        "kind": "script",
        "title": "Opening Script - Mild Physical Discomfort",
        "body": """I know there's a little discomfort—we'll keep this gentle.
Just notice your breath as it is… no need to change anything.
In… and out… comfortably.
If you need to adjust your position, that's okay.
Let's take this one easy breath at a time.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "opening_script"
        }
    },

    "moderate_opening": {
        "kind": "script",
        "title": "Opening Script - Moderate Physical Discomfort",
        "body": """Hi, I know the discomfort is a bit more noticeable—we'll go gently.
Just notice your breath as it is… no need to change it.
In… and out… slowly.
If the discomfort pulls your attention, that's okay—just come back to your breath or notice the support beneath you.
We'll take this one breath at a time.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "moderate",
            "type": "opening_script"
        }
    },

    "severe_opening": {
        "kind": "script",
        "title": "Opening Script - Severe Physical Discomfort",
        "body": """Hi, I know the discomfort is quite strong right now. We'll keep this very simple, and you're in control—you can pause anytime.
Just notice your breath as it is… even a small breath is enough.
If that's hard, feel the support of the bed or chair holding you.
You're safe, and I'm right here with you.
Let's just take this one breath at a time.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "severe",
            "type": "opening_script"
        }
    },

    # ========== BREATHING EXERCISES - MILD DISCOMFORT ==========
    "mild_belly_breathing": {
        "kind": "breathing_exercise",
        "title": "Deep Belly Breathing - Mild Physical Discomfort",
        "body": """Therapist: Before we begin, just settle into a position that feels comfortable for you. You don't need to force anything. Are you feeling okay to start?

Client: Yeah, I think so.

Therapist: Good. Today we'll do a simple deep belly breathing exercise. The goal isn't to breathe perfectly — just to gently notice and slow the breath. You can place one hand on your chest and the other on your belly if that feels comfortable.

Client: Okay.

Therapist: As you breathe in through your nose, see if you can let the belly rise slightly, almost like filling a balloon. And as you breathe out slowly through your mouth, let the belly soften and fall.

Client: Alright.

Therapist: Let's try one together. Slow inhale… 1… 2… 3… 4… And a gentle exhale… 1… 2… 3… 4… 5… 6…

Client: I can feel my stomach moving a little.

Therapist: That's good. There's no need to make the breath very deep or forceful. Just comfortable and natural. Again, breathing in slowly through the nose… letting the belly expand… And breathing out slowly… releasing tension from the shoulders and jaw.

Client: My breathing feels a bit slower now.

Therapist: Nice. Just continue at that pace. With each exhale, imagine your body softening a little more. If your mind wanders, that's completely okay — simply guide your attention back to the feeling of the breath.

Client: Okay, I'll try.

Therapist: You're doing well. Take another slow breath in… And a longer, relaxed breath out. Notice the support beneath you. Notice the gentle rise and fall of your belly. Nothing else you need to do right now except breathe.

Client: I feel a little calmer.

Therapist: I'm glad to hear that. Let's take two more slow breaths together. Inhale gently… And exhale slowly… One more time… Breathing in… And breathing out… letting the body relax.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "breathing_exercise",
            "technique": "deep_belly_breathing"
        }
    },

    "mild_4_4_breathing": {
        "kind": "breathing_exercise",
        "title": "4-4 Breathing - Mild Physical Discomfort",
        "body": """Therapist: Before we begin, just try to sit in a position that feels as comfortable as possible. You don't have to force anything.

Client: Okay, I'll try.

Therapist: Good. Today we'll do a simple 4–4 breathing exercise. We'll breathe in gently for 4 counts, then breathe out slowly for 4 counts. There's no pressure to do it perfectly.

Client: Alright.

Therapist: First, just notice your breathing naturally for a moment. No need to change it yet.

Client: Okay…

Therapist: Now slowly breathe in through your nose… 1… 2… 3… 4… And gently breathe out… 1… 2… 3… 4…

Client: That feels manageable.

Therapist: Good. Let's do that again. Slow breath in… 1… 2… 3… 4… And slowly out… 1… 2… 3… 4… Try to let your shoulders soften a little as you breathe out.

Client: I can feel a little tension releasing.

Therapist: That's good to notice. No need to force relaxation—just allowing your body to slow down a bit. Let's continue one more time. Breathing in gently… 1… 2… 3… 4… And breathing out slowly… 1… 2… 3… 4…

Client: My breathing feels a bit steadier now.

Therapist: You're doing well. If your mind wanders or your body still feels tense, that's completely okay. Just gently bring your attention back to the counting and the breath.

Client: Okay, I can do that.

Therapist: Let's take two more slow breaths together at your own pace…

Client: I'm starting to feel a little calmer.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "breathing_exercise",
            "technique": "4_4_breathing"
        }
    },

    "mild_extended_exhale": {
        "kind": "breathing_exercise",
        "title": "Extended Exhale Breathing - Mild Physical Discomfort",
        "body": """Therapist: Before we start, just settle into a position that feels supportive for your body. You can adjust, stretch, or shift if you need to.

Client: Okay, I'm comfortable enough.

Therapist: Good. Today we're going to try extended exhale breathing. That simply means your exhale will be a little longer than your inhale. This can help the body slow down and feel calmer. There's no need to force the breath.

Client: Alright.

Therapist: First, just notice your natural breathing for a few seconds.

Client: Okay…

Therapist: Now gently breathe in through your nose for 4 counts… 1… 2… 3… 4… And slowly breathe out for 6 counts… 1… 2… 3… 4… 5… 6…

Client: The longer exhale feels different.

Therapist: Yes, sometimes people notice the body softening a little on the exhale. Let's try it again gently. Breathe in… 1… 2… 3… 4… And slowly breathe out… 1… 2… 3… 4… 5… 6… Let your jaw and shoulders loosen a little as you breathe out.

Client: I think my shoulders are relaxing a bit.

Therapist: That's good. You don't have to make anything happen—just noticing is enough. Let's continue at a comfortable pace. Slow inhale… 1… 2… 3… 4… And longer exhale… 1… 2… 3… 4… 5… 6…

Client: My breathing feels slower now.

Therapist: Good. If at any point the longer exhale feels uncomfortable, you can shorten the count. The goal is comfort and steadiness, not perfection.

Client: Okay, that helps.

Therapist: Let's do two more breaths together. Breathing in gently… 1… 2… 3… 4… And breathing out slowly… 1… 2… 3… 4… 5… 6…""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "breathing_exercise",
            "technique": "extended_exhale_breathing"
        }
    },

    "mild_body_scan_breathing": {
        "kind": "breathing_exercise",
        "title": "Body Scan Breathing - Mild Physical Discomfort",
        "body": """Therapist: Before we begin, take a moment to settle into a position that feels as comfortable and supported as possible. You can adjust your posture anytime during the exercise.

Client: Okay.

Therapist: Good. Today we'll combine slow breathing with a gentle body scan. The goal isn't to make sensations disappear, but simply to notice them without judging or fighting them.

Client: Alright.

Therapist: Start by taking a slow, comfortable breath in through your nose… and gently breathing out through your mouth.

Client: Okay…

Therapist: Again, breathing in slowly… and breathing out slowly. As you breathe, just notice the surface supporting your body beneath you.

Client: I can feel that.

Therapist: Good. Now bring your attention to the top of your head. You don't need to change anything—just notice any sensations there.

Client: It feels a little tense.

Therapist: Just noticing the tension is enough. Now gently let your attention move down to your forehead and jaw. Take a slow breath in… …and a long breath out. See if those muscles can soften even slightly as you exhale.

Client: My jaw was tighter than I realized.

Therapist: That's very common. Now slowly bring your attention down into your neck and shoulders. Notice any heaviness, tightness, or discomfort there.

Client: My shoulders feel really tight.

Therapist: As you breathe out, imagine giving those muscles permission to loosen just a little—without forcing them. Slow breath in… …and slow breath out.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "breathing_exercise",
            "technique": "body_scan_breathing"
        }
    },

    # ========== OBSERVATION TECHNIQUES ==========
    "observe_breath_mild": {
        "kind": "observation",
        "title": "Observe Your Breath - Mild Pain",
        "body": """Let's start by bringing your attention to your breath, in a way that feels easy for you.

There's no need to take deep breaths if that feels uncomfortable—just notice your natural breathing.

You might feel the air moving in through your nose… and out again…
or simply notice a small rise and fall in your body, wherever it feels most comfortable.

If the discomfort draws your attention, that's okay. You don't need to fight it.
Just gently shift your focus back to your breath, even if it's only for a moment.

Let your breath be soft and steady…
each exhale giving a small sense of release, without forcing anything.

You're not trying to change the pain—just giving your mind a place to rest.

If your attention moves away, kindly guide it back to your breathing, at your own pace.

Let's stay here together for a few moments, simply noticing each breath as it comes and goes.""",
        "metadata": {
            "step": "3",
            "state_code": "observation",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "observation_technique"
        }
    },

    "observe_breath_severe_with_grounding": {
        "kind": "observation",
        "title": "Observe Your Breath with Grounding - Severe Pain",
        "body": """Let's begin by noticing your breath, in whatever way feels easiest for you.

There's no need to change it—just allow it to be natural and gentle.

If the pain feels strong, that's okay. You're not doing anything wrong.
We're just going to find small moments of comfort within it.

Bring your attention to your breathing…
feeling the air come in… and go out.

If focusing on the breath is difficult, you can also notice something else grounding—
like the feeling of the bed or chair supporting your body…
or your feet resting against the surface beneath you.

You might gently say to yourself:
"I am here."
"I am safe in this moment."
"This will pass."
"I can take this one breath at a time."

Let each breath be soft…
and with each exhale, imagine releasing just a tiny bit of tension, without forcing anything.

If the pain pulls your attention away, that's okay.
Kindly guide it back—to your breath, or to the feeling of support around you.

You're not alone in this. I'm right here with you.

Let's stay with this, one breath at a time.""",
        "metadata": {
            "step": "3",
            "state_code": "observation",
            "emotional_state": "physically_uncomfortable",
            "intensity": "severe",
            "type": "observation_technique"
        }
    },

    "observe_breath_acute_pain": {
        "kind": "observation",
        "title": "Observe Your Breath - Acute Pain",
        "body": """Let's gently bring your attention to your breath.
There's no need to take deep breaths—just notice whatever breath is there.

If the pain feels sharp or overwhelming, see if you can focus just on this one breath…
and then the next. We're only taking it one moment at a time.

You might say quietly to yourself:
'This is intense, but it will pass.'
'I can get through this one breath.'

If it helps, notice something steady and supportive—
the surface beneath you… holding you… supporting your body.

Let your exhale be soft, like a small release of tension, without forcing it.

If your attention gets pulled into the pain, that's okay.
Gently bring it back—to your breath, or to the feeling of being supported.

I'm here with you. Let's stay with just this breath… and then the next.""",
        "metadata": {
            "step": "3",
            "state_code": "observation",
            "emotional_state": "physically_uncomfortable",
            "intensity": "acute",
            "type": "observation_technique"
        }
    },

    "observe_breath_chronic_pain": {
        "kind": "observation",
        "title": "Observe Your Breath - Chronic Pain",
        "body": """Let's begin by noticing your breath, just as it is.
There's no need to change anything—just allow your breathing to be natural.

If the pain is always there, that's okay.
We're not trying to push it away—just making a little space around it.

Bring your attention to your breath…
noticing the gentle rhythm of inhale and exhale.

You might say to yourself:
'I can live alongside this moment.'
'There is more than just the pain.'
'I can find small moments of ease.'

See if you can also notice areas in your body that feel neutral or slightly more comfortable,
even if they are small.

Let your breath move in and out, creating a sense of space…
a softening, without forcing any change.

If your mind returns to the pain, gently guide it back—
to your breath, or to any place in your body that feels even a little easier.

Take this one moment at a time. You're doing enough just by being here.""",
        "metadata": {
            "step": "3",
            "state_code": "observation",
            "emotional_state": "physically_uncomfortable",
            "intensity": "chronic",
            "type": "observation_technique"
        }
    },

    # ========== REASSURANCE & ASSESSMENT SCRIPTS ==========
    "assessment_clarifying": {
        "kind": "script",
        "title": "Clarifying the Discomfort - Assessment",
        "body": """Can you tell me where you're feeling the discomfort?

How would you describe it—sharp, dull, pressure, aching?

When did it start?

Is it constant or does it come and go?""",
        "metadata": {
            "step": "2",
            "state_code": "assessment",
            "emotional_state": "physically_uncomfortable",
            "type": "assessment_script"
        }
    },

    "assessment_intensity": {
        "kind": "script",
        "title": "Assessing Intensity - Assessment",
        "body": """On a scale from 0 to 10, how strong is it right now?

Is it mild, moderate, or severe for you?""",
        "metadata": {
            "step": "2",
            "state_code": "assessment",
            "emotional_state": "physically_uncomfortable",
            "type": "assessment_script"
        }
    },

    "assessment_impact": {
        "kind": "script",
        "title": "Understanding Impact - Assessment",
        "body": """Is it making it hard for you to focus on the exercise?

Does it get worse when you pay attention to it?

Is there any position that makes it feel better or worse?""",
        "metadata": {
            "step": "2",
            "state_code": "assessment",
            "emotional_state": "physically_uncomfortable",
            "type": "assessment_script"
        }
    },

    "collaborative_decision": {
        "kind": "script",
        "title": "Collaborative Decision-Making",
        "body": """How would you like to proceed from here?

Shall we continue gently, modify the exercise, or pause?

We can decide together—what would help you feel most comfortable?""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "type": "support_script"
        }
    }
}


def add_physically_uncomfortable_content():
    """Insert physically uncomfortable therapeutic content into database."""

    with get_session() as db:
        print("=" * 80)
        print("ADDING PHYSICALLY UNCOMFORTABLE THERAPEUTIC CONTENT")
        print("=" * 80)

        lib_items = []

        for key, content in PHYSICALLY_UNCOMFORTABLE_LIBRARY.items():
            item = LibraryItem(
                id=uuid.uuid4(),
                kind=content["kind"],
                title=content["title"],
                body=content["body"],
                item_metadata=content["metadata"]
            )
            lib_items.append(item)
            print(f"  ✓ {content['title']}")

        db.add_all(lib_items)
        db.flush()

        print("\n" + "=" * 80)
        print(f"SUCCESS! ADDED {len(lib_items)} LIBRARY ITEMS")
        print("=" * 80)
        print(f"\nContent added:")
        print(f"  - Emotional State: physically_uncomfortable")
        print(f"  - Opening Scripts: mild, moderate, severe")
        print(f"  - Breathing Exercises: 4 techniques")
        print(f"  - Observation Techniques: 4 variations")
        print(f"  - Assessment Scripts: 4 assessment types")
        print(f"\nTotal: {len(lib_items)} library items")
        print("\nThese are now available for RAG retrieval during chat sessions")
        print("=" * 80 + "\n")

        db.commit()


if __name__ == "__main__":
    try:
        add_physically_uncomfortable_content()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
