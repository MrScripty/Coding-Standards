from __future__ import annotations

import ast
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


_PYTHON_RANGE = ">=3.11,<3.13"
_DEPENDENCY_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


@dataclass(frozen=True, slots=True)
class PythonPackageFinding:
    code: str
    message: str
    path: str
    field: str | None = None
    expected: str | None = None
    observed: str | None = None


@dataclass(frozen=True, slots=True)
class PythonPackageContract:
    manifest: str
    project_name: str
    dependencies: tuple[str, ...]
    public_root: str
    entrypoints: tuple[str, ...]

    @property
    def root_path(self) -> PurePosixPath:
        return PurePosixPath(*self.public_root.split("."))


def _dependency_name(requirement: str) -> str:
    match = _DEPENDENCY_NAME.match(requirement)
    if match is None:
        return ""
    return match.group(0).lower().replace("_", "-")


def _indexed_paths(root: Path) -> tuple[str, ...]:
    completed = subprocess.run(
        ("git", "ls-files", "-z", "--cached"),
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
    return tuple(
        sorted(
            path.decode("utf-8")
            for path in completed.stdout.split(b"\0")
            if path
        )
    )


def _load_contract(
    root: Path,
    manifest: str,
) -> tuple[PythonPackageContract | None, list[PythonPackageFinding]]:
    findings: list[PythonPackageFinding] = []
    try:
        with (root / manifest).open("rb") as source:
            raw = tomllib.load(source)
    except (OSError, tomllib.TOMLDecodeError) as error:
        return None, [
            PythonPackageFinding(
                "PYTHON_PACKAGE.MANIFEST_UNAVAILABLE",
                f"package manifest cannot be loaded: {error}",
                manifest,
            )
        ]
    project = raw.get("project")
    package = raw.get("tool", {}).get("standards-package")
    if not isinstance(project, dict) or not isinstance(package, dict):
        return None, [
            PythonPackageFinding(
                "PYTHON_PACKAGE.MANIFEST_CONTRACT",
                "manifest requires project and tool.standards-package tables",
                manifest,
            )
        ]
    unknown = set(package) - {
        "schema-version",
        "public-import-root",
        "repository-entrypoints",
    }
    if unknown:
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.UNKNOWN_FIELD",
                "standards-package contains an unknown field",
                manifest,
                field=sorted(unknown)[0],
            )
        )
    if package.get("schema-version") != 1:
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.SCHEMA_VERSION",
                "standards-package schema-version must equal integer 1",
                manifest,
                field="schema-version",
                expected="1",
                observed=repr(package.get("schema-version")),
            )
        )
    name = project.get("name")
    python_range = project.get("requires-python")
    dependencies = project.get("dependencies")
    public_root = package.get("public-import-root")
    entrypoints = package.get("repository-entrypoints")
    if type(name) is not str or not name:
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.PROJECT_NAME",
                "project name must be a nonempty string",
                manifest,
                field="project.name",
            )
        )
    if python_range != _PYTHON_RANGE:
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.PYTHON_RANGE",
                "requires-python must equal the admitted A1b range",
                manifest,
                field="project.requires-python",
                expected=_PYTHON_RANGE,
                observed=repr(python_range),
            )
        )
    if (
        not isinstance(dependencies, list)
        or any(type(item) is not str or not item for item in dependencies)
        or len({_dependency_name(item) for item in dependencies}) != len(dependencies)
        or any(not _dependency_name(item) for item in dependencies)
    ):
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.DEPENDENCIES",
                "project dependencies must be unique valid requirement strings",
                manifest,
                field="project.dependencies",
            )
        )
        dependencies = []
    if (
        type(public_root) is not str
        or not public_root.startswith("tools.")
        or any(not part.isidentifier() for part in public_root.split("."))
    ):
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.PUBLIC_ROOT",
                "public-import-root must be one canonical tools.* Python root",
                manifest,
                field="public-import-root",
            )
        )
    if (
        not isinstance(entrypoints, list)
        or any(type(item) is not str or not item for item in entrypoints)
        or len(set(entrypoints)) != len(entrypoints)
    ):
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.ENTRYPOINTS",
                "repository-entrypoints must be a unique string list",
                manifest,
                field="repository-entrypoints",
            )
        )
        entrypoints = []
    if findings:
        return None, findings
    assert isinstance(name, str)
    assert isinstance(public_root, str)
    return (
        PythonPackageContract(
            manifest,
            name.lower().replace("_", "-"),
            tuple(sorted(_dependency_name(item) for item in dependencies)),
            public_root,
            tuple(entrypoints),
        ),
        [],
    )


