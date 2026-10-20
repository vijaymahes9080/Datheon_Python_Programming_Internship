# Validation, Testing, & Quality Verification Report

**Python Practical Lab** — Verification Matrix & Audit

---

## 1. Executive Summary

All four tasks in the **Python Practical Lab** suite have been implemented independently, verified for architectural compliance, equipped with comprehensive `unittest` suites, and published alongside interactive browser showcases.

| Component | Task | Core Engine | Test Suite | Web Showcase | Status |
|---|---|---|---|---|---|
| **Word Challenge** | Task 01 | `word_challenge/game.py` (376 lines) | `test_game.py` (282 lines) | `word_challenge/index.html` | ✅ Verified |
| **Market Journal** | Task 02 | `market_journal/tracker.py` (447 lines) | `test_tracker.py` (290 lines) | `market_journal/index.html` | ✅ Verified |
| **Desktop Sorter** | Task 03 | `desktop_sorter/sorter.py` (422 lines) | `test_sorter.py` (313 lines) | `desktop_sorter/index.html` | ✅ Verified |
| **FAQ Assistant** | Task 04 | `faq_assistant/assistant.py` (308 lines) | `test_assistant.py` (344 lines) | `faq_assistant/index.html` | ✅ Verified |

---

## 2. Test Suite Architecture & Coverage Matrix

### Task 01: Word Challenge (`word_challenge/tests/test_game.py`)
- `TestWordLoading`:
  - `test_load_words_normal_file`: Validates word loading from text files.
  - `test_load_words_filters_short_and_long`: Asserts rejection of words $<4$ or $>12$ characters.
  - `test_load_words_missing_file_fallback`: Asserts automatic fallback to embedded 50-word vocabulary without crash.
  - `test_load_words_empty_file_fallback`: Handles zero-byte input files gracefully.
- `TestGameLogic`:
  - `test_check_guess_correct`: Asserts matching letters return `(is_new=True, is_correct=True)`.
  - `test_check_guess_incorrect`: Asserts non-matching letters return `(is_new=True, is_correct=False)`.
  - `test_check_guess_duplicate`: Repeated guess returns `(is_new=False, ...)` with zero penalties.
  - `test_display_state`: Verifies masked string rendering (`_ p p _ e`).
  - `test_gallows_stages_length`: Asserts exactly 7 stages (0 to 6 errors).
- `TestWinLossConditions`:
  - `test_victory_scenario`: Simulates complete correct sequence leading to victory flag.
  - `test_defeat_scenario`: Simulates 6 wrong guesses triggering terminal game over state.

### Task 02: Portfolio Tracker (`market_journal/tests/test_tracker.py`)
- `TestCalculations`:
  - `test_gain_calculation`: Asserts `(current_price * shares) - (purchase_price * shares)`.
  - `test_loss_calculation`: Negative returns calculated accurately.
  - `test_break_even`: Zero gain/loss handled cleanly.
  - `test_percentage_calculation`: Accurately formats percentage return.
- `TestUnpricedHolding`:
  - `test_unpriced_position_display`: Market value returns `UNAVAILABLE` rather than $0.
  - `test_unpriced_gain_loss`: Return metrics return `N/A`.
- `TestPortfolioTotals`:
  - `test_all_priced_totals`: Complete summation across all priced equities.
  - `test_mixed_portfolio_is_partial`: Asserts `is_partial = True` flag when unpriced securities are present.
- `TestCSVExport`:
  - `test_export_csv_schema`: Verifies header row and numeric precision.
  - `test_export_csv_roundtrip`: Reads back generated CSV to confirm persistence.
- `TestTickerValidation`:
  - `test_known_ticker`: Confirms match against S&P 500 constituents.
  - `test_unknown_ticker`: Warns user while allowing manual entry.

