# Planning evidence and design selection

Status: planning only. No production packet builder or checker has been implemented,
and no candidate acceptance or new external review is claimed.

## Source-backed problem

The supplied historical review status describes a separate read-only reviewer and
makes clear that its recommendations are not owner decisions or CI reruns. The
pilot report lists unavailable CI/delivery logs, replacement-process transcripts
and a baseline checkout. Other slice reports make similar distinctions. The
routing-fact review preserved at the current commit likewise notes a truncated
large generated diff and unavailable CI/delivery evidence. These are packaging
and access limitations, not new defects or reopened acceptance requirements.

Their source locators are the preserved per-slice reviews under `docs/plans/` and
the conversation's original `REVIEW_STATUS.md`/review concatenation. The latter
predates the completed boundary review; its old pending status is not current
acceptance authority. The plan uses its evidence-gap observations only.

## Verified current state

The GitHub read returned `32e78530096f2884d4c77e0a5a02a0de2ff869fe` on main.
Its source artifact from Actions run `36472002507` was downloaded and verified.
The source bundle resolves to tree `08759cc18fd2973c105743e050746996fbb67308`.
The source run was still in progress when fetched, so it is not reported as a pass.
Routing acceptance's source/CI/live/review records remain unchanged.

An isolated clone was used for source inspection and deterministic probes. No
production file, source worktree owned by the user, remote ref, provider registration
or standards store was modified. The task-local main branch exists only so the
existing Router can capture the exact accepted source during planning.

## Existing machinery and selected reuse

Repository Git already binds exact revisions, verifies object frames and hashes,
retains bounded reader sessions and distinguishes regular-file modes. This is a
suitable source owner. A separate Git parser, `git archive` extraction or worktree
copy would either duplicate that responsibility or change the source semantics.
Its current generic invocation/read APIs need inspection for a strictly local,
no-helper diff path; any necessary new capability belongs there and must leave
current Engine/capture/publication behavior unchanged.

The existing plan validator and package-contract/CI mechanisms provide structural
and integration checks. The packager must not become another plan parser or
an automated acceptance engine. Its new schema validates only the explicit packet
request and inventory, using the already installed jsonschema implementation.

## Planning probes (observed, not implementation tests)

The reproduction [probe.py](evidence/probe.py) uses the existing Repository Git
adapter to read every available primary changed/context file from both commits.
Independent Git blob identities agree with the exact bytes. It uses no candidate
packet code because that code does not yet exist.

| Observation | Result |
| --- | ---: |
| Primary changed paths | 49 |
| Additional explicit context paths | 5 |
| Distinct selected source paths | 54 |
| Existing baseline/candidate file versions read | 87 |
| Total exact source bytes | 4,526,413 |
| Largest selected blob | 599,254 bytes |
| Complete primary patch | 1,083,975 bytes |

The source/CI/records identities and changed paths were obtained from real Git.
The candidate and both supplemental revisions share the exact `tools/` subtree,
not the entire tree. The CI subject additionally changes `.gitignore`, removes
an old ZIP and updates suite inputs. The later accepted records differ in those
plus documentation. The prototype does not infer whether that CI satisfies a claim;
that decision has its separate owner.

A new disposable Git fixture contains an `export-ignore` source file and later dirty
worktree bytes plus an untracked ZIP. The existing exact-read adapter returns the
original committed bytes, leaves those changes and the index untouched, while
`git archive` omits the selected source file. This validates the decision to use
exact object reading, not archive attributes, for baseline/candidate evidence.

Files: [source identities](evidence/example-source-identities.json),
[full measurements](evidence/design-probe.json), [probe log](evidence/design-probe.log).
These are not latency, model-token, whole-repository audit or packet-code safety
measurements. Archive limits, hostile Git configuration, publication and checking
must be tested on the real implementation.

## External technical references

Official Git documentation confirms that archive export attributes may omit files
or substitute content, and that `--no-ext-diff`, `--no-textconv`, `--no-renames`, raw
NUL-separated path output and full binary diffs are explicit choices rather than
universal defaults:

- https://git-scm.com/docs/git-archive — ATTRIBUTES (`export-ignore`, `export-subst`).
- https://git-scm.com/docs/git-diff — external helpers, text conversion, raw paths,
  rename detection and binary/full-index output.

These references explain the selected safety boundary. They are not tests of this
repository's eventual new invocation path or claims that network activity is
already impossible. The implementation must prove its supported local-only path.

## Alternatives and cost admission

- **Another manual checklist:** remains sufficient for a one-off review, but repeats
  precise two-version copying, evidence-gap accounting, large-file access and safe
  publication each time. The observed repeated gaps justify a small reusable owner.
- **Reuse `git archive`:** declined for the exact-source guarantee; observed export
  omission shows a difference from source-object reading.
- **Bundle an entire Git repository or history:** declined as the default; it copies
  unrelated material and leaves a shell-disabled reviewer to reconstruct scope.
- **Automatically fetch CI and launch reviewers:** declined; network credentials,
  payload authorization and provider semantics are independent from local assembly.
- **Parse plans and assert every claim complete:** declined; material availability
  is not objective acceptance, and the existing plan/reviewer/owner boundaries hold.
- **New signature or content-addressed storage service:** declined; local SHA-256
  member/inventory checks address packet consistency, with authenticity limits made
  explicit. No new attestation infrastructure is needed.

The archive checker adds value beyond ZIP CRC by binding exact members, revision
roles and declared material to one complete inventory and detecting substituted,
extra or absent contents. It does not replace independent source/CI or review
validation. Test it with independently built/tampered fixtures rather than only
having the builder check itself. Reconsider this machinery if it cannot reduce
review preparation/reader ambiguity without developing into a review platform.
