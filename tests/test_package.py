"""Independent packaging checks; not a model-behavior benchmark."""
import hashlib
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_manifest_exact_coverage_and_bytes(self):
        listed = {}
        for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, rel = line.split("  ", 1)
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
            self.assertNotIn(rel, listed)
            self.assertNotIn("..", Path(rel).parts)
            self.assertFalse(Path(rel).is_absolute())
            listed[rel] = digest
        files = {p.relative_to(ROOT).as_posix(): p for p in ROOT.rglob("*") if p.is_file()
                 and not {".git", "__pycache__"} & set(p.relative_to(ROOT).parts)
                 and p.suffix != ".pyc" and p.name != "SHA256SUMS"}
        self.assertEqual(set(listed), set(files))
        for rel, path in files.items():
            self.assertEqual(listed[rel], hashlib.sha256(path.read_bytes()).hexdigest(), rel)

    def test_metadata_and_credit(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("name: " + ROOT.name + "\n", text)
        self.assertIn('version: "0.1.0"', text)
        self.assertIn("license: MIT", text)
        for name in ("SKILL.md", "AUTHORS.md", "README.md", "CITATION.cff", "LICENSE"):
            value = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("Marksman Capital USA", value)
        self.assertIn("Hurling", (ROOT / "CITATION.cff").read_text())

    def test_linked_resources_and_entrypoint_size(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(text.splitlines()), 150)
        for rel in re.findall(r"\]\(((?:references|scripts)/[^)]+)\)", text):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_version_record(self):
        for name in ("CITATION.cff", "CHANGELOG.md", "README.md"):
            self.assertIn("0.1.0", (ROOT / name).read_text(encoding="utf-8"))


if __name__ == "__main__": unittest.main()
