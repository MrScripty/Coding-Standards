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

Application operations are `route`, `read`, `related`, `routing_facts`, `query`
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
current native operation. Identical snapshot roles share one material value;
distinct roots keep independent lifecycle and content observations. Exact
proposal projections carry their already-compiled base into logical authoring,
while changed candidates take the complete compiler path. Retained-decision
and pre-/post-submission evaluations still run independently, with current
lifecycle, revision and authorization observations at their existing boundaries.
The immutable material does not retain provider outcomes or evaluation results.

Each subsequent operation loads and verifies its own captured bytes. Publication
verification, target compare-and-swap and recovery obtain fresh observations;
no operation-local material crosses those barriers as permission or readiness.
The MCP/facade/SQLite lifetime remains per call. There is no cross-call compiled
cache, persistent derived cache, or alternate identity format in this increment.

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

Current Engine package/transport implementation: 0.2.0. Engine interface: 31.
Analysis request: 6; result/state and Analysis handles: 7. The semantic-revision
interpretation change belongs to Analysis 7. Unchanged Snapshot, proposal,
readiness, application and generic identity/storage contracts keep their
existing independent versions. Updating one implementation does not couple all
version domains.

Before replacing an installed Engine, inspect active proposals, readiness and
recovery-required work through its current authoring interface. Complete an
existing recovery obligation with its owning version, or retain its exact store
with an explicit operator disposition. Keep retained store bytes and Git history.
Then install the new code and reconnect clients with purpose-selected launch
configuration. An explicitly chosen fresh store may capture the accepted source;
store selection does not convert old proposal records into new-format state.

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
