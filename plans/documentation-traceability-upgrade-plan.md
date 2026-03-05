# Plan: Documentation Traceability Upgrade

## Objective

Upgrade documentation standards so module docs preserve design intent, API consumer guidance, and decision rationale instead of generic file-inventory text.

## Scope

### In Scope

- Update documentation standards to require meaningful rationale content.
- Update README template to support explicit "None" cases without inventing decisions.
- Strengthen decision-traceability script with placeholder detection and "None" validation rules.
- Update hook template guidance so decision-traceability checks are included by default.

### Out of Scope

- Full retrofit of all existing READMEs across downstream repositories.
- Project-specific architecture rewrites in downstream repositories.
- Replacing ADR policy or changing commit formatting standards.

## Inputs

### Problem

Current standards enforce README structure, but many generated READMEs are semantically empty and do not preserve why decisions were made.

### Constraints

- Standards must remain reusable across language stacks.
- Rules must avoid forcing fabricated rationale when no alternatives existed.
- Enforcement should be deterministic and lightweight for local hooks and CI.

### Assumptions

- Repositories adopting these standards can run bash-based validation scripts.
- Existing consumers prefer incremental standards changes over a full process reset.
- "None" sections are acceptable when accompanied by concrete justification and revisit conditions.

### Dependencies

- `DOCUMENTATION-STANDARDS.md`
- `templates/README-TEMPLATE.md`
- `templates/check-decision-traceability.sh`
- `templates/lefthook.yml`
- `TOOLING-STANDARDS.md` for hook integration consistency

### Risks

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Overly strict checks create false positives | Medium | Start with clear placeholder bans and explicit pass criteria; document examples. |
| Teams bypass documentation checks | High | Make hook template include traceability by default and align CI guidance. |
| Authors write low-value filler to pass checks | High | Enforce banned phrase patterns and require concrete reason/revisit fields for `None` cases. |

## Clarifying Questions (Only If Needed)

- None at this time.

## Definition of Done

- Documentation standard defines semantic quality requirements, not only section presence.
- README template supports truthful `None` entries with required context.
- Traceability script fails on placeholder language and invalid `None` usage.
- Hook template includes decision-traceability check in default recommended setup.
- Changes are internally consistent with existing plan/tooling/documentation standards.

## Milestones

### Milestone 1: Update Documentation Policy

**Goal:** Encode semantic documentation quality requirements in the standards.

**Tasks:**
- [x] Add rules for "required section must have concrete content or explicit `None` with reason + revisit trigger."
- [x] Add banned placeholder language examples.
- [x] Add API consumer contract requirements for host-facing modules.
- [x] Define minimum meaningful content expectations per section.

**Verification:**
- Manual review against `PLAN-STANDARDS.md` and `DOCUMENTATION-STANDARDS.md` for consistency.
- Confirm policy language includes no requirement to fabricate rejected alternatives.

**Status:** Complete

### Milestone 2: Update README Template

**Goal:** Provide a template that drives useful, truthful documentation output.

**Tasks:**
- [x] Replace filler-prone prompts with decision-focused prompts.
- [x] Add explicit `None` pattern examples with required reason and revisit trigger.
- [x] Add API usage/contract section for client-facing modules.

**Verification:**
- Render template as markdown and confirm required sections map to policy.
- Validate template includes concrete "good" examples and no placeholder boilerplate.

**Status:** Complete

### Milestone 3: Strengthen Traceability Enforcement

**Goal:** Enforce content quality guardrails automatically.

**Tasks:**
- [x] Add placeholder phrase detection to `check-decision-traceability.sh`.
- [x] Validate `None` entries require reason and revisit trigger markers.
- [x] Keep checks fast and compatible with existing diff-based module detection.

**Verification:**
- Run script against sample passing and failing README fixtures.
- Run `bash -n templates/check-decision-traceability.sh`.

**Status:** Complete

### Milestone 4: Hook Template and Adoption Guidance

**Goal:** Ensure enforcement is actually enabled when standards are adopted.

**Tasks:**
- [x] Confirm `templates/lefthook.yml` keeps decision-traceability enabled by default.
- [x] Add adoption note in standards README pointing to script + hook wiring.
- [x] Cross-check with `TOOLING-STANDARDS.md` examples.

**Verification:**
- Validate hook template references the script path correctly.
- Manual consistency check across modified standards docs.

**Status:** Complete

## Execution Notes

Update during implementation:
- 2026-03-05: Plan created.
- 2026-03-05: Milestones 1-4 implemented with atomic commits per task.

## Commit Cadence Notes

- Commit each completed milestone as a verified logical slice.
- Follow `COMMIT-STANDARDS.md` for commit formatting and history cleanup.

## Optional Subagent Assignment

| Owner/Agent | Scope | Output Contract | Handoff Checkpoint |
| ----------- | ----- | --------------- | ------------------ |
| N/A | N/A | N/A | N/A |

## Re-Plan Triggers

- New requirement conflicts with current README or ADR traceability rules.
- Validation script performance or portability issues block adoption.
- Downstream pilot feedback shows high false-positive rates.

## Recommendations (Only If Better Option Exists)

- Recommendation: Add a small CI fixture suite for documentation-lint script behavior; this reduces regression risk in standards updates with minimal maintenance cost.

## Completion Summary

### Completed

- Updated documentation policy with non-fiction section completion rules.
- Added banned placeholder language policy and quality minimums by section.
- Added host-facing API consumer contract documentation requirements.
- Updated README template prompts, `None` examples, and contract section.
- Enhanced traceability script for placeholder rejection and `None` marker validation.
- Kept diff-based traceability detection while improving lookup performance.
- Synced hook template, standards README, and tooling examples for adoption.

### Deviations

- None.

### Follow-Ups

- Consider extending base-ref resolution in traceability script for single-branch
  repos where `main...HEAD` or `master...HEAD` may resolve to no-op diffs.

### Verification Summary

- `bash -n templates/check-decision-traceability.sh`
- Fixture run (pass and fail cases) using
  `TRACEABILITY_BASE_REF=HEAD~1 ./scripts/check-decision-traceability.sh`

### Traceability Links

- Module README updated: N/A (standards repository)
- ADR added/updated: N/A
- PR notes completed per `templates/PULL_REQUEST_TEMPLATE.md`: Pending PR creation

## Brevity Note

The plan is concise by default and expands only where execution decisions or risk controls require detail.
