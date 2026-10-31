"""Optional exact-source helper integration; never opens a database or server."""
import json
import os
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = os.environ.get("BOOKORBIT_SOURCE_REPO")
BASE = json.loads((ROOT / "compatibility.json").read_text())["stableServer"]["serverBase"]
HELPER = ROOT / "server-support/bookorbit-3.6.0/prepare-source.py"


@unittest.skipUnless(SOURCE, "Set BOOKORBIT_SOURCE_REPO to a local exact-base source repository")
class PrepareSourceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bookorbit-extras-source-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / "checkout"
        self.run_command("git", "clone", "--shared", "--no-checkout", SOURCE, str(self.target))
        self.run_command("git", "-C", str(self.target), "switch", "--detach", BASE)

    def run_command(self, *args, expected=0):
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stderr)
        return result.stdout

    def helper(self, *args, expected=0):
        return self.run_command("python3", str(HELPER), str(self.target), *args, expected=expected)

    def test_both_and_complete_source_archive(self):
        archive = self.root / "source.tar.gz"
        self.helper("--features", "both", "--source-archive", str(archive))
        self.assertTrue((self.target / "server/src/db/migrations/0132_undo_reading_opening.sql").exists())
        self.assertIn("tag-matches", (self.target / "server/src/modules/koreader/koreader-catalog.controller.ts").read_text())
        with tarfile.open(archive) as source:
            names = set(source.getnames())
            self.assertIn("bookorbit-extras-source/LICENSE", names)
            self.assertIn("bookorbit-extras-source/client/src/App.vue", names)
            self.assertIn("bookorbit-extras-source/server/src/modules/koreader/koreader-opening.controller.ts", names)
            self.assertFalse(any("node_modules" in name or name.endswith("/.env") for name in names))
        self.helper(expected=2)

    def test_dirty_checkout_is_unchanged(self):
        marker = self.target / "private-fixture.txt"
        marker.write_text("Do not overwrite")
        self.helper(expected=2)
        self.assertEqual(marker.read_text(), "Do not overwrite")
        self.assertFalse((self.target / "server/src/db/schema/reading-openings.ts").exists())

    def test_existing_archive_is_not_overwritten(self):
        archive = self.root / "existing.tar.gz"
        archive.write_bytes(b"keep")
        self.helper("--source-archive", str(archive), expected=2)
        self.assertEqual(archive.read_bytes(), b"keep")
        self.assertFalse(self.run_command("git", "-C", str(self.target), "status", "--porcelain").strip())

    def test_subdirectory_is_not_a_checkout(self):
        self.run_command("python3", str(HELPER), str(self.target / "server"), expected=2)
        self.assertFalse(self.run_command("git", "-C", str(self.target), "status", "--porcelain").strip())


if __name__ == "__main__":
    unittest.main()
