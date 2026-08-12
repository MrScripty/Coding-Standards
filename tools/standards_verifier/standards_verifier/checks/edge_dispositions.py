from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file
from .table import read_table_rows


MANIFEST_HEADER = (
    "package_id",
    "edge_type",
    "source",
    "target",
    "owner",
    "disposition",
    "replacement",
    "evidence",
    "rationale",
    "state",
)
PACKAGE_HEADER = (
    "train_order",
    "package_id",
    "subject",
    "owner",
    "risk",
    "semantic_outcome",
    "write_set",
    "prerequisites",
    "verification",
    "state",
)
EDGE_HEADER = ("edge_type", "source", "target")
EXECUTABLE_EDGE_TYPES = frozenset(
    {"executable_reference", "helper_dependency", "verifier_dependency"}
)
DISPOSITIONS = frozenset(
    {
        "native-engine",
        "independent-gate",
        "suite-requires",
        "same-owner-package",
        "external-owned-artifact",
        "invalid/unresolved",
    }
)
REPLACEMENT_KINDS = {
    "native-engine": ("assertion",),
    "independent-gate": ("checker", "suite"),
    "suite-requires": ("suite",),
    "same-owner-package": ("package",),
    "external-owned-artifact": ("artifact",),
    "invalid/unresolved": ("unresolved",),
}
STATES = frozenset({"admitted", "accepted"})


def _required_string(
    raw: dict[str, Any], field: str, suite: str, check: str
) -> str:
    value = raw.get(field)
    if not isinstance(value, str) or not value:
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING",
                "invalid",
                "field must be a non-empty string",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return value


def _contained_path(
    root: Path, value: str, *, suite: str, check: str
) -> None:
    path = PurePosixPath(value)
    resolved_root = root.resolve()
    candidate = (resolved_root / Path(*path.parts)).resolve(strict=False)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or not candidate.is_relative_to(resolved_root)
    ):
        raise EngineError(
            Diagnostic(
                "PATH.OUTSIDE_REPOSITORY",
                "invalid",
                "path must remain within the repository",
                suite=suite,
                check=check,
                path=value,
            )
        )


def _diagnostic(
    context: CheckContext,
    check: str,
    code: str,
    message: str,
    *,
    path: str,
    row: int | None = None,
    field: str | None = None,
    expected: str | None = None,
    observed: str | None = None,
) -> Diagnostic:
    return Diagnostic(
        code,
        "invalid",
        message,
        suite=context.suite_id,
        check=check,
        path=path,
        row=row,
        field=field,
        expected=expected,
        observed=observed,
    )


