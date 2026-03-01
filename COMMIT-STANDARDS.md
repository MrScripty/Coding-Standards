# Commit Standards

Git workflow and conventional commits guide for consistent, readable history.

## Conventional Commits Format

All commits must follow this format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Components

| Component | Required | Description |
|-----------|----------|-------------|
| type | Yes | Category of change (see below) |
| scope | Recommended | Area of codebase affected |
| description | Yes | Brief summary in imperative mood |
| body | No | Detailed explanation if needed |
| footer | No | Breaking changes, issue refs, metadata |

### Commit Types

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature or capability | `feat(auth): add password reset flow` |
| `fix` | Bug fix | `fix(api): handle null response correctly` |
| `refactor` | Code restructuring (no behavior change) | `refactor(utils): extract validation helpers` |
| `chore` | Build, tooling, config changes | `chore(deps): update testing framework` |
| `docs` | Documentation only | `docs(readme): add installation steps` |
| `style` | Formatting, whitespace (no logic change) | `style(lint): fix indentation` |
| `test` | Adding or updating tests | `test(auth): add login edge cases` |
| `perf` | Performance improvements | `perf(db): add index for user queries` |
| `ci` | CI/CD pipeline changes | `ci(workflow): update to actions/checkout@v4` |

### Choosing a Type

```
Did you add new functionality?                    → feat
Did you fix a bug?                               → fix
Did you change code without changing behavior?   → refactor
Did you only change config/build/tooling?        → chore
Did you only update documentation?               → docs
Did you only change formatting?                  → style
Did you only add/update tests?                   → test
Did you only improve performance?                → perf
Did you only change CI/CD pipelines?             → ci
```

## Scopes

Define scopes that map to your project's structure:

```markdown
## Example Scopes

| Scope | Covers |
|-------|--------|
| api | API endpoints, request handling |
| auth | Authentication, authorization |
| ui | User interface components |
| db | Database, migrations, queries |
| config | Configuration, environment |
| deps | Dependencies |
| ci | CI/CD pipelines |
```

### Scope Guidelines

1. **Be consistent** - Use the same scope for related changes
2. **Keep it short** - Single word preferred
3. **Match structure** - Scopes should reflect directory or module names
4. **Omit if unclear** - Better no scope than wrong scope

## Writing Good Descriptions

### Use Imperative Mood

Write as if completing: "This commit will..."

```
// GOOD (imperative)
add user authentication
fix null pointer exception
remove deprecated API

// BAD (other moods)
added user authentication
fixes null pointer exception
removing deprecated API
```

### Be Specific

```
// BAD: Vague
fix bug
update code
make changes

// GOOD: Specific
fix race condition in session timeout
update validation to reject empty strings
rename userId to accountId for clarity
```

### Keep It Short

**Target: Under 72 characters**

If you need more detail, use the body.

## Commit Body

Use the body for:
- Explaining **why** the change was made
- Describing the **approach** taken
- Noting any **trade-offs** or alternatives considered

```
fix(auth): prevent session fixation attack

Previously, session IDs were preserved across login, allowing
attackers to fixate a session. Now regenerate session ID on
successful authentication.

Alternative considered: Binding sessions to IP addresses was
rejected due to issues with mobile users changing networks.
```

## Commit Footer

### Breaking Changes

```
feat(api): change response format to JSON:API

BREAKING CHANGE: Response envelope changed from { data: ... }
to { data: ..., meta: ..., links: ... }. Clients must update
their parsing logic.
```

### Issue References

```
fix(checkout): calculate tax correctly for exempt items

Fixes #234
Closes #235
Refs #200
```

### Co-Authors

```
feat(dashboard): add real-time updates

Co-authored-by: Name <email@example.com>
```

### Agent Footer (Multi-Agent Orchestration)

When commits are produced by automated agents:

```
feat(backend): add user authentication

Agent: auth-service-agent
```

This footer enables tracking which agent produced which changes in
multi-agent workflows. Useful for auditing and debugging automated
contributions.

## Pre-Commit Checklist

Before every commit:

```bash
# 1. Check what's staged
git status

# 2. Review the actual changes
git diff --cached

# 3. Review unpushed history for regression + fix pairs
# If no upstream is configured, compare against your intended base branch
# (for example: origin/main..HEAD)
git log --oneline --decorate @{upstream}..HEAD

# 4. Run linters/formatters
[your-lint-command]

# 5. Run tests (at minimum, affected tests)
[your-test-command]

# 6. Commit with conventional format
git commit -m "type(scope): description"
```

