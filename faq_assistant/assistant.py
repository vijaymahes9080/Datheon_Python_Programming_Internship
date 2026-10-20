"""
faq_assistant/assistant.py
--------------------------
FAQ Conversation Assistant — rule-based chatbot backed by a real FAQ dataset.

Entry point: python faq_assistant/assistant.py

The assistant loads sample_faq.json and responds to:
  - Greetings (matched against the dataset's greeting list)
  - FAQ questions (keyword-overlap scoring against dataset entries)
  - Help requests
  - Exit commands (bye / exit / quit)
  - Fallback with clarifying question for unrecognised input

All responses are grounded in the actual dataset. No business hours,
pricing, product details, or contact information are fabricated.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RESOURCES_DIR = Path(__file__).parent / "resources"
FAQ_FILE = RESOURCES_DIR / "sample_faq.json"

FAQ_MATCH_THRESHOLD = 0.15  # Minimum keyword overlap score to report a match

HELP_TEXT = """
  I can help with:
  • Greetings — say hello, hi, hey, etc.
  • FAQ questions — ask about hours, submissions, certificates, etc.
  • Type 'bye', 'exit', or 'quit' to leave.
  • Type 'help' to see this message again.
"""

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


class FAQData:
    """Container for the loaded FAQ dataset."""

    def __init__(self, greetings: list[str], faqs: list[dict]) -> None:
        self.greetings = greetings  # list of greeting strings
        self.faqs = faqs            # list of {question, answer} dicts


def load_faq(path: Path = FAQ_FILE) -> Optional[FAQData]:
    """Load the FAQ JSON from disk.

    Returns a FAQData object, or None if the file is missing or malformed.
    Handles missing keys gracefully — partial data is still usable.
    """
    if not path.exists():
        return None

    try:
        with path.open(encoding="utf-8") as fh:
            raw = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None

    if not isinstance(raw, dict):
        return None

    greetings = raw.get("greetings", [])
    if not isinstance(greetings, list):
        greetings = []

    faqs_raw = raw.get("faqs", [])
    if not isinstance(faqs_raw, list):
        faqs_raw = []

    faqs = []
    for entry in faqs_raw:
        if isinstance(entry, dict) and "question" in entry and "answer" in entry:
            faqs.append({"question": str(entry["question"]), "answer": str(entry["answer"])})

    return FAQData(greetings=greetings, faqs=faqs)


# ---------------------------------------------------------------------------
# Text normalisation
# ---------------------------------------------------------------------------


def normalize(text: str) -> str:
    """Lowercase, strip outer whitespace, collapse internal whitespace."""
    return re.sub(r"\s+", " ", text.strip().lower())


def tokenize(text: str) -> set[str]:
    """Extract non-trivial word tokens from normalised text."""
    stopwords = {
        "a", "an", "the", "is", "are", "was", "were", "i", "my", "your",
        "do", "did", "will", "can", "could", "should", "would", "to",
        "for", "of", "in", "on", "at", "be", "have", "has", "had",
        "this", "that", "what", "how", "when", "where", "who", "why",
        "and", "or", "but", "if", "so", "not", "no", "yes",
    }
    words = re.findall(r"[a-z]+", text)
    return {w for w in words if w not in stopwords and len(w) > 1}


# ---------------------------------------------------------------------------
# Intent classification
# ---------------------------------------------------------------------------


class Intent:
    EXIT = "exit"
    GREETING = "greeting"
    FAQ_MATCH = "faq_match"
    HELP = "help"
    FALLBACK = "fallback"


def _build_greeting_pattern(greetings: list[str]) -> re.Pattern:
    """Build a regex that matches any greeting phrase from the dataset."""
    escaped = [re.escape(g) for g in greetings]
    pattern = r"^(" + "|".join(escaped) + r")\b"
    return re.compile(pattern, re.IGNORECASE)


_EXIT_PATTERN = re.compile(r"^(bye|exit|quit|goodbye|see you|farewell)\b", re.IGNORECASE)
_HELP_PATTERN = re.compile(
    r"\b(help|commands|what can you do|options|assist)\b", re.IGNORECASE
)


def score_faq_match(query_tokens: set[str], faq_entry: dict) -> float:
    """Return an overlap score between query tokens and a FAQ question.

    Score = |intersection| / |union|  (Jaccard similarity)
    Returns 0.0 when either set is empty.
    """
    question_tokens = tokenize(normalize(faq_entry["question"]))
    if not query_tokens or not question_tokens:
        return 0.0
    intersection = query_tokens & question_tokens
    union = query_tokens | question_tokens
    return len(intersection) / len(union)


def find_best_faq(
    query: str,
    faqs: list[dict],
) -> tuple[Optional[dict], float]:
    """Find the best-matching FAQ entry for the given query.

    Returns (best_entry, score) or (None, 0.0) if nothing qualifies.
    """
    tokens = tokenize(normalize(query))
    best_entry = None
    best_score = 0.0

    for entry in faqs:
        score = score_faq_match(tokens, entry)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_score >= FAQ_MATCH_THRESHOLD:
        return best_entry, best_score
    return None, 0.0


def classify_intent(
    user_input: str,
    data: FAQData,
    greeting_pattern: Optional[re.Pattern] = None,
) -> tuple[str, Optional[dict]]:
    """Classify the user's input into an intent.

    Priority order (most specific first):
      1. EXIT
      2. GREETING
      3. FAQ_MATCH
      4. HELP
      5. FALLBACK

    Returns:
        (intent_name, extra_data)
        extra_data is the matched FAQ dict for FAQ_MATCH, else None.
    """
    normalised = normalize(user_input)

    # 1. Exit
    if _EXIT_PATTERN.match(normalised):
        return Intent.EXIT, None

    # 2. Greeting
    if greeting_pattern and greeting_pattern.match(normalised):
        return Intent.GREETING, None

    # 3. FAQ match
    best_entry, score = find_best_faq(normalised, data.faqs)
    if best_entry is not None:
        return Intent.FAQ_MATCH, best_entry

    # 4. Help
    if _HELP_PATTERN.search(normalised):
        return Intent.HELP, None

    # 5. Fallback
    return Intent.FALLBACK, None


# ---------------------------------------------------------------------------
# Response generation
# ---------------------------------------------------------------------------


def generate_response(
    intent: str,
    extra: Optional[dict],
    data: FAQData,
) -> str:
    """Map an intent to a response string.

    All non-fallback, non-greeting responses come from the actual dataset.
    """
    if intent == Intent.EXIT:
        return "Goodbye! Feel free to return if you have more questions."

    if intent == Intent.GREETING:
        return (
            "Hello! I'm the FAQ assistant. Ask me a question or type 'help' "
            "to see what I can do."
        )

    if intent == Intent.FAQ_MATCH and extra:
        return extra["answer"]

    if intent == Intent.HELP:
        return HELP_TEXT.strip()

    # Fallback — ask a clarifying question
    return (
        "I'm not sure I understood that. Could you rephrase your question? "
        "Type 'help' to see the topics I can assist with."
    )


# ---------------------------------------------------------------------------
# Interactive REPL
# ---------------------------------------------------------------------------


def run_assistant() -> None:
    """Run the interactive FAQ assistant loop."""
    data = load_faq()

    print("\n" + "=" * 55)
    print("  FAQ Conversation Assistant")
    print("=" * 55)

    if data is None:
        print(
            "  ⚠ FAQ dataset not found or malformed.\n"
            "  Limited functionality — only built-in responses available.\n"
        )
        data = FAQData(greetings=["hello", "hi", "hey"], faqs=[])
    else:
        print(f"  ✓ Loaded {len(data.greetings)} greetings, "
              f"{len(data.faqs)} FAQ entries.")

    print("  Type 'help' for available topics. Type 'bye' to exit.")
    print("=" * 55 + "\n")

    greeting_pattern = _build_greeting_pattern(data.greetings) if data.greetings else None

    try:
        while True:
            try:
                user_input = input("  You: ").strip()
            except EOFError:
                break

            if not user_input:
                continue

            intent, extra = classify_intent(user_input, data, greeting_pattern)
            response = generate_response(intent, extra, data)
            print(f"\n  Assistant: {response}\n")

            if intent == Intent.EXIT:
                break

    except KeyboardInterrupt:
        print("\n\n  Session interrupted. Goodbye!\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_assistant()
