"""
scripts/test_classifier.py
Test the updated 7-state classifier.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classifier.simple_classifier import classifier

# Test messages for each emotional state
test_messages = {
    "comfortable": [
        "I'm feeling good and ready to begin",
        "Yes, let's start. I'm peaceful and relaxed",
        "I'm excited and prepared for this"
    ],
    "emotional": [
        "I'm feeling really overwhelmed and emotional right now",
        "This is making me cry and I'm struggling",
        "I'm so upset and distressed"
    ],
    "hesitant": [
        "I'm not really sure about this",
        "I'm a bit nervous, but maybe",
        "I'm hesitant and doubtful"
    ],
    "uncertain": [
        "I have mixed feelings about this",
        "I'm conflicted and confused",
        "I don't know what to think"
    ],
    "needs_reassurance": [
        "I'm worried and anxious about this",
        "I'm scared and need help",
        "I'm panicking, please help me"
    ],
    "unwilling": [
        "I don't want to do this",
        "No, I refuse to participate",
        "I'm not interested in this"
    ],
    "physically_uncomfortable": [
        "I'm in pain and feeling uncomfortable",
        "I'm dizzy and nauseous",
        "I'm exhausted and my back aches"
    ]
}

print("=" * 80)
print("CLASSIFIER TEST - 7 EMOTIONAL STATES")
print("=" * 80)

for expected_emotion, messages in test_messages.items():
    print(f"\n[Testing: {expected_emotion.upper()}]")
    print("-" * 80)

    for message in messages:
        result = classifier.classify(message)
        match = "✓" if result.emotion == expected_emotion else "✗"
        print(f"{match} Message: \"{message}\"")
        print(f"  → Detected: {result.emotion} (confidence: {result.confidence:.0%})")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
