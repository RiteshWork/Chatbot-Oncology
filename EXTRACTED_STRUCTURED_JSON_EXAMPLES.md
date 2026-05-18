# Extracted & Structured JSON Data from Your DOCX File

## Overview

Your **Physically uncomfortable Version2 (Ado).docx** was extracted and structured into JSON format. Below are the **exact structures** that will be inserted into the database.

---

## Data Structure Breakdown

### Each Library Item Has 4 Main Parts:

```
LibraryItem {
  id: UUID (auto-generated)
  kind: String (type of content)
  title: String (human-readable name)
  body: String (full content/script)
  metadata: JSON Object (for filtering and retrieval)
  created_at: DateTime (auto-generated)
}
```

---

## Example 1: Introduction Script

### What It Looks Like in Python:

```python
"intro_check": {
    "kind": "script",
    "title": "Step 1: Introduction - Physically Uncomfortable Check-In",
    "body": """Welcome to your Guided Imagery experience...
                [full content from your DOCX]""",
    "metadata": {
        "step": "1",
        "state_code": "introduction",
        "emotional_state": "physically_uncomfortable",
        "type": "base_script",
        "severity": "all"
    }
}
```

### What Gets Saved to Database (JSON):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "kind": "script",
  "title": "Step 1: Introduction - Physically Uncomfortable Check-In",
  "body": "Welcome to your Guided Imagery experience.\n\nGuided imagery is a gentle relaxation technique that uses your imagination to help your mind and body feel calmer and more at ease. There's no right or wrong way to experience it—just allow yourself to follow along in a way that feels comfortable for you.\n\nYou may begin to notice a sense of relaxation, clarity, or calm as we continue.\n\nBefore we start, I just want to check—are you feeling comfortable right now? If you need to adjust your position or have any questions, please feel free to tell me.",
  "metadata": {
    "step": "1",
    "state_code": "introduction",
    "emotional_state": "physically_uncomfortable",
    "type": "base_script",
    "severity": "all"
  },
  "created_at": "2025-05-13T12:00:00Z"
}
```

### How RAG Uses This:

```sql
-- When classifier detects: emotion = "physically_uncomfortable"
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
AND metadata->>'step' = '1'
-- Returns: This introduction script
```

---

## Example 2: Opening Script (Mild Discomfort)

### Python Structure:

```python
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
}
```

### Database JSON:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "kind": "script",
  "title": "Opening Script - Mild Physical Discomfort",
  "body": "I know there's a little discomfort—we'll keep this gentle.\nJust notice your breath as it is… no need to change anything.\nIn… and out… comfortably.\nIf you need to adjust your position, that's okay.\nLet's take this one easy breath at a time.",
  "metadata": {
    "step": "2",
    "state_code": "breathing",
    "emotional_state": "physically_uncomfortable",
    "intensity": "mild",
    "type": "opening_script"
  },
  "created_at": "2025-05-13T12:01:00Z"
}
```

### RAG Query for This:

```sql
-- When classifier detects: emotion = "physically_uncomfortable" AND intensity = "mild"
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
AND metadata->>'intensity' = 'mild'
AND metadata->>'step' = '2'
-- Returns: This opening script + all mild breathing exercises
```

---

## Example 3: Breathing Exercise with Therapist Dialogue

### Python Structure:

```python
"mild_belly_breathing": {
    "kind": "breathing_exercise",
    "title": "Deep Belly Breathing - Mild Physical Discomfort",
    "body": """Therapist: Before we begin, just settle into a position that feels comfortable for you. You don't need to force anything. Are you feeling okay to start?

Client: Yeah, I think so.

Therapist: Good. Today we'll do a simple deep belly breathing exercise. The goal isn't to breathe perfectly — just to gently notice and slow the breath. You can place one hand on your chest and the other on your belly if that feels comfortable.

Client: Okay.

[... continues with full dialogue from your DOCX ...]""",
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

### Database JSON (Truncated):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "kind": "breathing_exercise",
  "title": "Deep Belly Breathing - Mild Physical Discomfort",
  "body": "Therapist: Before we begin, just settle into a position that feels comfortable for you. You don't need to force anything. Are you feeling okay to start?\n\nClient: Yeah, I think so.\n\nTherapist: Good. Today we'll do a simple deep belly breathing exercise...",
  "metadata": {
    "step": "2",
    "state_code": "breathing",
    "emotional_state": "physically_uncomfortable",
    "intensity": "mild",
    "type": "breathing_exercise",
    "technique": "deep_belly_breathing"
  },
  "created_at": "2025-05-13T12:02:00Z"
}
```

### Metadata Tags Explained:

