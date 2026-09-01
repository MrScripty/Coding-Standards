# A2-P5 Combined-Design Efficiency Execution Admission

**Status:** `correction and re-audit admitted; complete measurement blocked`

## Question And Authority Boundary

Is the accepted combined design non-dominated on the current Coding Standards
corpus and a representative controlled-authoring workflow? The selected design
is the P2R2 change-proportional projected-revision material model, the P4R
typed-continuation facade, and P3 verified expected-target publication with
observation-based cold recovery.

P5 measures a design comparison only. It selects no latency, throughput,
memory, capacity, schema, migration, public version, verifier portfolio, or
platform promise. A prototype result can admit the combined design to later
production planning; it cannot establish production performance or authorize
canonical Engine code.

The accepted predecessor authorities are:

- P2R2 evidence commit `b76f443b5bc05b179d20193bf27ea4d3054db7f3`
  for projected-material identity, exact replay, current compiler and Analysis
  composition, change-proportional retained material, and one SQLite aggregate
  owner;
- P3 evidence commit `53fd98f292400aee6929d0cc950cc6163944a5a5`
  for verification-before-publication, expected-target Git publication,
  durable attempt identity, exact observation, and cold recovery; and
- P4R evidence commit `9a0c34325e2849c437072b12b3188bede7f08d4e`
  for the eight-intent, 16-field typed-continuation facade and its 49-fact
  representative workload.

Those earlier observations are design inputs, not reusable P5 measurements or
budgets. P5 must measure the combined candidates again from the exact admitted
base.

## Current Standards Route

The public A1c `create_snapshot` plus `query(route)` path ran on exact base
`b503dcb76fd27aca41df154f37e20f6635de44bf` with all eight development
activities, the Library application, Generated Contract, IPC, and Persistence
boundaries, and Architecture, Contracts, Concurrency, Resilience,
Cross-Platform, Dependencies, Security, Diagnostics, and Performance topics.
It selected 23 standards and returned zero unresolved fact categories:

- `core` and `router`;
- `workflow.planning`, `workflow.implementation`, `workflow.verification`,
  `workflow.documentation`, `workflow.commit`, `workflow.build`,
  `workflow.tooling`, and `workflow.release`;
- `profile.application.library`, `profile.boundary.generated-contract`,
  `profile.boundary.ipc`, and `profile.boundary.persistence`; and
- `topic.architecture`, `topic.contracts`, `topic.concurrency`,
  `topic.resilience`, `topic.cross-platform`, `topic.dependencies`,
  `topic.security`, `topic.diagnostics`, and `topic.performance`.

IPC is newly selected because P5 crosses and measures the Git subprocess
boundary. The private process Adapter must decode a closed action variant
before dispatch, reject extra or malformed fields, avoid a shell, bound output
and time, and distinguish invalid, unsupported, and unavailable outcomes.
Concurrent Plan Integration, Interop, Language Binding, language, framework,
Frontend, Accessibility, and Launcher profiles remain unselected.

### Frozen Private Process Contract

The private process request envelope has exactly five required fields and no
optional or extra fields: `category`, `action`, `contract_version`,
`correlation_id`, and `payload`. `category` is exactly `git`,
`contract_version` is integer `1`, `correlation_id` matches
`^a2p5:[0-9a-f]{24}$`, and `payload` is a mapping decoded into one of these
closed variants:

| Action | Exact payload and cross-field rules |
| --- | --- |
| `clone-local` | `{source, destination}`; both are normalized absolute paths without NUL or newline, `source` equals the Adapter-configured local repository, and `destination` is an absent, nonsymlinked descendant contained by the Adapter-owned scratch root; source-object presence is not trusted pre-spawn |
| `add-all` | `{}`; operates only in the configured isolated candidate worktree |
| `write-tree` | `{}`; operates only in the configured isolated candidate worktree |
| `commit-tree` | `{tree_oid, parent_oid, message}`; OIDs are 40- or 64-character lowercase hexadecimal values, `parent_oid` equals the captured expected base, and the UTF-8 message is 1 through 160 bytes with no NUL, CR, or LF |
| `resolve-target` | `{}`; reads only clone-local `refs/heads/main` |
| `update-target` | `{candidate_oid, expected_oid}`; both use the OID rule, `expected_oid` equals the captured admitted-base target, and the Adapter executes one compare-and-swap update of only clone-local `refs/heads/main` |
| `git-version` | `{}`; records the Git implementation used by the experiment |

Every required payload field has the displayed type and bound; every missing,
extra, wrong-type, out-of-bound, path-escape, symlink-escape, OID-shape, or
cross-field mismatch is invalid before spawn. The decoder returns a frozen
typed variant, and the handler receives only that variant, never the producer's
raw mapping. Producer-side typing is not trusted. The child receives no shell,
`LC_ALL=C`, an allowlisted executable search path, the Adapter-owned working
directory, and only the deterministic author/committer variables required by
`commit-tree`.

Every invocation has an exact 30-second timeout and independently bounded
stdout and stderr of at most 262,144 bytes each. The outbound value has exactly
`{kind, action, returncode, stdout, stderr}`: `kind` is `process-result`,
`action` equals the decoded request action, `returncode` is an integer from
-255 through 255, and stdout/stderr are strictly decoded UTF-8 strings whose
encoded byte lengths meet the bound. The outbound value is decoded and
validated before domain use. A nonzero but well-formed Git result remains a
domain input; for example, a failed `update-target` becomes target-stale only
after exact target observation.

The process-negative fixtures cover missing and extra envelope fields; wrong
envelope types and bounds; every recognized action with a missing, extra,
wrong-type, out-of-bound, or cross-field-invalid payload; unknown category;
unknown action; mismatched category/action; a declared action with no decoder;
an unavailable executable; a producer-only typed value; an attempted raw-
mapping handler bypass; timeout; stdout or stderr over the bound; strict output
decode failure; and the registered clone-local first-child spawn, pre-child
containment-proof, child-two spawn, post-child containment-proof, and
missing-admitted-object variants. Each clone fixture records its two child
slots, actual started count, destination cleanup, configured-source identity,
and absence of unrelated state. Every valid variant also executes against real
scratch Git on both runtimes.

