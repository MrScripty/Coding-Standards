# Boundary repairs from the interface-43 audit

**Plan status:** Verifying
**Acceptance status:** partial
**Canonical plan:** `docs/plans/boundary-repairs/plan.md`
**Operation:** verify (user-authorized boundary repairs)
**Current phase:** Candidate verification
**Next slice:** B1 — Complete locked-runtime verification and independent review
**Base:** `af6b829aae7beba98c7aa523c51c832011587d12`
**Ledger:** [execution-ledger.md](execution-ledger.md)
**Issues:** [issues.md](issues.md)
**Report:** [reports/verification.md](reports/verification.md)

## Objective and bounded scope

Make the same declared boundary mean the same thing at every affected entry point:
logical graph resolution does not observe the live filesystem; Engine store selection
preserves final-component admission; schema-typed integral numbers become Python
integers before domain use; Analysis evidence digests obey the existing lowercase
SHA-256 representation. Add the six missing existing direct package suites to CI.

Keep operation shapes, identity domains, valid stored records, evidence verification,
authoring decisions, native-only input, output delivery, and publication unchanged.
Interface 44 records the corrected Digest scalar constraint: maxLength 71 excludes a
trailing newline that the former pattern alone admitted. Generated contracts follow
that canonical declaration; request/state/handle/store versions remain unchanged. Performance caches, garbage collection,
integrity-check policy, routing APIs and the rest of the audit are outside B1.

## Standards and admission

Core and the executable Router selected 28 modules with zero unresolved facts.
The retained route/readback covers implementation, verification, planning,
proportionality, documentation, build/tooling, release/commit; library,
generated-contract/IPC/persistence; contracts, architecture, security, diagnostics,
cross-platform; code design, replay, schema/protocol/evolution and independent oracles.
This is code maintenance, not normative standards authoring. Source is an isolated
clone; no user files, production stores, external configuration or remote refs change.

## Binding decisions and systemic population

- Graph owns resolution authority. Handle logical mode before any filesystem lookup,
  preserving registered aliases and existing logical path errors. Keep filesystem
  mode's containment and unconnected-artifact behavior.
- Snapshot store owns final-component regular-file/no-symlink admission. Engine may
  resolve a relative parent against the current working directory, including permitted
  intermediate symlinks, but passes the final name without resolving it. This preserves
  the existing relative-path convenience; direct SnapshotModule still requires an
  absolute Path. This is not race-free filesystem sandboxing.
- ContractRuntime owns schema-directed Python representation after canonical validation.
  Normalize only positions constrained to integer, including referenced/union and
  container positions. Preserve number-only/unconstrained and opaque literal data,
  schema documents, defaults, omissions,
  arbitrary-size integers, caller inputs, and strict rejection of booleans/non-finite
  numbers. Anonymous structured properties use their declared schemas as named ones do.
- Analysis owns its EvidenceReference invariant without importing generated transport
  code. Use the existing lowercase SHA-256 grammar and prove parity with generated and
  authoring representations through shared conformance cases in an integration test.
  Each boundary retains its existing typed failure; byte and provider checks stay live.
- Interface edition 44 records a tightened public Digest declaration. The independent
  validator remains the maxLength semantics owner; the compiler admits that supported
  keyword and preserves it in every projection. No persisted-format, request/state or
  handle version changes. Current-process replacement and catalog refresh remain explicit.

The systemic families are logical-vs-physical resolution, store-path composition,
integer conversion through every supported structural location, and digest syntax
across the three existing evidence representations. Stop discovery after these owners
and reachable consumers have regression dispositions. Additional co-owned files may
be recorded; new authority, persistence or support changes require re-planning.

## Simplicity and ownership review

**Applicability:** applicable, because boundary composition is corrected.
1. Graph resolves names, SnapshotStore admits files, Contracts maps validated values,
   Analysis admits evidence references, and CI invokes existing tests.
2. Immutable graph/material and value validation remain separate from filesystem
   state and live evidence. No caching or lifecycle policy changes.
3. Callers no longer need to guess which name spelling observes a filesystem, coerce
   revisions individually, or compensate for a higher layer bypassing file admission.
4. A numeric representation repair lives in decoding and its consumers' regressions;
   a path policy remains with storage plus one composition site; digest conformance
   is tested across existing independent boundaries.
