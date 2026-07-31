# Standards Library

Reusable engineering standards with routed workflows, profiles, topics, and
reference material.

## Quick Start

1. Read [Core Standards](CORE-STANDARDS.md).
2. Use the [Standards Router](STANDARDS-ROUTER.md) to select only applicable
   workflows, profiles, and topics.
3. Record project-specific contracts and exceptions in the adopting
   repository.
4. Copy a template or tool only when routed guidance requires it.
5. Reference the adopted standards version in the project's main README.

## Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [CORE-STANDARDS.md](CORE-STANDARDS.md) | Universal ownership, boundary, failure, lifecycle, quality, and verification invariants | Every adopted project |
| [STANDARDS-ROUTER.md](STANDARDS-ROUTER.md) | Applicability, exclusions, dependency routing, and migration authority | Start of every task |
| [workflows/implementation.md](workflows/implementation.md) | Bounded implementation slices and commit boundary | Any repository change |
| [workflows/commit.md](workflows/commit.md) | Atomic commits, branch review, and explicit history-rewrite authority | Commit creation or history maintenance |
| [workflows/planning.md](workflows/planning.md) | Active plans, lifecycle, re-planning, and delegated ownership | Multi-step or high-risk work |
| [workflows/verification.md](workflows/verification.md) | Objective-aligned evidence selection | Any acceptance claim |
| [workflows/documentation.md](workflows/documentation.md) | Proportional durable documentation and traceability profiles | Responsibility, decision, contract, or operational-boundary changes |
| [workflows/release.md](workflows/release.md) | Release applicability, versioning, changelog, contract, and acceptance boundaries | Shipping artifacts or changing published promises |
| [reference/recipes/commits.md](reference/recipes/commits.md) | Non-normative staging and conventional commit examples | Formatting a commit after the workflow has selected process rules |
| [reference/recipes/documentation.md](reference/recipes/documentation.md) | Non-normative comment, Markdown, public-interface, and algorithm examples | Applying a selected documentation requirement |
| [reference/recipes/releases.md](reference/recipes/releases.md) | Non-normative changelog automation example | Configuring a selected release tool |
| [topics/contracts.md](topics/contracts.md) | Runtime decoding proof, contract classes, migration, compatibility, degraded outcomes, and typed diagnostics | Boundary decoding, contract evolution, persisted state, or fallback decisions |
| [topics/concurrency.md](topics/concurrency.md) | Shared-state coordination, lock boundaries, nonblocking async lifecycle, failure observation, and cancellation ownership | Concurrent state or asynchronous work with lifecycle obligations |
| [topics/security.md](topics/security.md) | Canonical untrusted-input authority and filesystem-containment policy | Untrusted values authorizing operations or resource access |
| [topics/cross-platform.md](topics/cross-platform.md) | Canonical path construction and filesystem-identity policy | Path behavior across supported platforms or filesystems |
| [profiles/boundaries/interop.md](profiles/boundaries/interop.md) | Foreign memory, resource authority, lifecycle, thread, and validated-adapter contracts | Foreign pointers, handles, callbacks, runtimes, or resources |
| [profiles/boundaries/ipc.md](profiles/boundaries/ipc.md) | Action-specific message decoding and validated-variant dispatch | Structured data crossing process, message, worker, plugin-host, or independently deployed component boundaries |
| [profiles/boundaries/language-bindings.md](profiles/boundaries/language-bindings.md) | Binding mechanisms, representation categories, thin adapters, conversion outcomes, and generated wrappers | Host-language APIs, generated bindings, stable ABIs, serialized values, or opaque handles |
| [profiles/applications/library.md](profiles/applications/library.md) | Reusable library ownership and consumer conditions | Library/package changes |
| [profiles/applications/launcher.md](profiles/applications/launcher.md) | Launcher command projection, procedure delegation, process lifecycle, and outcome preservation | Repository launcher or launcher-visible action changes |
| [profiles/frameworks/godot.md](profiles/frameworks/godot.md) | Godot engine affinity, dispatch ownership, and point-of-use object lifetime | Godot thread, deferred-dispatch, or object-lifetime mechanisms |
| [profiles/languages/csharp/async.md](profiles/languages/csharp/async.md) | C# continuation scheduling, affinity, invocation isolation, and typed outcomes | C# async continuation or affinity mechanisms |
| [profiles/languages/typescript/async.md](profiles/languages/typescript/async.md) | TypeScript current-invocation authority, terminal classification, cancellation, and state application | Overlapping TypeScript async operations or stale results |
| [profiles/languages/rust/README.md](profiles/languages/rust/README.md) | Rust mechanisms and focused verification | Rust-owned changes |
| [profiles/languages/rust/async.md](profiles/languages/rust/async.md) | Rust async applicability and contract-driven sync/async boundary selection | Rust async APIs, suspension boundaries, concurrent I/O, streams, backpressure, cancellation, or async resource lifetimes |
| [profiles/languages/rust/cross-platform.md](profiles/languages/rust/cross-platform.md) | Rust target contracts, configuration placement, and claim-matched evidence | Rust target contracts, triples, support claims, target-dependent mechanisms/artifacts, or target evidence |
| [profiles/languages/rust/interop.md](profiles/languages/rust/interop.md) | Checked dimensions, raw-slice preconditions, callback lifetimes, and copy-after-proof | Rust access to foreign memory or borrowed callback data |
| [profiles/languages/rust/language-bindings.md](profiles/languages/rust/language-bindings.md) | Rust binding representations, fallible conversion, and native/host evidence | Rust APIs exposed through another language |
| [CODING-STANDARDS.md](CODING-STANDARDS.md) | Code organization, simplicity/complection guidance, layering, service independence, runtime wiring guidance | Setting up any new codebase |
| [TESTING-STANDARDS.md](TESTING-STANDARDS.md) | Test placement strategy, naming, coverage, vertical slices, and cross-layer verification guidance | Writing maintainable tests |
| [COMMIT-STANDARDS.md](COMMIT-STANDARDS.md) | Migration index, conventional commit syntax, and message examples | Existing links and commit-message reference |
| [ARCHITECTURE-PATTERNS.md](ARCHITECTURE-PATTERNS.md) | System design patterns, monorepo package roles, executable contracts, composition roots, and resilient workflow coordination | Multi-layer, client-server, monorepo, or service-oriented apps |
| [TOOLING-STANDARDS.md](TOOLING-STANDARDS.md) | Linting, hooks, automation | Enforcing code quality |
| [FRONTEND-STANDARDS.md](FRONTEND-STANDARDS.md) | Declarative rendering, UI synchronization, frontend testing/tooling conventions | Web, desktop UI, and component-heavy frontend codebases |
| [DOCUMENTATION-STANDARDS.md](DOCUMENTATION-STANDARDS.md) | Migration index for canonical documentation, release, and recipe owners | Existing links only |
| [SECURITY-STANDARDS.md](SECURITY-STANDARDS.md) | Remaining string sanitization and network transport guidance | Security concerns not yet migrated to canonical topics and profiles |
| [CONCURRENCY-STANDARDS.md](CONCURRENCY-STANDARDS.md) | Migration index plus remaining language-specific concurrency material | Existing links and unmoved language-specific concerns |
| [CROSS-PLATFORM-STANDARDS.md](CROSS-PLATFORM-STANDARDS.md) | Remaining platform abstraction, native library, and CI guidance | Cross-platform concerns not yet migrated to topics |
| [INTEROP-STANDARDS.md](INTEROP-STANDARDS.md) | Migration index plus remaining event, cross-language contract, and serialization guidance | Existing links and unmoved interop concerns |
| [LANGUAGE-BINDINGS-STANDARDS.md](LANGUAGE-BINDINGS-STANDARDS.md) | Migration index for canonical Language Binding boundary guidance | Existing links only |
| [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) | Dependency evaluation, versioning, auditing, and minimization | Adding or reviewing third-party packages |
| [PLAN-STANDARDS.md](PLAN-STANDARDS.md) | Migration index for planning guidance | Existing links only |
| [LAUNCHER-STANDARDS.md](LAUNCHER-STANDARDS.md) | `launcher.sh` contract, lifecycle flags, dependency checks, and app startup | Standardizing app entry points and setup workflows |
| [LANGUAGE-BINDINGS-STANDARDS.md](LANGUAGE-BINDINGS-STANDARDS.md) | Binding architecture, FFI wrapper design, code generation, type mapping | Exposing a core library to multiple target languages |
| [RELEASE-STANDARDS.md](RELEASE-STANDARDS.md) | Migration index for canonical release workflow and recipe reference | Existing links only |
| [ACCESSIBILITY-STANDARDS.md](ACCESSIBILITY-STANDARDS.md) | Semantic HTML, keyboard interaction, ARIA, a11y linting | UI components in web or desktop apps |
| [languages/README.md](languages/README.md) | Language-specific extensions to the generic standards | Rust and future language-specific rules |

## Templates

Ready-to-use configuration files in `/templates/`:

| Template | Purpose |
|----------|---------|
| [README-TEMPLATE.md](templates/README-TEMPLATE.md) | Concise boundary and contract README profiles |
| [PLAN-TEMPLATE.md](templates/PLAN-TEMPLATE.md) | Implementation plan template |
| [PULL_REQUEST_TEMPLATE.md](templates/PULL_REQUEST_TEMPLATE.md) | PR checklist for decision traceability |
| [check-decision-traceability.sh](templates/check-decision-traceability.sh) | CI/hook script to enforce README/ADR decision updates |
| [decision-traceability-map.tsv](templates/decision-traceability-map.tsv) | Project-owned decision-bearing path and artifact map |
| [lefthook.yml](templates/lefthook.yml) | Pre-commit hook configuration |
| [.editorconfig](templates/.editorconfig) | Editor formatting settings |

## Customization

These standards are intentionally generic. When adopting them:

1. **Replace placeholders** - Look for `[YOUR-...]` markers
2. **Add tech-specific rules** - Extend with language-specific conventions
3. **Define your scopes** - Map commit scopes to your project structure
4. **Configure tooling** - Adapt hook commands to your build tools

## License

These standards are provided as-is for free use in any project.
