"""
market_journal/tracker.py
--------------------------
Portfolio Market Journal — terminal-based stock portfolio performance tracker.

Entry point: python market_journal/tracker.py

DISCLAIMER: This application is for educational purposes only and does not
constitute investment advice. Price data is entered manually and is not
verified, endorsed, or sourced from any financial data provider. Do not make
investment decisions based on this tool.

Features:
  - Add stock positions (ticker, purchase price, quantity, optional current price)
  - Validate tickers against S&P 500 constituents dataset
  - Calculate gain/loss per position
  - Report partial portfolio totals when some prices are unknown
  - Export a timestamped CSV report
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RESOURCES_DIR = Path(__file__).parent / "resources"
CONSTITUENTS_FILE = RESOURCES_DIR / "constituents.csv"
REPORTS_DIR = Path(__file__).parent / "resources"

PRICE_SOURCE_MANUAL = "manual"
PRICE_SOURCE_UNAVAILABLE = "unavailable"

DISCLAIMER = """
╔══════════════════════════════════════════════════════════════╗
║            EDUCATIONAL USE DISCLAIMER                        ║
║                                                              ║
║  This application is for EDUCATIONAL PURPOSES ONLY.         ║
║  It does NOT provide investment advice.                      ║
║  Price data is entered manually — no live market data.       ║
║  Do not base financial decisions on this tool.               ║
╚══════════════════════════════════════════════════════════════╝
"""

# ---------------------------------------------------------------------------
# Data types (plain dicts — no external dependencies)
# ---------------------------------------------------------------------------

# Position dict keys:
#   ticker        str    — e.g. "AAPL"
#   company       str    — company name from dataset, or ticker if unknown
#   purchase_price float — price per share at time of purchase
#   shares        float  — number of shares held
#   current_price float | None — current price per share (None if unknown)
#   price_source  str    — PRICE_SOURCE_MANUAL or PRICE_SOURCE_UNAVAILABLE
#   added_at      str    — ISO timestamp

# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------


def load_constituents(path: Path = CONSTITUENTS_FILE) -> dict[str, str]:
    """Load S&P 500 constituents into a {symbol: company_name} mapping.

    Returns an empty dict if the file is missing or malformed.
    The CSV columns are: Symbol, Security, GICS Sector, ...
    """
    if not path.exists():
        return {}

    constituents: dict[str, str] = {}
    try:
        with path.open(encoding="utf-8", errors="replace", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                symbol = (row.get("Symbol") or "").strip().upper()
                company = (row.get("Security") or "").strip()
                if symbol:
                    constituents[symbol] = company
    except (OSError, csv.Error):
        return {}

    return constituents


def validate_ticker(
    ticker: str,
    constituents: dict[str, str],
) -> tuple[bool, str]:
    """Check if a ticker exists in the constituents dataset.

    Args:
        ticker: Uppercase ticker symbol.
        constituents: Mapping from load_constituents().

    Returns:
        (found, company_name) — company_name is '' when not found.
    """
    ticker = ticker.strip().upper()
    if ticker in constituents:
        return True, constituents[ticker]
    return False, ""


# ---------------------------------------------------------------------------
# Calculations (pure functions — no I/O)
# ---------------------------------------------------------------------------


def calculate_position(position: dict) -> dict:
    """Compute derived metrics for a single position.

    Returns a new dict with added keys:
      invested_value   float — purchase_price * shares
      current_value    float | None
      gain_loss        float | None
      pct_change       float | None
    """
    invested = position["purchase_price"] * position["shares"]
    current_price = position["current_price"]

    if current_price is not None:
        current_value = current_price * position["shares"]
        gain_loss = current_value - invested
        pct_change = (gain_loss / invested * 100) if invested != 0 else 0.0
    else:
        current_value = None
        gain_loss = None
        pct_change = None

    return {
        **position,
        "invested_value": invested,
        "current_value": current_value,
        "gain_loss": gain_loss,
        "pct_change": pct_change,
    }


def calculate_portfolio_totals(portfolio: list[dict]) -> dict:
    """Aggregate portfolio-level totals.

    If any positions are unpriced, the current_value total is PARTIAL and
    this is clearly flagged — it is never presented as a complete valuation.

    Returns:
        {
            total_invested: float,
            total_current_value: float | None,
            total_gain_loss: float | None,
            total_pct_change: float | None,
            priced_count: int,
            unpriced_count: int,
            is_partial: bool,
        }
    """
    enriched = [calculate_position(p) for p in portfolio]

    total_invested = sum(p["invested_value"] for p in enriched)
    priced = [p for p in enriched if p["current_value"] is not None]
    unpriced_count = len(enriched) - len(priced)

    if priced:
        total_current = sum(p["current_value"] for p in priced)
        total_gain_loss = total_current - sum(p["invested_value"] for p in priced)
        total_pct = (
            total_gain_loss / sum(p["invested_value"] for p in priced) * 100
            if sum(p["invested_value"] for p in priced) != 0
            else 0.0
        )
    else:
        total_current = None
        total_gain_loss = None
        total_pct = None

    return {
        "total_invested": total_invested,
        "total_current_value": total_current,
        "total_gain_loss": total_gain_loss,
        "total_pct_change": total_pct,
        "priced_count": len(priced),
        "unpriced_count": unpriced_count,
        "is_partial": unpriced_count > 0,
    }


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def prompt_float(prompt: str, min_value: float = 0.0) -> Optional[float]:
    """Prompt for a non-negative float. Returns None on blank input."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            value = float(raw)
            if value < min_value:
                print(f"  Value must be ≥ {min_value}. Try again.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid number (e.g. 150.75). Try again.")


