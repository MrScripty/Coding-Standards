# Python Verification Engine Standards And Design Audit

- **Status:** Historical investigation evidence; superseded as planning input
- **Date:** 2026-08-21
- **Scope:** `tools/standards_verifier`, `tools/graph_engine`, the Standards
  Router, canonical module metadata, registered verification suites, and the
  active Bash-to-Python verification migration
- **Initial observed revision:** `157e211ad237d59ecf470d7914b2cff086a4c4c3`
- **Revalidated revision:** `08190314808665cfe8ab10a0284d90274ac6f021`
- **Working-tree note:** Concurrent Rust-async migration work observed during
  the initial audit was subsequently accepted at the revalidated revision. It
  was not part of this audit's write set.

## Lifecycle Notice

This report remains the pinned historical evidence for the engine and
standards-system findings observed at the revisions above. Its proposed
milestones, acceptance matrix, and first planning decision are no longer
current work instructions. They were superseded as planning input by the
accepted [Python Verification Engine Design Recovery plan](../../python-verification-engine-recovery/plan.md).

The recovery plan's [current issue dispositions](../../python-verification-engine-recovery/issues.md)
record SW-01 through SW-04 and PE-01 through PE-04 and PE-07 as resolved,
PE-06 as resolved without an implementation change, and PE-05 as controlled
until its accepted zero-Bash trigger. The observations, counts, and conclusions
below are intentionally preserved against their recorded revisions rather than
rewritten to describe the current repository.

## Purpose

This report originally gave developers plan-ready evidence for improving the
Python verification engine and the standards system around it. It separates:

1. engine implementation that conflicts with existing standards;
2. weaknesses in standards routing, graph coverage, and enforcement;
3. performance concerns that require an owned measurement contract before an
   optimization is selected; and
4. migration-only code that needs an explicit terminal disposition.

This report does not authorize implementation, choose a final design, or change
the active verification-engine plan's current slice.

## Subsequent Scope Limitation: Verification Oracles

This audit assessed engine topology, authority boundaries, loading, result
classification, and migration lifecycle. It did not assess whether each
configured assertion is an independent and fit oracle for the claim attributed
to it. In particular, it did not evaluate source bytes versus consumer-visible
rendering, whether copied explanatory prose proves semantic accuracy, or
whether coordinated edits to a subject and its expected literal preserve
meaning.

