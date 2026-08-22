# Audit Follow-Up Admission And Current Baseline

## Authority

- Operation: `continue`.
- Accepted base: `56f5124b1ed848fa80b8f35e46a298d4a33ed37c`.
- Repository state at admission: clean before the plan projection changed.
- Shared authority: one serial integration owner.
- Migration state: no Bash-retirement package is admitted while this recovery
  changes shared verifier evidence and contracts.

## Current Derived Baseline

These values were derived from the accepted repository rather than stored as
configuration constants:

| Observation | Current value | Derivation |
| --- | ---: | --- |
| registered declarative suites | 215 | `verify.py --list` |
| retained Bash checkers | 56 | repository `verify-*.sh` paths |
| verifier unit tests | 373 | discovered test methods |
| neutral graph unit tests | 35 | discovered test methods |
| temporary checker nodes | 60 | generated node rows excluding the header |
| temporary checker edges | 401 | generated edge rows excluding the header |
| temporary checker components | 60 | generated component rows excluding the header |

The Milestone 4 report remains historical evidence for its accepted revision.
It does not establish current performance acceptance because it measured 207
suites and 65 Bash checkers and recorded only one approximate post-change
complete run.

## Architecture Applicability

Architecture is selected only when module responsibility, dependency direction,
composition, data authority, or state ownership changes.

| Change | Architecture result | Reason |
| --- | --- | --- |
| accepted table membership scope | excluded | It extended configuration interpreted by the existing table-check owner; no module, dependency, composition, or authority boundary changed. |
| accepted conditional row constraints | excluded | It added another assertion within the same table-check responsibility and did not create a new owner or dependency direction. |
| exact route selection and graph-derived closure evidence | selected | Connecting scenario decisions to canonical-module resolution and graph closure creates a downstream routing-validation responsibility and explicit dependency on repository graph composition. |
| mechanically derived migration candidate completeness | selected | Establishing a candidate provider and exact comparison with terminal dispositions changes provider responsibility and dependency direction. |
| one shared projection parser inside `table.py` | excluded | This consolidates duplicate parsing inside one existing module and does not move authority. |
| one policy-owned source-index membership composition | excluded if implemented through the existing table source contract | Policy membership remains downstream data and generic table mechanics retain their current owner; re-plan if implementation requires a new owner or reversed dependency. |
| removal of the redundant `EngineError` numeric input | excluded | Exit status remains derived by the existing diagnostics owner; the change removes duplicate input without moving responsibility. |
| performance remeasurement | excluded | Measurement changes evidence, not architecture. Performance is selected separately. |

## Performance Applicability And Budget Authority

Performance is selected because the recovery changes current performance claims,
their evidence, and their acceptance state.

The Python-engine recovery plan owns the five repository-local workflow budgets.
They are maintainer acceptance limits for interactive discovery, focused
feedback, declarative integration, generated freshness, and mixed wave
checkpoints. They are not universal standards or inferred implementation
targets.

The existing limits remain provisional comparison points only:

| Workload | Historical limit | Derivation and consumer decision |
| --- | ---: | --- |
| list | 0.250 s | rounded local interactive-discovery limit above the accepted 0.191 s baseline |
| focused | 0.250 s | rounded local focused-feedback limit above the accepted 0.198 s baseline |
| all declarative | 1.500 s | local integration-feedback limit above the accepted 1.215 s baseline |
| generated evidence | 1.500 s | local freshness-feedback limit above the accepted 1.071 s baseline |
| complete checkpoint | 150.000 s | local wave-checkpoint limit above the accepted 128.647 s baseline |

Milestone 9 must take seven post-warm-up serial samples for each fast workload
and three serial complete-workload samples. It will preserve a limit only when
the current median, range, workflow impact, and variability justify it. If a
current claim cannot be established, the result is `unavailable`; the recovery
must not fit implementation to an unexplained number.

## Admission Result

The follow-up is admitted as Milestones 6 through 9. Milestone 7 is next. Its
first design gate must prove that routing closure and migration candidates can
be derived from existing canonical authorities without lexical inference,
copied graph edges, or a second hand-maintained candidate list.
