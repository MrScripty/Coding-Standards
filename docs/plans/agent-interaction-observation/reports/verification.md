# Observation verification

## Subject and environment

Exact O1 source candidate: `/tmp/coding-standards-observation-o1`, baseline `149ba317e9397519bc181a048ecf76aef129a69c`, tested staged tree `96d775f8b3885ef08ff9b2d72396cc13216ec90c`. The [indexed-file SHA-256 inventory](qualification/source-inventory.json) and [recoverable patch](qualification/source-candidate.patch.gz) are retained in the repository. All 1,523 indexed hashes were unchanged throughout final qualification. The six source/test/document files match the original worktree; unrelated existing changes were not incorporated into this isolated candidate.

Linux, Python 3.12.3, existing `/home/jeremy/.local/share/standards-engine/venv/bin/python`. Installed lock versions: attrs 26.1.0, jsonschema 4.26.0, jsonschema-specifications 2025.9.1, referencing 0.37.0, rpds-py 2026.6.3, typing-extensions 4.16.0. `pip check`: no broken requirements. No installation occurred.

## Executed evidence

- Focused recorder and stdio tests: 14 tests passed in 25.436s, `/tmp/observation-focused-final.log`. Following the final regression-oracle correction, 10 recorder tests passed in 1.167s, `/tmp/observation-recorder-final.log`.
- Observation plus existing MCP, RuntimeIdentity and output-delivery tests: 41 tests passed in 61.836s, `/tmp/observation-affected.log`, before the independently reviewed harness bound and special-path correction. The later 14+10 runs verify those localized changes.
- Original worktree recorder tests: `/tmp/observation-original-recorder.log`; transport fixture stops before O1 with the existing mismatch recorded in O-I1. This does not constitute combined-worktree acceptance.
- Generated suite-input projection refreshed through its owning `write_suite_input_projection` producer in the isolated candidate; `check_suite_input_projection` returned 0. No generated contracts were modified.
- `git diff --check`: passed. Scoped source diff confirms no change to agent contracts/generated definitions or Snapshot/Analysis/domain owners.
- Independent source review and both finding dispositions: [review](independent-review.md).

## Claim map

| Claim | Deciding evidence |
| --- | --- |
| O-A1 | Real stdio literal invocation list equals ordered SQLite request JSON, including absent names/arguments, invalid shapes and extra supplied data; lifecycle traffic excluded. |
| O-A2 | SQLite session fields equal the actual process RuntimeIdentity metadata across both purposes and selected catalog/output modes. |
| O-A3 | Complete enabled/disabled/initialization-failed/write-failed stdio outputs compare equally after replacing only the known per-process UUID in both result encodings. Read/discovery workflows, protocol errors, catalogs and schemas are compared. MCP results never consume recorder output by construction. |
| O-A4 | Literal projection expectation retains four string identifiers only; nested/bodies/message/details/input feedback fields are excluded. Actual standards read body remains absent from recorded metadata. |
| O-A5 | Real SQLite triggers fail session/request/metadata/close writes after admission. Recorder becomes inert; one exact bounded diagnostic is asserted. Stdio write failure after actual handshake leaves all results unchanged; metadata failure is also compared through the real MCPServer. Diagnostic-channel failure is contained. |
| O-A6 | Inert recorder holds no dictionary/state; failing connect/serialization spies are never invoked. Disabled real process creates no file in its selected working directory. |
| O-A7 | Separate real SQLite reader sees committed pre-dispatch request. Cold sessions retain original rows and reset only per-session sequence; version/schema negatives retain exact database bytes. Literal relative `:memory:` resolves to a real durable file. |
| O-A8 | All 13 locked workflow groups passed (1,255 tests), with 73/73 complete-verifier suites passed; logs/results below. Source diff proves agent contract/domain source unchanged. Combined worktree requires O-I1 reconciliation. |
| O-A9 | Independent read-only review found no product defect and confirmed both advisory/test-oracle findings resolved. |

## Full locked workflow — passed

The final corrected source passed all thirteen package-discovery groups from `.github/workflows/purpose-separated-engine.yml`: 1,255 tests total. The Engine group passed 625 tests in 2,202.090s; the twelve shorter groups were refreshed on the same frozen source and passed 630 tests. The complete verifier exited 0: selected 73, passed 73, failed 0, blocked 0. [Results, commands and source identities](qualification/results.json), [full Engine log](qualification/standards_engine.log), [complete verifier log](qualification/complete.log).

The earlier Engine session 56279 stopped at the daemon restart with no terminal result; its [incomplete log](qualification/standards-engine-interrupted.log) is retained and contributes no passing evidence. Replacement native session 81022 completed with exit 0; refreshed-short-group session 22488 completed with exit 0. The two repaired fixture consumers also [passed directly](qualification/publication-fixture.log); independent fixture review found no material findings.

## Combined original worktree recheck

The owning suite-input producer regenerated the original worktree projection using its current inputs; its freshness check returned 0. Only new O1-owned files were added to the index for membership observation; unrelated staging was preserved. The complete verifier (`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:tools/standards_verifier` with the locked interpreter and `tools/standards_verifier/verify.py --complete`) exited 2: selected 73, passed 72, failed 1, blocked 0. The sole failure is `policy-semantic-impact` / `ANALYSIS.EVIDENCE_DIGEST_MISMATCH`, confirming O-I1. Retained [original-tree verifier log](qualification/original-complete.log). This is current-tree structural evidence, not passing combined-worktree acceptance.

## Acceptance scope

The original worktree's unrelated modified standards-library plan contradicts retained coverage evidence and stops current-content fixture compilation. O1 does not rewrite receipts or repair that other owner's normative/evidence state. Candidate evidence applies only to the named isolated source. Installed MCP configuration remains unchanged; operator destination selection/deployment is a later action after source acceptance.

All O-A1–O-A9 are satisfied for the named isolated source. On 2026-10-01 the user explicitly dismissed O-I1 as material to this work. O1 is accepted on that verified source; O-I1 is retained as a nonblocking external finding. The combined original tree is not represented as having passed its complete verifier.

Final record and evidence checks: canonical projection freshness passed after all records were indexed. Complete verification after the records still passed 73/73 suites on the isolated candidate and failed only O-I1 (72/73 passed) on the original tree. The replay patch is gzip-compressed to retain exact unified-diff context without making context whitespace an artifact whitespace violation. Decompress it and use `git apply --index` on the recorded baseline to reconstruct the tested source.
