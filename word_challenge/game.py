"""
word_challenge/game.py
----------------------
Hangman Word Challenge — terminal-based word guessing game.

Entry point: python word_challenge/game.py

Rules:
  - A random secret word is chosen from the word list.
  - The player guesses one letter at a time.
  - Maximum 6 incorrect guesses before defeat.
  - Duplicate guesses carry no penalty.
  - The word is revealed on defeat.
  - The player may replay after each round.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RESOURCES_DIR = Path(__file__).parent / "resources"
WORDS_FILE = RESOURCES_DIR / "words.txt"

MIN_WORD_LEN = 4
MAX_WORD_LEN = 12
MAX_WRONG = 6

# Fallback word list used when the dataset is unavailable.
FALLBACK_WORDS: list[str] = [
    "python", "keyboard", "monitor", "network", "program",
    "terminal", "archive", "browser", "library", "variable",
    "function", "integer", "boolean", "iterate", "recursion",
    "syntax", "import", "module", "package", "inherit",
    "abstract", "interface", "pointer", "memory", "binary",
    "decimal", "hexadec", "compile", "execute", "runtime",
    "dataset", "cluster", "quantum", "digital", "circuit",
    "voltage", "current", "battery", "reactor", "silicon",
    "chapter", "science", "history", "culture", "fiction",
    "journal", "article", "publish", "graphic", "animated",
]

# ---------------------------------------------------------------------------
# ASCII gallows — 7 stages (stage 0 = empty, stage 6 = full figure)
# ---------------------------------------------------------------------------

GALLOWS: list[str] = [
    # Stage 0 — empty gallows
    r"""
  +-------+
  |       |
  |
  |
  |
  |
 ===
""",
    # Stage 1 — head
    r"""
  +-------+
  |       |
  |       O
  |
  |
  |
 ===
""",
    # Stage 2 — head + torso
    r"""
  +-------+
  |       |
  |       O
  |       |
  |
  |
 ===
""",
    # Stage 3 — head + torso + left arm
    r"""
  +-------+
  |       |
  |       O
  |      /|
  |
  |
 ===
""",
    # Stage 4 — head + torso + both arms
    r"""
  +-------+
  |       |
  |       O
  |      /|\
  |
  |
 ===
""",
    # Stage 5 — head + torso + arms + left leg
    r"""
  +-------+
  |       |
  |       O
  |      /|\
  |      /
  |
 ===
""",
    # Stage 6 — full figure (defeat)
    r"""
  +-------+
  |       |
  |       O
  |      /|\
  |      / \
  |
 ===
