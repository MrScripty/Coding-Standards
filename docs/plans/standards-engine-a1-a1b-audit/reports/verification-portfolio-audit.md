# Standards Engine A1/A1b Verification Portfolio Audit

**Status:** Complete for AUD-A5

**Scope:** Accepted A1 at implementation commit
`2359a98740b6035a0414bfaf5427ceaa1301a1c8`, tree
`97c850ab718287007c1e1daac538f40869f71a1d`; accepted A1b at implementation
commit `84412f22fa9fe082f089eaa347c30c23f185ffee`, tree
`8e0f96a61fcea2398418b17d16a061c20f7463f5`; and the historical reviews and
standards-recovery evidence that explain why their checks exist.

This is a claim-level audit, not a test-count judgment. A large portfolio can
be necessary. A small portfolio can still provide false confidence. Every
recommendation below asks what failure is reachable, what consequence follows,
which oracle decides it, what other proof already exists, and when the check
should end.

## Method And Decision Rule

The audit classifies each mechanism against nine questions:

1. What named product, compatibility, security, durability, or process claim
   does it prove?
2. Can the failing state reach the checked consumer through the real path?
3. What is the consequence, and which scoped threat model makes it material?
4. Is the deciding oracle independent of the subject under test?
5. Does another test, type, smart constructor, static rule, dependency, or
   public Interface already prove the same claim?
6. Would an exception, assertion, trace, or ordinary debugging be sufficient?
7. Is the check permanent, release-bound, migration-only, or diagnostic-only?
8. What execution, maintenance, artifact-churn, and design cost does it add?
9. What exact condition permits consolidation or deletion?

The classification terms are:

- **retain**: a distinct reachable failure has a material consequence and an
  adequate oracle;
- **consolidate**: the claim is justified, but more than one layer proves it;
- **time-box**: the claim is migration or acceptance evidence with a defined
  end;
- **diagnostic-only**: fail-stop behavior plus normal diagnosis is sufficient;
- **product choice**: the verification is necessary only if A1c retains the
  requirement that created it; and
- **unresolved**: the repository evidence does not establish necessity or safe
  deletion.

Repository-owned primary evidence is cited as `COMMIT:path`. Counts below were
reproduced directly from the two immutable trees by parsing the TOML/JSON
registries and Python test definitions. They are diagnostic inventory, never
the reason for a deletion recommendation.

## Executive Conclusion

### Facts

Accepted A1 passed 581 named package tests, 218 declarative suites, 53 retained
Bash checkers, 33 public examples, eight identity fixtures, four operation
envelopes, and generated freshness. Accepted A1b reported 679 broad package
tests, 226 suites, the same 53 Bash checkers, generated freshness, a required-
real interruption test, and a 45-test governed-source/Git matrix on each of
CPython 3.11 and 3.12. The individually reported A1b package counts sum to 677,
not 679; the two-test difference is not explained in the acceptance records.
This does not affect the claim analysis, but it should not be silently
normalized. (`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`;
`580d9c95:docs/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`;
`84412f22:docs/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`)

A1's two local contract implementations passed together while implementing the
wrong Draft 2020-12 Unicode equality. Their agreement was a consistency oracle,
not an external-conformance oracle. The accepted final review also reproduced
the local matrix without finding the semantic error. The later reproduction
used the official Draft clauses to show the failure. This is direct evidence
that more checks do not compensate for the wrong oracle.
(`2359a987:tools/standards_engine/contracts/validate_contracts.py`;
`2359a987:tools/standards_engine/standards_engine/_generated_contract.py`;
`c4408363:docs/plans/standards-engine-standards-recovery/reports/json-schema-instance-equality-reproduction.md`)

A1b corrected the semantic owner by placing Draft validation behind
`jsonschema.Draft202012Validator`. It nevertheless validates some values at
several successive points: facade prevalidation, generated decode validation,
nested generated-model normalization, result construction, and facade output
validation. (`84412f22:tools/standards_engine/standards_engine/tools.py`;
`84412f22:tools/standards_contracts/standards_contracts/runtime.py`;
`84412f22:tools/standards_contracts/standards_contracts/compiler.py`)

The clearest example of verification machinery becoming a design burden is
the governed Python package contract. Its production implementation is 1,419
lines, plus a 262-line declarative-check Adapter and a 713-line unit-test file.
It has 32 unit tests and 17 overlapping declarative defect cases; those 32
tests plus 13 Git-reachability tests form the 45-test matrix run on both Python
versions. Four successive implementation reviews rejected branch binding,
`sys` provenance, assignment-order, Git-environment, or reachability behavior
in this verifier before A1b could be accepted. The admitted profile explicitly
does not defend against adversarial arbitrary Python computation. Its primary
claim is therefore a self-imposed architecture and reproducibility contract,
not an external security boundary.
(`84412f22:tools/standards_verifier/standards_verifier/python_packages.py`;
`84412f22:tools/standards_verifier/standards_verifier/checks/python_package_contract.py`;
`84412f22:tools/standards_verifier/tests/test_python_package_contract.py`;
`84412f22:evaluation/standards-effectiveness/fixtures/contracts/a1b/python-package-imports.toml`;
`580d9c95:docs/plans/standards-engine-a1b/execution-ledger.md`, entries from
“Corrected Implementation Content Review Rejection” through final acceptance)

### Inferences

A1 and A1b both contain checks with distinct protective value. Arbitrary
agent-tool input, persisted bytes, filesystem races, content-addressed
identity, public operation behavior, known semantic regressions, and crash
atomicity are not safely replaced by “debug it later.” Their failures can
cross a real trust Seam or silently damage durable authority.

They also contain verification whose marginal value is much weaker: repeated
validation after an immutable value has already acquired proof, exact duplicate
freshness checks, declarative copies of unit defect matrices, hardcoded copies
of dependency locks, exact hashes for host-only test tools and embedded
temporary scripts, and migration/path-presence assertions without a retirement
date. These are candidates because their named claims overlap or their threat
model is insufficient, not because the portfolio is large.

