"""
responses.py
------------
Centralized response and intent-keyword dictionary for the rule-based chatbot.
Keeping all response data here (instead of inline in chatbot.py) keeps the
control logic clean and makes the bot's vocabulary easy to extend.
"""

# Patterns that, when found in user input, are treated as a greeting.
GREETING_PATTERNS: list[str] = [
    "hello", "hi", "hey", "good morning", "good afternoon",
    "good evening", "whats up", "yo", "greetings",
]

GREETING_RESPONSES: list[str] = [
    "Hello there! How can I help you today?",
    "Hi! What can I do for you?",
    "Hey! Great to see you. Ask me anything.",
    "Greetings! I'm ready to assist.",
]

# Patterns that indicate the user wants to end the conversation.
FAREWELL_PATTERNS: list[str] = [
    "bye", "goodbye", "see you", "later", "take care", "farewell",
]

FAREWELL_RESPONSES: list[str] = [
    "Goodbye! Have a wonderful day.",
    "See you soon! Take care.",
    "Bye! Feel free to come back anytime.",
    "Farewell! It was nice chatting with you.",
]

UNKNOWN_RESPONSES: list[str] = [
    "I'm not sure I understand. Could you rephrase that?",
    "Hmm, that's outside what I currently know. Try asking differently.",
    "I don't have an answer for that yet, but I'm learning!",
    "Sorry, could you clarify what you mean?",
]

# Core intent dictionary used by RuleBasedChatbot._match_intent().
# Each intent maps to a list of trigger keywords and a single response.
# This dictionary IS the control-flow mechanism: looking up a key in
# INTENT_RESPONSES (or scanning its keyword lists) replaces what would
# otherwise be dozens of "if 'x' in text: ... elif 'y' in text: ..." lines.
INTENT_RESPONSES: dict[str, dict] = {
    "identity": {
        "keywords": ["who are you", "your name", "what are you"],
        "response": "I'm DecodeBot, a rule-based AI chatbot built with Python dictionaries.",
    },
    "creator": {
        "keywords": ["who made you", "who created you", "your creator", "who built you"],
        "response": "I was built as part of the DecodeLabs Artificial Intelligence Industrial Training portfolio.",
    },
    "capabilities": {
        "keywords": ["what can you do", "help me", "your features", "what do you do"],
        "response": (
            "I can answer simple questions, hold a basic conversation, "
            "and demonstrate rule-based intent matching using dictionaries."
        ),
    },
    "time": {
        "keywords": ["time", "clock", "what time"],
        "response": "I don't have a live clock connected, but your system clock will have the exact time!",
    },
    "weather": {
        "keywords": ["weather", "temperature", "rain", "forecast"],
        "response": "I can't fetch live weather here, but you could extend me with a weather API call!",
    },
    "thanks": {
        "keywords": ["thank you", "thanks", "appreciate it"],
        "response": "You're very welcome! Happy to help.",
    },
    "joke": {
        "keywords": ["joke", "funny", "make me laugh"],
        "response": "Why do programmers prefer dark mode? Because light attracts bugs!",
    },
    "ai_definition": {
        "keywords": ["what is ai", "artificial intelligence", "define ai"],
        "response": (
            "Artificial Intelligence is the field of building systems that can "
            "perform tasks which typically require human intelligence, such as "
            "reasoning, learning, and decision-making."
        ),
    },
    "machine_learning": {
        "keywords": ["machine learning", "what is ml"],
        "response": (
            "Machine Learning is a subset of AI where systems learn patterns "
            "from data instead of following hardcoded rules."
        ),
    },
    "mood": {
        "keywords": ["how are you", "how are you doing", "hows it going"],
        "response": "I'm just a program, so I don't have feelings, but I'm running smoothly! How about you?",
    },
}
