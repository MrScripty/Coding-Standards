# Purpose-separated Engine contract

This is implementation and deployment documentation. It describes the Engine
mechanism; it does not classify the real standards as positively written or
ready for application use.

## Host configuration

Engine/facade construction and local transport launch require an explicit
`application` or `authoring` purpose. Purpose remains fixed for that interface.
Tool arguments, detail options and handles select material, not purpose.
Authorization remains the existing independent injected contract. The local
facade is an owner-operated always-allow authorization adapter for admitted
authoring operations; this release does not supply a multi-user access service.

Application operations are `route`, `read`, `read_many`, `related`, `routing_facts`, `query`
and `inspect`. The focused MCP catalog omits native `query`; `--advanced` can
expose it within the same purpose. Authoring retains the complete existing
workflow. Canonical interface operation variants own each purpose's input and
result definitions; MCP and CLI project only their reachable schema closure.

The public application boundary constructs dedicated result values from
qualified domain material. Full detail remains within that boundary. Both
MCP result encodings carry the same value. Unknown/private identities and
malformed requests receive bounded application outcomes. Detailed operational
failures stay in host-private diagnostics, which the host must keep outside an
application agent's independently readable filesystem.

## Accepted authority and snapshots

New snapshots capture the configured local accepted branch, `main`, rather than
the checked-out branch. This prevents an unpublished branch from becoming
application-visible through automatic snapshot capture. Proposal reads use
exact proposal revision authority and are authoring-only.

The two support manifests are mandatory captured inputs:

- `evaluation/standards-effectiveness/application-content.toml`
- `evaluation/standards-effectiveness/decision-provenance.toml`

Both are empty in this code delivery. Existing normative and reference bytes
remain unchanged and authoring-readable after the code candidate is integrated
into accepted `main`. Application reads initially report that the requested
guidance awaits application publication. This is intentional bootstrap behavior,
not an inference that legacy prose was reviewed.

A supported snapshot contains its exact support records, exposure decisions,
Router inputs and material. Reopening uses those captured bytes. Later exposure
withdrawal affects newly captured accepted authority, while a retained historical
snapshot keeps its original decision. This mechanism does not retroactively
erase context or revoke bytes already delivered to an agent.

Old captures lacking the support contract return
`SUPPORT.UNSUPPORTED_CAPTURE` (bounded as `APPLICATION.UNSUPPORTED_CAPTURE` in
application output). Old Analysis records are unsupported under Analysis 7.
Existing SQLite storage mechanics and Snapshot handle version 5 remain in use;
there is no automatic deletion, conversion, alternate old reader or dual write.

## Operation-local performance ownership

Capture owns one bounded exact-revision Git read session for its recorded
first pass, closes that session, and compiles the frozen replay independently.
Both the requested-path closure and semantic signature still have to agree.
The selected accepted-main revision stays fixed throughout that capture.

Analysis preparation and resolution borrow verified immutable inputs for the
current operation. Identical snapshot roles share one material value; distinct
roots keep independent lifecycle and content observations. Focused proposal
creation, revision, analysis and resolution pass one explicit proposal-material
scope through preflight, prospective validation and native analysis. It retains
one verified base and only the most recent exact projection; changing revisions
replaces that projection. Authoring receives its pure preparation dependency
per invocation while retaining ownership of durable roots and conditional writes.

Each material access checks current snapshot lifecycle. Stored revisions, heads,
authorization and pre-/post-submission decisions retain their independent checks.
Changed candidates take the complete compiler path; capture's two passes remain
independent. Scope cleanup releases retained references on success or failure.
The scope contains no provider outcomes or evaluation results. Nested public
re-entry constructs its own scope, and public request shapes remain unchanged.

Each subsequent operation loads and verifies its own captured bytes. Publication
verification, target compare-and-swap and recovery obtain fresh observations;
no operation-local material crosses those barriers as permission or readiness.
Each facade/Engine/SQLite lifetime remains per call. MCP now owns the installed
interface and a bounded cache of pure snapshot compilation as described below.
Operation-local workflow state, evaluations and permissions remain per-call.
Exact draft projection retention is described separately below.

## Process-owned pure reuse

The MCP server compiles its installed API interface once. Discovery and invocation
consume that same contract, and every request still uses the complete generated
decoder and current purpose-qualified result checks. The interface describes the
installed implementation, not the accepted standards revision. Replacing Engine
code or its API schema requires a controlled process restart. Ordinary standards
publication keeps the installed interface valid. Standalone facades prepare their
own interface unless their trusted owner supplies an already prepared one.

