"""
market_journal/tests/test_tracker.py
-------------------------------------
Unit tests for the Portfolio Market Journal.

Run with:
    python -m unittest discover market_journal/tests -v
"""

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from market_journal.tracker import (
    calculate_portfolio_totals,
    calculate_position,
    export_csv,
    load_constituents,
    validate_ticker,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_position(
    ticker="TEST",
    company="Test Corp",
    purchase_price=100.0,
    shares=10.0,
    current_price=None,
    price_source="unavailable",
):
    return {
        "ticker": ticker,
        "company": company,
        "purchase_price": purchase_price,
        "shares": shares,
        "current_price": current_price,
        "price_source": price_source,
        "added_at": "2026-01-01T00:00:00",
    }


# ---------------------------------------------------------------------------
# Calculations
# ---------------------------------------------------------------------------

class TestCalculatePosition(unittest.TestCase):
    """Tests for calculate_position()."""

    def test_basic_gain(self):
        pos = _make_position(purchase_price=100.0, shares=10, current_price=120.0)
        result = calculate_position(pos)
        self.assertAlmostEqual(result["invested_value"], 1000.0)
        self.assertAlmostEqual(result["current_value"], 1200.0)
        self.assertAlmostEqual(result["gain_loss"], 200.0)
        self.assertAlmostEqual(result["pct_change"], 20.0)

    def test_basic_loss(self):
        pos = _make_position(purchase_price=200.0, shares=5, current_price=150.0)
        result = calculate_position(pos)
        self.assertAlmostEqual(result["invested_value"], 1000.0)
        self.assertAlmostEqual(result["current_value"], 750.0)
        self.assertAlmostEqual(result["gain_loss"], -250.0)
        self.assertAlmostEqual(result["pct_change"], -25.0)

    def test_breakeven(self):
        pos = _make_position(purchase_price=50.0, shares=4, current_price=50.0)
        result = calculate_position(pos)
        self.assertAlmostEqual(result["gain_loss"], 0.0)
        self.assertAlmostEqual(result["pct_change"], 0.0)

    def test_unpriced_position_returns_none(self):
        pos = _make_position(purchase_price=100.0, shares=5, current_price=None)
        result = calculate_position(pos)
        self.assertAlmostEqual(result["invested_value"], 500.0)
        self.assertIsNone(result["current_value"])
        self.assertIsNone(result["gain_loss"])
        self.assertIsNone(result["pct_change"])

    def test_fractional_shares(self):
        pos = _make_position(purchase_price=10.0, shares=0.5, current_price=20.0)
        result = calculate_position(pos)
        self.assertAlmostEqual(result["invested_value"], 5.0)
        self.assertAlmostEqual(result["current_value"], 10.0)
        self.assertAlmostEqual(result["gain_loss"], 5.0)
        self.assertAlmostEqual(result["pct_change"], 100.0)


class TestPortfolioTotals(unittest.TestCase):
    """Tests for calculate_portfolio_totals()."""

    def test_all_priced(self):
        portfolio = [
            _make_position(purchase_price=100.0, shares=10, current_price=110.0),
            _make_position(purchase_price=200.0, shares=5, current_price=180.0),
        ]
        totals = calculate_portfolio_totals(portfolio)
        self.assertAlmostEqual(totals["total_invested"], 2000.0)
        self.assertAlmostEqual(totals["total_current_value"], 2000.0)  # 1100 + 900
        self.assertFalse(totals["is_partial"])
        self.assertEqual(totals["unpriced_count"], 0)

    def test_partial_portfolio_flagged(self):
        portfolio = [
            _make_position(purchase_price=100.0, shares=10, current_price=110.0),
            _make_position(purchase_price=200.0, shares=5, current_price=None),
        ]
        totals = calculate_portfolio_totals(portfolio)
        self.assertTrue(totals["is_partial"])
        self.assertEqual(totals["unpriced_count"], 1)
        self.assertEqual(totals["priced_count"], 1)

    def test_all_unpriced_returns_none_totals(self):
        portfolio = [
            _make_position(purchase_price=100.0, shares=5, current_price=None),
            _make_position(purchase_price=200.0, shares=3, current_price=None),
        ]
        totals = calculate_portfolio_totals(portfolio)
        self.assertIsNone(totals["total_current_value"])
        self.assertIsNone(totals["total_gain_loss"])
        self.assertIsNone(totals["total_pct_change"])
        self.assertEqual(totals["unpriced_count"], 2)
        self.assertTrue(totals["is_partial"])

    def test_single_position(self):
        portfolio = [_make_position(purchase_price=50.0, shares=2, current_price=60.0)]
        totals = calculate_portfolio_totals(portfolio)
        self.assertAlmostEqual(totals["total_invested"], 100.0)
        self.assertAlmostEqual(totals["total_current_value"], 120.0)
        self.assertAlmostEqual(totals["total_gain_loss"], 20.0)


# ---------------------------------------------------------------------------
# Ticker validation
# ---------------------------------------------------------------------------

class TestTickerValidation(unittest.TestCase):
    """Tests for validate_ticker()."""

    MOCK_CONSTITUENTS = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "GOOG": "Alphabet Inc.",
    }

    def test_valid_ticker_found(self):
        found, company = validate_ticker("AAPL", self.MOCK_CONSTITUENTS)
        self.assertTrue(found)
        self.assertEqual(company, "Apple Inc.")

    def test_invalid_ticker_not_found(self):
        found, company = validate_ticker("ZZZZ", self.MOCK_CONSTITUENTS)
        self.assertFalse(found)
        self.assertEqual(company, "")

    def test_case_insensitive_lookup(self):
        found, company = validate_ticker("msft", self.MOCK_CONSTITUENTS)
        self.assertTrue(found)
        self.assertEqual(company, "Microsoft Corporation")

    def test_empty_constituents_always_not_found(self):
        found, company = validate_ticker("AAPL", {})
        self.assertFalse(found)

    def test_missing_constituents_file(self):
        result = load_constituents(Path("/nonexistent/constituents.csv"))
        self.assertEqual(result, {})


