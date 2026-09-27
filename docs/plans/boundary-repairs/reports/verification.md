# Boundary repairs — verification and delivery

**Source baseline:** `af6b829aae7beba98c7aa523c51c832011587d12` (interface 43).

**Candidate:** interface **44**. **State:** source implemented; Verifying pending
supported locked-runtime CI and independent material review. No remote changes or
production standards publication were performed. All database, proposal and Git
publication tests used isolated test material.

## Implemented boundaries

**F04 — Logical graph isolation.** Logical resolution now handles every spelling
before filesystem fallback. Registered nodes/aliases resolve from the registered
view. An unregistered name stays unknown when a same-named file, directory,
symlink or dangling symlink appears or disappears. Filesystem-backed graph
resolution retains its separate containment and unconnected-artifact semantics.
No new registry or resolution mode was introduced.

**F05 — Store selection.** The Engine resolves the selected parent and passes the
final component unchanged to the existing SnapshotStore admission. Final symlinks,
dangling symlinks and directories are rejected without replacing or changing the
database. Relative Engine paths remain cwd-relative; SnapshotModule itself still
requires an absolute Path. Intermediate directory symlinks remain permitted.
This is selected-file admission, not a race-free filesystem sandbox. The existing
unavailable-parent exception behavior was preserved, not generalized in this patch.

**F06 — Integer representation.** After canonical validation, schema-constrained
integral floats become Python integers before domain construction. References,
selected unions, named/anonymous properties, maps, arrays, nullable and implicit
containers, and simultaneous reference/union clauses retain their declared numeric
constraints. Booleans, fractions, out-of-range and non-finite values are rejected
where invalid before conversion. Already-integral Python values retain arbitrary
precision. Number-only/unconstrained positions and opaque literal data with no
integer schema are not coerced. Schema documents, defaults and caller input are
not mutated. Domain semantic-revision rules remain unchanged.

**F07 — Evidence digests.** Analysis EvidenceReference now requires an exact string
containing `sha256:` followed by 64 lowercase ASCII hex digits. Its existing typed
failure is retained. A common conformance corpus exercises Analysis, generated
transport and authoring representations plus the independent validator. Resolved
bytes, provider contracts and current authorization still receive their original
checks; valid-looking syntax never substitutes for evidence.

The shared corpus also found the old wire pattern accepted a trailing newline.
Canonical Digest now additionally declares `maxLength: 71`. The compiler admits
this existing Draft 2020-12 keyword and preserves it in generated projections;
jsonschema remains its sole executable constraint owner. Unicode character-count
and generated-model tests cover that admission. Interface 44 identifies this
narrowed public scalar. No custom regex interpretation or replacement validator
was introduced.

**F11 — Direct CI coverage.** The existing locked CI command sequence now runs the
six existing direct suites for identity, applicability, graph engine, standards
graph, snapshots and Repository Git. No separate CI framework or dependency change
was added. Current version-bearing documentation and examples were updated together.

## Evidence and scope

| Check | Observation |
| --- | --- |
| Complete Engine selection, four file-disjoint shards | 523 tests; initially 522 passed and one stale-example test failed |
| Final integrated Engine rerun | 94 passed, including the corrected test and all newly affected Engine boundaries |
| Reconciled current Engine coverage | All 523 distinct current test IDs observed passing |
| Contracts/compiler final suite | 81 run: 80 passed, one supported-environment check skipped |
| Other ten supporting-package suites | 469 run: 468 passed, one root-dependent permission skip |
| Permission case under unprivileged UID | Passed separately; the original root-run skip is preserved |
| Final graph suite after failure-cleanup improvement | 41 passed, included in the package population above |
| Exact six added CI selections | All exited successfully with the CI's ordinary unittest commands |
| Baseline-to-candidate retained state | Same snapshots, Analysis/status, readiness/status, repeated review and exact readback |
| Altered real fixture evidence | Exact `ANALYSIS.EVIDENCE_DIGEST_MISMATCH`; restoring bytes restores identical readiness |
| Publication boundary during retention check | Baseline accepted main did not advance; no migration, deletion or publication |