One MCP process also owns a repository/purpose-scoped compilation cache with a
two-entry and 32 MiB accounted-retention limit shared by snapshot and draft
projection entries. Snapshot keys contain the exact verified
captured paths, bytes and source revision, plus the installed compiler function.
Python dictionary equality distinguishes hash collisions. Each new operation
opens and validates its store, checks snapshot lifecycle and verifies complete
content identity before lookup. Missing, quarantined, purged, replaced or corrupt
storage therefore remains observable. Equal verified inputs may share pure
compilation even when obtained from distinct store roots; store-specific handles,
access checks and result envelopes remain fresh. No store facts enter the cache.

Successful full compilation is eligible for retention. The cache has no negative
entries, response objects, live authorization/provider outcomes, mutable proposal
heads, readiness or publication outcomes. Snapshot-bound attestations and exposure
declarations remain part of that historical material; they grant no new access.
Eviction, oversized inputs and entries whose retained size cannot be established use the normal verified computation. The accounting
walk charges reachable Python data once per entry, includes captured bytes and
mapping tables, and conservatively charges inter-entry sharing separately. It
materializes pathlib value caches before accounting. Imported implementation
code and bounded LRU bookkeeping are separate from the per-entry budget. The
budget is not a process-RSS or transient-working-memory limit.

Capture always resolves accepted main and runs both independent live/frozen
compiler passes and closure checks. Neither pass consults the cache. A later
explicit read may reuse only a compilation of its own fully verified capture.
Advancing main affects new captures; historical snapshots preserve their captured
material. Publication candidate verification and recovery keep their existing
fresh observations. Each new process starts empty and reconstructs correctly.

The transport retains serial dispatch and opens/closes a fresh facade and SQLite
connection for each call. Pure cached structures are read-only through their
owned interfaces; each response and continuation is newly constructed. The cache
is not a thread-safety guarantee for concurrent use of one Engine. Independent
server processes retain separate fixed-purpose resources. Stream EOF or failure
releases the server-owned interface, catalog and cache; closing a borrowing Engine
closes its store without releasing the owner's cache.

## Exact draft projection reuse

Draft reads, analysis, status, creation/revision preparation and focused resolution
can retain the pure projection of one exact immutable proposal revision. They use
the existing compilation-cache owner and its shared two-entry / 32 MiB budget.
One base plus one current draft fits the measured workload; older entries can be
evicted normally. The runtime adds no persistent cache or new wire format.

Each new public call reads the actual stored revision/root and fully validates its
original captured base before lookup. The key binds exact base bytes/paths, the
existing canonical representation of the complete revision (original snapshot,
repository membership, proposal identity, ordinal and all change sets), and the
installed replay recipe. Static compiler implementations qualify; custom stateful
adapters execute cold. The compiler's original accepted base remains the semantic
comparison authority. On an exact-revision miss, an eligible verified prefix may
supply successor construction as described below. Without one, the entire program
replays with all normal checks.

Retained semantic-intent maps are private copies. Each operation receives fresh
intent maps and result envelopes while sharing read-only sources and compiled
structures. Status and pre-/post-submission evaluations still run. Authorization,
evidence, snapshot lifecycle, proposal-head observations and conditional writes
remain current. A prospective projection retained before a failed publication is
only reusable computation: its handle still requires a real stored revision/root.

Review, candidate verification, application and recovery retain their existing
fresh replay paths. New snapshot capture retains both independent compiler passes.
Main advancement affects new captures, never the base of an existing draft. Old
explicit revisions retain historical meaning and can have live stale status.
Corruption, quarantine, purge or missing/replaced stores reject before projection
reuse. Server restart reconstructs cold, and close releases both entry kinds.

### Incremental successor construction

The logical compiler can copy a previously verified projection and execute only
its appended change sets. Eligibility binds the exact original frozen base,
original snapshot identity, complete base repository membership, canonical
change-set prefix, installed compiler identity, projected bytes and projected
membership. The compiler snapshots the program representation into immutable
inputs, then issues continuation provenance only after successful final compilation
and cumulative analysis. Caller-owned edit mappings and semantic-intent maps cannot
rewrite that provenance.

