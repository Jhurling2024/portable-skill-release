import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_manifest", ROOT / "scripts/package_manifest.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "fixture-skill"
        self.root.mkdir()
        (self.root / "SKILL.md").write_bytes(b"fixture\n")
        (self.root / "LICENSE").write_bytes(b"fixture license\n")

    def test_round_trip_and_deterministic_manifest(self):
        package.create(self.root)
        before = (self.root / "SHA256SUMS").read_bytes()
        package.create(self.root)
        self.assertEqual(before, (self.root / "SHA256SUMS").read_bytes())
        self.assertTrue(package.check(self.root)["ok"])

    def test_changed_bytes_detected(self):
        package.create(self.root)
        (self.root / "SKILL.md").write_bytes(b"fixture\r\n")
        self.assertEqual(["SKILL.md"], package.check(self.root)["changed"])

    def test_deleted_file_detected(self):
        (self.root / "extra.txt").write_text("fixture")
        package.create(self.root)
        (self.root / "extra.txt").unlink()
        self.assertEqual(["extra.txt"], package.check(self.root)["missing"])

    def test_unlisted_file_detected(self):
        package.create(self.root)
        (self.root / "extra.txt").write_text("fixture")
        self.assertEqual(["extra.txt"], package.check(self.root)["extra"])

    def test_duplicate_and_traversal_entries_rejected(self):
        package.create(self.root)
        path = self.root / "SHA256SUMS"
        original = path.read_text()
        path.write_text(original + original)
        with self.assertRaises(ValueError): package.check(self.root)
        path.write_text("0" * 64 + "  ../secret\n")
        with self.assertRaises(ValueError): package.check(self.root)

    def test_credential_files_rejected(self):
        for name in (".env", ".env.local", "id_rsa", "credentials.json"):
            file = self.root / name
            file.write_text("synthetic")
            with self.assertRaises(ValueError): package.create(self.root)
            file.unlink()

    def test_vcs_and_bytecode_are_ignored(self):
        package.create(self.root)
        for directory in (".git", "__pycache__"):
            (self.root / directory).mkdir()
            (self.root / directory / "untracked").write_text("fixture")
        self.assertTrue(package.check(self.root)["ok"])

    def test_both_root_and_nested_layouts(self):
        package.create(self.root)
        outer = Path(self.tmp.name) / "origin"
        nested = outer / "skills" / "fixture-skill"
        shutil.copytree(self.root, nested)
        (outer / ".git").mkdir()
        self.assertTrue(package.check(nested)["ok"])
        (self.root / ".git").mkdir()
        self.assertTrue(package.check(self.root)["ok"])

    def test_missing_required_files(self):
        (self.root / "LICENSE").unlink()
        with self.assertRaises(ValueError): package.create(self.root)

    def test_spaces_and_unicode_paths(self):
        (self.root / "evidence notes.txt").write_bytes(b"fixture")
        (self.root / "caf\u00e9.md").write_bytes(b"fixture")
        package.create(self.root)
        self.assertTrue(package.check(self.root)["ok"])

    def test_check_does_not_mutate(self):
        package.create(self.root)
        before = {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        package.check(self.root)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()})

    def test_manifest_symlink_rejected_when_supported(self):
        outside = Path(self.tmp.name) / "outside.txt"
        outside.write_text("unchanged")
        try: (self.root / "SHA256SUMS").symlink_to(outside)
        except OSError: self.skipTest("symlink creation unavailable")
        with self.assertRaises(ValueError): package.create(self.root)
        self.assertEqual("unchanged", outside.read_text())

    def test_cli_exit_codes(self):
        script = str(ROOT / "scripts/package_manifest.py")
        for args, expected in ((["create", str(self.root)], 0), (["check", str(self.root)], 0)):
            proc = subprocess.run([sys.executable, script, *args], capture_output=True, text=True)
            self.assertEqual(expected, proc.returncode, proc.stdout + proc.stderr)
            self.assertTrue(json.loads(proc.stdout)["ok"])
        (self.root / "SKILL.md").write_text("changed")
        proc = subprocess.run([sys.executable, script, "check", str(self.root)], capture_output=True, text=True)
        self.assertEqual(1, proc.returncode)
        (self.root / "SHA256SUMS").write_text("bad line")
        proc = subprocess.run([sys.executable, script, "check", str(self.root)], capture_output=True, text=True)
        self.assertEqual(2, proc.returncode)


if __name__ == "__main__": unittest.main()