The patch adds **28 test methods**, included above rather than additional to these
totals. `DELIVERY/evidence/results-summary.json` reconciles every current Engine test
ID. Final structural, freshness, syntax, diff and reconstruction results are written
separately under `DELIVERY/evidence` so packaging checks are not inferred from test
counts. The complete Engine selection plus focused correction is **not** a claim
of one uninterrupted all-green full-suite run on the final artifact.

### Failures and correction history

The initial regression campaign exposed the audited defects; some early graph
subtests also inherited artifacts after an expected failure. The final test cleans
up each attempted artifact independently. The first numeric workflow assertion
included an extra separator newline from the source module, unlike the exact
heading/body edit submitted; only that fixture expectation was corrected. A
separate container-family probe exposed nullable/implicit and sibling-constraint
construction, which was repaired within the shared decoder. The final additional
ref/oneOf regression covers an admitted shape not currently used by the canonical
corpus, rather than silently leaving the same integer defect in that family.

The full Engine campaign's one failing method found two current discovery examples
still advertising interface 43. Their values were advanced to 44; the freshness
assertion was retained. Final focused tests passed. One earlier contracts invocation
was interrupted by the execution environment before completion and is not counted
as a successful run. A retained-state checker initially looked for a rejection code
at the top level instead of inside the focused workflow outcome; it was corrected
to assert the exact existing wrapper and digest-mismatch code. Original logs and
verdicts are retained separately from successful reruns.

## Contract and state preservation

All **40 operation declarations** are unchanged. Of **326** previous definitions,
**325** are unchanged; only Digest gains its exact maximum length. Analysis request
version **6**, result/state projection **7**, handle versions, schema identity domains
and SQLite formats are unchanged. Valid existing digest values and records need no
conversion. Invalid digest spellings are rejected, not silently repaired.

An actual interface-43 process from the baseline produced a snapshot, proposal,
Analysis and readiness. Independent candidate processes reopened that private store
using interface 44, including a final replay after source finalization. Current byte
verification remained effective. This is real old/new process evidence, not an
in-memory mocked migration. It does not certify arbitrary unsupported historical
formats or the user's production database.

Native-only inputs, both discovery tools, eager/on-demand output choices, purpose
filtering, explicit decisions, atomic batches, and publication/recovery remain.
No cache, garbage-collection, integrity-check policy, routing-fact shortcut, new
session mechanism, authorization behavior or other audit-stage change was made.

## Standards and ownership

Core and the executable Router selected 28 modules with zero unresolved task facts.
The scoped plan, ledger and findings are in `docs/plans/boundary-repairs/`; exact
route/readback evidence is supplied in the delivery. Production changes stay with
Graph resolution, SnapshotStore's existing admission plus its Engine composition,
Contracts' post-validation construction, Analysis evidence validation and the
canonical Digest declaration. The independent validator still decides acceptance.
There is no new production module, registry or runtime dependency.

A material self-review checked the ownership and failure boundaries, exact scalar
and operation deltas, rejection before effects, preservation tests and the changed
consumer population. That is not represented as independent external review.
Normative policy, approval/provenance declarations, user configuration, dependency
locks, unrelated archives and remote refs were not modified.

## Environment and remaining qualification

Local execution: Linux, CPython **3.13.5**, jsonschema **4.26.0**, rpds-py **2026.5.1**.
The supported deployment is locked CPython **3.11/3.12** with rpds-py **2026.6.3**.
A supported-interpreter installation attempt failed on unavailable DNS/network;
no lock was changed or check relabeled as passing. Run the amended existing CI in
its supported environment, and obtain independent review of the material patch
before marking the plan Accepted. No paid model or configured Codex session was run.

## Integration

Use `DELIVERY/README.md` and the read-only per-file baseline check. The patch is
based on `af6b829a`; preserve later or unrelated work instead of overwriting it.
Apply the complete source, example and generated-input update. Restart the MCP
server and refresh/reconnect clients for interface 44. Keep native-only launch
configuration and the existing output-delivery choice; no new mode flag is needed.
Preserve every store and workflow handle. An explicitly selected final-component
DB symlink is now rejected as required by the store contract; select the actual
regular database path rather than deleting data or unlinking user resources.
