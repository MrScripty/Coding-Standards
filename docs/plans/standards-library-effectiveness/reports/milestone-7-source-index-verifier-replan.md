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
- unique route names, canonical repository targets, and source-relative
  Markdown hrefs; and
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
5. every required route has a unique canonical target and unique href, the
   target exists after anchor removal, the href resolves from the source
   directory to that exact target and anchor without escaping the repository,
   and the exact href appears as a Markdown target in the source;
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
- the removed two-column route schema;
- a source-relative href that escapes the repository, resolves to a different
  canonical target or anchor, or is absent from the source;
- a source absent from the closure manifest;
- a corpus row that remains normative;
- legacy authority or fallback wording;
- heading or line-bound drift; and
- owner-map/disposition count disagreement.

Tests must invoke the same engine used by the live aggregate verifier. A test-
only parser or reduced policy copy is not acceptable.

## Nested Route Schema Replacement

Repair `7.4c3rh` replaces every registered `routes.tsv` row with the strict
three-column schema `route`, `target`, and `href`. `target` is the canonical
repository-relative identity used for existence and uniqueness checks. `href`
is the source-relative Markdown projection and may contain the `../` segments
required by nested stable entrypoints. The engine normalizes `href` against the
former source's directory, rejects repository escape, and requires its path and
anchor to equal `target` exactly before checking the source text.

The old two-column schema is invalid after this repair. The engine has no
compatibility parser, inferred href, root-relative-link convention, or nested
source bypass. All registered route fixtures change atomically, and the engine
positive fixture uses a nested `languages/rust/` source so the accepted
contract is directly exercised.

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

## Source-Specific Checker Repair

Preflight for each source package must inspect checkers that read the former
source. Assertions are classified before editing:

- semantic assertions prove canonical owner behavior, required routes, exact
  dispositions, typed outcomes, or prohibited legacy policy;
- structural assertions repeat title, heading, size, corpus, registration, or
  generic non-authority wording now owned by the aggregate engine; and
- obsolete assertions require migration-era wording or a temporary lifecycle
  state that the accepted source package must remove.

A source package may update only its own source-specific checker when an
obsolete structural assertion would otherwise require preserving legacy text.
It must retain semantic owner, route, disposition, and negative evidence; it
may delegate shared shape and registration evidence to the live aggregate
verifier. The package cannot add dual old/new assertions, accept either legacy
or canonical wording, or preserve migration-era text as compatibility
evidence.

Shared engine code, aggregate policy, cross-source checkers, canonical-owner
checkers, and historical execution-train checkers remain serial integration
authority. Their isolated preparation may proceed concurrently only after the
package inventory assigns each mutable checker to exactly one package and
freezes the semantic evidence that must remain. A checker that cannot receive
an exclusive write owner, or whose semantic obligations remain disputed, stops
that package for a checker-infrastructure re-plan.

## Concurrent Preparation And Serial Acceptance

Preparation order and acceptance order are separate contracts. Independent
packages may be analyzed, edited, and focused-tested concurrently in isolated
worktrees when the preparation inventory gives them non-overlapping former
source, fixture directory, and checker write sets. Shared engine, aggregate,
Router, corpus, manifest, disposition, owner-map, generated, plan, findings,
and ledger files remain read-only to preparation workers.

Workers cannot edit shared acceptance state. Each worker returns a patch for
its exclusive source, fixture directory, and listed verifier-subject set; the
proposed single corpus-row transition; focused command results; and any
semantic or write-set conflict. A worker cannot weaken owner, route,
disposition, typed outcome, or negative-policy evidence to make an index pass.
It cannot add a legacy-compatible branch, alternate title, permissive route,
or inferred fixture value.

A prepared package is not accepted evidence. The serial integration owner
reviews semantic and mechanical changes separately, applies packages only in
contiguous manifest order, writes each shared corpus and planning transition,
and runs every package's focused gates. Later packages may remain prepared
while an earlier manifest package is unresolved; they cannot be registered or
reported accepted ahead of it.

