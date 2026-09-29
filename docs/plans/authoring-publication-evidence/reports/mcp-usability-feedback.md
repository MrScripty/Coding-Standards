# Standards Engine MCP usability feedback

**Observed:** 2026-09-29, while admitting A1 from the isolated implementation
worktree. The live MCP reported interface 45 and implementation 0.2.0, with the
installation current and suitable for reuse. It was not restarted or modified.

## Calls and results

| Call | Result | Usefulness |
| --- | --- | --- |
| `runtime_info` | Returned the live interface, implementation, and installation state. | Useful to confirm the existing process could be reused before reading standards. |
| `routing_facts` | Returned snapshot `snapshot:v1:322889ba-df55-43d9-a2a5-68c1993dd498`. | Useful stable boundary for the rest of the authoring reads. |
| `route` with selected implementation, planning, verification, and commit concerns, plus architecture, contracts, security, diagnostics, and workflow tags | Returned an oversized result that was truncated by the caller. | The selection itself was relevant, but the chosen broad route did not fit the available response window. |
| `read_many` for the selected core, implementation, planning, commit, verification, standards-authoring, architecture, code-design, contracts, and security materials | Returned the selected source material against the same snapshot. | More useful for focused reading after the route response was too large. |

The practical sequence was to check runtime state, capture one snapshot, request
a bounded selection, then read only the sources needed for this change. `route`
remains useful for discovery, but broad combined topic/tag selection should be
split or followed by `read_many` rather than consumed as one large result. This is
feedback from one authoring session, not a general latency or reliability claim.

The root implementation agent made the MCP calls. The fixture and architecture
review workers did not use MCP; their work used the isolated repository source,
tests, and the admitted plan. Local Engine verification was performed through the
owner's `verify_repository(refresh_verification_inputs=True)` operation and did
not restart or replace the live MCP process.

## 2026-09-29 — final A1 routing check

The integration owner reused the same snapshot for the final A1 obligations check.
`routing_facts(snapshot)` made the registered fact vocabulary and allowed values
available without capturing another view. The first `route` call returned
`needs-facts` because the owner had omitted the framework fact; supplying the
observed empty framework set produced a complete route with no unresolved
questions or policy items. The explicit missing-fact result was useful and the
correction was small.

The complete route selected 30 standards. A broad `read_many` page for eight
selected standards returned more source text than the caller window could retain.
Reading a smaller, named subset is the safer way to inspect obligations; the
route selection itself remained useful. A concise per-standard summary or a
caller-selectable content budget would reduce truncation while preserving exact
source reads on demand.

Only the integration owner reports Standards Engine MCP use. The GPT-6.1 Sol
fixture writer, Astra architecture and standards reviewers, Luna spec reviewer,
observer reviewers, and archive/plan discovery workers reported no MCP calls;
their source and acceptance findings are recorded in the execution ledger. Their
MCP usability experience is therefore not inferred from the owner's calls.
