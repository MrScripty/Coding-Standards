# Tooling Standards

Legacy tooling guidance pending exact migration. Canonical generic automation
authority is [Tooling](workflows/tooling.md).

> **Acceptance authority:** [workflows/verification.md](workflows/verification.md)
> defines acceptance claims and what evidence proves. This file owns automation,
> scheduling, and reporting mechanisms. Moving a check between local hooks, CI,
> dedicated runners, release jobs, or manual procedures does not change its
> claim.

## Pre-Commit Hooks

Canonical hook selection and orchestration are defined by
[Tooling](workflows/tooling.md). The remaining subsections are migration input,
not competing generic authority.

### Why Pre-Commit Hooks

The former rationale is retained only as a non-normative
[Tooling recipe](reference/recipes/tooling.md#hook-feedback).

### Hook Runner Example

The former Lefthook selection and installation example is retained only in the
non-normative [Tooling recipe](reference/recipes/tooling.md#lefthook-example).

### Basic Configuration

Canonical configuration selection is defined by [Tooling](workflows/tooling.md).
The former configuration is retained only as a non-normative
[Tooling recipe](reference/recipes/tooling.md#lefthook-example).

### Hook Categories

Canonical scheduling is defined by [Tooling](workflows/tooling.md). The table
below remains migration input and does not define default stages.

| Hook | When | Typical Checks |
|------|------|-------------|
| pre-commit | Before each commit | Affected fast checks with useful local feedback |
| pre-push | Before pushing | Broader or more expensive checks selected by the project |
| commit-msg | After writing message | Validate commit message format |

These are scheduling defaults, not acceptance categories. A required claim may
run at either hook, in CI, on a dedicated environment, or through a recorded
manual procedure.

### Branch-History Review Reminder

Canonical history-review reminders and rewrite authority are defined by the
[Commit Workflow](workflows/commit.md#branch-history-review).

### Performance Tips

Canonical scheduling and cost decisions are defined by
[Tooling](workflows/tooling.md). The list below remains migration input.

1. **Run in parallel** - Independent checks should run concurrently
2. **Check only staged files** - Use `{staged_files}` placeholder
3. **Schedule by measured cost** - Keep interactive hooks useful and place
   expensive claims at an owned later gate
4. **Use file globs** - Only run checks on relevant file types

### Persisted Artifact Validation Hooks

Canonical persisted-artifact check orchestration is defined by
[Tooling](workflows/tooling.md). The recommendations below remain migration
input and are not defaults.

If the repo commits JSON, YAML, manifests, templates, saved workflows, or other
schema-backed artifacts, add fast staged-file validation where feasible.

Recommended approach:
- Run lightweight schema or shape validation in `pre-commit` for changed files
- Restrict checks to staged artifact paths for speed
- Regenerate derived artifacts in tooling when regeneration is deterministic
- Run broader validation or acceptance checks in `pre-push` when full-context
  verification is too slow for `pre-commit`

The goal is to stop checked-in examples and fixtures from drifting away from the
current producer contract.

---

## EditorConfig

Canonical editor-neutral configuration selection is defined by
[Tooling](workflows/tooling.md#editor-and-file-configuration). The remaining
rationale and examples are migration input, not EditorConfig authority.

### Purpose

The former EditorConfig rationale is retained only in the non-normative
[Tooling recipe](reference/recipes/tooling.md#editorconfig-example).

### Standard Configuration

The former template and file-family settings are retained only in the
non-normative [Tooling recipe](reference/recipes/tooling.md#editorconfig-example).

### Key Settings

Select settings through the canonical
[Tooling workflow](workflows/tooling.md#editor-and-file-configuration). The
former universal settings table is retired and defines no defaults.

---

## Linting Strategy

Canonical lint policy and orchestration are defined by
[Tooling](workflows/tooling.md#lint-policy-and-orchestration).

### Language-Agnostic Principles

Select purpose, scope, severity, automation, and schedule through the canonical
Tooling workflow. Warning failure, autofix, changed-file scope, tiers, and CI
placement are not defaults.

### Common Linter Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| Style | Formatting, conventions | Prettier, ESLint, Black |
| Quality | Bugs, complexity, patterns | ESLint, Pylint, Clippy |
| Security | Vulnerabilities | Semgrep, Bandit, npm audit |
| Type | Type correctness | TypeScript, mypy, Flow |

### TypeScript/JavaScript: ESLint 9+ (Flat Config) + Prettier

**IMPORTANT:** In ESLint 9 flat config, type-aware rules (like `strictTypeChecked`) must be
scoped inside a `files` block. Applying them globally will attempt to type-check non-TS files
(config files, JS scripts, etc.) and fail. Always scope type-checked rules to source files.

```javascript
// eslint.config.js
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import prettier from 'eslint-config-prettier';

export default tseslint.config(
    // Global ignores — always a separate block with no other keys
    {
        ignores: ['dist/**', 'node_modules/**', 'scripts/**', '*.config.*'],
    },
    // Type-aware rules scoped to source files only
    {
        files: ['src/**/*.{ts,tsx}'],
        extends: [
            eslint.configs.recommended,
            ...tseslint.configs.strictTypeChecked,
            prettier,
        ],
        languageOptions: {
            parserOptions: {
                project: './tsconfig.json',
            },
        },
        rules: {
            '@typescript-eslint/no-unused-vars': [
                'error',
                { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
            ],
            'no-console': 'error',
        },
    }
);
```

#### Common Flat Config Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| `strictTypeChecked` at top level | Type errors on `.js` config files | Move into `files: ['src/**/*.{ts,tsx}']` block |
| Missing `ignores` block | Linting `dist/`, `node_modules/` | Add separate `{ ignores: [...] }` block |
| `--ext ts,tsx` flag | Silently ignored in flat config | Use `files` patterns instead |

Frontend-specific lint details (including React runtime-specific rule guidance)
are defined in [FRONTEND-STANDARDS.md](FRONTEND-STANDARDS.md).

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

### TypeScript Strict Mode

Enable all strict checks for type safety:

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### Custom Rules for Architecture

Enforce architectural patterns with custom lint rules:

```javascript
// .eslintrc.js - Prevent direct state mutation
{
  rules: {
    'no-restricted-syntax': [
      'error',
      {
        selector: 'AssignmentExpression[left.object.name="state"]',
        message: 'Do not mutate state directly. Use setState or dispatch.',
      },
    ],
  },
}
```

---

## Formatting

### Principle: Format on Save

Configure editors to format automatically:

```json
// VS Code settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### Principle: Check in CI

CI should verify formatting without changing files:

```bash
# Prettier check mode
prettier --check "src/**/*.ts"

# Exit code 1 if files would change
```

### Format vs. Lint

| Tool | Purpose | When |
|------|---------|------|
| Formatter (Prettier) | Code style, whitespace | Every save |
| Linter (ESLint) | Code quality, patterns | Pre-commit, CI |

Configure them to not conflict:
```bash
npm install eslint-config-prettier --save-dev
```

---

## CI Integration

### Quality Gates Are Mandatory

**All blocking gates must pass before code merges.** If any gate is removed or disabled
(even temporarily), errors accumulate silently and become expensive to fix in bulk.

Full lint remains mandatory in CI as an audit step, even when temporarily
non-blocking during debt burn-down.

| Gate | What it catches | Non-negotiable? |
|------|----------------|-----------------|
| Lint (critical anti-patterns) | Security/correctness/concurrency high-risk patterns | Yes — blocks PR |
| Lint (no-new-violations) | New lint debt relative to baseline | Yes — blocks PR |
| Lint (full audit) | Complete lint debt inventory | Required to run; blocking once debt reaches zero |
| Type check | Type errors, interface mismatches | Yes — blocks PR |
| Format check | Inconsistent formatting | Yes — blocks PR |
| Tests | Regressions, broken behavior | Yes — blocks PR |
| Decision traceability | Missing module reasoning updates when code changes | Yes — blocks PR |

**Never remove a quality gate from CI without immediately replacing it.** A lint step removed
"temporarily" can result in hundreds of errors accumulating before anyone notices.

### Prefer Failure Aggregation Over Fail-Fast

Long-running CI should maximize defect visibility per run. Do not structure GitHub
Actions so one blocking failure cancels unrelated checks that could have reported
additional problems.

Rules:
- Run independent blocking gates as separate jobs when possible so lint, typecheck,
  formatting, tests, and platform builds all report in the same workflow run.
- For job matrices, set `strategy.fail-fast: false` unless cancelling the remaining
  matrix work is an intentional cost-saving tradeoff.
- Use an optional final summary job with `if: always()` to collect job outcomes and
  present one list of failures at the end of the run.
- Do not use `continue-on-error: true` on blocking gates just to keep the workflow
  moving. Prefer separate jobs. Reserve `continue-on-error` for explicitly
  non-blocking audit/reporting steps such as full-lint debt inventory.
- If a single command can surface multiple findings in one invocation (for example,
  a linter or test runner that reports all failures before exiting), prefer that
  mode over wrappers that stop on the first issue.

### Tiered CI Execution

CI should fail quickly when later work would be pointless, while still reporting
independent failures that help developers fix the branch in one pass.

Use three tiers:

| Tier | Purpose | Examples | Execution Rule |
|---|---|---|---|
| Preflight | Cheap checks that prove later jobs can run meaningfully | dependency install, lockfile integrity, tool bootstrap, generated-file drift, basic config validation | Run first; fail fast |
| Core quality | Independent blocking gates with high diagnostic value | critical lint, no-new lint, typecheck, format check, unit tests | Run in parallel after preflight |
| Expensive validation | Slow or resource-heavy checks that are wasteful if core quality fails | integration tests, browser tests, cross-platform builds, package builds, release smoke, coverage upload | Run only after required core gates pass |

Rules:
- Keep preflight small. It should catch invalid setup, missing tools, stale
  generated artifacts, and dependency/lockfile failures; it should not become a
  second copy of the full test suite.
- Do not gate one independent core quality job behind another just because both
  are blocking. For example, lint, typecheck, and unit tests should usually run
  side by side after preflight.
- Gate expensive jobs with `needs` on the relevant core jobs and the default
  `success()` behavior. If an expensive job is still useful after partial core
  failure, document why and make the condition explicit.
- Use `strategy.fail-fast: false` inside diagnostic matrices by default so one
  platform or shard failure does not hide the rest.
- The final CI summary job should use `if: always()` and report skipped jobs as
  intentionally skipped when an upstream tier failed.
- Preflight commands should be runnable locally through the launcher or package
  scripts, for example `./launcher.sh --ci-preflight` or
  `npm run ci:preflight`.

### Lint Debt Ratchet (When Full Lint Is Temporarily Non-Blocking)

1. Keep a committed baseline snapshot of current full-lint violations.
2. `lint:no-new` must fail if a PR increases total violations or introduces new violations in changed code.
3. Baseline updates are allowed only when counts stay the same or decrease.
4. When a rule/category reaches zero debt, promote it into a blocking tier.
5. Full lint returns to fully blocking once baseline debt is zero.

### CI Performance Standards

CI performance work must preserve the same quality signal. Do not speed up CI by
removing required gates, narrowing required platform coverage, hiding blocking
failures, or skipping tests without an explicit affected-test strategy.

Rules:
- Cache dependency downloads in every job that installs dependencies. Prefer
  package-manager-aware setup actions such as `actions/setup-node` with
  `cache: npm`, `actions/setup-python` with `cache: pip`, or ecosystem-specific
  cache actions that key from lockfiles.
- Cache package-manager stores and build-tool caches, not generated source
  trees or runtime state that can hide missing build steps. Avoid caching
  `node_modules`; use `npm ci` with an npm cache instead.
- Cache keys must include the runner OS, package manager, relevant lockfile
  hash, and toolchain version when the cache contains compiled artifacts. Use
  broad restore keys only for dependency download caches, not compiled outputs.
- Every job that invokes a package manager must still run the lockfile-enforcing
  install command (`npm ci`, `pnpm install --frozen-lockfile`,
  `cargo build`/`cargo test` with `Cargo.lock`, `dotnet restore --locked-mode`,
  etc.) after restoring cache.
- Add `timeout-minutes` to jobs or slow steps so hung tests and stalled
  dependency downloads fail clearly.
- Use top-level `concurrency` to cancel superseded runs for the same PR or
  branch. Do not use concurrency cancellation to replace `fail-fast: false`
  inside a live matrix run.
- Use path filters only to skip whole workflows whose owned files are untouched.
  Required checks must remain present for protected branches, either through
  matching always-run placeholder jobs or branch protection that matches the
  filtered workflow design.
- Do not make path filters the only guard around release work. Release workflows
  should be constrained by tag triggers; path filters are for skipping
  irrelevant validation work, not for deciding whether a commit is a release.
- Split independent gates into separate jobs even when this repeats dependency
  installation. Use caching or a small reusable setup action/composite action to
  reduce repeated setup cost rather than combining unrelated gates into one
  low-visibility job.
- Upload artifacts only when a downstream job, release process, or failure
  diagnosis needs them. Set retention periods intentionally for large artifacts.
- On CI failure, prefer GitHub job summaries, annotations, and uploaded
  artifacts for logs/results. Do not commit failure logs such as
  `docs/ci/ci.log` back to the default branch as part of normal CI.
- If durable CI logs are required, write them to a separate diagnostics branch,
  issue/PR comment, or external artifact store. The workflow must avoid
  recursive CI triggers and must not publish secrets, tokens, environment dumps,
  or unredacted third-party service output.
- Measure before adding heavyweight optimization. Track job duration, cache hit
  rate, and slowest steps when CI time becomes a recurring cost.

Recommended GitHub Actions defaults:

```yaml
permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

Recommended Node dependency setup:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: npm
    cache-dependency-path: package-lock.json

- run: npm ci
```

Recommended Rust dependency setup:

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/registry
      ~/.cargo/git
    key: cargo-${{ runner.os }}-${{ hashFiles('rust-toolchain.toml', '**/Cargo.lock') }}
    restore-keys: |
      cargo-${{ runner.os }}-

- run: cargo test --workspace
```

If caching Rust `target/` or other compiled outputs, use exact keys that include
the OS, Rust toolchain, target triple, feature mode, and lockfile hash. Do not
use broad restore keys for compiled output caches.

Recommended failure diagnostics:

```yaml
- name: Write failure summary
  if: failure()
  run: |
    {
      echo "## CI Failure"
      echo "- Workflow: $GITHUB_WORKFLOW"
      echo "- Job: $GITHUB_JOB"
      echo "- Run: $GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
    } >> "$GITHUB_STEP_SUMMARY"

- name: Upload failure logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: ci-logs-${{ github.run_id }}-${{ github.job }}
    path: |
      logs/**/*.log
      test-results/**/*.xml
    if-no-files-found: ignore
    retention-days: 14
```

### Recommended CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  preflight:
    runs-on: ubuntu-latest
    timeout-minutes: 8
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Preflight
        run: npm run ci:preflight

  lint_critical:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Lint (critical anti-patterns)
        run: npm run lint:critical

  lint_no_new:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run lint:no-new

  lint_full_audit:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run lint:full

  typecheck:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run typecheck

  format_check:
    needs: preflight
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run format:check

  test:
    needs: preflight
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm test

  integration:
    needs: [lint_critical, lint_no_new, typecheck, format_check, test]
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: package-lock.json
      - run: npm ci
      - run: npm run test:integration

  ci_summary:
    if: always()
    needs: [preflight, lint_critical, lint_no_new, lint_full_audit, typecheck, format_check, test, integration]
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Summarize blocking results
        env:
          PREFLIGHT: ${{ needs.preflight.result }}
          LINT_CRITICAL: ${{ needs.lint_critical.result }}
          LINT_NO_NEW: ${{ needs.lint_no_new.result }}
          TYPECHECK: ${{ needs.typecheck.result }}
          FORMAT_CHECK: ${{ needs.format_check.result }}
          TEST: ${{ needs.test.result }}
          INTEGRATION: ${{ needs.integration.result }}
        run: |
          failures=0

          for gate in PREFLIGHT LINT_CRITICAL LINT_NO_NEW TYPECHECK FORMAT_CHECK TEST INTEGRATION; do
            result="${!gate}"
            echo "- ${gate}: ${result}" >> "$GITHUB_STEP_SUMMARY"
            if [ "$result" = "skipped" ]; then
              echo "  - Skipped because an upstream tier did not pass." >> "$GITHUB_STEP_SUMMARY"
            fi
            if [ "$result" != "success" ]; then
              failures=1
            fi
          done

          exit "$failures"
```

### CI vs. Local Checks

Projects may use staged or incremental checks locally and broader checks in CI,
but this is a cost optimization rather than a proof hierarchy. Required claims
must run wherever their environment is available, including locally,
pre-commit, pre-push, CI, a dedicated runner, release verification, or a manual
gate. Do not classify an evidence kind as CI-only.

---

## Decision Traceability

### Impact Map

Follow the
[Documentation Workflow](workflows/documentation.md). Automated enforcement
must operate on project-owned facts rather than treating every source change as
a decision change.

Configure only paths whose modification is known to alter a durable
responsibility, contract, decision, or procedure:

```text
trigger_path	boundary_id	profile	artifact_path
src/api/public-contract.ts	api	contract-readme	src/api/README.md
src/engine/policy/	engine-policy	adr	docs/adr/ADR-001-engine-policy.md
ops/recovery/	recovery	runbook	docs/runbooks/recovery.md
```

- `trigger_path` is an exact repository-relative path, or a prefix when it ends
  in `/`.
- `boundary_id` is a stable project-owned identifier.
- `profile` is `boundary-readme`, `contract-readme`, `adr`, or `runbook`.
- `artifact_path` is the canonical durable artifact that owns the knowledge.

Do not map broad source directories unless every change beneath that prefix
really changes the named durable knowledge. Routine implementation paths stay
out of the map.

An ADR row requires `## Affected Boundaries` with an exact entry such as:

```markdown
- `boundary:engine-policy`
```

This association prevents an unrelated changed ADR from satisfying every
boundary. A mapped artifact is not interchangeable with another artifact type.

```bash
mkdir -p scripts .standards
cp templates/check-decision-traceability.sh scripts/check-decision-traceability.sh
cp templates/decision-traceability-map.tsv \
  .standards/decision-traceability.tsv
chmod +x scripts/check-decision-traceability.sh
```

Copy [templates/check-decision-traceability.sh](templates/check-decision-traceability.sh)
into your repo as `scripts/check-decision-traceability.sh` and replace every
example map row with project-owned facts.

### Explicit Diff Modes

Every invocation names what it inspects:

- `--mode staged` reads only the index with `git diff --cached`;
- `--mode range` requires explicit `--base-ref` and `--head-ref` commits and
  reads their three-dot diff.

Missing modes, maps, refs, or invalid refs fail with a configuration diagnostic.
The checker never guesses a branch, falls back to another range, or silently
skips an unresolved diff. It evaluates both prior and current map rows so
removing a row cannot hide the change that deletes or relocates a mapped path.

Add staged mode to pre-commit:

```yaml
pre-commit:
  commands:
    decision-traceability:
      run: >-
        ./scripts/check-decision-traceability.sh --mode staged
        --map .standards/decision-traceability.tsv
```

Use explicit pull-request commits in CI:

```yaml
jobs:
  quality:
    steps:
      - name: Decision traceability
        run: |
          ./scripts/check-decision-traceability.sh \
            --mode range \
            --map .standards/decision-traceability.tsv \
            --base-ref "${{ github.event.pull_request.base.sha }}" \
            --head-ref "${{ github.event.pull_request.head.sha }}"
```

### PR Template Enforcement

Use a PR template so every change records problem, constraints, rationale, and
alternatives:

```bash
mkdir -p .github
cp templates/PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE.md
```

---

## Dependency Auditing

See [DEPENDENCY-STANDARDS.md](DEPENDENCY-STANDARDS.md) for security auditing, lock file
integrity, unused dependency detection, and CI integration for dependency checks.

---

## Tool Installation Checklist

### Minimum Setup

1. **EditorConfig** - `.editorconfig` file
2. **Formatter** - Prettier or equivalent
3. **Linter** - ESLint or language equivalent
4. **Pre-commit hooks** - Lefthook or Husky

### Commands to Add

```json
// package.json
{
  "scripts": {
    "lint": "npm run lint:critical && npm run lint:no-new",
    "lint:critical": "node scripts/lint-critical.mjs",
    "lint:no-new": "node scripts/lint-no-new.mjs",
    "lint:full": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write \"src/**/*.{ts,js,json,css}\"",
    "format:check": "prettier --check \"src/**/*.{ts,js,json,css}\"",
    "typecheck": "tsc --noEmit",
    "test": "jest",
    "prepare": "lefthook install"
  }
}
```

> **Note:** ESLint 9+ flat config ignores `--ext` flags. File filtering is handled by `files`
> patterns in `eslint.config.js`. Use `eslint src/` without `--ext`.

---

## Bypassing Hooks (Emergency Only)

Canonical hook-bypass authority is defined by the
[Commit Workflow](workflows/commit.md#hook-bypass-authority). This legacy
section defines no emergency, command, documentation, or follow-up default.
