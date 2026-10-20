# Task 03: Desktop File Sorter & Cleanup Utility

A safe, multi-category filesystem reorganization utility implemented in Python standard library (`shutil`, `pathlib`, `argparse`).

---

## Overview

Desktop File Sorter automatically classifies unorganized files in target folders (such as Downloads or Desktop) into categorized subfolders based on file extensions. It provides rigorous safety guarantees, including root-directory protection, dry-run previews, non-destructive collision renaming, and persistent audit logs.

---

## Extension Classification Map

The utility categorizes files into 9 distinct buckets:

| Category | File Extensions |
|---|---|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.md` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.tiff` |
| **Videos** | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a` |
| **Archives** | `.zip`, `.tar`, `.gz`, `.rar`, `.7z`, `.bz2`, `.xz` |
| **Code** | `.py`, `.js`, `.ts`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.h`, `.json`, `.xml`, `.yml`, `.yaml`, `.sql`, `.sh` |
| **Spreadsheets**| `.xls`, `.xlsx`, `.ods`, `.csv` |
| **Presentations**| `.ppt`, `.pptx`, `.odp` |
| **Other** | All unmapped or extensionless files |

---

## Safety Architecture

1. **Root Drive & Critical Path Protection**:
   Target directories matching filesystem roots (`C:\`, `/`) or the sorter's own repository directory are rejected immediately with a `ValueError`.
2. **Dry-Run Inspection Guarantee**:
   Running with `--dry-run` performs a full directory scan, constructs the organization plan, and displays intended actions without moving a single file.
3. **Collision-Safe Renaming**:
   If a destination file already exists with identical name, the engine appends an incremental numeric suffix (e.g. `report.pdf` &rarr; `report_1.pdf`). Files are **never** silently overwritten.
4. **Audit Trail Logging**:
   Every confirmed sort run generates an audit log in `logs/sorter_<timestamp>.log` documenting each source path, category, and final destination.

---

## Directory Structure

```
desktop_sorter/
├── sorter.py               # Main CLI sorting engine
├── index.html              # Interactive web showcase and sorting simulator
├── README.md               # Safety manual and documentation
├── logs/                   # Directory for persistent execution logs
│   └── .gitkeep
└── tests/
    └── test_sorter.py      # Automated unit test suite (unittest)
```

---

## Execution Guide

### CLI Commands

```bash
# Navigate to the sorter directory
cd d:/intership/python/vj/desktop_sorter

# 1. Inspect without making any changes (DRY RUN)
python sorter.py --target "C:\Users\User\Downloads" --dry-run

# 2. Execute confirmed organization
python sorter.py --target "C:\Users\User\Downloads" --confirm

# 3. Interactive prompt (will ask for confirmation before moving)
python sorter.py --target "C:\Users\User\Downloads"
```

### Running the Automated Test Suite

```bash
python -m unittest tests/test_sorter.py -v
```

---

## Automated Test Coverage

The test suite in `tests/test_sorter.py` verifies:

1. `TestClassification`: Validates correct extension-to-category resolution across all 9 categories.
2. `TestCollisionPolicy`: Verifies numeric suffix resolution on duplicate files without overwrites.
3. `TestUnsafeTargets`: Tests rejection of filesystem roots and non-existent directories.
4. `TestDryRun`: Confirms zero file movements during preview operations.
5. `TestLogOutput`: Validates that log files are created and contain expected transaction records.
