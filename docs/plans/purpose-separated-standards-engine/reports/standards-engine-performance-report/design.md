# Standards Engine performance design

**Status:** proposed design; no optimization implemented.  
**Analysis date:** 2026-09-23.  
**Branch:** `implementation/purpose-separated-standards-engine`.  
**Inspected revision:** `8750761133b66297a2bfac4e495fd1c8a893b96a`.

## Recommendation

Improve the cost of preserving integrity before adding a cache around the existing slow path. The first implementation increment should combine exact-format identity-encoding improvements, bounded reuse of verified Git objects during capture, and explicit reuse of immutable material within an operation. Preserve the existing full compiler and all capture/replay, authorization, publication, recovery, and disclosure boundaries.

A bounded pure compiled-snapshot cache and supported-interface reuse at the existing MCP-process lifetime are a second, conditional increment. Keep the Engine/SQLite lifetime per call: reopening costs only milliseconds in the measured database and preserves the current open-time validation boundary. Its design is specified below, but its current marginal saving is approximately 0.3 seconds per ordinary read, not the whole 2.9-second read. Admit that extra retained state only if the first increment leaves meaningful repeated-call latency or schema-loading cost. Selective compilation and a persistent on-disk compiled cache are not selected.

The measured contributors and complete measurement limitations are in [the evidence report](evidence.md). Proposed budgets are targets for a later implementation comparison, not demonstrated speedups or accepted production service levels.

## Scope and governing contracts

This is a design and evidence task. Application source, tests, normative standards, dependency locks, the real accepted branch, and the user's installed database remain unchanged. Measurements run against an isolated reconstruction of the published branch. A separate disposable benchmark clone points its **local** `main` at the candidate, as required for pre-merge qualification by `PURPOSE-SEPARATION.md`; the source reconstruction retains the original `main`.

The applicable guidance is Core and the Router; Performance and Verification; Development Proportionality; Architecture and Immutable Results And Replay; Contracts; Persistence; Concurrency; and Security for the existing purpose/authorization boundary. Relevant obligations are measurement fidelity, proportionate machinery, independently sufficient module boundaries, exact replay, honest supported-environment claims, and owner-specific lifecycle. This task creates no new generic standards policy.

Preserved product promises:

1. New capture resolves accepted `main` once to an exact Git revision, reads that revision, independently compiles recorded Git material and frozen material, compares requested path closure and semantic signatures, and publishes only after success.
2. Explicit snapshot and proposal handles select their exact material. Cold replay uses captured bytes, rather than current files or an originating process.
3. Application/authoring purpose is host-owned and immutable for the interface. Each response is constructed through its existing purpose-qualified path.
4. Current access authorization, review decisions, proposal heads, application readiness, exact candidate verification, compare-and-swap publication, and recovery observations retain their current checks and timing boundaries.
5. Existing supported contract semantics remain single-valued. The design preserves identity-v2 preimages and content IDs; it introduces no old-format reader, fallback authority, dual write, or automatic migration.

## Measured problem decomposition

For the 434-file, 3,708,028-byte captured corpus, the temporary SQLite database was 4,558,848 bytes. Three isolated serial operation sweeps measured a median 15.234-second capture and approximately 2.9-second explicit reads. The operation breakdown locates approximately 2.54 seconds of a read in snapshot loading outside SQLite, principally content-identity reconstruction; SQLite content retrieval is about 0.011 seconds and compilation about 0.32 seconds.

Capture makes 1,137 source reads of 434 unique paths, leading to 6,134 verified object requests for only 524 distinct repository/OID/type combinations. Each object request launches a new `git cat-file --batch` process. Git commands consumed approximately 11.34 seconds in the representative capture. The independent frozen compilation itself was approximately 0.315 seconds. The two-pass guarantee is necessary; repeatedly launching Git to read the same immutable commit and tree objects is not the guarantee.

The isolated long workflow test took 119.855 seconds in its body and 137.863 seconds including its class setup and runner work. It recomputed content identity 32 times (86.127 seconds), compiled 52 times (18.528 seconds), and reconstructed a proposal projection 21 times. Parent and child span durations overlap; those projection durations must not be added again. This is CPU-intensive repeated derivation, not evidence that a 240 MB database caused a wait.

## Options and trade-offs

