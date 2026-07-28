# Commit Recipe

**Standards metadata**

- ID: `reference.recipes.commits`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A contributor needs examples for staging or formatting a commit.
- Does not apply when: Commit process or history authority is being decided.
- Requires: `workflow.commit`
- Specializes: `none`
- Verification: Commit consolidation dispositions and link checks.
- Canonical owner: `reference/recipes/commits.md`

This recipe illustrates the [Commit Workflow](../../workflows/commit.md). It
does not grant history-rewrite authority or override project-specific commit
types, scopes, footers, or line-length conventions.

## Conventional Shape

```text
<type>(<scope>): <imperative description>

[optional rationale and material contract effects]

[optional footer(s)]
```

Common types include:

| Type | Typical use |
| --- | --- |
| `feat` | New externally observable capability |
| `fix` | Correctness defect |
| `refactor` | Structure change without intended behavior change |
| `test` | Test-only change |
| `docs` | Documentation-only change |
| `perf` | Measured performance improvement |
| `build` | Build system or dependency mechanism |
| `ci` | Automation pipeline |
| `chore` | Maintenance not represented by a more precise type |

Use project-defined types when they differ. A scope names the affected owned
area and is omitted when no accurate scope exists.

## Subject And Body

Prefer a specific imperative subject:

```text
fix(session): rotate identifier after authentication
docs(router): add contract evolution route
test(parser): cover truncated frame diagnostic
```

Use the body for rationale, constraints, and material tradeoffs:

```text
fix(session): rotate identifier after authentication

Preserving the anonymous identifier allowed session fixation. Generate a new
identifier only after credentials are accepted and invalidate the prior one.
```

Keep verification commands and tool output in the plan ledger, pull request, or
completion record.

## Footers

Use repository-supported footers when applicable:

```text
BREAKING CHANGE: The response envelope now requires a version field.
Fixes #234
Co-authored-by: Name <name@example.com>
Agent: bounded-slice-agent
```

Do not invent a footer that downstream tooling does not understand.

## Staging Commands

Inspect and stage the declared write set:

```bash
git status --short
git add path/to/source path/to/focused-test
git diff --cached --check
git diff --cached
```

Interactive staging can separate independent hunks:

```bash
git add -p
```

Broad staging commands are appropriate only when the complete resulting index
is reviewed and exactly matches the declared write set.

## Branch Review Commands

After the project resolves an explicit intended base, read-only commands can
inspect the branch:

```bash
git log --graph --oneline --decorate <base-ref>..HEAD
git diff --stat <base-ref>...HEAD
```

These commands report history. They do not authorize amend, reset, rebase,
squash, or commit dropping.

## Example Messages

```text
feat(search): add typo-tolerant matching

Rank matches within the accepted edit-distance limit while preserving exact
matches first.
```

```text
fix(api): serialize concurrent state updates

Move mutation behind the canonical state owner so simultaneous requests cannot
publish conflicting revisions.

Fixes #127
```

```text
refactor(date): centralize display formatting

Replace five equivalent formatters with the existing locale-aware owner. No
observable format changes are intended.
```