### Task 03: Desktop Sorter (`desktop_sorter/tests/test_sorter.py`)
- `TestClassification`:
  - `test_document_extensions`: `.pdf`, `.docx`, `.txt`, `.rtf`, `.odt` &rarr; `Documents`.
  - `test_image_extensions`: `.jpg`, `.png`, `.gif`, `.svg`, `.webp` &rarr; `Images`.
  - `test_video_audio_extensions`: `.mp4`, `.mp3`, `.wav` &rarr; `Videos` / `Audio`.
  - `test_code_and_archives`: `.py`, `.json`, `.zip`, `.tar.gz` &rarr; `Code` / `Archives`.
  - `test_unknown_extension`: Fallback to `Other`.
- `TestCollisionPolicy`:
  - `test_collision_resolution`: `file.pdf` &rarr; `file_1.pdf` &rarr; `file_2.pdf`.
  - `test_no_overwrite_guarantee`: Existing file content remains byte-identical.
- `TestUnsafeTargets`:
  - `test_reject_filesystem_root`: Rejects `C:\` and `/`.
  - `test_reject_script_directory`: Rejects sorter's own code folder.
- `TestDryRun`:
  - `test_dry_run_moves_nothing`: Validates zero file movement in preview mode.
- `TestLogOutput`:
  - `test_audit_log_created`: Validates creation and content of timestamped `.log` files.

### Task 04: FAQ Assistant (`faq_assistant/tests/test_assistant.py`)
- `TestFAQLoading`:
  - `test_load_valid_faq`: Successfully ingests `sample_faq.json`.
  - `test_missing_file_fallback`: Falls back to embedded data structure.
  - `test_corrupt_json_fallback`: Resilient against syntax errors.
- `TestNormalization`:
  - `test_case_and_whitespace`: Normalizes casing, strips leading/trailing spaces.
  - `test_punctuation_removal`: Strips question marks, commas, periods.
- `TestIntentRecognition`:
  - `test_exit_intent`: Detects `bye`, `exit`, `quit`.
  - `test_greeting_intent`: Detects `hello`, `hi`, `good morning`.
  - `test_help_intent`: Detects `help`, `commands`.
  - `test_faq_intent`: Correctly matches dataset questions.
  - `test_fallback_intent`: Correctly routes unrecognized queries to clarifying questions.
- `TestFAQMatching`:
  - `test_jaccard_scoring`: Threshold validation on exact and fuzzy phrasing.

---

## 3. Web Portal Link & Asset Audit

Every page has been audited for internal link integrity:

| Origin Page | Target Link | Target Path | Link Status |
|---|---|---|---|
| `index.html` | Card 01 | `word_challenge/index.html` | ✅ OK (200) |
| `index.html` | Card 02 | `market_journal/index.html` | ✅ OK (200) |
| `index.html` | Card 03 | `desktop_sorter/index.html` | ✅ OK (200) |
| `index.html` | Card 04 | `faq_assistant/index.html` | ✅ OK (200) |
| `index.html` | Design Doc | `documentation/DESIGN.md` | ✅ OK (200) |
| `index.html` | Data Doc | `documentation/DATA_SOURCES.md` | ✅ OK (200) |
| `index.html` | Validation Doc | `documentation/VALIDATION.md` | ✅ OK (200) |
| `word_challenge/index.html` | Home Link | `../index.html` | ✅ OK (200) |
| `market_journal/index.html` | Home Link | `../index.html` | ✅ OK (200) |
| `desktop_sorter/index.html` | Home Link | `../index.html` | ✅ OK (200) |
| `faq_assistant/index.html` | Home Link | `../index.html` | ✅ OK (200) |
| All Pages | Shared Stylesheet | `web/styles/main.css` | ✅ OK (200) |

---

## 4. Execution Commands Quick Reference

```bash
# Task 01: Hangman
python word_challenge/game.py
python -m unittest word_challenge/tests/test_game.py -v

# Task 02: Stock Portfolio
python market_journal/tracker.py
python -m unittest market_journal/tests/test_tracker.py -v

# Task 03: Desktop Sorter
python desktop_sorter/sorter.py --dry-run
python desktop_sorter/sorter.py --confirm
python -m unittest desktop_sorter/tests/test_sorter.py -v

# Task 04: FAQ Assistant
python faq_assistant/assistant.py
python -m unittest faq_assistant/tests/test_assistant.py -v
```
