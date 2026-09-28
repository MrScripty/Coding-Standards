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

Selected source uses exact commit IDs, Git object reads, and local-only Git
commands. Dirty worktrees, staged changes, and untracked ZIPs are ignored as
source. The generated index links to included complete files and the primary
patch; imported records are kept verbatim.
