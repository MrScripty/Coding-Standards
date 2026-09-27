# On-demand output-contract delivery

> **Scoped supersession:** [Native-only MCP](../native-only-mcp/plan.md) now owns
> input presentation and launch cutover. Its native-only decision replaces this
> plan's compatibility-retention/mode guidance, not its other features, historical
> measurements or outstanding evidence. Output eager/on-demand delivery remains
> independently supported.

Status: Verifying
Acceptance: pending
Phase: local implementation and verification complete
Next slice: supported-runtime CI, actual-host on-demand qualification and independent review.
Base: `52b122683faf05ef85c86c6903a61d54870a9be4`
Operation: verify; user-authorized continuation of the agent interaction work.

## Objective and scope

Reduce the initial MCP catalog by offering exact output contracts on demand. Keep
existing canonical validation, structured results, errors, evidence, atomic
workflow decisions, publication, recovery and all retained identities unchanged.
The executable Router selected implementation, verification, documentation, build,
planning, proportionality, library, generated-contract/IPC, contracts, architecture,
security, diagnostics, performance and their selected details with no unknown facts.
Readback is retained in delivery evidence. This is code maintenance, not policy editing.

## Decisions and ownership

- `--output-schemas eager|on-demand` is a host-owned delivery choice independent of
  input schema presentation. Eager remains the default for existing supported
  consumers. An explicit on-demand catalog omits `outputSchema`, rather than
  publishing a permissive substitute, and points to `describe_output`.
- `describe_output` exposes the canonical purpose/operation result algebra and
  bounded definition pages, not a schema for MCP's outer CallToolResult envelope.
  It shares selection, reference traversal and pagination with `describe_input`.
  Input discovery's wire shape stays intact. No registry or mutable session is added.
- Each omitted schema has a canonical digest in tool `_meta`. This keeps the
  existing catalog digest sensitive to output-only contract changes. Discovery
  returns that same digest. Digest equality permits client reuse of exact schemas;
  it is not authorization and does not equate different operation capabilities.
- Both delivery choices continue through the existing typed result construction.
  The discovery services validate their own generated result envelopes. Client-side
  validation can use a retrieved exact schema or the eager catalog.
- Actual-host qualification owns promotion of on-demand delivery. The existing
  Codex harness will test that choice without supplying output schemas to the model
  out of band. Observer validation may use the canonical schema independently.
- Interface 42 records the additive discovery tool/catalog option. Previous
  operation and persisted definitions remain unchanged. Restart/reconnect for the
  new tool/catalog, preserve stores, snapshots, proposals, readiness and recovery.

## Composed-design review: applicable

1. Concerns: contracts own output semantics; discovery owns immutable definition
   selection/paging; MCP catalog owns transmission; the host chooses delivery at
   startup; the facade/domain owns validated execution; tests own observation.
2. Necessary interleaving: purpose/operation selects result roots and the running
   catalog binds discovery. Output transmission does not affect workflow state.
3. Caller knowledge: operators select delivery; clients inspect structured results
   and discover exact schemas only as needed; startup owns one compiled interface.
4. Change paths: result shape changes update its canonical owner/generation and
   tests; page policy changes discovery; delivery policy changes catalog/startup.
5. Dependencies: existing compiled contracts and structural reference traversal;
   no private Git/store representation is exposed to discovery.
6. Independence: both wire deliveries share the same result validation. Input and
   output discovery share mechanics but retain separate scoped roots and outcomes.
7. Deletion: removing discovery would force full eager output or duplicated schema
   descriptions. Removing eager now would break supported validating consumers.
   Removing the digest would permit an output-only change to retain the catalog ID.
8. Complexity: one shared definition observer, one public output-discovery tool,
   one startup selection, no new persistence, validator, background task or transport.

## Write set

Engine canonical schema/interface/examples and generated projections; existing
input discovery generalized into contract discovery; MCP catalog/server; facade;
CLI observer wiring; catalog inventory; affected qualification harness/replay and
focused tests; Engine docs and skill references; this plan/ledger/issues/report;
generated verification input manifest. New files remain within these owners.
Normative standards, approvals/provenance, locks, production stores, user ZIPs and
remote refs are excluded. No dependency update is admitted.

## Acceptance

A1: All purpose-qualified output schemas reconstruct exactly through whole-record
pages in either delivery/input mode, including recursion and typed rejections.
A2: On-demand catalog omits eager output schemas, reports exact schema digests,
preserves validation and result bytes, and rejects stale/off-purpose selection.
A3: Real MCP stdio navigation, rejection and proposal-to-readiness paths work with
retrieved output validation; no automatic discovery per action or publication.
A4: Measure full catalogs and separately record descriptions/input/output/meta;
report bytes, not token/latency savings. Existing host harness supports this mode.
A5: Focused/affected checks, generated freshness, structural verification and patch
reconstruction pass. Supported-runtime CI, actual client/model observation and
independent review remain separately recorded when unavailable here.

Milestones: shared discovery/catalog and local consumer measurements complete;
base-pinned delivery verified locally. Actual-host qualification and external
acceptance remain pending, with eager kept as the default.
Replan only for a change to semantic authority, admission or client requirements.
See [execution ledger](execution-ledger.md), [issues](issues.md), and
[verification](verification.md).
