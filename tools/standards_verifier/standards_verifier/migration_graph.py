from __future__ import annotations

import csv
import io
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable

from .inventory import (
    DEPENDENCY_PATTERN,
    collect_inventory,
    repository_files,
)


MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"


GENERATED_ROOT = Path("evaluation/standards-effectiveness/generated")
NODE_OUTPUT_PATH = GENERATED_ROOT / "checker-dependency-nodes.tsv"
EDGE_OUTPUT_PATH = GENERATED_ROOT / "checker-dependency-edges.tsv"
COMPONENT_OUTPUT_PATH = GENERATED_ROOT / "checker-dependency-components.tsv"
GRAPH_OUTPUT_PATHS = (NODE_OUTPUT_PATH, EDGE_OUTPUT_PATH, COMPONENT_OUTPUT_PATH)

NODE_HEADER = (
    "node",
    "kind",
    "resolved",
    "component",
    "component_size",
    "cyclic",
    "wave",
    "executable_inbound_count",
    "contract_inbound_count",
    "dependency_inbound_count",
    "dependency_outbound_count",
)
EDGE_HEADER = ("edge_type", "source", "target")
COMPONENT_HEADER = (
    "component",
    "size",
    "cyclic",
    "wave",
    "members",
    "dependencies",
    "inbound_components",
    "executable_inbound_files",
    "contract_inbound_files",
)


@dataclass(frozen=True, slots=True)
class GraphDiagnostic(Exception):
    code: str
    status: str
    message: str
    exit_code: int
    path: str | None = None

    def __str__(self) -> str:
        location = f" (path={self.path})" if self.path is not None else ""
        return f"{self.code} [{self.status}]{location}: {self.message}"


@dataclass(frozen=True, slots=True, order=True)
class GraphEdge:
    edge_type: str
    source: str
    target: str


@dataclass(frozen=True, slots=True)
class GraphNode:
    path: str
    kind: str
    component: str
    component_size: int
    cyclic: bool
    wave: int
    executable_inbound_count: int
    contract_inbound_count: int
    dependency_inbound_count: int
    dependency_outbound_count: int


@dataclass(frozen=True, slots=True)
class GraphComponent:
    component: str
    members: tuple[str, ...]
    cyclic: bool
    wave: int
    dependencies: tuple[str, ...]
    inbound_components: tuple[str, ...]
    executable_inbound_files: tuple[str, ...]
    contract_inbound_files: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MigrationGraph:
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]
    components: tuple[GraphComponent, ...]


def _script_index(root: Path) -> dict[str, tuple[str, ...]]:
    paths: dict[str, list[str]] = defaultdict(list)
    for candidate in sorted(root.rglob("*.sh")):
        relative = candidate.relative_to(root)
        if not candidate.is_file() or ".git" in relative.parts:
            continue
        paths[candidate.name].append(relative.as_posix())
    return {name: tuple(matches) for name, matches in paths.items()}


def _resolve_dependency(
    source: str,
    name: str,
    script_index: dict[str, tuple[str, ...]],
) -> str:
    matches = script_index.get(name, ())
    if not matches:
        raise GraphDiagnostic(
            code="GRAPH.TARGET_UNAVAILABLE",
            status="unavailable",
            message=f"dependency target {name} is absent",
            exit_code=3,
            path=source,
        )
    if len(matches) != 1:
        raise GraphDiagnostic(
            code="GRAPH.TARGET_AMBIGUOUS",
            status="invalid",
            message=f"dependency target {name} resolves to {','.join(matches)}",
            exit_code=2,
            path=source,
        )
    return matches[0]


