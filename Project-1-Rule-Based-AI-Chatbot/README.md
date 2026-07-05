# Project 1 — Rule-Based AI Chatbot

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Complete-success)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

A console-based rule-based AI chatbot built entirely with Python's standard
library. Instead of a long chain of `if-elif` statements, the bot's
"intelligence" comes from a **dictionary-driven intent lookup system**,
demonstrating clean separation between conversational data and control logic.

## Objectives

- Demonstrate the **Input → Process → Output (IPO)** model in a working program.
- Replace inefficient `if-elif` decision chains with dictionary lookups and a dispatch table.
- Implement conversation memory, graceful exit handling, and a persisted chat log.
- Produce a maintainable, extensible chatbot architecture.

## Problem Statement

Beginner chatbot implementations often hardcode dozens of `if/elif` branches
to detect user intent. This does not scale, is hard to test, and mixes data
with logic. This project solves that by storing all intents, keywords, and
responses as structured data (`responses.py`) and using a small, generic
matching engine (`chatbot.py`) to process any number of intents without
additional branching logic.

## Theory

| Concept | Application in this Project |
|---|---|
| IPO Model | Core architecture of `get_response()` |
| Dictionary Lookup | `INTENT_RESPONSES` dict keyed by intent name |
| Dispatch Pattern | `self.intent_dispatch` maps intents to callables |
| Control Flow | Sequential guard clauses before falling through to dictionary matching |
| State Management | `ConversationHistory` class tracks every turn |

## Architecture & Workflow

See [`architecture.md`](architecture.md) for full class/responsibility breakdown and [`flowchart.md`](flowchart.md) for Mermaid diagrams of the control flow and a sequence diagram of one conversational turn.

```
Project-1-Rule-Based-AI-Chatbot/
├── chatbot.py                 # Core bot logic, IPO pipeline, CLI loop
├── responses.py                # Intent dictionary + response pools (data layer)
├── requirements.txt
├── architecture.md
├── flowchart.md
├── test_cases.md
├── conversation_examples.md
└── screenshots/
```

## Implementation & Code Explanation

- `responses.py` defines `INTENT_RESPONSES`, a dictionary mapping intent names to `{"keywords": [...], "response": "..."}`.
- `RuleBasedChatbot._normalize()` lowercases and strips punctuation from user input.
- `RuleBasedChatbot._match_intent()` performs a substring scan against each intent's keyword list — the dictionary-lookup replacement for `if-elif`.
- `RuleBasedChatbot._build_dispatch_table()` builds a second dictionary, `self.intent_dispatch`, mapping intent → handler function, illustrating the Command/Dispatch design pattern.
- `ConversationHistory` records every turn with a timestamp and writes the transcript to `chat_log.txt` on exit.

## Execution Steps

```bash
# 1. Navigate into the project folder
cd Project-1-Rule-Based-AI-Chatbot

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. No external dependencies are required (standard library only)

# 4. Run the chatbot
python chatbot.py
```

## Expected Output

```
DecodeBot: Hello! I'm DecodeBot, your rule-based AI assistant.
DecodeBot: Type 'exit', 'quit', or 'bye' anytime to end our chat.

You: hello
DecodeBot: Hi! What can I do for you?
```

Full transcripts are in [`conversation_examples.md`](conversation_examples.md).

## Screenshots

> Place terminal screenshots of a live chatbot session inside the `screenshots/` folder (e.g. `screenshots/chat_session_1.png`).

## Applications

- Customer support FAQ bots
- Onboarding assistants for websites/apps
- Educational tool for teaching control-flow and dictionary data structures
- Foundation for more advanced NLP-based chatbots

## Advantages

- Zero external dependencies — runs anywhere Python 3 runs
- O(1)-style dictionary lookups instead of long conditional chains
- Easy to extend: add a dictionary entry, not a code branch
- Fully deterministic and testable

## Limitations

- No true natural language understanding (purely keyword/substring based)
- Cannot handle synonyms it hasn't been told about, spelling errors, or context across multiple turns
- Single-language (English) keyword set

## Future Scope

- Integrate `nltk` or `spaCy` for lemmatization and fuzzy keyword matching
- Add a small intent-classification ML model (see Project 2) to reduce manual keyword tuning
- Build a Flask/FastAPI web interface around the same `RuleBasedChatbot` class
- Persist conversation history to SQLite instead of a flat text file

## Interview Questions

1. **Why use a dictionary instead of if-elif chains for intent matching?**
   Dictionaries give O(1) average lookup, separate data from logic, and let you add new intents without touching control-flow code — improving maintainability and adherence to the Open/Closed Principle.

2. **Explain the IPO model in the context of this chatbot.**
   Input: capture and normalize raw text. Process: match the normalized text against intent keyword dictionaries. Output: return the response tied to the matched intent or a fallback.

3. **How does the dispatch table differ from the keyword dictionary?**
   `INTENT_RESPONSES` is a *data* dictionary (intent → keywords/response text). `self.intent_dispatch` is a *behavior* dictionary (intent → callable handler), demonstrating the Command pattern.

4. **What are the limitations of substring-based keyword matching?**
   It can produce false positives (e.g., "I am not happy" matching a "happy" keyword) and cannot generalize to synonyms or typos — a limitation that motivates moving toward statistical/ML-based NLP.

5. **How would you scale this chatbot to handle hundreds of intents?**
   Keep all intents as data (already the case here), potentially move them to a JSON/YAML config or database, and consider hybrid approaches (rule-based for high-confidence intents, ML classifier as fallback).

6. **Why normalize input before matching?**
   To make matching case-insensitive and punctuation-tolerant, ensuring "Hello!", "hello", and "HELLO" all map to the same intent.

## Conclusion

This project demonstrates that a clean, maintainable, and testable chatbot can
be built without any external NLP libraries by applying solid software
engineering principles — data/logic separation, dictionary-based dispatch, and
the IPO model — to a classic rule-based AI problem.
