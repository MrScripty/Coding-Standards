# Tooling Recipes

**Standards metadata**

- ID: `reference.recipes.tooling`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A project has selected a development-tool workflow and needs illustrative hook or editor configuration.
- Does not apply when: Tool, dependency, editor-configuration, file-setting, acceptance, scheduling, or bypass decisions are being made.
- Requires: `workflow.tooling`, `topic.dependencies`
- Specializes: `none`
- Verification: Tooling-reference dispositions, metadata, link, and authority checks.
- Canonical owner: `reference/recipes/tooling.md`

This material is non-normative. [Tooling](../../workflows/tooling.md) owns tool
selection, configuration, automation, and scheduling. [Dependencies](../../topics/dependencies.md)
owns dependency selection and installation. Projects must make those decisions
before adapting an example below.

## Maintained Editor Configuration Recipe

For ordinary UTF-8 source files shared across editors, an `.editorconfig` can
express the Tooling defaults without selecting a language formatter:

```ini
root = true

[*]
charset = utf-8
insert_final_newline = true
```

Scope this to owned source files when the repository also contains formats
whose consumers require a different encoding or ending. Leave indentation and
language layout to the existing formatter. Verify an affected editor or tool
actually consumes the settings, then check the resulting file with its real
consumer. The following retained migration examples illustrate additional
mechanisms and historical configurations, not a current universal preset.

## Legacy Tool Setup And Package Script Example

The legacy setup example listed EditorConfig, a formatter such as Prettier, a
linter such as ESLint, and a hook runner such as Lefthook or Husky. This list is
historical illustration only. It does not establish a minimum setup, required
tool category, product choice, installation checklist, or provisioning
authority.

One legacy `package.json` example used:

```json
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

For ESLint versions using flat configuration, the legacy note omitted `--ext`
and relied on configuration `files` patterns. Product version, package manager,
script names, command composition, paths, globs, flags, check allocation, hook
installation, and result interpretation must come from canonical decisions;
none of this example is a default.

## Hook Feedback

A local hook can shorten feedback time for formatting, linting, type, or test
failures. That possible benefit does not make a hook stage, product, command,
or check an acceptance requirement. Required evidence remains defined by the
selected verification contract regardless of where the check runs.

## Lefthook Example

Lefthook is one possible language-agnostic hook runner. A project that has
selected it through its canonical tooling and dependency decisions might use
commands such as:

```bash
npm install lefthook --save-dev
curl -sSfL https://get.lh.run | sh
lefthook install
```

These are alternatives from the legacy example, not installation defaults.
Verify the selected installation source, current syntax, trust requirements,
and version policy before use.

An illustrative configuration is:

```yaml
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

The product, stages, parallel mode, globs, commands, and check allocation are
examples only. They do not define a fallback configuration.

## EditorConfig Example