The operation-local owner may offer its last projection. The existing bounded
cache may offer the immediate predecessor of the same proposal on an exact
successor miss. Both feed the same compiler-owned eligibility check; neither
adds a cache, persistent checkpoint, store format or compatibility mode. An
incompatible or absent prefix selects complete replay, including after eviction
or restart. A cold focused workflow may first reconstruct its predecessor during
preflight and then use that newly verified material for the suffix in the same
operation; it still pays for the first reconstruction.

Successors use a new file table with immutable byte values. All edit semantics,
manifest membership calculations and cumulative analysis retain the original
accepted base. Final authority compilation, semantic successor validation and
complete-program policy/module analysis still run. This is a computation reuse
boundary, not a new accepted baseline or authorization/publication proof. The
independent review, candidate-verification, application and recovery paths above
continue to select full replay.

The deciding structural claim is suffix-only edit execution and manifest
regeneration for a simple append with an eligible predecessor. Canonical program
comparison, final compilation, retention accounting and complete analysis remain
whole-material work. Representative successor-admission latency qualification is
tracked in the [incremental successor report](../../docs/plans/purpose-separated-standards-engine/reports/performance-incremental-successors.md);
it is distinct from repeated-read latency or focused-test duration.

## Bounded grouped reads

`read_many` takes one explicit snapshot and 1–32 ordered `items`. Each item has a
`target` and optional `detail`; authoring also permits the single-read coverage
and routing options. Exact duplicate requests are invalid. Reuse the snapshot
returned by routing or a single read, and select only the needed guidance.

The result contains the original snapshot and ordered single-read results.
One complete durable content/identity validation supplies the whole operation;
current snapshot lifecycle is checked before every item and before return.
Purpose, exposure, prerequisite and item-option checks use the ordinary read
projection. Any failed item or lifecycle observation rejects the entire set.
No item content is returned on failure. A new independent call verifies durable
content again. This is a new explicit operation, not a change to single reads.

The complete domain result is bounded to 2 MiB in the transport's default JSON
encoding (ASCII escaping and default separators); protocol framing, alternate
pretty-printing and MCP's duplicate structured/text encodings are outside that
payload bound. A larger set returns `READ_MANY.RESULT_LIMIT` in authoring or
`APPLICATION.RESULT_LIMIT` in application. Select fewer items or smaller policy
scopes; the Engine neither truncates material nor substitutes partial success.
`read_many` uses the named operation through MCP, the reference CLI and the
native facade; it is not a new request variant inside `query` or `query_proposal`.
Restart clients/servers after the interface update to discover the new operation.

## Application qualification

A declaration identifies an entire canonical module or registered operational
prompt/template and the Engine-derived exact reviewed binding. Scoped policy
reads inherit the containing module's qualification. Whole-module material
includes headings, tables, links, metadata and registered policy declarations;
Router material additionally binds the actual routing facts, rules and bases.
Operational aids bind their source content and registered policy-owner facts.

The derived states are `unreviewed`, `current` and `needs-review`. Content changes
preserve the old declaration as stale until explicit renewed approval or
withdrawal. An application read requires its selected unit and actual mandatory
prerequisites to be current. Unknown applicability remains a request for facts;
a missing required qualification is an explicit unavailable observation.

Supplementary relationships remain selective. A prompt's policy-impact
association does not acquire `Requires` semantics. The application graph view
contains permitted endpoints before traversal, so hidden intermediary nodes
cannot connect otherwise disconnected visible material. Whole-module discovery
includes relationships declared by its registered policy units.

Eligibility is an editorial decision. The runtime checks the declaration,
binding and required closure; it does not classify sentiment or prove prose
quality. No positivity model or lexical prohibition list is part of the runtime.

## Decision provenance

Each record owns one descriptive subject association. The standards-aware graph
source derives the `justified-by` edge in `decision-provenance`; no second
editable copy of that association exists. Supersession links form an acyclic
history. Retired records remain readable by authoring callers and can retain
historical subjects, while active records require a current canonical subject.
These relationships have no automatic normative-dependency or impact meaning.

A record includes its canonical identity and subject, Engine-derived subject
binding, origin, rationale, and the existing four-field evidence representation.
Optional sections hold assumptions, limits, alternatives, reconsideration and
supersession. Historical-origin claims require evidence references. An explicitly
unrecorded origin permits an empty account instead of fabricated history.

