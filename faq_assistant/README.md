# Task 04: FAQ Conversation Assistant

A deterministic, rule-based conversational terminal assistant grounded strictly in a verified JSON FAQ dataset.

---

## Overview

FAQ Conversation Assistant demonstrates rule-based natural language processing without heavyweight external dependencies. The assistant accurately identifies user intents, answers domain-specific internship inquiries using Jaccard keyword similarity scoring against `resources/sample_faq.json`, and handles ambiguous queries honestly through clarifying fallbacks.

---

## Intent Classification Pipeline

User queries pass through a prioritized decision hierarchy:

```
[User Input]
     │
     ▼
[1. EXIT INTENT?] ────────► "bye", "exit", "quit" ──────────► Graceful Exit
     │ No
     ▼
[2. GREETING INTENT?] ────► Regex match with dataset greetings ─► Warm Greeting
     │ No
     ▼
[3. HELP INTENT?] ────────► "help", "commands" ─────────────► Available Capabilities
     │ No
     ▼
[4. FAQ MATCH?] ──────────► Jaccard token overlap ≥ 0.25 ───► Verified Dataset Answer
     │ No
     ▼
[5. FALLBACK INTENT] ─────► Clarifying prompt (Never fabricates facts)
```

---

## Jaccard Similarity Algorithm

For FAQ queries, the engine normalizes both the user query and each dataset question:

$$\text{Jaccard Similarity} = \frac{|T_{\text{query}} \cap T_{\text{faq}}|}{|T_{\text{query}} \cup T_{\text{faq}}|}$$

Where $T$ represents the set of alphanumeric words excluding common stopwords (`a`, `the`, `is`, `for`, `in`, `to`, `of`, etc.). If the highest score exceeds the threshold ($0.25$), the corresponding answer is returned.

---

## Directory Structure

```
faq_assistant/
├── assistant.py            # Main interactive CLI conversation engine
├── index.html              # Interactive web showcase and live chat simulator
├── README.md               # Architecture documentation
├── resources/
│   └── sample_faq.json     # Verified FAQ dataset (greetings and Q&A items)
└── tests/
    └── test_assistant.py   # Automated unit test suite (unittest)
```

---

## Execution Guide

### Running the Terminal Assistant

```bash
# Navigate to the task directory
cd d:/intership/python/vj/faq_assistant

# Launch the interactive assistant
python assistant.py
```

### Sample Session Queries

- `"Hello!"` &rarr; Returns friendly greeting from the dataset.
- `"What is an internship?"` &rarr; Retrieves verified definition.
- `"How can I apply for an internship?"` &rarr; Retrieves application advice.
- `"Are internships paid or unpaid?"` &rarr; Retrieves compensation details.
- `"What is the weather today?"` &rarr; Triggers polite clarifying fallback.
- `"bye"` &rarr; Exits session gracefully.

### Running the Automated Test Suite

```bash
python -m unittest tests/test_assistant.py -v
```

---

## Automated Test Coverage

The test suite in `tests/test_assistant.py` verifies:

1. `TestFAQLoading`: Tests handling of valid JSON, missing files, and corrupt syntax.
2. `TestNormalization`: Verifies whitespace collapse, lowercasing, and punctuation removal.
3. `TestIntentRecognition`: Confirms exact intent routing across all defined classes.
4. `TestFAQMatching`: Asserts high scoring on genuine queries and low scoring on off-topic questions.
5. `TestFallbackBehavior`: Confirms clarifying fallback response when below threshold.
6. `TestExitCommands`: Verifies `bye`, `exit`, `quit` regardless of capitalization.
