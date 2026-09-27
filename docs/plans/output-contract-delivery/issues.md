# Findings and dispositions

- O1 — host qualification, integration owner: actual Codex/model is unavailable in
  this execution. Keep eager delivery default; qualify opt-in on-demand using the
  updated existing harness and record actual model-visible declarations/results.
- O2 — environment, integration owner: local Python/dependency versions differ from
  the locked supported runtime. Preserve the lock and require exact-diff CI.
- O3 — review, integration owner: independent external review remains required.
- O4 — identity, fixed in this slice: omitted output schemas must still contribute
  their exact contract digests to catalog identity; test output-only changes.
