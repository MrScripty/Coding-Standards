# Findings and Dispositions

## Q1 — Supported runtime/client qualification

Owner: Engine deployment qualification. Status: partially satisfied; client/reviewer gates open.
The locked Python 3.12.3 runtime qualification now passes locally.
The original delivery run used Python 3.13.5 with rpds-py 2026.5.1 and skipped
the exact-runtime qualification test. The configured Codex client and
independent reviewer are not present here. Preserve the supported locked
3.11/3.12 matrix and real-client qualification as explicit acceptance gates.
Local tests and stdio execution do not certify either missing environment.

## D1 — Wider transport and input simplifications

Owner: Engine agent interface. Status: deferred, outside this slice.
Full-schema description duplication has a documented supported-client reason.
Route-plus-content and request-local evidence references require separate
consumer evidence. Retain their current contracts instead of speculatively
removing compatibility or adding new state.