| Design | Benefit supported by baseline | Cost / correctness concern | Decision |
| --- | --- | --- | --- |
| Reuse already-verified material and projections inside an operation | Identical base/proposed snapshot is loaded twice in `prepare`; same-snapshot `resolve` loads it four times. `_validate_projected_inputs` reconstructs a projection already obtained by its caller. | Requires explicit proof lifetime and separation from live authorization, lifecycle, and publication barriers. | First increment. |
| Optimize identity encoding without changing bytes or IDs | Content-identity work is about 88% of a read's wall time and 72% of the isolated long test body. | Exact escaping, arbitrary integers, path ordering, framing lengths, and failure behavior must remain equivalent. | First increment; highest repeated-read leverage. |
| Capture-scoped verified Git object reuse | 6,134 requests versus 524 unique objects identifies about 91.5% redundant object fetches. | Bounded memory and correct repository/gitlink/hash-algorithm scoping; mutable sources must retain existing recording semantics. | First increment. |
| A genuine capture-scoped batch Git reader | Amortizes remaining process and pipe setup beyond object reuse. | Adds pipe framing, output-bound enforcement, cancellation, and child-process lifecycle. | Evaluate after object reuse; retain only if remaining capture cost warrants it. |
| Compiled immutable-snapshot cache | Avoids about 0.3 seconds of compilation per ordinary warm read; supports reuse across analysis operations. | A cache around `_compiled_snapshot` would otherwise skip lifecycle and content validation. Requires bounded, immutable ownership. | Conditional second increment, after cheap integrity work. |
| MCP-process-owned pure cache and compiled interface, with per-call Engine | Reuses derived material and avoids about 0.28 seconds of interface compilation; retains current database-open checks. | Explicit borrowed-cache ownership and namespace/bounds; no cached request state. | Preferred form of the conditional second increment. |
| One long-lived Engine/SQLite connection per MCP server | Also retains caches, but saves only about 0.004–0.005 seconds of store opening here. | Changes open-check frequency unless checks remain per call; adds connection replacement/shutdown concerns. | Not preferred for this baseline. |
| Selective / lazy compilation | Coverage/evidence compilation dominates the compiler-only profile; navigation often uses less than the full result. | Full compilation currently validates more than rendering needs. Skipping stages can accept malformed authority previously rejected. Adds dependency-specific proof and cache states. | Defer. |
| Persist compiled Python state on disk or add a shared cache service | Could reduce process-replacement recomputation. | New serialization/trust/versioning/recovery boundary, no demonstrated need after cheap validation and compilation. | Exclude from this design. |
| Reduce checks, bypass hashing, omit captured evidence, relax SQLite integrity/durability | Would remove work. | Changes the promised result or detection boundary, rather than improving its implementation. | Outside the accepted objective. |

## Preferred core design and module boundaries

### 1. Exact identity encoding remains Identity-owned

`tools/standards_identity/standards_identity/encoding.py` remains the sole owner of identity-v2 encoding and framing. Snapshot code continues supplying its existing domain, prefix, paths, and bytes. Improve the implementation behind that boundary.

The existing path-byte-set builder validates and constructs each framed entry once and then constructs it again. Retain the validated first construction and sort those entries, preserving empty/duplicate-path and Unicode checks. The byte content is represented as millions of integer values; every byte currently travels through the arbitrary-size integer formatter, including list creation and `divmod`. Use an exact small-integer fast path or bounded precomputed byte tokens, retaining the general arbitrary-integer path. Encode contiguous unescaped string segments together, preserving the existing exact quote, backslash, control-character, Unicode and surrogate behavior.

Begin with these local transformations. Introduce a compact byte-sequence representation or streamed hashing only if retained allocation and encoding cost still dominate. Such a specialization belongs inside Identity and emits the **same existing canonical preimage**, including encoded-length framing; it is not a Snapshot-owned second encoder. `encode_identity_value` and `hash_identity` must share one definition of encoding semantics.

Keep complete content hashing on durable loads. A faster hash of a different record, a file-count check, or trusting the database's stored content ID would change the claim. Standard `json.dumps` is not presumed identical to the current custom escaping and arbitrary-integer behavior.

### 2. Verified Git reuse is capture-owned, not a global file cache

