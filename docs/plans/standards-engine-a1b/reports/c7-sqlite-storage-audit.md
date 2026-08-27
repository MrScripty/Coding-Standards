# C7 SQLite Durable Storage Audit

**Status:** Focused design evidence; not planning admission

**Reviewed planning boundary:** commit
`9794b92708aad42c4838f9ad5c6b78e3984d73b3`, tree
`0f7bc73dcaf6c7cacf348c6f8de50ff5f41928c5`

**Related proposal:** [Candidate C7 design proposal](c7-design-proposal.md)

## Question

Can a gitignored SQLite database replace C6's Linux-ext4 direct-file object
Adapter while preserving immutable direct lookup, content identity, cold
reconstruction, and typed failure on the admitted Linux/ext4 target?

## Decision

Select SQLite as the C7 durable object-store direction on Linux x86-64 with a
local case-sensitive ext4 store, subject to exact runtime and required-real
evidence before admission.

SQLite stores canonical immutable envelope BLOBs and nothing domain-specific.
It does not replace Git-authored standards authority, owner codecs, canonical
identity bytes, direct dependency declarations, semantic validation, or
cross-machine export.

This audit replaces the one planned native immutable-file publication protocol
with SQLite. Other platforms and filesystems are future re-plan triggers, not
hypothetical implementations in A1b.

## Authority Boundary

| Concern | Owner |
| --- | --- |
| Markdown/TOML/schema/fixture/attestation meaning | Git-tracked authored artifact |
| Object semantic identity and payload | owning domain Module |
| Canonical envelope and direct dependency integrity | `standards_authority` |
| Transaction, locking, atomic publication, reopening | SQLite store Adapter |
| SQLite schema-v1 initialization and verification | `standards_authority` persistence Adapter |
| Database path and local-filesystem support | platform composition |
| Optional flattened closure or query acceleration | discardable cache |

Database bytes, page layout, row order, row IDs, SQLite release, journal files,
and transaction history are not semantic authority.

## Interface

The internal Adapter Interface is:

```python
class DurableObjectStore:
    def get(self, handle: AuthorityObjectId) -> StoredEnvelope: ...
    def put_if_absent(
        self,
        handle: AuthorityObjectId,
        envelope: bytes,
    ) -> PutResult: ...
```

`PutResult` is `inserted` or `existing-identical`. A conflicting existing row
is `IDENTITY.COLLISION`, not a third success result. SQL, cursors, connections,
transactions, paths, retries, and SQLite errors do not cross the Interface.

The Module does not initially expose enumeration, update, delete, garbage
collection, mutable aliases, latest heads, arbitrary queries, or cache APIs.

## Minimal Database Schema

```sql
PRAGMA application_id = 1397047601; -- 0x53454131, "SEA1"
PRAGMA user_version = 1;

CREATE TABLE authority_objects (
    handle TEXT COLLATE BINARY PRIMARY KEY,
    envelope BLOB NOT NULL,
    CHECK (typeof(handle) = 'text'),
    CHECK (typeof(envelope) = 'blob')
) WITHOUT ROWID;

CREATE TRIGGER authority_objects_no_update
BEFORE UPDATE ON authority_objects
BEGIN
    SELECT RAISE(ABORT, 'authority object rows are immutable');
END;

CREATE TRIGGER authority_objects_no_delete
BEFORE DELETE ON authority_objects
BEGIN
    SELECT RAISE(ABORT, 'authority object rows are immutable');
END;
```

The numeric application ID and user version above are frozen with the admitted
schema. They are the sole database-kind and schema-version authorities; no
metadata row repeats them. Authority validates the typed handle and envelope
kind before SQL and after every read. The BLOB contains the complete canonical
envelope.

No separate SQL dependency table is admitted initially. Traversal decodes the
stored envelope through the owner codec. Adding a dependency index later
requires measured need and must remain a verified discardable projection.

## Connection Profile

The simplest initial profile is rollback-journal mode rather than WAL:

```text
journal_mode = DELETE
synchronous = EXTRA
locking_mode = NORMAL
trusted_schema = OFF when supported by the selected runtime
extension loading = disabled
```

Reasons:

- the store is small and insert-only;
- one short writer transaction is sufficient;
- DELETE mode avoids a persistent WAL and shared-memory lifecycle;
- SQLite documents `synchronous=EXTRA` as adding directory synchronization
  after rollback-journal deletion; and
- performance evidence does not yet justify WAL complexity.