def _strong_components(
    nodes: tuple[str, ...],
    adjacency: dict[str, set[str]],
) -> tuple[tuple[str, ...], ...]:
    index = 0
    indexes: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[tuple[str, ...]] = []

    def visit(node: str) -> None:
        nonlocal index
        indexes[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for target in sorted(adjacency[node]):
            if target not in indexes:
                visit(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indexes[target])

        if lowlinks[node] != indexes[node]:
            return
        members: list[str] = []
        while True:
            member = stack.pop()
            on_stack.remove(member)
            members.append(member)
            if member == node:
                break
        components.append(tuple(sorted(members)))

    for node in nodes:
        if node not in indexes:
            visit(node)
    return tuple(sorted(components))


def _component_id(members: tuple[str, ...]) -> str:
    identity = "\0".join(members).encode("utf-8")
    return f"component-{sha256(identity).hexdigest()}"


def collect_migration_graph(root: Path) -> MigrationGraph:
    root = root.resolve()
    checker_records = collect_inventory(root)
    checker_paths = tuple(record.checker for record in checker_records)
    checker_set = set(checker_paths)
    script_index = _script_index(root)

    executable_nodes = set(checker_paths)
    dependency_edges: set[GraphEdge] = set()
    pending = deque(checker_paths)
    visited: set[str] = set()
    while pending:
        source = pending.popleft()
        if source in visited:
            continue
        visited.add(source)
        content = (root / source).read_text(encoding="utf-8")
        for match in DEPENDENCY_PATTERN.finditer(content):
            name = match.group("name")
            target = _resolve_dependency(source, name, script_index)
            edge_type = (
                "verifier_dependency"
                if name.startswith("verify-")
                else "helper_dependency"
            )
            dependency_edges.add(GraphEdge(edge_type, source, target))
            if target not in executable_nodes:
                executable_nodes.add(target)
                pending.append(target)

    reference_content: list[tuple[str, str, str]] = []
    for path in repository_files(root):
        content = path.read_text(encoding="utf-8")
        suffix = path.suffix
        if suffix in {".py", ".sh"}:
            reference_type = "executable_reference"
        elif suffix in {".toml", ".tsv"}:
            reference_type = "contract_reference"
        else:
            continue
        reference_content.append(
            (path.relative_to(root).as_posix(), reference_type, content)
        )

    reference_edges: set[GraphEdge] = set()
    for target in sorted(executable_nodes):
        basename = Path(target).name
        for source, edge_type, content in reference_content:
            if source != target and basename in content:
                reference_edges.add(GraphEdge(edge_type, source, target))

    edges = tuple(sorted(dependency_edges | reference_edges))
    nodes = tuple(sorted(executable_nodes))
    adjacency = {node: set() for node in nodes}
    for edge in dependency_edges:
        adjacency[edge.source].add(edge.target)

    raw_components = _strong_components(nodes, adjacency)
    component_by_node: dict[str, str] = {}
    members_by_component: dict[str, tuple[str, ...]] = {}
    for members in raw_components:
        component = _component_id(members)
        members_by_component[component] = members
        for member in members:
            component_by_node[member] = component

    dependencies: dict[str, set[str]] = {
        component: set() for component in members_by_component
    }
    inbound_components: dict[str, set[str]] = {
        component: set() for component in members_by_component
    }
    for edge in dependency_edges:
        source_component = component_by_node[edge.source]
        target_component = component_by_node[edge.target]
        if source_component == target_component:
            continue
        dependencies[source_component].add(target_component)
        inbound_components[target_component].add(source_component)

    waves: dict[str, int] = {}

    def wave_for(component: str) -> int:
        if component not in waves:
            waves[component] = (
                0
                if not dependencies[component]
                else 1 + max(wave_for(item) for item in dependencies[component])
            )
        return waves[component]

    for component in sorted(members_by_component):
        wave_for(component)

    executable_inbound: dict[str, set[str]] = defaultdict(set)
    contract_inbound: dict[str, set[str]] = defaultdict(set)
    dependency_inbound: dict[str, int] = defaultdict(int)
    dependency_outbound: dict[str, int] = defaultdict(int)
    for edge in edges:
        if edge.edge_type == "executable_reference":
            executable_inbound[edge.target].add(edge.source)
        elif edge.edge_type == "contract_reference":
            contract_inbound[edge.target].add(edge.source)
        else:
            dependency_inbound[edge.target] += 1
            dependency_outbound[edge.source] += 1

    graph_components: list[GraphComponent] = []
    cyclic_by_component: dict[str, bool] = {}
    for component, members in sorted(members_by_component.items()):
        cyclic = len(members) > 1 or any(
            member in adjacency[member] for member in members
        )
        cyclic_by_component[component] = cyclic
        graph_components.append(
            GraphComponent(
                component=component,
                members=members,
                cyclic=cyclic,
                wave=waves[component],
                dependencies=tuple(sorted(dependencies[component])),
                inbound_components=tuple(sorted(inbound_components[component])),
                executable_inbound_files=tuple(
                    sorted(
                        {
                            source
                            for member in members
                            for source in executable_inbound[member]
                            if source not in members
                        }
                    )
                ),
                contract_inbound_files=tuple(
                    sorted(
                        {
                            source
                            for member in members
                            for source in contract_inbound[member]
                        }
                    )
                ),
            )
        )

    graph_nodes = tuple(
        GraphNode(
            path=node,
            kind="verifier" if node in checker_set else "helper",
            component=component_by_node[node],
            component_size=len(members_by_component[component_by_node[node]]),
            cyclic=cyclic_by_component[component_by_node[node]],
            wave=waves[component_by_node[node]],
            executable_inbound_count=len(executable_inbound[node]),
            contract_inbound_count=len(contract_inbound[node]),
            dependency_inbound_count=dependency_inbound[node],
            dependency_outbound_count=dependency_outbound[node],
        )
        for node in nodes
    )
    return MigrationGraph(
        nodes=graph_nodes,
        edges=edges,
        components=tuple(graph_components),
    )


def _render(header: tuple[str, ...], rows: Iterable[tuple[object, ...]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return output.getvalue()


def _render_list(values: tuple[str, ...]) -> str:
    return ",".join(values) if values else "-"


def render_nodes(graph: MigrationGraph) -> str:
    return _render(
        NODE_HEADER,
        (
            (
                node.path,
                node.kind,
                "yes",
                node.component,
                node.component_size,
                "yes" if node.cyclic else "no",
                node.wave,
                node.executable_inbound_count,
                node.contract_inbound_count,
                node.dependency_inbound_count,
                node.dependency_outbound_count,
            )
            for node in graph.nodes
        ),
    )


def render_edges(graph: MigrationGraph) -> str:
    return _render(
        EDGE_HEADER,
        ((edge.edge_type, edge.source, edge.target) for edge in graph.edges),
    )


def render_components(graph: MigrationGraph) -> str:
    return _render(
        COMPONENT_HEADER,
        (
            (
                component.component,
                len(component.members),
                "yes" if component.cyclic else "no",
                component.wave,
                _render_list(component.members),
                _render_list(component.dependencies),
                _render_list(component.inbound_components),
                _render_list(component.executable_inbound_files),
                _render_list(component.contract_inbound_files),
            )
            for component in graph.components
        ),
    )


def expected_graph_outputs(root: Path) -> dict[Path, str]:
    graph = collect_migration_graph(root)
    return {
        NODE_OUTPUT_PATH: render_nodes(graph),
        EDGE_OUTPUT_PATH: render_edges(graph),
        COMPONENT_OUTPUT_PATH: render_components(graph),
    }


def _validate_tsv(
    path: Path,
    display_path: Path,
    expected_header: tuple[str, ...],
) -> None:
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.reader(stream, delimiter="\t"))
    except UnicodeDecodeError as error:
        raise GraphDiagnostic(
            code="GRAPH.ARTIFACT_INVALID",
            status="invalid",
            message="generated graph is not UTF-8",
            exit_code=2,
            path=display_path.as_posix(),
        ) from error
    if not rows or tuple(rows[0]) != expected_header:
        raise GraphDiagnostic(
            code="GRAPH.ARTIFACT_INVALID",
            status="invalid",
            message="generated graph header is invalid",
            exit_code=2,
            path=display_path.as_posix(),
        )
    if any(len(row) != len(expected_header) for row in rows[1:]):
        raise GraphDiagnostic(
            code="GRAPH.ARTIFACT_INVALID",
            status="invalid",
            message="generated graph row width is invalid",
            exit_code=2,
            path=display_path.as_posix(),
        )


def check_graph(
    root: Path,
    *,
    output: Callable[[str], None] = print,
) -> int:
    root = root.resolve()
    try:
        expected = expected_graph_outputs(root)
        headers = {
            NODE_OUTPUT_PATH: NODE_HEADER,
            EDGE_OUTPUT_PATH: EDGE_HEADER,
            COMPONENT_OUTPUT_PATH: COMPONENT_HEADER,
        }
        for relative, content in expected.items():
            target = root / relative
            if not target.is_file():
                raise GraphDiagnostic(
                    code="GRAPH.ARTIFACT_UNAVAILABLE",
                    status="unavailable",
                    message="generated graph artifact is absent",
                    exit_code=3,
                    path=relative.as_posix(),
                )
            _validate_tsv(target, relative, headers[relative])
            if target.read_text(encoding="utf-8") != content:
                raise GraphDiagnostic(
                    code="GRAPH.ARTIFACT_STALE",
                    status="invalid",
                    message="generated graph does not match repository inputs",
                    exit_code=1,
                    path=relative.as_posix(),
                )
    except GraphDiagnostic as diagnostic:
        output(str(diagnostic))
        return diagnostic.exit_code
    graph = collect_migration_graph(root)
    output(
        f"PASS checker-dependency-graph "
        f"({len(graph.nodes)} nodes, {len(graph.edges)} edges, "
        f"{len(graph.components)} components)"
    )
    return 0


def write_graph(root: Path) -> int:
    root = root.resolve()
    try:
        outputs = expected_graph_outputs(root)
    except GraphDiagnostic as diagnostic:
        print(diagnostic)
        return diagnostic.exit_code
    for relative, content in outputs.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    graph = collect_migration_graph(root)
    print(
        f"WROTE checker-dependency-graph "
        f"({len(graph.nodes)} nodes, {len(graph.edges)} edges, "
        f"{len(graph.components)} components)"
    )
    return 0
