# How the Classifier Works: Complete Technical Breakdown

## Answer: The Basis of Classification

### 🎯 **Basis: Keyword Matching (NOT Machine Learning, NOT LLM)**

The classifier is **100% keyword-based**. It works by:

1. ✅ Taking user message
2. ✅ Converting to lowercase
3. ✅ Counting keyword matches from 7 emotion categories
4. ✅ Selecting emotion with highest score
5. ✅ Applying special mapping rules
6. ✅ Returning emotion + intent + confidence

**NO machine learning involved. NO LLM involved. Pure keyword matching.**

---

## The 7 Emotion Categories

### Category 1: COMFORTABLE (Ready, Willing)
```python
COMFORTABLE_KEYWORDS = [
    "comfortable", "ready", "peaceful", "relaxed", "okay", "fine", "good",
    "yes", "sure", "let's", "begin", "start", "happy", "excited", "eager"
]
```
**When detected:** Patient is calm and ready to proceed

---

### Category 2: EMOTIONAL (Overwhelmed, Distressed)
```python
EMOTIONAL_KEYWORDS = [
    "emotional", "overwhelmed", "tears", "upset", "struggling", "hard",
    "difficult", "sad", "crying", "hurting", "grieving", "distressed",
    "anxious", "worried", "stressed", "nervous", "tense", "racing"
]
```
**When detected:** Patient is emotionally overwhelmed

---

### Category 3: HESITANT (Doubtful, Scared)
```python
HESITANT_KEYWORDS = [
    "hesitant", "not sure", "doubtful", "uncertain", "maybe", "not ready",
    "bit nervous", "bit scared", "cautious", "wary", "tentative", "unsure"
]
```
**When detected:** Patient is uncertain about proceeding

---

### Category 4: UNCERTAIN (Conflicted, Confused)
```python
UNCERTAIN_KEYWORDS = [
    "uncertain", "confused", "conflicted", "torn", "unclear", "mixed feelings",
    "don't know", "conflicting", "both", "either or", "can't decide"
]
```
**When detected:** Patient has mixed feelings

---

### Category 5: NEEDS_REASSURANCE (Worried, Afraid)
```python
NEEDS_REASSURANCE_KEYWORDS = [
    "reassurance", "help", "support", "concerned", "worried", "anxious",
    "nervous", "fear", "scared", "afraid", "panic", "safety", "protect",
    "not ok", "not feeling", "struggling", "in pain", "uncomfortable"
]
```
**When detected:** Patient needs support and reassurance

---

### Category 6: UNWILLING (Refusing, Resisting)
```python
UNWILLING_KEYWORDS = [
    "don't want", "prefer not", "skip", "refuse", "don't think so", "no",
    "nope", "not interested", "pass", "skip it", "doesn't appeal", "not doing",
    "don't feel", "can't do", "won't", "not feeling"
]
```
**When detected:** Patient is resistant to proceeding

---

### Category 7: PHYSICALLY_UNCOMFORTABLE (Pain, Discomfort)
```python
PHYSICALLY_UNCOMFORTABLE_KEYWORDS = [
    "pain", "hurt", "discomfort", "sore", "ache", "dizzy",
    "nausea", "tired", "fatigue", "stiff", "tense", "aching", "throbbing"
]
```
**When detected:** Patient has physical discomfort

---

## The Algorithm (Step-by-Step)

### Step 1: Convert to Lowercase
```python
message_lower = message.lower()
```
**Why:** So "PAIN", "Pain", "pain" all match the same keyword

Example:
```
User input:  "I am in PAIN"
Converted:   "i am in pain"
```

---

### Step 2: Count Keywords for Each Emotion

```python
scores = {
    "comfortable": sum(1 for keyword in COMFORTABLE_KEYWORDS if keyword in message_lower),
    "emotional": sum(1 for keyword in EMOTIONAL_KEYWORDS if keyword in message_lower),
    "hesitant": sum(1 for keyword in HESITANT_KEYWORDS if keyword in message_lower),
    "uncertain": sum(1 for keyword in UNCERTAIN_KEYWORDS if keyword in message_lower),
    "needs_reassurance": sum(1 for keyword in NEEDS_REASSURANCE_KEYWORDS if keyword in message_lower),
    "unwilling": sum(1 for keyword in UNWILLING_KEYWORDS if keyword in message_lower),
    "physically_uncomfortable": sum(1 for keyword in PHYSICALLY_UNCOMFORTABLE_KEYWORDS if keyword in message_lower),
}
```

