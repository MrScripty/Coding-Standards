# Standards Library

Reusable engineering standards with routed workflows, profiles, topics, and
non-normative reference material.

Canonical applicability and dependency selection are owned by the
[Standards Router](STANDARDS-ROUTER.md). This README is a repository entrypoint;
it does not select modules or establish canonical ownership.

## Start Here

1. Read [Core Standards](CORE-STANDARDS.md).
2. Use the [Standards Router](STANDARDS-ROUTER.md) to select guidance from
   observable task and repository facts.
3. Record project-specific contracts and exceptions in the adopting
   repository through the selected canonical owners.

Unknown applicability is a Router diagnostic. Do not read every document,
select guidance from this README, or use a linked module as fallback authority.

The remaining template, customization, and license sections are scheduled for
closure in row 35.2. They cannot override Core or Router.

## Templates

Ready-to-use configuration files in `/templates/`:

| Template | Purpose |
|----------|---------|
| [README-TEMPLATE.md](templates/README-TEMPLATE.md) | Concise boundary and contract README profiles |
| [PLAN-TEMPLATE.md](templates/PLAN-TEMPLATE.md) | Implementation plan template |
| [PULL_REQUEST_TEMPLATE.md](templates/PULL_REQUEST_TEMPLATE.md) | PR checklist for decision traceability |
| [check-decision-traceability.sh](templates/check-decision-traceability.sh) | CI/hook script to enforce README/ADR decision updates |
| [decision-traceability-map.tsv](templates/decision-traceability-map.tsv) | Project-owned decision-bearing path and artifact map |
| [lefthook.yml](templates/lefthook.yml) | Pre-commit hook configuration |
| [.editorconfig](templates/.editorconfig) | Editor formatting settings |

## Customization

These standards are intentionally generic. When adopting them:

1. **Replace placeholders** - Look for `[YOUR-...]` markers
2. **Add tech-specific rules** - Extend with language-specific conventions
3. **Define your scopes** - Map commit scopes to your project structure
4. **Configure tooling** - Adapt hook commands to your build tools

## License

These standards are provided as-is for free use in any project.