Add a bounded exact-revision read session within `tools/repository_git`, constructed for one exact selected revision and its explicit gitlink mapping. Capture owns one such session; another bulk revision read, such as `maintain_evidence`, may own its own session using the same mechanism. Cache only fully verified object bytes, addressed by repository identity, object ID, expected type and hash algorithm. Retain the existing header, size, frame, mode, type and object-ID checks before admission. A repeat lookup reuses the same verified immutable object; first reads retain exact error classification.

The Engine composes that reader beneath `_GitRevisionSource`. `RecordingContentSource` continues observing every requested logical path and comparing repeat results. It remains unchanged for mutable or independently implemented content sources. Fresh frozen replay continues to run through a separate recorder and a fresh full compiler; neither compiler result may be answered from a compiled cache.

An initial **8 MiB verified-object payload / 1,024-entry cap** is proposed for the captured workload (3.71 MB file bytes and 524 unique observed objects). These are candidate-local tuning values, not new generic standards. Measure bookkeeping and tree-object retention before accepting them. Eviction or an oversized valid object causes ordinary verified reading, with no correctness change. Existing per-object safety limits remain authoritative. Destroy this cache at the owning capture or bulk-read operation's completion or failure. A verified object remains a valid immutable input for that operation; the session does not claim continuous health of its original on-disk storage after the successful read. Every fresh session verifies its own first reads.

If repeated process startup remains material after this change, the same repository owner can run one batch reader per underlying Git repository for the capture. Git's documented batch protocol already supports multiple requests in one process. Preserve per-frame verification and independent stderr draining; consume and reap the child on every terminal path. A new whole-capture deadline must not replace the existing per-operation contract. This additional adapter is contingent on measured residual cost.

### 3. Explicit material reuse inside one public operation

In `standards_engine/engine.py`, carry verified captures, compiled snapshots and exact `LogicalProjection` values through the pure preparation/evaluation path. A small local operation-owned mapping or explicit parameters suffice; there is no global context registry or new durable record.

For identical base and proposed snapshot IDs, validate the material once and use the same immutable value for both roles. Preserve each role's identity and the existing current lifecycle checks. For distinct inputs, retain distinct verified values. Pass the already obtained proposal projection to `_validate_projected_inputs` instead of rebuilding it to inspect the same facts. Where logical authoring also recompiles its unchanged base, pass the existing compiled base through a bounded internal input that is explicitly bound to the verified source; independently compile the changed candidate. The two fresh snapshot-capture passes remain separate from this reuse.

`resolve` still evaluates the pre-submission and post-submission decision states separately. Reuse their immutable input material, not the evaluation, permissions or decision result. Apply the same rule to repeated immutable proposal material during `propose`, `analyze`, and `query_proposal`.

Live source/evidence observations, provider execution, current authorization, current proposal-head checks, and the explicit pre-/post-verifier publication validations remain fresh where they are currently required. A code path crossing one of those barriers reacquires the required authority; it does not cite an earlier material lookup as proof of permission or readiness. No reuse survives the owning operation unless the separately admitted cache design applies.

## Conditional compiled cache and transport lifetime

### Entry and lookup rules

The cache stores only the fully compiled representation of an exact frozen content set. Scope it to a trusted owner with fixed repository identity, installed compiler/contract implementation, and purpose. For MCP this is an explicit cache owned by the existing server process and borrowed by each per-call Engine; standalone callers can keep reuse operation-local. The key is the validated content-set identity within that namespace, including the observed store identity where required to isolate store lifecycles. Public handles, source revision, access state and result envelopes are reconstructed from the current request; they are not cached results.

**Each public operation first performs the existing readable-root/lifecycle and durable content integrity checks.** Use the optimized exact hash. Only then consult the compiled cache. Cache availability never makes a missing, quarantined, expired, corrupted, or unsupported capture readable. Within the operation, the verified material can flow as described above.

On a miss, compile through the existing full pipeline. Retain the successful frozen representation; failures are returned and not negatively cached. Where capture has just completed both independent passes, its second validated result may seed this cache only after successful publication. Retain a frozen content source, not the first pass's live Git reader or either recorder's mutable tracking state. The graph currently exposes read-only mapping views; all other reachable collections and sources need the same ownership review before sharing.

A hit supplies pure canonical material to the existing purpose-qualified projection. Application approvals, dependencies and filtered relationships come from the exact selected snapshot. Build fresh response objects and continuations. Keep authoring data inside the trusted process; it is never an application output-cache entry.

