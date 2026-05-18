# Emotion-Based State Transitions

## Updated Flow with Classifier-Driven State Transitions

The system now uses the **classifier output (emotion)** to determine whether to proceed to the next step or stay for more support.

### How It Works

```
Patient sends message
    ↓
CLASSIFIER analyzes emotion
    → "calm" or "anxious"
    ↓
ORCHESTRATOR evaluates transition condition
    ↓
    IF emotion == "calm"
        → Proceed to next step
    ELSE IF emotion == "anxious"
        → Stay in current step (condition fails)
        → Provide additional support
```

---

## State Transition Logic

### Step 1: Introduction
**Condition to proceed:** `emotion == 'calm'`

```
Patient: "I'm feeling good and ready to begin"
    ↓
Classifier: emotion = "calm"
    ↓
Condition "emotion == 'calm'" evaluates to TRUE
    ↓
PROCEED to Step 2: Deep Breathing
```

---

### Step 2: Deep Breathing
**Condition to proceed:** `emotion == 'calm'`

If patient is **calm**:
```
Patient: "I'm feeling more relaxed now"
    ↓
Classifier: emotion = "calm"
    ↓
Condition "emotion == 'calm'" evaluates to TRUE
    ↓
PROCEED to Step 3: Observe Your Breath
```

If patient is **anxious**:
```
Patient: "I'm getting anxious, this is overwhelming"
    ↓
Classifier: emotion = "anxious"
    ↓
Condition "emotion == 'calm'" evaluates to FALSE
    ↓
STAY in Step 2: Deep Breathing
    ↓
Bot provides reassurance and support
Bot: "It's completely okay to feel anxious. Let's slow down and 
focus on your breathing. You're safe, and I'm here with you. 
Let's take a few more gentle breaths together..."
```

---

### Step 3: Observe Your Breath
**Condition to proceed:** `emotion == 'calm'`

- **If calm** → Proceed to Step 4 (Countdown)
- **If anxious** → Stay in Step 3, provide breath observation guidance

---

### Step 4: Countdown
**Condition to proceed:** `emotion == 'calm'`

- **If calm** → Proceed to Step 5 (Safe Place)
- **If anxious** → Stay in Step 4, provide countdown guidance with reassurance

---

### Step 5: Safe Place Visualization
**Condition to proceed:** `emotion == 'calm'`

- **If calm** → Proceed to Step 7 (Closing)
- **If anxious** → Stay in Step 5, allow more time for visualization and healing

---

### Step 7: Hindsight & Closing
**Final state** - No transitions after this

---

## Example: Anxious Patient Journey

### Start (Step 1: Introduction)
```
Bot: Hello, I'm RelaxBot... How are you feeling right now?
Patient: "I'm a bit nervous about this"
Classifier: emotion = "anxious"
Condition fails: emotion != "calm"
Action: STAY in Step 1, provide reassurance
```

### Reassurance Response (Still Step 1)
```
Bot: It's completely natural to feel nervous. You're safe here,
and this is your journey at your own pace. There's no pressure.
Whenever you feel ready to begin, just let me know.

Patient: "Okay, I'm ready to try"
Classifier: emotion = "calm"
Condition succeeds: emotion == "calm"
Action: PROCEED to Step 2: Deep Breathing
```

### Step 2: Deep Breathing
```
Bot: Let's begin with some gentle breathing...
Patient: "I'm still feeling a bit tense"
Classifier: emotion = "anxious"
Condition fails: emotion != "calm"
Action: STAY in Step 2, provide more breathing support
```

### More Breathing Support (Still Step 2)
```
Bot: Let's take our time. There's no rush. Each breath brings
you more calm. Let's breathe together: inhale... exhale...
inhale... exhale... You're doing great.

Patient: "I feel calmer now"
Classifier: emotion = "calm"
Condition succeeds: emotion == "calm"
Action: PROCEED to Step 3: Observe Your Breath
```

---