## Mandatory History Cleanup Before Commit

This process is mandatory for all branches.
Treat it as a default part of every commit routine, not optional cleanup.

Before creating a new commit, inspect unpushed local commits for a clear
regression plus a later fix for that same regression. Use judgment.

When a clear regression/fix pair exists, you must rewrite unpushed history to:
- Drop the regression commit
- Fold the fix into the appropriate earlier commit (`fixup` preferred)

Use `fixup!` commits during development so cleanup remains fast and reliable with
autosquash.

### Workflow

```bash
# Inspect unpushed commits
# If no upstream is configured, compare against your intended base branch
# (for example: origin/main..HEAD)
git log --oneline --decorate @{upstream}..HEAD

# Mark intended cleanup as fixup during normal development
git commit --fixup <target-commit>

# Rewrite unpushed history and autosquash fixups
# If no upstream is configured, use your intended base branch
# (for example: origin/main)
git rebase -i --autosquash @{upstream}
```

After rewriting history, re-run affected tests before creating the next commit.

## Commit Frequency

### Commit Often

Make small, focused commits:

```
// BAD: One giant commit
"feat: implement entire user management system"

// GOOD: Incremental commits
"feat(user): add user model and database schema"
"feat(user): implement user creation endpoint"
"feat(user): add email validation"
"feat(user): implement user listing with pagination"
"test(user): add unit tests for user service"
```

### One Logical Change Per Commit

Each commit should be:
- **Atomic:** Complete in itself
- **Reversible:** Can be reverted cleanly
- **Reviewable:** Easy to understand in isolation

## Staging Best Practices

### Stage Specific Files

```bash
# BAD: Stages everything (may include unwanted files)
git add .
git add -A

# GOOD: Stage specific files
git add src/auth/login.ts
git add src/auth/login.test.ts
```

### Review Before Committing

```bash
# Always check what you're about to commit
git diff --cached

# Or use interactive staging
git add -p
```

### Exclude Sensitive Files

Never commit:
- `.env` files with secrets
- API keys or credentials
- Personal configuration
- Large binary files (unless intentional)

## Commit Message Examples

### Feature

```
feat(search): implement fuzzy matching

Add Levenshtein distance algorithm for typo-tolerant search.
Results now include matches within edit distance of 2.

- Add fuzzy matching utility function
- Integrate with existing search pipeline
- Update search results ranking
```

### Bug Fix

```
fix(api): handle concurrent request race condition

Multiple simultaneous requests could corrupt shared state.
Now using mutex lock around critical section.

Fixes #127
```

### Refactor

```
refactor(utils): extract date formatting to dedicated module

Date formatting was duplicated across 5 files. Centralized
into utils/date.ts with consistent formatting options.

No behavior change - all existing formats preserved.
```

### Chore

```
chore(ci): add automated release workflow

Configure GitHub Actions to:
- Run tests on all PRs
- Build and publish on version tags
- Generate changelog from commits
```

## Handling Mistakes

### Amend Last Commit (Before Push)

```bash
# Fix the last commit message
git commit --amend -m "correct message"

# Add forgotten files to last commit
git add forgotten-file.ts
git commit --amend --no-edit
```

### After Pushing

Don't rewrite public history. Instead:

```bash
# Create a new commit that fixes the issue
git commit -m "fix(scope): correct mistake from previous commit"
```

The mandatory cleanup rule applies only to unpushed local commits.
Never rewrite shared, already-pushed history.

## Merge Commits vs. Squash

### When to Squash

- Feature branches with messy "WIP" commits
- Multiple "fix typo" or "oops" commits
- When the intermediate commits aren't meaningful

### When to Keep History

- Each commit represents a logical step
- Commits are already clean and atomic
- You want to preserve the development narrative

### Rewriting Unpushed Merge Commits

Rewriting unpushed merge commits is allowed when cleaning local history.

Use extra caution: merge rewrites can change branch topology and integration
context. Prefer merge-aware rebase mode and verify the final graph before
pushing.

```bash
# Merge-aware history rewrite (when merge commits are involved)
# If no upstream is configured, use your intended base branch
# (for example: origin/main)
git rebase -i --rebase-merges @{upstream}

# Verify topology before push
# If no upstream is configured, compare against your intended base branch
# (for example: origin/main..HEAD)
git log --graph --oneline --decorate @{upstream}..HEAD
```
