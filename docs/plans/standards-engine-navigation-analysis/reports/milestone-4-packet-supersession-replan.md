# Milestone 4 Packet-Supersession Replan

## Status

Implementation is stopped at a verified packet-lifecycle contract conflict.
The immutable analysis-state work remains uncommitted at this boundary.

## Trigger

Every packet is content-addressed from its complete immutable `AnalysisState`.
The engine also keeps a shared mutable set of superseded packet IDs. These two
rules conflict when the same deterministic analysis is prepared more than once.

The focused reproduction was:

1. Prepare one modification analysis and receive packet `P`.
2. Resolve `P` to a completed report.
3. Prepare the exact same request again without ambient prior state.
4. Receive the same packet identity `P`.
5. Attempt to resolve the newly returned packet and receive `PACKET.STALE`.

The observed packet ID in both preparations was:

`packet:sha256:8b10b261fcf140f39244b9d5e348e8b12d09e2dd604cfd4335f5677214ae0674`

The result depends on mutable store history even though the request, exact
snapshots, analysis state, and packet bytes are equal. This violates the
accepted requirement that equal request inputs produce byte-identical usable
results and makes a content-addressed handle name both a valid immutable state
and a globally stale execution position.

## Options

| Option | Result | Assessment |
| --- | --- | --- |
| Remove global A1 supersession and allow immutable packet branches | `resolve(P, submission)` is a pure transition; equal inputs produce equal outputs, while different submissions create inspectable branches. | Recommended |
| Add an execution or session ID to packet identity | Distinguishes runs and supports one mutable head. | Reject for A1; breaks deterministic content identity and adds caller-visible coordination |
| Keep packet identity and add a separate mutable session handle | Preserves packet content identity but makes resolution depend on ambient session-head state. | Reject for A1; recreates the hidden state the immutable-state design removed |
| Return an earlier descendant when identical preparation is repeated | Avoids returning a stale packet by consulting store history. | Reject; preparation becomes ambient and no longer depends only on declared inputs |

## Superseding Single-State Decision

The accepted greenfield correction goes beyond removing supersession. Packet,
report, and state identities are three names for one underlying immutable
analysis value. A1 therefore adopts one `AnalysisState` and one
`AnalysisHandle`. Pending packets and completed reports remain presentation
vocabulary only as non-authoritative `PendingResult` and `CompleteResult`
projections.

State identity includes exact accepted and proposed authority, normalized
changes and semantic proposals, authorization-authority and provider input
views, semantic contract versions, every dependency-valid observation and
disposition including dormant decisions, authored coverage attestations, and
their evidence and authorization. It excludes prior handles, lineage, decision
order, derived work, certificates, completion, timestamps, summaries, and
storage location.

The bound analysis kernel resolves immutable authorities, projects results,
and advances state. Providers execute only during state construction or
advance over declared immutable inputs. Requirements, obligations, traces,
reading plans, certificates, and completion are deterministic cacheable
projections.

## Recommended Contract

A1 analysis should form an immutable content-addressed directed acyclic graph:

```text
AnalysisState S0
      + submission A -> AnalysisState S1
      + submission B -> AnalysisState S2
```

Advancing the same state with the same submission is idempotent. Advancing it
with a different authorized submission creates a separate branch; it does not
silently overwrite another result. Exact packet, requirement, obligation,
snapshot, evidence, and authorization validation still applies.

A1 has no packet staleness. A missing handle or authority is unavailable,
malformed content is invalid, absent work is not applicable, mismatched
dependencies are a context mismatch, and missing capability is unauthorized.
A different child transition has no effect.

Mutable-head compare-and-swap behavior remains necessary for Plan A2 controlled
authoring because authoring has a change session and a proposal head. It should
not be imported into read-only A1 analysis without that session identity.

## Required Replan

Before implementation resumes:

1. Replace packet, report, and analysis-state handles with one analysis handle.
2. Store only immutable authority inputs and dependency-valid accepted
   decisions; derive all work and completion projections.
3. Bind authorization-authority and provider contract/input views explicitly.
4. Remove global supersession and define repeated advance as an idempotent
   content-addressed transition with natural independent branches.
5. Add repeated preparation, decision-order normalization, dormant-decision,
   provider-unavailability, authorization-view, genuine cold-process, and exact
   authority-resolution fixtures.
6. Replace the runtime and schema atomically without compatibility loading.

Mutable compare-and-swap remains an A2 authoring concern. A2 must explicitly
bind a complete analysis handle to its current proposal head.
