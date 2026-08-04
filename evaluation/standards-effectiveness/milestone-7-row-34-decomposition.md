# Milestone 7 Row 34 Frontend Decomposition

## Owner Contract

`profiles/applications/frontend.md` owns UI projection, rendering lifecycle,
interaction adaptation, frontend state synchronization, and frontend-specific
evidence. It does not own domain state, generic async lifecycle, tooling
orchestration, TypeScript configuration authority, evidence acceptance meaning,
or accessibility outcomes.

TypeScript Async and Concurrency own overlapping work, cancellation, stale
completion, and result application. The TypeScript profile and Tooling own
static-analysis configuration and orchestration. Verification owns evidence
kind and environment. Accessibility owns supported user-access outcomes.
Frontend specializes those contracts only through concrete UI mechanisms.

## Exact Ownership

- `STD-0449` is an index and `STD-0450` refines Frontend applicability.
- `STD-0451` is an index; `STD-0452` and `STD-0453` split rendering and
  synchronization policy from TypeScript, DOM, event, timer, and FFI examples.
- `STD-0454` splits frontend lifecycle evidence from React timer mechanisms
  while preserving TypeScript Async and Concurrency authority.
- `STD-0455` is an index and `STD-0456` splits TypeScript static-analysis
  selection from React ESLint configuration examples.
- `STD-0457` through `STD-0463` are indexes to the accepted claim-selected
  Frontend evidence contract. Deleted selector, event, DOM-shim, geometry,
  timer-spy, and smoke-check defaults must not return.
- `STD-0464` is an index to Accessibility outcome authority and Frontend
  mechanism specialization.

Each identifier receives exactly one disposition. Frontend and React mechanisms
may appear only in non-normative recipes after canonical owners select them.

## Ordered Children

1. `34.1`: record `STD-0449` and `STD-0450` parent and applicability
   lineage.
2. `34.2`: migrate `STD-0451` through `STD-0453` rendering and
   synchronization and extract fixed mechanisms.
3. `34.3`: migrate `STD-0454` lifecycle-owned timer proof and extract React
   hook mechanisms.
4. `34.4`: migrate `STD-0455` and `STD-0456` TypeScript static-analysis
   routing and extract React ESLint configuration.
5. `34.5`: record `STD-0457` through `STD-0463` exact lineage to accepted
   claim-selected Frontend evidence without restoring retired mechanisms.
6. `34.6`: route `STD-0464` to Accessibility, close the legacy source, and
   run the P28 full-suite integration gate.

Shared decomposition, dispositions, plan, ledger, source closure, and cursor
assertions remain serial. Each child may additionally touch only its canonical
owner, the non-normative Frontend or Tooling recipe, its legacy section, and
focused fixtures and checker.

## Typed Outcomes And No Fallback

Return `unavailable` when state authority, projection, synchronization,
lifecycle owner, configuration authority, accessibility contract, environment,
or evidence is absent; `invalid` for contradictory ownership, stale result
application, inaccessible interaction, incomplete cleanup, unsafe rendering, or
false claims; and `unsupported` when the selected platform or mechanism cannot
satisfy a valid contract.

Do not fall back to copied UI state, DOM authority, declarative or imperative
rendering by default, event or polling by default, global timers, fixed cadence,
React hook patterns, disabled lint rules, selector priority, synthetic browser
proof, mocked geometry, pointer-only interaction, omitted accessibility, stale
content, empty success, or weaker evidence.

## Re-plan Triggers

Stop if implementation requires Frontend to own domain, generic async, Tooling,
Verification, or Accessibility policy; a React normative profile; restoration
of deleted testing mechanisms; multiple dispositions per identifier; a seventh
semantic child; or files outside the approved write sets.
