## Intent

Create an auditable, implementation-ready refactor plan that brings the target codebase into compliance with the standards in <path>. Because the standards may overlap across the same files, modules, or architectural boundaries, treat findings as a combined constraint set rather than isolated rule violations. The final plan must resolve multi-layered refactor recommendations into a sequenced implementation path that can be executed safely, including by parallel sub-agents where non-overlapping work can be delegated.

This task is planning only. Analyze the codebase thoroughly, record findings in Markdown, and produce the final refactor plan. Do not modify source code or implement the refactor.

## Artifact Rules

This is a read-only analysis for source code and project files. Do not create, edit, delete, format, or otherwise modify source code, tests, configs, build files, lockfiles, generated files, or other project implementation files. The only files you may create or edit are Markdown files used to record refactor pass instructions, findings, reports, ledgers, and the final refactor plan.

Write all refactor planning Markdown artifacts under the documentation artifact layout defined by `DOCUMENTATION-STANDARDS.md`. Use `docs/refactors/<refactor-slug>/` as the artifact root, with subdirectories such as `pass-instructions/`, `findings/`, `implementation-waves/`, and `reports/`, plus `coordination-ledger.md` and `final-plan.md`.

Follow the large refactor planning and concurrent worker planning requirements
in `PLAN-STANDARDS.md`.

## Process

Because the codebase is large and the standards may overlap, use an iterative multi-pass process:

1. Map the standards files under <path> and use their existing topic and language grouping to define focused analysis passes.
2. For each focused analysis pass, write a complete Markdown instruction file under `docs/refactors/<refactor-slug>/pass-instructions/` before launching any sub-agent.
   - Assign one selected standards file or closely related set of standards files.
   - Define the code areas the pass should inspect.
   - Tell the pass agent to keep the assigned standards prominent in context while inspecting the code.
   - Tell the pass agent not to discard standards because they are broad, qualitative, or not immediately reducible to a simple rule.
   - Tell the pass agent to record how each applicable standard constrains the refactor, and to defer non-applicable standards to the pass where they belong.
   - Require findings to include affected files, relevant code areas, violated standards, and required constraints.
   - Require unrelated issues to be recorded separately, such as bugs, stubs, missing tests, performance problems, or risky design gaps, if they will not be resolved by standards compliance.
3. Launch dedicated sub-agents for independent pass instruction files and run those analysis passes in parallel when their standards groups can be reviewed independently.
   - Each sub-agent must receive exactly one complete pass instruction file or prompt.
   - The sub-agent must be able to run to completion from that single instruction set without follow-up messages.
   - Each sub-agent must write its own Markdown findings file under `docs/refactors/<refactor-slug>/findings/`.
4. After discovery, group all findings by code area and treat them as a combined constraint set.
5. Create unified refactor recommendations for each area so overlapping standards are solved together.
6. Identify dependencies between recommendations and order them into a sequenced implementation plan.
7. Design the implementation sequence as phased parallel execution waves that can later be delegated safely to implementation sub-agents.
   - Follow the large refactor and concurrent worker plan requirements in `PLAN-STANDARDS.md`.
   - Write implementation wave and slice specs under `docs/refactors/<refactor-slug>/implementation-waves/`.
   - Require future implementation sub-agent reports under `docs/refactors/<refactor-slug>/reports/`.
   - Include the host-owned coordination ledger at `docs/refactors/<refactor-slug>/coordination-ledger.md`.
8. Re-check the complete plan against all standards and recorded findings.
9. Revise the plan and repeat validation until a full pass produces no new required changes.
10. Output the final plan to `docs/refactors/<refactor-slug>/final-plan.md` as a non-iterative implementation sequence, with each step listing affected files/areas, standards satisfied, dependencies, risks, validation criteria, ownership slices, safe parallel waves, required sub-agent report files, and coordination ledger structure.

Do not implement the refactor and do not launch implementation sub-agents. Produce the plan and supporting Markdown findings only. Take the time needed for a thorough analysis.
