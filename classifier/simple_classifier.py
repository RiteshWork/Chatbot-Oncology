"""
classifier/simple_classifier.py
Simple emotion/intent classifier based on keyword matching.

For now, uses basic heuristics. Can be replaced with ML model later.
"""

import logging
from orchestrator.schemas import ClassifierOutput

logger = logging.getLogger(__name__)


class SimpleClassifier:
    """Simple keyword-based emotion classifier for 7 emotional states."""

    # 1. Comfortable & Ready
    COMFORTABLE_KEYWORDS = [
        "comfortable", "ready", "peaceful", "relaxed", "okay", "fine", "good",
        "yes", "sure", "let's", "begin", "start", "happy", "excited", "eager"
    ]

    # 2. Emotional/Overwhelmed
    EMOTIONAL_KEYWORDS = [
        "emotional", "overwhelmed", "tears", "upset", "struggling", "hard",
        "difficult", "sad", "crying", "hurting", "grieving", "distressed",
        "anxious", "worried", "stressed", "nervous", "tense", "racing"
    ]

    # 3. Hesitant/Doubtful
    HESITANT_KEYWORDS = [
        "hesitant", "not sure", "doubtful", "uncertain", "maybe", "not ready",
        "bit nervous", "bit scared", "cautious", "wary", "tentative", "unsure"
    ]

    # 4. Uncertain/Conflicted
    UNCERTAIN_KEYWORDS = [
        "uncertain", "confused", "conflicted", "torn", "unclear", "mixed feelings",
        "don't know", "conflicting", "both", "either or", "can't decide"
    ]

    # 5. Needs Reassurance
    NEEDS_REASSURANCE_KEYWORDS = [
        "reassurance", "help", "support", "concerned", "worried", "anxious",
        "nervous", "fear", "scared", "afraid", "panic", "safety", "protect",
        "not ok", "not feeling", "struggling", "in pain", "uncomfortable"
    ]

    # 6. Unwilling/Refusing
    UNWILLING_KEYWORDS = [
        "don't want", "prefer not", "skip", "refuse", "don't think so", "no",
        "nope", "not interested", "pass", "skip it", "doesn't appeal", "not doing",
        "don't feel", "can't do", "won't", "not feeling"
    ]

    # 7. Physically Uncomfortable
    PHYSICALLY_UNCOMFORTABLE_KEYWORDS = [
        "pain", "hurt", "discomfort", "sore", "ache", "dizzy",
        "nausea", "tired", "fatigue", "stiff", "tense", "aching", "throbbing"
    ]

    @staticmethod
    def classify(message: str) -> ClassifierOutput:
        """
        Classify a user message to determine emotional state and intent.

        Args:
            message: User's message

        Returns:
            ClassifierOutput with intent, emotion, and confidence
        """
        message_lower = message.lower()

        # Count keyword matches for all 7 emotional states
        scores = {
            "comfortable": sum(1 for keyword in SimpleClassifier.COMFORTABLE_KEYWORDS
                              if keyword in message_lower),
            "emotional": sum(1 for keyword in SimpleClassifier.EMOTIONAL_KEYWORDS
                            if keyword in message_lower),
            "hesitant": sum(1 for keyword in SimpleClassifier.HESITANT_KEYWORDS
                           if keyword in message_lower),
            "uncertain": sum(1 for keyword in SimpleClassifier.UNCERTAIN_KEYWORDS
                            if keyword in message_lower),
            "needs_reassurance": sum(1 for keyword in SimpleClassifier.NEEDS_REASSURANCE_KEYWORDS
                                    if keyword in message_lower),
            "unwilling": sum(1 for keyword in SimpleClassifier.UNWILLING_KEYWORDS
                            if keyword in message_lower),
            "physically_uncomfortable": sum(1 for keyword in SimpleClassifier.PHYSICALLY_UNCOMFORTABLE_KEYWORDS
                                           if keyword in message_lower),
        }

        # Determine emotion state (highest-scoring state)
        max_score = max(scores.values())
        if max_score == 0:
            # Default to comfortable if no strong signals
            emotion = "comfortable"
            confidence = 0.5
        else:
            # Find the emotion with the highest score
            emotions_with_max = [state for state, score in scores.items() if score == max_score]
            emotion = emotions_with_max[0]

            # Special mapping: detect "anxious" handler trigger
            # If highest score is emotional but message has anxiety keywords, route to anxiety handler
            anxiety_keywords = ["anxious", "worried", "nervous", "panic", "scared", "afraid", "racing", "overwhelmed"]
            if ("emotional" in emotions_with_max or "needs_reassurance" in emotions_with_max) and \
               any(kw in message_lower for kw in anxiety_keywords):
                emotion = "anxious"

            # Special mapping: detect "resistant" handler trigger
            resistant_keywords = ["don't want", "refuse", "no", "nope", "don't think", "won't do"]
            if ("unwilling" in emotions_with_max or "hesitant" in emotions_with_max) and \
               any(kw in message_lower for kw in resistant_keywords):
                emotion = "resistant"

            confidence = min(max_score / 5.0, 1.0)  # Normalize to 0-1

        # Determine intent based on emotion and keywords (keeping existing logic)
        intent = "continue_session"  # Default intent
        if "ready" in message_lower or "begin" in message_lower:
            intent = "start_breathing"
        elif "anxious" in message_lower or "worried" in message_lower:
            intent = "request_calm"
        elif "help" in message_lower:
            intent = "request_support"

        logger.info(f"[Classifier] Message: '{message[:50]}...' → intent={intent}, emotion={emotion} (confidence: {confidence:.2f})")

        return ClassifierOutput(
            intent=intent,
            emotion=emotion,
            stress_level=None,
            confidence=confidence
        )


# Singleton instance
classifier = SimpleClassifier()