A record can become `needs-review` after its subject changes. Updating rationale
alone changes that support record and its localized review, not unchanged
normative semantic revisions or every unrelated consumer certificate.

## Authoring operation map

All edits travel in the existing `StandardsChangeSet` through `propose`/`revise`,
analysis, explicit review and atomic local `apply`. Exact fields are supplied by
the current generated schema; this table is a navigation aid, not a validator.

| Task | Edit or read |
| --- | --- |
| Read a complete owner or scoped policy | Authoring `read`; inspect metadata/relationships as needed |
| Revise module body and metadata | `revise-standard` |
| Relocate/rescope registered headings in a full rewrite | `revise-standard.scope_updates`, with all existing scope identities and explicit semantics |
| Register a selected scope within an existing owner | `register-policy-unit`, using the existing canonical module ID and a new policy declaration |
| Revise one policy scope | `revise-policy-unit` |
| Create/revise a supplementary reference | `create-standard` / `revise-standard` with the existing reference role |
| Inspect an existing registered prompt/template | Authoring `read` returns its opaque target handle |
| Revise a registered prompt/template | `revise-operational-artifact` using that handle, title and body |
| Record or replace decision reasoning | `put-provenance` |
| Retain a reasoning record as historical | `retire-provenance` |
| Approve exact final application material | `approve-application-content` |
| Withdraw an exposure decision | `withdraw-application-content` |
| Change normative prerequisites/specialization | `replace-standard-relationships` |
| Change other actual consumer relationships | Existing `put-policy-relationship` / `remove-policy-relationship` |
| Change Router decisions or presentation | Existing routing rule/fact edits |
| Inspect a draft | Authoring `query_proposal` against its exact revision |
| Publish the reviewed candidate | Existing explicit `review`, then `apply`; follow `recover` on recovery-required |

Existing-owner registration supports modules with zero or more registered
policies. It preserves existing prose and declarations, and can follow a
whole-module rewrite in the same candidate. New scopes are selected explicitly;
module and existing-policy edits precede the registration group, then consumer
relationships resolve against the completed registry. Existing canonical scope,
identity and lifecycle validation applies. Registration alone issues no coverage
certificate. The same logical program is replayed after restart or through an
eligible incremental successor; storage and handle editions are unchanged.

The [registration qualification plan](../../docs/plans/existing-policy-registration/plan.md)
tracks the current source correction and its outstanding full-checkout/MCP
acceptance. Interface 33 availability does not by itself certify that qualification.

The Engine resolves unordered same-change-set references against the final
candidate. It stages retirement and withdrawal privately before dependent owner
changes, computes approval/provenance bindings after material edits, and validates
the complete result before admitting the proposal revision. Contradictory edits
and dangling active subjects reject without publication. Registered operational
aid handles identify only captured prompt/template registrations; requests do
not authorize arbitrary repository-file or source-code writes.

Meaning-preserving rewrites may change structural text while keeping the policy's
semantic revision through an explicit `preserve` decision. Substantive changes
select the next revision. The candidate contains the exact intended semantic
revision before review; preservation/next-revision proposals are analyzed against
those same bytes. The Engine does not rewrite semantic versions after review.

## Versions and coordinated cutover

Current Engine package/transport implementation: 0.2.0. Engine interface: 36.
Analysis request: 6; result/state and Analysis handles: 7. The semantic-revision
interpretation change belongs to Analysis 7. Unchanged Snapshot, proposal,
readiness, application and generic identity/storage contracts keep their
existing independent versions. Updating one implementation does not couple all
version domains.

Before replacing an installed Engine, inspect active proposals, readiness and
recovery-required work through its current authoring interface. A replacement
supporting the same retained record formats can resume them through its documented
recovery path; interface 35 preserves those formats. When a retained format is
unsupported, complete its recovery with the owning implementation or preserve its
exact store under an explicit operator disposition. Keep store bytes and Git
history. Install current code/schemas and reconnect with purpose-selected launch
configuration. A fresh store does not carry an admitted application and is not a
recovery procedure. Store selection never converts old proposal records.

For pre-merge qualification, use a disposable clone whose local `main` identifies
the exact candidate. Avoid retargeting the user's real accepted branch merely to
make a test pass. The code is integrated before the content guide is executed.

The host controls access to the checkout, database and private logs. A caller
with independent access to those files can read them outside the Engine. Use a
fresh application context after standards authoring; changing an interface does
not remove information already in a model conversation.

## Verification boundaries