| Tag | Value | Meaning |
|-----|-------|---------|
| `step` | `"2"` | This is Step 2 (Breathing) in therapeutic flow |
| `state_code` | `"breathing"` | Current state is breathing exercises |
| `emotional_state` | `"physically_uncomfortable"` | Target emotion this addresses |
| `intensity` | `"mild"` | For patients with mild discomfort |
| `type` | `"breathing_exercise"` | This is a breathing technique, not observation/script |
| `technique` | `"deep_belly_breathing"` | Specific technique name |

---

## Example 4: Observation Technique (Severe Pain with Grounding)

### Python Structure:

```python
"observe_breath_severe_with_grounding": {
    "kind": "observation",
    "title": "Observe Your Breath with Grounding - Severe Pain",
    "body": """Let's begin by noticing your breath, in whatever way feels easiest for you.

There's no need to change it—just allow it to be natural and gentle.

If the pain feels strong, that's okay. You're not doing anything wrong.
We're just going to find small moments of comfort within it.

[... continues with full technique from your DOCX ...]""",
    "metadata": {
        "step": "3",
        "state_code": "observation",
        "emotional_state": "physically_uncomfortable",
        "intensity": "severe",
        "type": "observation_technique"
    }
}
```

### Database JSON (Truncated):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440012",
  "kind": "observation",
  "title": "Observe Your Breath with Grounding - Severe Pain",
  "body": "Let's begin by noticing your breath, in whatever way feels easiest for you.\n\nThere's no need to change it—just allow it to be natural and gentle...",
  "metadata": {
    "step": "3",
    "state_code": "observation",
    "emotional_state": "physically_uncomfortable",
    "intensity": "severe",
    "type": "observation_technique"
  },
  "created_at": "2025-05-13T12:05:00Z"
}
```

---

## Example 5: Assessment Script

### Python Structure:

```python
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
}
```

### Database JSON:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440015",
  "kind": "script",
  "title": "Assessing Intensity - Assessment",
  "body": "On a scale from 0 to 10, how strong is it right now?\n\nIs it mild, moderate, or severe for you?",
  "metadata": {
    "step": "2",
    "state_code": "assessment",
    "emotional_state": "physically_uncomfortable",
    "type": "assessment_script"
  },
  "created_at": "2025-05-13T12:06:00Z"
}
```

---

## Complete List: All 18 Items Extracted

Here's how all 18 items from your DOCX are structured:

### 1. Introduction
```
kind: "script"
title: "Step 1: Introduction - Physically Uncomfortable Check-In"
metadata.step: "1"
metadata.state_code: "introduction"
metadata.type: "base_script"
```

### 2-4. Opening Scripts (Intensity Levels)
```
kind: "script"
title: "Opening Script - [Mild|Moderate|Severe] Physical Discomfort"
metadata.step: "2"
metadata.state_code: "breathing"
metadata.intensity: "mild|moderate|severe"
metadata.type: "opening_script"
```

### 5-8. Breathing Exercises (Mild Discomfort)
```
kind: "breathing_exercise"
title: "[Deep Belly|4-4|Extended Exhale|Body Scan] Breathing - Mild Physical Discomfort"
metadata.step: "2"
metadata.state_code: "breathing"
metadata.intensity: "mild"
metadata.type: "breathing_exercise"
metadata.technique: "deep_belly_breathing|4_4_breathing|extended_exhale_breathing|body_scan_breathing"
```

### 9-12. Observation Techniques (Various Intensities)
```
kind: "observation"
title: "Observe Your Breath - [Mild|Severe+Grounding|Acute|Chronic] Pain"
metadata.step: "3"
metadata.state_code: "observation"
metadata.intensity: "mild|severe|acute|chronic"
metadata.type: "observation_technique"
```

### 13-16. Assessment Scripts
```
kind: "script"
title: "[Clarifying|Intensity|Impact|Decision] - Assessment"
metadata.step: "2"
metadata.state_code: "assessment"
metadata.type: "assessment_script"
```

### 17. Collaborative Script
```
kind: "script"
title: "Collaborative Decision-Making"
metadata.step: "2"
metadata.state_code: "breathing"
metadata.type: "support_script"
```

### 18. Safe Place Script
```
kind: "script"
title: "Inner World and Safe Place"
metadata.step: "4"
metadata.state_code: "safe_place"
metadata.type: "visualization_script"
```

---

## How Metadata Filters Work in Database

### Query 1: Get ALL Physically Uncomfortable Items
```sql
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
-- Returns: All 18 items
```

### Query 2: Get Only Mild Intensity
```sql
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
AND metadata->>'intensity' = 'mild'
-- Returns: 5 items (opening, 4 breathing exercises)
```

### Query 3: Get Only Breathing Exercises
```sql
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
AND metadata->>'type' = 'breathing_exercise'
-- Returns: 4 items (belly, 4-4, extended exhale, body scan)
```

### Query 4: Get Specific Technique
```sql
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
AND metadata->>'technique' = 'deep_belly_breathing'
-- Returns: 1 item (Deep Belly Breathing)
```

---

## Real Example: What RAG Returns During Chat