Missing decoder/executable, first-child spawn capability, or pre-child
containment proof is a pre-spawn capability failure: no child, domain, durable,
or Git mutation occurs. Once a child starts, timeout, oversized or undecodable
output, later-child spawn failure, containment-proof loss, or unavailable
required action completion is a post-spawn result failure: success is never
inferred. Setup and read-only actions create no application attempt; staging
and publication actions retain the attempt at the exact phase registered
below. Exact scratch object, candidate identity, and target observation decide
recovery. The command is never blindly retried.

Every decoded `clone-local` action owns exactly two Git children in this order:

1. `git clone --no-checkout --local --no-hardlinks --quiet -- SOURCE DEST`; and
2. `git -C DEST checkout --quiet -B main ADMITTED_BASE`.

`SOURCE`, `DEST`, the Git executable, and `ADMITTED_BASE` are Adapter-owned
decoded/configured values, never producer command fragments. This fixed
sequence materializes scratch `refs/heads/main` directly at the admitted OID,
independent of the source worktree's current branch, default branch, later
prototype commit, or archive ref. It remains one `clone-local` action with the
same two-field payload, not an eighth process action.

Pre-spawn decoding proves only the exact configured source identity and path
contract; it does not claim that an object exists. Successful completion of
child two, followed by independent `resolve-target`, is the only admitted-base
object/ref proof. A missing admitted object therefore produces child two's
well-formed nonzero Git result, cleanup, and the caller's registered
`A2P5.PROCESS_RESULT_UNAVAILABLE` classification.

The action has one cumulative 30-second deadline. Each child starts in a new
owned process group. Stdout bytes and stderr bytes are accumulated separately
in child order with no inserted bytes and each accumulated stream retains the
262,144-byte bound; only the aggregate is strictly UTF-8 decoded into the
existing five-field outbound value. The action return code is the first
nonzero child code, or zero only when both children return zero. If child one
fails, child two does not start. On either nonzero result, timeout, output-bound
failure, spawn failure, or decode failure, the Adapter terminates and reaps the
active group and all descendants and removes any destination. A successful
second child retains the destination.

Failure to find the decoder/executable or to start child one before any child
exists is `A2P5.PROCESS_CAPABILITY_UNAVAILABLE`. Once any child has started, a
child-two spawn failure, timeout, output-bound failure, or strict outbound
decode failure is `A2P5.PROCESS_RESULT_UNAVAILABLE`. A well-formed nonzero
child result remains the existing process-result domain input; `clone-local`'s
caller classifies it as `A2P5.PROCESS_RESULT_UNAVAILABLE`. These are instances
of the existing two process triples, not new conditions. The outer process
trace, not the closed outbound value, records two ordered child slots and an
actual started-child count of 0, 1, or 2; both-started is exactly two, and a
valid successful action requires both. No Git child runs beside or outside
this ownership. An independent `resolve-target` then proves the new clone's
`refs/heads/main` equals the admitted base.

The scratch-root threat model is one serial Adapter owner and no concurrent
process with that owner's filesystem identity or access to its mode-0700
temporary root. At construction, decode, immediately before each child,
between children, and before cleanup or acceptance, the Adapter uses `lstat`
to revalidate the root and every existing destination ancestor against its
captured device/inode/owner identity and requires nonsymlinked directories;
the destination is absent before child one and a contained nonsymlinked
directory before child two. A changed ancestor, unexpected entry, or missing
exclusive-owner fact is pre-spawn capability-unavailable when no child has
started and result-unavailable after a child starts. This bounded proof
lifetime does not claim containment against a concurrent same-owner attacker.

## Candidate Portfolio

| ID | Exact candidate | Selection role |
| --- | --- | --- |
| `selected` | P2R2 immutable revision plus bounded projected-material reference and exact-replacement overlay; P4R typed-continuation facade; P3 isolated verification, expected-old-target publication, exact observation, durable attempt, and recovery | candidate under test |
| `full-material` | same facade, current compiler/Analysis work, candidate bytes, verification, publication, and recovery, but each revision retains the complete projected corpus instead of bounded reference plus exact change material | ranking-eligible correctness-equivalent material baseline; prohibited from production by A1c no-full-corpus-per-edit authority |
| `flexible-facade` | same selected material and P3 application path, but P4R's exact correctness-equivalent 20-field flexible facade repeats proposal identity on revise, accepts optional prior Analysis on analyze, and repeats proposal plus expected revision with optional prior readiness on review | ranking-eligible correctness-equivalent caller-knowledge baseline |
| `unsafe-publication` | unchecked target update and publish-before-verify controls from P3 | correctness negatives only; excluded from efficiency ranking |

Minimal merged goals, tagged dispatch, A1c overload, proposal-as-snapshot,
caller Git facts, mutable current-evidence selection, and another Analysis
authority are correctness-incomplete or prohibited and cannot enter dominance
ranking. The `full-material` plus `flexible-facade` cross-product is omitted:
it adds the independently measured costs of both baselines and has no distinct
deciding value. No baseline creates a prospective production strategy Seam,
registry, or public selector.

Before any efficiency comparison, `full-material` and `flexible-facade` must
produce the same projected corpus bytes, compiler and Analysis result,
revision-bound handle chain, typed caller results, verified candidate tree and
object identity, expected-target publication postcondition, and cold recovery
outcome as `selected`.

The flexible field inventory is exact: create 3, find 2, revise 4, query 2,
analyze 2, review 5, apply 1, and recover 1, for 20 defined fields versus the
selected facade's 16. The representative workload omits optional prior
Analysis and prior readiness because it performs no reuse operation; they
remain defined fields and cannot disappear from the surface metric.

## Frozen Workloads

