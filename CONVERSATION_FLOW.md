# Conversation Flow - Step by Step with LLM Synthesis

## Complete Flow Overview

```
STEP 1: Introduction (Bot asks "How are you feeling?")
    ↓
Patient responds (e.g., "I'm ready", "I'm feeling anxious")
    ↓
CLASSIFIER analyzes response
    → Detects emotion: "calm" or "anxious"
    → Detects intent: "start_breathing" or others
    ↓
SESSION MANAGER receives classifier output
    ↓
ORCHESTRATOR checks transitions
    → Current: Step 1 (intro)
    → Condition: "True" (always proceed)
    → Next: Step 2 (breathing)
    ↓
RAG RETRIEVER gathers context
    → Gets Step 2 library items (breathing techniques)
    → Gets emotional guidelines based on emotion
    → Gets session history
    ↓
LLM GENERATOR creates personalized response
    → Uses system prompt with therapeutic guidelines
    → Incorporates current state (breathing)
    → Incorporates emotional context
    → Generates warm, personalized response using Groq API
    ↓
BOT sends LLM-generated response to patient
    ↓
[REPEAT for Steps 3, 4, 5, 7...]
```

---

## STEP 1: Introduction - "How Are You Feeling?"

### Bot's Initial Message (From Library)
```
"Hello, I'm RelaxBot, your therapeutic companion. I'm here to help you find 
moments of peace and relaxation through guided imagery. Before we begin this 
therapeutic journey, I'd like to understand your current state. How are you 
feeling right now?"
```

**Current State:** Step 1: Introduction
**Library Item:** "Step 1: Introduction"

### Patient's Response Examples

**Example 1 - Calm Patient:**
```
Patient: "I'm feeling good and ready to begin"
```

**Classification Result:**
- Emotion: **calm**
- Intent: **start_breathing**
- Confidence: 85%
- Keywords matched: "good", "ready", "begin"

**Example 2 - Anxious Patient:**
```
Patient: "I'm feeling quite anxious and worried about things"
```

**Classification Result:**
- Emotion: **anxious**
- Intent: **request_calm**
- Confidence: 90%
- Keywords matched: "anxious", "worried"

---

## STEP 2: Deep Breathing - LLM-Generated Response

### What Happens Behind the Scenes

1. **Classifier Output:**
   ```json
   {
     "emotion": "calm",
     "intent": "start_breathing",
     "confidence": 0.85
   }
   ```

2. **Orchestrator Transition:**
   ```
   Current State: Step 1 (intro)
   Condition: "True" → Always proceed
   Next State: Step 2 (breathing)
   ```

3. **RAG Retriever Gathers Context:**
   ```
   - Library Items for Step 2:
     "Be in a comfortable position with your eyes closed..."
   - Emotional Guidelines for "calm":
     "Patient is ready. Encourage deeper breathing."
   - Session History:
     Patient message: "I'm feeling good and ready to begin"
   ```

4. **LLM System Prompt Built:**
   ```
   You are a compassionate therapeutic chatbot supporting oncology patients.
   
   Current State: Step 2: Deep Breathing
   State Description: Deep breathing to relax body and mind
   
   Patient's Emotional State: calm
   
   Therapeutic Guidelines:
   - Patient is ready for deeper work
   - Encourage focus on breath
   - Emphasize relaxation and tension release
   
   IMPORTANT RULES:
   1. Be warm, empathetic, and supportive
   2. Keep responses concise (2-3 sentences)
   3. Use relaxation techniques when appropriate
   4. Stay within the therapeutic context of breathing
   
   Respond naturally as if continuing a therapeutic conversation.
   ```

5. **LLM User Prompt:**
   ```
   Recent conversation:
   Patient: "I'm feeling good and ready to begin"
   
   Now guide the patient into deep breathing step with a warm, supportive message.
   Keep it concise and actionable.
   ```

