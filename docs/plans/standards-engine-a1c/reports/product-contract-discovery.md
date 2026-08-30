# A1c Product-Contract Discovery

**Status:** `Open`

## Purpose

Record the product facts that must exist before A1c selects architecture,
persistence, compatibility, platform, or verification machinery. This report
does not choose an A1c design and does not authorize implementation.

## Current Evidence

The accepted [A1/A1b audit synthesis](../../standards-engine-a1-a1b-audit/reports/final-synthesis.md)
found no independent external Standards Engine consumer, retained A1 state,
non-test persisted-state caller, or operational backup/restore caller at its
fixed observations. A1b nevertheless supplies strong durable child-object
replay and operational recovery because its accepted plan selected those
guarantees.

Those observations motivate discovery; they are not current product decisions.

## Required Product Facts

### First Caller

- Caller identity and owner:
- Human or software workflow served:
- Public operation sequence:
- Inputs controlled by the caller:
- Outputs or handles retained by the caller:
- Failure and uncertainty outcomes the caller must distinguish:

### Deployment

- Deployment form: in-process tool, CLI, service, appliance, library, or other:
- Process boundary:
- Repository and worktree boundary:
- Machine and user-account boundary:
- Upgrade and rollback boundary:
- Independently deployed components:

### Handle Lifetime

For each handle family the caller actually uses, record whether it must survive:

| Boundary | Required | Caller workflow and consequence |
| --- | --- | --- |
| Repeated call in one process | unresolved | Pending |
| Process restart | unresolved | Pending |
| Repository content change | unresolved | Pending |
| Application upgrade | unresolved | Pending |
| Machine transfer | unresolved | Pending |
| Authorization/provider change | unresolved | Pending |

### State And Loss

| State or decision | Derivable from canonical inputs | Required retention | Consequence of loss | Operational owner |
| --- | --- | --- | --- | --- |
| Pending inventory | unresolved | unresolved | unresolved | unresolved |

### Compatibility

- Independently evolving producers and consumers:
- Required overlap window:
- Persisted or exchanged representations:
- Unsupported old-state behavior:
- Migration, replacement, or no-compatibility rationale:

### Platform

- Supported operating systems:
- Supported filesystems:
- Supported architectures:
- Supported Python runtimes:
- Required-real capabilities:

## Evidence Inputs For Plan-Owned Decisions

The plan owns A1c constraints and hypotheses. This report records the evidence
available to those decisions and must not become a second authority for their
disposition.

| Area | Current evidence | Missing evidence |
| --- | --- | --- |
| Public behavior | The accepted audit binds four read-only operations with typed request/result/rejection behavior and explicit uncertainty without valid-looking fallback. | Caller workflows must identify the minimum values, handles, and lifetime needed to deliver those behaviors. |
| Schema semantics | A1 repairs demonstrated that local Draft interpretation can agree internally while violating the selected external contract. | None for the requirement to use the selected maintained validator; later experiments must determine Adapter depth and internal representation. |
| Equality and identity | A1 repairs demonstrated that schema equality, domain equality, identity encoding, ordering, and deduplication have different semantics and owners. | Candidate locality probes must show where those owners compose without duplicating authority. |
| Immutable results | The accepted audit requires no ambient substitution within the handle lifetime A1c promises. | The caller and deployment facts must establish that promised lifetime and whether immutable branching is externally observable. |
| Child lookup and durable publication | A1b supplies direct cold lookup for child objects, SQLite publication, backup, restore, and interruption behavior. | No current non-test caller, retention period, loss consequence, or recovery owner has yet been established. |
| Historical coverage replay | A1b can bind broad coverage authority and replay historical evidence. | Product discovery must distinguish externally promised replay from repository-governance evidence. |
| Version scopes | A1b has independently scoped semantic and representation versions. | Actual independently evolving consumers and overlap windows remain unverified. |
| Governed-source interpretation | A1b enforces cross-package source constraints with repository-owned analysis. | A current threat, consumer failure, or contract requiring that mechanism remains unverified. |

## Discovery Completion

This report is complete only when every unresolved product fact is replaced by
evidence or an explicit unsupported/deferred decision, A1C-001 and A1C-002 are
resolved, and the plan can be re-planned with bounded design experiments. Empty
consumer or state results require a documented search boundary; they are not
proof merely because no current caller was found.
