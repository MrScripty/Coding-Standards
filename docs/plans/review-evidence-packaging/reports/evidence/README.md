# Planning evidence

These are source-selection and request-shape probes, not production packet code or
candidate acceptance. `probe.py` and `check-request-shape.py` record the exact
planning experiments; they use the task-local `/mnt/data/review-packet-planning`
layout. Adapt those owned paths deliberately to reproduce them. Do not run them
as an installed generator or infer that they implement the plan's safety contract.

The current source archive was verified before a clean isolated clone was inspected.
`standards-route.json` and `standards-readback.json` record actual interface-45
routing of the planning task and its 25 selected standards. `design-probe.json`
records exact file-object reading, byte counts, limited subtree equality and the
separate dirty-worktree/archive fixture. The full primary and supplemental patch
bytes were measured locally, not delivered as an implementation change.

`request-shape-check.json` checks the proposed JSON syntax with the existing
Draft 2020-12 validator. It does not resolve request references, read external
files, build an archive, or evaluate claim/evidence truth. `planning-validation.json`
records the current repository plan validator, link checks and clean source state.
The initial field-format diagnostic is preserved separately from the successful
final validation.

Historical review/source statements are not independently rerun tests. Missing
historical logs, performance recordings or external evidence remain unavailable
unless explicitly provided at future implementation/recipient qualification.
