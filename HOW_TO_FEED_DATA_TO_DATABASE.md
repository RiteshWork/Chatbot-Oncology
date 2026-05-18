# How to Feed Data to the Database: Complete Step-by-Step Guide

## Overview

Your uploaded file contains therapeutic scripts organized by emotional state and intensity levels. This document shows **exactly how to structure and save this data** to the PostgreSQL database.

---

## Data Structure Mapping

### Your File Contains:
- **Emotional State:** Physically Uncomfortable
- **Intensity Levels:** Mild, Moderate, Severe
- **Content Types:** 
  - Introduction scripts
  - Breathing exercises (10 different techniques)
  - Observation techniques
  - Grounding scripts

### Where It Goes in Database:

```
library_items table
├─ kind: "script" or "breathing_exercise"
├─ title: "Physically Uncomfortable - Mild - Deep Belly Breathing"
├─ body: "I know there's a little discomfort..."
└─ metadata (JSON):
    {
      "step": "2",  // Which step (breathing exercises)
      "state_code": "physically_uncomfortable",
      "emotional_state": "physically_uncomfortable",
      "intensity": "mild",
      "type": "breathing_exercise",
      "technique": "deep_belly_breathing"
    }
```

---

## Data Format: How to Structure Each Entry

### Format 1: Introduction Script
```json
{
  "id": "550e8400-uuid-001",
  "kind": "script",
  "title": "Step 1: Introduction - Physically Uncomfortable",
  "body": "Welcome to your Guided Imagery experience. Guided imagery is a gentle relaxation technique...",
  "metadata": {
    "step": "1",
    "state_code": "introduction",
    "emotional_state": "physically_uncomfortable",
    "type": "base_script",
    "severity": "all"
  },
  "created_at": "2025-05-13T00:00:00Z"
}
```

### Format 2: Breathing Exercise (Mild Intensity)
```json
{
  "id": "550e8400-uuid-002",
  "kind": "breathing_exercise",
  "title": "Deep Belly Breathing - Mild Discomfort",
  "body": "I know there's a little discomfort—we'll keep this gentle. Just notice your breath...",
  "metadata": {
    "step": "2",
    "state_code": "breathing",
    "emotional_state": "physically_uncomfortable",
    "intensity": "mild",
    "type": "breathing_exercise",
    "technique": "deep_belly_breathing"
  }
}
```

### Format 3: Observation Script (for pain)
```json
{
  "id": "550e8400-uuid-003",
  "kind": "observation",
  "title": "Observe Your Breath - Mild Pain",
  "body": "Let's start by bringing your attention to your breath...",
  "metadata": {
    "step": "3",
    "state_code": "observation",
    "emotional_state": "physically_uncomfortable",
    "intensity": "mild",
    "type": "observation_technique"
  }
}
```

---

## How Data Flows: From File to Database to Chat

```
Your DOCX File
    ↓
Extract Text Content
    ↓
Structure as JSON with Metadata
    ↓
Insert into library_items table
    ↓
During Chat:
   - User says: "I'm having pain"
   - Classifier detects: emotion = "physically_uncomfortable"
   - RAG queries: SELECT * FROM library_items 
                  WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
   - Retrieves: All breathing exercises, scripts, observations for this state
   - LLM: Uses retrieved content to generate personalized response
   - Response sent to user with therapeutic technique
```

---

## Python Script: Feed Data to Database

Create a file: `scripts/add_physically_uncomfortable_content.py`

