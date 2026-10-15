# Independent observability review

Reviewer role: independent design/source/privacy reviewer requested by the user.
Baseline: `188beda1fa477d21d576c233dd8c7f4c4c267d23`, interface 46.
Review date: 2026-10-14. Scope: the observability plan and existing production
MCP/catalog/runtime identity plus observer-v3 context. No paid model calls,
publication, installation changes, or implementation edits were performed.

Current disposition: independent source/privacy review **satisfied** for the exact
files bound below. R1–R7 are resolved. Earlier pending dispositions describe the
review stages and are superseded by the final disposition. Overall branch
acceptance still requires the owner's full Engine/observer-v3/projection and
publication gates; this review does not assert those unexecuted results.

## Design disposition

Proceed to implementation with the acceptance points below. The proposed ownership
and disclosure boundaries are appropriate. These are design requirements to verify,
not findings against implementation that does not exist yet. Implementation/source
acceptance remains pending.

The plan preserves the Engine's domain authority, opts in outside agent tools,
distinguishes construction from delivery, disables a failed recorder, rejects
unsupported retained state, and honestly excludes replay, intent, acquisition,
token and billing conclusions. No design change to observer-v3 is needed.

## Findings and required evidence

### D1 — Medium: include health emission in the fail-open boundary

Evidence: plan lines 74–77 require one stderr health report and no domain-return
change; existing stdio delivery is owned at `mcp.py:210–227`. A stderr write or
flush can itself raise. A failure handler that emits through an unguarded sink can
replace an otherwise valid response or mask the original interruption.

Disposition: guard health emission and recorder cleanup independently. Keep fixed
reason codes and in-memory counters; never include exception strings, database
paths or deployment input in failure text. Test a broken stderr sink as well as a
failed database, proving identical MCP output and exactly one domain invocation.
The synchronous implementation cannot promise an end-to-end latency bound for
arbitrarily blocked filesystem or stderr I/O; state that operational limit rather
than deriving it from SQLite busy timeout.

### D2 — High: structural privacy needs component-level authority

Evidence: plan lines 56–61 permit schema property names and sanitized pointers,
while `input_feedback.py:14–19` projects validator issues and
`validation_feedback.py:25–45` builds instance paths from input locations. It
already replaces names absent from the schema-path property set with `*`, but
that set is not position-aware: an arbitrary map key equal to an ancestor's
declared name can survive. Existing value-free messages therefore do not prove
every pointer component's exact-location authority. Static property names also
do not authorize collecting their scalar values or enum choices.

Disposition: admit only property components at their exact schema location;
unknown keys and `additionalProperties` keys need fixed markers, including inside
feedback pointers. Redact whole free-form/sensitive subtrees before traversal.
Never retain raw outputs, message text, raw hashes, selector guesses or client
identifiers. Admit selector strings only from the selected operation's exact
canonical definition inventory. Test nested arbitrary keys, escaped pointer
components, very long/deep objects and arrays, scalar substitutions, and secret
sentinels across the database, journal, report and health output. Treat absence
of an independent privacy oracle as pending evidence.

### D3 — Medium: schema identity and migration checks must share writer isolation

Evidence: plan lines 66–73 select multiple processes, `BEGIN IMMEDIATE`, v0 empty
initialization, intact v1 reopening and rejection of unrelated stores. Reading v0
or checking table absence before acquiring the transaction permits two initializers
to decide from stale facts. A `user_version` match alone does not establish the
application's owned schema.

Disposition: acquire the writer transaction before validating the state used for
initialization, verify the expected v1 schema/application identity, and preserve
unrelated/partial/future/corrupt databases. Test simultaneous first-open, v1 reopen,
spoofed/partial v1, lock exhaustion, quota failure and transactional rollback.
Do not change foreign database PRAGMAs or create observation tables before proving
ownership. A version pragma is a ledger, not an ownership proof.

### D4 — Medium: retention must own session growth and in-flight eviction

Evidence: plan lines 47–50 retain session metadata separately and lines 69–70
bound interactions while explicitly permitting unmatched-start eviction. A limit
on interactions alone can leave sessions growing through repeated restarts.
Another process can prune a start while its original owner is still executing.

