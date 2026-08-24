# Standards Recovery Plan Admission Review

## Reviewed Boundary

- Result: `Rejected`.
- Candidate commit: `e000ddc20b99e568f0b86d2910be9769699a1155`.
- Candidate tree: `243f5759a51068e415c17cbee550d3570e617d5f`.
- Comparison baseline: commit
  `3439aae9540786d9734431e633ea5b62afb50592`, tree
  `0ff4af77ebe5056c9478f04bf65dd87141f573d8`.
- Review axes: repository Standards and A1b-authoring-brief specification.
- Implementation admission: none. The plan remains `Blocked`.

## Standards

1. **High - verification authority and write set conflict.** Milestone 1 adds a
   new Bash recovery checker and changes existing Bash plan checkers while the
   active verification-engine plan owns Bash retirement. The proposed write set
   also omits generated checker graph artifacts affected by adding a checker.
   Prefer declarative-suite enforcement; otherwise coordinate the active
   migration authority and every generated projection before admission.
2. **High - Licensing decision is incomplete.** The plan selects and vendors a
   pinned third-party test subset without recording the copyright owner,
   authoritative terms, intended use and distribution, compatibility decision,
   or resulting obligations required by Licensing. Copying the upstream license
   file alone is not the incorporation decision.
3. **Medium - historical rejection is duplicated in current plan authority.**
   The rejected boundary belongs in the ledger and reports, not beside current
   binding fields in `plan.md`.

Standards total: three findings; worst severity: High. No baseline smell finding
was identified.

## Specification

1. **High - consumer-audit sequencing is incomplete.** The inventory explicitly
   leaves the independent horizon and known consumer classes unaudited, while
   the plan defers completion until Milestone 0 after plan admission. Admission
   is required to confirm a complete scope and consumer audit. Re-plan to admit
   only reproduction/audit work first and require a second exact-tree admission
   before policy mutation, or complete the audit before initial admission.
2. **Medium - the accepted A1 reproduction boundary is absent.** Phase 0 does
   not bind accepted A1 commit
   `2359a98740b6035a0414bfaf5427ceaa1301a1c8` and tree
   `97c850ab718287007c1e1daac538f40869f71a1d`, despite the brief requiring that
   boundary before historical-family reproduction.

Specification total: two findings; worst severity: High. The seven findings
from the prior admission rejection are repaired, and no A1b runtime or A2 scope
appears in the candidate.

## Verification Context

The exact candidate was clean. Focused plan checks, generated-artifact
freshness, all 218 registered declarative suites, all 53 retained Bash checkers,
and diff validation passed. These mechanical results do not prove the missing
authority, licensing, or audit-sequencing contracts.

## Admission Decision

Admission is rejected. No implementation base is bound and no policy, A1b, or
A2 operation is authorized. The next operation is a planning revision that
resolves all five findings, followed by another independent exact-tree review.