### Bounds

The measured incremental retained compilation allocation is 3.65 MB, excluding already-held captured bytes and imported code. Raw capture plus that increment is about 7.36 MB. Propose an **LRU with at most two compiled entries and a 32 MiB accounted-retention budget**, sufficient for a representative base/proposed pair with headroom. Confirm actual retained object accounting during implementation; this is not a process-RSS guarantee.

Account raw bytes and reachable compiled allocations without repeatedly charging shared immutable objects. An entry whose ownership or size cannot be established stays uncached. Oversized valid work uses the normal verified uncached path. Eviction changes cost only; active operations retain their borrowed immutable value until completion. Cache-owned memory and active-operation working memory are reported separately. The cache owner releases its entries deterministically at shutdown. Closing a borrowing per-call Engine closes its store but does not destroy the server-owned pure cache.

An entry-count-only `functools.lru_cache` around a method is not this design: it retains `self`/results and cannot express the lifecycle/integrity lookup boundary or byte accounting. Python's documentation also distinguishes a thread-safe cache map from single execution of a concurrent miss.

### MCP lifetime

Prefer retaining the current per-call Engine/facade/store lifetime. The existing MCP process owns a bounded cache of pure compiled material and one compiled supported-interface contract. Its call path injects those trusted dependencies into a fresh Engine/facade, executes the operation, and closes the SQLite connection as it does now. Interface selection and full store-open validation remain explicit; the cached interface describes the installed Engine API, not accepted-main policy.

This saves the expensive pure work without paying the semantic cost of reducing how often the database is reopened and integrity-checked. The measured 4–5 ms reopen cost does not justify changing that behavior. If a future deployment establishes meaningful open-time cost, evaluate a long-lived connection separately with an explicit integrity-check contract; it is not part of the preferred first design.

Keep the existing serial request dispatch. Each independent MCP process owns its own pure cache and fixed purpose; no distributed cache or extra service is introduced. Each Engine receives a fresh/current execution context under the existing authorization contract. A plain CLI invocation still opens, executes, and closes once; it gets correct cold behavior without a background process.

The installed implementation and generated interface are fixed for the MCP process lifetime. Engine code/schema replacement requires a controlled restart; ordinary standards publication is not code replacement. A new store is opened through the existing validation path and uses its own cache namespace. Missing/corrupt/replaced storage is not answered from retained material. Clear retained pure entries at server EOF or failure.

Implement the reuse boundary in the Standards Engine package, not as standards semantics inside MCP. The transport owns its lifetime and injects it; snapshot loading owns integrity; the Engine owns pure compilation. Avoid a cached facade with a mutable Engine pointer or an ambient global cache.

## Invalidation and failure matrix

| Event | Required behavior |
| --- | --- |
| Accepted `main` advances | Next automatic capture resolves the new OID and performs both fresh compiles and closure equality. Old explicit snapshots keep their old material. |
| Main changes during a capture | Complete the capture against the OID selected at entry; the subsequent new capture sees the next revision. No mixed working-tree reads. |
| Only non-captured files change | The source revision still reflects the selected commit. Equal verified content may reuse pure compilation; result provenance remains attached to the correct snapshot. |
| Old snapshot reopened in another process | Recheck store/lifecycle/content and cold-compile captured inputs; missing cache is immaterial. |
| Snapshot quarantined, purged, missing, or bytes corrupted | Current store check returns the existing typed failure before cache use. No stale cached result substitutes. |
| Exposure withdrawn on newer main | New capture reflects withdrawal. Explicit historical snapshots retain their documented historical approval semantics; current disclosure authorization remains separate. |
| Purpose or current permission differs | Dispatch and projection enforce the current trusted interface/authorization. Cached canonical material grants neither capability nor disclosure. |
| Proposal head changes | Existing revision binding and compare-and-swap checks decide readiness/application. An older pure projection never selects the new head. |
| Publication interrupted or outcome unknown | Existing recovery handles and observation-only recovery remain authoritative. Cache lookup does not authorize retry or infer success. |
| Budget exceeded or entry evicted | Normal verified computation; same value or same domain failure, different latency only. |
| Compilation rejects | Return the existing failure; no cached failed state or fallback to another snapshot. |
| Engine implementation/contract changes | Restart and create an empty process cache under the one installed supported contract. No serialized compiled-state compatibility path. |