Every case begins from a fresh disposable clone of the exact base and a fresh
scratch SQLite store. An independent fixture builder derives replacement
bytes through a scratch reference tree. When a source edit changes the
repository-index projection, the fixture includes the exact regenerated
`evaluation/standards-effectiveness/generated/suite-inputs.json` replacement
for both candidates; generated bytes are never hidden from change accounting.
The configured publication target is exactly the clone-local
`refs/heads/main`. Before measurement, both that ref and its captured expected
OID must resolve to admitted base
`b503dcb76fd27aca41df154f37e20f6635de44bf`; any other initial identity makes
the fixture unavailable. No alternate or synthetic ref represents configured-
main application.

The normal one-revision workflow `W1` performs 11 A2 calls plus one or two
unchanged A1c `resolve` calls: create; close/reopen and find; revise;
historical read; current read; route; related; analyze; resolve every exact
current obligation; review; isolated stage and verify; expected-target apply
with exact post-observation; and cold recovery. Every `W1` create supplies one
current-byte Commit replacement plus one rationale: base 1, mutation 3, and
semantic proposal 2, for 6 leaves. Find supplies zero leaves.
Historical read and current read supply 3 leaves each; route with empty facts
supplies 2; related supplies revision, kind, target, one group, direction, and
transitive for 6; analyze supplies 1; each unchanged A1c resolve supplies 10;
review supplies Analysis plus three exact owner/accept pairs for 7; apply and
recover supply 1 each. The one-resolution non-revise inventory totals 40; the
two-resolution multi-file inventory adds 10.

The common leaf-value inventory is frozen as follows. An opaque handle leaf
always equals the exact handle carried by the named preceding result; it is
never reconstructed or replaced by repository facts.

- `create.base-snapshot` is the handle returned by current A1c
  `create_snapshot` for the admitted base. The create mutation is exactly
  `{op: "replace", path: "workflows/commit.md", value: <admitted bytes>}`.
  Its semantic proposal is exactly
  `{kind: "rationale", text: "measure the admitted combined design"}`.
- `find_proposals` omits both optional fields. Its rediscovered head is the
  expected revision supplied to revise. Each valid revise mutation is an exact
  `{op: "replace", path, value}` tuple from the case table, in displayed path
  order, and its sole semantic proposal is exactly
  `{kind: "rationale", text: "measure exact replacement revision"}`.
- Historical query supplies the immediately preceding revision, request kind
  `read`, and target `workflow.commit`. Current query supplies the newly
  revised revision with the same kind and target. Route supplies the current
  revision and exactly `{kind: "route", facts: {}}`. Related supplies the
  current revision and exactly `{kind: "related", target:
  "workflow.commit", groups: ["standards-requires"], direction:
  "outgoing", transitive: false}`.
- Analyze supplies the current revision. The private material seam feeds the
  current Analysis kernel exactly
  `{kind: "modification", accepted_ids: ["workflow.commit.commit-message"],
  proposed_ids: ["workflow.commit.commit-message"], scope: {kind:
  "whole-artifact"}}` when Commit is replaced. When Planning is also replaced,
  it appends the same exact descriptor shape with both ID arrays containing
  only `workflow.planning.projection-completeness`.
  The generated suite-input replacement is derived evidence, not another
  semantic descriptor. The current Analysis state's `semantic_proposals` is
  exactly empty: A2 rationale remains Authoring material and is not coerced to
  the distinct A1c semantic-proposal contract. Repository-owned coverage
  attestations are loaded by the current A1c decision path. The initial result
  must have no fact or coverage work and exactly one `consumer-disposition` target,
  `commit-consolidation-dispositions`; multi-file additionally has second
  target `policy-semantic-impact`, in that order.
- Each unchanged A1c resolve supplies the exact current PendingResult analysis
  and obligation handles, `kind: "consumer-disposition"`, result
  `reviewed-no-change`, rationale
  `The exact selected consumer was reviewed.`, the exact obligation fingerprint,
  and one evidence reference. Evidence ID is `a2p5.review.` plus the exact
  target, its digest is SHA-256 of that UTF-8 ID, and its provider contract and
  version are `repository-content` and `1`. The admitted exact authorizer
  permits `standards.review.consumer` only with that evidence contract. After
  the first multi-file resolve, only `policy-semantic-impact` remains; the
  final resolve returns current A1c `complete-result` with no next operation.
- Review supplies the completed Analysis handle and the three decisions, in
  order, `{owner: "consumer", decision: "accept"}`,
  `{owner: "impact", decision: "accept"}`, and
  `{owner: "audit", decision: "accept"}`. Apply supplies the returned
  readiness handle; recovery supplies the returned application handle.
- The flexible baseline additionally supplies the proposal carried by the
  create result on every revise, and supplies that proposal plus the reviewed
  revision on final review. It omits optional prior Analysis and prior
  readiness in this no-reuse workload.

The exact 40 common non-revise leaf names and values are:

| Count | Leaf names | Exact values |
| ---: | --- | --- |
| 6 | `create.base-snapshot`; `create.mutation.op`; `create.mutation.path`; `create.mutation.value`; `create.semantic.kind`; `create.semantic.text` | base handle; `replace`; `workflows/commit.md`; admitted bytes; `rationale`; `measure the admitted combined design` |
| 3 | `query.historical.revision`; `query.historical.request-kind`; `query.historical.target` | immediately preceding revision handle; `read`; `workflow.commit` |
| 3 | `query.current.revision`; `query.current.request-kind`; `query.current.target` | current revision handle; `read`; `workflow.commit` |
| 2 | `query.route.revision`; `query.route.request-kind` | current revision handle; `route` |
| 6 | `query.related.revision`; `query.related.request-kind`; `query.related.target`; `query.related.group-1`; `query.related.direction`; `query.related.transitive` | current revision handle; `related`; `workflow.commit`; `standards-requires`; `outgoing`; `false` |
| 1 | `analyze.revision` | current revision handle |
| 10 per resolve | `a1c-resolve.analysis`; `a1c-resolve.submission.kind`; `a1c-resolve.obligation`; `a1c-resolve.result`; `a1c-resolve.rationale`; `a1c-resolve.evidence.id`; `a1c-resolve.evidence.digest`; `a1c-resolve.evidence.provider-contract`; `a1c-resolve.evidence.provider-version`; `a1c-resolve.fingerprint` | current analysis handle; `consumer-disposition`; exact current obligation handle; `reviewed-no-change`; displayed exact rationale; target-derived evidence ID; SHA-256 of ID; `repository-content`; `1`; exact current obligation fingerprint |
| 7 | `review.analysis`; `review.consumer.owner`; `review.consumer.decision`; `review.impact.owner`; `review.impact.decision`; `review.audit.owner`; `review.audit.decision` | completed Analysis handle; `consumer`; `accept`; `impact`; `accept`; `audit`; `accept` |
| 1 | `apply.readiness` | returned readiness handle |
| 1 | `recover.application` | returned application handle |

