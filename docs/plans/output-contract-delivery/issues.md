# Findings and dispositions

- O1 — host qualification, integration owner: the restarted Codex authoring
  connection now uses native/on-demand interface 42. Direct navigation, reads,
  relationship traversal, targeted output discovery and invalid-input feedback
  worked; see the connected observation in `verification.md`. A model-authored
  proposal-to-readiness run with real evidence under this delivery remains open.
  A disposable Codex app-server attempt matched the catalog but stopped before
  proposal execution because its approval policy blocked the call; see
  `verification.md` and the retained private trace. Do not classify this as a
  standards Engine workflow rejection or a readiness pass.
  Keep eager available for identified supported consumers that still require it;
  no new optimization is indicated by these observations.
- O2 — environment, integration owner: local Python/dependency versions differ from
  the locked supported runtime. Preserve the lock and require exact-diff CI.
- O3 — review, integration owner: independent external review remains required.
- O4 — identity, fixed in this slice: omitted output schemas must still contribute
  their exact contract digests to catalog identity; test output-only changes.
