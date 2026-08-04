# Plan Implementation Prompt

Implement one explicitly admitted plan transition. Supply the canonical
repository-relative `plan.md` path and explicit `start`, `continue`, or `verify`
operation.

Route the adopting repository through
[`STANDARDS-ROUTER.md`](../STANDARDS-ROUTER.md), then follow the canonical
[`Implementation Workflow`](../workflows/implementation.md), which consumes the
[`Planning Workflow`](../workflows/planning.md) admission decision. Preserve the
requested objective and return the owning typed diagnostic when admission or
canonical planning cannot authorize work.
