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
