# Ledger

## Admission

Pinned the newly pushed `34c2dcba` using its exact GitHub source bundle. Working tree
was clean; work is on a private local feature branch. Read Core, routed actual task
facts and relevant contract/implementation guidance. The current environment provides
Python 3.13.5 and rpds-py 2026.5.1, not the locked supported 3.11/3.12 environment.
No supported-runtime or live model-client acceptance is inferred from local checks.

The compatibility mode retains the existing supported-client workaround; native
presentation is an explicit new selection rather than an unqualified default change.

## Implementation and review

- Added host-selected compatibility/native catalog presentation. Native chooses the
  smaller equivalent projection per input; application schemas gain no artificial
  reference overhead. Kept structuredContent and matching JSON text unchanged.
- Added focused route-content paging over the existing read owner, with qualified
  closure, one snapshot/input, whole-item byte bounds and explicit continuations.
- Added generated agent input variants and request-local typed evidence expansion;
  domain inputs and persisted evidence remain native. Table-less requests keep the
  original decoding path. Added sibling-equivalence and negative-boundary tests.
- Corrected the new expander's Python/wire field-name mapping before qualification.
  Preserved native operation-specific uniqueness instead of inventing blanket rules.
- Review found JSON Schema whole-number floats were valid but not Python indices.
  Normalized already-validated route counts, matching the existing workflow detail
  convention, and added a focused regression for both purposes and fractional rejects.
- Updated affected generated-facade expectations and interface-version assertions.
  The existing main-advancement fixture mixed uncommitted new contracts with an old
  accepted tree and a new manifest; changed that one fixture to commit a coherent
  candidate before testing advancement. The Engine's rejection was correct.
- Expanded the write set to those directly affected test consumers and the active
  plan index. No normative policy, approval, provenance, lock or stored-state change.
- Local full coverage, targeted reruns, cold stdio measurements, retained interface-38
  contexts, generated freshness and structural checks are recorded in verification.
  Supported locked runtime, configured-client rendering and independent review remain
  distinct acceptance gates; none is inferred from local schema/unit success.