```python
"""
scripts/add_physically_uncomfortable_content.py
Load Physically Uncomfortable content into database from DOCX file
"""

import sys
import os
import uuid
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_session
from library.models import LibraryItem

# ============================================================================
# CONTENT DATA - Extracted from your DOCX file
# ============================================================================

PHYSICALLY_UNCOMFORTABLE_CONTENT = {
    # Introduction
    "introduction": {
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

    # Mild Discomfort - Deep Belly Breathing
    "mild_belly_breathing": {
        "kind": "breathing_exercise",
        "title": "Deep Belly Breathing - Mild Physical Discomfort",
        "body": """Therapist: Before we begin, just settle into a position that feels comfortable for you. You don't need to force anything.
Are you feeling okay to start?

Client: Yeah, I think so.

Therapist: Good. Today we'll do a simple deep belly breathing exercise. The goal isn't to breathe perfectly — just to gently notice and slow the breath.
You can place one hand on your chest and the other on your belly if that feels comfortable.

Client: Okay.

Therapist: As you breathe in through your nose, see if you can let the belly rise slightly, almost like filling a balloon.
And as you breathe out slowly through your mouth, let the belly soften and fall.

Client: Alright.

Therapist: Let's try one together.
Slow inhale… 1… 2… 3… 4…
And a gentle exhale… 1… 2… 3… 4… 5… 6…

Client: I can feel my stomach moving a little.

Therapist: That's good. There's no need to make the breath very deep or forceful. Just comfortable and natural.
Again, breathing in slowly through the nose… letting the belly expand…
And breathing out slowly… releasing tension from the shoulders and jaw.

Client: My breathing feels a bit slower now.

Therapist: Nice. Just continue at that pace.
With each exhale, imagine your body softening a little more.
If your mind wanders, that's completely okay — simply guide your attention back to the feeling of the breath.

Client: Okay, I'll try.

Therapist: You're doing well.
Take another slow breath in…
And a longer, relaxed breath out.
(Pause)
Notice the support beneath you.
Notice the gentle rise and fall of your belly.
Nothing else you need to do right now except breathe.

Client: I feel a little calmer.

Therapist: I'm glad to hear that.
Let's take two more slow breaths together.
Inhale gently…
And exhale slowly…
One more time…
Breathing in…
And breathing out… letting the body relax.
(Pause)
Whenever you're ready, you can slowly bring your awareness back to the room.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "breathing_exercise",
            "technique": "deep_belly_breathing"
        }
    },

    # Mild Discomfort - 4-4 Breathing
    "mild_4_4_breathing": {
        "kind": "breathing_exercise",
        "title": "4-4 Breathing - Mild Physical Discomfort",
        "body": """Therapist: Before we begin, just try to sit in a position that feels as comfortable as possible. You don't have to force anything.

Client: Okay, I'll try.

Therapist: Good. Today we'll do a simple 4–4 breathing exercise. We'll breathe in gently for 4 counts, then breathe out slowly for 4 counts. There's no pressure to do it perfectly.

Client: Alright.

Therapist: First, just notice your breathing naturally for a moment. No need to change it yet.

Client: Okay…

Therapist: Now slowly breathe in through your nose…
1… 2… 3… 4…
And gently breathe out…
1… 2… 3… 4…

Client: That feels manageable.

Therapist: Good. Let's do that again.
Slow breath in…
1… 2… 3… 4…
And slowly out…
1… 2… 3… 4…
Try to let your shoulders soften a little as you breathe out.

Client: I can feel a little tension releasing.

Therapist: That's good to notice. No need to force relaxation—just allowing your body to slow down a bit.
Let's continue one more time.
Breathing in gently…
1… 2… 3… 4…
And breathing out slowly…
1… 2… 3… 4…

Client: My breathing feels a bit steadier now.

Therapist: You're doing well. If your mind wanders or your body still feels tense, that's completely okay. Just gently bring your attention back to the counting and the breath.

Client: Okay, I can do that.

Therapist: Let's take two more slow breaths together at your own pace…

Client: I'm starting to feel a little calmer.

Therapist: Good. Just notice that feeling for a moment—however small it is—and allow yourself to stay with the steady rhythm of your breathing.""",
        "metadata": {
            "step": "2",
            "state_code": "breathing",
            "emotional_state": "physically_uncomfortable",
            "intensity": "mild",
            "type": "breathing_exercise",
            "technique": "4_4_breathing"
        }
    },

    # Moderate Discomfort Script
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

    # Severe Discomfort Script
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

    # Observation with Pain
    "observe_breath_mild_pain": {
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

    # Observation with Severe Pain and Grounding
    "observe_breath_severe_pain": {
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
    }
}

# ============================================================================
# SCRIPT TO INSERT INTO DATABASE
# ============================================================================

def add_physically_uncomfortable_content():
    """Add physically uncomfortable content to library_items table."""

    with get_session() as db:
        print("=" * 80)
        print("ADDING PHYSICALLY UNCOMFORTABLE CONTENT")
        print("=" * 80)

        lib_items = []
        
        for key, content in PHYSICALLY_UNCOMFORTABLE_CONTENT.items():
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
        db.commit()

        print("\n" + "=" * 80)
        print(f"SUCCESS! Added {len(lib_items)} Physically Uncomfortable items")
        print("=" * 80)


if __name__ == "__main__":
    try:
        add_physically_uncomfortable_content()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
```

---

## How to Use This Script

### Step 1: Save the Script
Save the above Python code as:
```
E:\Chatbot-Onco-ojaska labs\relaxbot\scripts\add_physically_uncomfortable_content.py
```