The Adapter verifies every selected pragma after setting it. An ignored,
changed, or unsupported required setting is `unsupported`.

WAL remains a measured future option. It is not an automatic fallback.

## Transaction Protocol

Python 3.11 and 3.12 compatibility uses `isolation_level=None` and explicit SQL
transactions rather than relying on version-dependent implicit behavior.

```text
1. Validate handle, envelope kind, and owner-produced identity before SQL.
2. BEGIN IMMEDIATE.
3. SELECT handle, envelope for the exact handle.
4. If absent, INSERT the exact row.
5. If present, compare the BLOB byte-for-byte.
6. Commit inserted or existing-identical success.
7. Roll back every exception.
8. Re-read and revalidate the published row before returning its handle.
```

SQLite permits one simultaneous writer. `BEGIN IMMEDIATE` makes contention
visible before any object mutation. The Adapter performs no application-level
retry loop.

The admitted busy timeout is 5000 milliseconds with no application retry.
Focused tests hold a competing write transaction past that bound and require
the exact `STORE.BUSY` `unavailable` outcome. Acceptance records measured
elapsed behavior on each required-real runtime. Timeout configuration is
execution behavior, not semantic identity.

## Publication And Interruption

One transaction publishes one immutable row. SQLite owns journal creation,
write ordering, commit, rollback, process-crash recovery, and platform VFS
synchronization.

Dependencies publish before dependents. Process termination may therefore
leave unreachable immutable rows, which are harmless. It cannot produce a
committed dependent whose required dependency row was absent when Authority
validated construction. Construction re-resolves dependencies inside the
publication operation before committing an aggregate root.

Required interruption evidence kills a child process:

- before `BEGIN IMMEDIATE`;
- after beginning but before insert;
- after insert but before commit;
- during commit through an injected test VFS or supported fault seam;
- immediately after commit before the caller receives success; and
- while another process reads or inserts the same handle.

Cold reopen must yield either no row or one complete valid row. Retry of the
same immutable put must converge to the same handle.

## Read And Corruption Behavior

`get(handle)` performs one primary-key lookup and then verifies:

- exact handle grammar;
- exact object kind;
- BLOB type and bounded size;
- canonical envelope decoding;
- owner codec membership;
- recomputed semantic identity;
- exact direct dependencies; and
- referenced dependency existence and kinds where the operation requires
  complete resolution.

Missing rows are `unavailable`. A malformed row, wrong kind, noncanonical BLOB,
hash contradiction, or SQLite corruption result is `invalid`. I/O, permission,
device, or temporary locking failures are `unavailable`. A newer well-formed
store schema or unsupported SQLite feature profile is `unsupported`.

The Adapter does not silently recreate or replace a corrupt database. Generated
authority may be rebuilt only through an explicit operator action that does not
discard irreplaceable analysis decisions.

## Schema Lifecycle

A1b owns only schema v1. Opening an absent store atomically creates that exact
schema. Opening an existing store verifies the SQLite header, application ID,
user version, table SQL, indexes, triggers, and required pragma profile. Any
other well-formed schema version is `unsupported`; malformed or contradictory
schema is `invalid`.

There is no migration framework, ordered migration catalog, dual reader, or
best-effort repair because no retained pre-A1b database exists. Discovering
retained state or requiring a schema change is a re-plan trigger.

## Primary References