A1c can materially reduce both code and tests by changing the design before
deleting checks: validate once at each external or durable Seam, make the
result an immutable proof-bearing value, keep direct typed operation
composition, use normal package tooling, and avoid byte-complete global
coverage authority unless exact replay of coverage is an actual product
requirement. A shallow design cannot be made deep merely by pruning tests
afterward.

### Counterevidence And Limits

Python annotations alone do not make wrong internal types impossible here. No
repository type-check gate for these packages was found, and the generated
constructors intentionally accept and normalize runtime mappings. Removing
runtime checks solely because signatures are typed would therefore be
unsupported. The safe proof substitution is an already validated immutable
model or a constructor that makes the invalid state unreachable, not an
annotation by itself.

Independent reviews repeatedly found real A1 and A1b defects. This audit does
not recommend removing content-bound review. It recommends adding an earlier
question to review: whether the contract and its permanent verification
machinery are necessary at all.

The full individual necessity of the 53 historical Bash checkers is outside
this A1/A1b product audit. Their unchanged presence shows that A1b did not add
them; it does not show that all should remain forever.

## Portfolio Inventory And Attribution

| Surface | Accepted A1 | Accepted A1b | Attribution and claim boundary |
| --- | ---: | ---: | --- |
| Named package tests in acceptance records | 581 | 679 broad reported; 677 from the named package rows | Product behavior, component contracts, verifier behavior, and integration are mixed. Counts alone prove no necessity. |
| Declarative suites | 218 | 226 | Only three added suites are A1b-specific: `a1b-authority-reconstruction`, `a1b-contract-conformance`, and `a1b-public-cutover`. Five others came from general standards recovery: authority scope, evidence-oracle boundaries, implementation-versus-dependency, recovery routing, and systemic replanning. |
| Declarative checks parsed from suite TOML | 1,192 | 1,242 | In A1b, 617 are text checks, 245 table checks, and 174 decision checks—1,036 of 1,242. Most of this portfolio proves standards/document consistency, not A1b runtime behavior. |
| Retained Bash checkers | 53 / 5,633 lines | Same 53 / same 5,633 lines | Broad inherited repository migration and standards checks; not growth caused by A1b. |
| Authored public examples | 33 | 13 | Positive public contract corpus; A1b reduced it. |
| Identity fixture corpus | 8 fixtures | 4 encoding cases and 24 identity domains | Exact identity compatibility; distinct from JSON Schema equality. |
| Policy-coverage claim files / claims | 2 / 28 | 10 / 47 | A1b expanded complete policy-unit coverage and later removed generated handles/digests from authored claims. |
| Generated suite-input manifest | absent | 25,938 lines, about 788 KiB; 226 suites, 917 files, 3,672 uses, 13 explicit absences, five repository-index uses | Exact transitive input closure for the global coverage horizon. |
| A1b package-source verifier | absent | 1,419 production lines, 32 unit tests, 17 declarative cases | Exact public-root/import/entrypoint architecture and clean-environment execution. |
| CPython correction matrix | absent | 45 tests on each of 3.11 and 3.12 | The 32 package-contract tests plus 13 Git-reachability tests. |
| Required-real interruption | absent | One capability-selected `strace` test in addition to application-stage interruption | Real SQLite sync interruption on the admitted host profile. |

Sources:
`2359a987:evaluation/standards-effectiveness/suites/`;
`84412f22:evaluation/standards-effectiveness/suites/`;
`2359a987:evaluation/standards-effectiveness/`;
`84412f22:evaluation/standards-effectiveness/generated/suite-inputs.json`;
`84412f22:tools/standards_engine/contracts/examples/a1-examples.json`;
`84412f22:tools/standards_engine/contracts/identity-fixtures.json`.

The inventory establishes cost and provenance. It does not label a test
redundant. The following sections do that only where claims can be compared.

## Public Validation Paths

### Accepted A1

The public agent-tool input path is:

1. `AgentToolFacade` converts arbitrary input to a mapping.
2. The facade runs the 751-line local `validate_contracts.validate` interpreter
   against the requested call definition.
3. The generated `decode_contract` runs a second local schema traversal,
   including `oneOf`, `const`, `enum`, types, patterns, cardinality, and
   `uniqueItems`.
4. Generated dataclass `__post_init__` calls `_coerce_object`, which recursively
   decodes/coerces each selected field again.
5. The native Engine executes with the generated call.
6. The facade serializes the result and runs the local validator again against
   the result-kind definition.

(`2359a987:tools/standards_engine/standards_engine/tools.py`, `AgentToolFacade`;
`2359a987:tools/standards_engine/standards_engine/_generated_contract.py`,
`decode_contract`, `_decode_node`, and `_coerce_object`)

The initial input validation is justified: the agent-tool object is arbitrary
external input. The output contract check is also a legitimate public Seam if
the native Engine does not otherwise promise a sealed generated result.

The second decoder was intended to create typed immutable objects, but it also
became a second incomplete schema interpreter. Both local paths used the same
NFC-normalized canonical identity bytes for equality. The tests
`test_generated_unique_items_matches_canonical_serialization` and
`test_generated_const_and_enum_use_canonical_serialization` explicitly proved
their agreement and thereby preserved the wrong behavior. This is not merely
overlap; it is overlap that amplified false confidence.

**A1 disposition:** retain one validation at the external input Seam and one
public result guarantee; delete both local dialect implementations in favor of
one selected semantic owner. Do not retain a second executable merely to
“cross-check” the first unless it is genuinely independent.

### Accepted A1b

The corresponding A1b input path is:

1. `AgentToolFacade._decode_call` selects the operation contract and converts
   arbitrary arguments to a mapping.
2. `AgentToolFacade._validate` recursively scans every nested mapping/list for
   known handle kinds and classifies a version mismatch as
   `INTERFACE.UNSUPPORTED_VERSION`.
3. The facade calls `CompiledContracts.validate`, which uses the selected Draft
   validator.
4. Generated `decode_contract` calls a separately instantiated
   `ContractRuntime.decode`; `decode` validates the complete value again.
