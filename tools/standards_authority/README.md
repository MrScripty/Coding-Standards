# Standards Authority

`standards_authority` stores immutable, content-addressed authority objects and
captures exact repository leaf content. It owns envelope integrity, dependency
closure, transactional persistence, and capture mechanics. Injected owner
codecs retain semantic identity and payload meaning.

The durable adapter stores only a canonical envelope BLOB under its typed
handle. It exposes direct lookup and put-if-absent, with no update, delete,
enumeration, mutable head, or semantic query interface.

`ContentSnapshot` contains only sorted logical Unicode-scalar paths and exact
bytes. Git and native capture observations are discarded after validation.
`ExecutionClosure` stores qualified roots and binds the dependency set derived
iteratively from owner-declared references.

Durable publication uses SQLite schema v1 in DELETE/EXTRA mode. The default
store is `.standards-engine/authority.sqlite3`; databases, journals, and
backups are generated local state and are never authored Git authority.
Verified backup and non-overwriting offline restore are operational adapters,
not semantic export/import.

The admitted durable and native-capture profile is CPython 3.11/3.12 on Linux
x86-64 with local case-sensitive ext4. Native capture proves equal endpoint
bindings and bytes after a retained-descriptor read and independent rewalk; it
does not claim that no transient same-user mutation occurred between those
endpoints. Other platforms or filesystems are explicit unsupported outcomes.
