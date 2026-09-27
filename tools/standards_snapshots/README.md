# Standards Snapshots

`standards_snapshots` owns immutable captured content, independently retained
opaque snapshot roots, SQLite persistence, discovery, quarantine, undelete,
expiry, transactional purge, opaque aggregate records, snapshot-dependent
aggregate heads, and derived child inspection.

The package accepts already captured logical paths and exact bytes. It does not
read repositories, invoke Git, parse standards, understand analysis payloads,
or expose content identity. Equal-content roots share internal storage while
retaining independent IDs and lifecycle. `load_content` reconstructs and
revalidates the exact captured path-byte set without exposing its deduplication
key.

Deleting a root quarantines the complete dependent aggregate, including its
discoverable heads, for seven days by
default. Undelete restores it before expiry. Later maintenance purges the root,
every aggregate depending on it, and derived child indexes in one transaction;
shared content remains until its final root is purged. Store schema v2 adds
aggregate heads; opening a valid v1 store performs the one supported atomic
v1-to-v2 migration and then operates only as v2. The migration requires the
exact accepted v1 schema and passing SQLite integrity/foreign-key checks,
preserves every A1c row family, and rolls back an interrupted transition.
Aggregate discovery uses a consistent read and durable insertion sequence.
Existing files are authenticated before persistent SQLite configuration;
failed opens close resources, and failed first initialization removes its
exact owned staging file.
Closed SQLite files are the administrative movement unit. Minimal
aggregate-root tombstones prevent an expired proposal identity from aliasing
later state. Backup, restore, import, export, merge, open-ended migration
machinery, immediate purge, and child deletion are outside the Interface.

## Selected database path

`SnapshotModule.open` requires an absolute Path and admits an existing final component
only when it is a regular non-symlink file. Intermediate directory symlinks are
permitted by this local operator-owned storage profile. The Engine's convenience
entry point resolves the selected parent (relative parents are cwd-relative), then
passes the final name unchanged to the store. Invalid selection never authorizes
replacement or deletion of an existing database. These admission checks are not a
race-free filesystem sandbox.

## Exact identity proof reuse

`load_content` accepts an optional trusted `ContentIdentityReuse` owner. Every call
still performs maintenance, reloads actual content and runs the existing per-file
checks. The reuse owner receives that complete capture and the Snapshot-owned codec;
its contract requires the identical computed content ID, not a cached caller claim.
Snapshot compares it with the currently loaded stored ID on every call. Omission
keeps standalone behavior cold. The Engine uses its existing scoped, bounded process
cache; roots, lifecycle, authority and response values are never identity-cache data.
No identity domain, store format or persisted representation changes.

## Admission and maintenance work

Each open of an existing current-schema database authenticates the application,
exact schema, and complete SQLite integrity/foreign-key state **before** persistent
configuration. Configuration is followed by the existing exact schema check. The
same full audit is not repeated for a store admitted at the current schema version.
This is a point-in-time audit on every open, not cached proof that the database can
never change. Selected content and aggregate reads retain their ordinary checks.

New initialization keeps its final integrity audit and owned-file cleanup on failure.
A store admitted as v1 keeps the pre-configuration audit, transaction-guarded
pre/post-migration audits, and final destination audit. The final audit also applies
when another opener finishes migration before this opener prepares the schema.
No integrity policy, SQLite profile, supported migration or stored format changes.

Maintenance remains synchronous at the same module call sites. It first performs a
short-lived existence read for quarantined roots whose deadline is at or before the
supplied time. No work means no maintenance writer transaction. The probe cursor is
closed before acquiring a writer; a positive probe only justifies acquiring the slot.
The existing transaction then re-selects the current due rows and atomically purges
roots and dependent aggregates/heads/children, and records tombstones according to
the schema.
Concurrent undelete, re-quarantine or purge cannot be overridden using stale probe data.

Nothing is cached about whether maintenance is due. A later observation sees newly
due work. When purge really is required, contention still returns the ordinary BUSY
outcome; callers do not receive success after a failed purge. Active reads can coexist
with another RESERVED writer when no purge is due, but EXCLUSIVE locks, configuration
changes, actual maintenance and other SQLite constraints can still block them. This
is not a general lock-free or read-only-filesystem guarantee.
