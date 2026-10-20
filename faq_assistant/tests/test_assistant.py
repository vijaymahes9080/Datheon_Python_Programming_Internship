"""
faq_assistant/tests/test_assistant.py
--------------------------------------
Unit tests for the FAQ Conversation Assistant.

Run with:
    python -m unittest discover faq_assistant/tests -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from faq_assistant.assistant import (
    FAQ_MATCH_THRESHOLD,
    FAQData,
    Intent,
    classify_intent,
    find_best_faq,
    generate_response,
    load_faq,
    normalize,
    score_faq_match,
    tokenize,
    _build_greeting_pattern,
)


# ---------------------------------------------------------------------------
# Sample dataset
# ---------------------------------------------------------------------------

SAMPLE_DATA = FAQData(
    greetings=["hello", "hi", "hey", "good morning", "good afternoon"],
    faqs=[
        {
            "question": "What are your hours of operation?",
            "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST.",
        },
        {
            "question": "How do I submit my internship project?",
            "answer": "You can submit your public GitHub repository link through your Student Workspace.",
        },
        {
            "question": "When will I receive my certificate?",
            "answer": "Certificates are reviewed and issued within 3-5 business days after your code review.",
        },
    ],
)

GREETING_PATTERN = _build_greeting_pattern(SAMPLE_DATA.greetings)


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

class TestFAQLoading(unittest.TestCase):
    """Tests for load_faq()."""

    def _write_json(self, data: dict) -> Path:
        fh = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(data, fh)
        fh.close()
        return Path(fh.name)

    def test_loads_valid_json(self):
        path = self._write_json({
            "greetings": ["hello", "hi"],
            "faqs": [{"question": "Q?", "answer": "A."}]
        })
        try:
            result = load_faq(path)
            self.assertIsNotNone(result)
            self.assertEqual(result.greetings, ["hello", "hi"])
            self.assertEqual(len(result.faqs), 1)
        finally:
            path.unlink(missing_ok=True)

    def test_missing_file_returns_none(self):
        result = load_faq(Path("/nonexistent/sample_faq.json"))
        self.assertIsNone(result)

    def test_malformed_json_returns_none(self):
        fh = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        fh.write("{not valid json")
        fh.close()
        path = Path(fh.name)
        try:
            result = load_faq(path)
            self.assertIsNone(result)
        finally:
            path.unlink(missing_ok=True)

    def test_non_dict_root_returns_none(self):
        path = self._write_json([1, 2, 3])
        try:
            result = load_faq(path)
            self.assertIsNone(result)
        finally:
            path.unlink(missing_ok=True)

    def test_missing_faqs_key_returns_empty_list(self):
        path = self._write_json({"greetings": ["hi"]})
        try:
            result = load_faq(path)
            self.assertIsNotNone(result)
            self.assertEqual(result.faqs, [])
        finally:
            path.unlink(missing_ok=True)

    def test_faq_entry_missing_answer_excluded(self):
        path = self._write_json({
            "greetings": [],
            "faqs": [
                {"question": "Valid Q?", "answer": "Valid A."},
                {"question": "No answer here"},  # malformed
            ]
        })
        try:
            result = load_faq(path)
            self.assertEqual(len(result.faqs), 1)
        finally:
            path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

class TestNormalize(unittest.TestCase):
    """Tests for normalize()."""

    def test_lowercase(self):
        self.assertEqual(normalize("HELLO"), "hello")

    def test_strips_whitespace(self):
        self.assertEqual(normalize("  hello  "), "hello")

    def test_collapses_internal_whitespace(self):
        self.assertEqual(normalize("hello   world"), "hello world")

    def test_empty_string(self):
        self.assertEqual(normalize(""), "")

    def test_mixed_case_and_spaces(self):
        self.assertEqual(normalize("  How Do I  Submit  "), "how do i submit")


class TestTokenize(unittest.TestCase):
    """Tests for tokenize()."""

    def test_removes_stopwords(self):
        tokens = tokenize("what are your hours")
        self.assertNotIn("what", tokens)
        self.assertNotIn("are", tokens)
        self.assertNotIn("your", tokens)
        self.assertIn("hours", tokens)

    def test_extracts_meaningful_words(self):
        tokens = tokenize("submit internship project")
        self.assertIn("submit", tokens)
        self.assertIn("internship", tokens)
        self.assertIn("project", tokens)

    def test_single_char_words_excluded(self):
        tokens = tokenize("a b c hello")
        self.assertNotIn("a", tokens)
        self.assertNotIn("b", tokens)
        self.assertNotIn("c", tokens)
        self.assertIn("hello", tokens)


# ---------------------------------------------------------------------------
# FAQ scoring and matching
# ---------------------------------------------------------------------------

class TestFAQScoring(unittest.TestCase):
    """Tests for score_faq_match() and find_best_faq()."""

    def test_exact_keyword_match_high_score(self):
        entry = {"question": "How do I submit my internship project?", "answer": "A."}
        tokens = tokenize("submit internship project")
        score = score_faq_match(tokens, entry)
        self.assertGreater(score, FAQ_MATCH_THRESHOLD)

    def test_unrelated_query_low_score(self):
        entry = {"question": "What are your hours of operation?", "answer": "A."}
        tokens = tokenize("python programming language")
        score = score_faq_match(tokens, entry)
        self.assertLess(score, FAQ_MATCH_THRESHOLD)

    def test_empty_query_returns_zero(self):
        entry = {"question": "When will I receive my certificate?", "answer": "A."}
        score = score_faq_match(set(), entry)
        self.assertEqual(score, 0.0)

    def test_find_best_faq_hours(self):
        entry, score = find_best_faq("what are your hours", SAMPLE_DATA.faqs)
        self.assertIsNotNone(entry)
        self.assertIn("hours", entry["question"].lower())

    def test_find_best_faq_certificate(self):
        entry, score = find_best_faq("when will I receive my certificate", SAMPLE_DATA.faqs)
        self.assertIsNotNone(entry)
        self.assertIn("certificate", entry["question"].lower())

    def test_find_best_faq_submit(self):
        entry, score = find_best_faq("how do I submit my project", SAMPLE_DATA.faqs)
        self.assertIsNotNone(entry)
        self.assertIn("submit", entry["question"].lower())

    def test_no_match_returns_none(self):
        entry, score = find_best_faq("xyzzy plugh quux blorb", SAMPLE_DATA.faqs)
        self.assertIsNone(entry)
        self.assertEqual(score, 0.0)


# ---------------------------------------------------------------------------
# Intent classification
# ---------------------------------------------------------------------------

class TestIntentClassification(unittest.TestCase):
    """Tests for classify_intent()."""

    def _classify(self, text: str) -> str:
        intent, _ = classify_intent(text, SAMPLE_DATA, GREETING_PATTERN)
        return intent

    def test_exit_bye(self):
        self.assertEqual(self._classify("bye"), Intent.EXIT)

    def test_exit_exit(self):
        self.assertEqual(self._classify("exit"), Intent.EXIT)

    def test_exit_quit(self):
        self.assertEqual(self._classify("quit"), Intent.EXIT)

    def test_exit_uppercase(self):
        self.assertEqual(self._classify("BYE"), Intent.EXIT)
        self.assertEqual(self._classify("QUIT"), Intent.EXIT)

    def test_greeting_hello(self):
        self.assertEqual(self._classify("hello"), Intent.GREETING)

    def test_greeting_hi(self):
        self.assertEqual(self._classify("hi"), Intent.GREETING)

    def test_greeting_hey(self):
        self.assertEqual(self._classify("hey"), Intent.GREETING)

    def test_greeting_good_morning(self):
        self.assertEqual(self._classify("good morning"), Intent.GREETING)

    def test_faq_hours(self):
        self.assertEqual(self._classify("what are your hours"), Intent.FAQ_MATCH)

    def test_faq_certificate(self):
        self.assertEqual(self._classify("when will I get my certificate"), Intent.FAQ_MATCH)

    def test_faq_submit(self):
        self.assertEqual(self._classify("how submit project"), Intent.FAQ_MATCH)

    def test_help_intent(self):
        self.assertEqual(self._classify("help"), Intent.HELP)

    def test_help_what_can_you_do(self):
        self.assertEqual(self._classify("what can you do"), Intent.HELP)

    def test_fallback_unrecognised(self):
        self.assertEqual(self._classify("xyzzy plugh quux blorb frobnic"), Intent.FALLBACK)

    def test_exit_takes_priority_over_greeting(self):
        # "bye" should be EXIT, not greeted
        self.assertEqual(self._classify("bye"), Intent.EXIT)


# ---------------------------------------------------------------------------
# Response generation
# ---------------------------------------------------------------------------

class TestResponseGeneration(unittest.TestCase):
    """Tests for generate_response()."""

    def test_exit_response_contains_goodbye(self):
        resp = generate_response(Intent.EXIT, None, SAMPLE_DATA)
        self.assertIn("oodbye", resp)

    def test_greeting_response_is_welcoming(self):
        resp = generate_response(Intent.GREETING, None, SAMPLE_DATA)
        self.assertTrue(len(resp) > 0)

    def test_faq_response_comes_from_dataset(self):
        entry = SAMPLE_DATA.faqs[0]  # hours of operation
        resp = generate_response(Intent.FAQ_MATCH, entry, SAMPLE_DATA)
        self.assertEqual(resp, entry["answer"])

    def test_fallback_asks_clarifying_question(self):
        resp = generate_response(Intent.FALLBACK, None, SAMPLE_DATA)
        # Should contain a question or suggestion, not a made-up fact
        self.assertTrue("?" in resp or "help" in resp.lower())

    def test_help_response_lists_topics(self):
        resp = generate_response(Intent.HELP, None, SAMPLE_DATA)
        self.assertIn("help", resp.lower())


# ---------------------------------------------------------------------------
# Ambiguous input
# ---------------------------------------------------------------------------

class TestAmbiguousInput(unittest.TestCase):
    """Verify graceful handling of edge cases."""

    def test_empty_input_does_not_crash(self):
        intent, extra = classify_intent("", SAMPLE_DATA, GREETING_PATTERN)
        self.assertIn(intent, vars(Intent).values())

    def test_whitespace_only_does_not_crash(self):
        intent, extra = classify_intent("   ", SAMPLE_DATA, GREETING_PATTERN)
        self.assertIn(intent, vars(Intent).values())

    def test_very_long_input(self):
        long_input = "what " * 200 + "hours"
        entry, score = find_best_faq(long_input, SAMPLE_DATA.faqs)
        # Either finds a match or returns None — must not crash
        self.assertIn(score >= FAQ_MATCH_THRESHOLD, [True, False])

    def test_no_faq_data_returns_fallback(self):
        empty_data = FAQData(greetings=["hello"], faqs=[])
        intent, extra = classify_intent("what are your hours", empty_data, GREETING_PATTERN)
        self.assertEqual(intent, Intent.FALLBACK)


if __name__ == "__main__":
    unittest.main(verbosity=2)
