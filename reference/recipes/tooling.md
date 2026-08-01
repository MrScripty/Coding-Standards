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
