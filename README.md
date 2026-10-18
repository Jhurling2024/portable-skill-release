# Portable Skill Release

Catch missing files, extra files, and changed bytes when a skill moves between a nested origin package and a public repository.

**Justin Hurling — Founder, Originator and Project Creator** · [@Jhurling2024](https://github.com/Jhurling2024)
**Marksman Capital USA LLC · Marksman Capital USA AI** · MIT · v0.1.0

[![Tests](https://github.com/Jhurling2024/portable-skill-release/actions/workflows/package-tests.yml/badge.svg)](https://github.com/Jhurling2024/portable-skill-release/actions/workflows/package-tests.yml)
[All Marksman AI Skills](https://github.com/Jhurling2024/marksman-ai-skills) · [Release](https://github.com/Jhurling2024/portable-skill-release/releases/tag/v0.1.0)

## Use it

Read [SKILL.md](SKILL.md), review the bundled script, and copy this entire repository
into a skill directory supported by your agent, named `portable-skill-release`. For the existing
OpenCode convention, use `YOUR_PROJECT/.opencode/skills/portable-skill-release/`. Inspect for an
existing installation before copying. Registration in a folder is not proof that a
particular client loaded it; verify invocation in your installed version.

The helper uses Python 3.12+ standard library, runs locally, and has no network,
telemetry, credentials, or paid dependency. From the skill root:

```text
python scripts/package_manifest.py check .
python -m unittest discover -s tests -v
```

For exact-byte package checking, use the bundled helper's `check` action above,
or run the independent packaging test. SHA256SUMS
covers the release files; obtain it from a trusted commit, not an untrusted third party.

## Evidence and limits

See [evaluation](docs/EVALUATION.md) and [research provenance](references/sources.md).
Tests measure helper behavior and packaging. They do not establish improved LLM task
performance, universal client compatibility, source truth, or security certification.
This skill neither grants permissions nor changes any existing installed skill.

This is a companion to [Common Sense Skill](https://github.com/Jhurling2024/common-sense-skill), which is
maintained and versioned separately. [AUTHORS.md](AUTHORS.md) records human direction
and AI assistance. MIT allows commercial reuse with its notice; attribution is not
a claim of exclusive ownership of general ideas or of third-party research.

## Contribute

Open an issue with the smallest reproducible failure, expected result, and environment.
Submit fixes with a regression case and MIT-compatible original contributions. Never
include tokens, private customer data, or complete third-party transcripts.