Counting retains P4R's rule: an opaque generated handle or immutable
result-carried fingerprint is one caller fact because the caller only returns
it to its declared continuation; every authored mutation, request, rationale,
evidence, or decision leaf is counted separately.

The prototype-only Analysis execution authority is the exact
`AuthorizationAuthorityContract` tuple: issuer `issuer.a2p5`, issuer semantic
revision `1`, principal `principal.a2p5`, authorization contract
`authorization-grant.v1`, authorization evidence contracts exactly
`(repository-content@1)`, revocation authority `revocation.a2p5`, revocation
authority semantic revision `1`, revocation contract
`authorization-revocation.v1`, and revocation evidence contracts exactly
`(repository-content@1)`.

Its exact `AuthorizationClaim` echoes action `consumer-disposition`, literal
subject kind `obligation`, the current obligation's exact domain ID, and
capability `standards.review.consumer`. Submission evidence is the one request
reference above resolved to bytes equal to its UTF-8 ID. Therefore the Commit
target reference digest is
`sha256:f85c5977c238625e24ccc2bbbcb110a3cab5685272a26015e72c43b16b314004`
and the Planning target reference digest is
`sha256:fed5bdd466219e964fd9d5f3ada0c96a5a94814ba3685d7c3c5a0c012475b1bf`.
Authorization evidence is exactly one `repository-content@1` reference with
ID/content bytes `a2p5.authorization-grant` and digest
`sha256:9a120e40734410f6c077914f76e46acd115d4787107105663d3af382c97d0166`.
Revocation evidence is exactly one `repository-content@1` reference with
ID/content bytes `a2p5.authorization-revocation` and digest
`sha256:76b851ca81a44acedc399e06dfccf9d4b813498a707894de255e272731c79ac5`.
The claim returns revocation state `not-revoked` and decision `allow`; every
action, subject-kind, subject-ID, capability, evidence-reference, evidence-byte,
or contract mismatch is unauthorized. This authority is an A1c execution
fixture, not another Analysis owner or production authorization decision.

For each valid revise, the exact names are `revise.expected-revision`, then
`revise.mutation-J.op`, `.path`, and `.value` for each one-indexed mutation in
displayed order, followed by `revise.semantic.kind` and
`revise.semantic.text`; values are respectively the rediscovered/current head,
`replace`, the displayed path and derived exact bytes, `rationale`, and
`measure exact replacement revision`. The invalid revise uses only expected
revision plus mutation-1's three named leaves. Flexible adds
`flex.revise.proposal` on every revise and `flex.review.proposal` plus
`flex.review.expected-revision` on final review. Multiple occurrences of an
operation append one-indexed `@N` to their inventory key for counting while
retaining the same semantic leaf name and exact value rule.

Each valid revise supplies expected revision (1), 3 leaves per replacement,
and one rationale (2). The flexible facade supplies the same leaves plus
proposal on revise and proposal plus expected revision on review, for three
additional leaves. Optional prior Analysis/readiness inputs are omitted. The
exact per-case inventories are therefore:

| Case | Exact input and expected work |
| --- | --- |
| `no-op` | `W1`; revise with one exact replacement of `workflows/commit.md` with its current bytes plus one rationale. Effective content delta is zero; the authored replacement payload remains counted. One exact A1c resolve completes Analysis. Exact selected/flexible totals: 46/49 leaves. |
| `small-edit` | `W1`; revise with the Commit edit, regenerated suite-input replacement, and one rationale. Append exactly `\n<!-- A2-P5 small edit -->\n` to `workflows/commit.md`. One exact A1c resolve completes Analysis. Exact selected/flexible totals: 49/52 leaves. |
| `multi-file` | `W1`; revise with Commit, Planning, and regenerated suite-input replacements plus one rationale. Append exactly `\n<!-- A2-P5 commit edit -->\n` to `workflows/commit.md` and exactly `\n<!-- A2-P5 planning edit -->\n` to `workflows/planning.md`. Two exact ordered A1c resolves complete Analysis. Exact selected/flexible totals: 62/65 leaves. |
| `invalid-edit` | Create and cold-find, then attempt one replacement `{op: "replace", path: "workflows/a2-p5-missing.md", value: <admitted Commit bytes>}` with an empty semantic-proposal list. Expect typed unavailable, no head movement, no analysis/readiness/attempt, and no staging or Git publication. The selected and flexible leaf inventories contain exactly 10 and 11 facts. |
| `repeated-revision` | `W3`; three cumulative revisions, each appending exactly `\n<!-- A2-P5 repeated N -->\n` to `workflows/commit.md` for `N` equal to 1, 2, and 3 and replacing the regenerated suite-input projection. Each revise uses the common rationale. For revision N, historical query uses revision N-1 and current/route/related/analyze use revision N, all with the common exact values; one exact A1c resolve completes each Analysis. Only revision 3 receives the common review/apply/recovery. Exact totals are 23 A2 calls plus three A1c resolves and 117/122 selected/flexible facts. Every prior revision and Analysis remains addressable. |

