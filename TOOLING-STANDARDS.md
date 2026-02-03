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
4. **Full check in CI** - Complete analysis on every PR

### Common Linter Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| Style | Formatting, conventions | Prettier, ESLint, Black |
| Quality | Bugs, complexity, patterns | ESLint, Pylint, Clippy |
| Security | Vulnerabilities | Semgrep, Bandit, npm audit |
| Type | Type correctness | TypeScript, mypy, Flow |

### TypeScript/JavaScript: ESLint + Prettier

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "no-console": "warn"
  }
}
```

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

      - name: Lint
        run: npm run lint

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
| Linting | Staged files only | All files |
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

### Regular Security Audits

```yaml
# In CI workflow
- name: Audit dependencies
  run: npm audit --audit-level=high
```

### Lock File Integrity

Always commit lock files:
- `package-lock.json` (npm)
- `yarn.lock` (yarn)
- `pnpm-lock.yaml` (pnpm)

Verify in CI:
```bash
npm ci  # Fails if lock file doesn't match package.json
```

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
    "lint": "eslint src --ext .ts,.js",
    "lint:fix": "eslint src --ext .ts,.js --fix",
    "format": "prettier --write \"src/**/*.{ts,js,json,css}\"",
    "format:check": "prettier --check \"src/**/*.{ts,js,json,css}\"",
    "typecheck": "tsc --noEmit",
    "test": "jest",
    "prepare": "lefthook install"
  }
}
```

---

## Bypassing Hooks (Emergency Only)

When absolutely necessary:

```bash
git commit --no-verify -m "emergency: fix production outage"
```

**Document why** in the commit message.

**Follow up** with proper fix that passes all checks.

This should be rare and auditable.
