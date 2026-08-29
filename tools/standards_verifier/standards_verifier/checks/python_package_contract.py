from __future__ import annotations

import subprocess
import tempfile
import textwrap
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file
from ..python_packages import audit_python_packages, execute_python_package_contract


@dataclass(frozen=True, slots=True)
class PythonPackageContractCheck:
    id: str
    fixtures: str

    def run(self, context: CheckContext) -> list[Diagnostic]:
        diagnostics = [
            Diagnostic(
                finding.code,
                "invalid",
                finding.message,
                suite=context.suite_id,
                check=self.id,
                path=finding.path,
                field=finding.field,
                expected=finding.expected,
                observed=finding.observed,
            )
            for finding in audit_python_packages(context.repo_root)
        ]
        diagnostics.extend(
            Diagnostic(
                finding.code,
                "invalid",
                finding.message,
                suite=context.suite_id,
                check=self.id,
                path=finding.path,
                field=finding.field,
                expected=finding.expected,
                observed=finding.observed,
            )
            for finding in execute_python_package_contract(context.repo_root)
        )
        diagnostics.extend(self._fixture_diagnostics(context))
        return diagnostics

    def _fixture_diagnostics(self, context: CheckContext) -> list[Diagnostic]:
        path = contained_file(
            context.repo_root,
            self.fixtures,
            suite=context.suite_id,
            check=self.id,
        )
        try:
            with path.open("rb") as source:
                raw = tomllib.load(source)
            cases = _fixture_cases(raw)
        except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
            return [
                Diagnostic(
                    "PYTHON_PACKAGE.FIXTURE_INVALID",
                    "invalid",
                    str(error),
                    suite=context.suite_id,
                    check=self.id,
                    path=self.fixtures,
                )
            ]
        diagnostics = []
        for case in cases:
            observed = _audit_fixture(case)
            expected = tuple(case["expected_codes"])
            if observed != expected:
                diagnostics.append(
                    Diagnostic(
                        "PYTHON_PACKAGE.FIXTURE_MISMATCH",
                        "invalid",
                        "package fixture did not reach its exact diagnostic set",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.fixtures,
                        field=case["id"],
                        expected=",".join(expected),
                        observed=",".join(observed),
                    )
                )
        return diagnostics


def parse_python_package_contract_check(
    raw: dict[str, Any],
    suite_id: str,
) -> PythonPackageContractCheck:
    unknown = set(raw) - {"id", "type", "fixtures"}
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "python_package_contract check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if type(check_id) is not str or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    fixtures = raw.get("fixtures")
    if type(fixtures) is not str or not fixtures:
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING",
                "invalid",
                "python_package_contract fixtures must be a non-empty path",
                suite=suite_id,
                check=check_id,
                field="fixtures",
            )
        )
    return PythonPackageContractCheck(check_id, fixtures)


def _fixture_cases(raw: object) -> tuple[dict[str, object], ...]:
    if type(raw) is not dict or set(raw) != {"schema_version", "cases"}:
        raise ValueError("package fixture envelope is incomplete or has unknown fields")
    if raw["schema_version"] != 1 or type(raw["cases"]) is not list:
        raise ValueError("package fixture schema is unsupported")
    result = []
    identifiers: set[str] = set()
    for case in raw["cases"]:
        expected = {"id", "consumer_dependencies", "consumer_source", "expected_codes"}
        if type(case) is not dict or set(case) != expected:
            raise ValueError("package fixture case has invalid fields")
        identifier = case["id"]
        dependencies = case["consumer_dependencies"]
        source = case["consumer_source"]
        codes = case["expected_codes"]
        if type(identifier) is not str or not identifier or identifier in identifiers:
            raise ValueError("package fixture IDs must be nonempty and unique")
        if (
            type(dependencies) is not list
            or any(type(item) is not str or not item for item in dependencies)
            or len(set(dependencies)) != len(dependencies)
            or type(source) is not str
            or not source
            or type(codes) is not list
            or any(type(item) is not str or not item for item in codes)
            or tuple(codes) != tuple(sorted(set(codes)))
        ):
            raise ValueError(f"package fixture {identifier!r} is invalid")
        identifiers.add(identifier)
        result.append(case)
    if not result:
        raise ValueError("package fixture must contain cases")
    return tuple(result)


def _audit_fixture(case: dict[str, object]) -> tuple[str, ...]:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        subprocess.run(
            ("git", "init", "-q"), cwd=root, check=True, capture_output=True
        )
        _write_package(
            root,
            "b",
            "b-package",
            (),
            'value = 7\n__all__ = ("value",)\n',
        )
        _write_package(
            root,
            "a",
            "a-package",
            tuple(case["consumer_dependencies"]),
            str(case["consumer_source"]),
        )
        subprocess.run(
            ("git", "add", "-A"), cwd=root, check=True, capture_output=True
        )
        return tuple(sorted(item.code for item in audit_python_packages(root)))


def _write_package(
    root: Path,
    directory: str,
    project: str,
    dependencies: tuple[str, ...],
    source: str,
) -> None:
    dependency_values = ", ".join(f'"{item}"' for item in dependencies)
    manifest = root / f"tools/{directory}/pyproject.toml"
    package = root / f"tools/{directory}/{directory}/__init__.py"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    package.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        textwrap.dedent(
            f'''\
            [project]
            name = "{project}"
            version = "0.1.0"
            requires-python = ">=3.11,<3.13"
            dependencies = [{dependency_values}]

            [tool.standards-package]
            schema-version = 2
            public-import-root = "tools.{directory}.{directory}"
            repository-entrypoints = []
            '''
        ),
        encoding="utf-8",
    )
    package.write_text(textwrap.dedent(source).lstrip(), encoding="utf-8")


__all__ = ("PythonPackageContractCheck", "parse_python_package_contract_check")