The later M6-I71 `rust-binding-callback-task` `documentation-projection`
failure demonstrates the distinction: the suite's
[`text` assertion](../../../../../evaluation/standards-effectiveness/suites/rust-binding-callback-task.toml)
rejects the wrapped source in the
[`README`](../../../../../evaluation/standards-effectiveness/verification-guide.md) even though
the rendered sentence is unchanged. Oracle fitness and explanatory projection
checks are therefore deferred to the separately proposed
[Plan B evidence-oracle recovery](standards-engine-navigation-analysis-authoring-brief.md#plan-b-evidence-oracle-recovery).
Nothing in this report's positive assessment of generic declarative mechanics
should be read as accepting every configured literal as valid semantic
evidence.

## Historical Executive Conclusion

The written Core and Architecture standards are not the primary cause of the
engine's design problems. They already require one canonical owner, dependencies
toward stable contracts, policy-independent mechanics, deletion of unowned
migration paths, and abstractions justified by demonstrated variation. Most
engine findings are missed applications of those rules.

The standards system nevertheless has material weaknesses:

- task routing is expressed in prose but is not comprehensively verified for
  engine-interface, architecture, migration, and performance scenarios;
- the repository graph's canonical-module coverage is derived from
  `metadata_graph` checks, so verification-suite selection determines which
  standards modules and `Requires` edges are queryable;
- 14 of 44 Core, Router, workflow, topic, and profile modules are absent as
  logical graph nodes, including `topic.performance`;
- the migration's speed objective is not represented by an owned performance
  claim, workload, baseline, metric, or acceptance budget; and
- shared-engine capability acceptance emphasizes parity and typed negative
  evidence but does not require an explicit Architecture applicability
  assessment when a semantic interface expands.

The primary corrective direction proposed at the time was therefore:

1. make routing and graph coverage complete enough to expose the applicable
   standards reliably;
2. re-establish a small engine interface containing repository-neutral
   verification mechanics;
3. keep policy and migration lifecycle in suites and their canonical evidence;
4. use one validated registry/catalog authority throughout an invocation;
5. define performance claims before changing loading, scanning, or caching; and
6. give every migration-only Python module an explicit zero-Bash disposition.

## Audit Guardrails

The audit applies the repository's own rules and a deep-module design test:

- A module is evaluated by the leverage of its interface and the locality it
  provides, not its raw line count.
- One call site does not by itself invalidate a module, and many call sites do
  not by themselves justify one.
- A useful seam lets callers ignore a coherent concern. A seam that exposes the
  same policy concepts as its implementation is shallow.
- Under the deletion test, deleting a useful module causes its owned complexity
  to reappear in callers. If deletion removes the complexity entirely, the
  module was probably carrying unnecessary policy or migration machinery.

These guardrails agree with [Core's simplicity and ownership rules](../../../../../CORE-STANDARDS.md#simplicity-and-ownership),
which explicitly reject file-length, type-count, dependency-count, and call-site
count as design authorities.

## Standards Alignment

### Existing standards that correctly diagnose the engine

| Existing rule | Audit consequence |
| --- | --- |
| One canonical owner; no second source of truth | A check must not independently reparse and reinterpret the suite registry. |
| Policy remains outside verification mechanics | Engine code must not contain migration states, canonical policy prose, topic identities, or source-specific exceptions. |
| Additional structure needs an owned invariant or demonstrated variants | A one-consumer check kind needs semantic justification beyond Bash parity. |
| Configuration exists only where the owner permits variation | Fixed claim modes and canonical policy domains must not be exposed as redundant settings. |
| Delete paths with no current owner or supported contract | Migration-only inventory, graph, retirement, and checkpoint machinery needs a terminal disposition. |
| Select Architecture when module authority or dependency direction changes | A new check kind or shared engine contract needs an explicit Architecture applicability assessment; select Architecture only when the Router's module, authority, dependency-direction, composition, or state-ownership facts are present. |
| Select Performance for a speed, resource-use, or regression claim | “Much faster” requires a named workload, baseline, metric, environment, and accepted comparison. |

Canonical evidence:

- [Core: Simplicity And Ownership](../../../../../CORE-STANDARDS.md#simplicity-and-ownership)
- [Core: Code And Terminology Discipline](../../../../../CORE-STANDARDS.md#code-and-terminology-discipline)
- [Core: Semantic Constants And Configuration](../../../../../CORE-STANDARDS.md#semantic-constants-and-configuration)
- [Architecture](../../../../../topics/architecture.md)
- [Performance](../../../../../topics/performance.md)
- [Verification-engine ownership and extension rules](architecture.md#ownership-boundary)

### Standards-system weaknesses

#### SW-01 — General routing decisions are not comprehensively executable

- **Severity:** High
- **Owner:** Router and routing verification
**Evidence:** The Router correctly selects Architecture for module, authority,
dependency-direction, and composition changes, and Performance for performance
claims. The registered [`s1-routing` suite](../../../../../evaluation/standards-effectiveness/suites/s1-routing.toml)
proves one bounded Rust-library example, metadata closure for that example, and
selected Router prose. The audit found no general task-to-module fixture covering
these verification-engine cases:

- adding a new shared check kind;
- adding an independently parsed source of authority;
- changing focused-suite loading or failure isolation;
- claiming the Python migration is faster;
- retiring migration-only Python infrastructure; or
- changing repository graph composition.

**Impact:** A migration slice can satisfy parity, mutation, and typed-diagnostic
checks without proving Architecture or Performance applicability or selecting
those topics when their conditions are present. Passing verification can
therefore coexist with a missed or over-broad routing decision.

**Required planning outcome:** Add fact-driven routing cases for these semantic
change shapes. Require an explicit Architecture applicability assessment, not
automatic Architecture selection. Do not add an unconditional
`workflow.implementation -> topic.architecture` or `workflow.implementation ->
topic.performance` edge; those topics remain conditionally selected from
observable task facts.

**Acceptance evidence:**

- positive cases select the exact applicable modules and their transitive
  `Requires` closure;
- negative cases prove that a local implementation change without architecture
  or performance facts does not select those topics;
- unknown authority, workload, or ownership facts produce an unresolved routing
  result rather than a convenient default; and
- one case covers a new verifier check kind that changes a module seam and
  therefore selects Architecture;
- one case covers a bounded check inside an unchanged module and does not select
  Architecture; and
- one case covers a measured speed objective.

#### SW-02 — Canonical-module graph coverage depends on verification suites

- **Severity:** High
- **Owner:** Repository graph composition and canonical-module corpus membership
**Evidence:** [`repository_graph._metadata_modules`](../../../../../tools/standards_verifier/standards_verifier/repository_graph.py)
loads module metadata only from paths present in registered `MetadataGraphCheck`
instances. A standards module can therefore be canonical, routed, and verified
as text while remaining absent from the graph. For example, the
[`performance-owner-contract` suite](../../../../../evaluation/standards-effectiveness/suites/performance-owner-contract.toml)
checks `topics/performance.md` as text but does not register its metadata.

At the revalidated revision:

- the selected canonical corpus contains 44 Core, Router, workflow, topic, and
  profile modules;
- 30 are registered as logical graph nodes;
- 14 are absent; and
- `python3 tools/query_edges.py --node topic.performance` returns
  `GRAPH.UNKNOWN_NODE`.

The values 44, 30, and 14 are generated observations of that revision, not
acceptance constants.

This is an inverted dependency: verification-suite topology determines the
visibility of canonical standards metadata. It also means the graph cannot be
treated as a complete route or module-dependency catalog.

**Required planning outcome:** Decide and document one of two explicit graph
contracts:

1. **Complete canonical-module graph:** introduce one canonical corpus-membership
   or provider-registration source independent of validation suites. That source
   owns only which canonical documents participate. Module IDs, canonical-owner
   path aliases, `Requires`, and `Specializes` relations remain authoritative in
   each document's metadata and are derived when the provider loads the corpus;
   or
2. **Partial registered-edge graph:** retain partial coverage but make the
   interface and diagnostics explicit that it cannot answer module existence,
   routing, or complete dependency questions.

The complete contract is recommended because the current graph already exposes
metadata `Requires` edges and logical module aliases, which invites complete
dependency queries.

**Acceptance evidence for the recommended contract:**

- every canonical module in the owned corpus has exactly one logical node and
  one repository-path alias;
- every declared `Requires` item has exactly one outgoing metadata edge;
- removed or duplicate module IDs and unresolved requirements fail with typed
  diagnostics;
- graph population is independent of which semantic enforcement suites happen
  to use `metadata_graph`; and
- no manifest or provider copies module IDs, canonical-owner aliases,
  `Requires`, or `Specializes` values from module metadata;
- Router selection remains separate from graph dependency closure.

#### SW-03 — The migration has no owned performance acceptance claim

- **Severity:** Medium
- **Owner:** Verification-engine plan with Performance and Verification
**Evidence:** The active plan's A1–A6 acceptance claims cover deterministic
execution, diagnostics, contract representation, Bash replacement, zero Bash,
and removal of the temporary reference model. They do not define a speed,
latency, memory, startup, or resource-use criterion. The phrase “much faster”
therefore has no authoritative workload or pass/fail meaning.

**Impact:** Eager loading and repeated scans can be observed, but the project
cannot determine whether an optimization is necessary or prove that a proposed
optimization improves the intended consumer workflow.

**Required planning outcome:** Define at least these separate workloads before
optimizing:

- list registered suites;
- run one focused suite and its dependency closure;
- run all declarative suites;
- validate generated migration artifacts; and
- run the complete checkpoint while retained Bash checkers exist.

For each selected claim, record metric, representative repository state, runtime
and build configuration, environment, baseline, variability policy, comparison
or budget, and consumer impact. Local single-sample timings in this report are
diagnostic observations only.

#### SW-04 — Shared capability acceptance lacks a recurring Architecture applicability gate

- **Severity:** Medium
- **Owner:** Verification-engine migration governance
**Evidence:** The architecture report says to compose existing primitives and
make custom Python the last option. The active plan permits a new reusable
primitive only for multiple coherent owners or one otherwise inexpressible
safety-critical invariant. That rule is narrower than Core: one caller may
justify a module when it owns a coherent invariant, removes substantial repeated
reasoning, or lets the caller ignore an owned concern. Consumer count does not
decide. Separately, the `source_index_closure` capability was accepted as
“bounded” from its configured paths, derived values, and strong negative
evidence without recording an Architecture applicability assessment or
demonstrating why existing table, Markdown, relation, and text mechanics could
not express the policy.

**Impact:** Strong behavior verification protects an increasingly broad
implementation rather than protecting the intended engine seam.

**Required planning outcome:** Make an explicit Architecture applicability
assessment mandatory when a slice adds or materially expands any of the
following:

- a check kind exposed in suite configuration;
- a parser or independently loaded authority source;
- a long-lived runtime owner;
- a migration-specific engine module;
- check context or registry interface fields; or
- a performance-sensitive loading or scheduling path.

These are assessment triggers, not automatic Architecture selection. Select
Architecture only when the assessment finds a module, authority,
dependency-direction, runtime-composition, or state-ownership change. Evaluate a
module from the invariant it owns, the concern callers can ignore, and the
reasoning it removes. The trigger and decision do not depend on a file, line,
class, consumer, or check-kind count.

## Missing Canonical Graph Nodes And `Requires` Edges

The following module nodes and all their declared outgoing `Requires` edges are
absent from the current metadata dependency graph:

| Missing logical node | Canonical path | Declared `Requires` targets whose outgoing edges are absent |
| --- | --- | --- |
| `workflow.build` | `workflows/build.md` | `core`, `workflow.implementation`, `workflow.verification` |
| `topic.cross-platform` | `topics/cross-platform.md` | `core`, `workflow.verification` |
| `topic.diagnostics` | `topics/diagnostics.md` | `core`, `workflow.verification`, `topic.contracts` |
| `topic.licensing` | `topics/licensing.md` | `core`, `workflow.verification` |
| `topic.performance` | `topics/performance.md` | `core`, `workflow.verification` |
| `profile.application.launcher` | `profiles/applications/launcher.md` | `core`, `workflow.verification`, `topic.resilience` |
| `profile.boundary.ipc` | `profiles/boundaries/ipc.md` | `core`, `workflow.verification`, `topic.contracts`, `topic.security` |
| `profile.boundary.language-bindings` | `profiles/boundaries/language-bindings.md` | `core`, `workflow.verification`, `topic.contracts`, `profile.boundary.interop` |
| `profile.framework.godot` | `profiles/frameworks/godot.md` | `core`, `workflow.verification`, `topic.concurrency` |
| `profile.language.csharp.async` | `profiles/languages/csharp/async.md` | `core`, `workflow.verification`, `topic.concurrency` |
| `profile.language.rust.cross-platform` | `profiles/languages/rust/cross-platform.md` | `core`, `workflow.verification`, `topic.cross-platform`, `profile.language.rust` |
| `profile.language.rust.language-bindings` | `profiles/languages/rust/language-bindings.md` | `core`, `workflow.verification`, `profile.language.rust`, `profile.boundary.language-bindings` |
| `profile.language.rust.security` | `profiles/languages/rust/security.md` | `core`, `workflow.verification`, `topic.security`, `profile.language.rust` |
| `profile.language.rust.unsafe` | `profiles/languages/rust/unsafe.md` | `core`, `workflow.verification`, `profile.language.rust` |

This table does not propose conditional Router edges. It records only nodes,
path aliases, and unconditional dependencies already declared in canonical
module metadata.

## Python Engine Findings

### PE-01 — `source_index_closure` embeds policy and migration topology

- **Severity:** High
- **Owner:** Verification-engine check interface and migration-source-closure policy

**Historical evidence:**
`tools/standards_verifier/standards_verifier/checks/source_index_closure.py` at
pinned revision `08190314808665cfe8ab10a0284d90274ac6f021` contains the evidence
below. Reproduce it without recreating the deleted path with:

```text
git show 08190314808665cfe8ab10a0284d90274ac6f021:tools/standards_verifier/standards_verifier/checks/source_index_closure.py
```

Its accepted replacement and deletion evidence is recorded in the
[Milestone 3 interface disposition](../../python-verification-engine-recovery/reports/milestone-3-interface-disposition.md#source-index-closure).

The historical implementation contains:

- exact migration manifest, corpus, owner-map, and disposition schemas;
- allowed migration states such as `concise`, `expanded`, `retain-index`, and
  `rewrite-index`;
- required and prohibited legacy-authority prose;
- Router-specific absence rules;
- exact owner-map/disposition lineage semantics; and
- one fixed four-file fixture topology.

The implementation is 786 lines, but line count is not the finding. The finding
is that callers must understand a wide policy interface and the engine owns
facts that its architecture assigns to standards, suites, and fixtures. The
check has one registered consumer while generic text, table, decision, Markdown,
and relation checks account for most current verification.

**Impact:** Policy changes require engine edits; the module is shallow relative
to its interface; source-index migration history becomes a permanent engine
concept; and strong custom tests make later simplification more expensive.

**Required planning outcome:** Replace the policy-specific check with a suite
composition over existing generic mechanics. If one missing reusable mechanic
is proven, give it a repository-neutral input/output contract and justify it by
the coherent invariant it owns, the concern callers can safely ignore, or the
substantial repeated reasoning it removes. Consumer count does not decide.

**Acceptance evidence:**

- no migration state, Router rule, canonical prose, owner-map column name,
  disposition column name, or source-index fixture filename remains in engine
  implementation;
- the source-index suite still proves ordered headings, routes, line budgets,
  prohibited text, canonical membership, and Router exclusion;
- existing positive and negative mutations retain their typed outcomes;
- tests exercise the generic interface rather than private source-index
  implementation details; and
- obsolete custom code and its tests are deleted rather than layered under a
  compatibility adapter.

### PE-02 — `edge_dispositions` creates a second registry authority

- **Severity:** High
- **Owner:** Suite registry/configuration module
**Evidence:** The verifier strictly loads and validates the suite registry in
[`config.py`](../../../../../tools/standards_verifier/standards_verifier/config.py).
`edge_dispositions.py` (historical path: `tools/standards_verifier/standards_verifier/checks/edge_dispositions.py`)
then opens the configured registry again with `tomllib`, silently skips malformed
non-dictionary entries, accepts partial entries, and builds its own path and
dependency maps.

**Impact:** One invocation can have two interpretations of registry authority.
The weaker parser can accept or ignore states that the canonical loader rejects,
and future registry schema changes must be implemented twice.

**Required planning outcome:** Load and validate the registry exactly once. Pass
the resulting immutable catalog through the existing check context or another
internal engine seam. The check consumes suite identities, paths, checks, and
dependencies from that catalog and never opens registry or suite TOML itself.

**Acceptance evidence:**

- registry and suite TOML are parsed by one canonical loader;
- malformed, duplicate, unknown, or missing entries have identical diagnostics
  regardless of which selected check consumes the catalog;
- assertion replacement lookup uses already validated suite/check identities;
- focused and complete execution observe the same catalog revision; and
- tests prove there is no fallback raw-TOML parser.

### PE-03 — Focused selection eagerly loads every suite body

- **Severity:** Medium
- **Owner:** Verifier loading and selection interface
**Evidence:** [`Verifier.__init__`](../../../../../tools/standards_verifier/standards_verifier/engine.py)
loads every registered suite before `--list`, focused selection, or dependency
closure is known. At the observed revision this means 207 suite files and 1,052
checks are constructed even for a one-suite request. Text, table, and decision
checks represent 906 checks, or 86.1% of the registered check population.

**Impact:** Focused execution inherits unrelated suite parse failures and startup
cost. Listing suite IDs performs work unrelated to listing. The module provides
less failure isolation than its focused-run interface implies.

**Required planning outcome:** First decide the intended strictness contract.
The recommended shape is:

1. strictly load the registry catalog;
2. compute the selected dependency closure from registry entries;
3. load only selected suite bodies for focused execution;
4. load all suite bodies for `--all` and `--complete`; and
5. list IDs from the validated registry without loading suite bodies.

**Acceptance evidence:**

- a malformed selected suite fails with the existing typed diagnostic;
- a malformed dependency blocks its dependent;
- an unrelated malformed suite does not block a focused suite or `--list` if
  the recommended contract is accepted;
- `--all` still validates every suite;
- selection order and once-only execution are unchanged; and
- claim-matched startup measurements compare the old and new behavior.

### PE-04 — Assertion failures can return configuration exit status

- **Severity:** Medium
- **Owner:** Diagnostic and result classification
**Evidence:** The documented exit contract assigns status `1` to unsatisfied
assertions and `2` to invalid configuration, usage, or evidence representation.
`SourceIndexClosureCheck._raise_assertion` raises `EngineError` without an
explicit status, while [`EngineError`](../../../../../tools/standards_verifier/standards_verifier/diagnostics.py)
defaults to status `2`. `Verifier._run_suite` preserves that status instead of
normalizing the `ASSERT.*` failure to `1`.

**Impact:** Automation cannot reliably distinguish a policy assertion failure
from invalid configuration. The diagnostic code says assertion while the process
status says representation/configuration.

**Required planning outcome:** Establish one canonical result-classification
mechanism. Checks should return assertion diagnostics through the ordinary
result path; exceptions should represent invalid, unavailable, or unsupported
execution conditions. Do not infer process status from a string prefix alone.

**Acceptance evidence:**

- an unsatisfied source-index heading assertion returns `1`;
- malformed check configuration returns `2`;
- a required missing input returns `3`;
- an unsupported requested capability returns `4`;
- text and JSON report the same semantic classification; and
- every check kind is covered by a shared exit-contract test.

### PE-05 — Zero-Bash closure does not disposition all migration-only Python

- **Severity:** Medium
- **Owner:** Verification-engine plan and terminal migration lifecycle
**Evidence:** Plan acceptance requires zero Bash verification paths and removal
of the temporary Bash reference model. It does not provide a file-by-file or
capability-by-capability terminal disposition for Python modules whose only
consumer is the Bash migration lifecycle. Candidates include inventory,
migration-graph, generated-artifact, numeric-audit, numeric-retirement,
edge-disposition, numeric-lifecycle, and retained-checkpoint behavior.

**Impact:** Removing Bash entrypoints can satisfy the literal acceptance gate
while leaving substantial migration topology as permanent engine implementation.

**Required planning outcome:** Create one canonical terminal-disposition table
for every migration-specific Python module and exposed check kind. Each row must
select `retain`, `replace`, or `delete`, name the post-zero-Bash consumer and
contract, and identify acceptance evidence. Missing consumers cannot default to
retention.

**Acceptance evidence:**

- every migration-only module and check kind has one disposition;
- retained modules name a current non-migration consumer and stable interface;
- replacement rows delete the old implementation in the accepting slice;
- delete rows prove imports, registry uses, documentation, and tests are absent;
- `--complete` has one Python-only meaning without retained-Bash orchestration;
  and
- no frozen migration graph, lifecycle state, or numeric-retirement authority
  remains without a current owner.

### PE-06 — Generated-artifact validation repeats repository scans

- **Severity:** Low until a performance claim is accepted
- **Owner:** Generated-artifact orchestration and Performance
**Evidence:** Inventory collection scans repository shell files; migration graph
collection performs its own shell scan and calls inventory collection; numeric
retirement state calls inventory-backed numeric audit. The generated-artifact
checkpoint invokes these phases sequentially.

**Impact:** The same repository state is rediscovered multiple times, but the
materiality of the cost is not currently established by an authoritative
workload or budget.

**Required planning outcome:** Measure first. If the generated-artifact workload
is materially affected, construct one immutable in-memory repository snapshot at
the narrowest orchestration seam and pass it to inventory, graph, and retirement
logic. Do not add a persistent cache without an explicit invalidation and trust
contract.

**Acceptance evidence:**

- before/after measurements use the same repository state and environment;
- every phase consumes one consistent snapshot;
- output bytes and diagnostics remain unchanged;
- mutation tests prove added, removed, renamed, and changed shell files are
  observed; and
- no required verification is omitted for speed.

### PE-07 — `acceptance_claims` mixes workflow policy with engine mechanics

- **Severity:** Low
- **Owner:** Verification policy representation

**Historical evidence:**
`tools/standards_verifier/standards_verifier/checks/acceptance_claims.py` at
pinned revision `08190314808665cfe8ab10a0284d90274ac6f021` implements the
behavior below. Reproduce it without recreating the deleted path with:

```text
git show 08190314808665cfe8ab10a0284d90274ac6f021:tools/standards_verifier/standards_verifier/checks/acceptance_claims.py
```

Its accepted replacement and deletion evidence is recorded in the
[Milestone 3 interface disposition](../../python-verification-engine-recovery/reports/milestone-3-interface-disposition.md#acceptance-claims).

The historical implementation defines a `kind@environment@mode` grammar,
semicolon set language, special
`either` substitution semantics, canonical table shape, and result comparison.
At the pinned revision it had one registered suite, which is a topology
observation rather than evidence against the module. Its `modes` field is
configurable but is then required to equal exactly `automated`, `manual`, and
`either`.

**Impact:** Workflow.Verification policy is partly encoded in engine behavior,
and an invariant is exposed as configuration. A small policy change can require
Python changes even though suites and fixtures are intended to own selected
policy.

**Required planning outcome:** Apply the deletion and depth tests, then choose
the correct seam based on ownership rather than consumer count:

1. use declarative composition if the existing generic mechanics express the
   invariant without repeated policy reasoning;
2. retain or reshape a repository-neutral module if it owns a coherent set
   invariant behind a small stable interface and removes substantial reasoning
   from its caller; or
3. move the behavior to a Verification-owned policy adapter downstream of the
   generic engine if claim kinds, environments, modes, or substitution semantics
   are the module's essential interface.

**Acceptance evidence:**

- canonical claim kinds, environments, and modes remain owned by Verification
  policy or fixture data;
- invariants are not redundantly configurable;
- the selected placement names its owner, interface, and ignored caller concern
  without using consumer count as authority;
- every existing positive and negative scenario remains covered; and
- removal deletes obsolete parser tests instead of retaining them beneath a new
  adapter.

## Positive Findings To Preserve

The audit recommended that the corrective plan preserve the parts of the design
that were already working:

- `tools/graph_engine` is repository-neutral and exposes a small immutable graph
  interface; policy-specific composition remains downstream.
- Registry and suite configuration are strict at the canonical loader.
- The engine prohibits arbitrary command execution from suite configuration.
- Diagnostics carry stable codes, typed outcomes, suite/check identity, and
  evidence locations.
- Suite dependencies are deterministic and execute at most once.
- Generic `text`, `table`, and `decision` mechanics account for most registered
  checks, showing that broad declarative reuse is achievable.
- The 342 engine unit tests pass in the observed working state.

It recommended deepening these modules rather than replacing them wholesale.

## Historical Recommended Plan Shape

The sequence below is retained as the audit's original planning proposal. It
was subsequently implemented or dispositioned through the accepted
[recovery plan](../../python-verification-engine-recovery/plan.md) and must not
be used as the current milestone sequence.

### Milestone 0 — Stabilize and record the baseline

**Goal:** Start from one reproducible repository revision rather than concurrent
migration state.

**Required outputs:**

- clean or explicitly dispositioned working tree;
- exact revision and explicit disposition of any uncommitted registry state; a
  separate suite-registry digest is required only when registry bytes are
  independently transported or an uncommitted registry is intentionally an
  accepted input;
- passing engine unit tests;
- passing `--all` declarative checkpoint;
- current retained-Bash count and zero-Bash lifecycle state; and
- named performance workloads with baseline measurements where Performance is
  selected.

**Re-plan trigger:** Any ongoing migration changes the registry, engine check
population, retained Bash inventory, or graph module corpus.

### Milestone 1 — Correct routing and graph authority

**Goal:** Make applicable standards and unconditional module dependencies
reliably discoverable before engine restructuring.

**Slices:**

1. decide complete-versus-partial repository graph contract;
2. establish canonical corpus membership or provider registration independent
   of semantic suites, while deriving IDs, aliases, and relations from module
   metadata;
3. close every missing node, alias, and declared `Requires` edge if the complete
   contract is accepted, without encoding observed counts as acceptance
   constants;
4. add general routing fixtures for engine interface, architecture, migration,
   and performance cases; and
5. document that Router selection and graph dependency closure are distinct.

**Gate:** Every canonical module query resolves, exact dependency closure is
verified, and conditional route cases neither omit nor over-select topics.

### Milestone 2 — Restore single configuration authority and exit semantics

**Goal:** Remove contradictory authority before deeper restructuring.

**Slices:**

1. expose one immutable validated suite catalog to checks;
2. remove raw registry and suite reparsing from `edge_dispositions`;
3. centralize assertion versus configuration/result classification; and
4. add cross-check-kind exit-contract evidence.

**Gate:** One registry parse, no fallback parser, and exact statuses `0` through
`4` match the documented interface.

### Milestone 3 — Remove policy-specific engine interfaces

**Goal:** Recompose source-index and acceptance-claim verification through the
smallest stable generic interface.

**Slices:**

1. map every `source_index_closure` responsibility to an existing primitive;
2. prove any genuinely missing repository-neutral mechanic before adding it;
3. migrate the source-index suite while retaining mutation parity;
4. delete the custom source-index check and implementation;
5. apply the deletion test to `acceptance_claims`; and
6. remove redundant invariant configuration.

**Gate:** The implementations replacing `source_index_closure` and
`acceptance_claims` contain no source-index, Router-policy, migration-state, or
canonical Verification-domain literals except generic diagnostic vocabulary.
Other migration checks remain governed by their current lifecycle until
Milestone 5.

### Milestone 4 — Improve focused loading and measured performance

**Goal:** Improve fault isolation and performance only against accepted claims.

**Slices:**

1. separate registry catalog loading from suite-body loading;
2. load focused dependency closures lazily under the accepted strictness
   contract;
3. measure list, focused, all-suite, generated-artifact, and complete workloads;
4. consolidate repository scanning only if measurements justify it; and
5. retain before/after regression evidence with representative variability.

**Gate:** Correctness and diagnostics are unchanged, selected performance claims
are satisfied, and no cache or lifecycle complexity is added without evidence.

### Milestone 5 — Enforce zero-Bash terminal deletion

**Goal:** Prevent migration topology from becoming permanent product
architecture.

**Slices:**

1. inventory every migration-only Python module and check kind;
2. approve one retain/replace/delete disposition per item;
3. delete temporary graph, inventory, retirement, and retained-checkpoint paths
   as their consumers disappear;
4. remove obsolete tests and documentation through the same interface slices;
   and
5. verify the Python-only command and repository graph from final-state sources.

**Gate:** Zero Bash, zero undispositioned migration-only Python, no compatibility
adapter, one current owner for every retained module, and no owner-specific
standards or migration-only policy anywhere in engine implementation.

## Historical Objective Acceptance Matrix

This matrix records the proposed acceptance criteria that informed the recovery
plan. Current acceptance state is owned by the recovery plan and its issue
dispositions.

| ID | Observable criterion | Evidence kind |
| --- | --- | --- |
| R1 | Engine-interface and performance task fixtures select the exact Router modules and `Requires` closure. | focused routing decisions |
| G1 | Every canonical module ID and path alias resolves and every declared `Requires` edge is present exactly once. | metadata/graph contract |
| E1 | Registry and suite configuration have one validated in-memory authority per invocation. | focused and integration |
| E2 | The implementations replacing `source_index_closure` and `acceptance_claims` contain no source-index, Router, migration-state, or canonical Verification-domain policy. | source inspection plus negative fixture |
| E3 | Assertions return `1`; invalid representation/configuration returns `2`; unavailable returns `3`; unsupported returns `4`. | cross-check-kind contract |
| E4 | Focused and list operations do not load unrelated suite bodies under the accepted loading contract. | focused fault-isolation tests |
| P1 | Named performance workloads meet their accepted budget or comparison in the required environment. | performance measurement |
| Z1 | Every migration-only Python module has an accepted retain/replace/delete disposition. | lifecycle table closure |
| Z2 | Final Python-only verification contains no retained Bash orchestration or temporary migration graph. | complete final-state checkpoint |
| Z3 | No engine check implementation contains owner-specific standards or migration-only policy. | terminal source inspection plus lifecycle closure |

## Historical Explicit Non-Goals

The proposed recovery plan was not to:

- impose line-count, file-count, class-count, check-kind-count, or call-site-count
  thresholds;
- rewrite the repository-neutral graph engine merely because downstream graph
  composition is incomplete;
- add unconditional Architecture or Performance dependency edges to every
  implementation task;
- preserve old custom checks under wrappers, aliases, or compatibility adapters;
- invent a generalized expression language merely to replace one specialized
  verifier check;
- add persistent caching before a performance claim and invalidation contract
  exist;
- weaken strict configuration or typed diagnostics for faster startup; or
- mix unrelated migration packages into the remediation write set.

The expression-language non-goal above is limited to the contemplated
replacement of a specialized verifier check. It does not decide or prohibit
A1's independently justified, bounded three-valued applicability language,
which has a different analysis contract and requires its own accepted design.

## Observed Transient State

The repository changed during report preparation. At one recorded diagnostic
run against the initial observed revision plus an in-progress Rust-async checker
migration, the transient result was:

- `python3 -m unittest discover -s tools/standards_verifier/tests`:
  **342 tests passed** in 2.283 seconds;
- `python3 tools/standards_verifier/verify.py --all`:
  **207 selected, 204 passed, 3 failed**;
- the three failures concern the in-progress `rust-async-boundary` migration,
  stale executable-edge disposition evidence, and row-35 references to the
  removed checker; and
- these failures are not evidence for the engine design findings above.

The migration was subsequently accepted as M6-I60. Revalidation at clean
revision `08190314808665cfe8ab10a0284d90274ac6f021` established the then-current
snapshot:

- `python3 -m unittest discover -s tools/standards_verifier/tests`:
  **342 tests passed**;
- `python3 tools/standards_verifier/verify.py --all`:
  **207 selected, 207 passed, 0 failed**; and
- the derived inventory reports **65 retained Bash checkers**.

The proposed Milestone 0 required a stable revision and rerun of the gates
before accepting a remediation baseline or performance comparison.

## Historical Suggested First Planning Decision

The decision proposed below was taken by the accepted recovery plan: corpus
membership is path-only authority, while module IDs, aliases, roles,
`Requires`, and other relations are derived from canonical document metadata.
It is retained here to show how the audit evidence led to that decision, not as
an outstanding planning action.

Before editing engine code, the audit proposed deciding whether the repository
graph promised a complete canonical standards-module dependency view or only a
partial registry of explicitly contributed edges. For a complete view, it
proposed selecting one owner for corpus membership or provider registration
only and deriving module IDs, canonical-owner path aliases, and relations from
each canonical document's metadata. That decision would close or explicitly
bound the observed missing-module set without turning 44, 30, or 14 into
acceptance constants, and would give the subsequent engine plan a reliable way
to prove its Architecture and Performance routing without confusing
conditional applicability with unconditional `Requires` edges.
