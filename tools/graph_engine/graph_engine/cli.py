from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .errors import GraphError, UnsafeOutputError
from .manifest import DEFAULT_SOURCE_REGISTRY, load_registry
from .model import Direction, Edge
from .registry import EdgeRegistry, EdgeView, TraversalStep


@dataclass(frozen=True, slots=True)
class Row:
    kind: str
    requested: str
    canonical_node: str
    edge_id: str
    direction: str
    opposite: str
    source: str
    target: str
    relation: str
    groups: str
    traversable: str
    metadata: str
    provenance: str
    path: str


FIELDS = tuple(Row.__dataclass_fields__)


def _parser(default_repo_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query explicitly registered repository edges and named groups."
    )
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    parser.add_argument("--registry", default=DEFAULT_SOURCE_REGISTRY)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--node")
    selector.add_argument("--edge")
    selector.add_argument("--list-groups", action="store_true")
    parser.add_argument("--direction", choices=tuple(item.value for item in Direction))
    parser.add_argument("--group")
    parser.add_argument("--traverse", action="store_true")
    parser.add_argument("--transitive", action="store_true")
    return parser


def _metadata(edge: Edge) -> str:
    return ";".join(f"{key}={value}" for key, value in edge.metadata.items())


def _provenance(edge: Edge) -> str:
    value = edge.provenance
    return f"{value.kind}:{value.source_id}:{value.locator}"


def _row_for_view(requested: str, canonical: str, view: EdgeView) -> Row:
    edge = view.edge
    return Row(
        "edge",
        requested,
        canonical,
        edge.id,
        view.direction.value,
        view.opposite,
        edge.source,
        edge.target,
        edge.relation,
        ",".join(edge.groups),
        str(edge.traversable).lower(),
        _metadata(edge),
        _provenance(edge),
        "",
    )


def _row_for_edge(edge: Edge) -> Row:
    return Row(
        "edge",
        edge.id,
        "",
        edge.id,
        "",
        "",
        edge.source,
        edge.target,
        edge.relation,
        ",".join(edge.groups),
        str(edge.traversable).lower(),
        _metadata(edge),
        _provenance(edge),
        "",
    )


def _row_for_step(step: TraversalStep) -> Row:
    edge = step.edge
    return Row(
        "traversal",
        step.from_node,
        step.from_node,
        edge.id,
        step.direction.value,
        step.to_node,
        edge.source,
        edge.target,
        edge.relation,
        ",".join(edge.groups),
        str(edge.traversable).lower(),
        _metadata(edge),
        _provenance(edge),
        " -> ".join(step.path_nodes),
    )


def _rows(args: argparse.Namespace, registry: EdgeRegistry) -> tuple[Row, ...]:
    if args.list_groups:
        if args.node or args.edge or args.group or args.traverse or args.transitive or args.direction:
            raise GraphError("list-groups cannot be combined with query or traversal options")
        return tuple(
            Row(
                "group",
                group.id,
                "",
                "",
                ",".join(
                    sorted(direction.value for direction in group.traversal.directions)
                ),
                "",
                "",
                "",
                group.purpose,
                group.id,
                str(group.traversal.transitive).lower(),
                ";".join(f"{key}={value}" for key, value in group.metadata.items()),
                f"{group.provenance.kind}:{group.provenance.source_id}:{group.provenance.locator}",
                "",
            )
            for group in registry.groups.values()
        )

    if args.edge:
        if args.group or args.transitive:
            raise GraphError("exact edge queries do not accept group or transitive options")
        edge = registry.edge(args.edge)
        if not args.traverse:
            if args.direction:
                raise GraphError("direction requires edge traversal")
            return (_row_for_edge(edge),)
        if not args.direction:
            raise GraphError("edge traversal requires explicit direction")
        result = registry.traverse_edge(args.edge, Direction.parse(args.direction))
        return tuple(_row_for_step(step) for step in result.steps)

    assert args.node
    canonical = registry.resolve(args.node)
    if args.transitive:
        args.traverse = True
    if args.traverse:
        if not args.group:
            raise GraphError("node traversal requires one named group")
        if not args.direction:
            raise GraphError("node traversal requires explicit direction")
        result = registry.traverse_group(
            args.node,
            args.group,
            Direction.parse(args.direction),
            transitive=args.transitive,
        )
        return tuple(_row_for_step(step) for step in result.steps)

    direction = Direction.parse(args.direction or Direction.BOTH.value)
    groups = (args.group,) if args.group else None
    if direction is Direction.INCOMING:
        views = registry.incoming(args.node, groups)
    elif direction is Direction.OUTGOING:
        views = registry.outgoing(args.node, groups)
    else:
        views = registry.incident(args.node, groups)
    return tuple(_row_for_view(args.node, canonical, view) for view in views)


def _safe(value: str) -> str:
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise UnsafeOutputError("TSV value contains a record-breaking control character")
    return value


def render_tsv(rows: Iterable[Row]) -> str:
    lines = ["\t".join(FIELDS)]
    for row in rows:
        lines.append("\t".join(_safe(getattr(row, field)) for field in FIELDS))
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None, *, default_repo_root: Path) -> int:
    args = _parser(default_repo_root).parse_args(argv)
    try:
        registry = load_registry(args.repo_root, args.registry)
        output = render_tsv(_rows(args, registry))
    except GraphError as error:
        details = " ".join(
            f"{key}={value}" for key, value in error.failure.details.items()
        )
        print(f"{error.failure.code}: {error.failure.message}{(' ' + details) if details else ''}")
        return 3 if error.failure.code in {
            "GRAPH.UNKNOWN_NODE",
            "GRAPH.UNKNOWN_GROUP",
            "GRAPH.UNKNOWN_EDGE",
            "GRAPH.MISSING_ARTIFACT",
        } else 1
    print(output, end="")
    return 0
