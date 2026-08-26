# Policy-Impact Authority V2 Prerequisite Acceptance

**Status:** `Accepted`

## Reviewed Identity

- Accepted candidate commit:
  `7bc8bd070f882eb9779dc678139777d05a6ce7c7`.
- Accepted candidate tree:
  `35a22f824f7ed5f50347032b956b2108fc073f77`.
- Admitted recovery start and direct parent: commit
  `879c29899a764a7c000542a4f256ce70718656d6`, tree
  `bae195b37e07c39e28af7773365b20c65dfa9870`.
- Rejected predecessor candidate: commit
  `101001bd2373631b0474d214871ba11ad1b6e4ab`, tree
  `955e77e06c2477569da6a6f3f8263c602ca7533d`.
- Review axes: repository Standards and the accepted policy-impact authority
  v2 ADR plus Milestone 2 of the active plan.

At review start, `HEAD` matched the accepted candidate, `HEAD^{tree}` matched
the accepted tree, and the worktree was clean. The candidate is the direct
child of the admitted recovery start. Its 19-path delta is wholly contained by
the Milestone 2 write set: the contract, compiler/model, focused compiler and
verifier code/tests, eight owner-local attestation files, three current plan
artifacts, and two recovery reports. This acceptance report is the only
repository change authorized and authored by the independent review.

## Standards Review

No findings.

The candidate conforms to the routed Core, Router, Implementation,
Verification, Planning, Documentation, Commit, Library, Generated Contract,
Build, Contracts, Dependencies, Architecture, and Diagnostics authorities:

- `standards_policy_impact` remains the one policy-impact validity and
  projection owner; no caller-side compatibility classifier or declaration
  parser is introduced;
- the serialized contract replaces repeated dead per-kind booleans with one
  effective required-registered-suite rule and rejects unsupported rule values;
- present authored values are decoded before graph adaptation, so malformed
  optionals retain typed field-specific rejection instead of becoming absence;
- direct and registered verifier loaders preserve lower-Module failure meaning
  through the same typed diagnostic Interface without catching programming
  errors generically;
- focused negative fixtures mutate one valid precondition and assert the exact
  diagnostic code and distinguishing fields;
- compatibility evidence grows from loaded relationship kinds and target
  classes, exercises every representative target pairing, and stores no
  mutable relationship, artifact, edge, or standards total;
- coverage attestations renew through the existing owner-local Interface after
  the corrected contract freeze, without creating a second subject authority;
  and
- the plan truthfully remains `Implemented` with `partial` acceptance and one
  exact-tree review next slice.

No documented-standard breach or baseline code-smell finding was identified.
Standards total: zero findings.

## Specification Review

No findings.

The exact candidate satisfies the Milestone 2 acceptance-rejection recovery:

- `evidence_owner_rule = "required-registered-suite"` is required, validated,
  consumed while loading declarations, and bound into relationship dependency
  identity; `RelationshipKind.evidence_required` and all nine serialized
  copies are absent;
- omitted evidence owners, unsupported global rules, the retired per-kind
  field, and malformed present `validator` values reach their intended typed
  diagnostics;
- registered verifier loading translates policy-impact, metadata, and graph
  failure families consistently with direct loading, while analysis failure
  translation remains typed after coverage compilation;
- every loaded relationship kind is crossed with the complete representative
  target set, including both canonical-router and supplemental
  routing-projection forms, and each pair reaches its exact accepted result or
  `POLICY_IMPACT.INCOMPATIBLE_TARGET`;
- the corrected contract changes dependency identities but preserves graph
  topology, relationship kinds, source/consumer identity, scope,
  applicability, evidence owner, rationale, artifact metadata, provenance, and
  public operation shape;
- active policy-unit, requirement, attestation, and certificate subject sets
  are exactly equal after the corrected freeze, with one complete attestation
  and generated certificate per current subject; and