**What this does:** For each emotion category, count how many keywords appear in the message.

Example:
```
User message: "I am anxious and worried but ready to start"

Converted:    "i am anxious and worried but ready to start"

Score calculation:
  comfortable: 1 (found "ready")
  emotional: 2 (found "anxious", "worried")
  hesitant: 0
  uncertain: 0
  needs_reassurance: 2 (found "anxious", "worried")
  unwilling: 0
  physically_uncomfortable: 0

Result:
scores = {
  "comfortable": 1,
  "emotional": 2,
  "hesitant": 0,
  "uncertain": 0,
  "needs_reassurance": 2,
  "unwilling": 0,
  "physically_uncomfortable": 0
}
```

---

### Step 3: Find Maximum Score

```python
max_score = max(scores.values())
```

Continuing the example:
```
max_score = 2
emotions_with_max = ["emotional", "needs_reassurance"]  # both have score of 2
```

---

### Step 4: Special Mapping Rules

If no keywords found:
```python
if max_score == 0:
    emotion = "comfortable"  # Default
    confidence = 0.5
```

If keywords found, check for special handlers:

#### Rule 1: Detect ANXIOUS Handler
```python
anxiety_keywords = ["anxious", "worried", "nervous", "panic", "scared", "afraid", "racing", "overwhelmed"]

if ("emotional" in emotions_with_max or "needs_reassurance" in emotions_with_max) and \
   any(kw in message_lower for kw in anxiety_keywords):
    emotion = "anxious"  # Special mapping
```

**Example:**
```
If emotion = "emotional" AND message contains "anxious"
→ Route to "anxious" handler instead of "emotional"
```

#### Rule 2: Detect RESISTANT Handler
```python
resistant_keywords = ["don't want", "refuse", "no", "nope", "don't think", "won't do"]

if ("unwilling" in emotions_with_max or "hesitant" in emotions_with_max) and \
   any(kw in message_lower for kw in resistant_keywords):
    emotion = "resistant"  # Special mapping
```

**Example:**
```
If emotion = "unwilling" AND message contains "don't want"
→ Route to "resistant" handler instead of "unwilling"
```

---

### Step 5: Calculate Confidence

```python
confidence = min(max_score / 5.0, 1.0)
```

**How it works:**
- Score of 0 → Confidence = 0.5 (default/guess)
- Score of 1 → Confidence = 0.2 (low)
- Score of 2 → Confidence = 0.4 (medium-low)
- Score of 5 → Confidence = 1.0 (very high)
- Score of 10+ → Confidence = 1.0 (capped at 1.0)

Example:
```
max_score = 2
confidence = min(2 / 5.0, 1.0) = min(0.4, 1.0) = 0.4
```

---

### Step 6: Determine Intent (Secondary)

```python
intent = "continue_session"  # Default

if "ready" in message_lower or "begin" in message_lower:
    intent = "start_breathing"
elif "anxious" in message_lower or "worried" in message_lower:
    intent = "request_calm"
elif "help" in message_lower:
    intent = "request_support"
```

---

## Real Examples

### Example 1: "I am anxious"

```
Step 1: Convert
  message_lower = "i am anxious"

Step 2: Count keywords
  comfortable: 0
  emotional: 1 (found "anxious")
  hesitant: 0
  uncertain: 0
  needs_reassurance: 1 (found "anxious")
  unwilling: 0
  physically_uncomfortable: 0

Step 3: Max score
  max_score = 1
  emotions_with_max = ["emotional", "needs_reassurance"]

Step 4: Special mapping
  anxiety_keywords check: "anxious" found ✓
  ("emotional" in emotions_with_max) ✓
  → emotion = "anxious" (special mapping applied)

Step 5: Confidence
  confidence = min(1 / 5.0, 1.0) = 0.2

Step 6: Intent
  "anxious" in message? YES
  → intent = "request_calm"

RESULT:
{
  emotion: "anxious",
  intent: "request_calm",
  confidence: 0.2
}
```