6. **Groq API Generates Response:**
   Using mixtral-8x7b-32768 model with temperature 0.7
   
   **LLM Output Example:**
   ```
   "That's wonderful! I'm glad you're feeling ready. Let's begin with some 
   gentle, deep breathing. Find a comfortable position, and when you're ready, 
   close your eyes. As you breathe in, imagine bringing in calm, healing energy. 
   As you breathe out, let go of any tension. We'll take this at your own pace."
   ```

### Bot's Actual Response
```
That's wonderful! I'm glad you're feeling ready. Let's begin with some gentle, 
deep breathing. Find a comfortable position, and when you're ready, close your 
eyes. As you breathe in, imagine bringing in calm, healing energy. As you 
breathe out, let go of any tension. We'll take this at your own pace.
```

**Current State:** Step 2: Deep Breathing
**Response Type:** LLM-generated (not static)
**Emotion Awareness:** Yes (adapted to "calm" state)

---

## STEP 3: Observe Your Breath

### Patient's Response During Breathing
```
Patient: "I'm feeling more relaxed, my mind is clearer"
```

### Classifier Output
- Emotion: **calm**
- Intent: **continue_session**
- Confidence: 92%

### State Transition
```
Current: Step 2 (breathing)
Condition: "True" → Always proceed
Next: Step 3 (observation)
```

### LLM-Generated Response
**System Prompt Includes:**
- Current State: Step 3: Observe Your Breath
- Description: Natural breathing with So/In and Hum/Out technique
- Patient Emotion: calm
- Guidelines: Introduce technique gently, guide practice

**LLM Output Example:**
```
"Excellent work! You're already becoming more relaxed. Now let's deepen this 
experience. As you continue breathing naturally, I'd like you to add a gentle 
mental focus. With each inhale, quietly say 'In' or 'So', and with each exhale, 
say 'Out' or 'Hum'. This ancient technique helps anchor your mind and deepen 
your relaxation. Let's practice this together for a few minutes."
```

### Bot's Response
```
Excellent work! You're already becoming more relaxed. Now let's deepen this 
experience. As you continue breathing naturally, I'd like you to add a gentle 
mental focus. With each inhale, quietly say 'In' or 'So', and with each exhale, 
say 'Out' or 'Hum'. This ancient technique helps anchor your mind and deepen 
your relaxation. Let's practice this together for a few minutes.
```

---

## STEP 4: Countdown

### Patient's Response
```
Patient: "I can feel myself getting deeper into relaxation, my mind is quiet"
```

### Classifier Output
- Emotion: **calm**
- Intent: **continue_session**
- Confidence: 95%

### State Transition
```
Current: Step 3 (observation)
Condition: "True" → Always proceed
Next: Step 4 (countdown)
```

### LLM-Generated Response
**Prompt Includes:**
- Focus on countdown/deepening
- Patient is deeply calm
- Transition to visualization

**LLM Output Example:**
```
"Perfect! Your mind is settling beautifully. Now, with each breath, imagine 
numbers appearing before you - 10, 9, 8... Each number takes you deeper into 
a peaceful, calm state. As we count down together, feel yourself sinking gently 
into profound relaxation. I'll guide you: 10... breathing in peace... 9... 
letting go... 8... sinking deeper..."
```

---

## STEP 5: Safe Place Visualization

### Patient's Response
```
Patient: "I'm ready, I can see myself in a beautiful place already"
```

### Classifier Output
- Emotion: **calm**
- Intent: **continue_session**
- Confidence: 96%

### State Transition
```
Current: Step 4 (countdown)
Condition: "True" → Always proceed
Next: Step 5 (imagery)
```

### LLM-Generated Response (Multi-sensory Guidance)
**Prompt Includes:**
- Safe place visualization
- Multi-sensory exploration
- Healing focus

**LLM Output Example:**
```
"Wonderful! You have such a beautiful inner sanctuary. Let's explore it together. 
Look around - what colors, shapes, or textures do you notice? Now, listen - 
what sounds surround you? Perhaps birds, water, rustling leaves? Feel the air 
on your skin. What's the temperature? This is your healing place. Allow yourself 
to feel completely safe, completely held by this environment. Everything here 
nurtures and heals you."
```