def _local_module_path(package_file: Path, module: str | None) -> Path:
    base = package_file.parent
    if module:
        base = base.joinpath(*module.split("."))
    candidate = base.with_suffix(".py")
    if candidate.is_file():
        return candidate
    return base / "__init__.py"


def resolve_public_exports(root: Path, contract: PythonPackageContract) -> tuple[str, ...]:
    cache: dict[Path, tuple[str, ...]] = {}

    def resolve(path: Path) -> tuple[str, ...]:
        path = path.resolve()
        if path in cache:
            return cache[path]
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        aliases: dict[str, tuple[str, ...]] = {}
        assignments: list[ast.expr] = []
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.level == 1:
                child = _local_module_path(path, node.module)
                for name in node.names:
                    if name.name == "__all__" and name.asname:
                        aliases[name.asname] = resolve(child)
            if (
                isinstance(node, (ast.Assign, ast.AnnAssign))
                and (
                    any(
                        isinstance(target, ast.Name) and target.id == "__all__"
                        for target in node.targets
                    )
                    if isinstance(node, ast.Assign)
                    else isinstance(node.target, ast.Name)
                    and node.target.id == "__all__"
                )
            ):
                value = node.value
                if value is not None:
                    assignments.append(value)
        if len(assignments) != 1:
            raise ValueError(f"{path}: expected exactly one __all__ assignment")
        expression = assignments[0]
        if not isinstance(expression, (ast.Tuple, ast.List)):
            raise ValueError(f"{path}: __all__ must be one tuple or list")
        exports: list[str] = []
        for item in expression.elts:
            if isinstance(item, ast.Constant) and type(item.value) is str:
                exports.append(item.value)
                continue
            if isinstance(item, ast.Starred) and isinstance(item.value, ast.Name):
                try:
                    exports.extend(aliases[item.value.id])
                except KeyError as error:
                    raise ValueError(
                        f"{path}: starred __all__ value must come from a local child"
                    ) from error
                continue
            raise ValueError(f"{path}: __all__ contains a non-static export")
        if not exports or len(set(exports)) != len(exports):
            raise ValueError(f"{path}: __all__ must be nonempty and unique")
        cache[path] = tuple(exports)
        return cache[path]

    return resolve(root / contract.root_path / "__init__.py")


def _matching_root(
    module: str,
    roots: dict[str, PythonPackageContract],
) -> tuple[str, PythonPackageContract] | None:
    matches = [
        (name, contract)
        for name, contract in roots.items()
        if module == name or module.startswith(f"{name}.")
    ]
    return max(matches, key=lambda item: len(item[0])) if matches else None


