# Findings and acceptance gates

- Q1 — integration: local runtime is Python 3.13.5 / rpds-py 2026.5.1, not the
  supported locked Python 3.11/3.12 environment. Preserve the lock and obtain CI
  evidence for the exact diff; baseline CI does not certify these changes.
- Q2 — reviewer: independent external review is separate from implementation
  self-review and independent test oracles. Keep Accepted status pending until done.
- D1 — deferred: typed routing-edit families remain outside this capture handoff.
  No new public interface or user-config migration is required by this slice.

- F1 — capture/identity memory sharing, resolved in scope: the handoff originally
  retained duplicate equal byte sets when adding the first identity proof. Retain
  the existing exact key for identity-only extension. Regression plus before/after
  allocation accounting verify the fix within compiled_cache.py, without changing
  key equality, limits, codec/compiler checks or current durable validation.

## Final source disposition

F1 is resolved by exact key retention and independent memory-accounting evidence.
All local C1 code/behavioral checks passed. Q1 and Q2 remain explicit acceptance
requirements, not reasons to weaken the proof, change the lock or add a fallback.
No other source blocker was demonstrated. D1 remains intentionally deferred.