The invalid case is paired with an unmeasured valid source fixture containing
the same create/find calls, one replacement of `workflows/commit.md` with the
same admitted Commit bytes, and an empty semantic-proposal list; only its
target path changes. The prototype must encode the complete admission-owned
required and supplied leaf names and values for every case and derive the
displayed totals from those sets. No fixture may alter commit metadata,
workload scale, validator choice, or another condition between candidate and
baseline.

Before freezing this workload, an actual canonical A1c create/prepare/resolve
probe on the admitted base ran in CPython 3.11.14 with SQLite 3.50.4 and CPython
3.12.3 with SQLite 3.45.1. On both, the Commit descriptor returned only
`commit-consolidation-dispositions` and one current resolve returned
`complete-result`; Commit plus Planning returned those two registered targets
in order, the first resolve left only `policy-semantic-impact`, and the second
returned `complete-result`. This validates the workload shape, not projected-
material equivalence or P5's terminal verdict; the isolated prototype must
reproduce it for every ranked candidate.

## Measurement Contract

An outer collector, independent of candidate accounting, owns the frozen
workload, leaf inventory, clock, process trace, filesystem measurements, and
SQLite inspection. It records these dimensions separately and never produces
a weighted score:

1. A2 and unchanged-A1c public call occurrences;
2. defined facade fields, supplied atomic caller facts, result-carried handles,
   and ambiguous next actions;
3. base corpus file count, logical bytes, and digest;
4. changed-path count, projected corpus bytes, differing byte positions,
   length delta, canonical replacement payload bytes, semantic-proposal bytes,
   and generated-projection bytes;
5. logical incremental durable bytes by proposal, revision, material reference,
   exact change material, Analysis, dependency, readiness, and application
   attempt records, measured from canonical serialized records;
6. SQLite page-size times page-count and filesystem apparent/allocated bytes,
   with database, WAL, and SHM observations reported separately from logical
   retained bytes;
7. sampled peak scratch apparent and allocated bytes at post-authoring,
   post-materialization, post-verification, post-publication, and post-recovery,
   including projected files, Git objects, worktrees, and stores;
8. material-resolution accesses plus Git and total process calls by closed
   Adapter action and workflow phase; and
9. raw `time.perf_counter_ns` observations for authoring, query,
   analysis/resolve, review, stage/materialize, verify, publish, recovery, and
   end-to-end `create_proposal` through terminal cold recovery.

Every metric is encoded as an exact applicability record. An applicable true
zero is distinct from missing evidence; a nonapplicable value has no numeric
value and one registered reason. Missing, extra, defaulted, or contradictory
dimensions are unavailable and cannot be converted to zero. Every applicable
structural and timing dimension reports the three selected values, three
baseline values, their separate minimum/median/maximum summaries, and the
three paired baseline-minus-selected differences. The raw pairs, not their
summaries, decide dominance.

The valid `no-op`, `small-edit`, `multi-file`, and `repeated-revision`
workloads execute all five scratch checkpoints and all nine timing phases. The
`invalid-edit` workload executes only the `post-authoring` scratch checkpoint,
the `authoring` timing, and an `end-to-end` timing that starts immediately
before `create_proposal` and stops immediately after the typed unavailable
`revise_proposal` result. Its query, analysis/resolve, review,
stage/materialize, verify, publish, and recovery timings and its four later
scratch checkpoints are exactly nonapplicable with reason
`workflow-terminated-before-phase`. All other declared structural dimensions
remain applicable for `invalid-edit`; an established absence such as zero
application-attempt bytes or zero staging calls is an explicit measured zero.
The post-failure ref, store, and process nonmutation oracles run outside the
end-to-end interval.

Dominance compares a case/dimension only when it is applicable for both paired
candidates. Matching registered nonapplicability removes that dimension only
for that case. An applicability mismatch, an unregistered reason, or an
applicable missing observation makes the comparison unavailable and returns
`revise`. This is the complete applicability matrix; execution may not choose
another treatment after observing results.

For correctness-equivalent candidates, fewer calls, defined fields, supplied
facts, ambiguities, logical durable bytes, allocated bytes, scratch bytes,
material accesses, process calls, and consistently ordered time are better.
Base corpus and changed-material measures describe the common workload and do
not rank a candidate. Result-carried handle count is a continuation-
completeness constraint, not a lower-is-better metric.

Fixture clone/build and teardown costs are measured and reported separately;
they are excluded from the comparable end-to-end interval. The selected
logical revision state is change-proportional only if its reachable serialized
closure contains fixed-size identities/dependency rows plus canonical authored
change material and no serialized untouched base or projected corpus term.
SQLite allocation is descriptive and cannot substitute for that structural
accounting.

## Environment And Variability

Execute the complete workload separately in the dependency-complete
`/tmp/coding-standards-a1c-py311` and
`/tmp/coding-standards-a1c-py312` environments with `PYTHONPATH=.`,
`PYTHONDONTWRITEBYTECODE=1`, and safe-path `-P`. Record exact CPython, SQLite,
Git, kernel, CPU, available memory, filesystem type/block size, admitted commit,
corpus identity, and relevant environment flags. Do not pool runtimes.

For every runtime, candidate, and workload case, perform one untimed warm-up
and then three measured fresh-scratch observations. Rotate candidate order per
repetition so one candidate is not always warmed by the other. Retain every
raw observation and report minimum, median, maximum, and paired differences.
Timing has a consistent direction only when all three paired differences have
the same sign on both runtimes; otherwise it is `overlapping` and cannot decide
dominance. Structural byte, call, field, fact, and process counts remain exact
independent dimensions. No absolute or percentage latency threshold is
inferred.

If dominance would depend on an overlapping timing dimension after structural
metrics are considered, the timing oracle is `unavailable` and the prototype
returns `revise`; it does not add samples or change the variability rule after
observing results.

### Raw Evidence And Outer Recalculation

