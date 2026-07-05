# Architecture — Rule-Based AI Chatbot

## 1. The IPO Model

This chatbot is structured around the classic **Input → Process → Output (IPO)** model used in introductory AI and software engineering courses.

| Stage | Responsibility | Implementation |
|---|---|---|
| **Input** | Capture raw text from the user and normalize it (lowercase, strip punctuation/whitespace) | `RuleBasedChatbot._normalize()` |
| **Process** | Decide what the user meant by matching normalized text against known intent keyword sets | `RuleBasedChatbot._match_intent()`, `_is_greeting()`, `_is_farewell()` |
| **Output** | Return the response tied to the matched intent, or fall back to an "unknown" response | `RuleBasedChatbot.get_response()` |

```
 ┌────────────┐     ┌────────────────┐     ┌────────────────┐
 │   INPUT    │ --> │    PROCESS     │ --> │     OUTPUT     │
 │ Raw text   │     │ Normalize +    │     │ Selected /     │
 │ from user  │     │ Dictionary     │     │ fallback       │
 │            │     │ Lookup         │     │ response       │
 └────────────┘     └────────────────┘     └────────────────┘
```

## 2. Why a Dictionary Instead of if-elif Chains?

A naive chatbot might be written as:

```python
if "hello" in text:
    return "Hi there!"
elif "bye" in text:
    return "Goodbye!"
elif "weather" in text:
    return "..."
# ...30 more elif branches
```

This scales poorly: every new intent adds another branch, the function becomes
unreadable, and maintenance is painful. Instead, this project stores intents
as **data** in `responses.py`:

```python
INTENT_RESPONSES = {
    "weather": {"keywords": [...], "response": "..."},
    "joke":    {"keywords": [...], "response": "..."},
}
```

`_match_intent()` then iterates this dictionary once, checking if any keyword
is a substring of the normalized input. Adding a new intent means adding one
dictionary entry — zero changes to control-flow logic. This separates **data**
(what the bot knows) from **logic** (how the bot decides), a core software
engineering principle.

## 3. Control Flow

```
get_response(user_text)
 ├─ normalize(user_text)
 ├─ if normalized is empty -> ask user to repeat
 ├─ if normalized is an exit command -> stop loop, farewell
 ├─ if normalized matches a greeting pattern -> greeting response
 ├─ if normalized matches a farewell pattern -> stop loop, farewell
 ├─ matched_intent = _match_intent(normalized)
 │    └─ scans INTENT_RESPONSES keyword lists
 ├─ if matched_intent found -> dispatch handler -> return response
 └─ else -> return random UNKNOWN_RESPONSES entry
```

## 4. Dictionary Lookup Mechanics

Two dictionary-driven mechanisms work together:

1. **Keyword matching dictionary** (`INTENT_RESPONSES`) — maps an intent name
   to its trigger keywords and response text. Lookup is by iteration over
   keys with substring containment checks against the keyword list.
2. **Dispatch table** (`self.intent_dispatch`) — maps an intent name directly
   to a bound handler function (a closure created in `_make_handler`). This
   demonstrates the **Command/Dispatch pattern**: instead of calling a
   function conditionally via if-elif, the correct function is looked up and
   invoked via `self.intent_dispatch[matched_intent](text)`.

## 5. Class Responsibilities

| Class | Responsibility |
|---|---|
| `ConversationHistory` | Stores every user/bot turn with a timestamp; can persist the session to `chat_log.txt` |
| `RuleBasedChatbot` | Owns the IPO pipeline, the intent dispatch table, and the console interaction loop |

## 6. Extensibility

To add a new capability:
1. Add a new key to `INTENT_RESPONSES` in `responses.py` with `keywords` and `response`.
2. No changes are needed in `chatbot.py` — the dispatch table is built dynamically from the dictionary at runtime.

This makes the architecture **open for extension, closed for modification**
(the Open/Closed Principle from SOLID design).