5. Stable values/contracts cross boundaries; no new cross-package runtime dependency.
6. Each repair has direct negative and positive tests plus its consuming path. Failure
   meaning and production authority remain at the existing owner.
7. No new production module, registry, validator or adapter. The existing interface
   edition records the corrected scalar promise, not a new versioning mechanism. The redundant
   graph logical check moves out of a spelling-specific branch; no replacement layer.
8. Inherent complexity is declared schema traversal and path/value admission. Tests
   extend the existing framework; CI adds commands rather than a runner abstraction.

## Write set

- `tools/graph_engine/graph_engine/registry.py`, its README and `tests/test_logical_resolution.py`.
- `tools/standards_engine/standards_engine/engine.py`, and
  `tests/test_store_path_boundary.py`, `tests/test_numeric_boundary.py`,
  `tests/test_evidence_digest_boundary.py`.
- `tools/standards_contracts/standards_contracts/runtime.py`, its README and
  `tests/test_integer_decoding.py`.
- `tools/standards_analysis/standards_analysis/trust.py`, its README and
  `tests/test_authority.py` if direct coverage is needed.
- `tools/standards_snapshots/README.md` for existing path-admission scope.
- `.github/workflows/purpose-separated-engine.yml`.
- `tools/standards_contracts/standards_contracts/compiler.py`, and
  `tests/{test_compiler,test_semantics,test_projection}.py` for maxLength admission.
- `tools/standards_engine/contracts/{a1-contract.schema.json,a1-interface.toml,examples/a1-examples.json}`;
  owner-generated `contracts/generated/agent-tools.json`, `standards_engine/_generated_contract.py`.
- `tools/standards_engine/tests/{test_runtime_identity,test_schema_presentation,test_consumer_publication}.py`
  for current-edition expectations; Engine README and
  `.agents/skills/standards-engine/references/environment.md` for current deployment identity.
- This directory and owner-regenerated
  `evaluation/standards-effectiveness/generated/suite-inputs.json`.

## B1 — coordinated repairs and verification

**Lifecycle:** Verifying. Source repairs are implemented. Hold the
candidate fixed for affected package and integration tests; regenerate verification
inputs after staging only intended source files. Review exact diff and negative cases;
package a base-checked patch and complete changed files. No deployed host work is required.

| Claim | Criterion | Kind / environment / mode | Status |
|---|---|---|---|
| A1 | Logical aliases and failures are invariant under bare/path file, directory and symlink changes; filesystem mode still works | focused / representative / automated | satisfied |
| A2 | Direct and composed selected-file admission agree; rejection preserves bytes; relative and intermediate-path behavior is explicit | integration / representative / automated | satisfied |
| A3 | Integer normalization reaches real proposals; generic numeric/literal data and input immutability remain; negatives reject without effects | contract + system / representative / automated | satisfied |
| A4 | Generated, Analysis and authoring digest representations agree; real mismatched bytes still reject | contract / representative / automated | satisfied |
| A5 | CI includes six direct suites; exact commands, affected tests, structural/freshness and reconstruction pass locally | integration + artifact / representative / automated | satisfied |
| A6 | Material review is dispositioned and supported locked-runtime qualification is recorded | contract / representative / either | pending |

## Evidence and completion

Use actual graph/store/Engine entry points and the independent Draft 2020-12 validator.
Use cold stdio to prove numeric request consumption and no-effects failures. Preserve
baseline-created snapshots/readiness in a disposable retained-state comparison when
checking shared decoding; no production publication. A failing baseline test must fail
for its intended reason. Do not count later reruns as earlier passes.

Supported runtime: locked Python 3.11/3.12. This container currently has Python 3.13.5;
a supported-interpreter installation attempt failed because DNS/network access is
unavailable. Continue deterministic implementation and record that limitation; preserve
the dependency lock. Candidate CI and independent review remain acceptance evidence,
not authority to change existing semantics.

Re-plan for changed domain meaning, persisted formats, new client obligations, new
runtime dependencies, or a failing proof that invalidates this composition. Ordinary
regressions remain in B1. Mark Verifying while required external checks remain open;
accept only with all required evidence. The performance and architecture audit stages
remain separate and are not implicitly authorized by this patch.
