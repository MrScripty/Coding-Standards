# A2 Milestone 0 Prototype Evidence Index

**Status:** `exact executions admitted; runs pending`

The canonical [design-validation protocol](design-validation-protocol.md)
predeclares every question, comparison, dimension, oracle, and threshold.
Prototype source is never merged to `main`. This index will record exact
branch commits and terminal worktree dispositions after each isolated run.

| ID | Exact path | Branch and worktree | Exact admitted base | Prototype commit | Verdict | Worktree disposition |
| --- | --- | --- | --- | --- | --- | --- |
| A2-P1 | `tools/standards_engine/prototypes/a2/authoring-state-model.prototype.html` | `prototype/a2-m0-state-model`; `/tmp/coding-standards-a2-p1-state-model` | `bbdfb485e914540e0e53092dab71c9b80f55102d` | pending | pending | pending; expected `removed-archived` |
| A2-P2 | `tools/standards_engine/prototypes/a2/projected-view.prototype.py` | `prototype/a2-m0-projected-view`; `/tmp/coding-standards-a2-p2-projected-view` | `bbdfb485e914540e0e53092dab71c9b80f55102d` | pending | pending | pending; expected `removed-archived` |
| A2-P3 | `tools/standards_engine/prototypes/a2/publication-recovery.prototype.py` | `prototype/a2-m0-publication-recovery`; `/tmp/coding-standards-a2-p3-publication-recovery` | `bbdfb485e914540e0e53092dab71c9b80f55102d` | pending | pending | pending; expected `removed-archived` |
| A2-P4 | `tools/standards_engine/prototypes/a2/facade-workflow.prototype.py` | `prototype/a2-m0-facade-workflow`; `/tmp/coding-standards-a2-p4-facade-workflow` | `bbdfb485e914540e0e53092dab71c9b80f55102d` | pending | pending | pending; expected `removed-archived` |
| A2-P5 | `tools/standards_engine/prototypes/a2/efficiency-measurement.prototype.py` | `prototype/a2-m0-efficiency`; `/tmp/coding-standards-a2-p5-efficiency` | `bbdfb485e914540e0e53092dab71c9b80f55102d` | pending | pending | pending; expected `removed-archived` |

The A2 prototype owner owns each private worktree, its one authored source
path, and the branch-local generated suite-input projection required by that
new tracked path. Canonical `main` is the integration target and the A2
integration owner is its sole integrator. Prototype branches have no production
consumer and never merge. Each run uses scratch state only, then receives a
named recovery ref before its worktree is removed. A material result that
changes a registered question, oracle, state model, or threshold requires a new
canonical admission.
