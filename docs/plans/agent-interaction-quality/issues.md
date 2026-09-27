# Findings and Dispositions

- Q1 (qualification, integration): supported locked CPython 3.11/3.12 is not
  available in this container. Run locked CI on the delivered diff; local tests
  do not close that gate.
- Q2 (deployment, host operator): raw catalog cost from a live report differs from
  the source measurement. Inventory the actual purpose/mode/catalog before
  attributing the difference to a bug. No automated host reconfiguration.
- Q3 (retirement, integration): actual-client trace reconciliation, other concrete
  supported-client dispositions and independent review have not been supplied.
  Retain compatibility; remove it only at the recorded coordinated cutover.

- Q4 — resolved during implementation: two navigation test-isolation mistakes and
  three cross-package private imports were corrected before the full clean Engine
  run. Initial logs remain in delivery evidence; the final tests/checkpoint passed.
- Q5 — measured tradeoff: full tool-array JSON grows by 78,917 bytes for authoring
  and 31,664 for application, chiefly from typed output schemas. This update improves
  action feedback and repeated routing responses; it does not claim smaller complete
  catalogs or model-token savings. The inventory utility supports actual host
  measurements before any further optimization or compatibility retirement.
