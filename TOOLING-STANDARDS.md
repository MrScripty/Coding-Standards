# Tooling Standards

Code quality automation through linting, formatting, and pre-commit hooks.

## Pre-Commit Hooks

### Why Pre-Commit Hooks

Catch issues before they enter version control:
- Formatting inconsistencies
- Linting errors
- Type errors
- Failing tests

### Recommended Tool: Lefthook

Lefthook is language-agnostic and supports parallel execution.

**Installation:**
```bash
# npm
npm install lefthook --save-dev

# Or standalone
curl -sSfL https://get.lh.run | sh
```

**Initialize:**
```bash
lefthook install
```

### Basic Configuration

See [templates/lefthook.yml](templates/lefthook.yml) for a ready-to-use template.

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{ts,js}"
      run: npm run lint {staged_files}

    format-check:
      glob: "*.{ts,js,json,css}"
      run: npm run format:check {staged_files}

    typecheck:
      run: npm run typecheck

    decision-traceability:
      run: ./scripts/check-decision-traceability.sh

pre-push:
  commands:
    test:
      run: npm test
```

### Hook Categories

| Hook | When | What to Run |
|------|------|-------------|
| pre-commit | Before each commit | Fast checks: lint, format, typecheck, decision traceability |
| pre-push | Before pushing | Slower checks: full test suite |
| commit-msg | After writing message | Validate commit message format |

### History Cleanup Enforcement (Advisory Only)

History cleanup for regression/fix pairs is mandatory in process, but hook
enforcement should remain advisory only.

Do not hard-fail hooks for this rule. Detecting "clear regression + later fix"
requires human judgment and is not reliably automatable.

Recommended approach:
- Add a non-blocking pre-push reminder command
- Keep rewrite decisions manual
- Require cleanup only on unpushed history

### Performance Tips

1. **Run in parallel** - Independent checks should run concurrently
2. **Check only staged files** - Use `{staged_files}` placeholder
3. **Skip heavy checks in pre-commit** - Move full test suite to pre-push
4. **Use file globs** - Only run checks on relevant file types

### Persisted Artifact Validation Hooks

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

### Purpose

Consistent formatting across editors and IDEs without tool-specific configuration.

### Standard Configuration

See [templates/.editorconfig](templates/.editorconfig) for a ready-to-use template.

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

# Web files typically use 2-space indent
[*.{js,ts,jsx,tsx,json,css,scss,html,svelte,vue}]
indent_size = 2

# Markdown needs trailing whitespace for line breaks
[*.md]
trim_trailing_whitespace = false

# Makefiles require tabs
[Makefile]
indent_style = tab
```

### Key Settings

| Setting | Recommended | Why |
|---------|-------------|-----|
| indent_style | space | Consistent display across environments |
| end_of_line | lf | Avoid Windows/Unix issues |
| charset | utf-8 | Universal encoding |
| insert_final_newline | true | POSIX compliance, cleaner diffs |

---

## Linting Strategy

### Language-Agnostic Principles

1. **Fail on warnings** - No "acceptable" warnings in CI
2. **Autofix when possible** - Reduce manual work
3. **Check only changed files** - For speed in pre-commit
4. **Use tiered linting in CI** - Block critical issues and regressions; run full-lint audit on every PR

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

### Lint Debt Ratchet (When Full Lint Is Temporarily Non-Blocking)

1. Keep a committed baseline snapshot of current full-lint violations.
2. `lint:no-new` must fail if a PR increases total violations or introduces new violations in changed code.
3. Baseline updates are allowed only when counts stay the same or decrease.
4. When a rule/category reaches zero debt, promote it into a blocking tier.
5. Full lint returns to fully blocking once baseline debt is zero.

### Recommended CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  lint_critical:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint (critical anti-patterns)
        run: npm run lint:critical

  lint_no_new:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint:no-new

  lint_full_audit:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint:full

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run typecheck

  format_check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run format:check

  test:
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
      - run: npm ci
      - run: npm test

  ci_summary:
    if: always()
    needs: [lint_critical, lint_no_new, lint_full_audit, typecheck, format_check, test]
    runs-on: ubuntu-latest
    steps:
      - name: Summarize blocking results
        env:
          LINT_CRITICAL: ${{ needs.lint_critical.result }}
          LINT_NO_NEW: ${{ needs.lint_no_new.result }}
          TYPECHECK: ${{ needs.typecheck.result }}
          FORMAT_CHECK: ${{ needs.format_check.result }}
          TEST: ${{ needs.test.result }}
        run: |
          failures=0

          for gate in LINT_CRITICAL LINT_NO_NEW TYPECHECK FORMAT_CHECK TEST; do
            result="${!gate}"
            echo "- ${gate}: ${result}" >> "$GITHUB_STEP_SUMMARY"
            if [ "$result" != "success" ]; then
              failures=1
            fi
          done

          exit "$failures"
```

### CI vs. Local Checks

| Check | Local (pre-commit) | CI |
|-------|-------------------|-----|
| Linting | Staged files / fast checks | Critical + no-new (blocking) + full audit |
| Formatting | Staged files only | All files |
| Type check | Incremental | Full |
| Tests | Affected only | Full suite |

---

## Directory Validation

### README Enforcement

Enforce decision traceability with a script that checks all of the following:
- Every changed directory under `src/` has a `README.md`
- Required decision headings exist in each changed directory README
- `None` sections include both `Reason:` and `Revisit trigger:`
- Banned placeholder language is rejected
- PRs touching `src/` update the affected directory README(s) or add/update an ADR

For directories that must expose additional contract sections, configure the
script with comma-separated paths relative to `src/`:

```bash
export TRACEABILITY_HOST_FACING_DIRS="api,bindings/python"
export TRACEABILITY_STRUCTURED_PRODUCER_DIRS="schema,templates/workflows"
```

Configured host-facing directories must include `## API Consumer Contract`.
Configured structured-producer directories must include
`## Structured Producer Contract`.

```bash
mkdir -p scripts
cp templates/check-decision-traceability.sh scripts/check-decision-traceability.sh
chmod +x scripts/check-decision-traceability.sh
```

Copy [templates/check-decision-traceability.sh](templates/check-decision-traceability.sh)
into your repo as `scripts/check-decision-traceability.sh`.

Add to pre-commit and CI:
```yaml
pre-commit:
  commands:
    decision-traceability:
      run: ./scripts/check-decision-traceability.sh
```

```yaml
jobs:
  quality:
    steps:
      - name: Decision traceability
        run: ./scripts/check-decision-traceability.sh
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

When absolutely necessary:

```bash
git commit --no-verify -m "emergency: fix production outage"
```

**Document why** in the commit message.

**Follow up** with proper fix that passes all checks.

This should be rare and auditable.
