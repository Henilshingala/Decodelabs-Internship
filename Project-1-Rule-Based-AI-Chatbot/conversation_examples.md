# Conversation Examples — Rule-Based AI Chatbot

## Example 1 — General Conversation

```
DecodeBot: Hello! I'm DecodeBot, your rule-based AI assistant.
DecodeBot: Type 'exit', 'quit', or 'bye' anytime to end our chat.

You: hi
DecodeBot: Hi! What can I do for you?

You: who are you
DecodeBot: I'm DecodeBot, a rule-based AI chatbot built with Python dictionaries.

You: what is ai
DecodeBot: Artificial Intelligence is the field of building systems that can perform tasks which typically require human intelligence, such as reasoning, learning, and decision-making.

You: what is machine learning
DecodeBot: Machine Learning is a subset of AI where systems learn patterns from data instead of following hardcoded rules.

You: tell me a joke
DecodeBot: Why do programmers prefer dark mode? Because light attracts bugs!

You: thanks
DecodeBot: You're very welcome! Happy to help.

You: bye
DecodeBot: Goodbye! Have a wonderful day.

DecodeBot: Conversation log saved to chat_log.txt
```

## Example 2 — Unknown Input Handling

```
You: do you like pizza
DecodeBot: I'm not sure I understand. Could you rephrase that?

You: qwertyuiop
DecodeBot: Hmm, that's outside what I currently know. Try asking differently.

You: what can you do
DecodeBot: I can answer simple questions, hold a basic conversation, and demonstrate rule-based intent matching using dictionaries.

You: exit
DecodeBot: Bye! Feel free to come back anytime.
```

## Example 3 — Edge Cases

```
You:
DecodeBot: I didn't catch that. Could you type something?

You: !!!???
DecodeBot: I didn't catch that. Could you type something?

You: HOW ARE YOU??
DecodeBot: I'm just a program, so I don't have feelings, but I'm running smoothly! How about you?

You: quit
DecodeBot: See you soon! Take care.
```

## Resulting `chat_log.txt` Sample

```
[14:02:11] USER: hi
[14:02:11] BOT: Hi! What can I do for you?
[14:02:20] USER: who are you
[14:02:20] BOT: I'm DecodeBot, a rule-based AI chatbot built with Python dictionaries.
[14:02:40] USER: bye
[14:02:40] BOT: Goodbye! Have a wonderful day.
```