EditorConfig can express selected formatting settings across supporting editors
and IDEs. It is only one possible transport. The canonical
[Tooling workflow](../../workflows/tooling.md#editor-and-file-configuration)
must select the mechanism, settings, scope, and precedence before this sample is
adapted.

```ini
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{js,ts,jsx,tsx,json,css,scss,html,svelte,vue}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

The mechanism, root scope, patterns, indentation, line ending, encoding,
whitespace, final-newline, and file-family values are examples only. They are
not recommended defaults and may conflict with repository or consumer
contracts.

## Linter Category Examples

Teams sometimes group lint checks as style, quality, security, or type checks.
Example products include Prettier or ESLint for style, Pylint or Clippy for
quality, Semgrep or Bandit for security, and TypeScript or mypy for type
analysis. These categories overlap and the products can serve several purposes.

The taxonomy and products are illustrative only. The canonical
[lint policy](../../workflows/tooling.md#lint-policy-and-orchestration) selects
purpose, rules, scope, severity, and tooling from owned facts; it does not infer
them from a category label or this product list.

## TypeScript Tooling Examples

After the canonical [TypeScript profile](../../profiles/languages/typescript.md#static-analysis-and-compiler-configuration)
selects project boundaries and checks, an ESLint flat configuration might scope
type-aware analysis through a `files` block and an owned project configuration:

```javascript
export default tseslint.config({
  files: ['src/**/*.{ts,tsx}'],
  languageOptions: { parserOptions: { project: './tsconfig.json' } },
  extends: [...tseslint.configs.strictTypeChecked],
});
```

Product-specific failure modes can include applying type-aware presets to
non-TypeScript files, mixing ignore declarations into incompatible blocks, or
using command flags unsupported by the selected configuration format.

A formatter configuration used by the same legacy example was:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

A compiler example might enable `strict`, `noImplicitReturns`,
`exactOptionalPropertyTypes`, or `noUncheckedIndexedAccess`. An architecture
example might implement an owned prohibition through ESLint's
`no-restricted-syntax`. These products, versions, presets, globs, project paths,
flags, severities, and selectors are examples only, not defaults.

### Illustrative React Automatic JSX Lint Adapter

When the selected React runtime, TypeScript contract, lint purpose, and plugin
semantics prove that legacy JSX-scope and runtime prop-validation rules do not
apply, an ESLint adapter might contain:

```javascript
rules: {
  'react/react-in-jsx-scope': 'off',
  'react/prop-types': 'off',
}
```

This snippet does not select React, a React version, the automatic JSX runtime,
TypeScript, ESLint, these plugins, rule disablement, severity, parser, preset, or
validation strategy. A project name or version label cannot replace evidence
that each rule is inapplicable to every selected source and consumer.

## Formatting Automation Examples

After canonical [formatting policy](../../workflows/tooling.md#formatting-policy-and-orchestration)
selects authority and behavior, a VS Code configuration might enable
`editor.formatOnSave` and select a formatter extension. A project using
Prettier and ESLint might install `eslint-config-prettier` to disable overlapping
style rules.

Those editor settings, products, extension identifiers, package commands, and
format-on-save behavior are examples only. They do not select formatting
authority, grant mutation authority, or establish when evidence must run.

A selected Prettier check might use:

```bash
prettier --check "src/**/*.ts"
```

The command, check mode, source glob, and nonzero result interpretation depend
on the selected product version and formatting claim. They are not defaults.

## CI Orchestration Examples

After canonical [CI orchestration](../../workflows/tooling.md#ci-orchestration-and-scheduling)
selects dependencies, continuation, cancellation, and reporting behavior, a
GitHub Actions matrix can express selected continuation with
`strategy.fail-fast: false`. A final reporting job can use `if: always()`, and
an explicitly advisory step can use `continue-on-error: true`.

One possible three-group graph places setup validation before independent
quality checks and runs expensive checks only after their required claims pass.
GitHub Actions can express those edges with `needs` and conditions such as
`success()`. Selected commands might include `./launcher.sh --ci-preflight` or
`npm run ci:preflight`.

The provider, matrix behavior, summary job, error continuation, dependency
syntax, group names, group count, execution order, and commands are examples
only. They do not define a fallback topology or evidence contract.

## Automation Cost Examples

After canonical [automation-cost policy](../../workflows/tooling.md#automation-cost-and-operational-evidence)
selects caching, cancellation, and diagnostics, GitHub Actions can express
read-only contents permission and per-run cancellation:

```yaml
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Selected Node and Rust dependency caches might use `actions/setup-node@v4` with
`cache: npm`, or `actions/cache@v4` for Cargo registry and Git data. Commands
such as `npm ci` and `cargo test --workspace`, lockfile-derived keys, exact
compiled-output keys, and broad dependency-download restore keys are
product-specific examples, not defaults.

GitHub failure diagnostics might append a redacted summary to
`$GITHUB_STEP_SUMMARY` and conditionally use `actions/upload-artifact@v4` for
selected log or test-result paths. Artifact names, missing-file behavior, and
retention periods must come from the canonical decision; the legacy example's
14-day retention is illustrative only.

These provider actions, versions, permissions, concurrency expressions, cache
paths, key fields, commands, summary variables, artifact paths, and retention
values cannot select automation behavior or satisfy evidence by themselves.


## Complete CI Workflow Example

This is the complete legacy GitHub Actions example. It is non-normative and may
be adapted only after canonical Tooling and Verification decisions select every
behavior represented by it.

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

The workflow path, provider, triggers, permissions, jobs, gates, action versions,
caches, commands, timeouts, matrices, dependencies, summaries, and shell logic
are examples only and define no fallback.
