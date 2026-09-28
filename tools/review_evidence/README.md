# Review evidence builder

This local tool packages exact committed source versions and explicitly selected
review material into one ZIP for a developer to hand off. ZIPs are output
artifacts outside the repository. The tool does not fetch evidence, run tests,
judge claims, or send the packet anywhere.

Use the repository's hash-locked Python 3.12 environment and run with bytecode
writes disabled:

```sh
PYTHONPATH=. python -B -m tools.review_evidence.review_evidence build \
  --repo-root /absolute/repository \
  --request /absolute/request.json \
  --evidence-root /absolute/existing/evidence \
  --output /absolute/new-packet.zip
```

`--evidence-root` is needed only if the request selects local files. The output
parent must exist and the final ZIP must be new and outside source/evidence roots.
The request format is `review_evidence/request-schema.json`; an illustrative
request is in `docs/plans/review-evidence-packaging/reports/example-request.json`.

The JSON result has `built` (exit 0), `built-with-gaps` (exit 1), or a failure
(exit 2). References and missing local evidence are explicit gaps. The manifest
records assembly and byte hashes, not CI authenticity, claim satisfaction, or
acceptance. The builder validates its own completed staging archive before
publishing with a no-replace operation. There is no separate ZIP check command.
Imported evidence from another repository can carry a caller-reported repository
label and subject object ID; those fields never inherit the primary candidate's
identity or authenticate the external source.

Selected source uses exact commit IDs, Git object reads, and local-only Git
commands. Dirty worktrees, staged changes, and untracked ZIPs are ignored as
source. The generated index links to included complete files and the primary
patch; imported records are kept verbatim.

## Local filesystem and patch boundaries

Output and evidence directory chains are opened without following symlinks and
retained for the operation. Local evidence reads are relative to their admitted
root; a changed requested root is an unavailable input, even when a file is
missing. Staging, ZIP validation, no-replace linking and owned cleanup stay tied
to the selected directory/file handles. A replaced output pathname cannot redirect
those effects into a source or evidence directory. Requested directory identity is
rechecked before and after publication; a detected change aborts and removes only
this attempt's own link. These guards prevent pathname substitution from redirecting I/O. They are not
a sandbox against an actor able to relocate the held directory itself, replace
mounts, or rewrite process memory. Other writers' existing output is never replaced.

Output must also be outside both the private and common Git administrative
directories. Linked worktrees and separate-Git-directory repositories are supported
when output is outside all those roots. Portable ZIP validation includes directory
prefix spellings and file/directory collisions after NFC normalization and case
folding, not just duplicate complete member names. It rejects conflicting paths
without renaming source files or dropping members.

The primary patch is acquired through Repository Git's `revision_patch` boundary.
It keeps the candidate's committed attributes and exact binary/mode changes but
fixes patch formatting. Configured/global/system attribute files are excluded;
`info/attributes`, symlinked administrative `info` directories and local custom
diff-driver semantics are explicitly unsupported. These higher-precedence inputs
cannot be silently interpreted as committed source. Admission is checked before
and after the bounded Git command. Repository configuration must remain stable
through that observation; this is not a lock against a hostile local configuration
writer. No input configuration is edited to make it admissible. Ordinary Git
capture/publication and generic Git command behavior are unchanged.

The packet's `implementation.source_sha256` is specifically a digest of the
installed `packet.py` module. It is not a fingerprint of the entire tool, its
schema, dependencies or Git implementation, and it does not authenticate them.
