# Standards Authoring Workflow

**Standards metadata**

- ID: `workflow.standards-authoring`
- Role: `workflow`
- Level: `MUST`
- Applies when: Maintainers author, review, or publish this standards library through its managed authoring interface.
- Does not apply when: A project is applying operational standards without maintaining the library.
- Requires: `core`, `workflow.implementation`, `workflow.verification`
- Specializes: `none`
- Verification: Independent material review, declared consumer dispositions, candidate validation and purpose-qualified accepted readback.
- Canonical owner: `workflows/standards-authoring.md`

This workflow owns standards-maintenance procedure. Use the purpose-qualified
authoring interface and its current contract for managed mutations.

## Graph Maintenance

Before changing an audited policy owner, query its declared `policy-impact`
relationships by logical ID or registered repository alias and review every
returned material consumer. Audit an uncovered owner and explicitly register
its required policy scopes and actual semantic relationships before publication.

Give each edge one registered source declaration. The graph derives both
directions from that declaration while domain validation remains specific to
each relationship group and traversal follows explicit permission. Group
membership preserves one declaration and its meaning; the graph engine owns
indexing and traversal, while domain owners retain policy semantics.

Use the canonical graph declarations for current relationships and the review
record for change-specific dispositions. Establish missing semantic relationships
by review; hyperlinks, lexical similarity, prerequisites, suite ownership, and
other graph associations alone do not establish a semantic consumer.

## Operational Guidance And Supporting Material

Write operational requirements around general technical conditions, correct
actions, preserved properties, meaningful exceptions, authority, failure/lifecycle
semantics, and acceptance. Preserve MUST and SHOULD force and stable policy
identities. Treat a changed obligation, applicability decision, or authorization
boundary as a substantive policy revision.

Keep optional correct examples and explanations in scoped nonnormative references.
Prompts and templates convey procedure and link to canonical owners. Keep historical
failures, rejected approaches, trade-offs, source history, assumptions, and
reconsideration conditions in revision-bound decision provenance.

Label observed evidence, external requirements, engineering inference, and owner
preferences accurately. Record unknown historical origins explicitly. A current
justification supports current retention without inventing original motives.
Update provenance when its supporting evidence, reasoning, or assumptions change;
a rationale-only correction preserves unchanged operational semantics.

## Review And Publication

Inventory the whole application-visible module and the affected declared
consumer closure. Distinguish incomplete discovery from demonstrated completeness.
Review required dependencies, specialization, supplementary help, and provenance
according to their actual relationship meanings.

Prepare one coherent change through the Engine, including material consumers,
semantic decisions, provenance, and explicit exposure dispositions. Obtain
independent material review of generality, operational sufficiency, evidence
accuracy, and consumer coherence. Inspect the exact application view through the
supported validation path before publication.

Publish only the reviewed candidate through the authorized review/apply workflow.
Follow returned recovery operations for uncertain publication. Verify accepted
readback through authoring and application views, including complete qualification
of the required reading path. Keep unreviewed scope outside readiness claims.

Use actual downstream tasks for effectiveness evidence. Structural validity and
prose review establish their own properties; record the limits of any observed
behavioral improvement separately.
