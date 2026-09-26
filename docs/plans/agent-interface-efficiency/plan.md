# Agent Interface Efficiency

Status: Verifying
Acceptance: pending
Base: `34c2dcbaf9aa7ade5589ae5c88383719dda81200`
Operation: implement this plan; user-authorized continuation of the MCP simplification.

## Objective and admission

Reduce repeated schema descriptions, route/read round trips, and repeated evidence
references without changing policy, exact authority, review or publication meaning.
The first workflow simplification is already integrated; retain its immutable
contexts, bounded work pages, explicit decisions and lightweight status reads.

The executable Router was run against the base with explicit task facts and no
unresolved conditions. Selected concerns: implementation, verification, planning,
documentation, build, development proportionality; library; generated-contract and
IPC boundaries; contracts, architecture, dependencies, security, diagnostics and
performance; code design, replay, schemas, protocol adapters, evolution and test
oracles. No dependency, normative-policy or persistence-format change is planned.

The existing schema/compiler, facade, navigation projection and MCP transport own
this work. No workflow store, evidence registry, model evaluator, session pointer,
new authorization mechanism or general-purpose orchestration language is admitted.
The composed design has three independent presentation concerns; existing domain
operations still own routing, reads, evidence verification and decisions.

## Decisions

1. Host-selected MCP schema presentation: compatibility remains the default for
   known clients with incomplete nested-schema rendering. Native presentation uses
   the smaller complete inline/reference projection without schema text in descriptions.
   Both modes validate exactly the same inputs. No client-name heuristic or hidden
   downgrade; a restart chooses another catalog and its existing digest identifies it.
2. Optional `route.content` requests a bounded page of selected exact compact reads.
   Route and reads share one snapshot and compiled input. Page count is bounded;
   byte pressure returns fewer whole items with an exact snapshot/facts continuation.
   Unknown facts, full dependency qualification and purpose filtering are unchanged.
   An oversized first record returns a bounded typed limit rejection, never a
   truncated policy. Plain route and explicit single/grouped reads remain supported.
3. Authoring agent inputs may supply a request-local `evidence` table and typed
   `evidence_ref` uses. Generated agent input variants preserve native domain input
   types; the facade validates and expands only typed reference positions, then
   validates the native call before dispatch. Every use explicitly selects evidence.
   Missing/unused entries reject before effects; native evidence uniqueness is enforced after expansion.
   Provider/digest/current-authorization checks and expanded batch limits are unchanged.

## Compatibility and state

Interface 39 is an additive request capability and coordinated catalog update.
Native authoring request types, Analysis request/state versions, all handles, SQLite,
readiness, application and recovery representations stay unchanged. Application
catalogs contain no authoring evidence variants. Native schema mode is opt-in until
actual configured-client qualification is available. Restart/reconnect clients;
preserve stores, proposals and exact contexts. No automatic retries or publication.

## Write set

- Engine canonical schema/interface and generated model/tool projections.
- `tools.py`, `mcp.py`, `agent_navigation.py`, `context_projection.py`, plus one
  request-local evidence normalization module if required by its separate concern.
- Focused contract, navigation, evidence and MCP tests; affected catalog consumers,
  examples and optional configured-client harness.
- Engine READMEs/PURPOSE-SEPARATION and authoring/navigation/environment skill references.
- This plan, ledger, issues and verification; generated suite-input manifest.

Directly affected consumers inside these owners may be added in the ledger.
Normative content, approvals, provenance, locks and user stores are outside the write set.

## Acceptance

- Canonical native/agent schema validation and independent Draft 2020-12 validation
  agree for valid and malformed fixtures in both presentation modes; generated
  outputs are fresh. Input fields, omissions, recursion and extra-field rejection
  retain meaning. Runtime catalog identity tracks actual definitions; equivalent catalogs share an identity.
- Route-content equals ordinary exact reads, including all pages; known missing
  facts stay unresolved; partial pages, oversized records, invalid selections,
  unavailable qualifications and snapshot lifecycle changes are explicit.
  One compiled input is used per call, without additional snapshot capture.
- Shared and inline evidence produce identical exact native decisions/analysis and
  review outcomes. Alias errors, stale evidence, unsupported providers, foreign work,
  native uniqueness violations after expansion and expanded-size overflow publish nothing. Cold process
  reconstruction needs no alias table. Caller inputs remain unchanged.
- Real stdio traces compare call counts and serialized request/result/catalog bytes
  against the base. Report tradeoffs; byte counts do not claim token/billing savings.
- Focused and affected package suites, structural checkpoint and patch reconstruction
  pass. Supported locked Python 3.11/3.12, configured-client qualification and
  independent review remain separately named gates when unavailable locally.

## Sequence and next slice

Implement the three bounded concerns with tests, regenerate contracts, run integrated
checks and measurements, then package changed files and review evidence. Current next
slice: integration qualification and independent review after the local verification
and base-pinned delivery. Implementation of the three admitted concerns is complete;
remaining acceptance gates are tracked in issues.md and verification.md.
