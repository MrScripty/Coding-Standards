# Proposal 1: Retained evidence identity and complete inventories

Status: wording drafted; MCP submission rejected before a proposal was created.
The returned code was `ANALYSIS.EVIDENCE_DIGEST_MISMATCH`: “Resolved evidence
bytes do not match the declared digest.” Both the original owner placement and
an alternate placement wholly within Verification received this rejection. No
proposal or revision handle was returned. The exact cause remains unconfirmed.

The purpose evidence file's declared digest matches its current bytes, and the
same evidence reference was accepted for proposals 2 and 3. This does not prove
that the Engine's other retained evidence bindings are valid. Repairing or
retiring existing certificates is outside this drafting request.

## Purpose and effect

Clarify two recurring applications of Verification's existing evidence rules.
A saved success result must identify the source and material producing context
it actually observed before it qualifies a current claim. A completeness check
must establish the expected population and compare its required members.

Examples from the audit include stamping the current executable hash onto an
older replay result, accepting the right total count with the wrong members,
and allowing an empty loop or truncated pairwise comparison to report success.
Protected repository-state checks must observe the particular state they claim
to protect, including their own output writes when relevant.

These conditions follow the selected claim. They do not require a universal
receipt system, hash inventory, fixed fixture count, permanent scanner or
project sandbox. Existing construction proofs and proportionate reruns remain
valid.

Evidence: CR-0099, CR-0118, CR-0124, CR-0103, CR-0127 and CR-0136;
see [the source record and limits](evidence.md).

## Proposed edits and placement

The intended original placement is retained below:

- Add `Retained Evidence Identity` under `Coverage And Durable Evidence Records`
  in `workflow.verification`.
- Add `Complete Inventory Evidence` as a section of
  `workflow.verification.oracles`, before `Negative Fixture Isolation`.
- Register `workflow.verification.retained-evidence-identity` and
  `workflow.verification.inventory-completeness` as separate policy scopes at
  semantic revision 1, with supporting provenance.
- Preserve the existing registered scopes and their semantic revisions.

The rejected requests are preserved in
[the original request](01-evidence-request.json) and
[the alternate request](01-evidence-revised-request.json). They are draft
requests, not applied edits.

## Exact proposed wording

The following text is from the submitted draft request. There is no saved MCP
candidate available to read back for this proposal.

### Retained Evidence Identity

When a retained result is used to satisfy a current acceptance claim, establish
which material source, inputs, producer, configuration, and environment produced
that result. Select those facts from what can change the claimed property;
unrelated environment details do not become required evidence.

Bind the result to those facts when it is produced, or establish the connection
from authoritative retained records. Compare that producing context with the
current claim before reusing the result. Hashes computed from the current
checkout, executable, renderer, or input do not establish what produced an
earlier result. Reconcile reported measurements and aggregates with their
authoritative observations when the claim depends on them.

Keep historical qualification scoped to its original source and procedure.
Rerun the affected evidence when material producing facts changed or cannot be
established. Missing required identity or observations leaves the current claim
`unavailable`; contradictory identity or an unsupported inference is `invalid`.

Use existing records, an adequate construction guarantee, or a proportionate
rerun when they establish the connection. This rule does not require a new
receipt system, universal hash inventory, byte identity, signing, or a fixed
record format. Apply the existing evidence-machinery admission criteria before
introducing a permanent mechanism.

## Complete Inventory Evidence

When a validator claims that a population is complete, that protected state is
unchanged, or that every corresponding value was compared, establish the
expected members, cardinality, identity rules, and observation boundary from
the claim's independent or authoritative contract. Deriving the expected
population from only the observed output cannot establish completeness.

Compare every required member and relation. Reject missing or unexpected
members, forbidden duplicates, mismatched cardinality, and empty populations
when the contract requires members. Counts, empty iterations, and comparisons
that truncate to the shorter input cannot establish exact membership or a
complete pairwise comparison. An empty population is valid when the owning
contract permits it.

For a protected filesystem or repository-state claim, observe every relevant
state selected by that claim. Tracked worktree content, staged content, untracked
content, and ignored content are distinct possible inputs; a tracked diff does
not prove that all are unchanged. Include only the paths and state the claim
actually protects, rather than expanding to a repository-wide inventory by
default.

Account for relevant effects of the observation and result-publication procedure.
A result claiming protected state remains unchanged must still be true after
that procedure's own writes. Select a safe output location or establish the
postcondition according to the owned mutation contract.

Use an adequate construction guarantee or the smallest complete observation
that establishes the property. Missing expected-population or observation facts
is `unavailable`; incomplete comparison or contradictory membership is
`invalid`. This rule selects no fixed fixture count, inventory format, permanent
scanner, or requirement to sandbox a project.

## Review considerations

Review the existing Verification consumers against these new scopes and
establish their actual operational impact. Exercise representative stale-result,
missing-member, permitted-empty, and protected-state cases if this proposal
proceeds. The historical findings were not reproduced in this drafting work.
