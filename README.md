# Standards Library

Reusable engineering guidance for deciding how to plan, build, verify and maintain software.

The library covers shared principles, task workflows, language and application profiles, and focused topics such as security, concurrency and accessibility. Its Router selects the guidance that applies to the work in front of you, so you can read the relevant material rather than the entire library.

## Start here

1. Read [Core Standards](CORE-STANDARDS.md).
2. Use the [Standards Router](STANDARDS-ROUTER.md) with observable facts about your task and repository.
3. Record project-specific contracts and exceptions in the adopting repository through the selected canonical owners.

The Router owns applicability and dependencies. If applicability is unknown, resolve that diagnostic there; a link in this README does not select a module or make it authoritative.

## Useful starting points

- [README template](templates/README-TEMPLATE.md)
- [Plan template](templates/PLAN-TEMPLATE.md)
- [Pull request template](templates/PULL_REQUEST_TEMPLATE.md)

Templates are resources, not substitutes for the Router's selected guidance.

## Tools and maintenance

The standards can be read directly; there is no application to launch. For agent navigation, controlled authoring and verification, see the [Standards Engine](tools/standards_engine/README.md) and its [connection setup](.agents/skills/standards-engine/references/environment.md).

[Verification commands](tools/standards_verifier/README.md) cover registered structural checks and separate implementation tests. Passing them does not certify the prose or a downstream project's compliance.

[Active work](docs/plans/README.md) · [Completed work](docs/archive/README.md) · [Architecture decisions](docs/decisions/README.md) · [Evaluation evidence](evaluation/standards-effectiveness/README.md)

[CC0 1.0 Universal](LICENSE).
