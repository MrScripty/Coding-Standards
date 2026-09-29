# Attribute case-policy repair verification

**Status: locally verified; exact-candidate locked CI and independent review/owner
acceptance remain pending.** This is residual F4-C1 within the existing packaging
plan, not a new implementation sequence.

## Baseline, owner and change

The connected repository reports main at
`143c8de1706ccf4b82b5c78aeed644c071ed999a`, tree
`bb2876f0251243b1d7d38b7ee1026c080394a08e`. Its mounted Actions source artifact
`11003765805` was verified against archive SHA-256
`509e9b6b38904ae388c121326acf4e2040d4e88b91fe50730f55518584f5b6ba` and checked out
on a task-owned repair branch. The user authorized this remaining repair from the
follow-up source review. No later or unrelated user working-tree content was used.

Production change is confined to `GitRepository.revision_patch`: add the command-
local setting `core.ignoreCase=false` and document its meaning. The existing Git
owner now matches candidate-committed attribute patterns case-sensitively over
exact Git paths. Neither the repository's filesystem-compatibility setting nor
ordinary reads, worktree operations, capture or publication defaults are changed.

The complete patch still supports binary data, exact modes and committed attribute
choices. Case-sensitive matching does not mean disabling attributes: `*.TXT -diff`
continues to select a binary patch for `MATCH.TXT`, but not for `data.txt`.
Existing local-only execution, custom-driver rejection, info-attribute admission,
output bounds and command lifetime remain intact. The prior directory-handle,
common-Git-root and portable-component repairs were not modified.

No Engine interface, packet format, public signature, schema, metadata key, CLI
flag, migration or additional abstraction is introduced. Engine interface 45 and
packet format 1 remain unchanged. There is no source/evidence/provider network
operation added to the builder.

## Deciding evidence

Two regression methods were added at the existing owners:

- `test_exact_patch.ExactPatchTests.test_attribute_case_policy_is_fixed_without_reconfiguring_repository`
  invokes the original public Git adapter using real commits under repository
  settings false and true. It compares the lowercase path's hunk to a literal
  expectation built from independently observed blob IDs and exact file bytes,
  and requires the exact-case file's binary patch marker. It checks unchanged
  source, Git index, refs, HEAD and configuration after each operation.
- `test_repair_boundaries.ReviewRepairTests.test_cli_packet_case_policy_preserves_material_and_repository_configuration`
  invokes the actual CLI in replacement processes with the same request and
  selected commits under both settings. It checks successful outcomes, exact
  baseline/candidate source members, literal text and positive binary-policy
  oracles, identical complete ZIP and manifest bytes, no leftover staging files,
  and unchanged request/source/index/refs/configuration.

Both final regression definitions first failed on the unmodified production code
at the intended text-versus-binary assertion (two failures, no errors), then passed
with the one-setting correction. An earlier test draft also emitted secondary list-
index errors after a failed subtest; the draft was corrected before the final
baseline rerun. Both original logs remain in the delivery evidence and are not
counted as successful verification. The existing command-environment test also
asserts that the case policy is passed only on the owned patch invocation.

An initial task-routing probe supplied an undeclared `console` profile and was
correctly rejected; it was corrected to the registered `library` profile before
implementation. The executed Router then selected 21 standards with no unanswered
facts. This was task setup, not a production failure or acceptance test.

## Executed checks

| Selection | Observed result |
| --- | --- |
| Complete review-evidence package | 49 passed |
| Complete Repository Git package | 40 passed; one permission-dependent skip (41 run) |
| Complete metadata package | 43 passed |
| Engine capture-handoff, replacement-stdio and generated-contract selections | 29 passed |
| Total selected executions | 161 passed, one skipped, no failures (162 run) |
| New regression methods | Two; included in the totals above |
| Complete structural checkpoint | 73 suites / 121 checks passed |
| Generated projection freshness | Passed |
| Separate offline recipient comparison | All members byte-identical to the previously inspected example |

