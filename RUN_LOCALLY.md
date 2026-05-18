# ⚠️ IMPORTANT: Run These Scripts Locally

The cleanup and sample data scripts must be run on **your local machine** where PostgreSQL is running on localhost:5555.

The scripts will NOT work in the sandbox environment because your PostgreSQL server is on your local machine.

## Step-by-Step Instructions

### 1. Open PowerShell or Command Prompt

Open a terminal on your local machine (Windows Command Prompt or PowerShell).

### 2. Navigate to the Project

```bash
cd "E:\Chatbot-Onco-ojaska labs\relaxbot"
```

Make sure you can see the `scripts` folder.

### 3. Verify Python Environment

Ensure you're using the correct Python environment:

```bash
python --version
# Should be Python 3.10 or higher
```

If you have a virtual environment, activate it:

```bash
# Windows
.\venv\Scripts\activate

# Or if using relaxbot-py3.13
# Make sure you're already in that environment
```

### 4. Verify PostgreSQL is Running

Before running the scripts, make sure PostgreSQL is running:

```bash
# Test connection
psql -h localhost -p 5555 -U postgres -d chatbot_oncology
```

If you get a password prompt, enter: `root`

If the connection works, you'll see a prompt like:
```
chatbot_oncology=#
```

Then type `\q` to exit.

### 5. Run Cleanup Script

```bash
python scripts/cleanup_db.py
```

**Expected output:**
```
================================================================================
CLEANING UP DATABASE
================================================================================

[1] Deleting sessions...
  Deleted 0 sessions
[2] Deleting processes...
  Deleted 0 processes
[3] Deleting states...
  Deleted 0 states
[4] Deleting library items...
  Deleted 0 library items

================================================================================
DATABASE CLEANUP COMPLETE
================================================================================
```

(First time will show "Deleted 0" of everything - that's fine, the database is empty)

### 6. Run Create Sample Data Script

```bash
python scripts/create_sample_data.py
```

**Expected output:**
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

This is the PROCESS TEMPLATE. Sessions will be created at runtime.
================================================================================
```

### 7. Run Interactive Chat

```bash
python scripts/interactive_chat.py
```

**Expected output:**
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
✓ Session created: [your-session-uuid]
  Patient: interactive_user
  Process: Calm (7-state therapeutic flow)

STEP 2: Bot sends first message...

Bot: Welcome to your Guided Imagery VR experience...

[Current State: Step 1: Introduction]

STEP 3: Your turn - respond to the bot...

You: [type your response here]
```

Then type natural responses and experience the therapeutic flow!

## Troubleshooting

### Error: "connection refused on port 5555"

**Problem:** PostgreSQL is not running

**Solution:** Start PostgreSQL

#### Windows
```bash
# If installed as service
net start postgresql-x64-15

# Or using pgAdmin
# Open pgAdmin and start the server from there

# Or check Services
# Open Services (services.msc) and start "postgresql-x64-15"
```

#### macOS
```bash
brew services start postgresql
```

#### Linux
```bash
sudo service postgresql start
```

### Error: "database 'chatbot_oncology' does not exist"

**Problem:** Database wasn't created yet

**Solution:** Create it using psql

```bash
psql -h localhost -p 5555 -U postgres

# In psql prompt:
CREATE DATABASE chatbot_oncology;
\q
```

### Error: "GROQ_API_KEY not set in environment"

**Problem:** Missing API key in .env file

**Solution:** Check your .env file

```bash
# View .env file
cat .env

# Should contain:
# GROQ_API_KEY=ygsk_ZTMVTxxV51InEFTn4b0nWGdyb3FYkUyCJmdv7W2m5LBGjBuW30ZU
```

If GROQ_API_KEY is missing, add it.

### Error: "No module named..."

**Problem:** Dependencies not installed

**Solution:** Install dependencies

```bash
pip install -r requirements.txt
```

## Summary of Commands

Run these **on your local machine**, **in order**:

```bash
# 1. Navigate to project
cd "E:\Chatbot-Onco-ojaska labs\relaxbot"

# 2. Clean database (removes old data)
python scripts/cleanup_db.py

# 3. Create sample data (populates with therapeutic flow)
python scripts/create_sample_data.py

# 4. Run interactive chat (test the chatbot)
python scripts/interactive_chat.py
```

## What Happens

1. **cleanup_db.py** removes any old sessions, processes, states, and library items from the database
2. **create_sample_data.py** creates:
   - 6 therapeutic states (Steps 1-5, 7)
   - 1 process (guided_imagery_v1)
   - 6 library items (therapeutic scripts)
3. **interactive_chat.py** starts an interactive conversation where:
   - Bot sends first message (introduction)
   - You respond naturally
   - System classifies your emotion
   - Bot generates personalized response
   - State automatically transitions to next step
   - Repeat through all 6 steps

## Expected Duration

- cleanup_db.py: ~1-2 seconds
- create_sample_data.py: ~2-3 seconds
- interactive_chat.py: 20-30 minutes (per session)

## After Scripts Run Successfully

Once all three scripts run without errors, your chatbot is ready to use!

You can:

1. **Run interactive_chat.py again** to start a new session
2. **Start the FastAPI server** to test REST endpoints:
   ```bash
   python -m uvicorn api.app:app --reload --port 8000
   ```

3. **Integrate with your frontend** using the REST API

## Important Notes

- ✅ Run all scripts from the `relaxbot` directory
- ✅ Run on your local machine where PostgreSQL is running
- ✅ PostgreSQL must be on localhost:5555
- ✅ Database must be named `chatbot_oncology`
- ✅ .env file must have GROQ_API_KEY set
- ✅ Use Python 3.10 or higher

## Still Having Issues?

1. Verify PostgreSQL is running: `psql -h localhost -p 5555 -U postgres`
2. Verify database exists: `psql -h localhost -p 5555 -U postgres -l | grep chatbot_oncology`
3. Verify Python dependencies: `pip list | grep sqlalchemy`
4. Check .env file has GROQ_API_KEY

If you get stuck, check the full documentation:
- `SETUP_AND_TEST.md` - Detailed setup guide
- `README.md` - Complete project overview
- `BOT_RESPONSES_BY_STEP.md` - What to expect at each step

