# Evidence reduction

The user authorized deleting obsolete certificates and evidence machinery that
does not help agents find coding guidance or interact correctly with the Engine.
The accepted purpose is useful navigation, reading, graph inspection, authoring,
and verification. A passing model of a policy is not proof that code or an agent
follows that policy.

## Selected changes

Remove the 51 stale repository claims rather than renewing them. Preserve any
actually current claim when maintenance is used elsewhere. Empty coverage means
review is required; it does not mean every consumer is covered.

Retire synthetic policy-decision checks, historical migration/disposition gates,
arbitrary line-budget comparisons, and file-presence checks that do not execute
the claimed behavior. Keep current routing, Markdown destination and metadata
validation, generated contract checks, package boundary checks, and executable
Engine tests for material failures. Retire empty suites and their obsolete graph
nodes. Keep actual normative consumer relationships, with evidence ownership
limited to actual suite checks or an explicit review of the consumer. Functional tests remain
separate evidence and must actually be run when their behavior is claimed.

Register receipt implementation and functional-test consumers explicitly under
the policies governing their actual behavior. Do not make every policy depend
on every file. Remove the abstract oracle decision model rather than expand a
second policy language just to describe permissible evidence. Actual tests of
routing, publication, evidence-byte mismatch, replay, and failed edits supply
useful oracles for Engine functionality.

The contract compiler must consume the canonical Interface operation catalog.
A second hard-coded operation list and a test that compares another copied list
do not supply an independent conformance oracle. Keep real reference/shape
validation, capability binding, and consumer behavior checks.

## Engine maintenance boundary

`maintain_evidence` accepts explicit retirements, descriptions, consumer
registrations, relationship updates, an expected repository revision, and real
review evidence. It previews the exact resulting repository and runs the complete
checkpoint before an applied request writes affected working-tree files. It
rejects changed target bytes or a stale revision. It does not change normative
standard text, create completeness claims, or publish Git refs. Commit the
verified working-tree result with its implementation and review evidence.

This is evidence catalog administration, not a substitute for semantic proposal
review. The Engine owns the evidence-file mutations and derived input refresh.
No separate certificate-renewal queue or replacement policy-simulation harness is
introduced. Existing immutable snapshots retain their captured history.

The [maintenance inventory](evidence-retirement-inventory-2026-09-04.json)
records the selected check and suite retirements. It is historical review data,
not an executable acceptance gate.

The maintenance operation passed 38 focused tests (compiler/projection, generated
Interface/rendering, and evidence maintenance), including a real preview and
application in an isolated repository, preservation of independent edits, and
retention of current claims. The initial repository checkpoint passed 271 suites
and 858 checks. Catalog reduction and the final functional verification follow
that implementation boundary.

## Applied catalog reduction

Engine maintenance removed 51 stale claims in 11 files, 737 checks, 198 empty
suites, and 218 unused fixture inputs. The resulting checkpoint passes 73 suites
and 121 checks. No replacement certificate was issued. The retained checks have
narrow descriptions and the active verification guides no longer claim that
policy simulations demonstrate consumer behavior.

Consumer-local review ownership (`review:consumer`) preserves policy,
relationship, and direct consumer fingerprints without importing an unrelated
suite closure. A focused mutation test confirms that consumer changes invalidate
the requirement while unrelated input changes do not. The historical suite-only
contract remains readable. The second Engine maintenance pass retired 15 registered checker implementations
and their graph edges, and changed 319 relationships to consumer review ownership.
Together with the earlier unregistered baseline checker removal, 16 obsolete
checker modules were deleted. The retired table checker was removed from its
shared module; navigation still uses the shared TSV projection functions.

## Final validation and limits

Both maintenance previews and applications passed the complete checkpoint.
The resulting catalog contains 73 suites and 121 checks, down from 271 suites
and 858 checks. All 51 stale claims were removed; all 51 registered policy
subjects remain review-required. No claim was silently renewed or inferred from
passing structural checks. The abstract evidence-oracle decision suite and its
fixture machinery are gone.

A production-compiler mutation diagnostic changed the receipt implementation's
bytes in memory. Five relevant requirements changed; the unrelated commit-message
policy requirement stayed identical. The receipt implementation and its actual
functional test are registered inputs. This proves sensitivity within the
declared graph, not discovery of every possible consumer.

Focused functional and regression validation passed:

| Area | Tests | Observed behavior |
| --- | ---: | --- |
| Verifier | 156 | Retained checks, navigation destinations, input identity, graph composition, diagnostics |
| Analysis | 99 | Impact, review requirements, evidence/authorization binding, decision reuse |
| Snapshots | 23 | Durable store, immutable replay, interruption and recovery |
| Policy-impact compiler | 10 | Consumer-review ownership, legacy suite-only reads, invalid declarations |
| Logical authoring | 21 | Create, revise, move, retire, relationships, and atomic routing edits |
| Engine navigation | 7 | Routes, unknown facts, reading, related policies, immutable proposal reads |
| Evidence maintenance | 6 | Retirement, current-claim retention, real preview/apply, independent-edit protection |
| Verification Interface | 2 | Explicit refresh authority and typed missing-input rejection |
| Relationship Analysis and create/retire publication | 2 | Exact revision replay and Engine-owned topology publication |
| Audit publication | 1 | Review, verify, apply, recovery, and receipt readback without the original database |

Navigation initially exposed an outdated fixture that omitted `routing.details`;
that fixture now supplies the fact. Authoring fixtures now use consumer review
instead of a deleted suite. The maintenance integration fixture supplies its own
obsolete artifact rather than depending on stale certificates in the real repo.
The affected tests were rerun successfully. A heading-phrase assertion was also
removed from navigation; the content and snapshot relationship checks remain.

The cleanup exposed a real missing-input error escaping repository refresh.
The Engine now returns the Verifier's typed rejection, including the input path,
instead of a transport traceback. This behavior has a focused regression test.

Changed Python files pass Ruff with the existing standalone-test import-order
exception (`E402`); Git whitespace checks pass. These runs are a focused validation
set, not a claim that every repository test or downstream consumer was executed.
Historical snapshots and legacy receipt readers remain for Engine replay; the
current runner does not execute retired check kinds. Git history retains the
removed certificates, suites, fixtures, and checker implementations.