""",
]

# ---------------------------------------------------------------------------
# Word loading
# ---------------------------------------------------------------------------


def load_words(path: Path = WORDS_FILE) -> list[str]:
    """Load and validate words from the given file path.

    Filters out entries that are too short, too long, contain non-alpha
    characters, or are duplicates. Falls back to FALLBACK_WORDS if the file
    cannot be read.

    Args:
        path: Path to the word list text file.

    Returns:
        A deduplicated list of suitable words.
    """
    if not path.exists():
        _warn(f"Word file not found: {path}  —  using built-in fallback list.")
        return list(FALLBACK_WORDS)

    try:
        raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        _warn(f"Cannot read word file ({exc})  —  using built-in fallback list.")
        return list(FALLBACK_WORDS)

    seen: set[str] = set()
    valid: list[str] = []
    for line in raw:
        word = line.strip().lower()
        if (
            word
            and word.isalpha()
            and MIN_WORD_LEN <= len(word) <= MAX_WORD_LEN
            and word not in seen
        ):
            seen.add(word)
            valid.append(word)

    if not valid:
        _warn("Word file contained no valid entries  —  using built-in fallback list.")
        return list(FALLBACK_WORDS)

    return valid


def pick_word(words: list[str]) -> str:
    """Return a randomly selected word from the list."""
    return random.choice(words)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def build_masked_word(word: str, guessed: set[str]) -> str:
    """Return the word with unguessed letters replaced by underscores.

    Example: word='apple', guessed={'a','e'} → 'a _ _ _ e'
    """
    return " ".join(letter if letter in guessed else "_" for letter in word)


def display_state(word: str, guessed: set[str], wrong_count: int) -> None:
    """Print the current gallows stage, masked word, and guessed letters."""
    print(GALLOWS[wrong_count])
    print(f"  Word:    {build_masked_word(word, guessed)}")
    print(f"  Guessed: {', '.join(sorted(guessed)) if guessed else '—'}")
    wrong_letters = sorted(g for g in guessed if g not in word)
    print(f"  Wrong:   {', '.join(wrong_letters) if wrong_letters else '—'}  "
          f"({wrong_count}/{MAX_WRONG})")
    print()


def _banner(text: str, char: str = "=") -> None:
    """Print a simple banner line."""
    border = char * (len(text) + 4)
    print(f"\n{border}")
    print(f"  {text}")
    print(f"{border}\n")


def _warn(message: str) -> None:
    """Print a warning to stderr."""
    print(f"[WARNING] {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Core game logic (pure functions — testable without I/O)
# ---------------------------------------------------------------------------


def process_guess(
    letter: str,
    word: str,
    guessed: set[str],
) -> tuple[bool, bool]:
    """Evaluate a single letter guess.

    Args:
        letter: The guessed letter (should be a single alpha character).
        word: The secret word.
        guessed: Set of letters already guessed.

    Returns:
        (is_new, is_correct) where:
          is_new     — False if letter was already guessed (duplicate).
          is_correct — True if the letter appears in the word.
    """
    if letter in guessed:
        return False, letter in word
    return True, letter in word


def is_word_complete(word: str, guessed: set[str]) -> bool:
    """Return True when every letter in the word has been guessed."""
    return all(letter in guessed for letter in word)


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def prompt_letter(guessed: set[str]) -> str | None:
    """Prompt the player for a single letter.

    Returns the validated letter, or None on EOF/Ctrl+C.
    """
    try:
        raw = input("  Guess a letter: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return None

    if not raw:
        print("  Please enter a letter.\n")
        return prompt_letter(guessed)

    if len(raw) != 1 or not raw.isalpha():
        print("  Enter exactly one letter (a–z).\n")
        return prompt_letter(guessed)

    return raw


# ---------------------------------------------------------------------------
# Game round
# ---------------------------------------------------------------------------


def play_round(word: str) -> bool:
    """Run a single game round.

    Args:
        word: The secret word for this round.

    Returns:
        True if the player won, False if they lost.
    """
    guessed: set[str] = set()
    wrong_count = 0

    _banner(f"Hangman Word Challenge  —  {len(word)} letters")

    while True:
        display_state(word, guessed, wrong_count)

        # Win check
        if is_word_complete(word, guessed):
            _banner("🎉  You guessed it!", char="*")
            print(f"  The word was: {word.upper()}\n")
            return True

        # Lose check
        if wrong_count >= MAX_WRONG:
            print(GALLOWS[MAX_WRONG])
            _banner("💀  Out of guesses!", char="-")
            print(f"  The word was: {word.upper()}\n")
            return False

        letter = prompt_letter(guessed)
        if letter is None:
            print("\n  Game interrupted. Goodbye!\n")
            sys.exit(0)

        is_new, is_correct = process_guess(letter, word, guessed)

        if not is_new:
            print(f"  You already guessed '{letter}'. No penalty — try another.\n")
            continue

        guessed.add(letter)

        if is_correct:
            print(f"  ✓ '{letter}' is in the word!\n")
        else:
            wrong_count += 1
            print(f"  ✗ '{letter}' is not in the word.  ({wrong_count}/{MAX_WRONG} wrong)\n")


# ---------------------------------------------------------------------------
# Main game loop with replay
# ---------------------------------------------------------------------------


def run_game() -> None:
    """Load words and run the game with replay support."""
    words = load_words()
    wins = 0
    losses = 0

    print("\n" + "=" * 40)
    print("   HANGMAN WORD CHALLENGE")
    print("=" * 40)
    print(f"  Word list: {len(words):,} words loaded")
    print(f"  Rules: guess the word in {MAX_WRONG} wrong attempts")
    print("=" * 40 + "\n")

    try:
        while True:
            word = pick_word(words)
            won = play_round(word)
            if won:
                wins += 1
            else:
                losses += 1

            print(f"  Session — Wins: {wins}  Losses: {losses}\n")

            try:
                again = input("  Play again? (y/n): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                break

            if again not in ("y", "yes"):
                break

    except KeyboardInterrupt:
        pass

    print(f"\n  Thanks for playing!  Final — Wins: {wins}  Losses: {losses}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_game()
