# Milestone 7 Source-Index Verifier Re-plan

## Re-plan Finding

Source package `7.4c3.1` established final index-purity evidence with a bespoke
Coding verifier and flat route fixture. Applying that structure independently
to the remaining 26 packages would duplicate parsing, corpus, manifest,
identifier, link, heading, size, and prohibited-authority checks. It would also
place recurring policy in source-specific shell scripts and create avoidable
maintenance and review load.

The accelerated migration contract requires one reusable verifier per policy
family and allows batching only by shared semantic outcome. All final source
packages share one structural outcome: a former normative source becomes a
derived, concise, non-normative index whose routes resolve to canonical owners
and whose frozen identifiers remain exactly dispositioned. Source-specific
semantic evidence remains with existing owner verifiers.

## Selected Design

Create one reusable source-index closure engine, one live aggregate verifier,
and focused engine self-tests. Replace the bespoke Coding closure verifier with
the aggregate system; do not retain a compatibility wrapper.

The live registry is directory-based:

```text
fixtures/source-closure/
  coding/
    contract.tsv
    headings.tsv
    routes.tsv
    prohibited.tsv
  commit/
    ...
```

Each accepted source package owns one distinct fixture directory. This permits
isolated draft work on different sources without shared fixture-table writes.
The aggregate verifier discovers registered directories in deterministic source
order and invokes the same engine contract for each one. Shared engine,
aggregate verifier, plan, ledger, corpus, and final integration remain serial
integration-owner files.

## Canonical Inputs

The immutable final source-closure manifest remains the authority for source
order, canonical owner, historical shape, and `retain-index` or
`rewrite-index` treatment. The exact disposition and generated owner-map tables
remain the frozen identifier lineage. The current corpus remains the authority
for whether an accepted source is `derived`.

A per-source fixture does not repeat those decisions. It supplies only:

- source path, maximum concise line count, and expected title;
- the complete ordered heading set;
- unique required navigation targets; and
- exact prohibited legacy-authority literals specific to that source.

Missing fields, duplicate routes, duplicate headings, unresolved targets,
unregistered fixture files, a source absent from the immutable manifest, an
owner mismatch, a non-derived corpus row, identifier-count mismatch, malformed
TSV, or unknown fixture schema is a typed invalid verification outcome. The
engine cannot skip a malformed source or infer a default.

## Engine Contract

For every registered source, the engine must prove:

1. the source and canonical owner exist;
2. the source has exactly one immutable manifest row;
3. the corpus row is `derived` and retains its frozen kind, target role,
   preliminary disposition, and baseline source;
4. the current title, full ordered headings, and line count match the fixture;
5. every required route is unique, exists after anchor removal, and appears as
   a Markdown target in the source;
6. every prohibited literal is absent;
7. generic legacy-authority and fallback phrases are absent;
8. the generated owner map and exact disposition table contain the same
   positive source identifier count; and
9. the Router does not select the former source as authority.

The live aggregate verifier must report the exact number of registered sources
and reject any fixture directory lacking one of the four required files. It
does not mark pending manifest sources failed merely because their package has
not run; registration occurs atomically with source closure.

## Negative Engine Evidence

Focused engine fixtures must prove rejection of at least:

- malformed contract or table columns;
- a duplicate heading or route;
- an unresolved route target;
- a source absent from the closure manifest;
- a corpus row that remains normative;
- legacy authority or fallback wording;
- heading or line-bound drift; and
- owner-map/disposition count disagreement.

Tests must invoke the same engine used by the live aggregate verifier. A test-
only parser or reduced policy copy is not acceptable.

## Ordered Implementation

1. `7.4c3v1` establishes the engine and self-tests, moves the accepted Coding
   route fixture into a source-owned directory, adds Coding contract/headings/
   prohibition fixtures, replaces the bespoke Coding verifier with the live
   aggregate verifier, and proves the existing Coding closure unchanged.
2. `7.4c3.2` closes the Commit index and registers its independent fixture
   directory without changing shared engine code.
3. `7.4c3.3` through `7.4c3.27` register their own directories in immutable
   source order. Engine changes require a separate checker-infrastructure slice
   and full-suite gate; a source package cannot modify the engine to make its
   own content pass.

## Lifecycle Verification Ownership

The final source-closure planning checker owns the accepted aggregate design,
immutable source order, and durable package contract. It does not own the
mutable lifecycle state of `7.4c3v1`. The active plan records that state while
the live source-index aggregate verifier owns implementation acceptance after
the engine exists.

Requiring `7.4c3v1` to remain `Planned` after its evidence is accepted would
repeat finding F077 and make a completed parent checker invalidate correct
later work. The planning checker therefore requires the child milestone to
exist without fixing its transient state. The implementation slice is
authorized to mark F078 resolved when the bespoke verifier has been removed
and the aggregate engine owns the accepted evidence.

## Bounded Write Sets

Lifecycle repair `7.4c3v1r` may change only this re-plan, the final
source-closure planning checker, the active plan, and the execution ledger. It
cannot change standards, source indexes, fixtures, executable engine code,
corpus data, findings status, Router, dispositions, owner map, generated
inventories, metadata, configuration, or lockfiles.

The `7.4c3v1` implementation slice may change only the reusable engine, engine
self-test fixtures and verifier, live aggregate verifier, existing Coding
closure verifier and fixture paths, F078 resolution status, active plan, and
execution ledger. Coding source text, corpus, manifest, dispositions, owner
map, Router, canonical owners, other former sources, generated inventories,
metadata, configuration, and lockfiles remain unchanged.

Each later source package may change only its former source, its corpus row, its
own new fixture directory, active plan, and execution ledger. It cannot change
the shared engine, another source's fixtures, canonical owners, Router,
dispositions, owner map, or generated inventories. If the engine cannot express
a genuinely shared invariant, stop and re-plan a separate infrastructure slice.

## No Fallback

The engine cannot accept an unregistered source, partial fixture set, inferred
owner, unresolved target, permissive heading set, missing prohibition, stale
normative corpus row, weaker identifier count, or source-specific bypass. The
old bespoke Coding verifier is removed when the aggregate system assumes
authority; it is not retained as a compatibility path.

## Verification Gates

The planning slice requires this re-plan's focused structural assertions, final
source-closure planning evidence, plan structure, shell syntax, diff integrity,
and the complete suite because shared closure verification is being authorized.

Lifecycle repair `7.4c3v1r` requires a negative scan for transient child-state
ownership, durable child-presence evidence, plan structure, shell syntax, diff
integrity, and the complete suite because the shared parent checker changes.

`7.4c3v1` requires engine positive and negative fixtures, unchanged Coding
source/corpus semantics, exact Coding closure, aggregate discovery, Router
closure, historical checker ownership, shell syntax, diff integrity, and the
complete suite. Every subsequent source package requires its aggregate source
result, affected historical/owner checks, and the complete suite because corpus
classification remains shared.

## Re-plan Triggers

Stop and re-plan when:

- a source needs a structural invariant not shared by final indexes;
- source-specific semantics would have to enter the generic engine;
- fixture isolation cannot avoid overlapping draft write sets;
- replacing the Coding verifier weakens an accepted assertion;
- engine self-tests require a second parser or policy copy;
- generated artifacts must change before final `7.4c4`; or
- any package needs to change its canonical owner, immutable treatment, or
  objective.
