# Standards verification and Engine follow-up

The follow-up addresses brittle prose assertions, inconsistent Snapshot path
comparison, and missing Engine routing and verification operations. It follows
the [standards audit](standards-structure-and-guidance-2026-09-04.md) and
[migration](standards-migration-2026-09-04.md).

## Wording assertions

The registered catalog contained 786 `text`, 60 `markdown_section_text`, five
`exact_text`, and 11 `table_text_absence` assertions: 862 in total. All five
whole-document comparisons froze the prose of migration indexes. Two substring
checks inspected Python source for implementation fragments. Other checks froze
sentences, wrapping, link labels, retired wording, historical report text, or
literal TSV row prefixes.

The [disposition inventory](standards-verification-investigation-2026-09-04.evidence.json)
records every removed check and any replacement by suite/check ID:

- 79 checks have structural replacements. Migration indexes and the four suites
  previously composed entirely of text checks now check actual navigation
  destinations. Keyed migration assertions use parsed table projections over
  identifier, source, owner, and disposition fields, excluding narrative cells.
- 783 phrase assertions are retired. Existing decision fixtures, graph checks,
  links, metadata, contracts, and structured records remain. Replacing words
  with synonyms or regular expressions would preserve the same false assurance.
- All 271 suite IDs remain registered. The resulting checkpoint has 858 checks,
  versus 1,641 before this change. The four formerly prose-only suites now state
  their limited navigation claim in their descriptions.

This change deliberately withdraws claims that string presence establishes
policy meaning. Retained fixture rules exercise their configured decisions;
passing them does not prove those decisions adequately express the standards.
Consumer, impact, and audit review must evaluate guidance, missing nuances, and
semantic changes. This follow-up is not a new semantic review of every existing
policy or an assertion that the 783 removed checks have equivalent automatic
coverage. The original migration's downstream agent pilots remain outstanding.

The current stored coverage certificates do not match the current coverage
requirement identities; the registered coverage adapter reports no fully
covered owner. Certificates must be revalidated through the Engine audit
workflow. No certificate was silently renewed or re-keyed. A former test assumed
Planning was perpetually covered; it now supplies explicit covered and uncovered
authority outcomes and verifies that the adapter honors both.

A repository test rejects current registrations of the four retired check kinds.
Their parsers remain available for historical captured suite definitions.
`markdown_targets` checks resolved repository destinations while allowing prose,
labels, wrapping, and link order to change. Its regression test rejects a bare
path mentioned in prose instead of an actual link.

Exact comparisons still have legitimate, narrower uses: enum and canonical IDs,
protocol fields, content digests, canonical serialized bytes, generated
projections, and registered heading locators/anchors. These identify data or
representation contracts; they must not claim to judge sentence quality.
The two retired Python substring checks are superseded in purpose by the
existing Analysis replay and decision-traceability behavior tests, not by source
text or AST-shape assertions.

## One canonical Snapshot path order

Snapshot identity and `CapturedContent` already order paths by components in
Unicode codepoint order. For example, `profiles/rust/api.md` precedes
`profiles/rust.md` because the component `rust` precedes `rust.md`.
SQLite's `ORDER BY logical_path` instead compared slash-joined strings, putting
`rust.md` before `rust/api.md`. Database row order had leaked into a domain
comparison. The earlier repair sorted submitted files as strings, making the
comparison pass while retaining this second rule.

The storage reader now parses `SnapshotPath` and uses its canonical component
order. Publication compares that result directly with `CapturedContent`.
Identity framing and persisted content IDs are unchanged. Reopening and
recapturing equivalent content is tested with nested paths, punctuation, and
both composed and decomposed Unicode names. Unicode spellings remain distinct;
this is ordering, not normalization.

## Engine interaction

Interface version 21 adds `put-routing-rule`, `remove-routing-rule`,
`put-routing-fact`, and `remove-routing-fact` to atomic change sets. Callers
supply domain IDs, applicability, fact definitions, readable conditions, and
rationale. The Engine owns Markdown rows and TOML serialization, validates the
final rule/fact graph, and refreshes derived suite inputs. Atomic changes can
create a detail standard and route together, replace targets, or remove a fact
and its referencing rule together. Routing-only changes enter Router Analysis.
New topic and workflow standards can use nested detail IDs. Router reads can
request `include_routing: true` to obtain editable fact and rule definitions
through snapshot or proposal queries, without reading internal files. Fact
revision checks use the applicability owner's semantic projection, so value
order and prompt or alias changes do not create false semantic revisions.

`verify_proposal` runs the application checkpoint in an isolated candidate for
an exact revision without publishing or granting review approval.
`verify_repository` checks the working tree and offers an explicit authorized
`refresh_verification_inputs` option to rebuild stale generated suite inputs.
Its result includes a pass flag and diagnostic report. Snapshot capture remains
bound to committed content; verification does not manufacture an accepted head.
Application still reruns verification before publication.

The local authorization adapter also had an independently confirmed defect:
`repository-content` evidence was resolved to the identifier's bytes instead of
the referenced document. It now reads the repository file, validates its digest,
and rejects unavailable files or unsupported providers. Local authorization and
revocation statements have their own `local-statement` provider contract and
local authority revision 2. Custom authorization adapters retain their contracts.

## Validation

The public `verify_repository` checkpoint passes all 271 suites and 858 checks.
Focused Python runs and corrected-case reruns pass 437 distinct tests:

- 21 logical-authoring tests and 13 Interface tests, including public Router
  read → proposal edit → draft read, editable schema round trips, escaped table
  punctuation, atomic rule swaps, fact removal, and semantic revision behavior;
- eight result-rendering tests and one real draft-verification/application/cold
  readback integration test, including unchanged repository state after draft
  verification;
- 23 Snapshot tests, 20 contract compiler/projection tests, and 351 verifier tests.

The complete checkpoint was invoked through the bundled Engine transport.
Contract examples and generated projections agree with Interface version 21.
Changed runtime Python files pass Ruff, and the diff has no whitespace errors.
These are local checks, not a completed cross-platform matrix or downstream
agent pilot. Existing coverage certificates were not renewed.
