# Full-Codebase Standards Review Prompt

Create an implementation-ready standards refactor plan. This is planning and
analysis only; do not edit source, tests, config, generated artifacts, or
lockfiles.

Route the adopting repository through
[`STANDARDS-ROUTER.md`](../STANDARDS-ROUTER.md), then follow the canonical
[`Planning Workflow`](../workflows/planning.md). Preserve the requested
objective and identify the evidence that will accept it.

Record whether composed-design review applies. When it does, review the
produced artifact after its Modules are composed: caller and composition-root
knowledge, Interface Depth, representative change Locality, stable values and
Interfaces versus hidden knowledge, independent evolution, necessary
complexity, cumulative machinery, and deletion results. Do not infer simplicity
from files, Modules, tests, generated artifacts, ownership labels, or successful
correctness checks. Treat a hypothetical Adapter only as a Seam-shape probe and
require a current independent reason for permanent generality.