Each runtime emits one closed raw-evidence document. Its provenance binds the
actual prototype-source SHA-256, this admission's content SHA-256, admitted
commit and tree, current A1c Interface/manifest digest, exact configuration
digest, runtime executable, and complete ordered corpus manifest. The
configuration material covers candidate roles, case mutations, field and leaf
inventories, process contract and bounds, failure and interruption scenario
IDs, metric IDs and applicability, repetition/rotation rules, and the
dominance rule. The document retains the exact 15 warm-ups, 45 measured
observations, full fact inventories or their content-addressed bytes, raw
metrics, complete reachable durable rows and blobs, process/failure evidence,
interruptions, and unsafe-control evidence.

Producer diagnostics, checks, comparisons, status labels, and verdicts are
nondeciding. The two-report combiner strictly decodes both documents, rejects
unknown or missing fields, recomputes the complete execution matrices,
inventories, caller facts, equivalence, reachable closure, metric vectors,
summaries, paired differences, timing directions, and dominance directly from
raw evidence, and requires identical frozen configuration/corpus authority
with distinct exact CPython 3.11 and 3.12 environments. It cannot hard-code or
trust a completeness claim.

The combiner also requires a closed external-gate bundle bound to the same
source SHA, admission SHA, configuration digest, corpus digest, exact prototype
commit and tree, and audit subject identities. It records independent
specification and standards audit results, the complete repository-checkpoint
result, exact staged-scope/base/path review, sensitive-value review, and
conventional Commit subject/body review. The exact archive ref and protected
OID are included once created. The measurement script cannot self-certify
those authorities.

Missing, mismatched, stale, or inconclusive external evidence returns `revise`
with typed unavailable. A completed audit returns `reject` only when it
conclusively establishes that the selected registered design itself violates
A1c preservation, correctness, storage, IPC, a supported platform, or the
dominance rule. A correctable prototype or evidence-implementation defect that
does not change the registration returns `revise`, including when the defect
occurs at one of those boundaries; it does not by itself disprove the selected
design. A failing
repository checkpoint, staged-scope review, sensitive-value review, archive
check, or conventional Commit review is a correctable integration defect and
returns `revise` until the exact corrected source/commit and every affected
gate are rerun. Only the combined raw reports plus a passing bound bundle may
return `pass`.

## Correctness And Failure Oracles

The independent correctness authorities are the current compiler and Analysis
kernel, actual generated A1c DTOs and operation manifest, real scratch SQLite
with close/reopen, real scratch Git with deterministic candidate metadata and
expected-old-target update, external filesystem accounting, and the outer
monotonic clock. Candidate self-report is not a deciding oracle.

Each valid candidate must verdict-gate:

- exact projected bytes against the independently materialized reference tree;
- identical compiler/semantic and Analysis evaluation signatures;
- immutable proposal/revision/history identity and exact cold replay;
- distinct Authoring identities for no-op or same-content revisions while any
  internal material deduplication remains lifecycle-neutral;
- canonical route/read/related requests and unchanged A1c resolve meanings;
- one Authoring Module, one Analysis authority, and one SQLite aggregate owner;
- identical verified candidate tree/object identity;
- verification before publication, expected-target CAS, exact post-observation,
  durable attempt identity, and truthful cold recovery;
- exact current eight A1c roots and capabilities; and
- no caller repository, ref, OID, store, resolver, verification, capability, or
  completion fact.

The following prototype-local triples and postconditions are predeclared:

| Condition | Code | Outcome | Bounded message and postcondition |
| --- | --- | --- | --- |
| malformed, add, duplicate, traversal, or extra-field revise mutation | `A2P5.MUTATION_INVALID` | `invalid` | `replacement mutation is not canonical`; source proposal/head remains exact, no new revision/Analysis/readiness/attempt exists, target remains expected, and no scratch Git action starts |
| canonical absent revise target | `A2P5.MUTATION_TARGET_UNAVAILABLE` | `unavailable` | `replacement target is unavailable`; source proposal/head remains exact, no new revision/Analysis/readiness/attempt exists, target remains expected, and no scratch Git action starts |
| projected content fails current validation during revise | `A2P5.PROJECTED_MATERIAL_INVALID` | `invalid` | `projected material failed canonical validation`; source proposal/head remains exact, no new revision/Analysis/readiness/attempt exists, target remains expected, and no scratch Git action starts |
| staged candidate/reference bytes differ before verification | `A2P5.CANDIDATE_DIVERGED` | `invalid` | `candidate bytes differ from the reference material`; attempt retains candidate identity at phase `candidate-diverged` with verification pending, target remains expected, cold recovery is `unchanged` without changing that phase, and candidate is nonauthoritative |
| expected proposal head is stale | `A2P5.REVISION_STALE` | `invalid` | `expected revision is not the proposal head`; actual proposal/head remains exact, no new revision/Analysis/readiness/attempt exists, target remains expected, and no scratch Git action starts |
| apply authority absent | `A2P5.UNAUTHORIZED` | `unauthorized` | `required authorization is unavailable`; an unauthorized attempt has no candidate, no staging Git action occurs, target remains expected, and cold recovery records phase `rejected` and outcome `unauthorized` |
| selected verification rejects | `A2P5.VERIFICATION_FAILED` | `rejected` | `candidate verification failed`; candidate is staged, verification is `failed`, attempt phase and cold recovery are `verification-failed`, configured target remains expected, and candidate is not authoritative |
| configured target changes before CAS | `A2P5.TARGET_STALE` | `unavailable` | `configured target changed before publication`; verified candidate and attempt are retained, CAS does not overwrite the independently created competing OID, and cold recovery records phase/outcome `stale-target` with that competing target |
| observation unavailable after successful CAS | `A2P5.OBSERVATION_UNAVAILABLE` | `unavailable` | `publication outcome is unavailable`; verified candidate and phase `publishing` are retained, an independent probe confirms target equals candidate, unavailable cold observation leaves recovery outcome unset and phase `publishing`, and success is not inferred |
| unverified candidate observed as target | `A2P5.OBSERVATION_CONTRADICTORY` | `invalid` | `publication observation contradicts the recorded attempt`; target equals the staged candidate while verification is not passed, and cold recovery records phase `recovery-required` and outcome `invalid` without rollback |
| injected application interruption | `A2P5.APPLICATION_INTERRUPTED` | `unavailable` | `application response was interrupted; recover the recorded attempt`; retain the attempt and apply the exact cold-recovery matrix below |
| baseline projection differs before analyze | `A2P5.BASELINE_NOT_EQUIVALENT` | `invalid` | `candidate baseline is not correctness-equivalent`; divergent revision remains its isolated head, no Analysis/readiness/attempt exists, target remains expected, and all baseline metrics are excluded |
| outer metric removed after terminal recovery | `A2P5.MEASUREMENT_UNAVAILABLE` | `unavailable` | `required comparative measurement is unavailable`; candidate target and attempt remain terminal `applied`, no domain state changes, and verdict is `revise` |
| malformed process envelope or recognized-action payload | `A2P5.PROCESS_INVALID` | `invalid` | `process action payload is invalid`; no child, application attempt, durable mutation, or Git mutation occurs |
| well-formed unknown or mismatched process pair | `A2P5.PROCESS_UNSUPPORTED` | `unsupported` | `process action is unsupported`; no child, application attempt, durable mutation, or Git mutation occurs |
| decoder, executable, first-child spawn capability, or pre-child containment/owner proof unavailable before any spawn | `A2P5.PROCESS_CAPABILITY_UNAVAILABLE` | `unavailable` | `required process capability is unavailable`; no child, application attempt, durable mutation, or Git mutation occurs |
| timeout, output bound/decode, later-child spawn or containment proof, nonzero clone completion including missing admitted material, or another required bounded action outcome unavailable after spawn | `A2P5.PROCESS_RESULT_UNAVAILABLE` | `unavailable` | `required bounded process outcome is unavailable`; success is not inferred and the exact action-specific postcondition below applies |

