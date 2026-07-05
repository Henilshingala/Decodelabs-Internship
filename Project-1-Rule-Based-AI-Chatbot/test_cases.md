# Test Cases — Rule-Based AI Chatbot

These test cases can be run manually via `python chatbot.py`, or automated with `pytest` by importing `RuleBasedChatbot` and asserting on `get_response()` output.

| # | Input | Expected Behavior | Category |
|---|---|---|---|
| 1 | `hello` | Returns a greeting response | Greeting |
| 2 | `Hi there!` | Punctuation stripped, still matches greeting | Normalization |
| 3 | `who are you` | Returns identity response | Intent Match |
| 4 | `WHAT IS AI` | Case-insensitive match to `ai_definition` intent | Normalization |
| 5 | `tell me a joke` | Returns the joke response | Intent Match |
| 6 | `thanks a lot` | Returns thanks response | Intent Match |
| 7 | `asdkjqwe` | Returns one of `UNKNOWN_RESPONSES` | Fallback |
| 8 | `` (empty string) | Returns "I didn't catch that..." prompt | Edge Case |
| 9 | `   ` (whitespace only) | Treated as empty after normalization | Edge Case |
| 10 | `exit` | Ends loop, returns farewell, saves chat log | Exit Command |
| 11 | `bye` | Ends loop via farewell pattern detection | Exit Command |
| 12 | `123456` | No keyword match -> fallback response | Edge Case |
| 13 | `how are you doing today` | Matches `mood` intent | Intent Match |
| 14 | (non-string input, e.g. `None`, via direct function call) | Raises `TypeError`, caught and returned as friendly error string | Error Handling |
| 15 | `What can you DO??` | Punctuation removed, matches `capabilities` intent | Normalization |

## Sample pytest Suite

```python
import pytest
from chatbot import RuleBasedChatbot

@pytest.fixture
def bot():
    return RuleBasedChatbot()

def test_greeting(bot):
    response = bot.get_response("Hello!")
    assert "Hi" in response or "Hello" in response or "Hey" in response or "Greetings" in response

def test_identity_intent(bot):
    response = bot.get_response("who are you")
    assert "DecodeBot" in response

def test_unknown_input(bot):
    response = bot.get_response("zzxxqqvv")
    assert response  # non-empty fallback string returned

def test_exit_sets_running_false(bot):
    bot.get_response("exit")
    assert bot.is_running is False

def test_empty_input(bot):
    response = bot.get_response("")
    assert "didn't catch" in response.lower()
```

Run with:
```bash
pip install pytest
pytest test_chatbot.py -v
```
