# Targeted Test Strengthening — Verification

**Status: source implemented and locally verified; supported candidate CI and
independent review/owner acceptance remain pending.** The predecessor packaging
plan is not modified or declared Accepted by this delivery.

## Source and admission

The user authorized implementing the next selected step: five targeted regression
improvements. Work uses exact GitHub main
`91ceb0fedcd6bb23513cf414a60b1e506d7de893`, tree
`83b59dffdb8312867a65582d53c55edf2576604a`. The mounted source archive was verified
against SHA-256 `3e7c09713cde735ca525464872d8e9367b5b853b939635adcfbf790198d24af1`
and reconstructed on a private task branch. No user checkout, external configuration
or remote ref was edited. No candidate commit or push was made.

The baseline packaging workflow `36509340996` was freshly observed completed/
success, unlike the earlier in-progress record. That qualifies its own source, not
these new tests. The current packaging plan still says Verifying; external review
and owner disposition remain its separate gate. Prepare this test-only next slice
without changing its acceptance, and integrate in the user's selected order after
that preceding gate is resolved. The older six-slice refactoring and routing-fact
acceptances remain unchanged.

Core and the executable Router selected 20 standards with no unanswered task facts.
Their exact local route/readback is retained with the delivery. The task follows
Implementation's bounded change and Verification's negative-fixture/oracle rules.
The optional local Python 3.12 installation failed on DNS; dependency pins were
not altered to work around the unavailable toolchain.

## Five changes, five existing test owners

| Target | Change | Named regression detected |
| --- | --- | --- |
| Typed routing projection | Three existing negatives compare the complete AnalysisFailure record; normalization remains outside the projection exception scope. | A different code/outcome/message/path/field/observation passing merely because it is AnalysisError. |
| Canonical fact records | Deep-copy the expected record before mutation and check fresh list/dict/value/alias containers. | Returning a shared outer list or nested containers that mutate the expected value with the result. |
| Fact-material dependencies | One private AST predicate uses Python's relative-name resolver; explicit allow/deny fixtures cover static spelling variants. | Absolute, aliased, relative or from-package navigation imports bypassing the old narrow guard. |
| Immutable revision reuse | Substitute an actual successor's aggregate ID into the otherwise unchanged first record. | An identity-blind cached hit or incorrect admission of mismatched record identity. |
| Storage lifecycle | Two real SQLite connections, DELETE journal and an EXCLUSIVE writer exercise the no-work probe. | Incorrect BUSY adaptation, swallowed busy failure, or writer admission before the read probe. |

Four methods are added: two import-predicate fixture methods, one aggregate-identity
method, and one exclusive-lock method. Existing projection/record/dependency methods
are strengthened rather than duplicated. No production implementation, public
contract, catalog, CLI, schema, dependency, CI configuration or persisted format
changes. No MCP restart, migration or configuration update is required by the code.

The unchanged production contracts are the oracle, not an instruction to create
new failure meanings. Applicability owns undeclared-reference and unsupported-type
errors; Analysis maps them to `ROUTER_PROJECTION.INVALID` with `invalid`, the Router
projection path and the respective field/observed details. Authoring's final
record comparison owns `AUTHORING.INVALID_STORED_REVISION` with the exact authority/
identity message. Snapshot Store owns the SQLITE_BUSY → unavailable adaptation.

The dependency predicate is deliberately local to this existing test file. It uses
`ast.Import`, `ast.ImportFrom` and `importlib.util.resolve_name`; it is not a new
production dependency analyzer. Dynamic imports, attribute access and a complete
transitive module graph are excluded. The fixtures include 24 denied spellings
across the two presentation modules and an allowed sample containing unrelated
imports, harmless aliases, longer module names, comments and string literals.
No fixture import statement is executed.

## Normal verification

| Selection | Result |
| --- | ---: |
| Eight complete affected Engine test modules | 97 passed |
| Complete Standards Analysis package | 125 passed |
| Complete Standards Snapshots package | 41 passed |
| Complete Standards Verifier package | 168 passed |
| Total normal selected executions | 431 passed; no failures or skips |
| Sampled-fault evidence | 42 faults rejected by assertions, no incidental test errors |
| Complete structural checkpoint | 73/73 suites, 121 checks passed |
| Generated-contract freshness, syntax and diff checks | Passed; final post-record results ship in DELIVERY/evidence |

The Engine selection includes complete typed edit/projection/workflow tests, fact
ownership, immutable reuse, cold storage-lifecycle transport, logical authoring and
generated-contract tests. Thus real authoring/replay and replacement-process checks
run as regressions in addition to the directly edited tests. This is **not** a full
Engine or all-packages test run. Initial seven- and twelve-test checks and the final
post-record focused rerun overlap this coverage and are not counted a second time.

The first strengthened normal tests passed without production repairs. Existing
verifier tests deliberately print invalid/stale fixture messages; their 168-method
selection ended OK and is not a failed candidate validation. Every execution's
command and output is preserved, including task setup corrections in the ledger.

## Regression-detection experiment

The delivered `prove_regressions.py` loads original test definitions from the exact
base commit and runs them against the same unchanged production code as the new
tests. Fault substitutions exist only inside one `unittest.mock` context. No
production file is mutated, and normal acceptance tests run without these faults.