5. `_decode_node` recursively selects union branches and constructs generated
   models. Each generated model's `__post_init__` calls
   `ContractRuntime.normalize_model`, which serializes and validates that model
   and recursively decodes its fields. Nested models therefore acquire proof,
   then participate in validation of their containing models again.
6. Engine result paths commonly use generated `.from_value`, repeating the
   decode/validate/normalize path as the domain-to-public Adapter.
7. `AgentToolFacade._result` serializes the generated result and attempts
   validation against the operation's allowed result definitions until one
   passes. A wrong algebra member becomes an Engine programming error.

(`84412f22:tools/standards_engine/standards_engine/tools.py`;
`84412f22:tools/standards_contracts/standards_contracts/runtime.py`;
`84412f22:tools/standards_contracts/standards_contracts/compiler.py`, generated
model projection; `84412f22:tools/standards_engine/standards_engine/engine.py`,
result `.from_value` paths)

The Draft owner is now correct. The proof lifetime is not. At least the
top-level input is validated twice by the same selected dependency, while
nested generated values are revalidated during construction. On output, a
generated model validated during `.from_value` is serialized and validated
again by the facade.

There is one material counterargument: the facade loads the schema/interface
from the target repository while the generated Python module belongs to the
executing package. The double path detects repository/executable drift. That is
a version-negotiation concern, however, and can be proved once by binding the
target interface version before decode. It does not require revalidating every
nested proof-bearing object.

**A1b disposition:** consolidate, not blindly delete. A1c should validate the
complete arbitrary wire value once, hydrate an immutable generated graph
without repeated schema validation, and trust that graph until it reaches a
new external or durable Seam. A public result should be converted and validated
once at the domain-to-public Adapter, after which serialization should preserve
the proof. The handle-version distinction should be adapted from the deciding
schema error or one shallow version negotiation, not a second recursive walk.

### Internal Contract Validation And Debug Sufficiency

A1b's dynamic `OperationAuthorityContract`, qualified roots, and execution
closures are checked by `validate_execution_authority` at construction and
again when a persisted analysis state is materialized. The focused
`test_c7_analysis.py` matrix creates missing, duplicate, wrong-kind, unknown,
and wrong-side roots for every declared role and cardinality.
(`84412f22:tools/standards_engine/standards_engine/authority.py`;
`84412f22:tools/standards_engine/tests/test_c7_analysis.py`)

Validation after loading persisted cross-object references is justified: local
storage corruption can otherwise create silent, durable semantic errors. The
same exhaustive runtime contract is not inherently necessary for closures
constructed from fixed internal operations. If A1c expresses the four
operations with direct typed fields and constructors, wrong role/kind/cardinality
states can become structurally unreachable; an assertion and trace are then
adequate for a programmer defect. If A1c keeps data-driven operation contracts,
their cross-reference validation and selected negative tests remain justified.
This is a design-dependent proof substitution, not an instruction to delete
the A1b tests in place.

## Claim-Level Portfolio Classification