Focused tests cover qualification, staleness, purpose/handle escalation, hidden
intermediaries, schema closure, scope discovery and bounded diagnostics. Separate
process tests exercise CLI/MCP output and real SQLite reopening. The supporting
workflow test uses real proposal/review/Git publication with synthetic content;
its fixture decisions are not endorsements of real standards.

Run affected package tests and the structural checkpoint separately. The optional
`tests/mcp_workflow_client.py` additionally exercises the official SDK, both
purposes and interrupted-publication recovery using a separately supplied client
environment. The configured Codex adapter test names the authoring registration
with `--server`. Pinned-platform/client acceptance and independent review are
reported separately from supporting tests in another Python environment.

## Proposal consumer inputs and application preview (interface 34)

Use `register-consumer` inside `propose` or `revise` to declare an existing
tracked consumer. The Engine captures its original proposal-base bytes before
admission, retaining them in the immutable logical edit. Replay uses those bytes,
not the working tree or a later accepted revision. Registration, newly created
policy scopes and their consumer relationships can share one candidate. An
explicit relationship uses the registered canonical consumer ID. Registration
neither claims complete coverage nor creates a review certificate.

The content editor supports registered Markdown documentation as well as prompts
and templates. Hidden directories have the same repository containment and
tracked-file requirements. Fixture and implementation consumers remain read-only
through this editor. Original file bytes supply publication's baseline; an
unchanged registered source is not rewritten. Fixture bytes, unrelated policy
identities and prior proposal records remain intact.

An authoring caller uses `preview_application` with the exact draft revision and
one application read, route or related request. Candidate results carry that
revision, without published-snapshot or snapshot-child handles. Their
continuations remain candidate previews. The same application view enforces
qualification, prerequisite closure and graph filtering. A missing qualification
is a candidate-application rejection, not partial acceptance. Normal application
sessions retain their published-only operation set.

`maintain_evidence` remains accepted-repository maintenance, not draft mutation.
Use logical registration for draft-only scopes. After installing this change,
restart the actual MCP server and reconnect the client; initialization reports
the current interface edition and configured purpose. Existing workflow-response verbosity
and hot catalog replacement are not changed by this capability.


## Admitted publication recovery (interface 35)

Use `recover` with the original readiness context after an interrupted or failed
publication. Its default `observe` action reads the exact selected application;
it may record a durable applied outcome when the target is already the candidate,
but it performs no Git write. The native equivalent is `recover_application`.

When the target is still the expected revision, an authorized operator can select
`action: "complete-publication"`. This action reconstructs from the original
captured proposal and reviewed coverage, requires the exact already-admitted
commit ID, reruns complete verification, checks current readiness and both recovery
and application permission, and makes one expected-target publication attempt.
It keeps the existing application selection. Changed candidate content, stale
readiness, inaccessible evidence, denied authority and a competing target stay
explicitly unresolved. A target already at the candidate is reconciled without
another write. A failed outcome write after Git success is completed by the next
observation. Focused and native repeated recovery return the applied result.

An unchanged target does not establish that no prior publication occurred.
Explicit completion authorizes re-establishing the candidate at that target; it
is not a historical exactly-once claim. The Engine never removes a lock, changes
permissions, resets the store, forces the branch, or substitutes a newer draft.

The implementation process needs a Git-writable authorized host for the same
repository and store. Install Engine source without moving the real accepted ref
merely for installation: an admitted application is still bound to its original
expected target. Restart the server process and reconnect before reading the
interface-35 recovery schema. Install the current code and interface schemas
together in the implementation checkout, while leaving its accepted `main` at
the admitted expected revision. The facade loads interface schemas from
`--repo-root`; selecting a different Python module path alone does not update
those schemas. Store selection must remain unchanged if the installed host used
a nondefault store. Handoff data is the exact readiness/context, not a fabricated
handle assembled from a truncated identifier.

Authoring failure details carry the Git operation, exit code and recognized
fixed stderr phrase when available. Raw stderr can contain sensitive paths or
hook output and stays in the private Git exception, not the MCP response. Earlier
uncaptured stderr cannot be recovered retrospectively. Obtain a new bounded
observation from the supported operation on the correct host. Ordinary application
interfaces still cannot call either recovery operation or read its diagnostics.

## Routing and review workflow (interface 36)

### Router presentation

