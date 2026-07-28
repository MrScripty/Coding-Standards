# Baseline Findings Register

All findings are open at baseline. Milestone 0 records them but does not change
normative standards. A later milestone may close a finding only with source
changes and focused fixture evidence.

## Resolution Status

| Finding | Status | Evidence |
| --- | --- | --- |
| F001 | Resolved in Milestone 3 | Prompts are versioned, thin, path-neutral workflow entrypoints. |
| F004 | Resolved in Milestone 3 | Canonical planning lifecycle and structural fixtures. |
| F005 | Resolved in Milestone 3 | Planning and implementation prompts have separate intent and canonical workflow links. |
| F006 | Resolved in Milestone 4 | Verification owns typed acceptance claims; Testing, Tooling, Launcher, and Release link to that authority without redefining evidence. |
| F007 | Resolved in Milestone 6.1 | Documentation profiles are selected by durable decision, contract, responsibility, or operational impact; source-directory changes alone require no artifact. |
| F008 | Resolved in Milestone 6.3 | Staged review remains per commit; full-history review occurs at branch boundaries, and rewriting requires explicit authority, unshared commits, recoverability, and topology-aware verification. |
| F009 | Resolved in Milestone 6.2 | Checker invocations explicitly select index-only staged mode or an exact base/head commit range; unresolved inputs fail instead of selecting another diff. |
| F010 | Resolved in Milestone 6.2 | Project maps bind decision-bearing paths to one boundary/profile/artifact, and mapped ADRs must identify the exact boundary ID. |
| F012 | Resolved in Milestone 4 | Universal test durations, percentages, and CI-only categories were replaced by project/risk-based selection. |
| F013 | Resolved in Milestone 5 | Contract evolution is fact-driven; universal append-only and coexistence rules were removed. |
| F014 | Resolved in Milestone 5 | Degraded outcomes require authority and semantic fidelity; default/cache/partial fallback examples were removed. |
| F015 | Partially resolved in Milestone 7.1 | Commit process now has one workflow owner, examples have a reference owner, and the legacy file is an index; other mixed-role documents remain. |
| F020 | Partially resolved in Milestone 5.2 | Authoritative-store deletion fallback was removed; phased-mutation atomicity remains Milestone 7. |
| F024 | Resolved in Milestone 5.2 | Rust binding compatibility is classified independently for generated, package, ABI, wire, and persisted boundaries. |
| F026 | Partially resolved in Milestone 5.2 | Catch-all executor fallback was replaced by typed unsupported delegation; spawn and TOCTOU findings remain Milestone 7. |
| F027 | Resolved in Milestone 7.3a | Major version zero and prerelease identifiers are distinct, and retained publication guidance now consumes that decision. |
| F028 | Resolved in Milestone 7.3a | SBOM, checksum, signature, and provenance applicability follow artifact content, consumer, risk, channel, and regulatory facts. |
| F029 | Resolved in Milestone 7.3a | Release units may version independently or in lockstep, lockfiles follow dependency-resolution ownership, and publication pushes only the intended tag. |
| F031 | Resolved in Milestone 4.1 | Acceptance claim fixtures independently model proof kind, environment qualification, and execution mode. |
| D005 | Resolved in Milestone 7.1 | Commit and slice process is owned by implementation/commit workflows; prompts route only, and commit examples are non-normative reference. |
| F032 | Resolved in Milestone 7.2c2 | Documentation examples, proportional workflow policy, and release-owned changelog semantics have canonical owners; the legacy documentation file is now a bounded migration index. |
| F033 | Resolved in Milestone 7.2a | The commit disposition checker now filters its shared ledger by source; documentation rows have a separate owner-specific fixture. |
| F034 | Partially resolved in Milestone 7.3a | The canonical release workflow owns foundation, changelog, artifact, and reproducibility policy; remaining pipeline, rollback, and reference concerns continue in owner-bounded slices. |
| F035 | Resolved in Milestone 7.2c1 | Contract and verification ownership checks now follow the canonical release workflow instead of requiring duplicate direct links from the legacy release index. |
| F036 | Resolved in Milestone 7.3a | Retained pipeline and publication sections consume canonical artifact and prerelease decisions instead of restoring conflicting defaults. |
| F037 | Direction approved for Milestone 7.3b | Frozen release identifiers `STD-0552` through `STD-0576` will migrate in four owner-bounded slices for pipeline, maintenance/channels, publication, and routing/checklist concerns. |

## Systemic Findings

