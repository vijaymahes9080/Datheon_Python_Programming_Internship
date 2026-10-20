# Task 01: Hangman Word Challenge

A robust, modular, terminal-based word guessing game written in Python using only the standard library.

---

## Overview

Hangman Word Challenge is an independent implementation of the classic word-guessing game. It integrates with real-world lexical data (Google 10,000 English word list) and delivers a clean, defensive command-line interface with dynamic ASCII gallows visuals and input validation.

---

## Key Features

- **Lexical Data Ingestion**: Automatically loads filtered words from `resources/words.txt` (Google 10k English word list). Words are filtered between 4 and 12 characters, stripped of whitespace, and deduplicated.
- **Embedded Fallback Bank**: If the dataset file is absent or inaccessible, the game seamlessly falls back to an embedded 50-word vocabulary without crashing.
- **7-Stage ASCII Gallows Art**: Renders progressive visual stages representing 0 to 6 incorrect guesses.
- **Defensive Input Validation**:
  - Rejects numbers, punctuation, spaces, and multi-character inputs.
  - Detects duplicate guesses, notifying the user without deducting attempts.
- **Session Management**: Full replay loop ("Play again? [y/n]"), score tracking, and graceful handling of `Ctrl+C` (`KeyboardInterrupt`) and `EOFError`.

---

## Directory Structure

```
word_challenge/
├── game.py                 # Core game executable and engine
├── index.html              # Interactive web showcase with in-browser demo
├── README.md               # Application documentation
├── resources/
│   └── words.txt           # Google 10,000 English word list (9,894 valid words)
└── tests/
    └── test_game.py        # Automated unit test suite (unittest)
```

---

## Execution Guide

### Running the Terminal Game

Ensure Python 3.8+ is installed on your system:

```bash
# Navigate to the task directory
cd d:/intership/python/vj/word_challenge

# Launch the game
python game.py
```

### Running the Automated Test Suite

```bash
python -m unittest tests/test_game.py -v
```

---

## ASCII Gallows Stages

```
Stage 0 (0 errors)   Stage 1 (1 error)    Stage 3 (3 errors)   Stage 6 (Defeat)
  +---+                +---+                +---+                +---+
  |   |                |   |                |   |                |   |
      |                O   |                O   |                O   |
      |                    |               /|   |               /|\  |
      |                    |                    |               / \  |
      |                    |                    |                    |
=========            =========            =========            =========
```

---

## Automated Test Coverage

The test suite in `tests/test_game.py` validates:

1. `TestWordLoading`: Verifies loading from disk, fallback on missing file, filtering short (<4) and long (>12) words.
2. `TestGameLogic`: Checks letter matching, word masking (`_ p p _ e`), and stage incrementation.
3. `TestWinLoss`: Validates full winning sequences and 6-error terminal condition.
4. `TestDuplicateGuess`: Asserts duplicate guesses trigger `is_new=False` and do not penalize attempt counts.
5. `TestInvalidInput`: Asserts non-alphabetic inputs are rejected defensively.
