# Review-evidence boundary repairs — verification

**Status: Verifying.** The four demonstrated source repairs are implemented;
exact-candidate supported-runtime CI and independent repair review/owner
acceptance remain outstanding. Baseline: `6be1d7a081ef43d87126bbaa7ae59335dc3c6126`,
tree `fee9f21058847ef36731390407532fa44af6d61a`.

## Scope and deciding evidence

The user authorized F1–F4 repairs from the code review, not a redesign, standalone
checker, provider integration or priority-3 test-hardening project. The source ZIP
matched SHA-256 `04e50bde604b11da9090a6731dea362dab02ba44104307e96d7aa30b7bcd0503`.
The connected current main was checked before work. Core and the executable Router
selected 25 applicable modules, all read, with no unresolved facts. A clean owned
branch contains the patch. No user checkout, remote ref or accepted prior plan was
changed.

Production work is limited to five files: packet assembly/publication, portable
names, the new packet-private `local_files.py`, additive methods in the existing
Repository Git owner, and the CLI's safe projection of the new unsupported-configuration
diagnostic. Public build/request/result meanings and limits stay as before.
Engine source, schemas, interface 45, configuration, stores and accepted history
are unchanged. The unused public ZIP checker remains intentionally absent.

## F1 — Hold directory identity through the operation

A `LocalDirectory` walks the absolute chain through no-follow directory opens and
retains its final descriptor and observed chain identities. It owns only this local
operation lifetime, not a registry or global cache. Its caller controls explicit
root selection and output-overlap policy.

Evidence reads traverse relative to the admitted root and reject a changed root,
including missing-file observations. Output creation, writing, validation, linking
and owned cleanup stay on the retained directory/file descriptors. Validation reads
the already-open staging stream, not its pathname. Requested-directory identity is
checked before staging, before publication and after linking. A detected post-link
change removes only this attempt's matching final link; a replacement tree's files
are left untouched. No-clobber linking and cleanup-warning behavior are retained.

Deterministic tests replace the parent immediately before actual file creation,
after completed ZIP validation, and inside the real hard-link invocation. Other
cases replace evidence-root ancestors, swap before a leaf open, replace a root with
a new real directory, or remove a selected evidence file while replacing its root.
The interleavings prove no redirection through replacement paths, no overwritten
competing output and cleanup through the held directory. A descriptor-count check
covers success and failed root validation.

Limits remain explicit: these guards prevent pathname substitution from redirecting
I/O. They are not a sandbox against a local actor able to move the held directory
itself into another authority, replace mounts, modify process memory or otherwise
act with the same resource authority. Logical name checks are observations, not a
filesystem-wide lock. No new power-loss guarantee is claimed.

## F2 — Protect private and common Git control roots

`GitRepository.control_directories()` obtains exact private/common administrative
paths through the public bounded read-only Git execution owner. The packet excludes
both along with its source/evidence roots. Real linked-worktree and separate-Git-dir
fixtures reject output under administrative roots without creating files, while
external output continues to work. Existing Git read and publication defaults are
unchanged; this is additive observation behavior.

## F3 — Validate the whole portable path namespace

A single iterative component trie is used during collection and staged validation.
Each normalized/case-folded component has one exact spelling and one file/directory
role. Prefix collisions in either insertion order, differing directory case and
Unicode-equivalent prefixes reject without renaming or omitting source. Exact
shared directories remain valid. Tests include real Linux Git paths `A` and
`a/child`, deliberately malformed ZIP namespaces, and a normalization call-count
check over deep paths. The trie avoids quadratic full-prefix copying. No actual
Windows or macOS extraction was performed or claimed.

## F4 — Fix the committed patch interpretation

`GitRepository.revision_patch()` is a narrow opt-in exact patch boundary using the
existing bounded subprocess mechanism. It pins candidate attributes, disables
replacement/lazy-fetch/external/textconv behavior, suppresses global/system/configured
attribute files, and fixes quoting, prefixes, ordering, context, algorithm and
other documented patch formatting. Higher-precedence info attributes, symlinked
administrative info directories and local custom diff semantics are explicitly
unsupported, not copied into the packet or removed from user configuration.

Configuration admission is checked before and after the command. It must remain
stable through the observation: the operation is not a lock against a hostile
writer that changes and restores configuration within the subprocess interval.
The implemented policy is documented rather than implying that pinned commits
alone isolate every possible mutable Git installation. Different Git versions may
produce different binary encodings; there is no cross-version byte-identity claim.