- SQLite [atomic commit](https://www.sqlite.org/atomiccommit.html) defines the
  rollback-journal transaction and recovery model.
- SQLite [transaction control](https://www.sqlite.org/lang_transaction.html)
  defines `BEGIN IMMEDIATE`, one-writer behavior, and `SQLITE_BUSY`.
- SQLite [PRAGMA documentation](https://www.sqlite.org/pragma.html) defines
  `journal_mode`, `synchronous`, `application_id`, `user_version`, and
  integrity checks.
- SQLite [filesystem and corruption guidance](https://www.sqlite.org/howtocorrupt.html)
  records locking, synchronization, network-filesystem, and backup hazards.
- Python 3.12 [`sqlite3` documentation](https://docs.python.org/3.12/library/sqlite3.html)
  defines the selected standard-library Adapter surface and backup operation.

## Git And Repository Workflow

The database is local machine state and is excluded with all journal forms:

```gitignore
/.standards-engine/*.sqlite3
/.standards-engine/*.sqlite3-*
```

The exact final location follows the repository's existing ignore and state
directory conventions and must be decided before implementation. Generated
database files, dumps, journals, backups, and copied fixtures do not enter Git.

Git continues to own:

- authored standards and declarations;
- schemas and interface declarations;
- owner codec membership;
- deterministic fixtures and expected identities; and
- plans, ADRs, evidence, and attestations.

A clean checkout can recreate compiled objects. Analysis decisions that are
not derivable from Git remain durable immutable database objects and require
operational backup for disaster recovery.

## Backup

SQLite's backup API may support operator backup while the database is open.
It is operational storage backup, not a semantic interchange format and not a
Git artifact.

The A1b public facade exposes no export/import because no cross-machine
consumer is inventoried. Cold-process reconstruction on the same store remains
required. A future semantic-transfer consumer is a re-plan trigger.

## Store Root And Threat Model

The store path is trusted application configuration, not caller input. The
database resides in a private local application-state directory. The platform
composition layer must establish:

- the directory is owned by the current principal;
- other principals cannot write it;
- the final database path is not a symlink redirection;
- the volume is the admitted local case-sensitive ext4 filesystem; and
- opening and reopening resolve the same platform object identity.

The threat model excludes a malicious process running as the same principal,
which can alter any user-writable database or replace the executing code. It
does not exclude another principal racing a writable parent or redirecting an
unverified path.

SQLite reduces publication mechanics but does not eliminate store-root
security or filesystem capability evidence.

## Linux/ext4 Platform Contract

Required evidence covers CPython 3.11 and 3.12 on Linux x86-64 and local
case-sensitive ext4. Runtime admission is capability-based rather than tied to
an implementation-preserving SQLite patch release: SQLite must be at least
3.31.0, report `THREADSAFE=1`, expose Python `sqlite3.threadsafety == 3`,
accept and return the exact required pragma values, support the backup API, and
pass the complete transaction, interruption, integrity, and cold-reopen suite.
The acceptance report records each exact tested CPython and SQLite release and
compile-option set. The platform layer uses native ownership, permission, path
identity, mount identity, and filesystem-type facts. C6's hard-link publication
protocol is deleted rather than retained behind SQLite. Platform facts never
enter semantic object identity.

Network, removable, remotely synchronized, overlay, and unknown filesystems
are unsupported. SQLite depends on correct filesystem locking and
synchronization; application-level agreement cannot prove an unknown VFS.
macOS, Windows, another architecture or filesystem, and casefolded or
cross-mount ext4 are re-plan triggers.

## Dependency And Distribution Effects

Python's `sqlite3` standard-library Module introduces no separately installed
Python package. The actual SQLite library version and compile options vary by
Python distribution and target, so the supported runtime contract must record
and verify:

- Python implementation and version;
- SQLite runtime version;
- required compile options and available pragmas;
- thread-safety mode;
- selected platform and architecture; and
- the complete existing `jsonschema`/`referencing` wheel lock for that target.

SQLite runtime differences are support facts, not semantic identity inputs.
Freezing an exact SQLite release would incorrectly make a shared implementation
release into compatibility authority. An implementation-preserving runtime
update remains supported only when it satisfies the same capability profile and
reproduces identical stored objects and handles.

The private store root is explicit composition configuration, not an
environment-derived default or identity input. The Linux Adapter opens the
absolute root component-by-component from a retained `/` descriptor with
no-follow semantics, requires ownership by the effective user and mode
`0700`, and creates or verifies a regular `0600` database on the same mount.
It matches `fstat` device identity to one `/proc/self/mountinfo` record,
requires `ext4` and a writable local mount, and rejects the ext4 casefold flag
on every retained directory. Alias, symlink, cross-mount, network, removable,
overlay, unknown, or contradictory facts are typed `unsupported` or
`invalid`; path observations never enter semantic identity.

## Verification Matrix

| Claim | Evidence |
| --- | --- |
| Exact row identity | insert, same-handle same-bytes, same-handle different bytes |
| Immutability | public Interface has no mutation; SQL update/delete triggers reject |
| Atomicity | deterministic child-process termination around transaction stages |
| Concurrency | two readers, reader/writer, same-object writers, conflicting writers, busy expiry |
| Cold reconstruction | new process with only database path, codec sets, and handle |
| Corruption ownership | row BLOB/kind mutation, truncated database copy, malformed schema |
| Schema | exact schema-v1 initialization and verification; other versions reject |
| No semantic leakage | DB path, row insertion order, page size, VACUUM, backup, and SQLite release do not change handles |
| Local-filesystem requirement | real case-sensitive ext4 check; network/unknown negative |
| Direct lookup | every public handle resolves by primary key without scans or owner maps |
| Rebuild versus retention | generated objects rebuild; non-derivable decisions survive reopen and backup |

No in-memory database can satisfy durable publication evidence. Mocked platform
facts cannot satisfy real filesystem claims. Repeated success is not a crash
oracle without deterministic interruption points.

## Local Feasibility Prototype

A disposable, uncommitted prototype ran on the current Linux host with CPython
3.12.3 and SQLite 3.45.1. It used a temporary local database, DELETE journal
mode, EXTRA synchronization, explicit transactions, the proposed object table,
and immutable-row triggers.

The prototype observed:

- exact application ID and user version survived cold reopen;
- update and delete statements reached and were rejected by their intended
  triggers;
- process termination after insert but before commit left no row;
- process termination after commit left one complete row;
- cold `integrity_check` returned `ok` after both interruption cases;
- concurrent same-handle/same-BLOB writers converged to inserted plus
  existing-identical outcomes;
- a same-handle/different-BLOB writer reached collision handling; and
- expiry of a deliberately short lock wait produced `SQLITE_BUSY` before
  mutation.

This proves only that the proposed transaction shape is executable on the
observed host. It does not prove power-loss durability, SQLite implementation
conformance, a final busy bound, source capture, filesystem-family detection,
another Python build, or any required-real acceptance claim.
The prototype created no repository file and is not production code.

## Comparison With C6 Direct Files

| Concern | C6 | C7 SQLite |
| --- | --- | --- |
| Object lookup | path derived from kind and digest | primary-key lookup |
| Publication | staging file plus hard link | transaction insert |
| Writer coordination | application `flock` | SQLite transaction lock |
| Crash recovery | staging cleanup and retry | rollback journal and retry |
| Durability | file/directory `fsync` sequence | selected SQLite VFS and synchronous profile |
| Platform support | Linux ext4 only | Linux ext4 through SQLite's VFS |
| Immutable collision | compare existing file | compare existing row BLOB |
| Schema lifecycle | directory/envelope format replacement | exact schema v1; other versions unsupported |
| Git interaction | object files must be ignored | database and journals ignored |
| Domain authority | owner envelope codecs | unchanged owner envelope codecs |

SQLite removes substantial application-owned persistence implementation. It
adds a database schema and runtime capability contract, but that contract is
smaller and more cohesive than the native publication protocol it replaces.

## Findings And Closed Decisions

### Accepted direction

- Use SQLite as the sole initial durable object-store implementation.
- Store complete canonical envelopes as BLOBs keyed by handles.
- Keep authored authority as text in Git.
- Admit exactly schema v1 with no migration or semantic-transfer framework.
- Use DELETE journal mode and EXTRA synchronization initially.
- Use explicit `BEGIN IMMEDIATE` transactions.
- Keep rows immutable and omit mutable heads, dependency indexes, and caches.
- Keep semantic identity platform neutral.

### Closed planning decisions

1. Application ID is `1397047601` and schema version is `1`.
2. Busy timeout is 5000 milliseconds with no application retry.
3. Runtime admission uses the exact capability profile above; acceptance
   records exact tested releases rather than making patch releases semantic.
4. Local ext4 and private-root detection use the descriptor, mountinfo,
   ownership, permission, mount, and casefold checks above.
5. Deterministic crash evidence for DELETE/EXTRA is an implementation gate.
6. Dependency, licensing, persistence, security, cross-platform,
   policy-impact, and coverage projections are cutover obligations.

## Re-Plan Triggers

Re-plan if:

- SQLite cannot satisfy atomic durable local publication on a required target;
- a required store is on a network or unknown filesystem;
- domain queries over payload fields are required inside SQL;
- a mutable latest-state pointer, deletion, or garbage collection becomes
  required;
- database schema migration must reinterpret canonical envelope meaning;
- database bytes or SQLite versions must enter semantic identity;
- a schema migration or semantic export/import consumer becomes necessary;
- macOS, Windows, another architecture/filesystem, or casefolded/cross-mount
  ext4 becomes required;
- a required object exceeds bounded BLOB storage assumptions;
- direct lookup requires a scan or owner map;
- an external consumer requires committed database files; or
- source capture is incorrectly assumed solved by SQLite storage.

## Conclusion

SQLite is the simpler maintainable durable-store design for C7. It preserves
Git's strength for authored text, removes application-owned publication logic,
and keeps domain authority outside SQL. Its planning contracts are closed;
implementation remains blocked until the complete C7 content receives
independent admission.
