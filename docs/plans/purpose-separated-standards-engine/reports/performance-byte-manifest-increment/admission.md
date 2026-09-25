# Performance increment admission

Base: `2aef993edc8a47ce474468c641cc2e542e3ec8da`.
Branch: `implementation/purpose-separated-standards-engine`.
User direction: implement the next measured performance optimizations and deliver a ZIP.

## Outcomes and owners

1. Identity owns compact exact-byte array storage and encoding, with unchanged
   identity-v2 preimages, IDs and malformed-input behavior. Existing public value
   observation and equality remain sequence-based. Byte joins use bounded chunks.
2. Verifier owns suite-input compilation from explicit content and repository
   membership. Its filesystem adapter retains physical path checks; its frozen
   adapter requires actual bytes for every consumed file. Check execution and
   publication still use actual filesystem candidates. Engine logical authoring
   stops creating temporary repositories merely to derive the manifest.
3. The coordinated-publication test reuses snapshots only during intervals in
   which it intends to observe one accepted revision. Fresh captures after both
   real publications and independent implicit-capture/replay tests remain.

## Write set

- `tools/standards_identity/standards_identity/encoding.py`, its tests and README.
- Verifier suite-input/config/input-context and directly affected authority-input
  adapters; their focused tests, public export, README and derived input manifest.
- `tools/standards_engine/standards_engine/logical_authoring.py`, directly affected
  tests, and `tools/standards_engine/tests/test_supporting_workflow.py`.
- One bounded implementation/evidence report and reproduction data under the
  existing purpose-separated Engine reports directory.

Normative bodies, public wire/persistence formats, identity framing, dependency
locks, authorization, accepted-main capture, independent replay, full physical
candidate verification, recovery, installed config and stores remain unchanged.
No retained cross-call cache or shared mutable fixture framework is admitted.

## Design review

The verifier's content/declaration input is distinct from executing a check.
Directory and frozen sources implement only consumed input operations; the
canonical compiler and check-owned declarations remain shared. No shadow
compiler or guessed empty files are introduced. The physical adapter hides
containment/symlink behavior; the frozen adapter hides membership and byte lookup.
The Identity change stays in the existing value owner rather than a second codec.
Each outcome is reversible independently and receives its own focused evidence.

## Deciding evidence

Exact identity fixtures and independent preimage/digest comparisons cover bytes,
Unicode, arbitrary integers, ordering, mutation and large/chunked inputs. Frozen
and filesystem manifest bytes and exact diagnostics are compared over real and
focused malformed corpora; unavailable captured bytes remain unavailable. Existing
Git/SQLite publication, cold replay, purpose and recovery tests remain mandatory.
Performance comparisons use the same executable, dependencies, corpus and serial
operation sequence. Separate memory probes report tracemalloc rather than RSS.
Functional tests remain separate from the structural checkpoint. Supported
installed qualification remains honestly distinct from this local environment.
