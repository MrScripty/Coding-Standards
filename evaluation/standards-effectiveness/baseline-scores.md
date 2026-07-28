# Baseline Scenario Scores

## Rubric

Scores use the fixed scale in `README.md` across these dimensions:

- `A`: applicability;
- `O`: objective fidelity;
- `W`: ownership;
- `C`: complection control;
- `V`: verification fidelity;
- `L`: current-state legibility;
- `R`: re-plan containment;
- `P`: process proportionality; and
- `E`: contract evolution.

## Scores

| Scenario | A | O | W | C | V | L | R | P | E | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S1 small fix | 0 | 2 | 1 | 1 | 2 | 1 | 0 | 0 | 2 | 9/18 |
| S2 desktop workflow | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 6/18 |
| S3 durable worker | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 6/18 |
| S4 Rust FFI | 0 | 1 | 1 | 1 | 2 | 1 | 0 | 0 | 1 | 7/18 |
| S5 persisted break | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 4/18 |
| S6 dependency release | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 2 | 7/18 |
| S7 hardware capability | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 4/18 |

**Aggregate:** 43/126 (34.1%).

## Evidence Summary

- Applicability is `0` because the root quick start requires reading every
  document and no deterministic precedence/router contract exists.
- Objective fidelity is partial for cross-layer work: testing guidance requires
  real full paths, but planning closure does not require a named
  objective-level acceptance path.
- Ownership is partial because generic, architecture, testing, tooling,
  application, and language files repeat or specialize rules without declared
  canonical owners.
- Complection is partial or absent where normative rules, examples, tool
  recipes, state, and history share documents and lifecycle.
- Verification is strongest for focused tests and bindings, but the universal
  E2E duration/CI row and missing environment-gated closure make hardware and
  user-workflow outcomes ambiguous.
- Legibility is partial because plan templates expose milestones but only three
  statuses and no active-state/history separation.
- Re-plan containment is absent because new decisions are appended without a
  supersession and rollover contract.
- Proportionality is absent because every source directory requires a README,
  changed source requires README/ADR traceability, and full history inspection
  is required before every commit.
- Evolution is adequate for conventional public release scenarios but fails
  coordinated persisted replacement because immutable append-only guidance and
  broad degraded-mode examples are not authority-aware.

## Baseline Routing Load

The current quick start directs adopters to read every standards document.
Therefore every scenario has a baseline routed set of 100% of normative and
operationally derived guidance. The baseline median is 100%.

This is a routing measurement, not a claim that every sentence is semantically
applicable to every task.
