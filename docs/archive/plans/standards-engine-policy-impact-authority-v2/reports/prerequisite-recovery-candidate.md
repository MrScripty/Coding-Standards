# Policy-Impact Authority V2 Recovery Candidate

**Status:** `Implemented; independent acceptance pending`

**Admitted recovery start:** commit
`879c29899a764a7c000542a4f256ce70718656d6`, tree
`bae195b37e07c39e28af7773365b20c65dfa9870`

This report records the source-complete acceptance-recovery boundary. It does
not claim its own commit identity recursively. The independent acceptance
report must bind the exact clean candidate commit and tree containing this
report. It does not admit standards-recovery implementation, A1b, or A2.

## Recovered Contract

- One global `required-registered-suite` rule owns evidence-owner behavior.
  Every declaration must name one registered suite; unsupported rule values,
  omitted evidence, and the retired per-kind field reject through typed
  diagnostics. No optional-evidence or compatibility mode exists.
- Every present optional authoring field decodes strictly. A malformed value
  retains its exact authored-field diagnostic and cannot become absence while
  crossing the graph Adapter.
- Direct and registered verifier loaders translate policy-impact, metadata,
  and graph failures into the verifier's typed diagnostic Interface.
  Programming errors are not caught as caller failures.
- Compatibility evidence derives relationship kinds and representative target
  classes from the loaded contract and executes every pairing. It stores no
  mutable relationship, artifact, edge, or standards total.

## Bound Coverage

| Authority | Exact identity |
| --- | --- |
| Coverage horizon | `sha256:538c9ef051b79129beb5d471394d9c399c7e3c2882567c6aad4c16c1b4d62f43` |
| Compiled declarations | `sha256:dde852daaa6bb60d1987f44f46140e9de80cc3bd0c9d6277ec2f7fa037c8a0dd` |
| Provider contract | `sha256:e4124f6088b1c21c5e8a7d707cee7f57bb649fb0e6f129b9acaee5f2695899ed` |
| Authoring contract | `sha256:79e3da8c9b146588bff81a1da695a852680425edd68439d57dcea402e9948a4b` |
| Supplemental catalog | `sha256:aff67842c9b61404bc32b0755539b20ada91931912e597354d2b9d426815f620` |
| Fact schema | `sha256:694b87b31797467a94d0aaacb5a30c40c3ed259fc66e3811172d1c5e4e243884` |
| Transition projection | `sha256:b36112c64cb480e9c226bb832ada05577fb2345811bc731c201375b9afaf6b1e` |

The corrected and rejected compilers produce byte-identical canonical semantic
projections with SHA-256
`410a4d6fcaa3ef2fac61f1c09abafdc9f2e0089dd2147e204067c439375598f6`.
Topology, relation, target, scope, applicability, evidence owner, rationale,
artifact metadata, and public shape are unchanged. Only dependency identities
that previously represented the ineffective evidence configuration changed.

Coverage compilation proved exact equality:

```text
active policy-unit subjects
  == requirement subjects
  == attestation subjects
  == certificate subjects
```

Each subject has one current requirement, complete owner-local attestation,
and generated certificate. No stale, duplicate, extra, missing, excluded,
unresolved, or blocked subject remains. The
[recovered certification evidence](certify-recovered-coverage.md) records the
review, authorization, invalidation contract, and exact old/new authority
identities.

## Verification

The following commands passed against the source-complete worktree:

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
RUFF_CACHE_DIR=/tmp/coding-standards-ruff-cache ruff check \
  tools/standards_policy_impact \
  tools/standards_verifier/standards_verifier/policy_impact.py \
  tools/standards_verifier/tests/test_policy_impact.py
bash evaluation/standards-effectiveness/check-plan-structure.sh \
  docs/archive/plans/standards-engine-policy-impact-authority-v2/plan.md
git diff --check
```

Observed results were green: all 585 focused package tests passed; generated
contract and retained-checker inventories were fresh; 32 examples, 8 identity
fixtures, 4 operation envelopes, and 141 public definitions validated; all
224 registered declarative suites passed; the plan lifecycle fixtures passed;
and the complete checkpoint passed all 53 retained Bash migration checkers. No
Bash checker was added or extended.

## Scope Result

- Every mutation remains inside the admitted Milestone 2 write set.
- The supplemental catalog, relationship declarations, canonical metadata,
  suite registry, horizon declaration, public A1 contract, generated outputs,
  and transition-provenance TSV remain unchanged.
- No runtime compatibility loader, path classifier, graph-engine policy
  behavior, mutable count oracle, third-party dependency, A1b implementation,
  or A2 authoring work was added.
- Standards recovery remains blocked until this prerequisite receives exact
  independent acceptance and a separately admitted resume transition.

## Acceptance Request

An independent reviewer must review the exact clean candidate against
repository Standards and this plan, verify the commit/tree identity, and
author only `prerequisite-acceptance.md`. PIA2-A10, PIA2-006, final plan
acceptance, and standards-recovery resumption remain pending until that report
and the subsequent mechanical lifecycle transition.