Disposition: bound and prune orphan session metadata alongside retained records;
define how finish behaves when its start was already evicted. Such eviction must
not create a fabricated completion or unnecessarily disable otherwise healthy
recording. Exercise a live request crossing retention in a second process and
repeated short-lived sessions. Account for evictions in the persisted/report
denominators without retaining an unbounded history of evicted identifiers.

### D5 — Medium: bound report work and preserve distinct denominators

Evidence: plan lines 78–83 promise a bounded read-only report with latency, bytes,
incomplete observations and ordered discovery/failure sequences. Limiting only
the final serialized JSON does not bound query work or intermediate cardinality.
The existing direct dispatch returns at `mcp.py:100–107`; stdio writes/flushes at
`mcp.py:224–225` are a separate observation.

Disposition: declare scan/row/group/output budgets and truncation indicators;
use one consistent read snapshot. Keep constructed responses, flushed responses,
notifications, incomplete/evicted starts and protocol/typed/tool errors distinct.
Define which duration includes recording overhead, use monotonic elapsed time,
and count JSON UTF-8 bytes under an explicit newline policy. Ordered sequences
are same-process/operation correlation only, and must not cross unknown retention
gaps as if a complete history existed. Test read-only behavior against an active
writer and bounded output with many groups/sessions.

## Source and qualification boundaries

`runtime_identity.py:46–78` already owns process UUID, catalog/schema digests and
installation-source material digests; its module contract requires a coherent
installation before startup and does not claim hot reloading. Reuse those values
without introducing a Git commit or standards snapshot as implementation authority.
Per-operation digests must identify the complete canonical operation input schema,
not merely its abbreviated agent-facing presentation. A digest comparison reports
equality/difference; it cannot reconstruct an absent historical catalog.

`INPUT-DISCOVERY-QUALIFICATION.md:84–132` requires exact source/runtime/catalog,
chronological starts, isolated thread/turn and retained transcript/readbacks for
observer-v3 replay. Production shapes deliberately discard the evidence needed for
those claims. No production report may relabel its sequence counts as observer-v3
qualification or corrected historical replay. Synthetic tests must remain labeled
as process/integration evidence, with no model/client acceptance claim.

## Design-stage remaining acceptance

Exact-source review and tests are pending implementation. Required review focuses
on actual disclosure paths and failure handlers, all persisted fields, transaction
ordering, delivery/error/interruption paths, report bounds, and unchanged catalogs
and domain outcomes. No implementation approval, publication approval or deployment
qualification is implied by this design review.

## First implementation review

Source was uncommitted and changing during this review. The references below name
the first inspected implementation; final source hashes and dispositions will be
recorded after fixes. Independent synthetic probes used temporary SQLite databases
only. They did not invoke a model or modify production code.

| ID | Severity | Evidence and observed consequence | Required disposition |
| --- | --- | --- | --- |
| R1 | Medium | `InputShape.feedback` read `pointer`, but production `InputIssue` exposes `instance_pointer`. The real-dispatch privacy test failed because `expected_catalog` disappeared from retained feedback. The unit fixture supplied the nonexistent field. | Consume the actual production diagnostic field and retain a real-dispatch regression. |
| R2 | Medium | `begin` skipped all dictionaries lacking `id`. A probe dispatched `{'jsonrpc':'1.0','method':'ping'}` and received `-32600`, but retained starts remained zero. | Skip actual notifications while retaining malformed-envelope responses, without changing dispatch behavior. |
| R3 | Medium | `serve` computed `line.encode('utf-8')` outside the measurement guard even with observations omitted. A StringIO JSON request containing an unpaired surrogate raised `UnicodeEncodeError`; the baseline parser/serializer handles that input. | Make byte measurement optional and fail-open, preserving the omitted path. |
| R4 | Medium | With one call active, another recorder inserted 16 calls at `max_calls=16`. Finishing the evicted call permanently degraded the first recorder with `start-evicted-by-retention`. | Treat expected retention loss as a dropped terminal; preserve future recorder usability. |
| R5 | Medium | A two-scope probe with report `limit=1` emitted one group with no group truncation flag, but sequence denominator merged both scopes. Chronology scan and histogram cardinality were unaffected by limit. | Add explicit scan/group/output bounds and truncation; preserve construction/delivery scope in sequence denominators. |
| R6 | Medium | An empty v0 WAL database was committed to v1/three tables before rejection as `unsupported-journal-mode`; a byte comparison confirmed mutation despite rejected storage capability. | Prove journal/page-budget capability before migration publication and verify rejected retained states remain intact. |