| Verification family | Named claim and reachable failure | Consequence / threat model | Oracle and overlap | Disposition |
| --- | --- | --- | --- | --- |
| Agent-tool input validation | Arbitrary structured calls satisfy the public request contract before execution. | External arbitrary input can select invalid operations or corrupt interpretation. Security is conditional; correctness is certain. | Selected Draft validator is adequate. A1's second local decoder was non-independent; A1b repeats the same validator. | **Retain one boundary validation; consolidate repeated decode/model validation.** |
| Public output algebra | Every operation returns only an advertised result and valid wire value. | External callers can receive an incompatible result; this is a real compatibility Seam. | Generated result construction plus facade revalidation overlap in A1b. A direct type/algebra membership check plus one Adapter validation is sufficient. | **Retain one domain-to-public proof; consolidate facade revalidation of sealed models.** |
| Draft 2020-12 semantics | `const`, `enum`, `uniqueItems`, composition, pointers, and supported vocabulary follow the selected dialect. | Wrong public acceptance/rejection silently changes contract behavior. | A1's local-local agreement failed. A1b's direct and adapted checks call the same dependency, so they prove Adapter preservation, not library conformance. The dependency is the semantic owner; focused known-regression cases are useful. | **Retain Adapter tests and the A1 Unicode/Boolean regression; rely on the selected dependency for general dialect semantics.** |
| Generated projection semantics | Schema/interface changes affect generated fields, unions, defaults, tools, and results. | Stale or incomplete generated code breaks public compatibility. | Feature-local mutation tests are meaningful; byte freshness only proves synchronization. Engine tests and the declarative contract-projection check repeat exact live-file equality and example validation. | **Retain owner mutation tests and one repository freshness gate; consolidate consumer freshness copies.** |
| Authored examples | Every published example is valid and representative. | Users copy invalid examples; contract documentation drifts. | A1b validates the same 13 examples in Engine tests and the declarative projection check. Examples are positive samples, not exhaustive semantics. | **Retain one repository-level validation; remove duplicate consumer checks; keep a small intentional corpus.** |
| Identity fixtures and hash framing | Codepoint preservation, domain separation, exact framing, ordering, and stable public IDs do not change accidentally. | Handle compatibility, lookup, deduplication, and replay fail. | Exact expected hashes are an independent compatibility oracle when authored from the specified frame. They are distinct from JSON Schema equality. | **Retain.** |
| Navigation/analysis public behavior | Route, read, related, prepare, resolve, inspect, unknowns, lifecycle changes, and cold handles behave end to end. | The product produces wrong work or loses review state. | Public Interface tests are the highest-Leverage behavior evidence. Component tests should not repeat every internal hop. | **Retain representative public paths and known regressions; prefer them over internal implementation assertions.** |
| Snapshot/content capture | Handles bind immutable bytes, symlinks/escapes do not redirect capture, and later source mutation is isolated. | Wrong source is read; captured authority silently changes. Filesystem input can be arbitrary. | Before/after public reads and exact content identity are deciding oracles. | **Retain.** |
| Persisted envelope/cold decode | Stored bytes, kind, schema, handle, dependencies, and codec agree on reopen. | Local corruption can silently alter durable non-derivable decisions. | Validate once at durable decode; repository caching already proves one decode per repository. Rechecking intact values downstream is overlap. | **Retain durable decode/corruption tests; consolidate downstream revalidation.** |
| SQLite crash/recovery | A killed publication is absent or complete; restore never overwrites/races a destination; cold reopen preserves decisions. | Silent data loss or partial durable publication. This is not merely a programmer exception. | Child termination and required-real syscall interruption are stronger than repeated success. Some generic SQLite concurrency properties are dependency guarantees. | **Retain adapter-specific atomicity, restore, and cold-reopen tests if A1c persists state; review generic dependency-behavior cases for substitution.** |
| Store-root platform security | Another principal cannot redirect a trusted configured store through writable parents, aliases, or symlinks. | Cross-principal tampering can alter durable authority. Same-principal malicious processes are explicitly excluded. | Real filesystem ownership/path checks decide the admitted Linux/ext4 profile. | **Retain only if this threat is in A1c's deployment model; otherwise use normal private user-state composition.** |
| Policy impact and empty-impact coverage | A changed policy cannot be declared safe merely because no consumer edge was selected; unknowns remain visible. | False-negative impact analysis can omit required repository changes. | Public empty-impact/unknown tests are meaningful. Exact global byte horizons prove invalidation, not semantic adequacy of coverage. | **Retain no-silent-empty and unknown behavior; treat exact coverage certificates as a product choice.** |
| Generated suite-input closure | Every direct, transitive, absent, and Git-index input to every registered suite is bound into the horizon. | A changed checker input can leave an old coverage proof current. | Exact digests detect change but do not prove the suite still tests the right claim. Git diff/current suite execution already expose many changes. The 788 KiB artifact adds substantial Locality cost. | **Product choice; strong A1c deletion/simplification candidate.** |
| Package/import verifier | Manifests exactly match imports; only roots/exports are used; dynamic bypasses reject; clean entrypoints run. | Mainly architecture Locality and reproducible clean execution. The admitted scanner is non-adversarial. | Clean-install/import/entrypoint execution is a real oracle. The custom AST interpreter duplicates standard tooling and its direct/declarative matrices overlap. | **Retain clean-environment smoke and simple static import ownership; delete the custom capability-provenance interpreter for A1c unless a material threat is demonstrated.** |
| CPython 3.11/3.12 matrix | Supported interpreters import dependencies and execute public entrypoints; AST/Git behavior remains accepted. | A supported target can fail. | Cross-version public/dependency smoke is distinct. Repeating every Git and lexical unit case on both versions has weak marginal independence. | **Retain a small cross-version public/dependency matrix; run the full unit defect matrix once unless version-specific behavior is shown.** |
| Declarative standards suites | Normative text, decision tables, graph relations, and registered consumers stay connected. | Standards become internally inconsistent or incomplete. | Most suites are standards-library evidence, not A1b behavior. Three A1b-specific suites duplicate some package/path checks but also provide integration/migration closure. | **Keep generic policy checks by claim; time-box A1b-specific cutover/path assertions after A1c acceptance.** |
| 53 Bash checkers | Historical standards and migration contracts remain green. | Varies by checker; no one aggregate threat model exists. | Exactly unchanged between A1 and A1b. The checker inventory names inbound consumers, but individual claim/subsumption review is still required. | **Unresolved individually; require a separate lifecycle audit, not count-based deletion.** |
| Independent review | Standards/specification reasoning catches gaps not represented by executable oracles. | Systemic design or evidence defects survive local tests. | Reviews caught real A1/A1b defects; A1 final review still missed the external semantic mismatch. | **Retain; add necessity and marginal-value review, and do it before machinery is built.** |

## Generated Freshness, Examples, And Fixture Overlap

Freshness is valuable but narrow. A1's `validate_contracts.py` checked
freshness, examples, identities, operation envelopes, negative self-checks, and
all definitions; `test_generated_contract_projections_are_current` separately
ran the generator with `--check`. Several generated-model tests then compared
the embedded schema and field sets again. These checks still failed to detect
the Unicode semantic error because they shared the same expectation.
(`2359a987:tools/standards_engine/contracts/validate_contracts.py`;
`2359a987:tools/standards_engine/tests/test_generated_contract.py`)

A1b improves the mutation evidence in the Contracts Module, but exact
repository equality appears at least three times:

- Engine `test_generated_contract_projections_are_current` invokes projection
  `--check`;
- Engine `test_compiler_owns_the_complete_public_definition_closure` renders
  and compares every projection again;
- Engine `test_agent_tools_are_the_exact_compiler_projection` repeats the
  agent-tool subset; and
- the `a1b-contract-conformance` declarative `contract_projection` check
  compiles and compares both generated files and validates the same examples.

(`84412f22:tools/standards_engine/tests/test_generated_contract.py`;
`84412f22:tools/standards_verifier/standards_verifier/checks/contract_projection.py`;
`84412f22:evaluation/standards-effectiveness/suites/a1b-contract-conformance.toml`)

These are named-claim duplicates, not a conclusion from counts. A1c should
retain:

1. owner-local compiler mutation and model-behavior tests;
2. one complete repository freshness check over all generated outputs and
   authored examples; and
3. one public consumer behavior path.

It should not rerun exact byte equality independently in every consumer.

A1b's 13 authored examples are already smaller than A1's 33. They contain many
repeated content-shaped hashes needed only to satisfy handle syntax, while the
24-domain identity corpus separately owns exact identity expectations. A1c can
use stable syntactically valid placeholder IDs in examples and reserve exact
expected hashes for identity fixtures. This reduces churn without generating
the examples from the subject under test; fully generated examples would lose
their value as an authored consumer oracle.

## Policy Coverage And Suite-Input Machinery

### What It Proves

