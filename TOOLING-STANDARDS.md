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

pre-push:
  commands:
    test:
      run: npm test
```

### Hook Categories

| Hook | When | What to Run |
|------|------|-------------|
| pre-commit | Before each commit | Fast checks: lint, format, typecheck |
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

**Never remove a quality gate from CI without immediately replacing it.** A lint step removed
"temporarily" can result in hundreds of errors accumulating before anyone notices.

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
  quality:
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

      - name: Lint (no new violations)
        run: npm run lint:no-new

      - name: Lint (full audit)
        if: always()
        continue-on-error: true
        run: npm run lint:full

      - name: Type check
        run: npm run typecheck

      - name: Format check
        run: npm run format:check

      - name: Test
        run: npm test
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

Ensure every directory has documentation:

```bash
#!/bin/bash
# scripts/check-readmes.sh

find src -type d | while read dir; do
    if [ ! -f "$dir/README.md" ]; then
        echo "Missing README.md: $dir"
        exit 1
    fi
done
```

Add to pre-commit:
```yaml
pre-commit:
  commands:
    readme-check:
      run: ./scripts/check-readmes.sh
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