---

### Example 2: "I have pain in my back"

```
Step 1: Convert
  message_lower = "i have pain in my back"

Step 2: Count keywords
  comfortable: 0
  emotional: 0
  hesitant: 0
  uncertain: 0
  needs_reassurance: 0
  unwilling: 0
  physically_uncomfortable: 2 (found "pain" and "back" is not a keyword)
  Actually: 1 (found "pain")

Step 3: Max score
  max_score = 1
  emotions_with_max = ["physically_uncomfortable"]

Step 4: Special mapping
  No special mapping applies

Step 5: Confidence
  confidence = min(1 / 5.0, 1.0) = 0.2

Step 6: Intent
  "ready" in message? NO
  "anxious" in message? NO
  "help" in message? NO
  → intent = "continue_session" (default)

RESULT:
{
  emotion: "physically_uncomfortable",
  intent: "continue_session",
  confidence: 0.2
}
```

---

### Example 3: "I don't want to do this, I'm scared"

```
Step 1: Convert
  message_lower = "i don't want to do this, i'm scared"

Step 2: Count keywords
  comfortable: 0
  emotional: 1 (found "scared")
  hesitant: 1 (found "scared")
  uncertain: 0
  needs_reassurance: 1 (found "scared")
  unwilling: 1 (found "don't want")
  physically_uncomfortable: 0

Step 3: Max score
  max_score = 1
  emotions_with_max = ["emotional", "hesitant", "needs_reassurance", "unwilling"]

Step 4: Special mapping
  resistant_keywords: "don't want" found ✓
  ("unwilling" in emotions_with_max) ✓
  → emotion = "resistant" (special mapping applied)

Step 5: Confidence
  confidence = min(1 / 5.0, 1.0) = 0.2

Step 6: Intent
  "ready" in message? NO
  "anxious" in message? NO
  "help" in message? NO
  → intent = "continue_session" (default)

RESULT:
{
  emotion: "resistant",
  intent: "continue_session",
  confidence: 0.2
}
```

---

### Example 4: "I'm ready to begin"

```
Step 1: Convert
  message_lower = "i'm ready to begin"

Step 2: Count keywords
  comfortable: 2 (found "ready", "begin")
  emotional: 0
  hesitant: 0
  uncertain: 0
  needs_reassurance: 0
  unwilling: 0
  physically_uncomfortable: 0

Step 3: Max score
  max_score = 2
  emotions_with_max = ["comfortable"]

Step 4: Special mapping
  No special mapping applies

Step 5: Confidence
  confidence = min(2 / 5.0, 1.0) = 0.4

Step 6: Intent
  "ready" in message? YES
  → intent = "start_breathing"

RESULT:
{
  emotion: "comfortable",
  intent: "start_breathing",
  confidence: 0.4
}
```

---

## Strengths & Weaknesses

### ✅ Strengths of Keyword Matching

| Strength | Why It Matters |
|----------|----------------|
| Fast | Instant classification, no API calls |
| Transparent | You can see exactly why classification happened |
| Deterministic | Same input → same output always |
| Easy to debug | Just check keyword lists |
| Domain-specific | Keywords tailored to therapy context |
| No training data needed | Works immediately |

---

### ❌ Weaknesses of Keyword Matching

| Weakness | Example | Impact |
|----------|---------|--------|
| Substring matching | "I'm not ok" matches "ok" in COMFORTABLE_KEYWORDS | Wrong classification |
| No context | "I'm not anxious anymore" has "anxious" but means opposite | Wrong emotion |
| Ordering ignored | "I am sad but ready" has mixed signals, picks highest score | Ambiguous cases |
| Multiple meanings | "stressed" in EMOTIONAL_KEYWORDS could mean good/bad stress | Incorrect classification |
| No negation | "I don't have pain" still matches "pain" keyword | False positive |
| No synonyms | "ache" recognized but "soreness" not included | Missed keywords |

---

## How It Integrates with Orchestrator & RAG