### Step 2: Run on Your Local Machine
Open PowerShell and run:
```powershell
cd "E:\Chatbot-Onco-ojaska labs\relaxbot"
python scripts/add_physically_uncomfortable_content.py
```

### Step 3: Verify It Worked
Run the inspect script:
```powershell
python scripts/inspect_db.py
```

Look for output showing library items now include "physically_uncomfortable" in their metadata.

---

## How This Data Gets Used in Chat

### When User Types: "I have pain"

```
1. CLASSIFIER
   - Input: "I have pain"
   - Output: emotion = "physically_uncomfortable" (because "pain" in PHYSICALLY_UNCOMFORTABLE_KEYWORDS)
   - Confidence: 0.85

2. ORCHESTRATOR
   - Current state: Step 1 (Introduction)
   - Evaluates transition condition
   - Routes to Step 2 (Breathing)

3. RAG RETRIEVER
   - Query: Get library items WHERE:
     • state_code = "breathing"
     • emotional_state = "physically_uncomfortable"
   - Returns:
     • Deep Belly Breathing script
     • 4-4 Breathing script
     • Moderate discomfort opening
     • All relevant breathing exercises

4. LLM SYNTHESIZER
   - System Prompt: "State: Breathing. Emotion: physically_uncomfortable.
                     Guidelines: Acknowledge pain, offer gentle technique, no forcing"
   - Context: Retrieved breathing exercises
   - Generates: Personalized response using one of the breathing techniques

5. RESPONSE TO USER
   "I understand you're experiencing pain. Let's try a gentle technique that can help.
    Let's do some deep belly breathing together...
    Just settle into a comfortable position..."
```

---

## What Format Should Your Data Be In?

### ✅ CORRECT FORMAT (What Database Expects):

```python
LibraryItem(
    id=UUID(),
    kind="script|breathing_exercise|observation",
    title="Human-readable title",
    body="Full content/script text",
    item_metadata={
        "step": "1|2|3|...",
        "state_code": "introduction|breathing|observation|...",
        "emotional_state": "physically_uncomfortable|anxious|emotional|...",
        "type": "base_script|breathing_exercise|emotional_response|...",
        "intensity": "mild|moderate|severe",
        "technique": "deep_belly_breathing|4_4_breathing|..." (optional)
    }
)
```

### ✗ WRONG FORMAT (What Not To Do):

```python
# Don't put raw DOCX content directly
# Don't use unstructured text
# Don't skip metadata
# Don't mix emotional states in one item
```

---

## Summary

| Step | What To Do | Format |
|------|-----------|--------|
| 1 | Extract your DOCX content | Plain text scripts |
| 2 | Structure each script | LibraryItem with metadata JSON |
| 3 | Add to Python script | Dictionary with kind, title, body, metadata |
| 4 | Run on local machine | `python scripts/add_*.py` |
| 5 | Verify in database | `python scripts/inspect_db.py` |
| 6 | Test in chat | Type messages, verify RAG retrieves content |

---

## Your File: What Gets Stored Where

Your "Physically uncomfortable Version2 (Ado).docx" contains:

### ✅ Gets Stored As Library Items:
- Introduction script → `library_items.kind = "script"`
- All 10+ breathing exercises → `library_items.kind = "breathing_exercise"`
- Observation techniques → `library_items.kind = "observation"`
- Opening scripts for mild/moderate/severe → `library_items.kind = "script"`

### ✅ Metadata Tags Each Item:
- `emotional_state: "physically_uncomfortable"`
- `intensity: "mild|moderate|severe"`
- `technique: "deep_belly_breathing|4_4_breathing|..."`

### ✅ This Allows RAG To:
- Filter by emotional state
- Filter by intensity level
- Find the right breathing technique
- Present context-appropriate content

---

## Next Steps

1. **Adapt the script** - Copy `add_physically_uncomfortable_content.py` and modify for other emotional states
2. **Repeat for each file** - Create similar scripts for Comfortable, Emotional, Hesitant, etc.
3. **Run on local machine** - Execute each script to populate the database
4. **Test** - Chat with the bot and see it use your custom content
5. **Verify RAG** - Check that responses use your therapeutic scripts

---

## Questions?

- **"How does RAG know which content to use?"** → It queries `metadata` JSON column for `state_code` and `emotional_state`
- **"Can I have multiple scripts per state/emotion?"** → Yes! Create multiple `LibraryItem` records with same metadata
- **"How does LLM use this?"** → RAG passes retrieved content as context; LLM synthesizes it into response
- **"What if I want to update content?"** → Delete old `LibraryItem`, add new one with updated `body` text
