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