All six findings were sent promptly to the implementation owner. None alleges a
confirmed secret-value leak in the inspected recorder. R1 concerns missing useful
feedback; the separate structural privacy projection remains subject to final
source review and adversarial tests. Acceptance is pending fixes and final review.

## Fix review and additional admission finding

The revised source resolves R1–R6: real `instance_pointer` feedback is consumed;
malformed no-ID requests are retained; byte encoding is optional/guarded; normal
in-flight retention loss drops only its terminal; reports separate scope and expose
bounded sections/scan/truncation/measurement denominators; storage capabilities
are checked before migration publication. Sanitized shape summaries now include
successful as well as failed requests. The operating guide accurately distinguishes
delivery, domain completion, loss counters, idle retention and observer-v3 replay.

Independent command on CPython 3.12.14:

```sh
python -m unittest tools.standards_engine.tests.test_interaction_observer
```

Result: 21 tests passed in 27.416 seconds. This is synthetic local/process evidence,
not real model/client acceptance. Final acceptance remains pending R7 below.

### R7 — High: logically empty v0 can contain unrelated private bytes

The v0 admission predicate at the then-current `interaction_observer.py:293–295`
checked application/version zero and absence of tables. A database from which a
table was dropped satisfies that predicate while retaining the table's raw values
in freelist pages when secure deletion was previously disabled. Enabling secure
deletion later does not erase those existing remnants.

Independent temporary-database reproduction: disable `secure_delete`, create an
unrelated table, insert a repeated synthetic private-content sentinel, and drop
the table. The source has no tables, two pages and one freelist page. The recorder
accepted it as healthy, recorded a ping, and the sentinel remained in the resulting
observation file after close. No actual private content was used.

Required disposition: reject non-pristine v0 retained states before mutation.
Zero-length new/existing files are a sufficient narrow initial support policy;
supporting additional empty representations requires proof that they cannot carry
unrelated retained bytes. Preserve rejected files rather than wiping them. Add an
on-disk sentinel regression and update the documented v0 admission policy.

## Final source disposition

R7 is resolved by requiring both the original file-descriptor stat and current
physical file length under the writer lock to be zero before initializing v0.
The trusted-directory precondition excludes hostile path replacement. The guide
and plan now select zero-length new v0 sources explicitly. Rejected prior files
are preserved. A first attempted correction used transaction-observed page count
zero and rejected new files because SQLite materializes a virtual first page at
`BEGIN IMMEDIATE`; independent probing exposed this and the physical-length check
replaced it before acceptance.

An independent final temporary-database probe observed a fresh file becoming
healthy and the dropped-private-content file being rejected as
`nonpristine-database`, byte-for-byte unchanged with its sentinel still present.
The final focused command above passed **22 tests in 27.573 seconds** on CPython
3.12.14. It covers real dispatch/privacy, arbitrary outputs, parse/envelope errors,
tool exception/interruption/delivery failure, broken stderr, unavailable/locked/full
SQLite, supported/rejected/migration-interrupted states, retention across processes,
scope/report truncation, and cold stdio/process replacement. `git diff --check`
also passed. No real logs, private datasets or model calls were used.

| Finding | Final disposition |
| --- | --- |
| R1 | Resolved: production diagnostic field and real-dispatch regression. |
| R2 | Resolved: invalid no-ID envelopes observed; notifications excluded. |
| R3 | Resolved: optional guarded request measurement; omitted/enabled surrogate regression. |
| R4 | Resolved: late terminal loss counted while healthy recording continues. |
| R5 | Resolved: scoped sequences, bounded scan/sections, truncation flags, sanitized shapes and measurement counts. |
| R6 | Resolved: journal/page admission precedes migration publication; rejected bytes preserved. |
| R7 | Resolved: only pristine zero-length v0 is admitted; prior private remnants rejected without wiping. |

