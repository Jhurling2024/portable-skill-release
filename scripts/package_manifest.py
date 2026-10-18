"""Create or verify a portable skill's exact-byte manifest. No network access."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re

MANIFEST = "SHA256SUMS"
IGNORED_DIRS = {".git", "__pycache__"}


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or any(ord(c) < 32 for c in value):
        raise ValueError("unsafe package path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise ValueError("unsafe package path")
    return value


def inventory(root):
    if root.is_symlink() or not root.is_dir():
        raise ValueError("package root must be a real directory")
    found = {}
    def fail(error):
        raise error

    for here, dirs, files in os.walk(root, followlinks=False, onerror=fail):
        for name in list(dirs):
            if name in IGNORED_DIRS:
                dirs.remove(name)
            elif (Path(here) / name).is_symlink() or (Path(here) / name).is_junction():
                raise ValueError("package directory symlinks are not accepted")
        for name in files:
            file = Path(here) / name
            rel = safe_path(file.relative_to(root).as_posix())
            if file.is_symlink():
                raise ValueError("package file symlinks are not accepted")
            if not file.is_file():
                raise ValueError("package entries must be regular files")
            if rel == MANIFEST or file.suffix == ".pyc":
                continue
            if name == ".env" or name.startswith(".env.") or name.lower() in {"id_rsa", "id_ed25519", "credentials.json"}:
                raise ValueError("credential-like file must be reviewed outside release package")
            found[rel] = hashlib.sha256(file.read_bytes()).hexdigest()
    if "SKILL.md" not in found or "LICENSE" not in found:
        raise ValueError("SKILL.md and LICENSE are required")
    return found


def manifest_file(root):
    path = root / MANIFEST
    if path.is_symlink():
        raise ValueError("manifest symlinks are not accepted")
    return path


def create(root):
    files = inventory(root)
    path = manifest_file(root)
    path.write_bytes("".join(f"{files[name]}  {name}\n" for name in sorted(files)).encode("utf-8"))
    return {"ok": True, "files": len(files), "action": "created"}


def check(root):
    actual = inventory(root)
    expected = {}
    for line in manifest_file(root).read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ValueError("malformed checksum line")
        name = safe_path(match[2])
        if name == MANIFEST or name in expected:
            raise ValueError("manifest self-entry or duplicate path")
        expected[name] = match[1]
    missing = sorted(expected.keys() - actual.keys())
    extra = sorted(actual.keys() - expected.keys())
    changed = sorted(name for name in actual.keys() & expected.keys() if actual[name] != expected[name])
    return {"ok": not (missing or extra or changed), "files": len(actual),
            "missing": missing, "extra": extra, "changed": changed,
            "limitation": "Integrity is not authenticity, safety, or proof of agent performance."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["create", "check"])
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    try:
        result = (create if args.action == "create" else check)(args.package)
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    except (ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