The full Engine and other supporting-package suites were not rerun. The production
change is an opt-in patch setting with one builder consumer; the complete affected
Git/builder packages and existing shared capture/contract cases are the selected
regression scope. New tests are not added to totals a second time when rerun.
After final documentation and manifest regeneration, the new regressions, command-
environment check, freshness and structural checks are repeated; exact final
outcomes are preserved in `DELIVERY/evidence/final-checks.json`.

## Actual review packet

The committed routing example was rebuilt through the CLI. A separate standard-
library-only recipient process inspected the ZIP without importing the builder,
reading the source checkout or extracting files. It checked all inventory member
names, regular inert modes, lengths, hashes and index targets, and compared every
member byte with the prior inspected packet.

The result has 98 members, 96 resolving index links, 49 primary changed paths,
54 selected paths, 5,704,505 payload bytes and the complete 1,083,975-byte primary
patch. Its manifest is unchanged:
`sha256:30c2834feb20fa7c3d4efa16b12dae823a4341de4b41aff40fe6a672fef11ff3`.
The CLI returns `built-with-gaps` and exit 1 as intended: raw CI log missing, CI URL
referenced. Those gaps were not filled with fabricated results. This compares a
real packet; it does not reopen routing-fact acceptance or assert CI execution.

The unchanged packet manifest's implementation digest remains explicitly a digest
of `packet.py`, not of its Git dependency or the whole builder. No stronger origin
or implementation-authentication claim is made by this comparison.

## Scope, limitations and integration

Only `repository.py` changes production code. The two direct test files, two
READMEs, plan/ledger/issues, this report and generated suite-input manifest form
the coordinated delivery. All Engine contracts/runtime, packet schema/source,
existing normative guidance, dependency locks and CI configuration remain unchanged.
Fresh-baseline reconstruction checks the entire resulting tracked tree, individual
file hashes and modes; ZIP integrity and reconstruction results are in DELIVERY.

Handoff execution used Linux x86-64, CPython 3.13.5, Git 2.47.3, jsonschema 4.26.0
and rpds-py 2026.5.1. No supported Python 3.12 hash-locked environment was installed there.
The skipped case requires unprivileged POSIX permissions; no case-insensitive
filesystem or additional operating system was exercised. The fixed policy concerns
committed-path interpretation, not reconfiguration of filesystem compatibility.
The tests establish these configured cases, not harmlessness of every Git setting.
The existing requirement that configuration remain stable during observation and
the documented local-directory threat limits are unchanged.

Apply the scoped patch after its read-only baseline check, preserving unrelated
work. No registration or repository Git configuration changes are needed. Fresh
builder invocations load the corrected code. Keep historical packets and reports
unchanged. The plan remains Verifying: obtain supported locked-runtime CI for the
actual integrated candidate, narrow independent repair review and acceptance-owner
disposition. No remote push, production commit, standards publication, host update,
provider request or independent external review was performed during handoff preparation.

After integration on the named base, the repository's Python 3.12.3 environment
passed 49 Review Evidence tests, 41 Repository Git tests, 43 Standards Metadata
tests and the 29 selected Engine tests. Ruff lint on changed Python, the complete
structural check and authoring-purpose repository verification (121 checks across
73 suites) also passed. A separate ZIP inspection found 98 members, 96 resolving
links, the complete 1,083,975-byte patch, and the same two declared evidence gaps;
the manifest digest remained `sha256:30c2834feb20fa7c3d4efa16b12dae823a4341de4b41aff40fe6a672fef11ff3`.
These local results do not replace hosted CI or acceptance-owner disposition.

## Corroborating dependency contract

Git documents command-local configuration precedence and identifies `core.ignoreCase`
as a filesystem-compatibility setting. The operation-local override intentionally
does not edit that stored value. Official reference:
https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreignoreCase
