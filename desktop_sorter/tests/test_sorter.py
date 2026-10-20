"""
desktop_sorter/tests/test_sorter.py
------------------------------------
Unit tests for the Desktop File Sorter.

Run with:
    python -m unittest discover desktop_sorter/tests -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from desktop_sorter.sorter import (
    KNOWN_CATEGORIES,
    SortSummary,
    classify_file,
    dry_run,
    execute_sort,
    is_safe_target,
    resolve_collision,
    scan_directory,
)


# ---------------------------------------------------------------------------
# File classification
# ---------------------------------------------------------------------------

class TestClassifyFile(unittest.TestCase):
    """Tests for classify_file()."""

    def test_pdf_is_document(self):
        self.assertEqual(classify_file(Path("report.pdf")), "Documents")

    def test_jpg_is_image(self):
        self.assertEqual(classify_file(Path("photo.jpg")), "Images")

    def test_png_is_image(self):
        self.assertEqual(classify_file(Path("screenshot.png")), "Images")

    def test_mp4_is_video(self):
        self.assertEqual(classify_file(Path("movie.mp4")), "Videos")

    def test_mp3_is_audio(self):
        self.assertEqual(classify_file(Path("song.mp3")), "Audio")

    def test_zip_is_archive(self):
        self.assertEqual(classify_file(Path("archive.zip")), "Archives")

    def test_py_is_code(self):
        self.assertEqual(classify_file(Path("script.py")), "Code")

    def test_js_is_code(self):
        self.assertEqual(classify_file(Path("app.js")), "Code")

    def test_xlsx_is_spreadsheet(self):
        self.assertEqual(classify_file(Path("data.xlsx")), "Spreadsheets")

    def test_pptx_is_presentation(self):
        self.assertEqual(classify_file(Path("slides.pptx")), "Presentations")

    def test_unknown_extension_is_other(self):
        self.assertEqual(classify_file(Path("file.xyz123")), "Other")

    def test_no_extension_is_other(self):
        self.assertEqual(classify_file(Path("noextension")), "Other")

    def test_case_insensitive_extension(self):
        self.assertEqual(classify_file(Path("IMAGE.JPG")), "Images")
        self.assertEqual(classify_file(Path("DOC.PDF")), "Documents")

    def test_all_categories_are_known(self):
        # Every category returned must be in KNOWN_CATEGORIES
        test_files = [
            "a.pdf", "b.jpg", "c.mp4", "d.mp3", "e.zip",
            "f.py", "g.xlsx", "h.pptx", "i.xyz",
        ]
        for name in test_files:
            cat = classify_file(Path(name))
            self.assertIn(cat, KNOWN_CATEGORIES, f"{name} → {cat} not in KNOWN_CATEGORIES")


# ---------------------------------------------------------------------------
# Safety checks
# ---------------------------------------------------------------------------

class TestIsSafeTarget(unittest.TestCase):
    """Tests for is_safe_target()."""

    def test_nonexistent_path_rejected(self):
        safe, reason = is_safe_target(Path("/nonexistent/directory/xyz"))
        self.assertFalse(safe)
        self.assertIn("not exist", reason)

    def test_valid_temp_dir_accepted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            safe, reason = is_safe_target(Path(tmpdir))
            self.assertTrue(safe, reason)

    def test_filesystem_root_rejected(self):
        # On Windows, 'C:\' is a root; on Unix, '/'
        import os
        root = Path(Path.cwd().anchor)
        safe, reason = is_safe_target(root)
        self.assertFalse(safe)

    def test_script_directory_rejected(self):
        from desktop_sorter.sorter import SCRIPT_DIR
        # If the script_dir exists and is not a root, it should be rejected
        # when it's the target (it contains the script itself)
        if SCRIPT_DIR.exists():
            safe, reason = is_safe_target(SCRIPT_DIR, SCRIPT_DIR)
            self.assertFalse(safe)

    def test_file_not_directory_rejected(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as fh:
            path = Path(fh.name)
        try:
            safe, reason = is_safe_target(path)
            self.assertFalse(safe)
        finally:
            path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Collision resolution
# ---------------------------------------------------------------------------

class TestResolveCollision(unittest.TestCase):
    """Tests for resolve_collision()."""

    def test_no_collision_returns_original(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "file.txt"
            result = resolve_collision(dest)
            self.assertEqual(result, dest)

    def test_collision_returns_renamed_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "file.txt"
            dest.write_text("original")
            result = resolve_collision(dest)
            self.assertNotEqual(result, dest)
            self.assertEqual(result, Path(tmpdir) / "file_1.txt")

    def test_multiple_collisions_increment(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "file.txt"
            dest.write_text("v1")
            (Path(tmpdir) / "file_1.txt").write_text("v2")
            result = resolve_collision(dest)
            self.assertEqual(result, Path(tmpdir) / "file_2.txt")

    def test_resolved_path_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "new_file.pdf"
            dest.write_text("existing")
            result = resolve_collision(dest)
            self.assertFalse(result.exists())


# ---------------------------------------------------------------------------
# Dry run
# ---------------------------------------------------------------------------

class TestDryRun(unittest.TestCase):
    """Tests that dry_run() never moves files."""

    def _create_test_dir(self, tmpdir: str, files: list[str]) -> Path:
        target = Path(tmpdir)
        for name in files:
            (target / name).write_text(f"content of {name}")
        return target

    def test_dry_run_moves_nothing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = self._create_test_dir(
                tmpdir, ["report.pdf", "image.jpg", "data.xlsx"]
            )
            original_files = {f.name for f in target.iterdir()}
            dry_run(target)
            after_files = {f.name for f in target.iterdir()}
            self.assertEqual(original_files, after_files)

    def test_dry_run_returns_plan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = self._create_test_dir(tmpdir, ["doc.pdf", "pic.png"])
            plan = dry_run(target)
            self.assertEqual(len(plan), 2)

    def test_dry_run_empty_dir_returns_empty_plan(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            plan = dry_run(Path(tmpdir))
            self.assertEqual(plan, [])


# ---------------------------------------------------------------------------
# Confirmed execution
# ---------------------------------------------------------------------------

class TestExecuteSort(unittest.TestCase):
    """Tests for execute_sort() using temporary directories."""

    def _setup_dir(self, files: list[str]) -> Path:
        tmpdir = tempfile.mkdtemp()
        target = Path(tmpdir)
        for name in files:
            (target / name).write_text(f"content of {name}")
        return target

    def test_files_moved_to_correct_category(self):
        target = self._setup_dir(["report.pdf", "photo.jpg", "song.mp3"])
        try:
            summary = execute_sort(target, interactive=False)
            self.assertEqual(len(summary.moved), 3)
            self.assertTrue((target / "Documents" / "report.pdf").exists())
            self.assertTrue((target / "Images" / "photo.jpg").exists())
            self.assertTrue((target / "Audio" / "song.mp3").exists())
            # Original locations should be gone
            self.assertFalse((target / "report.pdf").exists())
        finally:
            import shutil
            shutil.rmtree(str(target), ignore_errors=True)

    def test_collision_no_silent_overwrite(self):
        target = self._setup_dir(["note.txt"])
        # Pre-create the destination so collision resolution is needed
        doc_dir = target / "Documents"
        doc_dir.mkdir()
        (doc_dir / "note.txt").write_text("existing content")
        try:
            summary = execute_sort(target, interactive=False)
            # Original should be gone from root
            self.assertFalse((target / "note.txt").exists())
            # Existing file should still have original content
            self.assertEqual((doc_dir / "note.txt").read_text(), "existing content")
            # New file should exist under a different name
            renamed = doc_dir / "note_1.txt"
            self.assertTrue(renamed.exists())
        finally:
            import shutil
            shutil.rmtree(str(target), ignore_errors=True)

    def test_directories_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            (target / "subdir").mkdir()
            (target / "file.txt").write_text("content")
            summary = execute_sort(target, interactive=False)
            # Only file.txt should be moved — subdir ignored
            self.assertEqual(len(summary.moved), 1)

    def test_empty_directory_moves_nothing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            summary = execute_sort(Path(tmpdir), interactive=False)
            self.assertEqual(len(summary.moved), 0)
            self.assertEqual(len(summary.errors), 0)

    def test_category_folders_not_reprocessed(self):
        """Files inside created category folders must not be moved again."""
        target = self._setup_dir(["image.jpg"])
        try:
            # First sort
            execute_sort(target, interactive=False)
            # Second sort — category folders now exist, their contents must stay
            summary2 = execute_sort(target, interactive=False)
            # Nothing left at the root level to move
            self.assertEqual(len(summary2.moved), 0)
        finally:
            import shutil
            shutil.rmtree(str(target), ignore_errors=True)


# ---------------------------------------------------------------------------
# Scan directory
# ---------------------------------------------------------------------------

class TestScanDirectory(unittest.TestCase):
    """Tests for scan_directory()."""

    def test_skips_symlinks(self):
        import os
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            real_file = target / "real.txt"
            real_file.write_text("hello")
            link = target / "link.txt"
            try:
                link.symlink_to(real_file)
                plan = scan_directory(target)
                names = [e["file"].name for e in plan]
                self.assertIn("real.txt", names)
                self.assertNotIn("link.txt", names)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks not supported on this platform")

    def test_skips_subdirectories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            (target / "subdir").mkdir()
            (target / "file.pdf").write_text("data")
            plan = scan_directory(target)
            names = [e["file"].name for e in plan]
            self.assertNotIn("subdir", names)
            self.assertIn("file.pdf", names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
