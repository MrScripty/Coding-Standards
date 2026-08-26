# Standards Recovery Candidate

**Status:** `Implemented; independent acceptance pending`

**Planning comparison baseline:** commit
`3439aae9540786d9734431e633ea5b62afb50592`, tree
`0ff4af77ebe5056c9478f04bf65dd87141f573d8`

**Milestone 1 frozen boundary:** commit
`7f533f59ddd0120a08c36e85f1c631eedbbe0caa`, tree
`70f2ec4f249ae6eb6774a17443b15943f57bdfec`

This report records the source-complete standards-recovery candidate. It does
not claim its own commit identity recursively. The independent acceptance
report must bind the exact clean candidate commit and tree that contain this
report. It does not admit A1b planning, A1b runtime work, or A2.

## Implemented Result

- Six policy families have stable, exact policy-unit ownership and complete
  Router, profile, graph, prompt, template, fixture, suite, and verification
  projections.
- Policy-impact v2 supplies one compiled relationship authority. The generic
  graph remains policy-neutral, and coverage uses an independent provider-v3
  horizon rather than treating graph presence or absence as completeness.
- The protected mapped-consumer closure resolves mechanically from canonical
  suite IDs plus audit-owned exact non-registry consumers. Every selected
  consumer has one non-blocked disposition.
- Final coverage reuses every dependency-valid attestation and proves exact
  active-policy-unit, requirement, attestation, and generated-certificate
  subject equality.
- Freshness, generated semantics, external conformance, schema instance
  equality, content identity, cold-process reconstruction, and intended
  negative diagnostics remain distinct evidence claims.
- The accepted A1 Draft 2020-12 equality disagreement is reproduced and
  preserved for A1b. No A1 runtime behavior, dependency, external corpus, or
  A2 authority changed during recovery.

## Bound Evidence

| Evidence | Result |
| --- | --- |
| [Historical A1 repair reproductions](historical-a1-repair-reproductions.md) | Generated closure, public results, immutable reads, cold reconstruction, version identity, and exact acceptance-oracle failures reproduced. |
| [JSON Schema instance-equality reproduction](json-schema-instance-equality-reproduction.md) | Local agreement is distinguished from Draft 2020-12 external conformance; runtime correction remains A1b-owned. |
| [Pre-policy scope audit](pre-policy-scope-audit.md) | Independent consumer classes and planned dispositions were established before policy mutation. |
| [Consumer dispositions](standards-recovery-consumer-dispositions.md) | Exact `W/S/E/R` closure, graph reconciliation, policy locators, and one non-blocked disposition per selected consumer. |
| [Final coverage](standards-recovery-coverage.md) | Frozen authority identities and exact subject, requirement, attestation, and certificate bindings. |
| [Reference-only Licensing decision](draft-2020-12-reference-licensing-decision.md) | Exact selected specification sources and resulting no-incorporation obligations. |

## Verification

The following independent lanes passed on the source-complete worktree:

```text
python3 -m unittest discover -s tools/standards_applicability/tests
python3 -m unittest discover -s tools/standards_metadata/tests
python3 -m unittest discover -s tools/graph_engine/tests
python3 -m unittest discover -s tools/standards_policy_impact/tests
python3 -m unittest discover -s tools/standards_graph/tests
python3 -m unittest discover -s tools/standards_analysis/tests
python3 -m unittest discover -s tools/standards_engine/tests
python3 -m unittest discover -s tools/standards_verifier/tests
python3 tools/standards_engine/contracts/generate_contract.py --check
python3 tools/standards_engine/contracts/validate_contracts.py
python3 tools/standards_verifier/generate_inventory.py --check
python3 tools/standards_verifier/verify.py --all
python3 tools/standards_verifier/verify.py --complete
ruff check <every Python path changed from the planning comparison baseline>
git diff --check
```

Observed results were green: all focused package suites passed; generated
contract and retained-migration artifacts were fresh; every registered
declarative suite passed; the complete checkpoint passed every retained Bash
migration checker; plan structure and lifecycle fixtures passed; every
recovery-changed Python path passed Ruff; and diff hygiene passed. Diagnostic
suite, checker, relationship, rule, or corpus totals are not acceptance
oracles.

A repository-wide Ruff diagnostic was not used as this recovery's gate because
it reports pre-existing findings in protected files outside the admitted write
set. The repository-wide behavioral oracle remains the complete checkpoint;
lint acceptance is exact over the recovery's Python delta.

## Scope Result

No attestation, policy, graph, suite, generated artifact, runtime, package test,
external corpus, dependency, A1b implementation, or A2 path changed in
Milestone 2. The exact candidate commit and tree remain for the independent
reviewer to bind after this report is committed.
