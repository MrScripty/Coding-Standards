# Coverage follow-up

The [verification follow-up](standards-verification-investigation-2026-09-04.md)
reported that repository coverage certificates were stale. Comparing exact Git
content through the production Analysis coverage compiler establishes when
that happened:

| Revision | Registered policy units | Current attestations |
| --- | ---: | ---: |
| `bec1f5d9` — before the audit | 51 | 51 |
| `5adff47f` — standards migration | 51 | 10 |
| `5d406ff4` — verification and Engine changes | 51 | 0 |

All three revisions contain the same 51 stored claims across 11 source files.
The loader ignores claims whose requirement IDs do not match the current
compiled scope. Passing the repository checkpoint does not establish that
consumer coverage is current.

## What changed

The [per-subject inventory](standards-coverage-followup-2026-09-04.evidence.json)
records prior/current requirement IDs, owners, semantic revisions, changed
projection fields, changed horizon members, and the prior evidence sources.
It compares the two implementation commits to the pre-audit revision using
the coverage compiler at `5d406ff4`; it does not claim to replay historical
compiler implementations.

- Nine policy units moved to detail owners while retaining their IDs.
- Two semantic revisions increased from 2 to 3:
  `topic.architecture.immutable-authority-closure` and
  `workflow.verification.acceptance-claims`.
- Ten policy-unit representation digests changed; two structural digests changed.
- The migration changed 41 local dependency horizons. The subsequent
  verification change left all 51 horizons different from the baseline.
  Across the final comparison, 72 distinct horizon members changed, including
  standards consumers, evidence suites, and Engine contract artifacts.
- Fact-schema, relationship-provider, and applicability-language identity fields
  did not change in this comparison. A global routing-fact invalidation does
  not explain these stale certificates.

These differences identify review scope. They do not establish that changed
evidence preserves a previous completeness claim. In particular, removal of
prose assertions withdrew their claimed evidence; a green structural check
cannot replace the semantic review those assertions purported to supply.

## Engine visibility

Interface version 22 supports `include_coverage: true` in a `read` request,
through both `query` and `query_proposal`. A module read returns its registered
policy units; a policy-unit read returns only that unit. Each entry contains its
current requirement digest and either `current-attestation` or `review-required`.
Omitting the option leaves ordinary reads unchanged.

The status belongs to the captured snapshot or exact proposal revision. It
uses the repository coverage authority, not live worktree files or a count of
passing tests. Empty `subjects` means no registered policy units in that scope;
it must not be interpreted as complete coverage. Analysis-local attestations
remain separate from repository certificates.

The public transport was exercised against the retained `5d406ff4` snapshot:
all 16 Planning policy units report `review-required`. The focused adapter test
also supplies authoritative covered and uncovered outcomes, checks unit/module
scope, and checks the empty-registry case. Proposal navigation exercises the
same optional projection.

## Remaining reviews

For each subject in the inventory, a reviewer must assess the changed consumers
and evidence, record exclusions where justified, and submit the actual evidence
against the exact requirement returned by Analysis. The inventory marks every
subject `required`; none of these certificates has been renewed.

The current Engine can resolve an attestation into an immutable Analysis state.
Its logical authoring interface has no operation to publish that reviewed claim
into the repository attestation registry for future independent snapshots.
That is a further authoring gap. A publication operation needs to consume an
authorized, evidence-bound review and recheck the destination requirement;
accepting replacement IDs or caller-authored certificate files would bypass
the review boundary. The optional read implemented here exposes status but
does not close that publication gap.

The two downstream pilots still need repository/task selections. Each pilot
should record the task and repository revision, routing facts and follow-up
questions, standards actually read, resulting plan or implementation, relevant
validation, missed or unnecessary guidance, and whether completion required
loading the full library. Routing word counts remain navigation measurements,
not completed pilots.

## Validation

- The public `verify_repository` operation refreshed derived suite inputs and
  passed all 271 suites / 858 checks.
- Forty-five tests passed across focused runs: 14 Interface, 20 contract,
  nine rendering, and two navigation regressions. The navigation checks confirm
  exact proposal-revision binding and live-worktree isolation. The initial
  dotted contract-test invocation failed to
  import its local `support` module; directory-based discovery passed all 20.
- Generated contract freshness, Ruff checks, and whitespace checks passed.
- The revised navigation fixture supplies its own policy body instead of
  searching for exact Planning prose; it also removes an exact summary-sentence
  assertion. Fixture payload equality and requirement identities remain
  legitimate behavioral assertions.
