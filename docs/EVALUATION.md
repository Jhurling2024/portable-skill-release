# Evaluation — v0.1.1

## Checkout regression fixed in v0.1.1

A fresh v0.1.0 clone in an arbitrarily named directory reproduced a metadata-test
failure: the test compared the skill name to the source-checkout directory name.
Release bytes and helper behavior were unaffected. v0.1.1 compares the skill's
declared identity to CITATION.cff and includes a renamed-checkout regression case.
The original tag is preserved and marked superseded; install folders should still
match the declared skill name. This adds one packaging test to the initial suite.

## Executed tool scenarios

Initial helper run: Python 3.12 on Windows, 13 unittest cases, 12 passed and one
manifest-symlink case skipped because this local sandbox could not create symlinks.
Exit 0. The local test harness used a writable workspace temporary directory after
the default sandbox temporary location denied writes. No product code was weakened
to accommodate that environment failure.

Executable cases cover deterministic creation, exact-byte LF/CRLF drift, missing and
extra files, duplicate/traversal manifest entries, credential-like file names,
VCS/bytecode exclusions, both root/nested layouts, required files, Unicode/spaces,
read-only checking, manifest symlinks where supported, and CLI success/mismatch/error.

Independent package tests check the shipped manifest with a separate hashlib
implementation, required metadata and credit, linked resources, entrypoint size,
and version records. CI runs on Windows and Linux and exposes skips in the log.
Integrity is checked after final edits and again from clean published checkouts.

## Instruction review

Reviewed against requests to mirror a nested skill, explain checkout-only checksum
failures, cut a corrected release, and distinguish publication from installation.
This is an author's instruction review, not a blind independent model evaluation.
No baseline-versus-skilled model experiment or production installation was run.

## Limits

The manifest can be maliciously regenerated along with a changed package; it is not
a signature or authenticity proof. The helper rejects links, unsafe paths, and some
obvious credential filenames but is not a complete secret or malware scanner.
Concurrent filesystem mutation, hard links, and hostile filesystem behavior remain
outside the trust model. Cross-platform tests do not establish every agent client's
ability to load the skill, nor improved model performance.

Run from the package root: `python -m unittest discover -s tests -v`.