After a contiguous group is integrated, one complete-suite run may accept
every contiguous integrated package in that group. Until that run passes, the
packages remain implementation work with verification pending. A failure is
localized with package-focused gates and corrected in the owning package; it
cannot be bypassed by dropping a checker or preserving obsolete source prose.

Preparation wave `p1` is frozen in
`../../../../evaluation/standards-effectiveness/milestone-7-source-package-preparation.tsv`. Every listed source has exclusive
typed verifier subjects and the same semantic preservation obligations. A
subject is exactly `checker:<repository-path>` or `suite:<registered-id>`;
untyped and unknown subjects are invalid, and each subject is unique across the
preparation wave. Missing or symlinked checker paths and unknown suite IDs are
invalid.
Architecture remains excluded from preparation wave `p1` because its three
known mixed policy checkers inspect overlapping sections of one high-risk
source; it requires one separately frozen Architecture package before work may
begin.

## Historical Checker Repair

A completed historical checker may prove immutable row identity, package
identity, owner review, exact dispositions, bounded historical outcomes, and
the canonical routes established when that row was accepted. It cannot require
mutable source prose to retain a migration-era sentence after a later source
closure package supersedes that wording.

When such coupling is found, the preparation inventory assigns the checker to
one exclusive package before editing. Isolated repair preparation may proceed
concurrently with disjoint packages; serial integration removes only the
obsolete prose assertion before that source package is accepted. The repair
must preserve immutable train/package/validation evidence, semantic routes,
non-authority evidence, typed outcomes, and all transitive owner checks. A
negative self-scan prevents the historical checker from reclaiming the obsolete
source wording.

## Mixed Documentation Changelog Checker Repair

The complete-suite preflight for source package `7.4c3.4` found that
`verify-documentation-changelog-closure.sh` classified every level-two heading
as a policy section. That checker also owns exact changelog dispositions and
canonical Release workflow behavior, so it is mixed policy infrastructure and
cannot be edited by the Documentation source package.

Separate serial repair `7.4c3hdoc` removes the blanket heading and line-shape
assertions. It preserves all 16 exact changelog dispositions, canonical Release
metadata and rules, required Documentation workflow/recipe/Release routes, and
negative legacy changelog evidence. Explicit prohibited legacy policy headings
replace the blanket test, so a canonical navigation heading is not
misclassified as policy. Final title, complete heading set, and line bound are
owned by the aggregate source-closure engine when package `7.4c3.4` registers
the Documentation fixtures.

The repair cannot introduce dual old/new source assertions, exempt
Documentation from the aggregate engine, weaken Release semantics, or add a
source-specific fallback. The source and its pending fixtures remain unchanged
until the repair is accepted.

## Bounded Write Sets

Lifecycle repair `7.4c3v1r` may change only this re-plan, the final
source-closure planning checker, the active plan, and the execution ledger. It
cannot change standards, source indexes, fixtures, executable engine code,
corpus data, findings status, Router, dispositions, owner map, generated
inventories, metadata, configuration, or lockfiles.

Standing protocol slice `7.4c3s` may change only this re-plan, the final
source-closure planning checker, findings, the active plan, and the execution
ledger. It cannot change standards, former sources, source-specific checkers,
fixtures, engine code, corpus data, Router, dispositions, owner map, generated
inventories, metadata, configuration, or lockfiles.

Historical repair `7.4c3h41` may change only the row 41 historical checker,
this re-plan, the final source-closure planning checker, findings, the active
plan, and the execution ledger. It cannot change standards, former sources,
source-specific checkers, fixtures, engine code, corpus data, Router,
dispositions, owner map, generated inventories, metadata, configuration, or
lockfiles.

Mixed-checker repair `7.4c3hdoc` may change only the Documentation changelog
checker, this re-plan, the final source-closure planning checker, findings, the
active plan, and the execution ledger. It cannot change standards, former
sources, source-specific checkers, fixtures, engine code, corpus data, Router,
dispositions, owner map, generated inventories, metadata, configuration, or
lockfiles.

