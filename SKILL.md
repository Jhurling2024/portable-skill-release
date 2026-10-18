---
name: portable-skill-release
description: Package and verify an Agent Skill for distribution across repository-root and nested-folder layouts. Use when cutting a skill release, importing a public mirror, debugging checksum failures across operating systems, or checking that published bytes match an inspected package.
license: MIT
metadata:
  author: "Justin Hurling (Founder and Originator)"
  copyright-holder: "Marksman Capital USA LLC"
  creator-github: "Jhurling2024"
  version: "0.1.0"
  opencode/slash: "true"
---

# Portable Skill Release

Make an inspected skill survive distribution unchanged. Report the package version,
release commit, manifest result, actual test environment, and any untested clients.

## Establish the package boundary

Find the exact skill root containing `SKILL.md`. Inspect required metadata, linked
resources, license, attribution, and runtime dependencies. Keep the skill name equal
to its installation folder name. Read existing registration and release conventions;
do not create an unrelated registry or silently migrate installed copies.

Only stage files selected for publication. Keep credentials, private transcripts,
unreviewed binaries, and unrelated application files outside the package. Use an
allowlist when copying from a private repository to a public one. Review staged
changes, not just working-directory contents. Common credential filenames are
rejected by the helper; it is not a complete secret scanner.

## Preserve and verify bytes

Use Python 3.12+ and the bundled helper:

```text
python scripts/package_manifest.py create path/to/skill
python scripts/package_manifest.py check path/to/skill
```

`create` explicitly writes `SHA256SUMS`; `check` reads only and requires exact file
coverage as well as matching SHA-256 hashes. Both reject symlinks and unsafe paths.
Only `.git`, `__pycache__`, `.pyc`, and the manifest itself are omitted. Extra files
are failures, not silently ignored by `.gitignore`. Read
[the release procedure](references/release-procedure.md) for import and checkout checks.

Hash the bytes that will ship. Do not normalize line endings during verification to
make a mismatch disappear. Set and test an appropriate `.gitattributes` policy before
tagging; byte-identical skill packages in this project use `* -text`.

After the last package edit, regenerate the manifest and run tests. Then verify a
fresh checkout at the intended commit in both relevant layouts: skill at repository
root (with `.git`) and skill nested inside an origin repository. Keep mirror metadata
outside the copied package so identical versions have identical manifests.

## Publish within the task's authorization

Follow the user's existing repository, review, and tagging rules. Existing explicit
authorization to publish a concrete release remains valid; a skill cannot grant
itself permission. Do not overwrite a release tag to hide a defect. Make a corrected
version and clearly mark affected releases.

Verify the remote tag, release assets, and fresh downloaded/checked-out package. A
release receipt is not an installation test. Record package tests, client invocation,
and measured agent behavior separately. A valid checksum does not establish safety,
authenticity, authorship, or useful behavior. A skill that merely loads may still harm
task performance; do not promise benchmark gains without a matched comparison.

Exit codes: 0 verified/created, 1 integrity mismatch, 2 invalid input or I/O failure.
The helper performs no network calls, installs nothing, and never pushes or publishes.

Research provenance: [references/sources.md](references/sources.md).
