# Capture and grouped-reading increment

Status: implemented; local qualification recorded in the companion evidence report. Base `bac7dc3dc39fbf519429ea91bff1e02e65925299`.

The user selected two consumer-performance changes: persistent batch Git reads
with parsed-tree reuse inside one revision-read session, and a bounded same-
snapshot multi-read API. Repository Git owns child lifecycle, object integrity,
path interpretation and retained-memory bounds. Engine navigation owns one
verified input set and fresh purpose-specific outputs. Canonical schemas own
wire shapes; generated models and catalogs are regenerated together.

Applicable guidance: Core and Router; Implementation, Verification and evidence
oracles, Performance, Development Proportionality, Architecture and Replay,
Contracts and generated-contract/IPC boundaries, Concurrency, Resilience and
Security. Existing storage, authorization, publication and recovery boundaries
remain authoritative. The previously agreed prospective positive-guidance and
proportionality practices apply; normative text stays unchanged.

Write scope: repository_git implementation/tests/README; standards_engine
navigation/facade/MCP/renderer/contracts/generated outputs/tests and implementation
documentation; derived verification-input manifest; this report directory.
New helpers remain inside their existing package owner. No second graph,
database, cross-call proposal cache or standards-content rewrite is introduced.

Design: each read session retains at most one active Git batch child; switching
an explicit gitlink repository closes that child and opens the selected one.
Verified object and decoded-tree data share the existing bounded LRU. Every
object miss checks protocol framing, type, length and hash. Each request retains
the existing Git command timeout; there is no total capture deadline. Closure,
mode and path checks remain. Normal close verifies EOF/exit and reaps workers;
exceptional close aborts the owned process and releases all state.

Multi-read uses an explicit snapshot and 1–32 ordered requested reads, with a
2 MiB JSON-result budget. It returns the complete set or one rejection, with no
partial result. Application and authoring inputs/results retain separate schema
variants. One durable integrity load supplies the operation; current snapshot
lifecycle is observed before each item and before return. Each item uses the
existing read projection and permission boundary. Detail and handles never
change purpose. Independent calls, fresh captures and publication remain fresh.

Simplicity review: repository sessions contain the actual pipe/cache lifetime;
removing them reinstates per-object processes and parsing. Grouped reads compose
the existing single-item projection and do not create a batch execution engine.
Consumers know one snapshot and a requested set, rather than compiler/storage
mechanisms. Child framing changes stay in Repository Git; wire changes stay in
Engine contracts/navigation. Reuse ends with its explicit owner.

Acceptance: exact baseline/candidate capture IDs and two independent compiles;
real Git corruption/missing/size/gitlink/timeout/EOF/cleanup tests; bounded decoded
memory; ordered multi-read equality including failures and purpose exclusions;
current lifecycle and cold replay; native/CLI/real MCP multi-read and schema
projection; same-environment timing with inputs/repeats/limits recorded. Required
checks remain intact. Repairs within this scope continue normally; changes to
ownership, guarantees or consumer contract require an explicit revised decision.
