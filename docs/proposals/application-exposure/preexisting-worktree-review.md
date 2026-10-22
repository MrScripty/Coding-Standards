# Existing checkout differences and GitHub publication

Inspected on 2026-10-04. This report does not commit or discard workspace edits.

Historical inspection: the user authorized cleanup on 2026-10-22. The
[reconciliation record](../../plans/authoring-publication-evidence/reports/checkout-reconciliation.md)
supersedes the checkout and untracked-file state below; the original publication
and review observations remain unchanged.

## The reviewed standards commit is pushable

Local main is `188beda1fa477d21d576c233dd8c7f4c4c267d23`.
A read-only GitHub ref query returned `dcc56f26e884ade260770beceba2501d3746200d`
for origin main. The outgoing range contains exactly one reviewed Engine commit
and eight files: the Rust sentence correction and its application-exposure,
policy-unit, consumer, provenance and generated metadata.

Git push sends this committed history. The dirty checkout and index do not
become part of that push. No all-files commit, stash, reset or checkout
reconciliation is needed to send the reviewed commit.

## The phrase pre-existing edits was too broad

Some differences are old checkout content following earlier canonical Engine
publications. Comparing bytes with historical commits confirmed exact matches:

| Workspace file | Older committed content it exactly matches |
| --- | --- |
| topics/concurrency.md | 8e2a59e202c9 |
| topics/security.md | 77704707c6d2 |
| workflows/implementation.md | 72963ad590ca |
| workflows/planning.md | 72963ad590ca |
| STANDARDS-ROUTER.md | 72963ad590ca |
| prompts/planning.md | 72963ad590ca |

Those copies omit already committed concurrency cessation, untrusted-execution,
and Planning discovery guidance. Their appearance as removals does not establish
an intentional new deletion. The missing untrusted-execution and discovery files
and associated registry/coverage differences also require reconciliation with
accepted history, rather than being blindly included in a new commit.

The current index additionally reflects the predecessor of the latest Engine
publication at all eight publication paths. Its apparent staged Rust reversal
and deleted Rust declarations are checkout-publication discrepancies; they are
not commits that would be pushed. Adding the whole workspace now would risk
turning old copies into regressions.

## Actual unfinished implementation and documentation

The existing tools changes include:

- Interface47 checkout reconciliation in repository_git and Standards Engine,
  with associated tests, contract-version updates and documentation.
- Optional private MCP interaction recording through --observation-db,
  a new interaction_observation module and tests.
- Output-contract delivery qualification notes and verification evidence.
- Standards-library effectiveness pilot admission and acceptance reconciliation.
- Test/CI efficiency and agent-interaction-observation plans.
- Untracked review, proposal and audit documents. Some are earlier work;
  the CodeRabbit and application-exposure evidence was created in this task.

These require their own scoped review and acceptance. They are not part of the
eight-file reviewed standards commit.

Current Git status contains75 tracked differing paths, grouped as9 standards/
prompt files,43 metadata/coverage files,17 tool files and6 plan files. These
counts include the publication discrepancies and overlapping changes; they
are not75 independent authored changes. Git also reports10 untracked file/
directory entries, with directories containing multiple files.

## Push attempt and authorization

The normal push attempt failed to resolve github.com in the restricted
execution environment. The requested network-enabled retry was rejected by
automatic approval review before execution. Its stated reason was that the
transcript did not explicitly authorize this exact commit to the configured
GitHub default branch.

Explicit approval was requested for:

`git push origin 188beda1fa477d21d576c233dd8c7f4c4c267d23:refs/heads/main`

Destination: https://github.com/MrScripty/Coding-Standards, branch main.
No force push, history rewrite or inclusion of uncommitted files is proposed.
Nothing has been pushed by this turn at the time this record is written.

### Subsequent authorized push

The user explicitly approved the exact push. It succeeded, advancing GitHub
main from dcc56f26 to188beda1. A subsequent git ls-remote query independently
confirmed refs/heads/main at188beda1fa477d21d576c233dd8c7f4c4c267d23.
Uncommitted workspace edits were not included.

The separate Rust baseline coverage certificate remains blocked by the
uncommitted review-evidence packaging gap recorded in outcome.md; the reviewed
32 exposure approvals and Rust correction are already locally committed.
