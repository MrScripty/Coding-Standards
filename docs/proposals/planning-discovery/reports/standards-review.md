# Independent Standards Review

Reviewed candidate `proposal-revision:sha256:9421465aaed112d9538bc6fd3f3bdb7a52bfe37e84f1f9ab05ff56f11b385990` against accepted snapshot `snapshot:v1:7b333e49-f100-427d-89b9-2388a4e560ee` (commit `daa70d98328a88b125dd9df3f896a0502e8233b7`). Engine readback confirms the five changed content artifacts are byte-identical to the prior `6f4c4cbc…` material diff; the intervening revision adds only coverage-publication requests.

## Finding: missing semantic consumers in the policy graph

Severity: medium; resolve before certifying consumer completeness.

`workflows/planning/discovery.md`, **Explain Back And Enter Planning**, explicitly applies Planning's written-plan criteria, transfers agreed decisions into canonical plan fields, and preserves explicit plan admission. The new detail therefore consumes `workflow.planning.written-plan-applicability`, `workflow.planning.active-plan-fields`, and `workflow.planning.plan-admission`. Candidate `policy-impact` declarations for these owners omit `workflow.planning.discovery`; the new detail's `Requires: workflow.planning` edge only establishes prerequisite reading.

This violates **Standards Authoring / Graph Maintenance**: “Audit an uncovered owner and explicitly register its required policy scopes and actual semantic relationships before publication.” That section also states that prerequisites alone do not establish semantic consumers. Without these declarations, a future revision of written-plan applicability or admission can omit discovery from its material consumer review.

Add scoped normative-consumer relationships from these Planning policy owners to the discovery handoff, then reanalyze and review the resulting coverage obligations. Review other canonical rules consumed by the new detail under the same criterion; a link alone is insufficient evidence for an edge.

No additional substantive wording, applicability, lifecycle, or authority conflict found. Discovery retains proportional handling and capability fallbacks; lifecycle states and implementation admission remain owned by Planning; development boundaries preserve Commit's topology and cleanup authority.

Sources: Engine reads of Core, Standards Authoring, Planning, Commit, and Development Proportionality; exact Engine candidate readbacks and `policy-impact` relationship queries; proposal edit manifests. Scope excludes unrelated staged work. This material review does not certify the whole consumer inventory, complete candidate verification, application qualification, publication, or downstream conversational effectiveness. Fowler code-smell heuristics produced no applicable finding in these prose changes.