A1 introduced reusable coverage requirements, attestations, and certificates
so an empty impact result could not succeed without current evidence. A1b
expanded the authored claims from 28 across two files to 47 across ten files
and built a transitive input projection. Every registered check declares its
present, absent, transitive, and repository-index inputs; Analysis serializes
those declarations; the coverage horizon incorporates their exact digests.
(`2359a987:tools/standards_analysis/standards_analysis/coverage.py`;
`84412f22:tools/standards_analysis/standards_analysis/suite_inputs.py`;
`84412f22:tools/standards_analysis/standards_analysis/coverage.py`)

This closes a real stale-proof path: a checker implementation or transitive
fixture could change while an older claim remained accepted. Content review
showed that the first central projection omitted transitive and Git-index
authority, and the check-owned replacement fixed that omission.
(`580d9c95:docs/plans/standards-engine-a1b/issues.md`, A1B-027)

### What It Does Not Prove

An exact input digest proves only that bytes changed. It does not prove that the
old or new checker is a valid oracle for the policy claim. Running all current
suites proves current outcomes but still does not prove semantic adequacy.
Coverage remains an authored assertion plus invalidation machinery.

The initial exact-handle design also caused global authored churn: a
representation-only trailing line changed the global horizon and would have
required replacing every authored requirement handle. A1b correctly replaced
authored hashes with stable subject and semantic-contract selectors. The
current generated proof layer still binds the 25,938-line manifest, 917 files,
and the global horizon, so representation changes continue to regenerate and
invalidate proof objects even though the 47 claims no longer need hand edits.
(`580d9c95:docs/plans/standards-engine-a1b/issues.md`, A1B-022;
`84412f22:docs/plans/standards-engine-a1b/reports/a1b-cutover-evidence.md`)

### Evidence-Constrained Disposition

If A1c's product requirement is “never return successful empty impact without
replayable proof of every verification input byte,” the machinery has a named
claim and cannot simply be removed. It should still be isolated as a separate
audit Module because its Interface and lifecycle are much deeper than ordinary
navigation.

If A1c only needs useful change guidance with explicit uncertainty, a much
smaller design is supported by the evidence:

- map policy units to current suite/check IDs;
- run or report the current registered checks;
- treat missing mapping as unknown or broad-review required;
- store a commit/tree locator and outcome report when historical audit is
  wanted; and
- let Git/code review expose byte changes rather than materializing every
  transitive input into a global identity.

The second design preserves the high-value “no silent empty impact” behavior
while deleting most of the byte-horizon machinery. Choosing between them is an
A1c product decision, not a verification decision that the standards should
make implicitly.

## Governed Python Package Contract And CPython Matrix

### Named Claims With Real Value

The A1b package contract proves that:

- each package manifest names its actual direct dependencies and one public
  root;
- imports resolve in a clean environment rather than through ambient source;
- public exports exist; and
- repository entrypoints perform a real typed operation rather than merely
  rendering help.

These have reachable failure paths. The accepted A1 history contained private
imports and public/package drift; a clean install or isolated indexed copy can
fail even when an ambient checkout passes. Clean import and entrypoint smoke on
both supported Python versions are therefore justified.

### Self-Imposed Machinery

The verifier goes much further. It parses Python, tracks lexical binding and
unbinding across functions, classes, comprehensions, assignments, exceptions,
conditionals, loops, and `try`; tracks possible `sys` provenance; recognizes
import machinery and `eval`/`exec`; sanitizes Git fixtures; and rejects dynamic
or reflective access. The profile explicitly avoids claiming to interpret
adversarial arbitrary Python. (`84412f22:tools/standards_verifier/standards_verifier/python_packages.py`;
`84412f22:docs/plans/standards-engine-a1b/execution-ledger.md`, “Corrected
Implementation Content Review Rejection”)

The consequence of an accidental private or dynamic import is generally
architecture drift or a clean-environment failure. It is not silent durable
corruption and, under the declared non-adversarial profile, not an external
attack. Standard import linting, manifest generation, code review, and clean
execution can detect those failures with much less machinery. An internal
engineer deliberately writing obfuscated dynamic import code can also defeat
this bounded scanner; treating the scanner as a security barrier would be
incorrect.

The verification itself duplicates defect families. The TOML fixture contains
17 declarative cases also represented in the 32 direct unit tests. Both are
executed in addition to the full 45-test matrix on each supported interpreter.
One declarative smoke case is useful to prove that the registered check reaches
the implementation. Copying the branch/provenance matrix into both unit and
declarative layers is not.

### A1c Disposition

For A1c:

- keep one manifest/public-root declaration, preferably derived where
  practical;
- use an established static import/lint tool for direct private/star/dynamic
  rules that it can soundly express;
- run clean root-import, export, and real entrypoint smoke;
- run that small smoke on CPython 3.11 and 3.12 if both remain supported; and
- run detailed source-rule unit cases once, not on every runtime, unless a
  version-specific AST or import behavior is identified.

Delete the custom binding/provenance interpreter unless A1c first documents a
material consequence that standard tooling and clean execution cannot detect.
The accepted history is evidence for deletion: a substantial fraction of late
A1b review and repair was spent making the verifier's internal Python model
correct rather than making the four product operations correct.

## Persistence, Interruption, And Corruption

A1b's durable tests are not one undifferentiated excess. They cover different
failure models:

- envelope and repository tests reject malformed bytes, unknown codecs,
  missing dependencies, cycles, handle/key disagreement, and invalid payloads;
- SQLite tests cover immutable insert, collision, cold reopen, backup/restore,
  no-overwrite races, schema version, and concurrent conflict;
- platform tests cover ownership, permissions, symlinks, aliases, mount, and
  ext4 admission; and
- interruption tests kill child processes at application stages and inject a
  signal at the real SQLite sync syscall.

(`84412f22:tools/standards_authority/tests/test_envelope.py`;
`84412f22:tools/standards_authority/tests/test_repository.py`;
`84412f22:tools/standards_authority/tests/test_sqlite_store.py`;
`84412f22:tools/standards_authority/tests/test_platform.py`;
`84412f22:tools/standards_authority/tests/test_interruption.py`)