@dataclass(frozen=True, slots=True)
class EdgeDispositionsCheck:
    id: str
    path: str
    packages_path: str
    edges_path: str
    registry_path: str
    participation_token: str
    edge_free_token: str

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        rows = read_table_rows(
            root,
            self.path,
            MANIFEST_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        package_rows = read_table_rows(
            root,
            self.packages_path,
            PACKAGE_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        graph_rows = read_table_rows(
            root,
            self.edges_path,
            EDGE_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        registry_paths, registry_requires = self._load_registry(context)

        diagnostics: list[Diagnostic] = []
        packages: dict[str, dict[str, str]] = {}
        for line_number, package in enumerate(package_rows, start=2):
            package_id = package["package_id"]
            if package_id in packages:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_PACKAGE_DUPLICATE",
                        "package identity is duplicated",
                        path=self.packages_path,
                        row=line_number,
                        field="package_id",
                        expected="unique",
                        observed=package_id,
                    )
                )
            else:
                packages[package_id] = package

        actual_by_subject: dict[str, set[tuple[str, str, str]]] = {}
        for edge in graph_rows:
            if edge["edge_type"] not in EXECUTABLE_EDGE_TYPES:
                continue
            identity = (edge["edge_type"], edge["source"], edge["target"])
            actual_by_subject.setdefault(edge["source"], set()).add(identity)
            actual_by_subject.setdefault(edge["target"], set()).add(identity)

        packages_by_owner: dict[str, set[str]] = {}
        for package_id, package in packages.items():
            packages_by_owner.setdefault(package["owner"], set()).add(package_id)

        represented: dict[str, set[tuple[str, str, str]]] = {}
        seen: set[tuple[str, str, str, str]] = set()
        for line_number, row in enumerate(rows, start=2):
            for field, value in row.items():
                if not value:
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_EMPTY_VALUE",
                            "edge disposition fields must not be empty",
                            path=self.path,
                            row=line_number,
                            field=field,
                        )
                    )

            key = (
                row["package_id"],
                row["edge_type"],
                row["source"],
                row["target"],
            )
            if key in seen:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_DUPLICATE",
                        "edge disposition identity is duplicated",
                        path=self.path,
                        row=line_number,
                        field="package_id,edge_type,source,target",
                        expected="unique",
                        observed="\t".join(key),
                    )
                )
            seen.add(key)

            package = packages.get(row["package_id"])
            if package is None:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_PACKAGE",
                        "edge disposition references an unknown package",
                        path=self.path,
                        row=line_number,
                        field="package_id",
                        observed=row["package_id"],
                    )
                )
                continue

            verification = package["verification"].split(",")
            if self.participation_token not in verification:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_PARTICIPATION",
                        "edge package does not opt into this contract",
                        path=self.path,
                        row=line_number,
                        field="package_id",
                        expected=self.participation_token,
                        observed=package["verification"],
                    )
                )

            package_checker = package["subject"].removeprefix("checker:")
            source_is_package = row["source"] == package_checker
            target_is_package = row["target"] == package_checker
            retained_endpoint: str | None = None
            if (
                not package["subject"].startswith("checker:")
                or source_is_package == target_is_package
            ):
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_ENDPOINT",
                        "exactly one edge endpoint must equal the package checker subject",
                        path=self.path,
                        row=line_number,
                        field="source,target",
                        expected=package_checker,
                        observed=f"{row['source']}->{row['target']}",
                    )
                )
            else:
                retained_endpoint = (
                    row["target"] if source_is_package else row["source"]
                )
            if row["owner"] != package["owner"]:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_OWNER",
                        "edge owner must equal the package owner",
                        path=self.path,
                        row=line_number,
                        field="owner",
                        expected=package["owner"],
                        observed=row["owner"],
                    )
                )
            if row["state"] != package["state"] or row["state"] not in STATES:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_STATE",
                        "edge state must be admitted or accepted and equal "
                        "package state",
                        path=self.path,
                        row=line_number,
                        field="state",
                        expected=package["state"],
                        observed=row["state"],
                    )
                )
            if row["edge_type"] not in EXECUTABLE_EDGE_TYPES:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_TYPE",
                        "edge type is not executable",
                        path=self.path,
                        row=line_number,
                        field="edge_type",
                        expected=",".join(sorted(EXECUTABLE_EDGE_TYPES)),
                        observed=row["edge_type"],
                    )
                )
            if row["disposition"] not in DISPOSITIONS:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_DISPOSITION",
                        "edge disposition is not supported",
                        path=self.path,
                        row=line_number,
                        field="disposition",
                        expected=",".join(sorted(DISPOSITIONS)),
                        observed=row["disposition"],
                    )
                )
            elif (
                row["disposition"] == "invalid/unresolved"
                and row["state"] == "accepted"
            ):
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_UNRESOLVED_ACCEPTED",
                        "an unresolved edge cannot be accepted",
                        path=self.path,
                        row=line_number,
                        field="disposition",
                    )
                )
            elif retained_endpoint is not None:
                self._validate_replacement(
                    context,
                    row,
                    package,
                    retained_endpoint,
                    line_number,
                    packages_by_owner.get(package["owner"], set()),
                    registry_paths,
                    registry_requires,
                    diagnostics,
                )

            _contained_path(
                root, row["source"], suite=context.suite_id, check=self.id
            )
            _contained_path(
                root, row["target"], suite=context.suite_id, check=self.id
            )
            contained_file(
                root,
                row["evidence"],
                suite=context.suite_id,
                check=self.id,
            )
            represented.setdefault(row["package_id"], set()).add(
                (row["edge_type"], row["source"], row["target"])
            )

        participating = {
            package_id: package
            for package_id, package in packages.items()
            if self.participation_token in package["verification"].split(",")
            or self.edge_free_token in package["verification"].split(",")
        }
        for package_id, package in participating.items():
            source = package["subject"].removeprefix("checker:")
            declared = represented.get(package_id, set())
            actual = actual_by_subject.get(source, set())
            verification = package["verification"].split(",")
            has_manifest = self.participation_token in verification
            is_edge_free = self.edge_free_token in verification
            if has_manifest and is_edge_free:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_MODE",
                        "package cannot require edge rows and declare itself edge-free",
                        path=self.packages_path,
                        field="verification",
                        expected="exactly one edge participation mode",
                        observed=package["verification"],
                    )
                )
                continue
            if is_edge_free:
                if declared:
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_FREE_ROWS",
                            "edge-free package must not have disposition rows",
                            path=self.path,
                            field="package_id",
                            expected="[]",
                            observed=repr(sorted(declared)),
                        )
                    )
                if actual:
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_FREE_PRESENT",
                            "edge-free package has incident executable graph edges",
                            path=self.edges_path,
                            field="package_id",
                            expected="[]",
                            observed=repr(sorted(actual)),
                        )
                    )
                if package["state"] == "admitted":
                    contained_file(
                        root,
                        source,
                        suite=context.suite_id,
                        check=self.id,
                    )
                elif package["state"] == "accepted" and (root / source).exists():
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_ACCEPTED_SOURCE_PRESENT",
                            "accepted checker source is still present",
                            path=source,
                            field="package_id",
                            observed=package_id,
                        )
                    )
                continue
            if not declared:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_PACKAGE_COVERAGE",
                        "participating checker package has no edge dispositions",
                        path=self.path,
                        field="package_id",
                        observed=package_id,
                    )
                )
                continue
            if package["state"] == "admitted":
                missing = sorted(actual - declared)
                absent = sorted(declared - actual)
                if missing:
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_INCOMPLETE_COVERAGE",
                            "admitted package omits current incident executable edges",
                            path=self.path,
                            field="package_id",
                            expected=repr(sorted(actual)),
                            observed=repr(sorted(declared)),
                        )
                    )
                if absent:
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_ADMITTED_ABSENT",
                            "admitted disposition names an absent incident executable edge",
                            path=self.path,
                            field="package_id",
                            expected=repr(sorted(actual)),
                            observed=repr(sorted(declared)),
                        )
                    )
            elif package["state"] == "accepted":
                if (root / source).exists():
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_ACCEPTED_SOURCE_PRESENT",
                            "accepted checker source is still present",
                            path=source,
                            field="package_id",
                            observed=package_id,
                        )
                    )
                if actual:
                    diagnostics.append(
                        _diagnostic(
                            context,
                            self.id,
                            "ASSERT.EDGE_ACCEPTED_PRESENT",
                            "accepted package still has incident executable graph edges",
                            path=self.edges_path,
                            field="package_id",
                            expected="[]",
                            observed=repr(sorted(actual)),
                        )
                    )
        return diagnostics

    def _validate_replacement(
        self,
        context: CheckContext,
        row: dict[str, str],
        package: dict[str, str],
        retained_endpoint: str,
        line_number: int,
        same_owner_packages: set[str],
        registry_paths: dict[str, str],
        registry_requires: dict[str, set[str]],
        diagnostics: list[Diagnostic],
    ) -> None:
        kind, separator, value = row["replacement"].partition(":")
        expected_kinds = REPLACEMENT_KINDS[row["disposition"]]
        if not separator or not value or kind not in expected_kinds:
            diagnostics.append(
                _diagnostic(
                    context,
                    self.id,
                    "ASSERT.EDGE_REPLACEMENT",
                    "replacement evidence has the wrong typed form",
                    path=self.path,
                    row=line_number,
                    field="replacement",
                    expected=" or ".join(
                        f"{expected_kind}:<value>"
                        for expected_kind in expected_kinds
                    ),
                    observed=row["replacement"],
                )
            )
            return

        root = context.repo_root
        if kind == "package":
            if value not in same_owner_packages:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "same-owner replacement package is absent or has another owner",
                        path=self.path,
                        row=line_number,
                        field="replacement",
                        observed=row["replacement"],
                    )
                )
            return
        if kind == "unresolved":
            if value != "none":
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "unresolved replacement must be unresolved:none",
                        path=self.path,
                        row=line_number,
                        field="replacement",
                        observed=row["replacement"],
                    )
                )
            return

        if kind in {"checker", "artifact"}:
            if value != retained_endpoint:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "retained checker or artifact must equal the edge endpoint "
                        "opposite the package checker",
                        path=self.path,
                        row=line_number,
                        field="replacement",
                        expected=f"{kind}:{retained_endpoint}",
                        observed=row["replacement"],
                    )
                )
                return
            contained_file(
                root,
                value,
                suite=context.suite_id,
                check=self.id,
            )
            return

        if kind == "suite" and row["disposition"] == "independent-gate":
            suite_path = registry_paths.get(value)
            if suite_path is None:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "independent suite gate is not registered",
                        path=self.path,
                        row=line_number,
                        field="replacement",
                        observed=row["replacement"],
                    )
                )
                return
            if row["evidence"] != suite_path:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "independent suite gate evidence must equal its registered path",
                        path=self.path,
                        row=line_number,
                        field="evidence",
                        expected=suite_path,
                        observed=row["evidence"],
                    )
                )
            return

        if kind == "assertion":
            suite_path, marker, assertion_id = value.partition("#")
            if not marker or not assertion_id:
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "assertion replacement must name a contained suite path "
                        "and check id",
                        path=self.path,
                        row=line_number,
                        field="replacement",
                        expected="assertion:<path>#<check-id>",
                        observed=row["replacement"],
                    )
                )
                return
            if suite_path not in registry_paths.values():
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "native assertion suite is not registered",
                        path=self.path,
                        row=line_number,
                        field="replacement",
                        observed=row["replacement"],
                    )
                )
                return
            if suite_path not in package["write_set"].split(","):
                diagnostics.append(
                    _diagnostic(
                        context,
                        self.id,
                        "ASSERT.EDGE_REPLACEMENT",
                        "native assertion suite is outside the package write set",
                        path=self.path,
                        row=line_number,
                        field="replacement",
                        observed=row["replacement"],
                    )
                )
                return
            self._validate_assertion(
                context, suite_path, assertion_id, line_number, diagnostics
            )
            return

        source_suite, separator, target_suite = value.partition("->")
        source_path = registry_paths.get(source_suite)
        if (
            not separator
            or not source_suite
            or not target_suite
            or source_path is None
            or target_suite not in registry_paths
            or target_suite not in registry_requires.get(source_suite, set())
        ):
            diagnostics.append(
                _diagnostic(
                    context,
                    self.id,
                    "ASSERT.EDGE_REPLACEMENT",
                    "suite replacement must name a registered requires edge",
                    path=self.path,
                    row=line_number,
                    field="replacement",
                    expected="suite:<source-suite-id>-><target-suite-id>",
                    observed=row["replacement"],
                )
            )
            return
        if source_path not in package["write_set"].split(","):
            diagnostics.append(
                _diagnostic(
                    context,
                    self.id,
                    "ASSERT.EDGE_REPLACEMENT",
                    "requiring suite is outside the package write set",
                    path=self.path,
                    row=line_number,
                    field="replacement",
                    observed=row["replacement"],
                )
            )

    def _load_registry(
        self, context: CheckContext
    ) -> tuple[dict[str, str], dict[str, set[str]]]:
        source = contained_file(
            context.repo_root,
            self.registry_path,
            suite=context.suite_id,
            check=self.id,
        )
        with source.open("rb") as handle:
            raw = tomllib.load(handle)
        entries = raw.get("suites")
        if not isinstance(entries, list):
            raise EngineError(
                Diagnostic(
                    "ASSERT.EDGE_REGISTRY",
                    "invalid",
                    "suite registry must contain suite entries",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.registry_path,
                )
            )
        paths: dict[str, str] = {}
        requires: dict[str, set[str]] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            suite_id = entry.get("id")
            path = entry.get("path")
            dependencies = entry.get("requires")
            if (
                isinstance(suite_id, str)
                and isinstance(path, str)
                and isinstance(dependencies, list)
                and all(isinstance(item, str) for item in dependencies)
            ):
                paths[suite_id] = path
                requires[suite_id] = set(dependencies)
        return paths, requires

    def _validate_assertion(
        self,
        context: CheckContext,
        suite_path: str,
        assertion_id: str,
        line_number: int,
        diagnostics: list[Diagnostic],
    ) -> None:
        source = contained_file(
            context.repo_root,
            suite_path,
            suite=context.suite_id,
            check=self.id,
        )
        with source.open("rb") as handle:
            raw = tomllib.load(handle)
        checks = raw.get("checks")
        if not isinstance(checks, list) or assertion_id not in {
            item.get("id") for item in checks if isinstance(item, dict)
        }:
            diagnostics.append(
                _diagnostic(
                    context,
                    self.id,
                    "ASSERT.EDGE_REPLACEMENT",
                    "native assertion id is absent from the registered suite",
                    path=self.path,
                    row=line_number,
                    field="replacement",
                    observed=f"assertion:{suite_path}#{assertion_id}",
                )
            )


def parse_edge_dispositions_check(
    raw: dict[str, Any], suite_id: str
) -> EdgeDispositionsCheck:
    allowed = {
        "id",
        "type",
        "path",
        "packages_path",
        "edges_path",
        "registry_path",
        "participation_token",
        "edge_free_token",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "edge dispositions check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    return EdgeDispositionsCheck(
        check_id,
        _required_string(raw, "path", suite_id, check_id),
        _required_string(raw, "packages_path", suite_id, check_id),
        _required_string(raw, "edges_path", suite_id, check_id),
        _required_string(raw, "registry_path", suite_id, check_id),
        _required_string(raw, "participation_token", suite_id, check_id),
        _required_string(raw, "edge_free_token", suite_id, check_id),
    )
