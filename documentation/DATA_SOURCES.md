# Dataset Sources, Schemas, & Fallback Policies

This document catalogs all datasets utilized across the **Python Practical Lab** project suite, verifying their provenance, schemas, local storage locations, and automated fallback mechanisms.

---

## Dataset Summary Matrix

| Task | Dataset Name | Source / Provider | Local Path | Format | Verification Status |
|---|---|---|---|---|---|
| **Task 01** | Google 10k English Words | [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english) | `word_challenge/resources/words.txt` | TXT | ✅ Verified & Cached (9,894 words) |
| **Task 02** | S&P 500 Constituents | [datasets/s-and-p-500-companies](https://github.com/datasets/s-and-p-500-companies) | `market_journal/resources/constituents.csv` | CSV | ✅ Verified & Cached (504 companies) |
| **Task 03** | Standard File Extensions | Python Standard Library (`shutil`) | Built-in Map | Dict | ✅ Verified Standard Library |
| **Task 04** | Sample FAQ Dataset | [datheon.in/datasets](https://www.datheon.in/datasets/sample_faq.json) | `faq_assistant/resources/sample_faq.json` | JSON | ✅ Verified & Cached (3 FAQs, 6 greetings) |

---

## 1. Task 01 — Google 10,000 English Words

### Origin
- **Source Repository**: `https://github.com/first20hours/google-10000-english`
- **Raw Endpoint**: `https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt`
- **Description**: Frequency-sorted English vocabulary list derived from Google's Trillion Word Corpus, with profanity filtered out.

### Format & Schema
- Plain UTF-8 text file.
- Single entry per line, lowercase ASCII characters.

### Ingestion & Sanitization Rules
1. Words with length $< 4$ or $> 12$ are excluded to ensure balanced puzzle difficulty.
2. Trailing and leading whitespace characters are stripped.
3. Duplicates are removed while preserving order.

### Fallback Policy
If `words.txt` is missing, unreadable, or contains no valid words, `load_words()` logs a warning and loads a 50-word embedded list (`algorithm`, `variable`, `framework`, `terminal`, `developer`, etc.), ensuring zero crashes.

---

## 2. Task 02 — S&P 500 Constituent Companies

### Origin
- **Source Repository**: `https://github.com/datasets/s-and-p-500-companies`
- **Raw Endpoint**: `https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv`
- **Description**: Registry of companies currently included in the standard S&P 500 index.

### Format & Schema
- Standard comma-separated values (CSV) with UTF-8 encoding.
- Columns:
  1. `Symbol`: Stock ticker (e.g. `AAPL`, `MSFT`, `BRK.B`)
  2. `Security`: Company legal name
  3. `GICS Sector`: Industry sector (e.g. `Information Technology`, `Financials`)
  4. `GICS Sub-Industry`: Specific sub-industry classification
  5. `Headquarters Location`: City, State/Country
  6. `Date added`: Inclusion date
  7. `CIK`: Central Index Key (SEC identifier)
  8. `Founded`: Founding year

### Fallback Policy
If `constituents.csv` is absent, the tracker displays an informative advisory note indicating that offline ticker entry mode is active. Manual ticker inputs continue to function normally.

---

## 3. Task 03 — Filesystem Extension Categories

### Origin
- Defined based on standard MIME file signatures and common desktop filesystem conventions.

### Category Classification
- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.md`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.tiff`
- **Videos**: `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a`
- **Archives**: `.zip`, `.tar`, `.gz`, `.rar`, `.7z`, `.bz2`, `.xz`
- **Code**: `.py`, `.js`, `.ts`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.h`, `.json`, `.xml`, `.yml`, `.yaml`, `.sql`, `.sh`
- **Spreadsheets**: `.xls`, `.xlsx`, `.ods`, `.csv`
- **Presentations**: `.ppt`, `.pptx`, `.odp`
- **Other**: Files lacking an extension or matching none of the above.

---

## 4. Task 04 — Sample FAQ Dataset

### Origin
- **Source Endpoint**: `https://www.datheon.in/datasets/sample_faq.json`
- **Description**: Ground-truth FAQ dataset covering foundational internship inquiries.

### Format & Schema
```json
{
  "greetings": [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good evening",
    "greetings"
  ],
  "faqs": [
    {
      "question": "What is an internship?",
      "answer": "An internship is a professional learning experience that offers meaningful, practical work related to a student's field of study or career interest."
    },
    {
      "question": "How can I apply for an internship?",
      "answer": "You can apply by preparing a tailored resume, crafting a compelling cover letter, and submitting applications through university career portals, LinkedIn, or directly on company careers pages."
    },
    {
      "question": "Are internships paid or unpaid?",
      "answer": "Internships can be either paid or unpaid depending on the organization, industry regulations, and jurisdiction. Most technical and software engineering internships are paid."
    }
  ]
}
```

### Fallback Policy
If `sample_faq.json` is missing or contains invalid JSON syntax, `load_faq()` initializes a hardcoded dictionary mirror of the schema, allowing the conversational assistant to remain operational without hallucination.
