# A2 Product-Contract Discovery

**Status:** `accepted for the initial controlled-authoring scope`

## Caller And Deployment

A2 preserves the accepted A1c product direction: software-development agents
acting for developers are the first caller, the Python Interface is the access
seam, and a harness-managed tool call is the primary deployment. One agent
workflow may span turns, process invocations, and authorized coordinator or
subagent handoffs. Handles identify durable state but grant no authority.

The authoring workflow serves the Coding Standards corpus itself. Project
repositories to which agents apply standards remain caller context and are not
publication targets or standards authority.

## Representative Workflow Trace

| Workflow | Accepted A1c behavior used unchanged | A2 behavior that must be validated | Required terminal distinctions |
| --- | --- | --- | --- |
| Create | `create_snapshot` captures current configured `HEAD` and returns an opaque root | Create a proposal root and immutable first revision linked to that handle without caller Git or store identity | created; invalid mutations; unauthorized; snapshot unavailable/quarantined/expired |
| Discover | `find_snapshots` rediscovers roots after process or agent loss | Discover durable proposal roots and current heads without a caller-owned catalog | found page; continuation; no matches; unauthorized |
| Revise | Snapshot and analysis state stay immutable | Store exact non-Git mutations as a new immutable revision and advance one head only by expected-revision compare-and-swap | revised; stale head; invalid change; unavailable root; unauthorized |
| Query/read | A1c `query` compiles and navigates one immutable snapshot | Project the proposal revision through the same compiler and semantic owners without treating it as accepted snapshot authority | route/read/related results; invalid projection; unresolved facts; unavailable authority |
| Analyze | A1c `prepare`, `resolve`, one immutable `AnalysisState`, and one `AnalysisHandle` own analysis | Bind analysis to the exact proposal revision and reuse current semantics without caller-duplicated facts or a second analyzer | pending; complete; rejected; prior-analysis reuse; material invalidation |
| Approve | `resolve` records authorized analysis submissions; completion is derived, not authored | Record separately authorized semantic, relationship, lifecycle, mutation, and apply decisions and derive readiness for the exact revision | ready; incomplete; unauthorized; revoked; stale revision; stale analysis |
| Apply | A1c has no canonical mutation operation | Materialize an isolated candidate, verify its exact bytes, publish through an expected-target transition, establish the postcondition, and retain immutable application intent, selection, and outcome | applied; stale target; verification failed; unauthorized; unavailable; recovery required |
| Snapshot delete/undelete | Quarantine and undelete operate on the complete aggregate with one fixed deadline | Proposal, revision, readiness, application intent, selection, and outcome records follow the base root lifecycle without independent destructive operations | quarantined; restored; expired; purged; no partial child state |
| Interruption/recovery | Stored A1c handles reconstruct after cold process restart | Resolve the readiness-selected immutable application and either return its durable outcome or reconcile the current exact target observation without resuming publication | applied/confirmed; expected target; diverged target; observation unavailable; outcome persistence unavailable |
| Agent handoff | Opaque handles cross authorized handoffs and process boundaries | A second authorized agent continues from proposal or readiness handles under current authority | resolved; unauthorized; revoked; unsupported contract |

## Caller Knowledge Budget

An authoring caller may supply desired non-Git mutations, semantic proposal
material, declared review decisions with evidence, and opaque handles returned
by the Engine. The caller must not supply:

- repository or worktree paths, refs, commits, trees, Git object IDs, raw
  patches as internal state, or raw canonical bytes;
- SQLite paths, schema versions, internal content hashes, child catalogs, or
  proposal-head storage fields;
- analysis facts, dependency identities, or verification results already owned
  by the proposal, A1c analysis, trusted providers, or execution context; or
- self-asserted capabilities or an authored “analysis complete” or “applied”
  Boolean.

## Application Success Decision

On 2026-09-01 the user directed A2 to proceed with the recommended direct
canonical-publication outcome. The configured Coding Standards repository and
its `refs/heads/main` ref are the one target authority. The Authoring Module,
not the caller, resolves that repository, target ref, expected old object, and
candidate object from trusted execution context and durable state.

`applied` means all of the following are established:

1. the candidate bytes passed every required verification;
2. the configured canonical ref changed from the internally captured expected
   object to the verified candidate through an atomic expected-target update;
3. a post-publication observation resolves that ref to the exact candidate; and
4. the durable immutable application outcome records the established identity.

A candidate commit, export, or external submission is not `applied`. An
unavailable or contradictory observation never guesses success and remains a
typed recovery outcome. The current interface v19, Repository Git Adapter,
Snapshot store v2, and Authoring implementation realize this selected meaning.

The deciding caller-visible outcome comparison was:

| Candidate outcome | Exact postcondition | Valid result name | Product consequence |
| --- | --- | --- | --- |
| Direct canonical publication | The selected canonical ref changed from the expected target to the verified candidate and resolves to the candidate identity | `applied` | Satisfies the plan objective directly but requires trusted write authority, exact target ownership, atomic compare-and-swap, and cold recovery. |
| Candidate commit only | A verified commit exists but no canonical ref changed | `candidate-created` | Useful staging evidence, never application success. |
| Patch export | A verified external artifact was produced | `exported` | External integration remains unobserved; A2 cannot report `applied`. |
| Pull-request submission | A request was accepted by an external service | `submitted` | Merge and canonical publication remain external and must be confirmed independently. |

Direct canonical-ref publication is selected because it is the only candidate
that satisfies the accepted A2 objective without an external observer. A
successful candidate commit, export, or submission cannot be relabeled
`applied`.

## Final Product Choices

A2 constitutes feature completeness for the initial Coding Standards
controlled-authoring scope. The fresh bounded repository inventory finds only
coordinated current-tree contract and test consumers and no retained store, so
v19/store-v2 is the one supported current format. No cross-engine reader,
overlap window, or migration framework is justified. Discovery of an
independently deployed consumer or retained external store is a re-plan trigger,
not a reason to build compatibility machinery speculatively.

No current caller requires proposal abandonment independently of its base
snapshot. Proposal state therefore retains the accepted aggregate lifecycle:
snapshot quarantine, undelete, expiry, and purge govern the complete dependent
closure. A future distinct abandonment need requires separate product and
lifecycle evidence.
