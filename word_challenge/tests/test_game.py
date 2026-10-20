"""
word_challenge/tests/test_game.py
---------------------------------
Unit tests for the Hangman Word Challenge.

Run with:
    python -m unittest discover word_challenge/tests -v
or:
    python -m unittest word_challenge.tests.test_game -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Allow importing game.py from the parent directory.
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from word_challenge.game import (
    FALLBACK_WORDS,
    MAX_WRONG,
    MIN_WORD_LEN,
    MAX_WORD_LEN,
    build_masked_word,
    is_word_complete,
    load_words,
    pick_word,
    process_guess,
)


class TestWordLoading(unittest.TestCase):
    """Tests for load_words()."""

    def test_loads_from_valid_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as fh:
            fh.write("apple\nbanana\ncherry\norange\ngrape\n")
            path = Path(fh.name)
        try:
            words = load_words(path)
            self.assertIn("apple", words)
            self.assertIn("banana", words)
            self.assertIn("cherry", words)
        finally:
            path.unlink(missing_ok=True)

    def test_missing_file_returns_fallback(self):
        words = load_words(Path("/nonexistent/path/words.txt"))
        self.assertEqual(words, FALLBACK_WORDS)

    def test_filters_short_words(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as fh:
            fh.write("ab\nabc\napple\n")  # 'ab' and 'abc' are too short
            path = Path(fh.name)
        try:
            words = load_words(path)
            self.assertNotIn("ab", words)
            self.assertNotIn("abc", words)
            self.assertIn("apple", words)
        finally:
            path.unlink(missing_ok=True)

    def test_filters_long_words(self):
        long_word = "a" * (MAX_WORD_LEN + 1)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as fh:
            fh.write(f"{long_word}\napple\n")
            path = Path(fh.name)
        try:
            words = load_words(path)
            self.assertNotIn(long_word, words)
            self.assertIn("apple", words)
        finally:
            path.unlink(missing_ok=True)

    def test_filters_non_alpha_words(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as fh:
            fh.write("hello2\nword!\napple\n")
            path = Path(fh.name)
        try:
            words = load_words(path)
            self.assertNotIn("hello2", words)
            self.assertNotIn("word!", words)
            self.assertIn("apple", words)
        finally:
            path.unlink(missing_ok=True)

    def test_deduplicates_words(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as fh:
            fh.write("apple\nAPPLE\napple\nbanana\n")
            path = Path(fh.name)
        try:
            words = load_words(path)
            self.assertEqual(words.count("apple"), 1)
        finally:
            path.unlink(missing_ok=True)

    def test_empty_file_returns_fallback(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as fh:
            fh.write("")
            path = Path(fh.name)
        try:
            words = load_words(path)
            self.assertEqual(words, FALLBACK_WORDS)
        finally:
            path.unlink(missing_ok=True)

    def test_normalises_to_lowercase(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as fh:
            fh.write("APPLE\nBanana\n")
            path = Path(fh.name)
        try:
            words = load_words(path)
            self.assertIn("apple", words)
            self.assertIn("banana", words)
        finally:
            path.unlink(missing_ok=True)


class TestPickWord(unittest.TestCase):
    """Tests for pick_word()."""

    def test_picks_from_list(self):
        words = ["alpha", "bravo", "charlie", "delta"]
        for _ in range(20):
            word = pick_word(words)
            self.assertIn(word, words)

    def test_single_word_list(self):
        self.assertEqual(pick_word(["only"]), "only")


class TestMaskedWord(unittest.TestCase):
    """Tests for build_masked_word()."""

    def test_all_hidden_initially(self):
        result = build_masked_word("apple", set())
        self.assertEqual(result, "_ _ _ _ _")

    def test_partial_reveal(self):
        result = build_masked_word("apple", {"a", "e"})
        self.assertEqual(result, "a _ _ _ e")

    def test_full_reveal(self):
        result = build_masked_word("apple", set("apple"))
        self.assertEqual(result, "a p p l e")

    def test_repeated_letters(self):
        # "banana" with 'a' guessed
        result = build_masked_word("banana", {"a"})
        self.assertEqual(result, "_ a _ a _ a")


class TestIsWordComplete(unittest.TestCase):
    """Tests for is_word_complete()."""

    def test_incomplete_returns_false(self):
        self.assertFalse(is_word_complete("apple", {"a", "p"}))

    def test_complete_returns_true(self):
        self.assertTrue(is_word_complete("apple", set("apple")))

    def test_superset_of_guesses_still_complete(self):
        guessed = set("apple") | {"z", "q"}
        self.assertTrue(is_word_complete("apple", guessed))


class TestProcessGuess(unittest.TestCase):
    """Tests for process_guess()."""

    def test_new_correct_guess(self):
        is_new, is_correct = process_guess("a", "apple", set())
        self.assertTrue(is_new)
        self.assertTrue(is_correct)

    def test_new_wrong_guess(self):
        is_new, is_correct = process_guess("z", "apple", set())
        self.assertTrue(is_new)
        self.assertFalse(is_correct)

    def test_duplicate_guess_correct(self):
        is_new, is_correct = process_guess("a", "apple", {"a"})
        self.assertFalse(is_new)
        self.assertTrue(is_correct)

    def test_duplicate_guess_wrong(self):
        is_new, is_correct = process_guess("z", "apple", {"z"})
        self.assertFalse(is_new)
        self.assertFalse(is_correct)


class TestWinCondition(unittest.TestCase):
    """Simulate a winning game sequence."""

    def test_win_by_guessing_all_letters(self):
        word = "python"
        guessed: set[str] = set()
        wrong_count = 0

        for letter in word:
            is_new, is_correct = process_guess(letter, word, guessed)
            if is_new:
                guessed.add(letter)
            if not is_correct:
                wrong_count += 1

        self.assertTrue(is_word_complete(word, guessed))
        self.assertLess(wrong_count, MAX_WRONG)

    def test_win_with_some_wrong_guesses(self):
        word = "banana"
        guessed: set[str] = set()
        wrong_count = 0

        # Guess wrong letters first
        for wrong in ["z", "q", "x"]:
            is_new, is_correct = process_guess(wrong, word, guessed)
            guessed.add(wrong)
            if not is_correct:
                wrong_count += 1

        # Now guess correct letters
        for letter in set(word):
            is_new, is_correct = process_guess(letter, word, guessed)
            guessed.add(letter)

        self.assertTrue(is_word_complete(word, guessed))
        self.assertEqual(wrong_count, 3)


class TestLossCondition(unittest.TestCase):
    """Simulate a losing game sequence."""

    def test_loss_at_six_wrong_guesses(self):
        word = "apple"
        guessed: set[str] = set()
        wrong_count = 0
        wrong_letters = ["z", "q", "x", "j", "v", "w"]  # none in 'apple'

        for letter in wrong_letters:
            is_new, is_correct = process_guess(letter, word, guessed)
            self.assertTrue(is_new)
            self.assertFalse(is_correct)
            guessed.add(letter)
            wrong_count += 1

        self.assertEqual(wrong_count, MAX_WRONG)
        self.assertFalse(is_word_complete(word, guessed))


class TestSixErrorBoundary(unittest.TestCase):
    """Verify exactly 6 wrong guesses trigger loss, 5 do not."""

    def _count_wrongs(self, word: str, wrong_letters: list[str]) -> int:
        guessed: set[str] = set()
        count = 0
        for letter in wrong_letters:
            is_new, is_correct = process_guess(letter, word, guessed)
            if is_new and not is_correct:
                count += 1
            guessed.add(letter)
        return count

    def test_five_wrongs_game_continues(self):
        count = self._count_wrongs("python", ["z", "q", "x", "j", "v"])
        self.assertEqual(count, 5)
        self.assertLess(count, MAX_WRONG)

    def test_six_wrongs_game_over(self):
        count = self._count_wrongs("python", ["z", "q", "x", "j", "v", "w"])
        self.assertEqual(count, MAX_WRONG)


if __name__ == "__main__":
    unittest.main(verbosity=2)
