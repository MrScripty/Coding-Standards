# A2 Current Consumer And State Inventory

**Observation date:** `2026-09-01`

**Admitted baseline:** `d9d5b56a622ba4ce77ac0feb37ac7e0b116b1d1e`

## Result

The bounded current repository contains the A1c implementation, generated
contract projections, package and contract tests, and the fresh-process
platform harness. It contains no non-test production registration or import of
`StandardsEngine`, no repository package entry point for `standards-engine`,
and no retained SQLite or database file. These are bounded repository results;
they do not prove that an external deployment or copied store does not exist.

The active Generic Standards Verification Engine migration has published
accepted state through M6-I113. Its generated evidence is fresh at 12 retained
Bash verifiers, 14 dependency nodes, 81 edges, and 14 components, but its plan
still requires a post-M6-I113 ownership audit before another migration package
is admitted. A2 therefore does not freeze future implementation-consumer or
coverage totals from this inventory.

## Bounded Search

| Population | Bounded method | Current result | Meaning |
| --- | --- | --- | --- |
| Runtime facade consumers | Search non-test Python, TOML, JSON, and shell sources for public imports, `StandardsEngine(`, and the package identity | No match outside the package implementation | No current-tree production runtime consumer found. External consumers remain undiscoverable here. |
| Package registration | Inspect `tools/standards_engine/pyproject.toml` | `repository-entrypoints = []` | The repository installs no command or registered tool entry point for A1c. |
| Public contract consumers | Inspect schema compiler, generated Python, generated agent-tool projection, examples, and contract tests | Present and active | These are coordinated repository-owned contract consumers, not evidence of an independently deployed runtime. |
| Behavioral consumers | Inspect `tools/standards_engine/tests` | Navigation, analysis, generated-contract, and fresh-process platform harness consumers are present | They decide tested behavior but do not create product demand or a compatibility promise. |
| Related package consumers | Search current packages | `standards_contracts`, `standards_identity`, `standards_analysis`, and `standards_metadata` tests read or validate A1c contract artifacts | Any public contract cutover must update and verify this coordinated test/projection closure. |
| Retained stores | Search tracked worktree files for `.sqlite3`, `.sqlite`, and `.db` excluding `.git` traversal | No match | No repository-retained A1c store requires migration. Copied or deployment-owned stores are outside the search boundary. |
| Default live-store path | Inspect the composition root and search the worktree | `.standards-engine/snapshots-v1.sqlite3`; path absent | The default is implementation behavior, not evidence that a current store exists. |
| Deployment/provider registration | Search non-test current-tree sources and inspect package manifest | No deployed harness or authorization-provider registration found | The test platform harness is the only executable repository example. Product direction still selects harness-managed calls. |
| Publication target | Inspect `repository_git` and the A1c composition root | Current configured repository `HEAD` is read authority; no write-capable Adapter exists | Milestone 0 must select one exact publication target and success postcondition before production planning. |
| Verification graph | Run the generated-artifact freshness check | Fresh: 12 Bash verifiers, 14 nodes, 81 edges, 14 components | Structural evidence is current, but the active migration plan still owns its next read-only audit and later mutations. |

## Current Public Contract

- Interface schema version: `12`.
- Request contract version: `4`.
- Result projection version: `4`.
- Public handle schema version: `5`.
- Operations: `create_snapshot`, `find_snapshots`, `delete_snapshot`,
  `undelete_snapshot`, `query`, `prepare`, `resolve`, and `inspect`.
- The schema is the sole public shape authority. The interface manifest owns
  operation roots, results, capabilities, and independent compatibility
  versions; generated Python and agent-tool JSON are disposable projections.
- Unsupported well-formed compatibility keys are typed `unsupported`; there
  is no prior-version reader or fallback.

The current `query` operation accepts only a `SnapshotHandle`. The current
analysis request accepts a base and proposed `SnapshotHandle`. A proposal
revision is not accepted canonical snapshot authority, so A2 cannot pass a
proposal revision through either field by reinterpretation.

## Current Durable State

The default store is one SQLite Snapshot Module with application ID
`0x43534131`, schema user version `1`, and a 5000 ms busy timeout. Its exact
schema owns:

- immutable content sets and content files;
- unique snapshot roots with active or quarantined lifecycle;
- immutable aggregate records and exact snapshot dependencies;
- derived child inspection indexes; and
- purged-root tombstones.

Triggers prevent mutation of content, aggregate records, dependencies, and
child indexes. Root deletion first deletes every dependent aggregate record.
Open rejects a wrong application ID, a newer version as `unsupported`, any
other version as `invalid`, and any non-exact schema. No migration mechanism or
compatibility reader exists.

## Compatibility And Release Consequences

The current-tree evidence would permit a coordinated repository-owned public
contract replacement because every discovered public projection and test
consumer is jointly controlled. It does not authorize that selection:

1. A1c explicitly defers cross-engine stored-state compatibility until feature
   completeness.
2. This inventory cannot discover copied stores or external Python consumers.
3. The product owner has not yet selected A2 as the feature-completeness
   trigger or promised an overlap window.

Therefore the current disposition is `decision-pending`, not “migration not
needed.” If the product owner selects feature completeness with A2 and confirms
no supported external overlap, one coordinated replacement plus typed stale-
state rejection is the minimal candidate. A real supported retained consumer
would instead require a bounded migration or compatibility contract with an
owner and retirement trigger.

## Reproduction Boundary

The inventory used read-only current-tree searches, package and schema
inspection, a tracked database-file search, the current generated-artifact
check, and the accepted A1c fresh-process tests as behavioral evidence. It did
not inspect user home directories, deployment machines, unpublished packages,
or external registries. Those boundaries are deliberate and must not be
reported as empty populations.
