# QuickStart Guide - Therapeutic Chatbot

## What's Been Implemented

Your therapeutic chatbot is now **fully functional** with:

✅ **Complete 6-step therapeutic flow:**
- Step 1: Introduction to guided imagery VR experience
- Step 2: Deep breathing exercises
- Step 3: Observe your breath (So/Hum technique)
- Step 4: Countdown visualization (10→1)
- Step 5: Safe place visualization
- Step 7: Hindsight & closing affirmation

✅ **Full RAG + LLM pipeline:**
- Emotion/intent classification of user messages
- Context retrieval based on therapeutic state
- Personalized response generation using Groq API
- Automatic state transitions

✅ **Production-ready components:**
- Database models with PostgreSQL
- Session management with automatic process assignment
- State machine orchestration
- REST API endpoints

## 3 Simple Steps to Test

### 1️⃣ Clean Database
```bash
cd E:\Chatbot-Onco-ojaska labs\relaxbot
python scripts/cleanup_db.py
```

Expected output:
```
================================================================================
CLEANING UP DATABASE
================================================================================
[1] Deleting sessions...
[2] Deleting processes...
[3] Deleting states...
[4] Deleting library items...

================================================================================
DATABASE CLEANUP COMPLETE
================================================================================
```

### 2️⃣ Create Sample Data
```bash
python scripts/create_sample_data.py
```

Expected output:
```
================================================================================
CREATING CALM FLOW PROCESS TEMPLATE (7 STATES)
================================================================================

[1] Creating States...
  Created state: Step 1: Introduction
  Created state: Step 2: Deep Breathing
  Created state: Step 3: Observe Your Breath
  Created state: Step 4: Countdown
  Created state: Step 5: Inner World - Safe Place
  Created state: Step 7: Hindsight & Closing

[2] Creating Process Definition...
  Created process: Guided Imagery - Therapeutic Visualization

[3] Creating Library Items...
  Created 6 library items

================================================================================
SUCCESS! CALM FLOW PROCESS CREATED
================================================================================
```

### 3️⃣ Run Interactive Chat
```bash
python scripts/interactive_chat.py
```

Then follow the prompts:

```
RELAXBOT INTERACTIVE CONVERSATION

Bot: Welcome to your Guided Imagery VR experience...

You: [type your response]

[System analyzes your emotion and generates response]

Bot: [personalized therapeutic response]

[Continue the conversation...]

Type "exit", "quit", or "bye" to end.
```

## What Happens When You Run It

```
User types message
    ↓
Emotion Classifier analyzes message
    → "I'm feeling anxious" → Emotion: anxious
    → "I'm ready to begin" → Emotion: calm
    ↓
Orchestrator checks state transitions
    → Current: Step 1 (Introduction)
    → Condition: "True" (always proceed)
    → Next: Step 2 (Breathing)
    ↓
RAG retrieves context
    → Gets Step 2 content (breathing script)
    → Gets therapeutic guidelines for anxiety
    → Gets conversation history
    ↓
LLM generates response
    → Uses Groq API (mixtral-8x7b-32768)
    → Incorporates emotional guidelines
    → Creates warm, supportive response
    ↓
Bot responds with personalized message
```

## API Testing (Optional)

### Start the API server:
```bash
python -m uvicorn api.app:app --reload --port 8000
```

### Create a session:
```bash
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "test_user", "process_code": "guided_imagery_v1"}'
```

Response (copy the session_id):
```json
{
  "success": true,
  "session_id": "12345-67890-...",
  "patient_id": "test_user",
  "message": "Session created. Use this session_id for /chat endpoint."
}
```