def _imported_dependencies(
    root: Path,
    source_paths: Iterable[str],
    owner: PythonPackageContract,
    roots: dict[str, PythonPackageContract],
    exports: dict[str, frozenset[str]],
) -> tuple[set[str], list[PythonPackageFinding]]:
    dependencies: set[str] = set()
    findings: list[PythonPackageFinding] = []
    for path in source_paths:
        tree = ast.parse((root / path).read_text(encoding="utf-8"), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                function = node.func
                dynamic = (
                    isinstance(function, ast.Name) and function.id == "__import__"
                ) or (
                    isinstance(function, ast.Attribute)
                    and function.attr == "import_module"
                )
                if dynamic:
                    findings.append(
                        PythonPackageFinding(
                            "PYTHON_PACKAGE.DYNAMIC_IMPORT",
                            "production sources cannot bypass static import ownership",
                            path,
                        )
                    )
            modules: list[tuple[str, tuple[ast.alias, ...], bool]] = []
            if isinstance(node, ast.Import):
                modules.extend((item.name, (), False) for item in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                modules.append((node.module, tuple(node.names), True))
            for module, names, from_import in modules:
                matched = _matching_root(module, roots)
                if matched is not None:
                    public_root, dependency = matched
                    if dependency.project_name == owner.project_name:
                        continue
                    dependencies.add(dependency.project_name)
                    if module != public_root:
                        findings.append(
                            PythonPackageFinding(
                                "PYTHON_PACKAGE.PRIVATE_IMPORT",
                                "cross-Module imports must target the public root",
                                path,
                                observed=module,
                                expected=public_root,
                            )
                        )
                        continue
                    if from_import:
                        for item in names:
                            if item.name == "*":
                                findings.append(
                                    PythonPackageFinding(
                                        "PYTHON_PACKAGE.STAR_IMPORT",
                                        "cross-Module star imports are prohibited",
                                        path,
                                        observed=public_root,
                                    )
                                )
                            elif item.name not in exports[public_root]:
                                findings.append(
                                    PythonPackageFinding(
                                        "PYTHON_PACKAGE.UNEXPORTED_IMPORT",
                                        "imported name is absent from the owner root __all__",
                                        path,
                                        field=item.name,
                                        observed=public_root,
                                    )
                                )
                    continue
                top_level = module.split(".", 1)[0]
                if top_level == "tools":
                    findings.append(
                        PythonPackageFinding(
                            "PYTHON_PACKAGE.UNOWNED_IMPORT",
                            "tools import has no manifest-owned public root",
                            path,
                            observed=module,
                        )
                    )
                elif top_level not in sys.stdlib_module_names and top_level != "__future__":
                    dependencies.add(top_level.lower().replace("_", "-"))
    return dependencies, findings


def audit_python_packages(root: Path) -> tuple[PythonPackageFinding, ...]:
    root = root.resolve()
    try:
        indexed = _indexed_paths(root)
    except RuntimeError as error:
        return (
            PythonPackageFinding(
                "PYTHON_PACKAGE.GIT_INDEX",
                f"cannot read Git index: {error}",
                ".git/index",
            ),
        )
    manifests = tuple(
        path
        for path in indexed
        if path.startswith("tools/")
        and path.endswith("/pyproject.toml")
        and len(PurePosixPath(path).parts) == 3
        and (root / path).is_file()
    )
    contracts: list[PythonPackageContract] = []
    findings: list[PythonPackageFinding] = []
    for manifest in manifests:
        contract, contract_findings = _load_contract(root, manifest)
        findings.extend(contract_findings)
        if contract is not None:
            contracts.append(contract)
    names = [item.project_name for item in contracts]
    roots_list = [item.public_root for item in contracts]
    entrypoints = [path for item in contracts for path in item.entrypoints]
    for values, field in (
        (names, "project.name"),
        (roots_list, "public-import-root"),
        (entrypoints, "repository-entrypoints"),
    ):
        repeated = sorted(value for value in set(values) if values.count(value) > 1)
        for value in repeated:
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.DUPLICATE_OWNERSHIP",
                    "package ownership value is duplicated",
                    value,
                    field=field,
                )
            )
    roots = {item.public_root: item for item in contracts}
    export_sets: dict[str, frozenset[str]] = {}
    for contract in contracts:
        init_path = contract.root_path / "__init__.py"
        display = init_path.as_posix()
        if display not in indexed or not (root / init_path).is_file():
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.PUBLIC_ROOT_UNAVAILABLE",
                    "public root __init__.py is absent from the Git index",
                    display,
                )
            )
            continue
        try:
            export_sets[contract.public_root] = frozenset(
                resolve_public_exports(root, contract)
            )
        except (OSError, SyntaxError, UnicodeError, ValueError) as error:
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.EXPORT_CONTRACT",
                    str(error),
                    display,
                )
            )
    owned_sources: dict[str, list[str]] = {item.project_name: [] for item in contracts}
    entrypoint_owners = {
        path: contract.project_name
        for contract in contracts
        for path in contract.entrypoints
    }
    for path in indexed:
        pure = PurePosixPath(path)
        if (
            not path.startswith("tools/")
            or not path.endswith(".py")
            or "tests" in pure.parts
            or not (root / path).is_file()
        ):
            continue
        owner = entrypoint_owners.get(path)
        if owner is None:
            candidates = [
                contract
                for contract in contracts
                if pure.is_relative_to(contract.root_path)
            ]
            if len(candidates) == 1:
                owner = candidates[0].project_name
        if owner is None:
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.UNOWNED_SOURCE",
                    "tracked production Python has no manifest owner",
                    path,
                )
            )
        else:
            owned_sources[owner].append(path)
    if set(export_sets) != set(roots):
        return tuple(findings)
    for contract in contracts:
        actual, import_findings = _imported_dependencies(
            root,
            owned_sources[contract.project_name],
            contract,
            roots,
            export_sets,
        )
        findings.extend(import_findings)
        declared = set(contract.dependencies)
        if actual != declared:
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.DEPENDENCY_CLOSURE",
                    "manifest dependencies must equal direct production imports",
                    contract.manifest,
                    field="project.dependencies",
                    expected=",".join(sorted(actual)) or "-",
                    observed=",".join(sorted(declared)) or "-",
                )
            )
    return tuple(findings)


__all__ = (
    "PythonPackageContract",
    "PythonPackageFinding",
    "audit_python_packages",
    "resolve_public_exports",
)