class TestLoadConstituents(unittest.TestCase):
    """Tests for load_constituents() with temp CSV files."""

    def test_loads_valid_csv(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False,
            encoding="utf-8", newline=""
        ) as fh:
            writer = csv.writer(fh)
            writer.writerow(["Symbol", "Security", "GICS Sector"])
            writer.writerow(["AAPL", "Apple Inc.", "Technology"])
            writer.writerow(["MSFT", "Microsoft Corporation", "Technology"])
            path = Path(fh.name)
        try:
            result = load_constituents(path)
            self.assertEqual(result["AAPL"], "Apple Inc.")
            self.assertEqual(result["MSFT"], "Microsoft Corporation")
        finally:
            path.unlink(missing_ok=True)

    def test_handles_malformed_csv_gracefully(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as fh:
            fh.write("NOT,A,VALID,HEADER\nwrong\n")
            path = Path(fh.name)
        try:
            result = load_constituents(path)
            self.assertIsInstance(result, dict)
        finally:
            path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

class TestCSVExport(unittest.TestCase):
    """Tests for export_csv()."""

    def test_exports_file(self):
        portfolio = [
            _make_position(ticker="AAPL", purchase_price=150.0, shares=10, current_price=175.0),
            _make_position(ticker="MSFT", purchase_price=300.0, shares=5, current_price=None),
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_csv(portfolio, Path(tmpdir))
            self.assertTrue(path.exists())

    def test_csv_contains_expected_columns(self):
        portfolio = [_make_position(purchase_price=100.0, shares=5, current_price=120.0)]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_csv(portfolio, Path(tmpdir))
            with path.open(encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                headers = reader.fieldnames or []
            self.assertIn("ticker", headers)
            self.assertIn("invested_value", headers)
            self.assertIn("gain_loss", headers)
            self.assertIn("pct_change", headers)
            self.assertIn("price_source", headers)

    def test_unpriced_positions_show_empty_not_zero(self):
        portfolio = [_make_position(purchase_price=100.0, shares=5, current_price=None)]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_csv(portfolio, Path(tmpdir))
            with path.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(rows[0]["current_value"], "")
            self.assertEqual(rows[0]["gain_loss"], "")

    def test_readable_back_correctly(self):
        portfolio = [
            _make_position(ticker="TEST", purchase_price=50.0, shares=20, current_price=60.0)
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_csv(portfolio, Path(tmpdir))
            with path.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["ticker"], "TEST")
            self.assertAlmostEqual(float(rows[0]["invested_value"]), 1000.0)
            self.assertAlmostEqual(float(rows[0]["current_value"]), 1200.0)
            self.assertAlmostEqual(float(rows[0]["gain_loss"]), 200.0)


# ---------------------------------------------------------------------------
# Input validation edge cases
# ---------------------------------------------------------------------------

class TestInputEdgeCases(unittest.TestCase):
    """Edge cases in calculations."""

    def test_large_number_of_positions(self):
        portfolio = [
            _make_position(purchase_price=100.0, shares=1, current_price=110.0)
            for _ in range(50)
        ]
        totals = calculate_portfolio_totals(portfolio)
        self.assertAlmostEqual(totals["total_invested"], 5000.0)
        self.assertAlmostEqual(totals["total_gain_loss"], 500.0)
        self.assertFalse(totals["is_partial"])

    def test_zero_shares_invested_is_zero(self):
        # Edge case: should not cause division by zero in pct_change
        pos = _make_position(purchase_price=100.0, shares=0.0, current_price=100.0)
        result = calculate_position(pos)
        self.assertAlmostEqual(result["invested_value"], 0.0)
        # pct_change should be 0 not crash
        self.assertAlmostEqual(result["pct_change"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
