from __future__ import annotations

import heapq
from collections import deque
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Iterable, Mapping

from .errors import (
    AliasConflictError,
    ForbiddenTraversalError,
    InvalidEdgeError,
    InvalidGroupError,
    InvalidSourceError,
    UnknownEdgeError,
    UnknownGroupError,
    UnknownNodeError,
)
from .model import Direction, Edge, EdgeGroup, EdgeSource, Node
from .paths import contained_path


@dataclass(frozen=True, slots=True)
class EdgeView:
    edge: Edge
    direction: Direction
    opposite: str


@dataclass(frozen=True, slots=True)
class TraversalStep:
    edge: Edge
    direction: Direction
    from_node: str
    to_node: str
    path_nodes: tuple[str, ...]
    path_edges: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TraversalResult:
    start: str | None
    nodes: tuple[str, ...]
    edges: tuple[str, ...]
    steps: tuple[TraversalStep, ...]


class EdgeRegistry:
    """Immutable index assembled only from explicitly registered sources."""

    def __init__(self, repo_root: Path, sources: Iterable[EdgeSource]) -> None:
        self.repo_root = repo_root.resolve()
        selected_sources = tuple(sources)
        source_ids = [source.id for source in selected_sources]
        if any(not isinstance(source_id, str) or not source_id for source_id in source_ids):
            raise InvalidSourceError("registered source IDs must be non-empty strings")
        if len(set(source_ids)) != len(source_ids):
            raise InvalidSourceError("registered source IDs must be unique")

        nodes: dict[str, Node] = {}
        groups: dict[str, EdgeGroup] = {}
        edges: dict[str, Edge] = {}
        aliases: dict[str, str] = {}
        physical_aliases: dict[Path, str] = {}
        for source in selected_sources:
            contribution = source.load()
            if not hasattr(contribution, "nodes") or not hasattr(contribution, "groups") or not hasattr(contribution, "edges"):
                raise InvalidSourceError(
                    "registered provider returned an invalid graph contribution",
                    source=source.id,
                )
            source_node_ids: set[str] = set()
            for node in contribution.nodes:
                if node.provenance is not None and node.provenance.source_id != source.id:
                    raise InvalidSourceError(
                        "node provenance does not match its registered source",
                        source=source.id,
                        node=node.id,
                    )
                if node.id in source_node_ids:
                    raise AliasConflictError(
                        "canonical node ID is duplicated within one source",
                        node=node.id,
                        source=source.id,
                    )
                source_node_ids.add(node.id)
                previous = nodes.get(node.id)
                nodes[node.id] = node if previous is None else self._merge_node(previous, node)
            for group in contribution.groups:
                if group.provenance.source_id != source.id:
                    raise InvalidSourceError(
                        "group provenance does not match its registered source",
                        source=source.id,
                        group=group.id,
                    )
                if group.id in groups:
                    raise InvalidGroupError("group ID is duplicated", group=group.id)
                groups[group.id] = group
            for edge in contribution.edges:
                if edge.provenance.source_id != source.id:
                    raise InvalidSourceError(
                        "edge provenance does not match its registered source",
                        source=source.id,
                        edge=edge.id,
                    )
                if edge.id in edges:
                    raise InvalidEdgeError("edge ID is duplicated", edge=edge.id)
                edges[edge.id] = edge

        for node in nodes.values():
            self._register_alias(aliases, node.id, node.id, node.id)
            for alias in (node.id, *node.aliases):
                self._register_alias(aliases, alias, node.id, node.id)
                physical = self._artifact_identity(alias)
                if physical is not None:
                    previous = physical_aliases.get(physical)
                    if previous is not None and previous != node.id:
                        raise AliasConflictError(
                            "two canonical nodes identify the same repository artifact",
                            alias=alias,
                            node=node.id,
                            previous=previous,
                        )
                    physical_aliases[physical] = node.id

        for alias, canonical in aliases.items():
            if alias in nodes and alias != canonical:
                raise AliasConflictError(
                    "alias contradicts a canonical node ID",
                    alias=alias,
                    node=canonical,
                )
        for edge in edges.values():
            if edge.source not in nodes or edge.target not in nodes:
                source_missing = edge.source not in nodes
                missing = edge.source if source_missing else edge.target
                raise InvalidEdgeError(
                    "edge endpoint is not registered",
                    edge=edge.id,
                    node=missing,
                    endpoint="source" if source_missing else "target",
                )
            unknown_groups = sorted(set(edge.groups) - set(groups))
            if unknown_groups:
                raise InvalidEdgeError(
                    "edge references an unknown group",
                    edge=edge.id,
                    group=unknown_groups[0],
                )

        incoming = {node_id: [] for node_id in nodes}
        outgoing = {node_id: [] for node_id in nodes}
        by_group = {group_id: [] for group_id in groups}
        for edge in edges.values():
            outgoing[edge.source].append(edge.id)
            incoming[edge.target].append(edge.id)
            for group_id in edge.groups:
                by_group[group_id].append(edge.id)

        self.nodes: Mapping[str, Node] = MappingProxyType(dict(sorted(nodes.items())))
        self.groups: Mapping[str, EdgeGroup] = MappingProxyType(dict(sorted(groups.items())))
        self.edges: Mapping[str, Edge] = MappingProxyType(dict(sorted(edges.items())))
        self.aliases: Mapping[str, str] = MappingProxyType(dict(sorted(aliases.items())))
        self._incoming = MappingProxyType(
            {key: tuple(sorted(value)) for key, value in sorted(incoming.items())}
        )
        self._outgoing = MappingProxyType(
            {key: tuple(sorted(value)) for key, value in sorted(outgoing.items())}
        )
        self._by_group = MappingProxyType(
            {key: tuple(sorted(value)) for key, value in sorted(by_group.items())}
        )

    @staticmethod
    def _merge_node(previous: Node, current: Node) -> Node:
        metadata = dict(previous.metadata)
        for key, value in current.metadata.items():
            existing = metadata.get(key)
            if existing is not None and existing != value:
                raise AliasConflictError(
                    "canonical node metadata conflicts across registered sources",
                    node=current.id,
                    field=key,
                )
            metadata[key] = value
        provenance = (
            previous.provenance
            if previous.provenance == current.provenance
            else None
        )
        return Node(
            previous.id,
            tuple(sorted(set((*previous.aliases, *current.aliases)))),
            provenance,
            metadata,
        )

    @staticmethod
    def _register_alias(
        aliases: dict[str, str], alias: str, canonical: str, node: str
    ) -> None:
        previous = aliases.get(alias)
        if previous is not None and previous != canonical:
            raise AliasConflictError(
                "alias resolves to contradictory canonical nodes",
                alias=alias,
                node=node,
                previous=previous,
            )
        aliases[alias] = canonical

    def _artifact_identity(self, alias: str) -> Path | None:
        logical = PurePosixPath(alias)
        if logical.is_absolute() or ".." in logical.parts:
            contained_path(self.repo_root, alias, must_exist=False)
        candidate = (self.repo_root / Path(*logical.parts)).resolve(strict=False)
        if "/" in alias and not candidate.exists():
            contained_path(self.repo_root, alias, must_exist=True)
        if candidate.exists():
            contained_path(self.repo_root, alias, must_exist=True)
            return candidate.resolve()
        return None

    def resolve(self, requested: str) -> str:
        canonical = self.aliases.get(requested)
        if canonical is not None:
            return canonical
        logical = PurePosixPath(requested)
        looks_like_path = "/" in requested or logical.is_absolute() or ".." in logical.parts
        if looks_like_path:
            candidate = contained_path(self.repo_root, requested, must_exist=True)
            relative = candidate.relative_to(self.repo_root).as_posix()
            return self.aliases.get(relative, relative)
        candidate = (self.repo_root / requested).resolve(strict=False)
        if candidate.exists():
            contained_path(self.repo_root, requested, must_exist=True)
            relative = candidate.relative_to(self.repo_root).as_posix()
            return self.aliases.get(relative, relative)
        raise UnknownNodeError("logical node is not registered", node=requested)

    def incoming(self, node: str, groups: Iterable[str] | None = None) -> tuple[EdgeView, ...]:
        canonical = self.resolve(node)
        selected = self._selected_groups(groups)
        if canonical not in self.nodes:
            return ()
        return tuple(
            EdgeView(self.edges[edge_id], Direction.INCOMING, self.edges[edge_id].source)
            for edge_id in self._incoming[canonical]
            if selected is None or selected.intersection(self.edges[edge_id].groups)
        )

    def outgoing(self, node: str, groups: Iterable[str] | None = None) -> tuple[EdgeView, ...]:
        canonical = self.resolve(node)
        selected = self._selected_groups(groups)
        if canonical not in self.nodes:
            return ()
        return tuple(
            EdgeView(self.edges[edge_id], Direction.OUTGOING, self.edges[edge_id].target)
            for edge_id in self._outgoing[canonical]
            if selected is None or selected.intersection(self.edges[edge_id].groups)
        )

    def incident(self, node: str, groups: Iterable[str] | None = None) -> tuple[EdgeView, ...]:
        values = (*self.incoming(node, groups), *self.outgoing(node, groups))
        return tuple(sorted(values, key=lambda view: (view.edge.id, view.direction.value)))

    def groups_for(self, node: str) -> tuple[EdgeGroup, ...]:
        group_ids = {
            group_id
            for view in self.incident(node)
            for group_id in view.edge.groups
        }
        return tuple(self.groups[group_id] for group_id in sorted(group_ids))

    def edge(self, edge_id: str) -> Edge:
        try:
            return self.edges[edge_id]
        except KeyError as error:
            raise UnknownEdgeError("edge is not registered", edge=edge_id) from error

    def edges_for_group(self, group_id: str) -> tuple[Edge, ...]:
        self._group(group_id)
        return tuple(self.edges[edge_id] for edge_id in self._by_group[group_id])

    def traverse_edge(self, edge_id: str, direction: Direction) -> TraversalResult:
        edge = self.edge(edge_id)
        if not edge.traversable:
            raise ForbiddenTraversalError("edge is not eligible for traversal", edge=edge_id)
        if direction is Direction.BOTH:
            steps = (
                self._step(edge, Direction.OUTGOING, edge.source, (edge.source,), ()),
                self._step(edge, Direction.INCOMING, edge.target, (edge.target,), ()),
            )
        elif direction is Direction.OUTGOING:
            steps = (self._step(edge, direction, edge.source, (edge.source,), ()),)
        else:
            steps = (self._step(edge, direction, edge.target, (edge.target,), ()),)
        return TraversalResult(
            None,
            tuple(sorted({step.from_node for step in steps} | {step.to_node for step in steps})),
            (edge.id,),
            steps,
        )

    def traverse_group(
        self,
        node: str,
        group_id: str,
        direction: Direction,
        *,
        transitive: bool = False,
    ) -> TraversalResult:
        start = self.resolve(node)
        group = self._group(group_id)
        if not group.traversal.permits(direction):
            raise ForbiddenTraversalError(
                "group does not permit the selected direction",
                group=group_id,
                direction=direction.value,
            )
        if transitive and not group.traversal.transitive:
            raise ForbiddenTraversalError(
                "group does not permit transitive traversal", group=group_id
            )
        if start not in self.nodes:
            return TraversalResult(start, (start,), (), ())

        queue = deque([(start, (start,), tuple())])
        expanded: set[str] = set()
        visited_nodes = {start}
        visited_edges: set[str] = set()
        steps: list[TraversalStep] = []
        while queue:
            current, path_nodes, path_edges = queue.popleft()
            if current in expanded:
                continue
            expanded.add(current)
            candidates = self._group_candidates(current, group_id, direction)
            for edge, edge_direction in candidates:
                if not edge.traversable or edge.id in visited_edges:
                    continue
                step = self._step(edge, edge_direction, current, path_nodes, path_edges)
                visited_edges.add(edge.id)
                visited_nodes.add(step.to_node)
                steps.append(step)
                if transitive and step.to_node not in expanded:
                    queue.append((step.to_node, step.path_nodes, step.path_edges))
        return TraversalResult(
            start,
            tuple(sorted(visited_nodes)),
            tuple(sorted(visited_edges)),
            tuple(steps),
        )

    def find_cycle(
        self,
        group_id: str,
        direction: Direction = Direction.OUTGOING,
    ) -> tuple[str, ...] | None:
        group = self._group(group_id)
        if direction is Direction.BOTH or not group.traversal.permits(direction):
            raise ForbiddenTraversalError(
                "cycle detection requires one permitted direction",
                group=group_id,
                direction=direction.value,
            )
        states: dict[str, int] = {}
        for root in sorted(self.nodes):
            if states.get(root, 0) != 0:
                continue
            states[root] = 1
            path = [root]
            positions = {root: 0}
            frames = [(root, iter(self._targets(root, group_id, direction)))]
            while frames:
                node, targets = frames[-1]
                try:
                    target = next(targets)
                except StopIteration:
                    frames.pop()
                    path.pop()
                    positions.pop(node)
                    states[node] = 2
                    continue

                state = states.get(target, 0)
                if state == 1:
                    cycle_start = positions[target]
                    return tuple((*path[cycle_start:], target))
                if state == 2:
                    continue
                states[target] = 1
                positions[target] = len(path)
                path.append(target)
                frames.append(
                    (target, iter(self._targets(target, group_id, direction)))
                )
        return None

    def dependency_order(
        self,
        group_id: str,
        selected: Iterable[str] | None = None,
        *,
        direction: Direction = Direction.OUTGOING,
        preferred_order: Iterable[str] = (),
    ) -> tuple[str, ...]:
        group = self._group(group_id)
        if direction is Direction.BOTH or not group.traversal.permits(direction):
            raise ForbiddenTraversalError(
                "dependency ordering requires one permitted direction",
                group=group_id,
                direction=direction.value,
            )
        if not group.traversal.transitive:
            raise ForbiddenTraversalError(
                "dependency ordering requires a transitively traversable group",
                group=group_id,
            )
        cycle = self.find_cycle(group_id, direction)
        if cycle is not None:
            raise InvalidGroupError(
                "dependency group contains a cycle",
                group=group_id,
                cycle=" -> ".join(cycle),
            )

        if selected is None:
            required = set(self.nodes)
        else:
            required: set[str] = set()
            for requested in selected:
                canonical = self.resolve(requested)
                required.add(canonical)
                result = self.traverse_group(
                    canonical,
                    group_id,
                    direction,
                    transitive=True,
                )
                required.update(result.nodes)

        preferred = tuple(self.resolve(node) for node in preferred_order)
        if len(set(preferred)) != len(preferred):
            raise InvalidGroupError("preferred dependency order contains duplicates")
        rank = {node: index for index, node in enumerate(preferred)}

        def node_key(node: str) -> tuple[int, int, str]:
            if node in rank:
                return (0, rank[node], node)
            return (1, 0, node)

        dependency_count = {node: 0 for node in required}
        dependents = {node: set() for node in required}
        for node in required:
            dependencies = set(self._targets(node, group_id, direction))
            for dependency in dependencies:
                if dependency not in required:
                    continue
                dependency_count[node] += 1
                dependents[dependency].add(node)

        ready = [node_key(node) for node, count in dependency_count.items() if count == 0]
        heapq.heapify(ready)
        ordered: list[str] = []
        while ready:
            *_, node = heapq.heappop(ready)
            ordered.append(node)
            for dependent in dependents[node]:
                dependency_count[dependent] -= 1
                if dependency_count[dependent] == 0:
                    heapq.heappush(ready, node_key(dependent))

        if len(ordered) != len(required):
            raise InvalidGroupError(
                "dependency group contains a cycle",
                group=group_id,
            )
        return tuple(ordered)

    def _targets(
        self, node: str, group_id: str, direction: Direction
    ) -> tuple[str, ...]:
        return tuple(
            edge.target if edge_direction is Direction.OUTGOING else edge.source
            for edge, edge_direction in self._group_candidates(
                node, group_id, direction
            )
            if edge.traversable
        )

    def _group_candidates(
        self, node: str, group_id: str, direction: Direction
    ) -> tuple[tuple[Edge, Direction], ...]:
        candidates: list[tuple[Edge, Direction]] = []
        if direction in {Direction.OUTGOING, Direction.BOTH}:
            candidates.extend(
                (view.edge, Direction.OUTGOING)
                for view in self.outgoing(node, (group_id,))
            )
        if direction in {Direction.INCOMING, Direction.BOTH}:
            candidates.extend(
                (view.edge, Direction.INCOMING)
                for view in self.incoming(node, (group_id,))
            )
        return tuple(sorted(candidates, key=lambda item: (item[0].id, item[1].value)))

    @staticmethod
    def _step(
        edge: Edge,
        direction: Direction,
        current: str,
        path_nodes: tuple[str, ...],
        path_edges: tuple[str, ...],
    ) -> TraversalStep:
        if direction is Direction.OUTGOING:
            expected, target = edge.source, edge.target
        else:
            expected, target = edge.target, edge.source
        if current != expected:
            raise ForbiddenTraversalError(
                "edge direction is incompatible with the traversal endpoint",
                edge=edge.id,
                node=current,
                direction=direction.value,
            )
        return TraversalStep(
            edge,
            direction,
            current,
            target,
            (*path_nodes, target),
            (*path_edges, edge.id),
        )

    def _selected_groups(self, groups: Iterable[str] | None) -> frozenset[str] | None:
        if groups is None:
            return None
        selected = frozenset(groups)
        for group_id in selected:
            self._group(group_id)
        return selected

    def _group(self, group_id: str) -> EdgeGroup:
        try:
            return self.groups[group_id]
        except KeyError as error:
            raise UnknownGroupError("edge group is not registered", group=group_id) from error
