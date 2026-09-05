# Milestone 7 Source Closure

Date: 2026-09-05. Status: accepted for Milestone 7 and A2.
Source authority: `ff6f3b217b3bea945f53f7b68af9afe403dfbbf1`.
Comparison baseline: `c99773d8`.

## Published Boundary

The Engine navigation authoring capability (`c99773d8`) and declared-route
preservation (`a94bbcd2`) enabled two reviewed, verified Engine applications:

| Publication | Corrected legacy entrypoints |
| --- | --- |
| `67d3e205` | Interop, Accessibility, Architecture, Tooling, Launcher, Rust Async, Rust Interop, Rust Language Bindings, Rust Security |
| `ff6f3b21` | Coding |

Both applications used a fresh MCP stdio process and the existing proposal,
analysis, resolution, review, verification, and application lifecycle. Accepted
Engine reads match the reviewed content and canonical destinations for all ten
indexes. Snapshot and proposal handles differ by design. Checkout changes only
materialized the Engine-published commits; no standards source was hand-written.
No remote push was performed.

The final read-only audit compared exact source revisions and Engine previews.
All ten corrected bodies match their previews; the other seventeen bodies match
both their original Engine reads and baseline Git bytes. Together with the
[manual semantic review](milestone-7-semantic-ownership-review.md), these establish
navigation-only legacy entrypoints at this accepted boundary. All 70 canonical
module bodies remain byte-for-byte unchanged.

## Routing And Link Evidence

| Check | Result |
| --- | --- |
| Registered legacy population | 27, all reviewed |
| Corrected / retained unchanged | 10 / 17 |
| Canonical modules unchanged | 70 |
| Router rules with canonical destinations | 54 |
| Historical IDs reconciled | 916 |
| Local inline links checked | 197, all resolve |
| Heading fragments checked | 21, all resolve |

The historical check reconciles identifiers one-to-one with disposition/source
records and verifies named target files. Frozen baseline evidence remains
unchanged. It is separate from current canonical membership, routing, and source
inspection; it does not reclassify historical corpus records as current policy.

The first publication changed exactly four required-destination assertions:

- `tooling-ci-workflow-reference / former-source-destinations`
- `tooling-reference-recipes / former-source-destinations`
- `verification-ownership / tooling-route-and-legacy-removal-destinations`
- `contract-ownership / rust-binding-contract-authority-destinations`

The first three replace legacy Frontend with its canonical application profile.
The last replaces legacy Testing, Rust Cross-Platform, and Rust Interop with
canonical Verification, Rust Cross-Platform, and Rust Interop, deduplicating the
already selected Interop destination. All other suite assertions are unchanged.

The initial audit found one stale Coding fragment among 195 links and 24
fragments. That link targeted Core's removed Code And Terminology Discipline
heading and was **not** listed in the route inventory. Code Design owns the
material. Coding's seventeen other declared routes include seven section links.
The same rewrite operation now preserves those captured requirements for
explicitly selected canonical owners. The final Coding index selects fifteen
owners, including Code Design, and retains all seventeen declared routes.
The route inventory is byte-for-byte unchanged. Coding publication changed only
its source, the Engine-owned navigation catalog, and generated suite inputs.
The final link check covers the actual inline Markdown and heading syntax in
these sources; it is not a general Markdown parser certification.

## Ownership And Consumer Evidence

The D001–D010 review and source corrections resolve M7-OWN-01 through M7-OWN-04.
The revised closure procedure (`19764768`) and separate final reconciliation
resolve M7-OWN-05. Coding publication and the final link audit resolve M7-OWN-07.
M7-OWN-06 remains explicitly deferred to Milestone 8's A5 concision review.

Policy-impact inspection of forty selected owners returned 167 unique declared
edges, with no endpoint in the nine initially selected legacy sources. Thirty-three
owners had incomplete mappings. Additional Coding inspection found two Code
Design edges, to Architecture and Verification, and no Core edges; these were
unchanged. These results describe declared relationships, not complete semantic
consumer coverage. Bounded tracked Markdown inline-link scans found six incoming
links for the first nine sources, all within rewritten sources, and none for
Coding. Other reference forms and downstream repositories are outside that scan.

## Verification And Limits

- Fourteen navigation tests pass, including protected-section application,
  omitted-owner rejection, and unsupported artifact-route rejection.
- Fourteen focused MCP/replay tests pass, including fresh-process state inspection
  and snapshot closure rejection.
- Both protected-navigation tests pass again after the live Coding correction;
  fixtures supply their own obsolete input independently of current source text.
- Contract projection, Ruff, and skill validation passed for the implementation.
- Each published candidate passed all 73 suites and 121 structural checks. The
  final documentation checkpoint also passes all 73 suites and 121 checks.

The earlier implementation report records the broader Analysis and Engine test
runs and focused repairs; this report does not claim a new full Engine discovery
run. Structural checks do not certify universal prose conformance, downstream
policy effectiveness, or complete semantic mapping.

Milestone 7 and A2 are accepted. The overall plan remains active: Milestone 8
must provide scenario comparison, two independent downstream pilots (A3),
migration and standards-version guidance (A4), and final manual review including
prompt concision (A5). No pilots or effectiveness gains are claimed here.
The connected client's old MCP process needs a restart to load the new contract;
production authoring and verification used fresh processes successfully.