Concurrent preparation protocol `7.4c3p` may change only this re-plan, the
final source-closure planning checker, the preparation inventory and its
focused verifier, findings, the active plan, and the execution ledger. It
cannot change standards, former sources, source-specific or mixed policy
checkers, source fixtures, engine code, corpus data, Router, manifests,
dispositions, owner map, generated inventories, metadata, configuration, or
lockfiles.

Nested route repair `7.4c3rh` may change only the reusable closure engine, its
self-test verifier and fixtures, all currently registered source-closure route
fixtures, this re-plan, the final source-closure planning checker, F083 status,
the active plan, and the execution ledger. It cannot change standards, former
sources, corpus data, Router, manifests, dispositions, owner map, generated
inventories, metadata, configuration, or lockfiles.

Preparation workers are limited to the former source, isolated fixture
directory, and checker paths assigned to their inventory row. Their returned
patch excludes corpus, plan, findings, ledger, manifest, Router, aggregate,
engine, generated, metadata, configuration, and lockfiles. Only the serial
integration owner may combine a prepared patch with those package-owned shared
state transitions.

The `7.4c3v1` implementation slice may change only the reusable engine, engine
self-test fixtures and verifier, live aggregate verifier, existing Coding
closure verifier and fixture paths, F078 resolution status, active plan, and
execution ledger. Coding source text, corpus, manifest, dispositions, owner
map, Router, canonical owners, other former sources, generated inventories,
metadata, configuration, and lockfiles remain unchanged.

Each later source package may change only its former source, its corpus row, its
own new fixture directory, active plan, execution ledger, and one explicitly
identified source-specific checker when preflight proves that checker owns an
obsolete structural assertion. It cannot change the shared engine, another
source's fixtures or checker, canonical owners, Router, dispositions, owner map,
or generated inventories. If the engine cannot express a genuinely shared
invariant, or the checker is not source-specific, stop and re-plan a separate
infrastructure slice.

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

Standing protocol slice `7.4c3s` requires one successful focused invocation of
the final source-closure planning checker, shell syntax, and diff integrity. By
explicit user direction on 2026-08-06, the complete suite is skipped for this
planning-only shared-checker change; the exception is recorded in the active
plan and execution ledger. Source package `7.4c3.4` returns to its declared
verification gate unless separately authorized.

Historical repair `7.4c3h41` requires the focused row 41 checker, the final
source-closure planning checker, historical checker ownership, shell syntax,
diff integrity, and the complete suite because accepted historical verifier
behavior changes.

Mixed-checker repair `7.4c3hdoc` requires focused Documentation changelog and
final source-closure planning checks, historical checker ownership, shell
syntax, diff integrity, and the complete suite because a mixed policy checker
changes.

Concurrent preparation protocol `7.4c3p` requires the preparation inventory
verifier, final source-closure planning evidence, plan structure, shell syntax,
diff integrity, and the complete suite because shared migration procedure and
verification authority change.

Nested route repair `7.4c3rh` requires nested positive engine evidence,
negative old-schema, mismatch, escape, and absent-href evidence, the live
aggregate result for every registered source, final source-closure planning
evidence, plan structure, shell syntax, diff integrity, and the complete suite
because shared engine and fixture contracts change.

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
- a mutable checker cannot be assigned to one exclusive preparation package;
- concurrent packages require overlapping source, fixture, or checker writes;
- a prepared package would need to mutate shared acceptance state;
- manifest-contiguous serial integration cannot be preserved;
- removing obsolete structural wording would weaken semantic owner, route,
  disposition, typed-outcome, or negative evidence;
- fixture isolation cannot avoid overlapping draft write sets;
- replacing the Coding verifier weakens an accepted assertion;
- engine self-tests require a second parser or policy copy;
- generated artifacts must change before final `7.4c4`; or
- any package needs to change its canonical owner, immutable treatment, or
  objective.
