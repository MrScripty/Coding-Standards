# Review-Evidence Packaging

**Plan status:** `Planned`

**Current phase:** P1 builder implementation started; qualification pending

**Next slice:** **P1 — Build one local, immutable review packet**

**Acceptance status:** `pending`

**Composed-design review:** `applicable`; see [Simplicity and Ownership Review](#simplicity-and-ownership-review).

**Execution ledger:** [execution-ledger.md](execution-ledger.md)

**Issues:** [issues.md](issues.md)

**Admission:** priority **4** in the user's selected **2 → 4 → 3** sequence.
Routing-fact ergonomics is Accepted; the earlier six-slice refactor is closed.
This new plan does not reopen either acceptance. The selected task is planning;
next implementation admission is `start` against this exact repository-relative
plan path after checking the current integrated source. No generator implementation
or new review verdict is supplied by this planning package.

## Implementation scope amendment

The owner directed on 2026-09-28 that a standalone ZIP checker is unnecessary.
P1 implements `build` only. The builder validates its completed staging archive
before no-clobber publication. Recipients inspect the manifest and members with
ordinary ZIP tools. Handoff ZIPs stay outside repository content.

## Objective

Produce one portable, local review packet that gives a reviewer the exact selected
baseline/candidate source, complete change evidence, relevant records and available
verification material, with unambiguous origins and explicit gaps. A reviewer must
not have to infer a baseline from removed diff lines or mistake a cited CI run for
included, inspected CI evidence. Preserve original reports and their limitations.

The tool owns **material selection, byte acquisition, inventory integrity and local
publication**. It does not own standards, claim truth, CI execution, reviewer
judgment, acceptance, provider permissions or remote publication. Bundling those
independent records does not merge their authorities.

## Baseline and deciding evidence

Inspected source: `32e78530096f2884d4c77e0a5a02a0de2ff869fe`, tree
`08759cc18fd2973c105743e050746996fbb67308`, Engine interface 45. The closure is now
on GitHub main. Source artifact `10992151447` from run `36472002507` was verified
against archive SHA-256
`bad4bd4b5de4a227113c1729652a1aad298a4d51591280089ec1c61d25579992`.
The run was in progress at admission: its artifact identifies source, not a passing
candidate test result. Existing routing acceptance and its earlier CI evidence
remain valid at their recorded owners.

The historical external-review packet identified missing baseline files, CI logs,
differential results and cold-process transcripts, and distinguished read-only
recommendations from owner decisions. A later routing review again noted a
size-truncated generated diff. [Design evidence](reports/design-evidence.md)
preserves those motivations without reclassifying any accepted work.

The planning probe reads the real routing implementation through Repository Git:
49 changed paths plus five explicitly selected context paths produce 87 available
baseline/candidate file versions, 4,526,413 uncompressed source bytes and a complete
1,083,975-byte primary patch. It also demonstrates that `git archive` can omit an
`export-ignore` file while exact object reading preserves it. These are source
selection and feasibility observations, not tests of an implemented packet builder.

## Objective Acceptance

| ID | Observable criterion | Kind | Environment | Mode | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| P-A1 | One explicit versioned request describes exact local revisions, selected context/records, evidence origins and caller-supplied claim associations; malformed or contradictory selections cannot become a packet. | contract | supported locked runtime | automated | pending | Closed request fixtures and failure oracles |
| P-A2 | The packet includes every primary changed file version that exists, full primary diff and selected context with exact bytes/modes/identities; baseline, candidate, CI subject and record revisions remain distinct. | integration | real local Git repositories | automated | pending | Independent Git/literal oracles, moves/deletions and drift cases |
| P-A3 | Included, referenced and missing evidence are distinguished; captured bytes and caller-reported provenance do not become authenticated CI results, exhaustive claim coverage or acceptance decisions. | contract + negative | local imported evidence | automated | pending | Exact status/provenance fixtures and contradictory inputs |
| P-A4 | Build is local and non-mutating toward source/index/refs/configuration/evidence; it follows no source symlinks, executes no source/evidence commands and contacts no network/provider. | system + security | supported Linux and real subprocesses | automated | pending | Dirty-tree preservation, hostile Git configuration, unsafe-file and network-negative tests |
| P-A5 | Publication is bounded, no-clobber and complete; the builder validates its staged inventory before publication. | release-artifact | real filesystem and ZIP files | automated | pending | Publication race, limits, malformed staging and inventory checks |
| P-A6 | A real routing-fact review example is navigable offline with both source versions, complete generated files and available later records; unavailable raw evidence stays explicit. | user-workflow | separately opened local packet | either | pending | Recipient inspection of the new output, not prior review relabeled |
| P-A7 | Existing Git/Engine contracts and accepted records are preserved; new package and existing affected selections, lock-qualified CI, generated freshness and structural checks pass. | integration | current Python 3.12 hash-locked CI | automated | pending | Exact candidate checks and preservation diff |
| P-A8 | Independent material review and owner disposition establish bounded ownership, useful evidence and supported cutover; only this new slice is accepted. | review | independent reviewer and owner | manual | pending | Source review, issue dispositions and final ledger |

All packet status fields concern material availability or byte consistency. They
are not projections of plan acceptance statuses. A reviewer inspecting the packet
may make a recommendation; only the authorized acceptance owner acts on it.

## Scope and constraints

### In scope

A repository-local Python CLI with a `build` command; a small packet-owned
request/manifest schema; exact committed-source selection; local, explicitly named
external evidence; one ZIP output and reader index; deterministic inventories and
file hashes; tests and operational guidance. Reuse the current supported dependency
lock and Repository Git for subprocesses and exact reads. Preserve interface 45.

### Out of scope

No new MCP tool, server mode, Engine/store schema, review service, registry, daemon,
provider integration, GitHub API fetch, test runner, scorer, acceptance automation,
secret scanner or redactor. No source fixes, change staging, commits, refs, history
rewrites, clone/worktree creation, test execution or archive extraction during build.
No implicit crawling of links, directories, Git history, untracked files, submodules
or arbitrary dependency graphs. No new general plan parser. No bulk packaging of
all repository files or all prior review artifacts by default.

Broader regression hardening is priority 3 and remains deferred. This feature still
includes its own deciding tests. The packet is not a retroactive prerequisite to
routing acceptance or to this tool's independent review.

## Binding Decisions

### D1 — Explicit inputs, not discovery of unstated scope

Use one schema-version-1 JSON request. Require the full local object IDs of
`baseline` and `candidate`, a descriptive repository label, the governing plan
path at a named revision, and a bounded review question. Optional named additional
revisions identify CI subjects or later records. Accept only full SHA-1/SHA-256
object IDs supported by Repository Git; do not resolve moving branches, infer a
merge base, select latest CI, or fetch absent objects. The repository label is
caller-supplied provenance, not an authenticated identity.

Automatically select the entire primary `baseline → candidate` changed-path set;
there is no ignore/filter flag for hiding part of that change. Add literal,
explicitly named context files and record files, each tied to its own revision.
Treat renames as exact delete/add unless the existing owner supplies a different
explicit representation. No recursive link walk or arbitrary glob selector is
needed. Emit an absence record where a changed path exists on only one side.
The selected context is not claimed to be a complete consumer graph.

The request may list claim IDs, their governing plan artifact and evidence IDs.
These are **operator-supplied associations**. Include the exact plan as the actual
claim source; do not duplicate its criteria/status as authoritative new fields or
parse Markdown prose to grant a verdict. Reject unknown evidence IDs, duplicate
request identities and inconsistent revision aliases. A missing declared claim
association is visibly unassociated, not satisfied. The recipient checks whether
the operator's claim selection is complete; a packet generator cannot infer that
from available bytes.

### D2 — Git remains the source owner

Obtain regular-file bytes through `GitRepository.read_session` with exact
`RepositoryRevision` and `RepositoryPath` values. Reuse existing object framing,
hash/type checks, bounds and lifetime handling. Working-tree edits, staged values,
ignored ZIPs, later commits and filesystem timestamps are not source authority.
Include Git mode, blob identity and packet SHA-256 per copied file; write packet
members as inert data, not executable or symlink filesystem objects.

Use the established bounded `git_output`/`git_command` owner for fixed read-only
metadata/diff commands. Any missing exact revision/tree-entry metadata or diff
capability is added narrowly at **Repository Git's public read-only boundary**,
with direct tests; do not import private parsers or implement a second raw Git
object decoder in the packager. No change to current write/publication APIs or
existing capture defaults is admitted. [Consumer inventory](reports/source-consumers.md)
identifies current interfaces and extension limits.

The new packet read path must disable replacement-object interpretation, external
diff drivers, textconv, rename heuristics and lazy fetching; use explicit
commit-to-commit arguments and stable raw/NUL path output. Do not run `git archive`
as the byte oracle because export attributes may omit or rewrite blobs. Never
fall back to checkout bytes, shallow diffs, text-only excerpts or permission guesses.
Pin patch attribute lookup to the candidate commit so dirty worktree attributes
cannot change the representation of the selected committed patch.

Implementation must prove that its selected Git invocation cannot invoke a
promisor remote or external helper. If the installed Git/adapter cannot provide
that local-only guarantee for a repository, reject that repository configuration
as unsupported before object reads. A narrowly explicit local-only observation
method is preferable to changing all Engine subprocess behavior. Repository Git
retains its current per-command bounds; add no elapsed-time expiry for the overall
review task or automatic retry.

V1 supports regular committed files and exact binary bytes under the existing
path-encoding contract. A selected symlink, gitlink, unsupported path or unavailable
source object returns an explicit failure before publication; do not follow it,
auto-fetch it, or mark a missing primary source file merely advisory. Empty primary
diffs may be described explicitly; they are not fabricated source changes.

### D3 — Distinct revision roles and narrowly proved equivalence

The primary patch compares the two selected endpoints, not an inferred merge base.
The source candidate, evidence's declared subject, and later record revision can
legitimately differ. Include each selected commit/tree identity. For additional
revisions produce a complete changed-path/mode/object-ID comparison against the
candidate; do not silently recast a later snapshot as earlier source.

An explicitly selected literal subtree or path set may have an equality comparison
computed from Git. Label exactly that scope and list changes outside it. Matching
`tools/` does not prove identical manifests, CI configuration, test discovery inputs,
or complete test applicability. Identical source does not prove tests executed.
Required test/acceptance coverage remains the owner’s decision.

Supplemental comparisons are metadata inventories, not automatic content capture
of every changed file. Copy only explicitly selected record/evidence files from
those revisions. This prevents a CI housekeeping commit that removes an unrelated
ZIP from causing that ZIP's binary body to enter the review packet. The full primary
diff and all of its changed source bytes are still complete.

### D4 — Evidence origin and availability are separate from its meaning

Evidence items have stable request IDs, a role (for navigation only), a declared
subject revision when known, and exactly one origin:

- `git-file`: an exact path at one named revision; normally used for a plan,
  review, live record, verification narrative or committed result.
- `local-file`: one literal relative path below an explicitly supplied evidence
  root; normally used for a previously retrieved CI log or delivery artifact.
- `reference`: a descriptive label and optional source URL with no included bytes.

No origin executes commands or follows URLs. Local roots and paths are explicit;
no search of `/tmp`, home directories, credentials, repository configuration or
neighboring evidence occurs. An archive supplied as a local file stays opaque;
request already-extracted log files explicitly when a reviewer needs their contents.
Directory or archive-member ingestion and provider downloaders are not part of V1.

Record physical availability as `included`, `referenced`, or `missing`. A selected
external item missing at its declared location is a gap, not a fabricated result.
For included files calculate the hash of the exact bytes written. An optional
caller-supplied expected hash is checked before inclusion; mismatch, changing reads,
unsafe paths or contradictory IDs produce a failed build, not substituted bytes.
Lack of an expected hash is allowed but labelled **recorded**, not externally verified.

Store imported files verbatim and preserve their cited limitations and original
verdicts. CI run IDs, URLs, subject declarations and reported conclusions are not
queried or authenticated by this offline tool. V1 does not scrape arbitrary test
logs or parse provider-specific status documents to declare CI successful. The raw
record and its declared association remain inspectable. A claim supported only by
a link is not labelled as having included or verified evidence.

A later acceptance decision may be included as an unchanged record. The generator
never changes or adopts it. Evidence imported from another repository/subject must
remain explicitly labelled and cannot inherit the primary candidate identity.

### D5 — One packet inventory, not an evidence/acceptance registry

The output is one version-1 ZIP with a generated `INDEX.md`, an inventory manifest,
complete primary patch, primary baseline/candidate files, selected record versions,
local evidence bytes and supplemental comparison inventories. See
[packet contract](reports/packet-contract.md) for the proposed layout and example.
The index provides direct local links and honest counts so a shell-disabled reader
can locate both source versions, including large generated files, without relying
on diff windows. Original documents are never rewritten merely to repair their
historical links; the generated index gives portable access to included targets.

Sort generated inventories by exact role/path and use one fixed JSON serialization
with finite numbers, deterministic key order and UTF-8. Retain original file bytes
and explicitly authored claim order. Use stable ZIP member order and metadata;
wall-clock packaging time and temporary filenames do not enter inventory identity.
The same request bytes, selected material and implementation/environment produce
the same manifest; do not promise byte-identical compression across different ZIP
implementations. Package integrity never depends on a temporary local path.

The manifest owns only this assembly: input-selection digest, implementation
provenance, exact revision roles, members, hashes/modes/sizes, origin observations,
claimed evidence associations and material gaps. It does not become canonical for
claims, CI semantics, reviews, acceptance state, timestamps or the repository graph.
Unrelated source versions remain independently replaceable; changing an included
record changes this packet, not the authority or status of the original record.

Before publication, the builder checks its completed ZIP without extraction for
path uniqueness, exact member set, sizes and SHA-256 values. The manifest does not
hash itself. The build result returns its digest. Self-consistency is not
provenance authentication or proof of semantic correctness. No signature system
or new identity codec is added.

### D6 — Bounds, filesystem ownership and no silent truncation

Reuse the current 64 MiB object bound for Git objects and adopt a named per-member
64 MiB bound. Initial packet-specific bounds are 256 MiB total uncompressed bytes,
4,096 file members and 1 MiB request JSON, including metadata. The real planning
sample uses about 4.53 MB of source plus a 1.08 MB patch; these bounds leave room for
explicit verification logs while preventing accidental unlimited exports. Keep the
bounds with the packet owner, validate them during build and staging, and test edges using
small injected limits. No unexplained hardcoded truncation or unlimited setting.

Copy complete records or fail with a bounded limit outcome. A source/diff/required
plan overflow prevents a packet, rather than a successful package missing its
largest files. Explicit reference-only evidence is permitted and always disclosed.
`INDEX.md` may be concise; raw source and evidence never become summaries.

Choose a new final ZIP outside the source repository and evidence root, with a
validated existing local output parent. Refuse an existing output, source/evidence
path overlap, symlink traversal, invalid ZIP member names, duplicate/case-colliding
portable output paths, or nonregular local inputs. Record unsupported encodings and
modes, not lossy normalized paths. Escape untrusted names and text in the generated
index; evidence content is untrusted data, never executable instructions to the tool.
No claim of automatic secret detection or upload approval is made.

Use a private same-directory temporary file with exclusive creation and restrictive
permissions. Close all readers, finish the archive and perform inventory validation
before no-replace publication. For the supported Linux filesystem, an exclusive
hard-link publication from the completed staging file is a possible existing OS
primitive; use a tested equivalent if needed, never check-then-replacing rename.
Keep only owned temporary paths eligible for cleanup. Interrupted staging is not a
published packet; do not sweep other tasks' temporary files. If publication succeeds
but owned cleanup fails, report the published artifact plus cleanup observation,
not a false absent-artifact failure. No repository lock or state store is required.

The documented CLI runs with bytecode writes disabled (`python -B`); source/evidence
filesystem preservation tests include index, refs, config, dirty/ignored files and
in-process interpreter side effects. No full repository copy, reviewed-payload imports, hooks,
filters, network calls, tests, acceptance mutations or agent runs occur during build.

### D7 — Observable results and implementation footprint

The command is `build --repo-root ... --request ... --evidence-root ...
--output ...zip`. The evidence root is
required only for selected local inputs; it is not inferred from the request's
location. Command names/flags are provisional until implementation admission.

Build reports `built` (all declared material physically included) or
`built-with-gaps` (one or more evidence items referenced/missing). Both name the
published file and inventory digest. Neither means reviewed or Accepted. Exit 0
means intact material with no declared gaps; exit 1 means an intact packet with
explicit gaps; exit 2 means invalid, unavailable, unsupported or failed construction
and no newly published final artifact. Staging validation failures return 2 before publication. Unexpected
failures receive a safe bounded diagnostic and preserve owned-state semantics.

Use a small `tools/review_evidence` Python package, following the current package
manifest/import conventions, with a thin CLI and cohesive request/material/index
operations. The format schema and ordinary validation belong to that package;
reuse the already pinned jsonschema dependency instead of implementing a schema
language. The Git adapter owns any necessary new exact-read metadata methods.
Do not insert packet logic into Engine runtime, repository-verifier checks,
applicability, identity or publication workflows. No Engine edition bump is needed.

Integrate the new package selection and its tests into current locked CI and the
existing package-contract inventory. No new CI system, runtime matrix, dependency
version, generic plugin interface or mandatory packet gate on every change is added.
Normal independent review can use the existing manual process to review this tool;
it must not require the tool to have already accepted itself.

## Simplicity And Ownership Review

**Applicability:** `applicable`

The artifact packages independently owned source, evidence, review and decision
records across a filesystem boundary.

- Independent concepts and dimensions: Git owns exact source objects; origin readers acquire
   explicit local bytes; packet assembly owns selection, bounded inventory and
   publication; plans/CI/reviews/acceptance remain separate authorities. Adding
   another document does not create a new evidence policy.
- State, identity, value, time, policy, and mechanism: commit/tree IDs identify
   source, SHA-256 records included bytes, request IDs join the inventory. Local
   acquisition is an observation, not continuous disk auditing or attestation.
   Timestamps and narrative status do not establish CI scope or approval.
- Caller and composition-root knowledge: name two commits, the plan, context and
   available evidence. The caller does not reconstruct baseline bodies, duplicate
   file hashes, handle unsafe archive names or combine partial results by hand.
   It still owns which claims/consumers need review and any external disclosure.
- Representative change paths and forced owners: a new artifact changes the request, not a
   validator registry; a different source candidate changes bound IDs and derived
   comparisons; a CI provider changes imported records, not a network adapter;
   a new packet format requires versioned builder/manifest coordination only.
- Stable Interfaces versus hidden knowledge: exact object paths, revision roles,
   availability and declared associations are explicit. Filename recency, branch
   names, historical prose, neighboring files or embedded URLs supply no authority.
   The component does not infer complete consumer or claim coverage.
- Independent evolution, testing, failure, and replacement: Git availability can fail before
   publication; a missing external artifact yields a labelled gap; import digest
   contradiction fails. Packet checks are reproducible without a repository, but
   cannot authenticate origin or rerun external evidence. CI/reviewer/owner decisions
   are independently usable without this tool.
- Deletion and cumulative machinery result: deleting the package would push precise two-version copying,
   evidence association, no-clobber publication and integrity handling back into
   every review preparation script. A new provider registry or generic plan parser
   would disappear without losing this objective, so neither is admitted. Staged
   validation prevents an incomplete or malformed builder output from being
   published; recipients retain the inventory for their own inspection.
- Necessary complexity and containment: source and record versions differ; some evidence is
   unavailable; filesystem/archive inputs can be unsafe. Keep these few concerns in
   one bounded package over the existing Git adapter. No new service, mutable
   registry, Engine tool, automated review gate or permanent content store is needed.

**Authority scope:** the request/manifest are canonical only for the one selected
assembly and its byte checks. Removing a CI record or acceptance report leaves the
rest's meaning unchanged. A copy's hash links data; it never transfers authority
from its producer. This satisfies the current Architecture authority-scope admission.

## Milestones

### P1 — Local packet construction and staged integrity validation

**Status:** `In progress`

**Goal:** implement D1–D7, as amended above, as one coherent vertical path over existing Git reads.

**Write set:** `tools/review_evidence/{README.md,pyproject.toml,review_evidence/,tests/}`;
limited read-only metadata/diff/local-only additions and tests in
`tools/repository_git/{repository_git/{repository.py,model.py,__init__.py},tests/,README.md}`
only if required by the chosen public adapter boundary; the existing package fixture
`evaluation/standards-effectiveness/fixtures/contracts/a1c/python-package-imports.toml`;
`.github/workflows/purpose-separated-engine.yml` for one additional package test
selection; the existing generated verification-input manifest; link-only pointers
in `docs/plans/README.md` and `.agents/skills/standards-engine/references/environment.md`;
and this plan's current records. Do not write previous accepted plans/reports.

**Work:** confirm source and boundaries, implement closed request/manifest and the build
command, reuse exact Git read ownership, add deterministic real-Git/file/archive
negative tests, update consumers and CI selection, and generate owned derived inputs.
Do not create sample CI conclusions when no evidence file exists.

**Gate:** P-A1–P-A5 and the affected code checks in P-A7. Exact-content tests use
literal expectations and independent Git observations. Prove no directory/index/ref
or network side effects under the actual documented entry point. No scope repair
may silently change evidence or acceptance meaning.

### P2 — Offline recipient example and acceptance

**Status:** `Planned`; depends on P1.

**Goal:** demonstrate a useful, independently navigable review artifact and close
this new plan through normal verification and review.

**Write set:** P1's source only for demonstrated blockers; test fixtures and user
guide; this plan's evidence/dispositions and generated verification inputs. Any
selected CI evidence acquisition is an explicit read performed outside the builder,
not permission to add network fetching to it.

**Work:** use the routing-fact source range and separately bound CI/record revisions;
assemble exact selected source and available evidence; represent missing raw logs
without borrowing conclusions from reports. Open the finished packet in a separate
read-only recipient context and locate both source versions, a full generated file,
the plan/claim links, actual evidence artifacts and gaps without needing shell or
external links. Inspect a gap-containing copy.
Preserve the observation without reopening the already accepted routing change.

**Gate:** P-A6, exact supported CI in P-A7, independent P-A8 and all remaining claims
satisfied. Record time/call/material counts only where actually observed; do not
promise fewer model tokens or faster engineering from a planning size comparison.
After this plan's acceptance, admit priority 3 separately.

## Evidence and verification plan

Independent tests cover full-ID pinning while refs/worktree change; modified,
added/deleted/renamed/mode-changed/binary/large files; `export-ignore` and
`export-subst`; complete generated bytes rather than a diff-only view; missing
source objects; no source symlink/gitlink following; local-only Git under hostile
external/textconv/promisor configuration; and full primary scope despite unrelated
working-tree files. Existing Repository Git object verification is reused rather
than replicated in packet tests.

Use exact member sets and independently computed digest/mode expectations. Inject
malformed staging archives with duplicate or traversal names and incomplete member
inventories. A changed manifest with no trusted external digest can be
self-consistent; document that limit instead of calling the format authenticated.
Exercise output-exists races, write/read failures, cleanup and positive/negative
budget boundaries.

For evidence, test included Git records and external files, explicit references,
missing files, unknown associations, wrong expected hashes, unsafe roots, changed
files, unsupported record format and foreign declared subjects. Generated prose
must never contain invented verdicts, test counts or claim satisfaction. Record a
CI URL as referenced when only that URL exists, even when a narrative says it passed.

The representative real example must show candidate/CI/record commit differences
and compute the exact selected scope equality without overstating CI applicability.
Preserve raw narratives and later acceptance files as separate records. All these
checks concern the new packet, not requalification of prior accepted production.

## Blockers

No source-design blocker is currently demonstrated. A local-only metadata/diff
adapter and atomic filesystem publication must be qualified in implementation;
they are not assumed tested by this plan. The actual operator's uncommitted
output-contract edits are not accessible and are not a source input. Raw historical
CI/delivery logs may be unavailable; that is an explicit first-example material gap,
not a reason to invent them or to reopen acceptance.

## Re-Plan Triggers

Re-plan if a real consumer requires mutable worktree capture, remote fetching,
archive-member discovery, multiple repositories/submodules, signed attestation,
provider-specific interpretation, automatic claim scoring, acceptance transitions,
a new persistent store, or global Git behavior changes. Re-plan if existing exact
read ownership cannot remain local/bounded or the artifact cannot be published
without overwriting unrelated work. A newly found direct integration file within
the same invariant is added to the write set, not an automatic wider redesign.

## Final Acceptance

This plan is `Planned`. Source inspection, ordinary planning probes and plan-schema
validation do not qualify an unimplemented builder or recipient workflow.
Preserve original failures and successful candidate evidence at their exact source
identities. Use current Python 3.12 hash-locked CI; do not change the matrix or claim
3.11 observations without running them. Independent review remains separate from
self-checking the archive. After normal acceptance, priority **3 — targeted test
strengthening** is next; no other improvement is admitted here.

- Acceptance status: `pending`
- Final status: `Planned`
