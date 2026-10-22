# Issues and Dispositions

| ID | Finding | Disposition | Owner | State |
| --- | --- | --- | --- | --- |
| F0 | Engine is 96.4% of verification; current log lacks per-test/setup attribution | Native unittest durations plus command/setup timing; unchanged passing baseline | CI owner, M0 | confirmed; instrumented on isolated candidate; hosted evidence pending |
| F1 | Repeated preparation and inconsistent full-tracked versus three-contract overlays | One test-owned material contract; measured scoped reuse only | Fixture owner, M1 | confirmed; planned |
| F2 | Pure packet checks inherit nine Git setup commands | Separate lightweight and real-Git fixtures; split mixed tests by claim | Packet test owner, M2 | confirmed; planned |
| F3 | Full repository/preview/apply verification duplicated in publication scenarios | Map evidence; substitute only redundant preview boundary; preserve real preview and apply | Publication test owner, M2 | confirmed; planned |
| F4 | Manual full TestCase replay and borrowed lifecycle for warm caches | Ordinary fixture actions, direct warm-cache assertions, retained unique claims | Publication/cache test owner, M2 | confirmed; planned |
| F5 | Recovery repeatedly builds admitted publication state | Profile setup; preserve fresh isolated state and existing verifier substitute | Recovery test owner, M2 | measured contribution pending |
| F6 | Routing scenarios reload unchanged modules/projection | Explicit immutable scope; keep mutation/replay loaders fresh | Analysis test owner, M2 | confirmed; low local and hosted cost |
| F7 | Coverage assertions can be skipped; two digest checks accept any sha256 prefix | Controlled required coverage and independent exact digests | Oracle owner, M0 | confirmed; repaired on isolated candidate; focused checks passed |
| F8 | Compiler main guard precedes OperationVariantTest | Move guard to bottom and qualify both entrypoints | Contracts test owner, M0 | confirmed; repaired on isolated candidate; direct and discovery checks passed |
| B1 | Failed main run is not a green timing baseline | Use successful comparable workload; retain failed run only as historical evidence | CI owner | resolved in plan design |
| B2 | Review environment differs from supported locked runtime | Local observations remain diagnostic; qualify candidate in hosted Python 3.12 | CI owner, M3 | acceptance pending |
| B3 | A1 has its own review/acceptance/integration state | Recheck source and resolve overlaps; preserve separate gates | Maintainer | integration condition |
| D1 | A fixture pool or broad hardlink/alternate optimization may add risk with little gain | Excluded absent a measured owned need and new design decision | Fixture owner | deferred mechanism |
| D2 | Sharding or production optimization may still be required | Revisit only the measured residual after duplication reduction | Maintainer | deferred; not an initial task |

Issue closure requires the named evidence, not a smaller file count, a helper extraction, fewer tests, or a faster unrelated local subset.
