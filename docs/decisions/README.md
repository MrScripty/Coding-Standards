# Architecture Decisions

Start with [A1c](standards-engine-a1c.md) for the Snapshot and Analysis
architecture and [A2](standards-engine-a2.md) for controlled logical authoring.
The [Engine README](../../tools/standards_engine/README.md) describes the
current public operations.

| Decision | Scope and current standing |
| --- | --- |
| [Navigation and Analysis (A1)](standards-engine-navigation-analysis.md) | Original read-only Engine design. Policy-impact authority was replaced by V2; contract and runtime architecture was subsequently revised through A1b and A1c. |
| [Policy-Impact Authority V2](standards-engine-policy-impact-authority-v2.md) | Compiled policy-impact ownership and relationship semantics. Its historical A1 context does not override later architecture decisions. |
| [Contract and Authority Foundations (A1b)](standards-engine-a1b.md) | Historical design and acceptance. A1c supersedes its runtime architecture. |
| [Snapshot and Analysis Architecture (A1c)](standards-engine-a1c.md) | Accepted runtime architecture, including the explicitly documented A2 projected-material supersession. |
| [Controlled Logical Authoring (A2)](standards-engine-a2.md) | Accepted authoring extension and logical changeset boundary. |

Acceptance records what was decided at a particular boundary. Supersession
notices identify the affected scope; the older decision retains its rationale
and evidence. Implementation plans and audit reports are indexed under
[repository work](../plans/README.md).

[Library information architecture](standards-library-information-architecture.md)
records the accepted restructuring direction; its path catalog describes the
migration design rather than an inventory of currently implemented profiles.
