# Standards Recovery Milestone 1 Router-Projection Verifier Admission

## Reviewed Boundary

- Result: `Approved for Milestone 1 Router-projection verifier admission`.
- Reviewed candidate commit:
  `879475365ea43c8962dbb319347e80cff665a87d`.
- Reviewed candidate tree:
  `231db42d0f9af703fd2c48343095ff203676e0ab`.
- Review axes: repository Standards and the exact Router-projection verifier
  recovery contract recorded in SESR-029.

The reviewed worktree was clean, `HEAD` matched the candidate commit, and the
candidate commit resolved to the reviewed tree. This report is the only
repository change authorized by the independent-review operation.

## Standards Review

No findings.

Independent review confirmed that the candidate follows the routed Planning,
Verification, Commit, and verification-migration authority:

- the verifier's loss of canonical target identity is recorded as a named
  systemic re-plan trigger rather than repaired while Milestone 1 is active;
- the plan, current phase, next slice, Milestone 1, ledger, and SESR-029 agree
  on the `Blocked` lifecycle before verifier implementation;
- the repair is correctly classified as `shared-contract` because it changes
  shared verifier behavior, and it retains separate admission, implementation,
  two-stage verification, and final exact-tree acceptance;
- the former green-complete-checkpoint prerequisite and blanket verifier
  exclusion are explicitly `Superseded` only where the new M1/M2 sequence
  requires replacement;
- the sole proposed mutation transfer is
  `tools/standards_verifier/standards_verifier/policy_impact.py` from the
  audited protected set to the exact Milestone 1 write set; and
- the generated graph deltas remain the exact previously admitted evidence,
  while coverage, policy, compiler, provider, checker, A1b, and A2 authority
  remains unchanged.

Standards total: zero findings.

## Specification Review

No findings.

Independent review confirmed the proposed correction is both necessary and
sufficient:

- policy-impact graph edges retain distinct canonical targets for `router` and
  `evaluation/standards-effectiveness/router-projection.toml`, while the
  current `ImpactEdge` retains only their repository paths;
- `router` resolves through canonical module membership to
  `STANDARDS-ROUTER.md`; the executable target is not a module and is owned by
  the exact registered `standards.policy-impact-catalog` source;
- the executable target has exactly two incoming `router-projection`
  relationships, from the Router and Generated Contract policy units;
- retaining the graph target node ID permits registry-driven classification
  without changing relationship or provider contracts;
- canonical module targets continue through module metadata validation and
  must resolve to module ID `router`;
- exact catalog-registered non-module projection targets delegate to the
  existing strict `load_router_projection()` adapter with the already loaded
  canonical module corpus and the edge repository path; and
- `AnalysisError` remains translated at the verifier adapter boundary, so
  strict Router projection failures keep typed engine diagnostics and do not
  become exception fallback or generic consumer failures.

Path or suffix inference, literal-path allowlists, fallback after malformed
module metadata, duplicate TOML parsing, unrelated catalog discriminators, a
new relation kind, relationship removal, and early coverage renewal are neither
needed nor admitted.

Specification total: zero findings.

## Two-Stage Evidence Contract

Milestone 1 may implement only the admitted verifier adapter correction after
the lifecycle transition and exact-head `start`. Its focused evidence must
prove both executable Router projection relationships, continued canonical
Router module validation, strict Router projection loading, exact generated
freshness and TSV deltas, and unchanged unrelated suites. The canonical
complete checkpoint must advance past `METADATA.FIELD_COUNT`; its sole
permitted remaining result is the already reproduced
`COVERAGE.STALE_ATTESTATION`. Any other diagnostic, broader source change, or
weaker classification invalidates this admission.

After all Milestone 1 relationship and horizon authority is frozen, Milestone
2 may renew coverage exactly once under its existing write set. Only after that
renewal may the three deferred cardinality-test corrections execute. The
unchanged `policy-semantic-impact` suite, affected verifier tests, and canonical
complete checkpoint must then pass before exact-tree standards-recovery
acceptance. The intermediate stale-coverage result is sequencing evidence, not
acceptance evidence.

## Verification

Independent read-only verification established:

- exact candidate commit/tree resolution and a clean worktree;
- the candidate changes only three governance files and the three previously
  admitted generated dependency-graph TSVs, with no verifier implementation;
- generated freshness passes at 53 current Bash verifiers, 57 dependency
  nodes, 379 edges, and 57 components;
- structured comparison with the admitted start base adds exactly four
  `contract_reference` edges, changes exactly two node
  `contract_inbound_count` fields from `1` to `3`, and changes exactly two
  component `contract_inbound_files` fields, with no row or topology change;
- plan structure and plan lifecycle checks pass;
- `standards-recovery-routing`, `evidence-oracle-boundaries`, and
  `systemic-finding-replanning` pass with 6, 7, and 9 checks respectively;
- both strict Router projection loader tests pass, and direct strict loading
  resolves projection ID `router.executable-projection`, owner `router`, seven
  facts, and 39 rules;
- the current verifier policy-impact suite passes seven of nine tests; its two
  repository-graph tests stop at the same executable-projection
  `METADATA.FIELD_COUNT` error;
- the canonical complete checkpoint reports 224 selected, 223 passed, one
  failed, and zero blocked, with `METADATA.FIELD_COUNT` as the sole failure;
- direct coverage compilation over the same frozen authority returns typed
  unavailable `COVERAGE.STALE_ATTESTATION` for
  `evaluation/standards-effectiveness/policy-coverage/attestations/workflow.commit.toml`;
  and
- candidate `git diff --check` passes.

## Authorized Transition And Implementation

This approval authorizes one mechanical transition commit after the commit
that contains this report. The transition commit must have the report commit as
its direct parent and may change only:

- `docs/plans/standards-engine-standards-recovery/plan.md`;
- `docs/plans/standards-engine-standards-recovery/execution-ledger.md`; and
- SESR-029 lifecycle fields in
  `docs/plans/standards-engine-standards-recovery/issues.md`.

The transition may only record the reviewed candidate and report identities,
move the plan and Milestone 1 from `Blocked` to `Planned`, set the current phase
to Router-projection verifier recovery ready for `start`, and name exact-head
Router-projection verifier recovery `start` as the sole next operation. It does
not itself authorize verifier implementation.

Only a valid `start` while that transition is current `HEAD` may record the
transition commit/tree, move the plan and Milestone 1 to `Active`, and authorize
modification of exactly:

- `tools/standards_verifier/standards_verifier/policy_impact.py`.

The implementation must retain the canonical target node ID on `ImpactEdge`,
resolve module membership from the already loaded canonical corpus, preserve
module metadata validation for canonical Router targets, require a non-module
projection target to be an exact node from the registered policy-impact
catalog, and delegate its repository path to `load_router_projection()`.
Existing typed `AnalysisError` translation remains the error boundary.

Tests, coverage attestations, policy declarations, policy units, node catalog,
suite registry, relationship kinds, provider contracts, compiler behavior,
Router authority, generated artifacts, checker sources, A1b, and A2 remain
excluded from this implementation slice. Any intervening commit, additional
transition path, broader implementation delta, path-based classification,
fallback, or different M1 terminal diagnostic invalidates this approval and
requires re-planning.

## Decision

Milestone 1 Router-projection verifier recovery is approved for the exact
reviewed candidate. This report does not transition or start Milestone 1,
modify verifier behavior, renew coverage, accept generated-evidence closure,
create A1b authority, or activate A2.

The sole next authorized operation is the constrained mechanical lifecycle
transition above.