### Chat with the bot:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "12345-67890-...", "message": "I'm ready to begin"}'
```

Response:
```json
{
  "success": true,
  "session_id": "12345-67890-...",
  "current_state": {
    "state_id": "uuid",
    "state_code": "guided_breathing",
    "state_name": "Step 2: Deep Breathing"
  },
  "llm_response": "Let's begin with some deep breathing...",
  "message_count": 1,
  "content": [...]
}
```

## Verify Everything Works

### ✅ Check 1: Database Connection
The scripts will fail if PostgreSQL isn't running on localhost:5555.
Make sure your PostgreSQL server is running with the database `chatbot_oncology`.

### ✅ Check 2: Groq API Key
The system will fall back to library scripts if API key fails, but to get full LLM responses, ensure GROQ_API_KEY is set in `.env`.

### ✅ Check 3: State Transitions
Watch for these state changes as you progress through the conversation:
```
Introduction → Breathing → Observation → Countdown → Safe Place → Hindsight
```

### ✅ Check 4: Emotional Classification
The system should recognize:
- Calm messages: "I'm ready", "Let's begin", "I feel relaxed"
- Anxious messages: "I'm nervous", "This is scary", "I'm worried"

## Key Files

| File | Purpose |
|------|---------|
| `scripts/cleanup_db.py` | Clear old data |
| `scripts/create_sample_data.py` | Populate database |
| `scripts/interactive_chat.py` | Test conversation |
| `api/app.py` | REST API endpoints |
| `orchestrator/session_manager.py` | Main orchestration |
| `rag/llm_generator.py` | LLM integration |

## Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: connection failed
```
**Solution:** Start PostgreSQL server
```bash
# Windows
pg_ctl -D "C:\Program Files\PostgreSQL\data" start

# macOS
brew services start postgresql

# Linux
sudo service postgresql start
```

### Groq API Error
```
Error generating response: authentication failed
```
**Solution:** Check .env file has valid GROQ_API_KEY

### Script Import Errors
```
ModuleNotFoundError: No module named 'orchestrator'
```
**Solution:** Run scripts from the `relaxbot` directory:
```bash
cd relaxbot
python scripts/interactive_chat.py
```

## What You'll See

### First Message (Bot)
```
"Welcome to your Guided Imagery VR experience. This module will help 
create vivid mental experiences by guiding you through a virtual environment. 
We hope this session will enhance relaxation, focus and wellbeing through 
visualization."
```

### Emotion Detection
```
[Classifier]
  Intent: start_breathing
  Emotion: calm
  Confidence: 85%
```

### Bot Response
```
"That's wonderful! Let's begin with some deep, relaxing breaths. 
Find a comfortable position and close your eyes if you're ready."
```

## Next Steps

After successful testing:

1. **Customize therapeutic scripts** - Edit library item bodies
2. **Add more processes** - Create different therapeutic flows
3. **Connect to UI** - Build web interface using the API
4. **Track outcomes** - Store session results and patient feedback
5. **Enhance classification** - Use advanced NLP models

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Input                            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          Session Manager (Orchestrator)                  │
├─────────────────────────────────────────────────────────┤
│ • Load session from database                            │
│ • Apply classifier (emotion/intent detection)           │
│ • Call orchestrator engine (state machine)              │
│ • Retrieve context with RAG                            │
│ • Generate response with LLM                           │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Classifier │  │ Orchestrator  │  │ RAG        │
    ├────────┤  ├────────┤  ├────────┤
    │ Intent  │  │ State  │  │ Library │
    │ Emotion │  │ Transition  │  │ Scripts │
    └────────┘  └────────┘  └────────┘
         │           │           │
         └───────────┼───────────┘
                     │
         ┌───────────▼───────────┐
         │   LLM Generator       │
         │   (Groq API)          │
         └───────────┬───────────┘
                     │
    ┌────────────────▼────────────────┐
    │      Personalized Response      │
    └─────────────────────────────────┘
```

## Success Indicators

When everything is working:

✅ Database cleanup runs without errors
✅ Sample data creates 6 states and 1 process
✅ Interactive chat starts and shows bot's first message
✅ Your messages are classified with emotion/intent
✅ Bot responds with therapeutic content
✅ State transitions happen automatically
✅ Conversation continues through all 6 steps

## Ready to Begin?

Run this now:
```bash
cd E:\Chatbot-Onco-ojaska labs\relaxbot
python scripts/interactive_chat.py
```

Good luck! 🧘‍♀️