Real tests change configured attributes and many presentation settings while keeping
source/request bytes fixed. Either complete packet bytes remain identical, or the
unsupported override returns `REPOSITORY_GIT.PATCH_CONFIGURATION` without publication.
A multiline/Unicode-path case proves ordinary diff output would change under the
same preferences. Committed attributes still deliberately select binary patches.
Existing missing-promisor, replacement-ref and hostile-driver tests pass; no network
or external driver is invoked by build. User configuration bytes remain unchanged.
The CLI reports the new owner's fixed safe unsupported-configuration message rather
than hiding it behind a generic error. A real CLI regression asserts the exact
message, nonzero outcome, absent packet, and no source-path or Git-stderr disclosure.

## Verification

| Selection | Final observed result |
| --- | --- |
| Review-evidence complete package | 48 passed |
| Repository Git complete package | 39 passed, one permission-dependent skip (40 run) |
| Ten other complete supporting packages | 538 passed, one supported-environment skip (539 run) |
| Engine capture-handoff/stdio/generated-contract selection | 29 passed |
| Total distinct selected test executions | 654 passed, two skipped (656 run), zero failures |
| New repair-specific methods | 27, included in package totals |
| Separate standard-library recipient check | Passed; exact old payloads and non-implementation manifest fields preserved |

The twelve supporting packages were each run completely. The Engine selection was
not the full Engine suite. Final repair/package reruns followed the component-trie
and multiline-oracle additions, then the narrow CLI diagnostic projection; unrelated
successful package evidence was not
invented or recounted. `DELIVERY/evidence/verification-summary.json` records each
selection and exact log. Original pre-repair failures remain distinct: five initial
regression methods produced nine failed assertions against the reviewed code,
including collision subcases. The initial coherent repair passed all original 28
builder tests before the expanded final regression set.

The complete structural checkpoint, generated freshness, syntax, scoped diff,
source-preservation and fresh-base reconstruction are recorded in final delivery
evidence after these records and generated inputs are finalized. No test count
above includes repeated reruns as additional distinct coverage.

## Real recipient observation

The committed routing example is still `built-with-gaps`: the raw CI log is missing
and the CI URL only referenced. A separate stdlib-only process opened the packet
without source imports or extraction and confirmed 98 members, 96 resolving index
links, 49 changed paths, 54 selected paths and the complete 1,083,975-byte patch.
All included source, evidence, comparison and index bytes equal the prior inspected
example, as do all manifest fields except implementation metadata. The resulting
manifest digest is `sha256:30c2834feb20fa7c3d4efa16b12dae823a4341de4b41aff40fe6a672fef11ff3`.

The `implementation.source_sha256` remains explicitly a per-file `packet.py` digest,
not a whole-builder/dependency fingerprint or origin authentication. This lower-
priority review observation is clarified in the README without creating a new
fingerprint registry. Existing reports, verdicts and gap meanings are preserved.

## Environment and acceptance limits

Local verification ran on Linux, CPython 3.13.5, Git 2.47.3, jsonschema 4.26.0 and
rpds-py 2026.5.1. A bounded attempt to provision Python 3.12 failed DNS resolution;
the unchanged supported dependency lock was not replaced to obtain a pass. No handoff-side
Python 3.12/3.11 result or exact-new-source hosted CI pass is claimed. The two skips
are the existing supported-environment assertion and elevated-user permission test.

P1 is Implemented and P2 is Verifying. Local P-A2–P-A6 observations have deciding
evidence. P-A1/P-A7 retain their required locked CI gate; P-A8 requires an independent
material review of these repairs and an authorized acceptance-owner disposition.
This implementation does not mark the packaging plan Accepted. Routing-fact work
and the earlier six-slice refactor remain closed. Priority 3 remains unadmitted.

No provider requests, configuration edits, remote commits or production standards
publications were performed. The package is a local, baseline-checked source patch.
Run the unchanged CI workflow and review the repaired boundaries before acceptance.

## Integration check in the repository

After applying the patch to the named base, the repository's locked Python 3.12.3
environment passed all 48 Review Evidence tests, all 40 Repository Git tests, and
the 29 selected Engine capture-handoff/generated-contract tests. Ten other support
package suites passed. The authoring-purpose repository check passed 121 checks
across 73 suites with refreshed generated inputs, and the complete structural
check passed. Ruff lint passed on the changed Python. The separate recipient ZIP
inspection found 98 members, 96 resolving links, the complete 1,083,975-byte patch,
and the same two declared evidence gaps; its manifest digest is the one recorded
above. These are local integration results, not hosted CI or owner acceptance.