| ID | Class | Evidence | Required disposition | Milestone |
| --- | --- | --- | --- | --- |
| F001 | Distribution gap | `.gitignore:1`; ignored `prompts/*.md` | Decide whether prompts are versioned thin entrypoints or explicitly local; never treat ignored files as repository authority. | 1, 3 |
| F002 | Routing | `README.md:5-12` | Replace full-library reading with deterministic routing and exclusions. | 2 |
| F003 | Precedence | `languages/README.md:3`; `languages/rust/RUST-STANDARDS.md:26-43` | Define generic ownership, profile specialization, and explicit override semantics. | 1, 2 |
| F004 | Plan lifecycle | `PLAN-STANDARDS.md:148-179,256-273`; `templates/PLAN-TEMPLATE.md:86,100` | Separate active state/history, add lifecycle states, supersession, and acceptance closure. | 3 |
| F005 | Prompt conflict | `prompts/planning.md:1-14`; `prompts/implement-plan.md:37-48` | Separate planning from implementation and make prompts reference canonical workflows. | 3 |
| F006 | Acceptance ownership | `TESTING-STANDARDS.md:141-165`; `PLAN-STANDARDS.md:148-179` | Give verification levels one owner and bind plan acceptance to named evidence. | 3, 4 |
| F007 | Disproportionate documentation | `DOCUMENTATION-STANDARDS.md:9-13,184-209` | Require durable docs at meaningful decision/contract boundaries, not every source directory/change. | 6 |
| F008 | History authority | `COMMIT-STANDARDS.md:210-242`; `PLAN-STANDARDS.md:243-252` | Keep atomic staged review; require explicit authority for history/worktree rewriting. | 6 |
| F009 | Traceability defect | `templates/check-decision-traceability.sh:103-119`; `TOOLING-STANDARDS.md:731-745` | Make configured staged/PR modes inspect the changes they claim to enforce. | 6 |
| F010 | Traceability ownership | `templates/check-decision-traceability.sh:130-136,209-218` | Link a changed ADR to affected decisions; any global ADR must not satisfy every directory. | 6 |
| F011 | Broad launcher profile | `LAUNCHER-STANDARDS.md:3-18,163-172` | Make launcher guidance conditional on applications that need a common launcher. | 6, 7 |
| F012 | Broad test metrics | `TESTING-STANDARDS.md:88-95,374-398,658-675` | Move duration/coverage/tool assumptions to project profiles; preserve risk-based verification. | 4 |
| F013 | Contract overgeneralization | `ARCHITECTURE-PATTERNS.md:202-220`; `CODING-STANDARDS.md:454-460` | Select evolution policy from authority, persistence, consumers, and deployment. | 5 |
| F014 | Degraded-mode overgeneralization | `ARCHITECTURE-PATTERNS.md:1093-1151` | Permit degradation only with authoritative, semantically valid data; otherwise return typed diagnostics. | 5 |
| F015 | Mixed roles | `ARCHITECTURE-PATTERNS.md`; `TOOLING-STANDARDS.md`; `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md` | Separate policy, profiles, pattern catalog, recipes, and product-local examples. | 7 |
| F016 | Broken reference | `SECURITY-STANDARDS.md:289`; no matching concurrency heading | Repair or remove the nonexistent graceful-shutdown anchor. | 7 |
| F032 | Consolidation ownership | `DOCUMENTATION-STANDARDS.md`; frozen IDs `STD-0349`-`STD-0448` | Move examples, documentation policy, and changelog guidance in separate reference, workflow, and release-owner slices. | 7 |
| F033 | Fixture ownership | `verify-consolidation-dispositions.sh`; shared disposition ledger | Filter each owner-specific fixture by source and verify new source groups independently. | 7 |
| F034 | Missing canonical owner | `owner-map.tsv`; `RELEASE-STANDARDS.md`; absent `workflows/release.md` | Establish release workflow ownership in an owner-bounded slice before moving changelog policy or closing the documentation index. | 7 |
| F035 | Fixture ownership | Release checks in `verify-contract-ownership.sh` and `verify-verification-ownership.sh` | Validate the canonical release dependency chain and only require the legacy file to route to that owner. | 7 |
| F036 | Dependent legacy override | Retained release pipeline and publication sections after partial migration | Make dependent legacy sections consume canonical decisions and verify that they cannot restore removed defaults. | 7 |
| F037 | Slice ownership | `RELEASE-STANDARDS.md`; frozen IDs `STD-0552`-`STD-0576` | Decompose pipeline mechanics, maintenance/channels, publication presentation, and language/checklist routing before implementation. | 7 |
| F031 | Acceptance dimensions | `workflows/planning.md:91-98`; `evaluation/standards-effectiveness/check-plan-structure.sh:4-14` | Model evidence kind, required environment, and execution mode independently; require all named claims rather than comparing one scalar rank. | 4 |

## Correctness And Safety Findings