def prompt_positive_float(prompt: str) -> float:
    """Prompt for a strictly positive float. Required — no blank allowed."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                print("  Value must be greater than zero. Try again.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid positive number. Try again.")


def prompt_ticker() -> str:
    """Prompt for a non-empty ticker symbol."""
    while True:
        raw = input("  Ticker symbol (e.g. AAPL): ").strip().upper()
        if raw and raw.isalpha() and len(raw) <= 5:
            return raw
        print("  Enter a valid ticker (1–5 letters, e.g. AAPL).")


# ---------------------------------------------------------------------------
# Portfolio I/O
# ---------------------------------------------------------------------------


def add_position(
    portfolio: list[dict],
    constituents: dict[str, str],
) -> None:
    """Interactively add a new position to the portfolio."""
    print("\n  — Add New Position —")
    ticker = prompt_ticker()
    found, company = validate_ticker(ticker, constituents)

    if found:
        print(f"  ✓ {ticker} — {company} (found in S&P 500 dataset)")
    else:
        print(f"  ⚠ {ticker} not found in S&P 500 dataset. "
              "It may be valid — proceeding anyway.")
        company = ticker  # Use ticker as display name if unknown

    purchase_price = prompt_positive_float("  Purchase price per share ($): ")
    shares = prompt_positive_float("  Number of shares: ")

    print("  Current price per share (press Enter to skip / mark unavailable): ", end="")
    current_price = prompt_float("", min_value=0.0)
    price_source = PRICE_SOURCE_MANUAL if current_price is not None else PRICE_SOURCE_UNAVAILABLE

    position = {
        "ticker": ticker,
        "company": company,
        "purchase_price": purchase_price,
        "shares": shares,
        "current_price": current_price,
        "price_source": price_source,
        "added_at": datetime.now().isoformat(timespec="seconds"),
    }
    portfolio.append(position)
    print(f"  ✓ Added {ticker} ({shares} shares @ ${purchase_price:.2f})")


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------


def _fmt_currency(value: Optional[float]) -> str:
    if value is None:
        return "UNAVAILABLE"
    sign = "+" if value >= 0 else ""
    return f"{sign}${value:,.2f}"


def _fmt_pct(value: Optional[float]) -> str:
    if value is None:
        return "UNAVAILABLE"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def display_portfolio(portfolio: list[dict]) -> None:
    """Print a formatted portfolio table."""
    if not portfolio:
        print("\n  Portfolio is empty. Add positions first.\n")
        return

    enriched = [calculate_position(p) for p in portfolio]
    totals = calculate_portfolio_totals(portfolio)

    print("\n" + "=" * 80)
    print("  PORTFOLIO MARKET JOURNAL")
    print("=" * 80)
    print(
        f"  {'#':<3} {'Ticker':<8} {'Company':<22} {'Shares':>8} "
        f"{'Buy $':>10} {'Cur $':>10} {'Invested':>12} {'Gain/Loss':>12} {'%':>8}"
    )
    print("-" * 80)

    for i, pos in enumerate(enriched, 1):
        cur = f"${pos['current_price']:.2f}" if pos["current_price"] is not None else "N/A"
        gl = _fmt_currency(pos["gain_loss"])
        pct = _fmt_pct(pos["pct_change"])
        company_short = pos["company"][:20]
        print(
            f"  {i:<3} {pos['ticker']:<8} {company_short:<22} {pos['shares']:>8.2f} "
            f"${pos['purchase_price']:>9.2f} {cur:>10} "
            f"${pos['invested_value']:>11,.2f} {gl:>12} {pct:>8}"
        )

    print("-" * 80)
    # Totals
    partial_note = " (PARTIAL)" if totals["is_partial"] else ""
    print(
        f"  {'TOTAL':<34} "
        f"{'':>10} {'':>10} "
        f"${totals['total_invested']:>11,.2f} "
        f"{_fmt_currency(totals['total_gain_loss']):>12} "
        f"{_fmt_pct(totals['total_pct_change']):>8}"
    )
    if totals["is_partial"]:
        print(
            f"\n  ⚠  Current value total is PARTIAL — "
            f"{totals['unpriced_count']} position(s) have no current price."
        )
        print(f"     Priced positions: {totals['priced_count']}  |  "
              f"Unpriced: {totals['unpriced_count']}")
    print("=" * 80 + "\n")


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------


def export_csv(portfolio: list[dict], output_dir: Path = REPORTS_DIR) -> Path:
    """Export the portfolio to a timestamped CSV file.

    Args:
        portfolio: List of position dicts.
        output_dir: Directory to write the report.

    Returns:
        Path to the written CSV file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_dir / f"portfolio_report_{timestamp}.csv"

    fieldnames = [
        "ticker", "company", "shares", "purchase_price", "current_price",
        "price_source", "invested_value", "current_value", "gain_loss",
        "pct_change", "added_at", "report_generated_at",
    ]

    enriched = [calculate_position(p) for p in portfolio]
    report_time = datetime.now().isoformat(timespec="seconds")

    with filename.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for pos in enriched:
            row = {**pos, "report_generated_at": report_time}
            # Replace None with empty string for CSV clarity
            for k, v in row.items():
                if v is None:
                    row[k] = ""
            writer.writerow(row)

    return filename


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------


def run_tracker() -> None:
    """Run the interactive portfolio tracker."""
    print(DISCLAIMER)
    constituents = load_constituents()
    if constituents:
        print(f"  ✓ Loaded {len(constituents):,} tickers from S&P 500 dataset.\n")
    else:
        print("  ⚠ S&P 500 constituents dataset not found — "
              "ticker validation disabled.\n")

    portfolio: list[dict] = []

    menu = """
  ┌─────────────────────────────┐
  │  Portfolio Market Journal   │
  ├─────────────────────────────┤
  │  1. Add position            │
  │  2. View portfolio          │
  │  3. Export CSV report       │
  │  4. Quit                    │
  └─────────────────────────────┘
  Choice: """

    while True:
        try:
            choice = input(menu).strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "1":
            add_position(portfolio, constituents)
        elif choice == "2":
            display_portfolio(portfolio)
        elif choice == "3":
            if not portfolio:
                print("\n  Portfolio is empty — nothing to export.\n")
            else:
                path = export_csv(portfolio)
                print(f"\n  ✓ Report saved to: {path}\n")
        elif choice == "4":
            break
        else:
            print("  Please enter 1, 2, 3, or 4.\n")

    print("\n  Session ended. No data was sent externally.\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_tracker()
