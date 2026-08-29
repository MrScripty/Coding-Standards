from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

from tools.standards_authority.standards_authority import (
    GitIndexError,
    git_output,
    indexed_paths,
    materialize_index,
)


_PYTHON_RANGE = ">=3.11,<3.13"
_DEPENDENCY_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_IMPORT_MACHINERY_ROOTS = frozenset(
    {
        "_frozen_importlib",
        "_frozen_importlib_external",
        "_imp",
        "builtins",
        "importlib",
        "pkgutil",
        "runpy",
        "zipimport",
    }
)
_IMPORT_CAPABILITY_NAMES = frozenset({"__import__", "eval", "exec"})
_IMPORT_CAPABILITY_ATTRIBUTES = frozenset(
    {
        "__import__",
        "exec_module",
        "find_spec",
        "import_module",
        "load_module",
        "module_from_spec",
        "resolve_name",
        "run_module",
        "run_path",
        "spec_from_file_location",
        "spec_from_loader",
    }
)


@dataclass(frozen=True, slots=True)
class PythonPackageFinding:
    code: str
    message: str
    path: str
    field: str | None = None
    expected: str | None = None
    observed: str | None = None


@dataclass(frozen=True, slots=True)
class EntrypointContract:
    path: str
    arguments: tuple[str, ...]
    fixture: str
    remove: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PythonPackageContract:
    manifest: str
    project_name: str
    dependencies: tuple[str, ...]
    public_root: str
    entrypoints: tuple[EntrypointContract, ...]

    @property
    def root_path(self) -> PurePosixPath:
        return PurePosixPath(*self.public_root.split("."))


def _dependency_name(requirement: str) -> str:
    match = _DEPENDENCY_NAME.match(requirement)
    if match is None:
        return ""
    return match.group(0).lower().replace("_", "-")


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
    if package.get("schema-version") != 2:
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.SCHEMA_VERSION",
                "standards-package schema-version must equal integer 2",
                manifest,
                field="schema-version",
                expected="2",
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
    parsed_entrypoints = _entrypoint_contracts(entrypoints)
    if parsed_entrypoints is None:
        findings.append(
            PythonPackageFinding(
                "PYTHON_PACKAGE.ENTRYPOINTS",
                "repository-entrypoints must be unique typed smoke operations",
                manifest,
                field="repository-entrypoints",
            )
        )
        parsed_entrypoints = ()
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
            parsed_entrypoints,
        ),
        [],
    )


def _entrypoint_contracts(value: object) -> tuple[EntrypointContract, ...] | None:
    if not isinstance(value, list):
        return None
    result: list[EntrypointContract] = []
    for item in value:
        if not isinstance(item, dict) or set(item) != {
            "path",
            "arguments",
            "fixture",
            "remove",
        }:
            return None
        path = item["path"]
        arguments = item["arguments"]
        fixture = item["fixture"]
        remove = item["remove"]
        if (
            type(path) is not str
            or not path
            or not _is_repository_path(path)
            or not isinstance(arguments, list)
            or any(type(argument) is not str or not argument for argument in arguments)
            or fixture
            not in {
                "reviewed-repository",
                "isolated-indexed-copy",
                "isolated-git-repository",
            }
            or not isinstance(remove, list)
            or any(type(selected) is not str or not selected for selected in remove)
            or any(not _is_repository_path(selected) for selected in remove)
            or len(set(remove)) != len(remove)
        ):
            return None
        result.append(
            EntrypointContract(path, tuple(arguments), fixture, tuple(sorted(remove)))
        )
    paths = tuple(item.path for item in result)
    if len(set(paths)) != len(paths):
        return None
    return tuple(result)


def _is_repository_path(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and bool(path.parts)
        and not any(part in {"", ".", ".."} for part in path.parts)
    )


def _local_module_path(package_file: Path, module: str | None) -> Path:
    base = package_file.parent
    if module:
        base = base.joinpath(*module.split("."))
    candidate = base.with_suffix(".py")
    if candidate.is_file():
        return candidate
    return base / "__init__.py"


