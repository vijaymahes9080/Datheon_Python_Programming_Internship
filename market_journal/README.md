# Task 02: Portfolio Market Journal

A robust terminal stock portfolio performance tracker with gain/loss analytics, transparent price sourcing, and S&P 500 constituent ticker verification.

---

## Overview

Portfolio Market Journal enables investors and students to track equity holdings, measure total invested capital against current valuations, and export structured audit reports. It adheres to strict financial transparency: unpriced securities are flagged as `UNAVAILABLE` rather than estimated or zeroed out, preventing misleading metrics.

---

## Key Features

- **S&P 500 Constituent Validation**: Parses `resources/constituents.csv` to validate ticker symbols against the official S&P 500 index registry.
- **Transparent Price Tagging**:
  - Positions with user-supplied quotes are tagged `PRICE_SOURCE: MANUAL`.
  - Unpriced positions are recorded as `UNAVAILABLE` and highlighted with a **PARTIAL VALUATION** warning.
- **Financial Calculation Engine**:
  - `Invested Capital = Purchase Price × Shares`
  - `Market Value = Current Price × Shares`
  - `Unrealized Gain / Loss = Market Value - Invested Capital`
  - `Total Return % = (Unrealized Gain / Loss ÷ Invested Capital) × 100`
- **CSV Audit Export**: Generates timestamped reports containing complete position metrics, timestamps, and valuation status.
- **Standard Library Only**: Built using Python's `csv`, `pathlib`, `datetime`, and `unittest` modules.

---

## Directory Structure

```
market_journal/
├── tracker.py              # Main interactive CLI tracker
├── index.html              # Interactive web showcase with in-browser calculator
├── README.md               # Application documentation
├── resources/
│   └── constituents.csv    # Official S&P 500 constituent companies dataset
└── tests/
    └── test_tracker.py     # Automated unit test suite (unittest)
```

---

## Execution Guide

### Running the Terminal Tracker

```bash
# Navigate to the task directory
cd d:/intership/python/vj/market_journal

# Launch the interactive journal
python tracker.py
```

### Interactive Menu Options

1. **Add Position**: Enter ticker symbol, shares, purchase price, and optional current price.
2. **View Portfolio**: Displays formatted tabular summary of all holdings, total cost, current value, and profit/loss.
3. **Export CSV**: Writes an audit report to `portfolio_report_<YYYYMMDD_HHMMSS>.csv`.
4. **Exit**: Gracefully ends the session.

### Running the Automated Test Suite

```bash
python -m unittest tests/test_tracker.py -v
```

---

## CSV Export Format

| Column | Description |
|---|---|
| `Ticker` | Stock ticker symbol (e.g. `AAPL`, `MSFT`) |
| `Shares` | Number of shares held (float) |
| `Purchase Price` | Cost basis per share ($) |
| `Current Price` | Market price per share ($ or `UNAVAILABLE`) |
| `Invested Capital` | Total cost basis ($) |
| `Current Value` | Current valuation ($ or `UNAVAILABLE`) |
| `Gain / Loss ($)` | Dollar return ($ or `N/A`) |
| `Return (%)` | Percentage return (% or `N/A`) |
| `Price Status` | `PRICED` or `UNAVAILABLE` |

---

## Automated Test Coverage

The test suite in `tests/test_tracker.py` verifies:

1. `TestCalculations`: Gain/loss calculations, positive returns, negative returns, break-even.
2. `TestUnpricedHolding`: Ensures unpriced assets do not corrupt calculations or evaluate to $0.
3. `TestPortfolioTotals`: Validates `is_partial` flag when mixed priced/unpriced holdings exist.
4. `TestCSVExport`: Tests file creation, column integrity, and numeric formatting.
5. `TestTickerValidation`: Validates ticker lookup against `constituents.csv`.