| Fault family | Samples | Observation |
| --- | ---: | --- |
| Wrong diagnostic fields on real projection errors | 18 | Six distinct fields for each of three real failure cases: original broad tests pass, strengthened tests fail. |
| Shared record containers | 4 | Shared outer list, records, values and aliases each escape the original expectation and fail the detached/freshness checks. |
| Alternate static navigation import spellings | 16 | Inert source-text observations pass the old guard and fail the actual strengthened material-owner guard. |
| Aggregate-ID-blind cache hit | 1 | Original record-mutation cases pass; the new valid-ID substitution is rejected by the test. |
| Wrong or swallowed busy outcome | 2 | The existing authorization-error probe test still passes; the new real exclusive-read case detects each error. |
| Writer acquisition before the read probe | 1 | Even with the same BUSY class/code, the new SQL observation rejects the wrong failure point. |

All 42 faults were detected by assertions, not setup/import/teardown errors. For
41, the specifically recorded counterpart baseline tests accepted the substitution.
This is **not a whole-suite mutation score**: notably, existing writer-contention
tests already exercise some BUSY adaptation. The new evidence is the real read-probe
path, not a claim that no older test could detect a broadly broken adapter. The
writer-before-probe example has no claimed old-suite survivor result.

The diagnostic substitutions preserve real normalization, applicability failure and
projection before altering the returned record. The import substitution changes only
the test's read of supporting.py, not the imported module or its on-disk bytes. The
container faults receive fresh private retained records on each run. The identity
fault omits only aggregate_id from the hit comparison; the normal decoder and all
other record fields remain in use. The SQLite faults still require a genuine
exclusive writer and genuine sqlite3 error rather than injecting a fake busy error.

These finite cases establish the requested test improvements, not complete detection
of all conceivable failures or universal conformance to Python/SQLite behavior.

## SQLite and fixture authority

The new store test establishes DELETE journal mode before contention and seeds an
active snapshot, aggregate head and root through the real module. A second actual
connection owns BEGIN EXCLUSIVE. A test-local shortened busy timeout controls only
that fixture's error wait; no duration or scheduler timing determines success.
The maintenance exception has code `SNAPSHOT_STORE.BUSY`, kind `unavailable`, and an
OperationalError cause with SQLITE_BUSY. Its SQL trace contains the one intended
read, no writer statement; the module holds no transaction and the writer still
owns its transaction. Finally always releases the owned writer, callback and timeout.
Counts are equal before/after contention and after a successful maintenance retry;
content, head and root readbacks remain exact. No sleeps or process kills are used.

The new identity fixture uses a real successor revision to obtain a syntactically
valid different aggregate ID, preventing an earlier malformed-ID rejection from
standing in for identity validation. Canonical decoding is observed on the miss.
After rejection the original cached object is still returned without another
decode, and its stored aggregate remains unchanged.

## Preserved source and integration

Only five existing test files, four new plan/evidence records, one index link and
the generated suite-input manifest are delivered (11 paths). A source-hash pass
checked all 1,498 unaffected tracked baseline files unchanged, including every
production file, earlier plan, configuration and lock. The manifest is regenerated
through `write_suite_input_projection`, not hand-edited. The delivery reconstruction
also verifies every changed file's mode/hash and the entire resulting Git tree.
Engine interface 45 and the packaging format and implementation remain untouched.

Use DELIVERY/README.md and its read-only exact-base preflight before applying the
scoped patch; reconcile later changes rather than overwriting them. Any controlled
fault script requires the original base commit for its baseline-test comparison.
It belongs in a disposable testing environment and is not a shipped production
runtime API or a new mandatory per-commit test framework.

Local execution used Python 3.13.5, SQLite 3.46.1, Git 2.47.3 and rpds-py 2026.5.1.
Supported locked Python 3.12 CI for this candidate and independent review/owner
acceptance remain T-A6/T-A7. No live model session, external review transmission,
remote push or production standards publication occurred. T-A1–T-A5 have direct
local evidence; the plan stays Verifying rather than claiming unsupported acceptance.
Packaging acceptance is still owned by its prior plan and is not silently satisfied
by this independent test work.

After integration on the named base, the repository's Python 3.12.3 environment
passed the four affected selections: 97 Engine, 125 Analysis, 41 Snapshots, and
168 Verifier tests (431 total, no failures). Authoring-purpose repository
verification passed 121 checks across 73 suites with refreshed generated inputs,
and the complete structural check passed. Ruff found seven pre-existing findings
in two touched Engine test files; comparison with their base versions found the
same seven. These local results do not replace hosted CI or owner acceptance.

## Source of the deferred targets

The scope follows the preserved external recommendations, whose original findings
and accepted dispositions are unchanged:

- [Typed routing projection diagnostics](../../typed-routing-edits/reports/external-review.md).
- [Fact-container freshness and static import guard](../../fact-ownership-and-working-set/reports/external-review.md).
- [Aggregate identity variant](../../immutable-work-reuse/reports/external-review.md).
- [Exclusive-read expiry probe](../../storage-lifecycle/reports/external-review.md).