Persisted bytes and interruption are exactly the cases where “raise an error
and debug it” is insufficient. A process can die without raising to the caller;
corruption can surface much later; partial publication can appear successful.
Tests for atomic absent-or-complete state, cold reconstruction of non-derivable
decisions, corruption rejection, and no-overwrite restore have distinct value.

The threat model is narrower for store-root security. The root is trusted
application configuration and the design excludes a malicious same-principal
process, but includes another principal redirecting a writable ancestor.
(`84412f22:docs/plans/standards-engine-a1b/reports/c7-sqlite-storage-audit.md`,
“Store Root And Threat Model”)
If A1c always creates state beneath an already private OS user-state directory,
some component-by-component ext4 machinery can be replaced by that deployment
guarantee. If it accepts arbitrary configured roots, the checks remain
justified.

Some tests exercise generic SQLite behavior—reader/writer interaction, busy
expiration, page/VACUUM independence—that may be substituted by the library's
guarantee plus a smaller Adapter suite. The repository evidence does not prove
which can be deleted without first fixing A1c's supported durability contract.
The correct sequence is product scope, Adapter contract, then test selection.

## Hash And Digest Purpose Audit

Hashes are not one mechanism with one verdict.

| Hash use | Claim | Threat / consequence | Disposition |
| --- | --- | --- | --- |
| Domain-separated public handle IDs | Exact semantic value has stable content-addressed identity. | Lookup, deduplication, compatibility, and replay. | **Retain exact framing and identity fixtures.** |
| Snapshot entry and Git object hashes | Captured bytes equal the object/manifest being named; corruption or race rejects. | Arbitrary repository input and durable replay. | **Retain, or rely on an equally strong Git/content-store guarantee at one owner.** |
| SQLite backup source/destination digests | A verified restore publishes byte-identical content and detects change during recovery. | Durable corruption or raced publication. | **Retain.** |
| Dependency wheel hashes in `requirements.lock` | Installer selects the reviewed artifacts with no ambient substitution. | Supply-chain integrity and reproducible native target. | **Retain the lock and `--require-hashes`.** |
| Hardcoded `EXPECTED` hash table in `test_dependency_resolution.py` | The lock still equals a second copied list in the test. | Ordinary reviewed dependency update, not an undetectable runtime failure. Pip already enforces the lock. | **Consolidate: test lock structure/installability; do not maintain the same artifact list twice.** |
| Installed dependency license-file hashes | Exact installed license bytes equal the planning record. | Licensing review evidence; not runtime compatibility. | **Record for a release/legal review when exact text matters; do not make permanent runtime tests without a redistribution requirement.** |
| `strace` binary, copyright, and LGPL text hashes | The host-only required-real oracle is byte-identical to one Ubuntu package selection. | Test-oracle provenance; no bundle or external product consumer. The host OS is otherwise trusted. | **Replace with package identity, capability probe, and recorded version unless compromised-host tooling is in the threat model.** |
| Embedded temporary reproduction-script hash | A `/tmp` script matches source fully embedded in a committed report. | No distinct consequence: Git binds the embedded source, and the command is historical. | **Omit in future evidence unless the script is external to the record.** |
| Generated projection byte equality | Checked-in generated output equals owner projection. | Stale code/artifact. | **Retain once at repository freshness.** |
| Suite-input file digests and global horizon | Any suite input byte change invalidates coverage proof. | Stale audit claim, not proof of semantic adequacy. | **Product choice; simplify for A1c unless exact replay is required.** |

Sources:
`84412f22:tools/standards_contracts/requirements.lock`;
`84412f22:tools/standards_contracts/tests/test_dependency_resolution.py`;
`84412f22:tools/standards_authority/tests/test_interruption.py`;
`c4408363:docs/plans/standards-engine-standards-recovery/reports/historical-a1-repair-reproductions.md`;
`84412f22:tools/standards_analysis/standards_analysis/suite_inputs.py`.

The `strace` case is especially revealing. The required-real test hardcodes the
executable hash, package version/architecture, copyright-file hash, and system
LGPL-text hash before probing and injecting the syscall. The exact tool version
helped bind a one-time accepted oracle, but a security-patched byte change with
identical required capability would now skip/fail the test. The test's product
claim is SQLite publication atomicity, not perpetual identity of Ubuntu's
license file. A capability-selected oracle should select on the capability
that makes the result deciding.

## Reviews As Evidence

### Facts

A1 was accepted only after withdrawn/rejected candidates found live-worktree
reads, incomplete generated closure, cold reconstruction gaps, public/domain
leakage, private imports, and weak negative oracles. The final zero-finding
review nevertheless accepted the local JSON equality defect.
(`933c9ab9:docs/plans/standards-engine-navigation-analysis/execution-ledger.md`;
`933c9ab9:docs/plans/standards-engine-navigation-analysis/reports/a1-final-acceptance.md`)

A1b reviews found exact trust-selection, source-independence, restore,
entrypoint, migration, suite-input, dynamic-import, Git-environment,
binding-lifetime, nested provenance, and assignment-order defects. The final
review independently reproduced the last governed-source cases.
(`580d9c95:docs/plans/standards-engine-a1b/execution-ledger.md`;
`580d9c95:docs/plans/standards-engine-a1b/reports/a1b-final-acceptance.md`)

### Inference

Independent review is a high-value oracle for design completeness and systemic
reasoning, but the acceptance question was mostly “does this implementation
satisfy the admitted standards and plan?” Once the plan admitted exact package
closure and a bounded Python source profile, reviewers correctly demanded that
the complex scanner be correct. The process did not force an equally strong
earlier comparison between that machinery and the consequence it prevented.

For A1c, review should happen in this order:

1. necessity and threat model;
2. simpler proof substitutions and dependency guarantees;
3. Interface and change-locality design;
4. implementation correctness; and
5. final portfolio subsumption and lifecycle review.

This preserves the demonstrated value of independent review while reducing
the chance that review effort is consumed perfecting an unnecessary contract.

## Consolidation And Deletion Candidates

These are A1c/general-standard candidates, not edits to accepted A1b.

### High-confidence consolidation

