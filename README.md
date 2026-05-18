# Therapeutic Chatbot for Oncology Patients

A sophisticated AI-powered therapeutic chatbot designed for oncology patients, featuring guided imagery sessions with emotion-aware responses powered by RAG + LLM architecture.

## 🎯 Overview

This chatbot implements a complete therapeutic flow (Steps 1-5 and 7) with:

- **State-Machine Orchestration:** Guided progression through 6 therapeutic steps
- **Emotion Classification:** AI-based detection of patient emotional state
- **RAG System:** Context-aware information retrieval for therapeutic guidelines
- **LLM Integration:** Personalized responses using Groq API
- **Interactive Sessions:** Bot-initiated conversations with natural dialogue flow

## 📊 Therapeutic Flow

```
Step 1: Introduction (Session Overview)
    ↓
Step 2: Deep Breathing (Physical Relaxation)
    ↓
Step 3: Observe Your Breath (So/Hum Technique)
    ↓
Step 4: Countdown (Visualization 10→1)
    ↓
Step 5: Safe Place (Healing Visualization)
    ↓
Step 7: Hindsight & Closing (Reflection & Affirmation)
```

## 🚀 Quick Start

### Prerequisites
- PostgreSQL running on localhost:5555
- Python 3.10+
- Groq API key in `.env`

### 3-Step Setup

**1. Clean Database**
```bash
cd E:\Chatbot-Onco-ojaska labs\relaxbot
python scripts/cleanup_db.py
```

**2. Create Sample Data**
```bash
python scripts/create_sample_data.py
```

**3. Run Interactive Chat**
```bash
python scripts/interactive_chat.py
```

Then type your responses to the bot and watch the therapeutic flow unfold!

## 🏗️ Architecture

### Core Components

#### 1. **Session Manager** (`orchestrator/session_manager.py`)
Central coordinator that:
- Loads sessions from database
- Applies emotion/intent classification
- Orchestrates state transitions
- Retrieves therapeutic context (RAG)
- Generates personalized responses (LLM)
- Assembles responses for user

#### 2. **Orchestrator Engine** (`orchestrator/engine.py`)
State machine that:
- Manages current state tracking
- Evaluates transition conditions
- Routes to next state
- Returns orchestrated response with context

#### 3. **Classifier** (`classifier/simple_classifier.py`)
Analyzes user messages to extract:
- **Emotion:** calm, anxious, neutral
- **Intent:** start_breathing, request_support, etc.
- **Confidence:** 0.0-1.0 confidence score

#### 4. **RAG System** (`rag/retriever.py`)
Context retrieval that provides:
- Library items (therapeutic scripts)
- Emotional guidelines
- Session history
- Therapeutic recommendations

#### 5. **LLM Generator** (`rag/llm_generator.py`)
Generates responses using:
- **Model:** Groq (mixtral-8x7b-32768)
- **System Prompt:** Therapeutic guidelines + emotional context
- **Fallback:** Library scripts if API fails

#### 6. **FastAPI** (`api/app.py`)
REST endpoints:
- `POST /sessions` - Create session
- `POST /chat` - Process message
- `GET /health` - Health check

### Data Flow

```
User Message
    ↓
Session Manager
    ├→ Load Session (DB)
    ├→ Classifier (emotion/intent)
    ├→ Orchestrator (state → next state)
    ├→ RAG Retriever (context)
    └→ LLM Generator (response)
    ↓
Response to User
```

## 📁 Project Structure

```
relaxbot/
├── api/
│   ├── app.py              # FastAPI application
│   ├── schemas.py          # Request/response schemas
│   └── __init__.py
├── classifier/
│   ├── simple_classifier.py # Emotion/intent detection
│   └── __init__.py
├── db.py                   # Database connection
├── models/
│   ├── sessions.py         # Session ORM model
│   ├── processes.py        # Process ORM model
│   ├── states.py           # State ORM model
│   ├── library.py          # Library items ORM
│   └── __init__.py
├── orchestrator/
│   ├── engine.py           # State machine orchestrator
│   ├── session_manager.py  # Main coordinator
│   ├── schemas.py          # Orchestrator schemas
│   ├── session_manager_schemas.py
│   └── __init__.py
├── rag/
│   ├── retriever.py        # Context retrieval
│   ├── llm_generator.py    # LLM-based generation
│   └── __init__.py
├── scripts/
│   ├── cleanup_db.py       # Database cleanup
│   ├── create_sample_data.py # Populate DB
│   ├── interactive_chat.py  # Interactive testing
│   └── test_*.py           # Test scripts
├── services/
│   ├── session_service.py  # Session creation
│   └── __init__.py
├── .env                    # Environment config
├── SETUP_AND_TEST.md       # Detailed setup guide
├── BOT_RESPONSES_BY_STEP.md # Step-by-step responses
├── QUICKSTART.md           # Quick reference
├── IMPLEMENTATION_CHECKLIST.md # What's implemented
└── README.md               # This file
```

## 🔄 Data Models

### Session
- `id` (UUID)
- `patient_id` (str)
- `process_id` (FK to Process)
- `current_state_id` (FK to State)
- `session_metadata` (JSON: messages, status)
- `started_at`, `updated_at`

### Process
- `id` (UUID)
- `code` (str, unique)
- `name` (str)
- `description` (str)
- `definition` (JSON: states, transitions)
- `is_active` (bool)

### State
- `id` (UUID)
- `code` (str)
- `name` (str)
- `description` (str)

### LibraryItem
- `id` (UUID)
- `kind` (str: "script", "affirmation")
- `title` (str)
- `body` (str)
- `item_metadata` (JSON)