Each negative differs from its valid source fixture in only the named
condition. The oracle captures exact Authoring records, SQLite rows, target ref
and object, scratch artifacts, authorization trace, and process trace before
and after. The verdict fails if a registered triple is unexercised, a message
is unbounded or sensitive, or an unrelated state changes.

For the post-spawn process failure, each action has one frozen source fixture.
`git-version` exercises the real 30-second timeout; `clone-local`, `add-all`,
and `resolve-target` reject stdout over the bound; `write-tree`, `commit-tree`,
and `update-target` reject stderr over the bound. The injected child completes
the named action before an output-bound rejection so its postcondition is
deterministic. Auxiliary `update-target` fixtures cover expected, third, and
unavailable target observations. Separate `clone-local` fixtures exercise
strict output decode failure, child-two spawn failure, post-child containment
proof loss, and a well-formed nonzero checkout for missing admitted material;
each has at least one actual child start, removes the destination, leaves the
configured source unchanged, and creates no accepted clone. The exact results
are:

| Action with unavailable result | Exact state and cold result |
| --- | --- |
| `git-version` | no attempt exists, no Git or durable state changes, and cold application recovery is inapplicable |
| `clone-local` | no attempt exists; the rejected destination is removed, the configured source is unchanged, no accepted clone exists, and cold application recovery is inapplicable |
| `resolve-target` | no attempt exists; an independent probe confirms the clone-local target remains the admitted expected OID, no Git or durable state changes, and cold application recovery is inapplicable |
| `add-all` | authorized attempt remains phase `staging`; the complete index equals the admitted-base index with only the named replacement entries changed, so cached diff contains exactly those paths and bytes; candidate identity is absent, target remains expected, and cold recovery is `unchanged` while retaining phase `staging` |
| `write-tree` | authorized attempt remains phase `staging`, the independently identified unreferenced tree exists, candidate identity is absent, target remains expected, and cold recovery is `unchanged` while retaining phase `staging` |
| `commit-tree` | authorized attempt remains phase `staging`, the independently identified unreferenced deterministic commit exists, candidate identity is absent, target remains expected, and cold recovery is `unchanged` while retaining phase `staging` |
| `update-target` | primary fixture retains verified candidate and phase `publishing`; target equals candidate and cold recovery records phase/outcome `applied`. Auxiliary observations require target expected and `unchanged` with phase `publishing`, a third OID and phase/outcome `stale-target`, or unavailable observation with phase `publishing` and unset recovery outcome. |

### Interruption And Cold-Recovery Matrix

For `selected`, `full-material`, and `flexible-facade` on both runtimes, one
independent scenario injects each interruption after the named durable state
and before returning a successful application response. The immediate typed
result is `A2P5.APPLICATION_INTERRUPTED`; a newly opened store and process
Adapter then recover using only the retained attempt and authoritative target:

| Injection point | Required durable and Git state before reopen | Exact cold result and postcondition |
| --- | --- | --- |
| before staging | authorized attempt phase is `created`; verification is `pending`; candidate identity is absent; target equals expected | `unchanged`; phase remains `created`, verification remains `pending`, target remains expected, candidate remains absent, and durable recovery outcome becomes `unchanged` |
| during staging | attempt phase is `staging`; `add-all` completed; the complete index equals admitted base with only the named replacement entries changed and cached diff contains exactly those paths and bytes; `write-tree` has not started; candidate identity is absent; target equals expected | `unchanged`; phase remains `staging`, the exact index remains scratch-only, candidate remains absent, target remains expected, and durable recovery outcome becomes `unchanged` |
| during verification | candidate identity is durable; phase is `verifying`; verification is `pending`; target equals expected | `unchanged`; phase remains `verifying`, verification remains `pending`, candidate remains nonauthoritative, target remains expected, and durable recovery outcome becomes `unchanged` |
| after verification and before publication | verification is `passed`; phase is `verified`; target equals expected | `unchanged`; phase remains `verified`, verification remains `passed`, candidate remains nonauthoritative, target remains expected, and durable recovery outcome becomes `unchanged` |
| after successful CAS and before response | verification is `passed`; pre-recovery phase is `publishing`; target equals candidate | `applied`; target remains candidate and cold recovery changes the durable phase and outcome to `applied` |