---

## STEP 7: Hindsight & Closing

### Patient's Response
```
Patient: "That was beautiful and healing, I feel so peaceful now"
```

### Classifier Output
- Emotion: **calm**
- Intent: **continue_session**
- Confidence: 97%

### State Transition
```
Current: Step 5 (imagery)
Condition: "True" → Always proceed
Next: Step 7 (hindsight)
```

### LLM-Generated Closing Response
**Prompt Includes:**
- Reflection and integration
- Affirmation
- Carry forward practice

**LLM Output Example:**
```
"You've done beautiful work today. The peace and healing you've experienced 
are real and available to you anytime. As you gently return to full awareness, 
carry this calm with you. Remember: you have within you all the strength, 
courage, and resilience you need. You can return to this peaceful place 
whenever you need to. Thank you for taking this time for yourself."
```

---

## How LLM Synthesizes Each Response

### For Each Message, LLM Considers:

1. **Current Therapeutic State**
   - What step are we on? (breathing, observation, countdown, safe place, closing)
   - What's the focus of this state?

2. **Patient's Emotional State**
   - Calm → More adventurous, deeper guidance
   - Anxious → More reassurance, grounding, validation

3. **Conversation History**
   - What has the patient said so far?
   - What level of relaxation have they reached?
   - What images/metaphors have they used?

4. **Therapeutic Guidelines**
   - Warm and empathetic
   - Concise (2-3 sentences typically)
   - Action-oriented guidance
   - Validation and encouragement

5. **Natural Continuation**
   - Feels like talking with a real therapist
   - Builds on previous messages
   - Doesn't repeat what's been said
   - Introduces next layer of depth

### Example: Two Different Responses for Same Step

**Calm Patient in Step 2:**
```
"That's wonderful! I'm so glad you're feeling ready. Let's begin with some 
gentle deep breathing. As you inhale, imagine bringing in fresh, healing energy. 
As you exhale, release any tension. We can take this at your own pace."
```

**Anxious Patient in Step 2:**
```
"It's completely okay to feel anxious. These feelings are normal, and breathing 
can help settle them. Let's start very gently. Just breathe normally at first - 
there's no pressure to do anything special. As you relax, we can gradually 
deepen your breath. You're in control here."
```

---

## Fallback Mechanism

If Groq API fails for any reason:

1. System logs the error
2. Falls back to relevant library item
3. User still gets a therapeutic response
4. Session continues seamlessly

Example fallback for Step 2:
```
"Be in a comfortable position with your eyes closed. As per your capacity let 
your breathing get a little deeper and fuller. With every breath in, notice 
that you bring in fresh air, fresh oxygen and fresh energy to your body."
```

---

## Summary: Key Differences from Static Scripts

| Aspect | Static Library | LLM-Generated |
|--------|---|---|
| **Personalization** | Same for all | Adapted to emotional state |
| **Conversation Flow** | Linear and fixed | Natural and flowing |
| **Patient References** | None | Uses what patient said |
| **Depth** | Surface level | Builds progressively |
| **Warmth** | Generic | Genuinely supportive |
| **Adaptation** | No | Yes (emotion, pace, journey) |

---

## Testing the Flow

When you run `python scripts/interactive_chat.py`:

1. **Bot greets and asks:** "How are you feeling right now?"
2. **You respond naturally** (e.g., "I'm ready", "I'm anxious")
3. **System classifies** your emotion
4. **LLM generates** warm, personalized response
5. **Transitions** to breathing step
6. **For each subsequent message:**
   - Classifier analyzes your response
   - LLM generates contextual reply
   - State progresses automatically
7. **After 6 steps:** Session complete with closing affirmation

Each response from the bot is **unique and personalized** based on:
- Your emotional state
- What you've said
- The current therapeutic step
- Therapeutic best practices

