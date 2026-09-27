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
