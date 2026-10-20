# Design System & UI/UX Architecture Specification

**Python Practical Lab** — Editorial Engineering Aesthetic

---

## 1. Aesthetic Rationale

The design system of **Python Practical Lab** is constructed around an **editorial technical aesthetic** that balances modern software clarity with high visual polish. Rather than defaulting to generic dark themes or sterile bootstrap templates, the platform employs a warm, publication-grade light palette paired with refined typography.

Every Python terminal application in this suite has a dual identity:
1. **A Pure Python Terminal Engine**: Implemented exclusively using the Python standard library, featuring defensive input parsing, ASCII art, and clear terminal output.
2. **An In-Browser Interactive Showcase**: Rendered in semantic HTML5 and vanilla JavaScript, enabling immediate browser-based evaluation of the underlying algorithms without requiring a local Python runtime.

---

## 2. Color Palette & Design Tokens

| Token Name | Hex Value | Purpose |
|---|---|---|
| `--clr-bg` | `#FAF9F6` | Primary background (warm off-white, paper-like readability) |
| `--clr-surface` | `#F5F4F0` | Card background & secondary content blocks |
| `--clr-surface-alt` | `#EEECE6` | Code headers, table header rows, and button inactive states |
| `--clr-border` | `#D8D5CC` | Primary structural borders |
| `--clr-border-light` | `#E8E6DF` | Subtle dividers and chip borders |
| `--clr-ink` | `#1E1B4B` | Primary text (deep midnight indigo, high contrast) |
| `--clr-ink-mid` | `#3D3A6B` | Secondary body text and labels |
| `--clr-ink-muted` | `#6B6890` | Captions, breadcrumbs, and metadata |
| `--clr-accent` | `#E05C43` | Primary action highlights, links, and focus rings (coral terracotta) |
| `--clr-accent-bg` | `#FDF1EE` | Coral tint for badges, alert backgrounds, and hover fills |
| `--clr-success` | `#2D8A5C` | Status tags, positive financial returns, passing tests |
| `--clr-warning` | `#B45309` | Partial valuation notices, warnings |
| `--clr-info` | `#1D4ED8` | Informational callouts and documentation links |

---

## 3. Typography Hierarchy

The system incorporates two Google Fonts alongside robust system fallbacks:
- **Body & Headings**: `Inter`, `-apple-system`, `BlinkMacSystemFont`, `sans-serif`
  - Crisp readability at small sizes, balanced optical kerning, and clean geometric letterforms.
- **Code & Financial Data**: `JetBrains Mono`, `Fira Code`, `monospace`
  - Fixed-width alignment for terminal ASCII art, gallows rendering, tabular stock records, and command snippets.

### Typographic Scale
- `Title (H1)`: `2.5rem` / `3.0rem` — Bold (700), tight letter spacing (`-0.025em`)
- `Section Header (H2)`: `1.875rem` — Semi-bold (600)
- `Card Header (H3)`: `1.25rem` — Semi-bold (600)
- `Body Text`: `1.0rem` (`16px`) — Regular (400), line-height `1.6`
- `Code / Badges`: `0.875rem` (`14px`) — Medium (500)

---

## 4. Layout Architecture & Responsiveness

### Universal Portal (`index.html`)
- **Hero Section**: Contextual orientation, key engineering pillars, and navigation anchors.
- **Projects Grid**: 2×2 CSS Grid layout on desktop screens (`≥ 900px`), collapsing gracefully to single-column card feeds on mobile devices (`≤ 600px`).
- **Tech Overview & Data Matrix**: Responsive data tables wrapped with horizontal scroll containers to preserve viewport integrity on small screens.

### Subproject Interactive Showcases
Each application directory contains a dedicated `index.html`:
- **Word Challenge (`word_challenge/index.html`)**: Features an in-browser ASCII gallows renderer synchronized with a virtual alphabet keyboard.
- **Market Journal (`market_journal/index.html`)**: Features an interactive portfolio calculator, live return indicators, and S&P 500 symbol resolution.
- **Desktop Sorter (`desktop_sorter/index.html`)**: Features visual classification buckets, mode switching (Dry-Run vs Confirmed), and a virtual audit log console.
- **FAQ Assistant (`faq_assistant/index.html`)**: Features a conversational chat interface with real-time intent labeling and clickable query suggestions.

---

## 5. Accessibility & Performance Standards

- **Semantic HTML5**: Native `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, and `<footer>` landmarks throughout.
- **WCAG 2.1 AAA Contrast**: Indigo ink (`#1E1B4B`) against off-white (`#FAF9F6`) achieves a contrast ratio of `14.8:1` (exceeding the 7:1 AAA threshold).
- **Reduced Motion Support**: Fully respects `@media (prefers-reduced-motion: reduce)`, disabling non-essential transitions.
- **Zero Third-Party JavaScript Bundlers**: All interactive widgets run on native standard vanilla JavaScript with 0 ms compilation overhead.
