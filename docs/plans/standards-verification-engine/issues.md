# Generic Standards Verification Engine Issues

| ID | Status | Severity | Evidence | Owner | Disposition |
| --- | --- | --- | --- | --- | --- |
| VE001 | Active | High | 274 Bash verifiers, 166 transitive invokers, 43 `sed` parsers, and repeated policy branches | This plan | Replace with strict declarative suites and one typed engine in measured waves. |
| VE002 | Active | Medium | No repository-owned verifier runtime declaration or bootstrap contract | Milestone 1 | Declare Python 3.11+ and prove version handling without installing or silently substituting another runtime. |
| VE003 | Active | High | Existing complete-suite convention discovers only `verify-*.sh` | Milestones 1 and 6 | Use one policy-free generic launcher during migration, then replace the convention with the engine command; do not retain per-suite wrappers. |
| VE004 | Active | High | Existing decision behavior is embedded in shell `if`/`elif` branches | Milestone 4 | Use bounded ordered predicates in suite data; reject arbitrary code and policy-specific engine branches. |
| VE005 | Active | Medium | Current checker graph repeats transitive checks and obscures execution counts | Milestone 5 | Register explicit acyclic dependencies and execute each selected suite once. |
| VE006 | Resolved in Milestone 1 re-plan | High | The first proposed Build checker is frozen by `milestone-7-row-35-readme-dependencies.tsv`, whose owner requires all 33 historical checker paths to exist. | Milestone 1 | Do not broaden the kernel slice or retain a wrapper. Replace unreferenced `verify-rust-test-style.sh`; migrate historical checker identities under the later shared migration-contract milestone. |
