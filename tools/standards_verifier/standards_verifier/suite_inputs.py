from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .checks.contract_projection import ContractProjectionCheck
from .checks.decision import DecisionCheck
from .checks.derived_evidence import (
    KeyCoverageCheck,
    RepositoryPathsCheck,
    RepositorySubjectsCheck,
    TableTextAbsenceCheck,
)
from .checks.edge_dispositions import EdgeDispositionsCheck
from .checks.exact_text import ExactTextCheck
from .checks.git_index_paths import GitIndexPathsCheck
from .checks.inclusion import InclusionCheck
from .checks.keyed_relation import KeyedRelationCheck
from .checks.line_budget import LineBudgetCheck
from .checks.markdown_heading_cardinality import MarkdownHeadingCardinalityCheck
from .checks.markdown_headings import MarkdownHeadingsCheck
from .checks.markdown_link_coverage import MarkdownLinkCoverageCheck
from .checks.markdown_links import MarkdownLinksCheck
from .checks.markdown_section_text import MarkdownSectionTextCheck
from .checks.markdown_structure import MarkdownStructureCheck
from .checks.metadata import MetadataGraphCheck
from .checks.metadata_route import MetadataRouteCheck
from .checks.migration_python_dispositions import MigrationPythonDispositionsCheck
from .checks.numeric_lifecycle import NumericLifecycleCheck
from .checks.path_state import PathStateCheck
from .checks.policy_impact import PolicyImpactCheck
from .checks.policy_impact_migration import PolicyImpactMigrationCheck
from .checks.python_package_contract import PythonPackageContractCheck
from .checks.reference_inventory import ReferenceInventoryCheck
from .checks.relation import RelationCheck
from .checks.table import (
    ProjectedTableSource,
    TableCheck,
    read_projected_table_rows,
)
from .checks.text import TextCheck
from .config import extend_catalog, load_registry_catalog
from .model import Check, CheckContext
from .paths import contained_file, contained_path


DEFAULT_REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"
DEFAULT_PROJECTION = (
    "evaluation/standards-effectiveness/generated/suite-inputs.json"
)
CONTRACT = "standards-verifier:suite-input-projection:v1"


@dataclass(frozen=True, slots=True, order=True)
class InputUse:
    suite: str
    check: str
    role: str


@dataclass(frozen=True, slots=True)
class InputDeclaration:
    path: str
    state: str
    role: str


def _digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _source(source: ProjectedTableSource, role: str) -> InputDeclaration:
    return InputDeclaration(source.path, "present", role)


def _present(role: str, *paths: str) -> tuple[InputDeclaration, ...]:
    return tuple(InputDeclaration(path, "present", role) for path in paths)


def _absent(role: str, *paths: str) -> tuple[InputDeclaration, ...]:
    return tuple(InputDeclaration(path, "absent", role) for path in paths)


def _projected_paths(
    context: CheckContext,
    check_id: str,
    source: ProjectedTableSource,
    role: str,
) -> tuple[InputDeclaration, ...]:
    rows = read_projected_table_rows(context, check_id, source)
    return _present(role, *(value for row in rows for value in row if value))


