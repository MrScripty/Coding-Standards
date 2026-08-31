# A1c Dependency And Version Decisions

## Repository Git Implementation Decision

### Requirement

Snapshot capture and repository verification require exact reads from one Git
commit, bounded subprocess output, sanitized execution, SHA-1 and SHA-256 object
identity verification, regular-file classification, UTF-8 repository paths, and
explicit traversal into configured gitlinks. The Adapter must return owned
`invalid`, `unsupported`, and `unavailable` outcomes and must not introduce
standards, snapshot, or analysis semantics.

### Candidates

| Candidate | Fit | Continuing cost | Decision |
| --- | --- | --- | --- |
| Git executable plus the current bounded Adapter | Git owns object lookup and type reporting; the Adapter verifies returned object identity and parses only the commit tree reference and raw tree-entry framing needed for exact configured traversal | Maintain the bounded framing subset and track Git object-format changes | selected |
| More Git CLI projections such as repeated `ls-tree` calls | Delegates tree framing but adds pathspec/quoting behavior, more subprocess transitions, and a separate reconciliation path for configured gitlinks and independently verified object bytes | Maintain command-output parsing and traversal reconciliation | rejected; not a smaller proof boundary for the selected contract |
| Dulwich | Supplies a mature pure-Python repository implementation and broader object semantics | Adds a runtime dependency and a second repository implementation beside the required Git executable; migration and security-update ownership exceed the current bounded subset | rejected for the current contract; reconsider if local semantic surface expands |
| pygit2/libgit2 | Supplies mature object traversal and repository semantics | Adds native provisioning, ABI, target, and release obligations not required by the current Python library deployment | rejected for the current contract |

The selected code is not a local implementation of Git as a whole. Git remains
the established semantics owner for object resolution and reported object type.
`repository_git` is a thin validation and policy Adapter over exact returned
objects. Its local subset is limited to two stable binary/text framings:

- the leading `tree` field of a commit object; and
- mode, name, and object ID entries in a tree object.

The Adapter independently verifies object hashes because exact immutable bytes
are the snapshot authority, not merely a successful subprocess result. Existing
tests cover malformed framing, type mismatch, hash mismatch, unsupported modes,
UTF-8 paths, hostile environment variables, bounds, and mapped gitlinks.

Re-evaluate this decision if the package adds revision expression semantics,
attributes, filters, sparse checkout, alternates, signatures, ref mutation,
index mutation, non-UTF-8 paths, another object format, or enough local Git
semantics that the bounded framing subset is no longer the smaller owner.

## Version Role Matrix

| Value | Role | Changes when | Consequence |
| --- | --- | --- | --- |
| Public interface schema `12` | Current-format discriminator for the complete agent facade | Operation membership or the top-level public operation contract changes incompatibly | Older interfaces are unsupported; no overlap reader is promised |
| Request contract `4` | Compatibility version for request meanings | A supported request's interpretation changes incompatibly | Requests using another version are unsupported |
| Result projection `4` | Compatibility version for result meanings | A supported result's observable meaning changes incompatibly | Consumers must use the matching result contract |
| Public handle schema `5` | Current-format discriminator for serialized opaque handles | Handle representation or resolution contract changes incompatibly | Other well-formed handle versions are unsupported |
| AnalysisState contract `4` | Persisted current-format discriminator and compatibility version | Stored field closure or reconstruction invariants change incompatibly | A well-formed other version is unsupported; malformed current state is invalid |
| Analysis identity domain `coding-standards:analysis:v5` | Identity-domain revision | Identity material, equality, framing, or semantic invalidation rules change | Equal logical inputs under another domain do not share identity |
| SQLite `user_version = 1` | Store current-format discriminator | Durable table/transaction representation changes incompatibly | Unknown well-formed versions are unsupported; contradictory stores are invalid |
| Snapshot root prefix `snapshot:v1` | Allocation-format discriminator | Opaque root textual representation changes | The new representation is a distinct handle format; content equality remains separate |

No value is an implementation release or umbrella build version. Values may
advance independently. The current repository promises no simultaneous reader
overlap or migration matrix for prior unreleased engine stores, so a compatibility
matrix or migration framework would add no current consumer value.

## Validation Proof Boundary

The generated decoder validates an incoming operation value once against the
canonical Draft 2020-12 schema and constructs frozen generated models without
revalidating each nested model. Direct model construction remains a separate
smart-constructor boundary and performs complete validation.

Engine results are already proof-bearing generated values. The facade checks
their exact generated class against the schema-derived operation result algebra
and serializes them; it does not discard that proof and validate the same value
again. A caller receiving the serialized mapping establishes its own proof at
that new trust or process boundary.