## Classifier Keywords

### Calm Keywords
- "calm", "ready", "peaceful", "relaxed", "okay", "fine", "good"
- "better", "yes", "sure", "let's", "begin", "start", "go"

### Anxious Keywords
- "anxious", "worried", "stressed", "nervous", "scared", "afraid"
- "panic", "tension", "overwhelmed", "help", "distressed"

---

## LLM-Generated Support Responses

When patient is anxious and condition fails, the bot provides LLM-generated support:

**System Prompt Includes:**
- Current state (e.g., "Step 2: Deep Breathing")
- Patient's emotional state: "anxious"
- Therapeutic guidelines for anxious patients

**Generated Response Example:**
```
"I can hear that you're feeling anxious, and that's completely okay.
This is a safe space, and we can go at your own pace. Let's focus on
something simple - just noticing your natural breath. There's nothing
to do, nowhere to rush to. You're safe here."
```

---

## Session Flow Examples

### Example 1: Calm Patient (Straight Through)
```
Step 1 (calm) → Step 2 (calm) → Step 3 (calm) → 
Step 4 (calm) → Step 5 (calm) → Step 7 (Complete)
Time: ~25 minutes
```

### Example 2: Anxious Patient (Takes More Time)
```
Step 1 (anxious → calm) → Step 2 (anxious → calm → anxious → calm) → 
Step 3 (calm) → Step 4 (calm) → Step 5 (calm) → Step 7 (Complete)
Time: ~40+ minutes
```

Patient gets support when needed, progresses when ready.

### Example 3: Mixed Emotions
```
Step 1 (calm) → Step 2 (calm) → Step 3 (anxious → anxious → calm) → 
Step 4 (calm) → Step 5 (anxious → calm) → Step 7 (Complete)
Time: ~35 minutes
```

System adapts to patient's emotional journey.

---

## Implementation Details

### Condition Evaluation
Each transition has a condition: `"emotion == 'calm'"`

The orchestrator evaluates this using:
1. **Classifier output** (from patient's latest message)
2. **Emotion value** (extracted from classifier output)
3. **Boolean evaluation** (does emotion equal "calm"?)

If TRUE → proceed to target state
If FALSE → stay in current state

### Fallback
If condition evaluation fails (error in expression):
- System logs error
- Default behavior: STAY in current state (fail-safe)
- Patient can continue responding

---

## What This Means for Patients

### Anxious Patients
- Get more support in early steps
- Can progress when they feel ready
- No pressure to rush through
- Bot adapts responses based on anxiety

### Calm Patients
- Progress smoothly through all steps
- Experience full therapeutic journey
- Reach closing affirmation

### Mixed Emotion Patients
- Get support when anxious
- Progress when calm
- Flexible journey based on emotional state

---

## Testing the New Flow

### Test 1: Calm Patient
```
You: "I'm feeling good and ready to begin"
Expected: → Step 2 (breathing)

You: "I'm relaxed now"
Expected: → Step 3 (observation)

You: "This is nice, continue"
Expected: → Step 4 (countdown)

[Continue through all steps]
```

### Test 2: Anxious Patient
```
You: "I'm feeling nervous"
Expected: STAY in Step 1 (introduction)
Bot: [Reassurance response]

You: "Okay, I'm ready now"
Expected: → Step 2 (breathing)

You: "This is overwhelming"
Expected: STAY in Step 2 (breathing)
Bot: [More breathing support]

You: "I'm calmer now"
Expected: → Step 3 (observation)

[Continue as patient becomes calm]
```

---

## Summary

The system now:
✅ **Classifies emotion** after every patient message
✅ **Evaluates transition conditions** based on emotion
✅ **Proceeds to next step** only if patient is calm
✅ **Stays in current step** if patient is anxious
✅ **Provides support** with LLM-generated responses
✅ **Adapts to patient's journey** (no forced progression)

Patient-centered, emotion-aware therapeutic progression!

