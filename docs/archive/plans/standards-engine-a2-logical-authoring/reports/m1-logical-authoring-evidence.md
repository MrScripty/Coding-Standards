# Milestone 1 Logical Authoring Evidence

**Status:** `Accepted`

## Outcome

The public Standards Engine Interface now accepts one atomic, cumulative
`StandardsChangeSet` expressed in canonical standards-domain IDs and authored
content. Callers no longer provide repository paths, complete serialized
files, SQL, Git identities, or representation-specific metadata envelopes.

The existing Authoring operations, immutable proposal aggregate, A1c compile
and Analysis path, Snapshot store, generated facade, and typed outcome model
remain the composition. One private fixed-authority compiler owns physical
projection. Milestone 1 does not change the canonical Git ref: local
application and proposal-specific commits remain Milestone 2.

## Implemented Contract

`create_proposal` and `revise_proposal` accept a normalized change set with one
explicit purpose and one or more closed logical edits. The supported edit
families are:

- create or revise a standard;
- revise, move, or retire a registered policy unit;
- retire a standard with explicit relationship dispositions;
- replace one standard's exact `Requires` and `Specializes` sets; and
- put or remove one fully specified policy-impact relationship.

Input order is normalized, duplicate logical facet writes reject, and revision
identity binds the complete cumulative logical program, exact base Snapshot,
exact base-revision repository path observation, proposal ordinal, and
Authoring contract v2. Proposal-head compare-and-swap, immutable historical
query, and cold SQLite replay remain enforced.

## Engine-Owned Projection

The compiler resolves IDs and authoring target handles against captured
authority, then mechanically updates only current fixed representations:

- standards Markdown and its metadata envelope;
- canonical corpus membership;
- policy-unit registry and module sidecars;
- policy-impact registry and declaration files; and
- generated suite-input projection, including topology and repository-index
  identity, through the canonical suite-input generator.

The resulting captured content is compiled through the existing metadata,
policy-unit, policy-impact, graph, Router, coverage, repository-coverage, and
A1c owners. No caller-owned persistence/repository path, second graph, second
parser, second analyzer, generic document AST, writer registry, or inferred
semantic relationship was added.

## A1c Integration Correction

Policy relationship changes retain their exact unchanged source-policy seed so
the existing A1c classifier can compare the relationship graph. Standard-level
relationship and whole-standard changes use a truthful `module` change kind
with exact accepted/proposed module IDs and no policy-unit IDs. This also
supports standards with no registered policy units and avoids inventing an
arbitrary policy owner.

Adding that closed A1c variant advances the Analysis request contract to v5
and result/persisted-state projection to v6 within the coordinated public
Interface v20 cutover. Handle schema v5 and Snapshot store schema v2 remain
unchanged. Unsupported retained Analysis state continues to fail with a typed
diagnostic.

## Verification

The following evidence exercises the production implementation rather than a
prototype:

- public create, focused revision, relationship reorganization, placement,
  retirement, exact revision query, A1c analysis, stale-head rejection, and
  cold-reopen workflows;
- deterministic identity under reordered edits and typed invalid, conflicting,
  missing-semantic, dangling, cyclic, and unsupported inputs;
- exact create/remove suite-input bytes compared with the canonical generator,
  including the proposed repository path observation;
- exact Git commit-tree path observation for Snapshot source revisions;
- generated schema, facade, example, and Python projection agreement;
- full `standards_analysis`, `standards_contracts`, and Standards Engine test
  suites plus focused Repository Git and canonical suite-input verifier suites
  on the supported Linux CPython 3.11 and 3.12 runtimes;
- the complete standards checkpoint; and
- an independent read-only specification and routed-standards audit with no
  actionable blocker.

The final source-equality guard was separately exercised through the public
no-policy-module, policy-relationship, whole-standard, and SQLite cold-replay
workflow after all implementation corrections.

## Acceptance Mapping

- **LA-A1:** satisfied. The generated public contract contains domain intent
  and opaque handles, not repository representation.
- **LA-A2 through analysis:** satisfied. All admitted logical operations are
  queryable and analyzable after process replacement.
- **LA-A3:** satisfied. Mechanical projection is complete and semantics remain
  explicit.
- **LA-A5 through LA-A7 proposal/replay portion:** satisfied. The implementation
  reuses A1c/A2 owners, preserves typed atomic failures and immutable replay,
  and passes both supported runtimes.

LA-A4 and the application/publication portions of LA-A5 through LA-A7 remain
open for Milestone 2. No claim in this report treats proposal compilation as
canonical application.

## Proportionality And Simplicity Result

The implementation follows the Milestone 0 admission. The one material review
finding was resolved at the existing owners because it threatened correctness:
Repository Git observes exact base paths, the suite-input generator remains
canonical, and A1c owns its new exact change variant. Investigation stopped
when the named public workflows and canonical equality tests passed. No
adjacent uncertainty, runtime measurement framework, compatibility layer,
background mechanism, or remote publication path was admitted.
