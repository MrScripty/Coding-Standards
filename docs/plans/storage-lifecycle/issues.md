# Issues and dispositions

- **L-E1 / environment:** local Python 3.13.5 and rpds-py 2026.5.1 are outside the repository's locked Python 3.11/3.12 environment. DNS prevented provisioning. Owner: integrator. Disposition: run the unchanged locked CI before acceptance; local evidence is not relabeled.
- **L-E2 / review:** independent material review is not available locally. Owner: integrator/reviewer. Disposition: review exact source and lifecycle/race evidence before acceptance.
- **L-D1 / scope:** a no-work purge result is never cached and does not authorize deletion. Recheck after writer admission; actual due work retains BUSY. Owner: Snapshots. Disposition: fix now with real race/lock tests.
- **L-D2 / scope:** full integrity auditing remains once per current-store open. Migration/creation validation is retained; scheduled audits, weaker PRAGMAs, indices and connection reuse are excluded. Owner: Snapshots. Revisit only with a separately admitted scale/integrity claim.

- **L-T1 / test corrections (resolved):** corrected root-versus-record diagnostic expectation and the private-stderr boundary for open-time MCP BUSY; final tests cover both. Production error contracts remain unchanged. Interrupted preliminary tool calls remain uncounted.
- **L-R1 / implementation complete:** no-work writer admission and duplicate current-store full auditing are removed with the race/corruption oracles preserved. Full final local campaign passed. Broader scale/audit scheduling remains explicitly deferred, not silently implemented.