| ID | Severity | Evidence | Required disposition | Milestone |
| --- | --- | --- | --- | --- |
| F017 | Critical | `SECURITY-STANDARDS.md:21-45`; `CROSS-PLATFORM-STANDARDS.md:163-174` | Replace string-prefix path checks with canonical, boundary-aware, symlink-aware containment. | 7 |
| F018 | Critical | `ARCHITECTURE-PATTERNS.md:280,451`; `SECURITY-STANDARDS.md:185` | Validate action-specific payloads before producing validated types; do not cast `unknown` as proof. | 7 |
| F019 | High | `CONCURRENCY-STANDARDS.md:23,35-67,121` | Avoid callbacks under locks, distinguish immutable/thread-safe data, and clarify blocking rules. | 7 |
| F020 | High | `ARCHITECTURE-PATTERNS.md:965-1006,1093` | Do not call phased mutation atomic without rollback/transaction; delete corrupt stores only when explicitly disposable. | 5, 7 |
| F021 | High | `languages/rust/RUST-API-STANDARDS.md:206-209`; `RUST-TOOLING-STANDARDS.md:15`; `RUST-RELEASE-STANDARDS.md:119` | Require `--all-features` only when features compose; otherwise test supported matrices. | 7 |
| F022 | Critical | `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:223-227,564` | Use checked conversions and distinguish framework-liftable types from C-ABI-safe types. | 5, 7 |
| F023 | Critical | `languages/rust/RUST-INTEROP-STANDARDS.md:8-28`; `RUST-UNSAFE-STANDARDS.md:44` | State allocation, initialization, provenance, lifetime, and size preconditions; require `SAFETY:` and caller `# Safety` contracts. | 7 |
| F024 | High | `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:106,810-814` | Define compatibility per framework, host language, ABI, and persisted artifact. | 5, 7 |
| F025 | High | `languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:31,525,635,719`; `RUST-ASYNC-STANDARDS.md:43` | Keep core independent of binding frameworks and give runtime ownership to composition/lifecycle policy. | 7 |
| F026 | High | `languages/rust/RUST-SECURITY-STANDARDS.md:9,96`; `RUST-ASYNC-STANDARDS.md:46`; `RUST-LANGUAGE-BINDINGS-STANDARDS.md:444` | Track spawned work, avoid TOCTOU examples, and never reinterpret every error as unsupported fallback. | 5, 7 |
| F027 | High | `RELEASE-STANDARDS.md:18-30,466-470` | Distinguish SemVer `0.x` instability from prerelease identifiers. | 5, 7 |
| F028 | High | `RELEASE-STANDARDS.md:162-163,216-231,368-374` | Make SBOM applicability consistent and artifact/risk-based. | 7 |
| F029 | High | `RELEASE-STANDARDS.md:68-74,252-263,527-530` | Separate package-version/lockfile models and push only the intended release tag. | 7 |
| F030 | High | `TOOLING-STANDARDS.md:155-160,321-328,388-395` | Reconcile fail-on-warning policy with explicitly owned temporary debt. | 6, 7 |

## Duplicate Ownership Clusters

These ten reviewed clusters form the semantic duplication baseline. The initial
30% reduction target means eliminating at least three clusters; the final
single-owner requirement should eliminate all competing normative ownership.

| ID | Competing locations | Intended owner |
| --- | --- | --- |
| D001 | Layering in `CODING-STANDARDS.md:59` and `ARCHITECTURE-PATTERNS.md:32-98` | Core dependency-direction rule; architecture catalog for patterns. |
| D002 | Backend/state policy in `CODING-STANDARDS.md:95` and `ARCHITECTURE-PATTERNS.md:125-163` | Core authority rule; frontend profile for projection/reconciliation. |
| D003 | Validation in Coding, Architecture, Security, and Interop | Security owns trust boundaries; Interop specializes foreign/wire boundaries. |
| D004 | README schema in Documentation, Coding, Architecture, template, and checker | Documentation workflow plus one canonical template. |
| D005 | Slice/commit procedure in Plan, Commit, and ignored prompts | Planning/implementation workflow; prompts route only. |
| D006 | Verification levels in Testing, Tooling, Launcher, and Release | Verification workflow; profiles select applicable mechanisms. |
| D007 | Rust baseline commands in API, Tooling, and Release | Rust tooling profile. |
| D008 | Rust unsafe policy in API, Interop, Bindings, and Unsafe | Rust unsafe topic/profile. |
| D009 | Generic dependency/security/cross-platform rules repeated in Rust files | Generic topic owner; Rust profile only for Cargo/Rust mechanisms. |
| D010 | Binding architecture, framework recipes, packaging, and compatibility in one Rust file | Boundary profile, framework reference, and project-local policy separated. |

## Semantics That Must Survive Consolidation

- Authoritative state and policy ownership with explicit projections.
- Dependency direction without mandating one universal layer count.
- Executable boundary contracts and validation once per trust boundary.
- Exact wire formats and checked conversions.
- Explicit foreign-resource ownership, lifetime, threading, and error contracts.
- Cancellation-aware, nonblocking task ownership and shutdown.
- Canonical filesystem containment.
- Bounded, non-sensitive diagnostics and typed unavailable/invalid outcomes.
- Accessible native interaction semantics.
- Reproducible dependency ownership and declared target/toolchain support.
- Full-path acceptance for cross-layer objectives.
- Atomic commits, staged-diff review, and no rewrite of shared history.

## Milestone 0 Disposition

All findings are deferred to their named milestones because Milestone 0 cannot
change normative standards. Critical findings must be addressed before the
affected source can become canonical in Milestone 7.
