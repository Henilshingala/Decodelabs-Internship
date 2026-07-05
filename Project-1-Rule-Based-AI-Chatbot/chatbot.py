"""
chatbot.py
----------
A Rule-Based AI Chatbot implementing the Input -> Process -> Output (IPO) model
using dictionary-based intent lookup instead of long if-elif chains.

Author: AI Engineering Portfolio
Python Version: 3.12+
"""

from __future__ import annotations

import re
import sys
import random
from datetime import datetime
from typing import Callable, Optional

from responses import (
    GREETING_PATTERNS,
    FAREWELL_PATTERNS,
    INTENT_RESPONSES,
    UNKNOWN_RESPONSES,
    GREETING_RESPONSES,
    FAREWELL_RESPONSES,
)


class ConversationHistory:
    """Stores and manages the chat session's conversation history."""

    def __init__(self) -> None:
        self._history: list[dict[str, str]] = []

    def add(self, speaker: str, message: str) -> None:
        """Append a new turn to the conversation history."""
        self._history.append(
            {
                "speaker": speaker,
                "message": message,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
            }
        )

    def get_history(self) -> list[dict[str, str]]:
        """Return the full conversation history."""
        return self._history

    def save_to_file(self, filepath: str = "chat_log.txt") -> None:
        """Persist the conversation history to a text file."""
        try:
            with open(filepath, "w", encoding="utf-8") as file_handle:
                for turn in self._history:
                    file_handle.write(
                        f"[{turn['timestamp']}] {turn['speaker'].upper()}: {turn['message']}\n"
                    )
        except OSError as error:
            print(f"Warning: could not save chat log ({error}).")


class RuleBasedChatbot:
    """A dictionary-driven rule-based chatbot.

    Follows the classic IPO (Input -> Process -> Output) model:
      1. INPUT   : Capture and normalize raw user text.
      2. PROCESS : Match normalized text against known intent patterns
                   using dictionary lookup (O(1) average case) rather
                   than a long chain of if-elif statements.
      3. OUTPUT  : Return the response tied to the matched intent, or a
                   fallback response if no intent matches.
    """

    EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye", "stop", "end"}

    def __init__(self, bot_name: str = "DecodeBot") -> None:
        self.bot_name = bot_name
        self.history = ConversationHistory()
        self.is_running = True
        self.intent_dispatch: dict[str, Callable[[str], str]] = self._build_dispatch_table()

    def _build_dispatch_table(self) -> dict[str, Callable[[str], str]]:
        """Construct the dictionary that maps intents to response handlers."""
        dispatch: dict[str, Callable[[str], str]] = {}
        for intent in INTENT_RESPONSES:
            dispatch[intent] = self._make_handler(intent)
        return dispatch

    def _make_handler(self, intent: str) -> Callable[[str], str]:
        """Create a closure handler bound to a specific intent key."""

        def handler(_user_text: str) -> str:
            return INTENT_RESPONSES[intent]["response"]

        return handler

    @staticmethod
    def _normalize(text: str) -> str:
        """Lowercase, strip, and remove punctuation from user input."""
        if not isinstance(text, str):
            raise TypeError("Input to chatbot must be a string.")
        text = text.strip().lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def _match_intent(self, normalized_text: str) -> Optional[str]:
        """Find the best matching intent key for the normalized input."""
        for intent, data in INTENT_RESPONSES.items():
            keywords = data["keywords"]
            if any(keyword in normalized_text for keyword in keywords):
                return intent
        return None

    def _is_greeting(self, normalized_text: str) -> bool:
        return any(pattern in normalized_text for pattern in GREETING_PATTERNS)

    def _is_farewell(self, normalized_text: str) -> bool:
        return any(pattern in normalized_text for pattern in FAREWELL_PATTERNS)

    def get_response(self, user_text: str) -> str:
        """Generate a chatbot response for a single user input (full IPO pipeline)."""
        try:
            normalized = self._normalize(user_text)
        except TypeError as error:
            return f"Sorry, I couldn't process that input ({error})."

        if not normalized:
            return "I didn't catch that. Could you type something?"

        if normalized in self.EXIT_COMMANDS:
            self.is_running = False
            return random.choice(FAREWELL_RESPONSES)

        if self._is_greeting(normalized):
            return random.choice(GREETING_RESPONSES)

        if self._is_farewell(normalized):
            self.is_running = False
            return random.choice(FAREWELL_RESPONSES)

        matched_intent = self._match_intent(normalized)

        if matched_intent is not None:
            handler = self.intent_dispatch[matched_intent]
            return handler(normalized)

        return random.choice(UNKNOWN_RESPONSES)

    def run(self) -> None:
        """Run the continuous chatbot conversation loop in the console."""
        print(f"{self.bot_name}: Hello! I'm {self.bot_name}, your rule-based AI assistant.")
        print(f"{self.bot_name}: Type 'exit', 'quit', or 'bye' anytime to end our chat.\n")

        while self.is_running:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{self.bot_name}: Session interrupted. Goodbye!")
                break

            self.history.add("user", user_input)
            response = self.get_response(user_input)
            self.history.add("bot", response)
            print(f"{self.bot_name}: {response}")

        self.history.save_to_file()
        print(f"\n{self.bot_name}: Conversation log saved to chat_log.txt")


def main() -> None:
    """Entry point for running the chatbot as a script."""
    bot = RuleBasedChatbot(bot_name="DecodeBot")
    bot.run()


if __name__ == "__main__":
    sys.exit(main())