## Concurrency and SQLite/Git costs

The representative read's SQLite work is small. Store opening, including integrity checks, is measured in milliseconds for this database. There is no evidence to justify changing journal mode, synchronization durability, constraints, isolation, or busy handling for the reported delay.

One concurrency concern remains visible in source: `SnapshotModule.maintain()` calls `purge_expired()`, which begins an immediate write transaction even when nothing expires. Multiple processes sharing a store can contend there. This is a **separate potential cause under write contention**, not the measured CPU-bound two-minute test. Measure that scenario before changing maintenance scheduling; expiry and lifecycle visibility are correctness boundaries.

Keep SQLite transactions narrow and retain current conditional writes. Pure compilation does not hold a write transaction. For in-process concurrency, preserve current serialized ownership instead of making one SQLite connection accidentally shared across worker threads. If a future embedding explicitly supports concurrent calls, use one connection/Engine per execution owner or a reviewed serialization boundary. A concurrent cache map alone would not make the Engine thread-safe.

Git object reuse is isolated to its capture and repository mapping. No lock is held while running unrelated analysis or publishing. A failed or cancelled capture releases reader/process/cache resources, and the next capture obtains a new accepted revision and fresh validation.

## Verification plan

Use the unchanged public behavior as the reference and test the affected mechanism at its real boundary. The original platform harness currently submits Analysis request version 5 to a version-6 interface. Correct that caller as a separately identified harness-conformance repair before claiming platform acceptance; never add a version-5 runtime fallback or relabel its present rejection as a passing timing sample.

| Claim | Focused evidence |
| --- | --- |
| Identity bytes and IDs unchanged | Existing identity-v2 fixtures plus differential exact-preimage and digest comparison for all 256 bytes, empty content, controls, quotes/backslashes, Unicode scalar boundaries, duplicate/reordered paths, large arbitrary integers, and framed-length boundaries. Keep malformed-input outcomes. A temporary reference oracle belongs only in tests and has a stated retirement condition. |
| Capture still performs independent proof | Count two fresh compiles; retain mutating-source, additional replay-read, path-closure mismatch and signature mismatch cases. Seeded cache must not satisfy either pass. |
| Git reuse preserves exact objects | Real disposable Git repositories with repeated trees/blobs, modes, mapped gitlinks, missing/corrupt objects, object-size failures and distinct repositories. Verify cache on/off values and failures, process count and cleanup. |
| Operation reuse preserves decision semantics | Same/different snapshots; valid and invalid evidence; before/after submissions; exact proposal revision; identity/authorization failure at the appropriate point. Assert one pure derivation per identical material per admitted operation, while all required dynamic checks execute. |
| Warm cache has no added authority | Populate then quarantine/purge/corrupt; revoke current access where supported; change proposal head; supply foreign handles and switch configured purposes across independent interfaces. Results and failures match uncached execution. |
| Main advancement and cold replay | Capture A; advance main to B; capture B; read both explicitly; restart process; read A with current working tree missing its historical source files. Verify exact snapshot-bound output. |
| Publication and recovery preserved | Existing real Git/SQLite coordinated publication, stale-readiness, interrupted publication and cold recovery tests with cache warm and empty. Retain exact candidate verification and compare-and-swap checks. |
| Bounds and lifecycle | Zero/one/two entries, overflow, oversized material, cache-disabled execution, repeated close/open, server EOF/error, store replacement, and cross-process reads/writes. Measure cache-owned bytes separately from process RSS and working peaks. |
| Actual transport gain | Fresh Python CLI, fresh MCP initialization, repeated explicit-handle calls in one MCP process, implicit new capture, and process replacement. Use the official configured-client/SDK lane in supported Python 3.11/3.12 before claiming installed-client acceptance. |

Performance measurement uses the same corpus, operation sequence, machine, supported interpreter and dependency lock for baseline/candidate pairs. Preserve test assertions and data scale. Report per-test body and class-fixture cost, operation wall/CPU time, Git child counts, hash/compile counts, database dimensions, cache hits/misses/evictions, and retained/peak memory. A structural checkpoint remains separate from functional suites.

## Proposed performance targets and acceptance decisions