def _check_inputs(
    check: Check,
    context: CheckContext,
) -> tuple[InputDeclaration, ...]:
    if isinstance(check, ContractProjectionCheck):
        return (
            *_present("schema", check.schema),
            *_present("interface", check.interface),
            *_present("generated-python", check.python),
            *_present("generated-agent-tools", check.agent_tools),
            *_present("examples", check.examples),
        )
    if isinstance(check, DecisionCheck):
        return _present("decision-table", check.path)
    if isinstance(check, EdgeDispositionsCheck):
        return (
            *_present("dispositions", check.path),
            *_present("packages", check.packages_path),
            *_present("edges", check.edges_path),
        )
    if isinstance(
        check,
        (
            ExactTextCheck,
            MarkdownHeadingCardinalityCheck,
            MarkdownHeadingsCheck,
            MarkdownSectionTextCheck,
            MarkdownStructureCheck,
            TextCheck,
        ),
    ):
        return _present("content", check.path)
    if isinstance(check, GitIndexPathsCheck):
        return _present("tracked-content", *check.tracked)
    if isinstance(check, InclusionCheck):
        return (
            _source(check.members, "members"),
            _source(check.container, "container"),
        )
    if isinstance(check, KeyCoverageCheck):
        return (_source(check.keys, "keys"), _source(check.records, "records"))
    if isinstance(check, KeyedRelationCheck):
        return (
            _source(check.keys, "keys"),
            *_present("expected", check.expected.path),
            *_present("observed", check.observed.path),
        )
    if isinstance(check, LineBudgetCheck):
        return (
            *_present("measured-content", *check.paths),
            *_present("baseline", check.baseline_path),
        )
    if isinstance(check, MarkdownLinkCoverageCheck):
        member_paths = tuple(
            value.partition("#")[0]
            for row in read_projected_table_rows(
                context, check.id, check.members
            )
            for value in row
            if value
        )
        return (
            *_present("markdown", check.path),
            _source(check.members, "members"),
            *_present("member-content", *member_paths),
        )
    if isinstance(check, MarkdownLinksCheck):
        declarations = list(_present("markdown", *(check.paths or ())))
        if check.members is not None:
            declarations.append(_source(check.members, "members"))
            declarations.extend(
                _projected_paths(
                    context,
                    check.id,
                    check.members,
                    "member-content",
                )
            )
        return tuple(declarations)
    if isinstance(check, MetadataGraphCheck):
        paths = check.paths or tuple(
            path for case in check.cases or () for path in case.paths
        )
        return _present("metadata", *paths)
    if isinstance(check, MetadataRouteCheck):
        return (
            *_present("routing-cases", check.path),
            *_present("routing-expectations", check.expectations_path),
        )
    if isinstance(check, MigrationPythonDispositionsCheck):
        package = contained_path(
            context.repo_root,
            check.package_path,
            suite=context.suite_id,
            check=check.id,
        )
        package_paths = tuple(
            path.relative_to(context.repo_root).as_posix()
            for path in sorted(package.rglob("*.py"))
            if path.is_file()
        )
        return (
            *_present("dispositions", check.path),
            *_present("package-python", *package_paths),
        )
    if isinstance(check, NumericLifecycleCheck):
        return _present(
            "numeric-lifecycle",
            check.baseline_path,
            check.decisions_path,
            check.packages_path,
            check.retirement_packages_path,
            check.retirements_path,
        )
    if isinstance(check, PathStateCheck):
        return (
            *_present("required-present", *check.present),
            *_absent("required-absent", *check.absent),
        )
    if isinstance(check, PolicyImpactCheck):
        if check.source_registry is not None:
            return _present("source-registry", check.source_registry)
        return _present(
            "fixture-manifest", *(case.manifest for case in check.cases or ())
        )
    if isinstance(check, PolicyImpactMigrationCheck):
        return (
            *_present("migration-evidence", check.evidence),
            *_present("accepted-registry", check.accepted_registry),
            *_present("proposed-registry", check.proposed_registry),
            *_present(
                "fixture-registry", *(case.registry for case in check.cases)
            ),
            *_absent(
                "retired-implementation",
                *(item.path for item in check.retired_implementation),
            ),
        )
    if isinstance(check, PythonPackageContractCheck):
        return _present("package-fixtures", check.fixtures)
    if isinstance(check, ReferenceInventoryCheck):
        return _present(
            "reference-inventory", check.candidates_path, check.manifest_path
        )
    if isinstance(check, RelationCheck):
        return (_source(check.left, "left"), _source(check.right, "right"))
    if isinstance(check, RepositoryPathsCheck):
        return (
            _source(check.paths, "paths"),
            *_projected_paths(
                context, check.id, check.paths, "projected-repository-path"
            ),
        )
    if isinstance(check, RepositorySubjectsCheck):
        declarations = [_source(check.subjects, "subjects")]
        for (subject,) in read_projected_table_rows(
            context, check.id, check.subjects
        ):
            kind, separator, identity = subject.partition(":")
            if separator and kind == "checker":
                declarations.extend(_present("checker-subject", identity))
        return tuple(declarations)
    if isinstance(check, TableCheck):
        declarations = list(_present("table", check.path))
        if check.members is not None:
            declarations.append(_source(check.members.source, "members"))
        return tuple(declarations)
    if isinstance(check, TableTextAbsenceCheck):
        return (
            *_present("content", check.path),
            _source(check.literals, "literals"),
        )
    raise TypeError(
        "suite-input projection has no adapter for "
        f"{type(check).__module__}.{type(check).__qualname__}"
    )


def compile_suite_input_projection(
    root: Path,
    registry_path: str = DEFAULT_REGISTRY,
) -> dict[str, object]:
    repo_root = root.resolve()
    catalog = load_registry_catalog(repo_root, registry_path)
    catalog = extend_catalog(repo_root, catalog, catalog.suite_ids)
    uses: dict[tuple[str, str], set[InputUse]] = {}
    for suite in catalog.suites:
        context = CheckContext(repo_root, suite.id, catalog)
        for check in suite.checks:
            for declaration in _check_inputs(check, context):
                key = (declaration.path, declaration.state)
                uses.setdefault(key, set()).add(
                    InputUse(suite.id, check.id, declaration.role)
                )

    paths: dict[str, str] = {}
    for path, state in uses:
        previous = paths.setdefault(path, state)
        if previous != state:
            raise ValueError(
                f"suite input has contradictory states: {path}: "
                f"{previous}, {state}"
            )

    inputs = []
    for (path, state), input_uses in sorted(uses.items()):
        if state == "present":
            source = contained_file(repo_root, path)
            digest: str | None = _digest(source.read_bytes())
        else:
            candidate = contained_path(repo_root, path)
            if candidate.exists() or candidate.is_symlink():
                raise ValueError(f"suite input must be absent: {path}")
            digest = None
        record: dict[str, object] = {
            "path": path,
            "state": state,
            "uses": [
                {"suite": use.suite, "check": use.check, "role": use.role}
                for use in sorted(input_uses)
            ],
        }
        if digest is not None:
            record["digest"] = digest
        inputs.append(record)

    registry = contained_file(repo_root, registry_path)
    suites = [
        {
            "id": entry.id,
            "path": entry.path,
            "digest": _digest(contained_file(repo_root, entry.path).read_bytes()),
        }
        for entry in catalog.entries
    ]
    return {
        "schema_version": 1,
        "contract": CONTRACT,
        "registry": {"path": registry_path, "digest": _digest(registry.read_bytes())},
        "suites": suites,
        "inputs": inputs,
    }


def suite_input_projection_bytes(root: Path) -> bytes:
    projection = compile_suite_input_projection(root)
    return (
        json.dumps(
            projection,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def check_suite_input_projection(root: Path) -> int:
    expected = suite_input_projection_bytes(root)
    path = root / DEFAULT_PROJECTION
    if not path.is_file() or path.read_bytes() != expected:
        print(f"STALE {DEFAULT_PROJECTION}")
        return 2
    return 0


def write_suite_input_projection(root: Path) -> int:
    path = root / DEFAULT_PROJECTION
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(suite_input_projection_bytes(root))
    return 0