def resolve_public_exports(
    root: Path, contract: PythonPackageContract
) -> tuple[str, ...]:
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
            if isinstance(node, (ast.Assign, ast.AnnAssign)) and (
                any(
                    isinstance(target, ast.Name) and target.id == "__all__"
                    for target in node.targets
                )
                if isinstance(node, ast.Assign)
                else isinstance(node.target, ast.Name) and node.target.id == "__all__"
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
        if _uses_dynamic_import_capability(tree):
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.DYNAMIC_IMPORT",
                    "production sources cannot bypass static import ownership",
                    path,
                )
            )
        for node in ast.walk(tree):
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
                elif (
                    top_level not in sys.stdlib_module_names
                    and top_level != "__future__"
                ):
                    dependencies.add(top_level.lower().replace("_", "-"))
    return dependencies, findings


def _constant_text(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and type(node.value) is str:
        return node.value
    return None


@dataclass(frozen=True, slots=True, order=True)
class _BindingEvent:
    order: int
    source_position: tuple[int, int]
    context: tuple[int, ...]
    bound: bool
    provenance: str


class _ScopeFacts(ast.NodeVisitor):
    def __init__(self) -> None:
        self.bindings: set[str] = set()
        self.events: dict[str, list[_BindingEvent]] = {}
        self.nonlocal_names: set[str] = set()
        self.positions: dict[int, int] = {}
        self.contexts: dict[int, tuple[int, ...]] = {}
        self._order = 0
        self._context: tuple[int, ...] = ()
        self._next_context = 0

    @staticmethod
    def _source_position(node: ast.AST) -> tuple[int, int]:
        return (
            getattr(node, "end_lineno", getattr(node, "lineno", 0)),
            getattr(node, "end_col_offset", getattr(node, "col_offset", 0)),
        )

    def _mark(self, node: ast.AST) -> None:
        self._order += 1
        self.positions[id(node)] = self._order
        self.contexts[id(node)] = self._context

    def visit(self, node: ast.AST) -> object:
        self._mark(node)
        return super().visit(node)

    def _visit_branch(self, children: Iterable[ast.AST]) -> tuple[int, ...]:
        self._next_context += 1
        previous = self._context
        self._context = (*previous, self._next_context)
        branch = self._context
        for child in children:
            self.visit(child)
        self._context = previous
        return branch

    def _branch_state(self, context: tuple[int, ...]) -> dict[str, _BindingEvent]:
        return {
            name: matching[-1]
            for name, events in self.events.items()
            if (
                matching := tuple(event for event in events if event.context == context)
            )
        }

    def _visible_state(self) -> dict[str, _BindingEvent]:
        return {
            name: matching[-1]
            for name, events in self.events.items()
            if (
                matching := tuple(
                    event
                    for event in events
                    if self._context[: len(event.context)] == event.context
                )
            )
        }

    def _join_branch_states(
        self,
        node: ast.AST,
        before: dict[str, _BindingEvent],
        contexts: Iterable[tuple[int, ...]],
        *,
        include_unchanged_path: bool = False,
    ) -> None:
        branch_states = [self._branch_state(context) for context in contexts]
        if include_unchanged_path:
            branch_states.append({})
        changed_names = set().union(*(state.keys() for state in branch_states))
        for name in sorted(changed_names):
            candidates = tuple(
                state.get(name, before.get(name)) for state in branch_states
            )
            definitely_bound = all(
                candidate is not None and candidate.bound for candidate in candidates
            )
            may_be_sys = any(
                candidate is not None and candidate.provenance == "sys"
                for candidate in candidates
            )
            self._event(
                name,
                node,
                bound=definitely_bound,
                provenance="sys" if may_be_sys else "other",
            )

    def _event(
        self,
        name: str,
        node: ast.AST,
        *,
        bound: bool,
        provenance: str = "other",
    ) -> None:
        self._order += 1
        self.bindings.add(name)
        self.events.setdefault(name, []).append(
            _BindingEvent(
                self._order,
                self._source_position(node),
                self._context,
                bound,
                provenance,
            )
        )

    def _bind(
        self,
        name: str,
        node: ast.AST,
        provenance: str = "other",
    ) -> None:
        self._event(
            name,
            node,
            bound=True,
            provenance=provenance,
        )

    def _value_provenance(self, node: ast.AST) -> str:
        if not isinstance(node, ast.Name):
            return "other"
        use_order = self.positions.get(id(node), self._order + 1)
        use_context = self.contexts.get(id(node), self._context)
        selected = tuple(
            event
            for event in self.events.get(node.id, ())
            if event.order < use_order
            and use_context[: len(event.context)] == event.context
        )
        if selected:
            latest = selected[-1]
            return latest.provenance if latest.bound else "other"
        return "sys" if node.id == "sys" else "other"

    def _target(
        self,
        node: ast.AST,
        *,
        bound: bool,
        provenance: str = "other",
    ) -> None:
        self._mark(node)
        if isinstance(node, ast.Name):
            self._event(
                node.id,
                node,
                bound=bound,
                provenance=provenance,
            )
        elif isinstance(node, ast.Starred):
            self._target(node.value, bound=bound, provenance=provenance)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for item in node.elts:
                self._target(item, bound=bound, provenance=provenance)
        elif isinstance(node, ast.Attribute):
            self.visit(node.value)
        elif isinstance(node, ast.Subscript):
            self.visit(node.value)
            self.visit(node.slice)

    def visit_Name(self, node: ast.Name) -> None:
        del node

    def visit_arg(self, node: ast.arg) -> None:
        self._bind(node.arg, node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for child in (
            *node.decorator_list,
            *node.args.defaults,
            *(item for item in node.args.kw_defaults if item is not None),
        ):
            self.visit(child)
        if node.returns is not None:
            self.visit(node.returns)
        self._bind(node.name, node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for child in (*node.decorator_list, *node.bases, *node.keywords):
            self.visit(child)
        self._bind(node.name, node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        for child in (
            *node.args.defaults,
            *(item for item in node.args.kw_defaults if item is not None),
        ):
            self.visit(child)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        del node

    visit_SetComp = visit_ListComp
    visit_DictComp = visit_ListComp
    visit_GeneratorExp = visit_ListComp

    def visit_Assign(self, node: ast.Assign) -> None:
        self.visit(node.value)
        provenance = self._value_provenance(node.value)
        for target in node.targets:
            self._target(target, bound=True, provenance=provenance)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.visit(node.annotation)
        if node.value is not None:
            self.visit(node.value)
        provenance = (
            self._value_provenance(node.value)
            if node.value is not None
            else "other"
        )
        self._target(node.target, bound=True, provenance=provenance)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.visit(node.target)
        self.visit(node.value)
        self._target(node.target, bound=True)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.visit(node.value)
        self._target(
            node.target,
            bound=True,
            provenance=self._value_provenance(node.value),
        )

    def visit_Delete(self, node: ast.Delete) -> None:
        for target in node.targets:
            self._target(target, bound=False)

    def visit_If(self, node: ast.If) -> None:
        self.visit(node.test)
        before = self._visible_state()
        body_context = self._visit_branch(node.body)
        else_context = self._visit_branch(node.orelse)
        self._join_branch_states(node, before, (body_context, else_context))

    def visit_While(self, node: ast.While) -> None:
        self.visit(node.test)
        before = self._visible_state()
        body_context = self._visit_branch(node.body)
        else_context = self._visit_branch(node.orelse)
        self._join_branch_states(
            node,
            before,
            (body_context, else_context),
            include_unchanged_path=True,
        )

    def visit_For(self, node: ast.For) -> None:
        self.visit(node.iter)
        before = self._visible_state()
        self._next_context += 1
        previous = self._context
        self._context = (*previous, self._next_context)
        body_context = self._context
        self._target(node.target, bound=True)
        for child in node.body:
            self.visit(child)
        self._context = previous
        else_context = self._visit_branch(node.orelse)
        self._join_branch_states(
            node,
            before,
            (body_context, else_context),
            include_unchanged_path=True,
        )

    visit_AsyncFor = visit_For

    def visit_With(self, node: ast.With) -> None:
        for item in node.items:
            self.visit(item.context_expr)
            if item.optional_vars is not None:
                self._target(
                    item.optional_vars,
                    bound=True,
                )
        for child in node.body:
            self.visit(child)

    visit_AsyncWith = visit_With

    def visit_Try(self, node: ast.Try) -> None:
        before = self._visible_state()
        contexts = [self._visit_branch(node.body)]
        contexts.extend(self._visit_branch((handler,)) for handler in node.handlers)
        contexts.append(self._visit_branch(node.orelse))
        self._join_branch_states(
            node,
            before,
            contexts,
            include_unchanged_path=True,
        )
        for child in node.finalbody:
            self.visit(child)

    visit_TryStar = visit_Try

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is not None:
            self.visit(node.type)
        if node.name is not None:
            self._event(
                node.name,
                node,
                bound=True,
            )
        for child in node.body:
            self.visit(child)
        if node.name is not None:
            self._event(node.name, node, bound=False)

    def visit_Import(self, node: ast.Import) -> None:
        for item in node.names:
            name = item.asname or item.name.split(".", 1)[0]
            self._bind(
                name,
                node,
                "sys" if item.name == "sys" else "other",
            )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for item in node.names:
            self._bind(item.asname or item.name, node)

    def visit_Global(self, node: ast.Global) -> None:
        self.nonlocal_names.update(node.names)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        self.nonlocal_names.update(node.names)


def _scope_facts(
    node: ast.AST,
) -> tuple[
    frozenset[str],
    dict[str, tuple[_BindingEvent, ...]],
    dict[int, int],
    dict[int, tuple[int, ...]],
]:
    collector = _ScopeFacts()
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        collector.visit(node.args)
        body = node.body if not isinstance(node, ast.Lambda) else (node.body,)
    else:
        body = getattr(node, "body", ())
    for child in body:
        collector.visit(child)
    bindings = frozenset(collector.bindings - collector.nonlocal_names)
    return (
        bindings,
        {
            name: tuple(sorted(events))
            for name, events in collector.events.items()
            if name in bindings
        },
        collector.positions,
        collector.contexts,
    )


class _DynamicImportProfile(ast.NodeVisitor):
    def __init__(self, tree: ast.Module) -> None:
        self.detected = False
        bindings, events, positions, contexts = _scope_facts(tree)
        self._scopes = [bindings]
        self._events = [events]
        self._positions = [positions]
        self._contexts = [contexts]
        self._scope_kinds = ["module"]

    @staticmethod
    def _source_position(node: ast.AST) -> tuple[int, int]:
        return getattr(node, "lineno", 0), getattr(node, "col_offset", 0)

    def _latest_event(
        self,
        index: int,
        name: str,
        node: ast.AST,
    ) -> _BindingEvent | None:
        events = self._events[index].get(name, ())
        current = len(self._scopes) - 1
        if index == current:
            position = self._positions[index].get(id(node))
            if position is None:
                return None
            context = self._contexts[index].get(id(node), ())
            selected = tuple(
                event
                for event in events
                if event.order < position
                and context[: len(event.context)] == event.context
            )
        else:
            source_position = self._source_position(node)
            selected = tuple(
                event
                for event in events
                if not event.context and event.source_position < source_position
            )
        return selected[-1] if selected else None

    def _shadowed(self, name: str, node: ast.AST) -> bool:
        current = len(self._scopes) - 1
        for index in range(current, -1, -1):
            kind = self._scope_kinds[index]
            if kind == "class" and index != current:
                continue
            bindings = self._scopes[index]
            if name not in bindings:
                continue
            if kind in {"function", "comprehension"}:
                return True
            selected = self._latest_event(index, name, node)
            if selected is not None and selected.bound:
                return True
        return False

    def _is_sys_alias(self, name: str, node: ast.AST) -> bool:
        current = len(self._scopes) - 1
        for index in range(current, -1, -1):
            kind = self._scope_kinds[index]
            if kind == "class" and index != current:
                continue
            bindings = self._scopes[index]
            if name not in bindings:
                continue
            if kind == "function" and index != current:
                return any(
                    event.provenance == "sys"
                    for event in self._events[index].get(name, ())
                )
            selected = self._latest_event(index, name, node)
            if selected is not None:
                if selected.provenance == "sys":
                    return True
                if selected.bound:
                    cutoff = selected.order
                else:
                    cutoff = selected.order
                if kind == "class":
                    continue
            else:
                cutoff = 0
            if index == current:
                position = self._positions[index].get(id(node))
                context = self._contexts[index].get(id(node), ())
                if position is not None and any(
                    event.bound
                    and event.provenance == "sys"
                    and cutoff < event.order < position
                    and (
                        context[: len(event.context)] == event.context
                        or event.context[: len(context)] == context
                    )
                    for event in self._events[index].get(name, ())
                ):
                    return True
            if kind != "class":
                return False
        return False

    def _known_source(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return node.id == "__builtins__" and not self._shadowed(node.id, node)
        if isinstance(node, ast.Attribute):
            return (
                node.attr == "modules"
                and isinstance(node.value, ast.Name)
                and self._is_sys_alias(node.value.id, node.value)
            )
        if isinstance(node, ast.Subscript):
            return self._known_source(node.value)
        return False

    def _visit_scope(self, node: ast.AST, children: Iterable[ast.AST]) -> None:
        bindings, events, positions, contexts = _scope_facts(node)
        self._scopes.append(bindings)
        self._events.append(events)
        self._positions.append(positions)
        self._contexts.append(contexts)
        self._scope_kinds.append(
            "function"
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
            else "class"
        )
        for child in children:
            self.visit(child)
        self._scope_kinds.pop()
        self._contexts.pop()
        self._positions.pop()
        self._events.pop()
        self._scopes.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for child in (
            *node.decorator_list,
            *node.args.defaults,
            *(item for item in node.args.kw_defaults if item is not None),
        ):
            self.visit(child)
        if node.returns is not None:
            self.visit(node.returns)
        self._visit_scope(node, node.body)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for child in (*node.decorator_list, *node.bases, *node.keywords):
            self.visit(child)
        self._visit_scope(node, node.body)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        for child in (
            *node.args.defaults,
            *(item for item in node.args.kw_defaults if item is not None),
        ):
            self.visit(child)
        self._visit_scope(node, (node.body,))

    def _visit_comprehension(
        self,
        node: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp,
        result_nodes: Iterable[ast.AST],
    ) -> None:
        first, *remaining = node.generators
        self.visit(first.iter)
        bindings = {
            name.id
            for name in ast.walk(first.target)
            if isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store)
        }
        events: dict[str, tuple[_BindingEvent, ...]] = {}
        self._scopes.append(frozenset(bindings))
        self._events.append(events)
        self._positions.append({})
        self._contexts.append({})
        self._scope_kinds.append("comprehension")
        for condition in first.ifs:
            self.visit(condition)
        for generator in remaining:
            self.visit(generator.iter)
            added = {
                name.id
                for name in ast.walk(generator.target)
                if isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store)
            }
            bindings.update(added)
            self._scopes[-1] = frozenset(bindings)
            for condition in generator.ifs:
                self.visit(condition)
        for result in result_nodes:
            self.visit(result)
        self._scope_kinds.pop()
        self._contexts.pop()
        self._positions.pop()
        self._events.pop()
        self._scopes.pop()

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node, (node.elt,))

    visit_SetComp = visit_ListComp
    visit_GeneratorExp = visit_ListComp

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node, (node.key, node.value))

    def visit_Import(self, node: ast.Import) -> None:
        if any(
            item.name.split(".", 1)[0] in _IMPORT_MACHINERY_ROOTS
            for item in node.names
        ):
            self.detected = True

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.module.split(".", 1)[0] in _IMPORT_MACHINERY_ROOTS:
            self.detected = True
        if node.module == "sys" and any(item.name == "modules" for item in node.names):
            self.detected = True

    def visit_Name(self, node: ast.Name) -> None:
        if (
            isinstance(node.ctx, ast.Load)
            and node.id in _IMPORT_CAPABILITY_NAMES
            and not self._shadowed(node.id, node)
        ):
            self.detected = True

    def visit_Call(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "getattr"
            and not self._shadowed("getattr", node.func)
            and len(node.args) >= 2
            and self._known_source(node.args[0])
            and _constant_text(node.args[1])
            in _IMPORT_CAPABILITY_ATTRIBUTES | {"__builtins__"}
        ):
            self.detected = True
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr == "modules" and self._known_source(node):
            self.detected = True
        elif (
            node.attr in _IMPORT_CAPABILITY_ATTRIBUTES
            and self._known_source(node.value)
        ):
            self.detected = True
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        if (
            _constant_text(node.slice)
            in _IMPORT_CAPABILITY_ATTRIBUTES | {"__builtins__"}
            and self._known_source(node.value)
        ):
            self.detected = True
        self.generic_visit(node)


def _uses_dynamic_import_capability(tree: ast.AST) -> bool:
    if not isinstance(tree, ast.Module):
        raise TypeError("dynamic import profile requires a Python module")
    profile = _DynamicImportProfile(tree)
    profile.visit(tree)
    return profile.detected


def audit_python_packages(root: Path) -> tuple[PythonPackageFinding, ...]:
    root = root.resolve()
    try:
        indexed = indexed_paths(root)
    except GitIndexError as error:
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
    entrypoints = [
        entrypoint.path for item in contracts for entrypoint in item.entrypoints
    ]
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
        entrypoint.path: contract.project_name
        for contract in contracts
        for entrypoint in contract.entrypoints
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


def python_package_authority_paths(root: Path) -> tuple[str, ...]:
    repository = root.resolve()
    indexed = indexed_paths(repository)
    selected = {
        path
        for path in indexed
        if path.startswith("tools/")
        and "tests" not in PurePosixPath(path).parts
        and (path.endswith(".py") or path.endswith("/pyproject.toml"))
    }
    for manifest in tuple(
        path for path in selected if path.endswith("/pyproject.toml")
    ):
        contract, findings = _load_contract(repository, manifest)
        if findings or contract is None:
            continue
        selected.update(item.path for item in contract.entrypoints)
        selected.update(path for item in contract.entrypoints for path in item.remove)
    return tuple(sorted(selected))


def execute_python_package_contract(
    root: Path, *, python_executable: Path | None = None
) -> tuple[PythonPackageFinding, ...]:
    repository = root.resolve()
    executable = (python_executable or Path(sys.executable)).absolute()
    try:
        indexed = indexed_paths(repository)
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
        if path.startswith("tools/") and path.endswith("/pyproject.toml")
    )
    contracts: list[PythonPackageContract] = []
    findings: list[PythonPackageFinding] = []
    for manifest in manifests:
        contract, contract_findings = _load_contract(repository, manifest)
        findings.extend(contract_findings)
        if contract is not None:
            contracts.append(contract)
    if findings:
        return tuple(findings)

    environment = {
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(repository),
    }
    for contract in sorted(contracts, key=lambda item: item.project_name):
        try:
            exports = resolve_public_exports(repository, contract)
        except (OSError, SyntaxError, UnicodeError, ValueError) as error:
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.EXPORT_CONTRACT",
                    str(error),
                    contract.manifest,
                )
            )
            continue
        script = (
            "import importlib; "
            f"module=importlib.import_module({json.dumps(contract.public_root)}); "
            f"[getattr(module, name) for name in {exports!r}]"
        )
        completed = subprocess.run(
            (str(executable), "-P", "-c", script),
            cwd=tempfile.gettempdir(),
            env=environment,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            findings.append(
                PythonPackageFinding(
                    "PYTHON_PACKAGE.PUBLIC_EXECUTION",
                    "public root or export failed in safe-path isolation",
                    contract.manifest,
                    observed=(completed.stderr or completed.stdout).strip(),
                )
            )
        for entrypoint in contract.entrypoints:
            try:
                completed = _execute_entrypoint(
                    repository, executable, environment, entrypoint
                )
            except (
                OSError,
                RuntimeError,
                ValueError,
                subprocess.SubprocessError,
            ) as error:
                findings.append(
                    PythonPackageFinding(
                        "PYTHON_PACKAGE.ENTRYPOINT_FIXTURE",
                        f"repository entrypoint fixture cannot be constructed: {error}",
                        entrypoint.path,
                    )
                )
                continue
            if completed.returncode != 0:
                findings.append(
                    PythonPackageFinding(
                        "PYTHON_PACKAGE.ENTRYPOINT_EXECUTION",
                        "repository entrypoint failed in safe-path isolation",
                        entrypoint.path,
                        observed=(completed.stderr or completed.stdout).strip(),
                    )
                )
            elif not completed.stdout.strip():
                findings.append(
                    PythonPackageFinding(
                        "PYTHON_PACKAGE.ENTRYPOINT_OUTPUT",
                        "repository entrypoint smoke operation produced no evidence",
                        entrypoint.path,
                    )
                )
    return tuple(findings)


def _execute_entrypoint(
    repository: Path,
    executable: Path,
    environment: dict[str, str],
    contract: EntrypointContract,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temporary:
        fixture = Path(temporary) / "fixture"
        replacements = {"{repository}": str(repository)}
        if contract.fixture == "isolated-indexed-copy":
            fixture.mkdir()
            materialize_index(repository, fixture)
            git_output(fixture, ("init", "-q"))
            git_output(fixture, ("add", "-A"))
            for selected in contract.remove:
                target = fixture.joinpath(*PurePosixPath(selected).parts)
                if not target.is_file():
                    raise ValueError(
                        f"entrypoint fixture removal is unavailable: {selected}"
                    )
                target.unlink()
            replacements["{fixture}"] = str(fixture)
        elif contract.fixture == "isolated-git-repository":
            if contract.remove:
                raise ValueError("Git entrypoint fixtures cannot remove files")
            fixture.mkdir()
            git_output(fixture, ("init", "-q", "-b", "main"))
            git_output(
                fixture, ("config", "user.email", "fixture@example.invalid")
            )
            git_output(fixture, ("config", "user.name", "Fixture"))
            (fixture / "content.txt").write_text("fixture\n", encoding="utf-8")
            git_output(fixture, ("add", "content.txt"))
            git_output(fixture, ("commit", "-q", "-m", "fixture"))
            oid = git_output(fixture, ("rev-parse", "HEAD")).decode("ascii").strip()
            manifest = fixture / "manifest.tsv"
            manifest.write_text(
                "oid\tcommit_disposition\treference\tauthority\n"
                f"{oid}\tretained\trefs/heads/main\tnone\n",
                encoding="utf-8",
            )
            replacements.update(
                {"{fixture}": str(fixture), "{manifest}": manifest.name}
            )
        elif contract.remove:
            raise ValueError("reviewed entrypoint fixtures cannot remove files")
        arguments = tuple(
            replacements.get(argument, argument) for argument in contract.arguments
        )
        if any(
            argument.startswith("{") and argument.endswith("}")
            for argument in arguments
        ):
            raise ValueError("entrypoint contract contains an unknown placeholder")
        return subprocess.run(
            (str(executable), "-P", str(repository / contract.path), *arguments),
            cwd=tempfile.gettempdir(),
            env=environment,
            capture_output=True,
            text=True,
        )


__all__ = (
    "PythonPackageContract",
    "EntrypointContract",
    "PythonPackageFinding",
    "audit_python_packages",
    "python_package_authority_paths",
    "resolve_public_exports",
)