| Candidate | Evidence of overlap | Required replacement proof |
| --- | --- | --- |
| Repeated A1b facade/decode/nested validation | Same selected Draft validator sees the top-level value at facade and generated decode; nested models revalidate during normalization; facade revalidates generated results. | One arbitrary-wire validation, immutable proof-bearing hydration, one domain-to-public validation, and explicit version negotiation. |
| Generated freshness in several Engine/declarative tests | Three Engine assertions and the declarative contract-projection check compare the same generated files; two validate the same examples. | Contracts owner mutation tests plus one complete repository freshness/example gate and one public consumer path. |
| Unit and declarative package defect matrices | 17 TOML cases repeat direct unit families, while both layers run in the broad checkpoint. | Full unit matrix at owner; one or a few declarative registration/integration cases. |
| Hardcoded dependency `EXPECTED` table versus hash lock | Test copies every version/hash already present in the lock. | Parse/validate lock shape, install with `--require-hashes`, verify direct manifest dependencies and imported selected runtime. |
| Full 45 tests on both Python versions | Git behavior and most lexical-unit cases have no demonstrated version-specific difference. | Full unit suite on primary version; clean dependency/public import/entrypoint and any identified version-specific regression on each supported version. |

### High-confidence time-box or removal after replacement

| Candidate | Reason | Removal condition |
| --- | --- | --- |
| `a1b-public-cutover` retired-A1 path assertions and migration TSV | Proves the one-time v10-to-v11 replacement and absence of superseded files. | A1c is accepted, no supported upgrade starts from the deleted A1 paths, and history retains the accepted evidence. |
| A1b-specific path-presence portions of authority/contract suites | They prove implementation shape more than enduring public behavior. | A1c generic behavior/contract suites cover the surviving claim and A1b becomes historical. |
| Exact host `strace`/license hashes in the runtime test | They bind incidental test-tool bytes beyond the capability needed for the oracle. | Capability/version/package provenance is recorded and the test proves the real sync interruption; or A1c uses a deterministic owned interruption hook. |
| Hash of a fully embedded temporary reproduction script | Committed source and command already bind the historical evidence. | Source is embedded or checked in and invocation is recorded. |

### Strong A1c design-deletion candidates

| Candidate | Why design deletion is preferable to test pruning | Product decision needed |
| --- | --- | --- |
| Custom 1,419-line Python binding/provenance verifier | Its own semantic model caused repeated late defects; clean execution and standard static tooling cover the material non-adversarial consequence. | Whether private/dynamic import is merely architecture discipline or an actual security boundary. |
| Data-driven execution role/cardinality algebra | It requires runtime cross-object validation and exhaustive negative matrices for four fixed operations. | Whether third parties extend operation contracts dynamically. No such consumer is recorded for A1/A1b. |
| Byte-complete global suite-input horizon | Large generated artifact and broad invalidation prove byte change, not semantic coverage. | Whether A1c promises exact historical replay of coverage proofs or only current impact guidance with explicit uncertainty. |
| Full immutable authority repository for every public child | Persistence and corruption tests are justified only because every child is a durable replayable object. | Which state is truly non-derivable and must survive a cold process. Persist only that state. |

### Unresolved; do not delete from this audit alone

- the individual 53 Bash checkers;
- exact license-text identity where a future bundled release or legal process
  requires it;
- SQLite concurrency/profile cases until A1c fixes its durability promise;
- cross-version cases with demonstrated interpreter/AST/native-wheel
  differences; and
- policy coverage certificates if exact replay remains an external product
  requirement.

## A1c Verification Shape

An evidence-constrained minimal A1c portfolio would be:

1. **Public Interface:** representative end-to-end tests for `query`, `prepare`,
   `resolve`, and `inspect`, including unknown/unavailable outcomes and one cold
   continuation if cold continuation remains a requirement.
2. **External input:** one selected Draft validator at agent-tool input, known
   A1 Unicode/Boolean regressions, strict-JSON adaptation, and stable diagnostic
   mapping.
3. **Proof lifetime:** immutable validated wire models; no revalidation until a
   new external or durable Seam.
4. **Generation:** owner-local compiler mutation tests and one repository
   freshness/example check.
5. **Identity:** the v2 encoding/domain fixture matrix and a small number of
   public handle compatibility cases.
6. **Persistence, only if required:** durable decode, corruption, atomic
   absent-or-complete publication, cold reopen of non-derivable decisions, and
   no-overwrite restore. Rely on SQLite for generic database semantics unless
   the Adapter changes them.
7. **Packages:** ordinary static import ownership plus clean public-root and
   real entrypoint smoke on supported runtimes; no custom partial Python
   interpreter.
8. **Impact:** public tests that unknowns stay visible and empty impact cannot
   silently claim certainty. Add exact coverage replay only if admitted as a
   separate product capability.
9. **Review:** one early necessity/threat review and one final content-bound
   Standards/specification review, with a portfolio subsumption table.
10. **Lifecycle:** migration and historical-shape checks carry an explicit
    deletion trigger.

This retains evidence at the high-Leverage Interfaces while removing checks
whose only role is to police machinery that A1c need not contain.

## General Standards Changes Supported By This Audit

The standards-evolution report determines whether existing guidance is absent,
ambiguous, or misapplied. This report supplies the verification evidence for
the following general, repository-agnostic changes.

### 1. Add a permanent-check admission record

Require every new permanent test, validator, hash assertion, verifier, or
generated freshness gate to record:

- the named claim;
- a reachable producer-to-consumer failure;
- consequence and scoped threat model;
- deciding oracle and its independence;
- proof substitutions considered;
- overlap/subsumption with current evidence;
- execution and maintenance cost; and
- lifecycle/removal trigger.

**Reason:** current rules decide whether evidence can prove a claim, but not
whether the claim warrants permanent machinery.

**Supporting evidence:** A1's two local validators coherently proved the wrong
semantic expectation; A1b's AST checker became 1,419 lines with repeated repair
rounds for a non-adversarial architecture rule.

### 2. Classify failure boundaries before requiring validation

Use four general classes:

