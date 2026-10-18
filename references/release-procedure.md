# Release procedure

1. Inspect the current registration record and publish destination. Select only the
   intended package; preserve upstream license notices if any material is reused.
2. Run package and helper tests without network credentials or production access.
3. Make release metadata consistent: skill version, changelog, citation, readme,
   attribution, and release notes. Regenerate the manifest after the final edit.
4. Inspect `git diff --cached` before committing. A clean staging tree does not scan
   ignored private files; use a clean release directory populated by an explicit copy.
5. Verify a clean checkout with the user's actual checkout policy. LF versus CRLF is
   a real byte difference. Root and nested layouts must both pass; VCS internals do
   not belong in the artifact inventory.
6. After an authorized push, verify the remote SHA/tag and run checks again from a
   fresh clone. For an origin/public mirror, compare SHA256SUMS in both repositories.
7. Record actual OS, runtime, test command, exit status, and unsupported conditions.

## Failure signals and recovery

- Changed hash: compare raw bytes and checkout attributes before assuming tampering.
  Do not rewrite an expected digest merely because the mismatch is inconvenient.
- Extra/missing file: inspect references and the release allowlist; rebuild from the
  inspected source, regenerate the manifest, and repeat a clean check.
- Root-only failure: inspect `.git` enumeration and relative paths; test the same
  package in both layouts. Do not disable coverage to obtain a passing result.
- Published defect: leave tag history intact, prepare the smallest fix, issue a new
  version, and identify the superseded release. Never remove a working installed
  skill until the replacement's import and invocation are verified.

The manifest is an integrity inventory, not a signature. Verify the trusted release
commit or publisher separately. Hard links, malicious operating systems, concurrent
mutation, and adversarial filesystems are outside this helper's trust model.