Router selection is declared by unfenced top-level two-column pipe tables.
Canonical normative-module links in the destination cell identify selected
modules. Header text, section headings and surrounding prose are presentation;
a historical example heading is not an executable delimiter. Reference-module
links are optional help. Code fences, indented code, HTML comments and non-table
prose do not declare selections.

The existing Analysis routing owner parses these exact rows for the Router
loader, `read(include_routing)` and logical route edits. The explicit executable
facts/rules still own applicability, and their target agreement is verified.
Edits preserve all text outside selected rows, and new rows join an existing
normative selection table. Ambiguous duplicate rows reject an individual edit.
Unsupported link paths or missing canonical targets remain explicit failures.
No Router body, policy identity or routing fact is automatically migrated.

### Decisions and concise workflow views

Focused workflow results default to `detail: compact`. A pending or complete
Analysis is represented by its exact handle, truthful work counts and a
`workflow_details` link; publication, readiness, recovery and errors retain
relevant fields. `detail: full` selects complete diagnostic output. Native
analysis operations retain their full result contract.

`resolve_many` is authoring-only. Supply one exact current proposal Analysis
`context` and 1–128 explicitly authored `submissions` (up to 256 KiB of JSON
submission material). All work handles bind that original context. Required
work newly revealed by a decision is retrieved in the next round rather than
invented as a handle on the old analysis. Duplicate targets and foreign work
reject before authorization.

Each item uses the ordinary single-decision validator with current evidence and
authority. The staged successor is evaluated before the next item. Only the
final Analysis aggregate is published, conditionally on the proposal head still
matching. A rejected batch records none of its intermediate Analysis states.
External authority/provider observations are not part of a global transaction.
No review, readiness, apply or implicit Git write is included in decision batching.

Example flow (obtain actual field values and handles from current results):

```text
workflow_details({analysis: context, section: "pending_obligations", limit: 8})
resolve_many({context: context, submissions: [explicit_decision_1, explicit_decision_2]})
```

Each `pending_obligations` item contains the complete `obligation` plus its
submission `work` handle. Coverage work is a coverage-requirement handle;
consumer/impact work is an obligation handle. `fact_requirements` supplies the
actual fact definition and work. Preserve every decision's fingerprint, evidence,
rationale and authority requirements. Registration is distinct from coverage.

Other detail sections expose all obligations, current coverage certificates,
recorded dispositions/facts, reading plan and changed policy units. Requests
select at most 16 records (default 8). The 64 KiB JSON domain-result limit is
independent of MCP framing and its text/structured duplication. Oversized items
are rejected, never truncated. Use smaller pages or existing targeted inspection.

Follow the exact `next` arguments. A nonzero offset requires the returned
`observation` digest. It binds the exact analysis, section and complete observed
items, preventing accidental mixing of contexts or sections. Historical details
remain snapshot-bound; decision and publication owners perform live evidence
validation. Lifecycle failures remain explicit. Pages are observations, not approvals or
new mutable workflow records. Explicit full analysis remains available.

### Running implementation and catalog

`runtime_info` is available to either purpose without opening Git or the
standards store. MCP initialization, tool listings, tool results and unknown-tool
errors expose the same opaque instance/interface/catalog metadata. The operation
also compares a supplied `expected_catalog` digest and observes on-disk runtime
installation state.

Runtime identity binds startup-selected code/package and interface inputs. It
excludes standards text, Git refs, authoring databases and user paths. It assumes
a coherent installation before startup, not concurrent replacement during import.
A disk change produces `restart-required`; unreadable inputs produce `unavailable`.
A matching installation with a differing client catalog requests `refresh-tools`.
The server cannot inspect or clear the client's private cache.

After replacing implementation files, stop the old process, install coherently,
start the new process, reconnect and inspect `runtime_info`/`tools/list` before
mutations. Check the new instance ID as well as interface 36 and the catalog digest.
`listChanged` remains false: no hot reload is implemented. Content publication
alone does not require an implementation restart. Standalone native facade
catalog identity describes its native operation contract; compare catalogs within
the same transport/purpose. The reference CLI uses the focused MCP catalog identity.

Interface 36 changes the focused result contract and adds three operations. It
preserves Analysis 7, original Snapshot/SQLite representations, readiness, exact
candidate recovery and the current coverage-authorization semantics. Existing
native or explicit-full diagnostics are current features, not a dual-version
compatibility implementation. Local migrated standards and receipts stay owned
by their accepted publication.
