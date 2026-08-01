# Tooling Recipes

**Standards metadata**

- ID: `reference.recipes.tooling`
- Role: `reference`
- Level: `REFERENCE`
- Applies when: A project has selected a development-tool workflow and needs illustrative hook configuration.
- Does not apply when: Tool selection, dependency installation, acceptance evidence, hook scheduling, or bypass authority is being decided.
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