No unresolved source/privacy findings remain in this reviewed scope. The design's
D1–D5 acceptance points are satisfied by the inspected construction and focused
evidence, within the operating guide's local POSIX/trusted-directory and synchronous
I/O limits. Same-user access remains outside the confidentiality/tamper boundary;
shape summaries remain correlation evidence and cannot qualify observer-v3 replay,
agent intent, schema acquisition, tokens or billing.

Current exact SHA256 binding (including the accepted test-only addendum below):

| File | SHA256 |
| --- | --- |
| `tools/standards_engine/standards_engine/interaction_observer.py` | `bc14652d3aa78ea400495d7f89fe9c4662c4de16acf759cac41d8279239a2a78` |
| `tools/standards_engine/standards_engine/mcp.py` | `3852b7531dbf53d9c3eceec5503c7544de7df48aee714f618542b57754ae8596` |
| `tools/standards_engine/tests/test_interaction_observer.py` | `3e39503185582b2ebeb13d86d92f65015e6ddb33f9133fee66db469b0e78d9a3` |
| `tools/standards_engine/MCP-OBSERVABILITY.md` | `852dae36046f4dd54c912c6e0efc7f7c5f722a4d31723eb647956b6903e2743e` |
| `tools/standards_engine/README.md` | `02fc2e17d6e4479d70fcb62caa189516db4e205ddfdc381a1b6ed721ed9ac15b` |

Any subsequent substantive change to these files invalidates this exact-source
binding and needs a review scoped to the changed claims. This reviewer performed
no publication or installation action and wrote only this report.

## Accepted test-only addendum

The sole subsequent source delta adds
`test_catalog_revision_report_attributes_exact_operation_schema_changes`. Removing
that method reproduces the preceding accepted test-file SHA256
`d9071a506955f0f2014d1901eec2f58ab01cb1a412c2ac4e56324480b59be3c3` exactly.
The production source, operating guide and README still match their accepted
hashes above.

The new synthetic test creates two recorder sessions with an explicit catalog
addition, removal and changed input type, then requires the exact corresponding
report categories and preserved synthetic implementation attribution. Its expected
categories follow directly from those independently specified fixture changes.
It proves recorder/report catalog comparison, not authentic runtime provenance or
model/client qualification. No findings against the delta.

Independent targeted command:

```sh
python -m unittest tools.standards_engine.tests.test_interaction_observer.ObserverTests.test_catalog_revision_report_attributes_exact_operation_schema_changes
```

Result: one test passed in 0.003 seconds. The owner's completed focused-suite log
at `/tmp/issue3-observer-tests.log` was also inspected: 23 tests passed in 25.572
seconds. That log is supporting owner evidence; the independent complete-suite
run remains the 22-test result above, with this one-test delta independently run.
Independent source/privacy review remains satisfied at the updated exact binding.

## Accepted constant-ownership addendum

The final production delta imports the recorder's three default retention/quota
constants into the MCP CLI and names the existing 8192-byte shape limit
`MAX_SHAPE_BYTES`. Independent reverse substitution reconstructs the two preceding
accepted source hashes exactly: observer
`17751c69e10db84d391120738079b8389dea1cb43626fd08139bb11498b5421f` and MCP
`153b3dd86023c9e6f5677889474ee224c28cb20e8945ba09de7eb235402d253b`.
There are no other source changes in this delta.

The shared defaults evaluate to 10000 calls, 604800 seconds and 33554432 bytes,
identical to the replaced CLI expressions. The named shape limit evaluates to
8192 and is used in the same comparison. This supplies a construction proof of
equivalent behavior while giving those policies one owner; no new test is needed
for the literal-to-constant replacement. Runtime implementation identity naturally
changes with source material, as its existing contract requires.

Tests, operating guide and README still match their accepted hashes. The current
table above binds the new production hashes. Independent source/privacy review
remains satisfied with no new findings. The owner's final combined focused run
and broader Engine/baseline-failure disposition remain separate evidence gates.
