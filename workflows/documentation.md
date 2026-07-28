# Documentation Workflow

**Standards metadata**

- ID: `workflow.documentation`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change creates or alters a durable responsibility, decision, contract, or operational boundary.
- Does not apply when: A change preserves documented responsibilities, decisions, contracts, and operational procedures.
- Requires: `core`
- Specializes: `none`
- Verification: Documentation decision, policy consolidation, and traceability checks.
- Canonical owner: `workflows/documentation.md`

## Select Documentation From Impact

Durable documentation is required when a reader must understand information
that source code and tests do not own clearly enough:

- why a meaningful module or operational boundary exists;
- which responsibility and invariants that boundary owns;
- what consumers rely on across a public, process, language, persistence, or
  generated-artifact boundary;
- why a consequential decision was selected; or
- how an operator must perform or recover a non-obvious procedure.

Directory count, file count, and the presence of a `src/` path are not
documentation requirements. A local implementation change that preserves all
documented decisions and contracts requires tests and code review, not an
unrelated README or ADR edit.

## Documentation Profiles

Select the smallest profile that preserves the affected knowledge:

| Profile | Select when | Required content |
| --- | --- | --- |
| `none` | The change preserves durable responsibilities, invariants, decisions, contracts, and procedures. | No documentation artifact. |
| `boundary-readme` | A meaningful module or operational boundary is created or its responsibility/invariants change. | Purpose, owned responsibility, invariants, entry points, and applicable links to accepted decisions or contracts. |
| `contract-readme` | Consumers need stable behavior at a public, process, language, persistence, or generated-artifact boundary. | Boundary README plus inputs/outputs, lifecycle, failures, compatibility or migration, and producer/consumer ownership. |
| `adr` | A durable decision crosses boundaries, has material alternatives, or must outlive the implementation plan. | Context, decision, alternatives, consequences, status, affected boundaries, and supersession links. |
| `runbook` | Operators need a repeatable deployment, recovery, migration, or incident procedure. | Preconditions, steps, validation, failure handling, rollback or repair, and owner. |

More than one profile may apply. When an ADR or contract document owns the
rationale, a README links to that owner and summarizes only the local
responsibility. Do not copy the full decision into every artifact.

If the impact cannot be classified, record an unresolved documentation
diagnostic. Do not create a speculative README or ADR as a fallback.

## Artifact Placement

Follow the adopting repository's documented placement and naming convention.
When no convention exists:

- keep boundary-owned documentation with the boundary;
- place project-level decisions, plans, and reports under a root `docs/`
  directory with concern-specific subdirectories; and
- group multi-file work under one descriptive, lowercase, hyphenated slug.

The artifact's owner and links must remain unambiguous. Do not scatter one work
item across unrelated roots, reorganize unaffected documentation to satisfy
this default, or retain an obsolete layout as a compatibility fallback. A
layout replacement updates affected links and automation in the same accepted
change.

## Boundary README

A boundary README is concise and specific. It contains:

- `Purpose`: why the boundary exists;
- `Responsibility`: behavior and state owned here, plus explicit exclusions;
- `Invariants`: conditions that must remain true;
- `Entry Points`: the interfaces or commands a reader should start from.

Add `Consumer Contract` or `Produced Contract` only when that contract exists.
Add `Decision Links` only when accepted rationale or a canonical contract
exists. Add operational instructions only when the boundary owns them. Omit
non-applicable sections instead of filling them with `None`, generic prose, or
invented alternatives.

## Repository Entry Point

When a repository is independently adopted, operated, or contributed to, its
root README is the discovery boundary. It states:

- the repository's purpose and intended audience;
- stable commands or interfaces needed to start;
- the minimum verified setup and use path for that audience; and
- links to owned contribution, operation, contract, decision, and license
  documents when those concerns apply.

Select sections from actual audience needs. Do not require a fixed heading
list, duplicate detailed owner documents, or maintain a file-by-file project
tree. Update the entry point when these facts change; unrelated implementation
changes require no root README churn.

## Contract Documentation

Contract documentation states the facts a consumer needs:

- input and output semantics;
- validation and typed failure outcomes;
- lifecycle, ordering, cancellation, idempotency, and retry behavior;
- compatibility, versioning, migration, or coordinated replacement policy;
- producer and consumer ownership; and
- verification evidence or executable contract location.

Follow [Contract Evolution](../topics/contracts.md). Unknown contract facts
remain diagnostics; documentation must not invent defaults or compatibility.

## Decision Traceability

Update durable documentation only when its owned knowledge changes:

- update the affected boundary README when responsibility or invariants change;
- update the canonical contract when consumer-visible semantics change;
- add or supersede an ADR when a durable cross-boundary decision changes; and
- update a runbook when its procedure or recovery semantics change.

Every ADR identifies affected boundary paths or stable contract identifiers.
An unrelated ADR cannot satisfy traceability for a changed boundary.

Plans and pull requests link to accepted rationale. They may summarize the
current change, but they do not become duplicate long-term owners.

## Quality Rules

- Write project-specific information that cannot be inferred from names alone.
- Keep contents lists limited to stable entry points, not every file.
- Keep examples aligned with real public entry points.
- Remove or supersede stale decisions; do not append competing authority.
- Treat generated documentation as derived output and update its source in the
  same change.
- Verify links and any executable examples affected by the change.
