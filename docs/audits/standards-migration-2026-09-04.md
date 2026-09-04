# Standards structure and guidance migration

Implemented the repository changes from the [audit](standards-structure-and-guidance-2026-09-04.md).
The user explicitly authorized direct repository edits and verification after
the Engine could not bootstrap changed verification inputs or express routing
edits. This migration does not modify Engine database records or claim that the
historical proposal was applied through the Engine.

## Structure and navigation

The Router now introduces design, development, and operation concerns before
application, boundary, and language mechanisms. Ten conditional pages hold code
design, immutable replay, schema generation, protocol adaptation, contract
evolution, advanced test oracles, GUI verification, platform verification, Rust
binding lifecycle, and release operations. Parent pages retain links at former
headings. Registered policy IDs and their relationships move with their owners;
pure relocation does not change policy meaning. Topics and workflows use
conditional links for refinement; the existing `Specializes` relation remains
reserved for profiles.

Contracts now starts with invariants and boundary decoding. Core explains
requirement strength, precedence, exceptions, and ordinary development judgment.
Detailed code-design guidance has its own conditional owner. The Router's new
`routing.details` fact allows explicit detail selection; unknown detail facts
remain unresolved rather than silently becoming empty.

Four Rust routes were added: Unsafe, Security, Interop, and Language Bindings.
Rust plus a relevant generic boundary selects the corresponding specialization;
unsafe operations also have an explicit language fact. All normative modules
have an executable route. Negative cases ensure ordinary Rust work and non-Rust
boundaries do not acquire unrelated Rust safety profiles.

Dependencies no longer requires Release; Tooling no longer requires Commit.
TypeScript and Frontend select Contracts when an actual contract concern is
affected. Rust API no longer assumes every API change is a library, dependency,
architecture, and resilience change. Conditional links retain access to those
owners. Generated contracts, persistence, and IPC require their relevant
specialized contract details.

## Guidance changes

- Ordinary regressions have a direct path; substantial evidence machinery keeps
  its cost and overlap review. Existing tests or construction guarantees may
  suffice when they prove the actual claim. Acceptance-claim semantic revision
  advances from 2 to 3.
- Missing development facts use plain-language explanation; application errors
  follow the application's own contract. Routine reversible choices can use
  suitable existing conventions without a separate approval record.
- New owned TypeScript code has a conditional `strict` default, with migration
  and compiler-upgrade qualifications. Tooling recommends ordinary UTF-8 source
  conventions while protecting format-specific requirements. Rust guidance and
  maintained recipes give concrete starting commands and their limits.
- Security distinguishes valid data, authenticated identity, and resource/action
  permission. It covers credential validation, tenant boundaries, disclosure,
  redaction, secret rotation, secure transport, cryptographic mechanisms, and
  executable dependency/build trust.
- Immutable replay binds historical result inputs; current permission can deny
  access without changing the historical result. Live inspection does not
  imply replay. This policy's semantic revision advances from 2 to 3.
- Resilience adds end-to-end deadlines, retry ownership, jitter, unknown commit
  outcomes, scoped idempotency records, and time semantics. Persistence explains
  lost-update prevention and whole-transaction retry.
- Repeated benchmark guidance was consolidated. Maintained recipes are clearly
  separated from retained historical examples. Rust Security now links to its
  current Rust API error owner.

## Independent task review

These are repository-level design reviews, not downstream agent trials.
Expected decisions were chosen from the task before checking the route or prose.

| Task | Required decision and observed guidance |
| --- | --- |
| Small internal Rust parser defect | Six broad modules; observable regression plus affected checks; no release or advanced oracle machinery. |
| TypeScript UI label | Frontend, TypeScript, accessibility, implementation, and verification; no unrelated contract-evolution reading. |
| Unsafe Rust FFI | Generic crossing plus Rust interop and unsafe preconditions; binding and security mechanisms when those conditions apply. |
| Read another user's resource by changing its valid ID | Input validation and authentication do not grant permission; check action/resource ownership and deny unauthorized disclosure. |
| View an immutable report after access is revoked | Reproduce the same historical content only if current access permits disclosure; a historical grant is not continuing access. |
| Retry a worker mutation after losing its response | A timeout is not proof that the effect failed; reconcile or use a scoped idempotency contract within the end-to-end budget. |
| Introduce a local module with no existing design record | Use a coherent owner and a suitable reversible convention; record material decisions proportionally rather than blocking on a missing serialized contract. |

Executable tests cover positive/exclusion routes, all-module reachability,
unknown details, activity dependencies, and canonical link targets and headings.
Existing text/section assertions were transferred to their content owners.
Routing fixture membership was reviewed by removing the unrelated activities and
adding the three applicable contract prerequisites; only its prerequisite order
was derived mechanically. Default and regression fixtures retain constrained
negative cases and add ordinary/default-positive cases.

## Reading measurements and validation

The [evidence](standards-migration-2026-09-04.evidence.json) compares the original
nine task probes with the current executable rules and records canonical file
hashes. It uses the original facts plus explicit known-empty detail facts, with
whole-page whitespace word counts. It measures navigation cost, not agent quality.

| Task probe | Before words | After words | Reduction |
| --- | ---: | ---: | ---: |
| audit | 8,875 | 7,914 | 10.8% |
| durable-worker | 21,490 | 20,814 | 3.1% |
| generated-contract | 19,014 | 13,425 | 29.4% |
| no-activities | 3,011 | 2,735 | 9.2% |
| persisted-schema | 13,806 | 11,863 | 14.1% |
| rust-ffi | 28,893 | 25,109 | 13.1% |
| rust-tooling | 13,229 | 10,573 | 20.1% |
| s1-rust-library-fix | 8,932 | 7,971 | 10.8% |
| typescript-ui-label | 16,041 | 10,587 | 34.0% |

All 271 registered verifier suites pass (1,641 checks). All 94 Standards Analysis tests and 25 Standards Metadata tests pass; the Analysis tests include 11 routing and canonical-link tests. There are 56 normative modules and zero unreachable modules.


## Remaining evaluation limits

The two downstream pilots in the existing standards-effectiveness plan remain
pending; this migration does not mark them accepted. Running those requires
actual downstream tasks and separately observed agent outcomes. Further splits
should be selected from that evidence rather than targeting a file-size quota.
Historical recipes remain available for migration evidence, and historical
Engine proposal handles remain historical; the direct migration supersedes the
unapplied proposal's intended changes.

The generic Markdown-link verifier still checks file existence. The added
canonical-corpus regression test supplies heading and retired-owner coverage
for current normative guidance without retroactively rewriting historical docs.

## Sources used for technical choices

The conditional TypeScript recommendation follows the documented strict-check
family and upgrade caveat ([TypeScript](https://www.typescriptlang.org/tsconfig/strict.html)).
Security guidance uses the identity/permission distinction and credential
lifecycle principles in [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
and [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).
Retry guidance uses the load and latency distinctions in
[AWS's retry and jitter paper](https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf).
Rust tooling syntax was checked against the
[Clippy usage documentation](https://doc.rust-lang.org/stable/clippy/usage.html).
The standards' particular defaults and applicability decisions are this
migration's recommendations, not claims of universal external mandates.
