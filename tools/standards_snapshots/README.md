# Standards Snapshots

`standards_snapshots` owns immutable captured content, independently retained
opaque snapshot roots, SQLite persistence, discovery, quarantine, undelete,
expiry, transactional purge, opaque aggregate records, and derived child
inspection.

The package accepts already captured logical paths and exact bytes. It does not
read repositories, invoke Git, parse standards, understand analysis payloads,
or expose content identity. Equal-content roots share internal storage while
retaining independent IDs and lifecycle. `load_content` reconstructs and
revalidates the exact captured path-byte set without exposing its deduplication
key.

Deleting a root quarantines the complete dependent aggregate for seven days by
default. Undelete restores it before expiry. Later maintenance purges the root,
every aggregate depending on it, and derived child indexes in one transaction;
shared content remains until its final root is purged. Closed SQLite files are
the administrative movement unit. Backup, restore, import, export, merge,
migration, immediate purge, and child deletion are outside the Interface.
