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

class StoreRecovery:
    def backup(self, source: StoreLocation, absent_destination: StoreLocation) -> BackupReceipt: ...
    def restore(self, backup: StoreLocation, absent_destination: StoreLocation) -> RestoreReceipt: ...
```

`PutResult` is `inserted` or `existing-identical`. A conflicting existing row
is `IDENTITY.COLLISION`, not a third success result. SQL, cursors, connections,
transactions, paths, retries, and SQLite errors do not cross the Interface.
Recovery locations are trusted operator/composition inputs, not public A1
request values. Backup and restore receipts report verified source and
destination fingerprints but are operational results, not authority objects.

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

The BLOB contract is authority envelope kind `authority-envelope`, version `1`.
Its bytes are exactly the identity-v2 canonical typed encoding, without the
identity hash frame, of a closed seven-field object: constant
`envelope_kind`, integer `envelope_version`, `object_kind`, `semantic_id`,
sorted unique `direct_dependencies`, `payload_contract`, and `payload`.
Dependency references contain exactly `object_kind` and `semantic_id`.
`object_kind` and `payload_contract` are nonempty opaque Unicode-scalar strings
owned by the injected codec sets; Authority compares them exactly and does not
parse semantic meaning from them. The payload is an identity-v2
JSON-compatible typed value; owners project raw bytes through closed
padded-Base64 fields and verify the decoded value. Unknown fields, floats,
noncanonical strings or numbers, duplicate or unsorted dependencies, and
encoded envelopes above 67,108,864 bytes reject before SQL. The bound is
verified before allocation and again from SQLite BLOB length before decoding.
A well-typed unknown envelope kind or positive version is `unsupported`;
malformed structure is `invalid`.

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
- during commit by running the otherwise-real Adapter under a capability-checked
  Linux `strace` syscall-injection harness that delivers `SIGKILL` at the first
  selected `fsync` or `fdatasync` reached after the child signals its exact
  pre-commit barrier;
- immediately after commit before the caller receives success; and
- while another process reads or inserts the same handle.

Cold reopen must yield either no row or one complete valid row. Retry of the
same immutable put must converge to the same handle.

The harness is test-only and changes no production Adapter or SQLite library.
It must prove from the trace that the selected synchronization syscall was
reached and injected; a timeout, repeated probabilistic kill, kill before the
barrier, or ordinary child failure is not evidence. Required-real admission
probes `strace` support for `--inject`, signal delivery, `fsync`, and
`fdatasync`, records the exact tool release, and returns `unsupported` for an
environment without that oracle. This avoids a custom VFS and keeps SQLite's
transaction implementation owned by SQLite.

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

The default live store is exactly
`<repository-root>/.standards-engine/authority.sqlite3`. Engine composition may
instead inject one explicit absolute `StoreLocation` for an operationally
restored store; the path remains trusted configuration and does not enter
semantic identity. Generated database files, dumps, journals, backups, and
copied fixtures do not enter Git.

Git continues to own:

- authored standards and declarations;
- schemas and interface declarations;
- owner codec membership;
- deterministic fixtures and expected identities; and
- plans, ADRs, evidence, and attestations.

A clean checkout can recreate compiled objects. Analysis decisions that are
not derivable from Git remain durable immutable database objects and require
operational backup for disaster recovery.

## Backup And Restore

Backup uses SQLite's backup API against the configured live store and an
explicit absent destination on the admitted private ext4 profile. It creates no
overwrite, rotation, or deletion authority. After backup completion, Authority
opens the destination independently, verifies the exact schema/profile,
`integrity_check`, every envelope bound and canonical encoding, every
owner-recomputed identity, every dependency, and every root closure, then
returns a receipt. Verification failure removes only the unpublished
destination or retains it under an explicitly selected diagnostic location;
the live source is unchanged.

Restore is offline and non-overwriting. Authority opens an explicit backup
read-only, performs the same complete verification, and uses SQLite backup to
materialize a distinct absent destination store. It then cold-reopens and
reverifies that destination before returning a receipt. A new Engine instance
may select the verified destination through its trusted `StoreLocation`; the
former configured store is never changed and remains the rollback selection.
An existing destination, in-use destination, source/destination alias, or
cross-mount destination rejects before mutation. A failed restore removes or
quarantines only its unpublished destination and cannot alter either source or
configured live store.

Authority never expires, rotates, overwrites, or deletes backups or former live
stores. The operator owns backup media, retention count, retention duration,
and the later explicit deletion of operational files. A1b's responsibility is
verified creation and non-destructive restoration. The A1 public facade exposes
no semantic export/import because no cross-machine consumer is inventoried.
Cold-process reconstruction from the selected restored store remains required.
A semantic-transfer consumer or in-place destructive restore is a re-plan
trigger.

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

The repository-local default or explicitly restored store root is resolved by
trusted composition, not environment lookup or public request input, and never
enters identity. The Linux Adapter opens the
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
| Atomicity | deterministic child-process termination around application stages plus capability-checked `strace` injection at the real SQLite synchronization syscall reached during commit |
| Concurrency | two readers, reader/writer, same-object writers, conflicting writers, busy expiry |
| Cold reconstruction | new process with only database path, codec sets, and handle |
| Corruption ownership | row BLOB/kind mutation, truncated database copy, malformed schema |
| Schema | exact schema-v1 initialization and verification; other versions reject |
| No semantic leakage | DB path, row insertion order, page size, VACUUM, backup, and SQLite release do not change handles |
| Local-filesystem requirement | real case-sensitive ext4 check; network/unknown negative |
| Direct lookup | every public handle resolves by primary key without scans or owner maps |
| Rebuild versus retention | generated objects rebuild; non-derivable decisions survive reopen, verified backup, offline restore to an absent destination, and cold selection of that destination |
| Recovery lifecycle | existing/aliased/in-use destination rejection, failed-restore isolation, source preservation, explicit restored-store selection, rollback to unchanged former store, and operator-owned retention |

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
5. Deterministic crash evidence uses the admitted Linux `strace` syscall
   injection capability against the real SQLite Adapter; a custom VFS,
   probabilistic kill, or application retry is not admitted.
6. Default live storage is
   `<repository-root>/.standards-engine/authority.sqlite3`; restore is offline,
   verified, non-overwriting, and publishes only by selecting a distinct store
   in a new Engine instance. Authority owns no backup retention or deletion.
7. Encoded authority envelopes are canonical identity-v2 typed bytes and are
   bounded at 67,108,864 bytes.
8. Dependency, licensing, persistence, security, cross-platform,
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
- in-place destructive restore, Engine-owned retention, or automatic backup
  deletion becomes necessary;
- the admitted Linux test environment cannot provide the exact syscall fault
  injection needed for deterministic during-commit evidence;
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