The verification-failure scenario is separate from interruption: it retains a
staged candidate, records verification `failed` and terminal phase
`verification-failed`, leaves the target at expected, and cold recovery returns
`verification-failed`. Every scenario retains its durable attempt. Exact
registered state/ref/attempt changes are required; mutation unrelated to the
named condition fails the verdict.

## Effectiveness, Efficiency, And Terminal Threshold

`pass` requires all of the following on both runtimes:

- every valid workflow reaches the exact caller-visible terminal result and
  every negative or interruption reaches its exact registered state, ref,
  attempt, and recovery postcondition with no unrelated mutation;
- both baselines establish correctness equivalence before their metrics enter
  comparison;
- selected logical durable state is structurally change-proportional and
  contains no full projected corpus, including through repeated revisions;
- no registered ranking-eligible correctness-equivalent baseline is no worse
  on every declared lower-is-better dimension and strictly better on at least
  one under the fixed timing rule;
- every raw observation, tradeoff, environment fact, and limitation is
  reported;
- the current 23-standard route, independent specification and standards
  audits, dual-runtime execution, repository gates, staged-scope, sensitive-
  value, and conventional Commit review pass.

This is vector dominance, not a composite score. A faster full-material control
cannot dominate while retaining more durable material. A facade with fewer
calls cannot dominate if it loses a caller goal; the correctness-incomplete
controls are excluded before comparison.

Return `revise` with typed `unavailable` when an applicable baseline,
representative environment, independent oracle, reliable required metric, or
deciding timing comparison is unavailable without disproving the design. A
changed question, workload, material model, oracle, metric, variability rule,
or threshold requires canonical re-registration before another run.

Return `reject` when the selected design violates A1c preservation, equivalent
behavior, a typed negative, IPC decoding, publication safety, one-authority
ownership, or caller-knowledge privacy; retains a full projected corpus per
revision or Analysis; fails a supported runtime for a design reason; or is
strictly dominated by a registered ranking-eligible correctness-equivalent
baseline.

## Architecture And Evidence Limits

The selected candidate retains one deep Authoring Module. Its material
resolver, publication/process Adapters, baseline switches, and measurement
instrumentation are private. The full-material control is not a second
authority and creates no production Seam. Deleting the Authoring Module would
redistribute revision, readiness, publication, and recovery knowledge into
callers; deleting the baselines, collectors, and prototype removes only
incidental evidence machinery.

For this prototype, one authoritative live prototype-evolved `SnapshotModule`
and its one canonical SQLite file own every snapshot-dependent revision/material,
Analysis, readiness, and attempt-transition aggregate. A private conditional
aggregate-publication/discovery seam may deepen the current store only to
exercise expected-head CAS and cold discovery through the existing canonical
aggregate tables. The prototype may not create a second SQLite file,
authoritative domain owner, foreign table, binding store, or domain-level SQL
path. Aggregate payload, children, and snapshot dependencies publish
atomically. Before cold find or recovery, the current domain owner fully
closes; a fresh owner then reopens the same file, with no overlap. The outer
collector may inspect the file only through a sequential read-only connection
after the domain owner closes and must close that connection before another
domain owner opens. It never shares a connection or writes. This is disposable
validation of the one-owner design; it selects no production schema, version,
or migration and grants no canonical store edit.

The two P3 unsafe-publication controls are reproduced as private negative-only
scenarios: unchecked update must overwrite an independently advanced target,
and publish-before-verify must expose a verification-invalid candidate. Their
exact failure behavior excludes them before ranking; their timings and bytes
never enter a candidate vector. They are unreachable private fault injections:
the first makes the decoded `update-target` handler omit its expected-old OID
only inside the negative harness, and the second invokes the ordinary decoded
CAS action before the private verifier only inside that harness. Neither fault
is accepted from the process envelope, Authoring Interface, or a ranked
candidate; both remain within Adapter process ownership and the seven-action
set.

P5 is limited to the admitted commit, current corpus, exact replacement
mutations, local Git and SQLite, single serial workflow, Linux, and the two
supported Python runtimes. It makes no Windows/macOS, concurrent throughput,
latency, capacity, memory, retained benchmark, schema, migration, public
version, or production verification claim. Publication occurs only in
disposable clones and never changes canonical `main`. The complete repository
checkpoint is an evidence gate after measurement, not the per-sample candidate
verification workload.

P5 may admit the combined design decision, not permanent benchmark or
instrumentation machinery. A later retained benchmark requires its own
regression claim, consumer, threshold authority, and lifecycle.

## Isolation And Execution Contract

- Exact base: `b503dcb76fd27aca41df154f37e20f6635de44bf`.
- Private branch: `prototype/a2-m0-efficiency-measurement`.
- Task-owned worktree:
  `/tmp/coding-standards-a2-p5-efficiency-measurement`.
- Sole authored source:
  `tools/standards_engine/tests/prototypes/a2/efficiency-measurement.prototype.py`.
- Branch-local generated artifact:
  `evaluation/standards-effectiveness/generated/suite-inputs.json`, changing
  only its repository-index digest after the source is staged.
- Required runtimes:
  `/tmp/coding-standards-a1c-py311/bin/python` and
  `/tmp/coding-standards-a1c-py312/bin/python`, both with `PYTHONPATH=.`,
  `PYTHONDONTWRITEBYTECODE=1`, and safe-path `-P`.
- Archive ref:
  `refs/archive/a2-prototypes/p5-efficiency-measurement`.
- Expected terminal disposition: `removed-archived`.

The prototype owner owns the private worktree and its two-file branch outcome.
Canonical `main` and the A2 integration owner own only the admission and later
evidence record. The prototype has no production or package consumer and never
merges. Existing files, package inputs, registries, suite definitions, graph,
inventory, and retirement evidence must remain unchanged. Any question,
workload, base, oracle, metric, variability, threshold, write-set, or generated-
diff change before creation is a stop-and-re-admit result.