- the candidate changes no supplemental catalog, relationship declaration,
  canonical metadata, suite registry, coverage horizon, public A1 contract or
  generated output, transition-provenance TSV, standards-recovery artifact,
  A1b artifact, or A2 artifact.

Specification total: zero findings.

## Semantic And Coverage Checks

The rejected and corrected compilers were executed from their exact repository
trees. A reviewer-authored canonical projection covered all compiled graph
nodes, groups, and edges; artifact identity and metadata; effective
relationship-kind semantics; and relationship source, consumer, kind,
applicability, scopes, propagation, evidence owner, rationale, and declaration
provenance. It excluded only the dependency fingerprints intentionally changed
by this recovery and the retired ineffective field. Both projections were
byte-identical at reviewer SHA-256
`44c2fc1eb3597c4447fe20217c58845fb709228e89b732d946cb65e84d99c6dc`.
This independently confirms the semantic equality represented by the
candidate evidence's separately serialized
`410a4d6fcaa3ef2fac61f1c09abafdc9f2e0089dd2147e204067c439375598f6`
projection.

The accepted tree compiled these exact authority identities:

| Authority | Exact identity |
| --- | --- |
| Coverage horizon | `sha256:538c9ef051b79129beb5d471394d9c399c7e3c2882567c6aad4c16c1b4d62f43` |
| Compiled declarations | `sha256:dde852daaa6bb60d1987f44f46140e9de80cc3bd0c9d6277ec2f7fa037c8a0dd` |
| Provider contract | `sha256:e4124f6088b1c21c5e8a7d707cee7f57bb649fb0e6f129b9acaee5f2695899ed` |
| Authoring contract | `sha256:79e3da8c9b146588bff81a1da695a852680425edd68439d57dcea402e9948a4b` |
| Supplemental catalog | `sha256:aff67842c9b61404bc32b0755539b20ada91931912e597354d2b9d426815f620` |
| Fact schema | `sha256:694b87b31797467a94d0aaacb5a30c40c3ed259fc66e3811172d1c5e4e243884` |
| Transition projection | `sha256:b36112c64cb480e9c226bb832ada05577fb2345811bc731c201375b9afaf6b1e` |

Independent coverage compilation established that active policy-unit subjects
equal requirement subjects, requirement subjects equal attestation subjects,
and attestation subjects equal certificate subjects. Every loaded attestation
has conclusion `complete`. The transition projection is byte-identical to the
rejected candidate and remains outside certification inputs.

## Verification

Independent verification against the accepted tree established:

| Verification surface | Result |
| --- | --- |
| Eight focused Python packages | 585 tests passed |
| Generated A1 freshness | `generate_contract.py --check` passed |
| Contract validation | 32 examples, 8 identity fixtures, 4 operation envelopes, and 141 definitions passed |
| Retained-checker inventory | Fresh; 53 current Bash verifiers |
| Registered declarative suites | 224 selected, 224 passed |
| Complete standards checkpoint | 53 retained Bash checkers passed |
| Scoped Ruff | Passed with cache isolated under `/tmp` |
| Active-plan structure | Passed |
| Candidate diff validation | Passed |
| Post-verification repository state | Exact candidate tree and clean worktree |

The focused package total comprises 12 applicability, 18 metadata, 35 graph
engine, 10 policy-impact, 2 standards-graph, 82 analysis, 46 standards-engine,
and 380 standards-verifier tests. The exact contract-derived matrix,
evidence-rule, strict-optional, omitted-owner, retired-field, and
registered-loader mutations all passed through production Interfaces.

## Decision And Scope

The prerequisite is accepted only for candidate
`7bc8bd070f882eb9779dc678139777d05a6ce7c7`, tree
`35a22f824f7ed5f50347032b956b2108fc073f77`. Standards review and
specification review each found zero findings.

This report does not modify plan lifecycle state, close PIA2-006, resume or
implement standards recovery, authorize broader A1b planning or
implementation, or activate A2. Any subsequent lifecycle transition must bind
this report's own commit and tree and remain a separately authorized change.