1. arbitrary/adversarial external input;
2. expected recoverable operational failure;
3. trusted-internal programmer defect with immediate contained failure; and
4. corruption capable of silent durable, security, safety, or irreversible
   harm.

Require strong validation for classes 1 and 4 and as needed for class 2.
Permit assertion/exception/trace plus focused regression evidence for class 3
when no distinct harmful state can escape.

**Reason:** treating all invariants alike spreads boundary machinery into
trusted internal paths.

**Supporting evidence:** agent-tool and durable SQLite checks have distinct
consequences; repeated validation of already immutable generated models and
wrong internal result-algebra cases are ordinarily programmer defects.

### 3. Make proof lifetime operational

State that once an immutable value has passed the owning boundary proof, later
Modules must not revalidate the same claim unless they cross a new trust Seam,
decode durable bytes, detect a material version transition, or add a genuinely
different invariant.

**Reason:** “do not revalidate intact proof-bearing values” needs a portfolio
admission consequence.

**Supporting evidence:** A1b's facade, runtime decode, nested normalization,
result construction, and facade output path repeat the same Draft proof.

### 4. Require claim clustering and layer ownership

Before acceptance, group all evidence by claim and select one owning layer.
Unit tests own algorithmic cases; integration tests prove real Seams; public
tests prove behavior. A second layer must name the different failure it
observes rather than copy the same matrix.

**Reason:** unit/declarative/public repetition can look like independent
coverage while sharing implementation and expectations.

**Supporting evidence:** A1b repeats generated freshness/example validation
and 17 package-source defect families across unit and declarative layers.

### 5. Add a hash-admission rule

Permit exact-byte hashes as permanent assertions only when bytes participate in
content identity, supply-chain integrity, persisted reconstruction, publication
integrity, or a specifically recorded legal/release artifact. Otherwise prefer
normal versioning, structural/capability checks, Git review, or no check.

**Reason:** a hash proves literal identity, not that literal identity matters.

**Supporting evidence:** dependency lock, snapshot, and restore hashes have
material claims; a copied lock table, fully embedded temporary-script hash, and
host license-text hashes do not have the same runtime consequence.

### 6. Prefer dependency guarantees and established tooling

Test the project's Adapter and known regressions, not the internals of a mature
selected dependency. Do not build a custom language interpreter or static
analyzer for an internal convention until established tooling is shown
insufficient and the unobserved failure has a material consequence.

**Reason:** custom proof machinery creates another semantic product to design,
test, review, and maintain.

**Supporting evidence:** adopting `jsonschema` removed A1's false local Draft
owner; the custom Python package analyzer then consumed repeated A1b repair
rounds.

### 7. Require evidence lifecycle and retirement

Classify every check as permanent, release-bound, migration-only, temporary
diagnostic, or historical reproduction. Migration/path-absence checks must name
the compatibility horizon or acceptance event that deletes them.

**Reason:** successful cutover evidence otherwise becomes permanent product
machinery after its failure path disappears.

**Supporting evidence:** the unchanged 53 retained migration checkers and
A1b-specific v10 retirement/path assertions have no A1c retirement decision in
their individual definitions.

### 8. Add necessity review before correctness review

Independent design review must ask whether a proposed contract, validator,
version, generated artifact, or verifier should exist before reviewing whether
its implementation is exhaustive.

**Reason:** correctness review appropriately forced the admitted A1b source
scanner to model branch/provenance details, but did not remove the self-imposed
contract.

**Supporting evidence:** late A1b acceptance work centered on making the
governed-source checker correct; A1's final review showed that exhaustive local
agreement can still miss an external semantic owner.

## Facts, Inferences, Counterevidence, And Open Questions

### Facts established by immutable sources

- A1's local validator and generated decoder shared the wrong Unicode equality
  and passed together.
- A1b uses the selected Draft dependency but repeats validation along the
  facade/generated-model path.
- A1b's suite-input artifact binds 917 files and 3,672 check uses into the
  coverage system.
- The 53 Bash checkers and their total source size are unchanged from A1 to
  A1b.
- Only three of A1b's eight added declarative suites are A1b-specific.
- The custom Python package verifier is 1,419 production lines and its final
  semantic corrections were required for A1b acceptance.
- Persisted-state and interruption evidence reaches failure modes that an
  ordinary in-process exception cannot reproduce.

### Inferences supported by those facts

- A1b's repeated proof lifetime and duplicated freshness layers have lower
  marginal value than its external/durable boundary checks.
- The governed-source verifier is disproportionate for its declared
  non-adversarial architecture threat and is a strong A1c design-deletion
  candidate.
- Exact global suite-input identity is a costly product capability, not a
  universal prerequisite for useful impact guidance.
- Standards need a necessity/subsumption/lifecycle gate in addition to their
  current claim-and-oracle rules.

### Counterevidence that constrains deletion

- Python type annotations are not enforced here; only validated immutable
  models or constructors can substitute for runtime checks.
- Review and negative tests repeatedly caught real defects.
- Clean supported-runtime execution catches ambient-import and native-wheel
  failures that unit tests on one interpreter cannot.
- Durable state, external input, and filesystem races have consequences beyond
  developer inconvenience.
- Exact identity and dependency hashes are not equivalent to arbitrary file
  hashes.

### Open questions for A1c admission

1. Which state is genuinely non-derivable and must survive cold process
   restart?
2. Is exact historical replay of policy-coverage proof a consumer requirement,
   or is current guidance with explicit uncertainty sufficient?
3. Does any external or adversarial actor cross the Python package/import Seam?
4. Must A1c support arbitrary configured store roots, or only a private OS
   user-state directory?
5. Are CPython 3.11 and 3.12 both continuing product targets, and which failures
   have actually differed between them?
6. Which of the 53 Bash checks still owns a distinct live claim after A1c, and
   which are migration history?
7. Is public output validation owned by the Engine result constructor or by the
   agent-tool Adapter? It should not be independently owned by both.

Until those questions are decided, this audit supports standards changes and
A1c design constraints, but not deletion of accepted A1b runtime or evidence.