Targets below are engineering proposals for this measured workload and require owner acceptance and same-environment remeasurement. Three operation sweeps establish a median/range, not a stable tail-latency SLA. None is a measured optimized result.

| Target | Baseline and derivation |
| --- | --- |
| Preserve exactly two independent full compiles for capture | This is the integrity claim, not a count to reduce. |
| At most one verified object fetch per distinct cache-resident Git key in a capture | 6,134 requests / 524 distinct keys. The measured population should fit the proposed budget; larger populations may evict. |
| Capture median at most 6 seconds on the same benchmark host | 15.234 seconds now. A simple equal-cost model replacing repeated fetches predicts roughly 4.9 seconds without changing identity work; 6 seconds adds uncertainty allowance. Unique-object costs are not yet separately measured, so this is a target rather than forecast. |
| Same-snapshot prepare/resolve at most 1.25 times a single verified material read after the first increment | Current prepare 5.994 seconds and resolve 12.120 seconds versus a roughly 2.9-second read; one verified input per operation plus small separate decision work targets about 3.6 seconds even before hash acceleration. Different snapshots scale with distinct material count. |
| Content-identity median at most one quarter of its baseline | The approximately 2.54-second integrity component is the dominant repeated-read cost. This is an explicit optimization goal for exact-format encoding, not a demonstrated capability. |
| Explicit-read median approximately 1.1 seconds without retained compilation | With the preceding identity goal, 0.011 seconds SQLite + 0.64 identity + 0.32 compilation + projection/measurement margin is approximately 1.0–1.1 seconds. Recalculate from the supported-host baseline. |
| Conditional warm compiled read approximately 0.75 seconds | Same full integrity work, excluding approximately 0.32-second compilation. Admit the cache only if this incremental responsiveness is worth its retained state. |
| Long-test body approximately 60 seconds or less | Holding other costs constant, cutting its measured 86.127-second identity contribution by 75% gives 55.26 seconds, before operation-level reuse. This is a target; preserve every assertion and report class setup separately. |

Fresh-process CLI/MCP targets retain measured import/startup overhead as a separate budget. The measured cold CLI median is 5.486 seconds, MCP initialization 1.783 seconds, and steady explicit-handle MCP reads 3.252 seconds; the 1.1-second target above is a native read with an already constructed facade. The optional 0.75-second warm target also assumes supported-interface reuse, with transport overhead reported separately. An implicit new-snapshot MCP read was 19.540 seconds in one observation; keep using the returned snapshot explicitly for a coherent reading sequence rather than silently weakening new-capture semantics. A warm-process result cannot satisfy a cold-process claim. Full-suite targets follow the per-test distribution after the selected causes are addressed; no claim of a fixed suite-wide speedup is made from one test.

Acceptance order: verify the current-contract harness, implement and measure the core increment, reassess residual latency and memory, then decide whether to implement the conditional cache/transport increment. Keep selective compilation and broader store tuning deferred unless the new profile identifies them as necessary. This sequencing addresses measured work while limiting new permanent state.

## Sources and evidence navigation

All repository references refer to the inspected revision. See [evidence.md](evidence.md) and the included machine-readable observations for measurements and exact scopes.

- `tools/standards_engine/PURPOSE-SEPARATION.md` — accepted-main capture, purpose, stored versions, qualification, cutover and recovery contract.
- `tools/standards_engine/standards_engine/engine.py` — capture, repeated `_compiled_snapshot`, proposal projection and evaluation.
- `tools/standards_snapshots/standards_snapshots/module.py` and `store.py` — durable validation, lifecycle, transactions and content identity.
- `tools/standards_identity/standards_identity/encoding.py` — exact identity-v2 framing and per-byte encoding.
- `tools/repository_git/repository_git/repository.py` — verified one-object-per-process Git reading.
- `tools/standards_engine/standards_engine/mcp.py`, `tools.py`, `context_projection.py` — facade lifetime, interface compilation and purpose-qualified outputs.
- [Git cat-file documentation](https://git-scm.com/docs/git-cat-file) — batch protocol.
- [Python 3.12 functools documentation](https://docs.python.org/3.12/library/functools.html) — memoization lifetime and concurrent misses.
- [SQLite PRAGMA documentation](https://www.sqlite.org/pragma.html) — integrity, busy and data-version semantics. `data_version` is not a content identity or an authorization proof.
