# Schema Projection Correctness and Ownership

> **Scoped supersession:** [Native-only MCP](../native-only-mcp/plan.md) now owns
> input presentation and launch cutover. Its native-only decision replaces this
> plan's compatibility-retention/mode guidance, not its other features, historical
> measurements or outstanding evidence. Output eager/on-demand delivery remains
> independently supported.

Status: Verifying
Acceptance: pending
Base: `ebf2fda1c10a69db2dcdff463a8f6a46d34ffac6`
Authority: user-authorized implementation of the schema-retirement review.

## Outcome and admission

Preserve literal JSON values and field names while projecting the admitted schema
profile; centralize structural traversal and reference discovery; separate pure
MCP catalog construction from transport; remove caller-supplied decoder types that
have no effect. Keep validation, purpose filtering, evidence expansion and durable
Engine authority with their existing owners.

The executable Router was run against the exact base with explicit facts and no
unresolved conditions. It selected implementation, verification, documentation,
planning, build, commit, development proportionality; library, generated-contract
and IPC profiles; contracts, architecture, dependencies, security, diagnostics,
performance, code design, replay, schema/protocol/evolution and oracle guidance.
No dependency, normative policy, persisted format or user-store changes are admitted.

This is a systemic schema-location defect with a bounded consumer family:
contracts compiler/profile traversal, post-validation union selectors, MCP schema
projection and CLI schema inspection. All use the contracts package's structural
owner. JSON Schema validation and reference evaluation remain delegated to
jsonschema/referencing. The new utility traverses the admitted profile plus the
adapter's emitted allOf; it does not admit new canonical keywords or evaluate
constraints. Missing real references retain explicit failures; annotation and
const/enum payloads remain uninterpreted data.

## Decisions and boundaries

- Introduce a small contracts-owned structural traversal/reference utility, used by
  the four consumers. Preserve recursion and reference-sibling constraints.
- Make mcp_catalog accept an already compiled interface and explicit catalog choices.
  MCP/CLI/client composition loads the installation. Transport retains JSON-RPC,
  connection lifetime and result framing; no catalog framework or plugin registry.
- Derive decoded types from the selected operation contract. Keep the fast native
  table-less evidence path and full validation before domain dispatch.
- A reproduced $ref-named field also yields invalid generated Python. Fix that
  affected name projection with deterministic escaping and collision checks;
  existing valid Python field names and wire names remain unchanged.
- Keep interface 39, all wire schemas, handle/state versions and stores unchanged.
  Current corpus catalogs must remain identical in both modes and purposes.
- Retain compatibility as default and the current native size selection until the
  actual supported clients are qualified. Do not combine semantic repair with an
  unqualified catalog change. A reference-only native projection is a later explicit
  decision, not a new configuration option.

## Write set

Contracts structural utilities, compiler and union selectors; Engine mcp_catalog,
mcp transport imports and facade decoder; CLI and affected tests/client harnesses;
package ownership documentation; this plan/ledger/issues/verification and plan index;
generated suite-input manifest. Generated model/tool outputs change only if their
canonical generator requires it. No direct edits to normative standards, approvals,
provenance or retained stores.

## Acceptance and sequence

1. Reproduce pre-change failures; add independently expected positive/negative cases
   for schema versus data positions, literal field names, constants/enums/defaults,
   recursive definitions, real missing/unsupported references and reference siblings.
2. Implement the shared owner, pure catalog boundary and facade cleanup; migrate
   internal consumers atomically. Test generated Python construction as well as
   canonical validation and MCP/CLI presentation.
3. Run affected packages, real stdio/CLI checks, generated freshness, the complete
   structural checkpoint, and exact baseline catalog comparisons. Inspect the diff
   and reconstruct the delivery from its pinned base.
4. Record local results separately from supported locked-runtime, configured-client
   and independent-review evidence. Acceptance remains Verifying when unavailable.

Implementation and local qualification are complete; see [verification](verification.md).
Supported-runtime local integration checks are recorded in verification.md.
Next slice: CI qualification and independent review. Compatibility
retirement remains a separate host-qualification gate; see issues.md for owner and
exit condition.