## 🧠 How It Works

### 1. Session Creation
```python
session = SessionService.create_session(
    patient_id="user123",
    process_code="guided_imagery_v1"
)
# Session created with initial state = Step 1: Introduction
```

### 2. Bot Sends First Message
```
Bot: "Welcome to your Guided Imagery VR experience..."
```

### 3. User Responds
```
You: "I'm ready to begin"
```

### 4. Message Processing
```
Classifier → Intent: start_breathing, Emotion: calm
Orchestrator → Current: Step 1, Next: Step 2
RAG → Library items for Step 2, Calm guidelines
LLM → Generate warm, therapeutic response
```

### 5. Bot Responds with Support
```
Bot: "That's wonderful! Let's begin with some deep, relaxing breaths..."
```

### 6. State Transition
```
Session state changes: Step 1 → Step 2
```

### 7. Conversation Continues
```
Repeat steps 3-6 for all therapeutic states
```

## 📈 Response Generation

Bot responses are generated by:

1. **Extracting Context**
   - Current therapeutic state
   - Patient's emotional state
   - Conversation history

2. **Building System Prompt**
   ```
   You are a compassionate therapeutic chatbot.
   Current state: {state_name}
   Patient emotion: {emotion}
   Guidelines: {therapeutic_guidelines}
   ```

3. **Generating with Groq**
   - Model: mixtral-8x7b-32768
   - Temperature: 0.7 (balanced creativity)
   - Max tokens: 1024

4. **Fallback to Library**
   - If API fails, use library scripts
   - Ensures patient always gets response

## 🎓 Therapeutic Principles

Each response embodies:

- **Validation:** Acknowledge feelings without judgment
- **Empowerment:** Reinforce patient's agency and strength
- **Grounding:** Keep patient present and safe
- **Progression:** Structured therapeutic flow
- **Personalization:** Adapt to emotional state

## 🧪 Testing

### Interactive Chat (Recommended)
```bash
python scripts/interactive_chat.py
```

### API Testing
```bash
# Start server
python -m uvicorn api.app:app --reload

# Create session
curl -X POST http://localhost:8000/sessions \
  -d '{"patient_id": "test", "process_code": "guided_imagery_v1"}'

# Chat
curl -X POST http://localhost:8000/chat \
  -d '{"session_id": "...", "message": "I am ready"}'
```

## 🔧 Configuration

### Environment Variables (.env)
```
DATABASE_URL=postgresql+psycopg://postgres:root@localhost:5555/chatbot_oncology
GROQ_API_KEY=your_api_key_here
```

### Therapeutic Parameters
- **Emotions Recognized:** calm, anxious, neutral
- **Session Steps:** 6 (Steps 1-5, 7)
- **Session Duration:** 20-30 minutes
- **Response Style:** Warm, empathetic, supportive

## 📝 Key Features

✅ **Complete Therapeutic Flow**
- All 6 therapeutic steps implemented
- Actual scripts from therapists
- Emotion-aware progression

✅ **Intelligent Responses**
- LLM-generated personalized responses
- RAG-based context retrieval
- Therapeutic guidelines embedded

✅ **Robust System**
- Session persistence in database
- Emotion classification
- State machine validation
- Fallback mechanisms

✅ **Production-Ready**
- FastAPI REST endpoints
- Error handling
- Logging
- Database ORM
- Input validation

## 🚨 Troubleshooting

### Database Connection Error
**Solution:** Ensure PostgreSQL is running on localhost:5555
```bash
pg_ctl -D "path\to\data" start  # Windows
brew services start postgresql   # macOS
sudo service postgresql start   # Linux
```

### Groq API Error
**Solution:** Verify GROQ_API_KEY in .env
- Check API key is valid
- System falls back to library scripts if API fails

### Import Errors
**Solution:** Run scripts from `relaxbot` directory
```bash
cd relaxbot
python scripts/interactive_chat.py
```

## 📚 Documentation

- **`QUICKSTART.md`** - 3-step quick start guide
- **`SETUP_AND_TEST.md`** - Detailed setup instructions
- **`BOT_RESPONSES_BY_STEP.md`** - Exact responses for each step
- **`IMPLEMENTATION_CHECKLIST.md`** - What's implemented

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Advanced NLP models
- [ ] Branching therapy paths
- [ ] Outcome tracking
- [ ] Patient progress dashboard
- [ ] Mobile app integration

## 👥 For Developers

### Understanding the Flow
1. Read `BOT_RESPONSES_BY_STEP.md` for therapeutic context
2. Review `orchestrator/session_manager.py` for main flow
3. Check `rag/llm_generator.py` for response generation
4. Explore `api/app.py` for endpoint structure

### Adding Features
1. New therapeutic process? Update `create_sample_data.py`
2. New classifier logic? Modify `classifier/simple_classifier.py`
3. New API endpoint? Add to `api/app.py`
4. New database model? Update `models/` and create migration

### Testing Changes
```bash
# Run cleanup and sample data
python scripts/cleanup_db.py
python scripts/create_sample_data.py

# Test with interactive chat
python scripts/interactive_chat.py
```

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review relevant documentation file
3. Check error logs in terminal
4. Verify database connection and API keys

## 📄 License

This therapeutic chatbot is designed specifically for oncology patient support and should be used in conjunction with professional medical and psychological care.

---

**Ready to Start?**
```bash
cd E:\Chatbot-Onco-ojaska labs\relaxbot
python scripts/interactive_chat.py
```

Experience the full therapeutic flow now! 🧘‍♀️