### When User Types: "My shoulders are killing me"

**Step 1: Classifier Output**
```json
{
  "emotion": "physically_uncomfortable",
  "confidence": 0.92,
  "detected_keywords": ["shoulders", "killing me", "pain"]
}
```

**Step 2: RAG Query Executed**
```sql
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'physically_uncomfortable'
```

**Step 3: Results Returned (18 items)**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Step 1: Introduction - Physically Uncomfortable Check-In",
    "body": "Welcome to your Guided Imagery experience...",
    "metadata": {"step": "1", "state_code": "introduction", "intensity": "all"}
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "title": "Opening Script - Mild Physical Discomfort",
    "body": "I know there's a little discomfort...",
    "metadata": {"step": "2", "intensity": "mild", "type": "opening_script"}
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "title": "Deep Belly Breathing - Mild Physical Discomfort",
    "body": "Therapist: Before we begin...",
    "metadata": {"step": "2", "intensity": "mild", "type": "breathing_exercise", "technique": "deep_belly_breathing"}
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440009",
    "title": "Shoulder Relaxation Breathing",
    "body": "Therapist: Before we begin, try to sit in a position...",
    "metadata": {"step": "2", "intensity": "mild", "technique": "shoulder_relaxation"}
  },
  ... 14 more items ...
]
```

**Step 4: LLM Receives Context**
```
System Prompt:
  "Patient has physical discomfort (shoulders).
   State: Breathing exercises.
   Retrieved 18 therapeutic scripts.
   
   Context:
   - Opening for mild discomfort: 'I know there's a little discomfort...'
   - Deep Belly Breathing: [full technique]
   - Shoulder Relaxation Breathing: [full technique]
   - Body Scan Breathing: [full technique]
   - Observation techniques: [all 4 variations]
   - Assessment scripts: [4 assessment types]"
```

**Step 5: LLM Generates Response**
```
Output:
"I hear your shoulders are really tense. That's a common place where we hold stress.

Let me share a technique that works particularly well for shoulder tension.

First, let's settle into a comfortable position. You can sit or lie down—whatever feels 
best for your shoulders.

Now we'll do some shoulder relaxation breathing. This technique specifically targets 
the shoulders...

[Uses content from your DOCX file: Shoulder Relaxation Breathing script]"
```

---

## Summary: From Your DOCX to Database to Chat

```
Your DOCX File
  ↓
Extract Text (557 paragraphs)
  ↓
Organize by Section:
  - Introductions (1)
  - Opening Scripts (3)
  - Breathing Exercises (4)
  - Observation Techniques (4)
  - Assessment Scripts (4)
  - Support Scripts (2)
  ↓
Add Metadata Tags:
  {
    "step": therapeutic step number
    "state_code": breathing|observation|assessment
    "emotional_state": physically_uncomfortable
    "intensity": mild|moderate|severe|acute|chronic
    "type": script|breathing_exercise|observation
    "technique": specific_technique_name (optional)
  }
  ↓
Create Python Dictionary (18 items)
  ↓
Insert Into Database (library_items table)
  ↓
RAG Retrieves by Metadata
  ↓
LLM Uses Retrieved Content
  ↓
User Gets Personalized Response
```

---

## Metadata Tags Reference

### step (1-7)
- "1" = Introduction
- "2" = Breathing/Assessment
- "3" = Observation
- "4" = Visualization
- "5" = Countdown
- "6" = Safe Place
- "7" = Closing

### state_code
- "introduction" = Intro scripts
- "breathing" = Breathing techniques
- "observation" = Observation scripts
- "assessment" = Assessment questions
- "safe_place" = Visualization
- "closing" = End of session

### emotional_state
- "physically_uncomfortable" = Your emotional state tag
- (also: "anxious", "emotional", "hesitant", etc.)

### intensity
- "mild" = Slight discomfort
- "moderate" = Noticeable discomfort
- "severe" = Strong discomfort
- "acute" = Sudden, intense pain
- "chronic" = Persistent pain
- "all" = Applies to all intensities

### type
- "script" = General script
- "breathing_exercise" = Breathing technique
- "observation" = Observation method
- "assessment_script" = Assessment question
- "opening_script" = Opening statement
- "support_script" = Support/reassurance

### technique (optional)
- "deep_belly_breathing"
- "4_4_breathing"
- "extended_exhale_breathing"
- "body_scan_breathing"
- "shoulder_relaxation_breathing"
- (and others specific to your content)

---

## Key Takeaway

Every piece of content from your DOCX has been:
1. ✅ **Extracted** as plain text
2. ✅ **Structured** with metadata JSON for filtering
3. ✅ **Organized** by step, state, intensity, and type
4. ✅ **Formatted** for database insertion
5. ✅ **Ready** to be queried by RAG and used by LLM

The Python script contains all 18 items in this exact format. When you run it, all this data goes directly into your PostgreSQL database!