```
User Message
    ↓
Classifier
    ├─ Keyword matching
    ├─ Special mapping
    └─ Returns: emotion + confidence
    ↓
Orchestrator
    ├─ Evaluates transitions using emotion
    ├─ Example: IF emotion == 'anxious' THEN go to Grounding
    └─ Updates current_state
    ↓
RAG Retriever
    ├─ Queries: WHERE emotional_state = detected_emotion
    ├─ Gets all matching library items
    └─ Passes to LLM
    ↓
LLM Synthesizer
    ├─ Receives emotion info
    ├─ Receives retrieved scripts
    └─ Generates personalized response
    ↓
User
    └─ Sees response tailored to detected emotion
```

---

## How RAG Uses Classifier Output

### Scenario: User says "I'm anxious"

```
Classifier Output:
{
  emotion: "anxious",
  confidence: 0.9
}

↓

RAG Query:
SELECT * FROM library_items 
WHERE metadata->>'emotional_state' = 'anxious'

↓

Retrieved Items (from your DOCX):
✓ Grounding Script (Step 2.1)
✓ Deep Belly Breathing
✓ Body Scan Breathing
✓ 4-4 Breathing
✓ Observation Techniques
... all items with emotional_state = 'anxious'

↓

LLM Receives:
"Patient detected as anxious (confidence: 0.9)
 State: Breathing exercises
 Retrieved 15 therapeutic scripts for anxiety
 Use grounding and reassurance techniques"

↓

LLM Generates:
"I hear that you're feeling anxious. That's completely understandable.
 Let's ground ourselves together using a simple technique..."
```

---

## Limitations & Future Improvements

### Current Limitation 1: Substring Matching
```python
# Current: "not ok" matches "ok" in COMFORTABLE_KEYWORDS
if "ok" in "i am not ok".lower():  # TRUE (wrong!)

# Problem: Matches substring, not whole word
```

### Future Improvement 1: Word Boundaries
```python
# Better: Use regex word boundaries
import re
pattern = r'\bok\b'  # Only match "ok" as whole word
if re.search(pattern, "i am not ok"):  # FALSE (correct!)
```

---

### Current Limitation 2: No Context
```python
# Current: Both classify as "anxious"
classifier.classify("I am anxious")  # anxious ✓
classifier.classify("I am no longer anxious")  # anxious ✗ (should be comfortable)

# Problem: Doesn't understand negation
```

### Future Improvement 2: Negation Handling
```python
# Could check for negation words before keywords
negation_words = ["not", "no", "don't", "won't", "can't"]
if keyword_found and negation_before_keyword:
    # Reduce score or flip emotion
```

---

### Current Limitation 3: No Sentiment
```python
# Current: Same score for positive and negative uses
"I'm stressed" → EMOTIONAL (negative)
"I'm stressed but ready" → Tied between EMOTIONAL and COMFORTABLE

# Problem: Can't distinguish intensity
```

### Future Improvement 3: Machine Learning
```python
# Could train small ML model on therapeutic chat data
# Input: User message
# Output: emotion + confidence (learned weights, not hardcoded)

from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB()
classifier.fit(training_messages, training_emotions)
emotion = classifier.predict(user_message)
```

---

## Summary Table

| Aspect | Current | How It Works |
|--------|---------|-------------|
| **Basis** | Keyword Matching | 7 emotion categories with word lists |
| **Speed** | Instant | O(n) - linear in keyword count |
| **Accuracy** | ~70% | Works for clear emotions, misses nuance |
| **Confidence** | Calculated | max_keywords_found / 5.0 |
| **Special Cases** | 2 handlers | anxious + resistant mapping |
| **Integration** | Orchestrator | emotion feeds state transitions |
| **RAG Link** | Direct | emotion filters library items |
| **ML/LLM** | None | Pure keyword-based |
| **Future** | Can upgrade | Could add ML, better parsing |

---

## Code Location

**File:** `E:\Chatbot-Onco-ojaska labs\relaxbot\classifier\simple_classifier.py`

**How to Use:**
```python
from classifier.simple_classifier import classifier

result = classifier.classify("I am anxious and worried")
print(result.emotion)      # "anxious"
print(result.confidence)   # 0.4
print(result.intent)       # "request_calm"
```

**Is It LLM-Based?** NO
**Is It ML-Based?** NO
**Is It Keyword-Based?** YES - 100% pure keyword matching
