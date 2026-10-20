# Python Practical Lab

**Four independent Python applications exploring game logic, portfolio analysis, filesystem automation, and conversational systems.**

---

## Project Overview

This repository contains four standalone Python programs built as part of a Python internship assignment. Each application is independently runnable and has its own documentation, tests, and data resources.

| # | Application | Entry Point | Description |
|---|---|---|---|
| 1 | [Hangman Word Challenge](word_challenge/) | `word_challenge/game.py` | Terminal word-guessing game with ASCII gallows art |
| 2 | [Portfolio Market Journal](market_journal/) | `market_journal/tracker.py` | Stock portfolio tracker with gain/loss analysis |
| 3 | [Desktop File Sorter](desktop_sorter/) | `desktop_sorter/sorter.py` | Safe file organizer by extension category |
| 4 | [FAQ Conversation Assistant](faq_assistant/) | `faq_assistant/assistant.py` | Rule-based chatbot backed by a real FAQ dataset |

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- No third-party packages required — all apps use the standard library only

### Running the Applications

```bash
# Task 1 — Hangman Word Challenge
python word_challenge/game.py

# Task 2 — Portfolio Market Journal
python market_journal/tracker.py

# Task 3 — Desktop File Sorter (dry run — safe preview)
python desktop_sorter/sorter.py --target /path/to/folder --dry-run

# Task 3 — Desktop File Sorter (confirmed execution)
python desktop_sorter/sorter.py --target /path/to/folder --confirm

# Task 4 — FAQ Conversation Assistant
python faq_assistant/assistant.py
```

---

## Repository Structure

```
python-practical-lab/
├── index.htm                   # Universal web portal (open in browser)
├── README.md                   # This file
├── requirements.txt            # Dependency declaration (stdlib only)
├── .gitignore
│
├── web/
│   ├── styles/main.css         # Shared design system
│   └── scripts/portal.js       # Portal navigation script
│
├── word_challenge/             # Task 1
│   ├── game.py
│   ├── index.htm
│   ├── README.md
│   ├── resources/words.txt     # Google 10k English word list
│   └── tests/test_game.py
│
├── market_journal/             # Task 2
│   ├── tracker.py
│   ├── index.htm
│   ├── README.md
│   ├── resources/constituents.csv   # S&P 500 constituents
│   └── tests/test_tracker.py
│
├── desktop_sorter/             # Task 3
│   ├── sorter.py
│   ├── index.htm
│   ├── README.md
│   ├── logs/
│   └── tests/test_sorter.py
│
├── faq_assistant/              # Task 4
│   ├── assistant.py
│   ├── index.htm
│   ├── README.md
│   ├── resources/sample_faq.json
│   └── tests/test_assistant.py
│
└── documentation/
    ├── DESIGN.md               # Visual and architecture design rationale
    ├── DATA_SOURCES.md         # Dataset sources, status, and fallbacks
    └── VALIDATION.md           # Test results and verification log
```

---

## Running Tests

```bash
# All tests via unittest discovery
python -m unittest discover word_challenge/tests -v
python -m unittest discover market_journal/tests -v
python -m unittest discover desktop_sorter/tests -v
python -m unittest discover faq_assistant/tests -v
```

---

## Web Portal

Open `index.htm` in any modern browser for the project landing page with navigation to all four applications.

---

## Datasets

| Task | Source | File |
|---|---|---|
| Hangman words | [google-10000-english](https://github.com/first20hours/google-10000-english) | `word_challenge/resources/words.txt` |
| S&P 500 tickers | [datasets/s-and-p-500-companies](https://github.com/datasets/s-and-p-500-companies) | `market_journal/resources/constituents.csv` |
| FAQ data | [datheon.in/datasets](https://www.datheon.in/datasets/sample_faq.json) | `faq_assistant/resources/sample_faq.json` |

See [documentation/DATA_SOURCES.md](documentation/DATA_SOURCES.md) for detailed availability status and fallback policies.

---

## Disclaimer

The Portfolio Market Journal application is for **educational purposes only** and does not constitute investment advice. Price data entered manually is not verified or endorsed. See the application's own disclaimer for full details.

---

## Documentation

- [Design Notes](documentation/DESIGN.md)
- [Data Sources](documentation/DATA_SOURCES.md)
- [Validation Report](documentation/VALIDATION.md)
