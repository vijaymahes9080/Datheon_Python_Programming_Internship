"""
desktop_sorter/sorter.py
------------------------
Desktop File Sorter — safe, extension-based file organizer.

Entry point:
    python desktop_sorter/sorter.py --target /path/to/folder --dry-run
    python desktop_sorter/sorter.py --target /path/to/folder --confirm

Usage:
    --target DIR    Directory to organise (required)
    --dry-run       Preview planned moves without touching files
    --confirm       Actually move files after confirmation prompt

Safety rules:
  - Dry run never moves files (verified by tests)
  - Actual execution requires --confirm flag AND interactive confirmation
  - Filesystem roots and the script's own directory are rejected
  - Symbolic links and subdirectories are skipped
  - Filename collisions are renamed, never silently overwritten
  - Files are never deleted
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Category map — extension → category name
# ---------------------------------------------------------------------------

CATEGORY_MAP: dict[str, str] = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".odt": "Documents", ".rtf": "Documents",
    ".md": "Documents", ".epub": "Documents",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images",
    ".webp": "Images", ".tiff": "Images", ".ico": "Images",
    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos",
    ".mov": "Videos", ".wmv": "Videos", ".flv": "Videos",
    ".webm": "Videos", ".m4v": "Videos",
    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio",
    ".aac": "Audio", ".ogg": "Audio", ".wma": "Audio",
    ".m4a": "Audio",
    # Archives
    ".zip": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".rar": "Archives", ".7z": "Archives", ".bz2": "Archives",
    ".xz": "Archives",
    # Code
    ".py": "Code", ".js": "Code", ".ts": "Code", ".html": "Code",
    ".htm": "Code", ".css": "Code", ".java": "Code", ".cpp": "Code",
    ".c": "Code", ".h": "Code", ".json": "Code", ".xml": "Code",
    ".yml": "Code", ".yaml": "Code", ".sh": "Code", ".bat": "Code",
    ".rb": "Code", ".go": "Code", ".rs": "Code",
    # Spreadsheets
    ".xls": "Spreadsheets", ".xlsx": "Spreadsheets",
    ".ods": "Spreadsheets", ".csv": "Spreadsheets",
    # Presentations
    ".ppt": "Presentations", ".pptx": "Presentations",
    ".odp": "Presentations", ".key": "Presentations",
}

KNOWN_CATEGORIES: frozenset[str] = frozenset(CATEGORY_MAP.values()) | {"Other"}

SCRIPT_DIR = Path(__file__).parent.resolve()
LOG_DIR = SCRIPT_DIR / "logs"


# ---------------------------------------------------------------------------
# File classification
# ---------------------------------------------------------------------------


def classify_file(path: Path) -> str:
    """Return the category name for a given file path based on its extension."""
    ext = path.suffix.lower()
    return CATEGORY_MAP.get(ext, "Other")


# ---------------------------------------------------------------------------
# Safety checks
# ---------------------------------------------------------------------------


def is_safe_target(target: Path, script_dir: Path = SCRIPT_DIR) -> tuple[bool, str]:
    """Verify the target directory is safe to organise.

    Rejects:
      - Non-existent paths
      - Non-directory paths
      - Filesystem roots (no parent, or parent == self)
      - Directories that contain the sorter's own source code

    Returns:
        (is_safe, reason_if_unsafe)
    """
    if not target.exists():
        return False, f"Target does not exist: {target}"

    if not target.is_dir():
        return False, f"Target is not a directory: {target}"

    # Reject filesystem roots
    if target == target.parent:
        return False, f"Refusing to organise a filesystem root: {target}"

    # Reject directories containing this script
    try:
        script_dir.relative_to(target)
        return False, (
            f"Refusing to organise {target} — it contains the sorter's own source code."
        )
    except ValueError:
        pass  # script_dir is NOT inside target — safe

    return True, ""


# ---------------------------------------------------------------------------
# Collision resolution
# ---------------------------------------------------------------------------


def resolve_collision(destination: Path) -> Path:
    """Return a non-colliding path by appending _1, _2, etc.

    Never overwrites an existing file silently.
    """
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


# ---------------------------------------------------------------------------
# Directory scanning
# ---------------------------------------------------------------------------


def scan_directory(target: Path) -> list[dict]:
    """Scan target for files to organise.

    Skips:
      - Subdirectories
      - Symbolic links
      - Known category folders at top level
      - The sorter's own log directory

    Returns a list of plan dicts:
        {file: Path, category: str, destination: Path, needs_rename: bool}
    """
    plan: list[dict] = []

    for item in sorted(target.iterdir()):
        # Skip directories (including category dirs we may have created)
        if item.is_dir():
            continue
        # Skip symbolic links
        if item.is_symlink():
            continue
        # Skip non-regular files
        if not item.is_file():
            continue

        category = classify_file(item)
        category_dir = target / category
        dest = category_dir / item.name
        needs_rename = dest.exists() and dest != item

        plan.append({
            "file": item,
            "category": category,
            "destination": dest,
            "needs_rename": needs_rename,
        })

    return plan


# ---------------------------------------------------------------------------
# Dry run
# ---------------------------------------------------------------------------


def dry_run(target: Path) -> list[dict]:
    """Print a preview of planned moves. Does NOT move any files.

    Returns the plan list (for testing).
    """
    plan = scan_directory(target)

    print(f"\n  DRY RUN — Target: {target}")
    print(f"  {len(plan)} file(s) would be organised\n")

    if not plan:
        print("  Nothing to organise.\n")
        return plan

    categories: dict[str, list] = {}
    for item in plan:
        categories.setdefault(item["category"], []).append(item)

    for cat, items in sorted(categories.items()):
        print(f"  [{cat}]  ({len(items)} file(s))")
        for entry in items:
            dest = entry["destination"]
            if entry["needs_rename"]:
                dest = resolve_collision(dest)
                flag = f" → renamed → {dest.name}"
            else:
                flag = ""
            print(f"    {entry['file'].name}{flag}")
        print()

    print("  No files have been moved. Use --confirm to execute.\n")
    return plan


# ---------------------------------------------------------------------------
# Confirmed execution
# ---------------------------------------------------------------------------


class SortSummary:
    """Accumulates results from a sort operation."""

    def __init__(self) -> None:
        self.moved: list[tuple[Path, Path]] = []
        self.skipped: list[tuple[Path, str]] = []
        self.errors: list[tuple[Path, str]] = []

    @property
    def total(self) -> int:
        return len(self.moved) + len(self.skipped) + len(self.errors)


def execute_sort(target: Path, interactive: bool = True) -> SortSummary:
    """Move files into category subdirectories.

    Args:
        target: The directory to organise.
        interactive: If True, prompt for confirmation before starting.

    Returns:
        A SortSummary with moved, skipped, and error records.
    """
    plan = scan_directory(target)
    summary = SortSummary()

    if not plan:
        print("  Nothing to organise.")
        return summary

    if interactive:
        print(f"\n  Ready to move {len(plan)} file(s) in: {target}")
        try:
            confirm = input("  Type 'yes' to proceed: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.")
            return summary

        if confirm != "yes":
            print("  Cancelled — no files moved.")
            return summary

    for entry in plan:
        src = entry["file"]
        category_dir = target / entry["category"]
        dest = category_dir / src.name
        dest = resolve_collision(dest)

        try:
            category_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
            summary.moved.append((src, dest))
            logging.info("MOVED: %s → %s", src.name, dest)
        except PermissionError as exc:
            summary.errors.append((src, f"Permission denied: {exc}"))
            logging.error("ERROR (permission): %s — %s", src.name, exc)
        except OSError as exc:
            summary.errors.append((src, str(exc)))
            logging.error("ERROR: %s — %s", src.name, exc)

    return summary


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def setup_logging(log_dir: Path = LOG_DIR) -> Path:
    """Configure file and console logging. Returns the log file path."""
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"sort_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return log_file


def print_summary(summary: SortSummary, log_file: Optional[Path] = None) -> None:
    """Print a human-readable sort summary."""
    print("\n" + "=" * 50)
    print("  SORT SUMMARY")
    print("=" * 50)
    print(f"  Moved:   {len(summary.moved)}")
    print(f"  Skipped: {len(summary.skipped)}")
    print(f"  Errors:  {len(summary.errors)}")
    if log_file:
        print(f"  Log:     {log_file}")
    print("=" * 50 + "\n")

    if summary.errors:
        print("  Errors encountered:")
        for path, reason in summary.errors:
            print(f"    {path.name}: {reason}")
        print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Desktop File Sorter — organises files by extension category.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sorter.py --target ~/Downloads --dry-run
  python sorter.py --target ~/Downloads --confirm
        """,
    )
    parser.add_argument(
        "--target", "-t",
        required=False,
        help="Directory to organise. Prompted interactively if omitted.",
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Preview planned moves without touching any files.",
    )
    parser.add_argument(
        "--confirm", "-c",
        action="store_true",
        help="Execute the sort after confirmation.",
    )
    return parser


def run_sorter() -> None:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # Resolve target
    if args.target:
        target = Path(args.target).resolve()
    else:
        try:
            raw = input("  Enter target directory path: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.")
            sys.exit(0)
        target = Path(raw).resolve()

    print(f"\n  Resolved target: {target}")

    safe, reason = is_safe_target(target)
    if not safe:
        print(f"\n  ✗ Unsafe target rejected: {reason}\n")
        sys.exit(1)

    if args.dry_run:
        dry_run(target)
        sys.exit(0)

    if args.confirm:
        log_file = setup_logging()
        logging.info("Sort started — target: %s", target)
        summary = execute_sort(target, interactive=True)
        print_summary(summary, log_file)
        logging.info("Sort complete — moved: %d, errors: %d",
                     len(summary.moved), len(summary.errors))
        sys.exit(0)

    print("\n  Specify --dry-run (preview) or --confirm (execute).")
    print("  Use --help for usage information.\n")
    sys.exit(1)


if __name__ == "__main__":
    run_sorter()
