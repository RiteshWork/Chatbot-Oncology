# Therapeutic Chatbot - Setup and Testing Guide

## Overview
This guide walks you through setting up the database and testing the complete therapeutic chatbot flow with the Guided Imagery process.

## Prerequisites
- PostgreSQL running on localhost:5555
- Python 3.10+
- Required packages: `pip install -r requirements.txt`
- Groq API key configured in `.env` file

## Current Setup Status

### Database Configuration
- **Connection:** `postgresql+psycopg://postgres:root@localhost:5555/chatbot_oncology`
- **Already Configured:** .env file has GROQ_API_KEY set

### Therapeutic Flow (Implemented)
The system now implements a complete 6-step guided imagery session:

1. **Step 1: Introduction** - Welcome and overview of the VR experience
2. **Step 2: Deep Breathing** - Guided breathing exercises
3. **Step 3: Observe Your Breath** - Using So/Hum technique for natural breathing
4. **Step 4: Countdown** - Visualization counting down from 10 to 1
5. **Step 5: Safe Place** - Guided imagery to a healing, safe location
6. **Step 7: Hindsight & Closing** - Recollection and affirmation

### Components Integrated

#### 1. **Orchestrator Engine** (`orchestrator/engine.py`)
- Manages state transitions based on process definitions
- Loads sessions and their current state
- Determines next state based on transitions

#### 2. **Session Manager** (`orchestrator/session_manager.py`)
- Coordinates between user input, classifier, and LLM
- Loads sessions from database
- Applies emotion/intent classification
- Calls RAG retriever for context
- Generates personalized responses with Groq LLM

#### 3. **Classifier** (`classifier/simple_classifier.py`)
- Analyzes user messages for emotion (calm/anxious)
- Detects intent (start_breathing, request_support, etc.)
- Provides confidence scores

#### 4. **RAG System** (`rag/retriever.py`)
- Retrieves relevant library items based on current state
- Extracts therapeutic guidelines based on emotional state
- Provides session history context

#### 5. **LLM Generator** (`rag/llm_generator.py`)
- Uses Groq API (mixtral-8x7b-32768)
- Generates personalized therapeutic responses
- Falls back to library content if API fails
- System prompt includes therapeutic guidelines

## Step-by-Step Setup and Testing

### Step 1: Clean Up the Database

Run the cleanup script to remove old data:

```bash
cd relaxbot
python scripts/cleanup_db.py
```

Expected output:
```
================================================================================
CLEANING UP DATABASE
================================================================================

[1] Deleting sessions...
  Deleted X sessions
[2] Deleting processes...
  Deleted X processes
[3] Deleting states...
  Deleted X states
[4] Deleting library items...
  Deleted X library items

================================================================================
DATABASE CLEANUP COMPLETE
================================================================================
```

### Step 2: Create Sample Data with Therapeutic Scripts

Run the sample data creation script:

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
    Flow: Intro → Breathing → Observation → Countdown → Safe Place → Hindsight

[3] Creating Library Items...
  Created 6 library items

================================================================================
SUCCESS! CALM FLOW PROCESS CREATED
================================================================================
States: 7
Process: 1 (guided_imagery_v1)
Library Items: 6
```

### Step 3: Start the FastAPI Server (Optional - for API testing)

In one terminal:

```bash
python -m uvicorn api.app:app --reload --port 8000
```

The API will be available at:
- Health check: `http://localhost:8000/health`
- Create session: `POST http://localhost:8000/sessions`
- Chat endpoint: `POST http://localhost:8000/chat`

### Step 4: Run Interactive Chat (Main Testing)

In another terminal:

```bash
python scripts/interactive_chat.py
```

This will:
1. Create a new session automatically
2. Bot sends first message from the Introduction state
3. You respond naturally
4. System classifies your emotion/intent
5. LLM generates personalized response
6. Conversation continues through all states
7. End with "exit", "quit", or "bye"

Example session flow:

```
RELAXBOT INTERACTIVE CONVERSATION
This demonstrates the complete flow:
1. Create session
2. Bot presents intro
3. You respond
4. Classifier analyzes your emotion
5. LLM generates personalized response
6. Continue through therapeutic states

STEP 1: Creating session...
✓ Session created: [uuid]
  Patient: interactive_user
  Process: Calm (7-state therapeutic flow)

STEP 2: Bot sends first message...
Bot: [Introduction script from Step 1]
[Current State: Step 1: Introduction]

STEP 3: Your turn - respond to the bot...
You: I'm ready, let's begin
[Processing...]
  Intent: start_breathing
  Emotion: calm
  Confidence: 85%

Bot: [Personalized response using RAG + Groq LLM]

[Continue exchanging messages...]
```

## Expected Behavior

### Message Processing Pipeline

For each user message:

1. **Classifier** analyzes emotion and intent
   - Example: "I'm feeling anxious" → emotion: "anxious", intent: "request_support"

2. **Orchestrator** checks state transitions
   - Moves to next state if transition conditions are met
   - Current state: Step 2 → Next state: Step 3

3. **RAG Retriever** gathers context
   - Gets library items for current state
   - Extracts therapeutic guidelines based on emotion
   - Retrieves session history

4. **LLM Generator** creates personalized response
   - Uses Groq API with therapeutic system prompt
   - Incorporates emotional guidelines
   - Generates warm, empathetic response

5. **Session Manager** returns complete response
   - Session ID, current state, generated response
   - Available library items, message count

### State Transitions

The flow automatically progresses:

```
User says something
    ↓
Classifier detects emotion
    ↓
Orchestrator evaluates transitions
    ↓
If emotion = "calm" → move to next state
If emotion = "anxious" → stay in current state, provide support
    ↓
RAG retrieves context for new state
    ↓
LLM generates response
    ↓
Response returned to user
```

## Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: connection failed
```
**Solution:** Ensure PostgreSQL is running on localhost:5555

### Groq API Error
```
Error generating response: [API Error]
```
**Solution:** 
- Verify GROQ_API_KEY is set in `.env`
- Check API key is valid
- System will fall back to library content

### State Not Transitioning
**Check:**
1. Condition evaluation (should be "True" not "true")
2. Session exists and is loaded
3. Orchestrator is receiving correct classifier output

### Library Items Not Appearing
**Check:**
1. Run `cleanup_db.py` then `create_sample_data.py`
2. Verify library items exist: query database or check `library_items` table

## API Endpoints (Optional)

### Create Session
```bash
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "test_user", "process_code": "guided_imagery_v1"}'
```

Response:
```json
{
  "success": true,
  "session_id": "uuid",
  "current_state": {
    "state_id": "uuid",
    "state_code": "guided_intro",
    "state_name": "Step 1: Introduction"
  },
  "content": [...]
}
```

### Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "uuid", "message": "I'm ready to begin"}'
```

Response:
```json
{
  "success": true,
  "session_id": "uuid",
  "current_state": {...},
  "llm_response": "Welcome to your guided journey...",
  "message_count": 1,
  "content": [...]
}
```

## Next Steps

After testing the interactive chat:

1. **Verify all 6 states work correctly**
2. **Check emotional classification works**
3. **Ensure LLM generates appropriate responses**
4. **Test state transitions between steps**
5. **Review library items are presented correctly**

## Files Summary

| File | Purpose |
|------|---------|
| `scripts/cleanup_db.py` | Clears old data from database |
| `scripts/create_sample_data.py` | Populates database with therapeutic process |
| `scripts/interactive_chat.py` | Interactive conversation testing |
| `orchestrator/session_manager.py` | Main orchestration layer |
| `orchestrator/engine.py` | State machine engine |
| `classifier/simple_classifier.py` | Emotion/intent classification |
| `rag/retriever.py` | Context retrieval system |
| `rag/llm_generator.py` | Groq-based response generation |
| `api/app.py` | FastAPI endpoints |

