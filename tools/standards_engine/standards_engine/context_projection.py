"""Host purpose and the single application-output construction boundary."""
from __future__ import annotations

import logging
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Callable, TYPE_CHECKING

from tools.graph_engine.graph_engine import Direction, EdgeRegistry, GraphContribution, GraphError
from tools.standards_graph.standards_graph import Provider
from tools.standards_contracts.standards_contracts import ContractError

from . import _generated_contract as c
from .supporting import resolve_material

if TYPE_CHECKING:
    from .engine import CompiledSnapshot, StandardsEngine


class Purpose(str, Enum):
    APPLICATION = "application"
    AUTHORING = "authoring"


APPLICATION_CALLS = {
    "route": c.RouteCall,
    "read": c.ApplicationReadCall,
    "read_many": c.ApplicationReadManyCall,
    "related": c.RelatedCall,
    "routing_facts": c.RoutingFactsCall,
    "query": c.ApplicationQueryCall,
    "inspect": c.ApplicationInspectCall,
}


def application_rejection(code: str = "APPLICATION.CONTENT_UNAVAILABLE", outcome: str = "unavailable"):
    messages = {
        "APPLICATION.CONTENT_UNAVAILABLE": "The requested guidance is awaiting application publication.",
        "APPLICATION.RESULT_LIMIT": "Select fewer items or narrower policy scopes within the 2 MiB reading limit.",
        "APPLICATION.INPUT_INVALID": "Supply arguments from this interface's published contract.",
        "APPLICATION.OPERATION_UNAVAILABLE": "This interface provides application navigation operations.",
        "APPLICATION.INTERNAL_UNAVAILABLE": "The requested application observation could not be established.",
        "APPLICATION.UNSUPPORTED_CAPTURE": "Use a snapshot captured by the supported content contract.",
    }
    return c.ApplicationRejectedResult.from_value({
        "kind": "application-rejected-result", "purpose": "application",
        "code": code, "outcome": outcome, "message": messages[code], "next_operations": [],
    })


def public_operation(function: Callable) -> Callable:
    """Admit application work before invoking any authoring implementation."""
    @wraps(function)
    def invoke(engine, call):
        if engine.purpose is Purpose.APPLICATION:
            try:
                return application_dispatch(engine, function.__name__, call)
            except Exception as error:
                logging.getLogger(__name__).error(
                    "Application observation failed: %s", type(error).__name__
                )
                return application_rejection("APPLICATION.INTERNAL_UNAVAILABLE")
        return function(engine, call)
    return invoke


class _UnqualifiedContent(Exception):
    pass


class ApplicationView:
    """Build application values from the qualified portion of one snapshot."""

    def __init__(self, compiled: CompiledSnapshot, snapshot: c.SnapshotHandle):
        self.compiled = compiled
        self.snapshot = snapshot.as_contract()
        self.eligible = frozenset(
            identity for identity, material in compiled.materials.items()
            if compiled.supporting.exposure_state(identity, material.binding) == "current"
        )
        visible = set(self.eligible)
        visible.update(unit.id for unit in compiled.corpus.policy_units if unit.module in self.eligible)
        groups = {key: value for key, value in compiled.graph.groups.items() if key in {
            "standards-requires", "standards-specializes", "standards-dependencies", "policy-impact", "semantic",
        }}
        edges = tuple(edge for edge in compiled.graph.edges.values()
                      if edge.source in visible and edge.target in visible
                      and set(edge.groups) <= groups.keys())
        nodes = tuple(node for key, node in compiled.graph.nodes.items() if key in visible)
        # Retain each original declaration's technical provenance while taking
        # a view. A projection is not a new author of those graph facts.
        by_source = {}
        for index, records in enumerate((nodes, tuple(groups.values()), edges)):
            for record in records:
                by_source.setdefault(record.provenance.source_id, ([], [], []))[index].append(record)
        sources = tuple(Provider(identity, GraphContribution(*(tuple(rows) for rows in records)))
                        for identity, records in sorted(by_source.items()))
        self.graph = EdgeRegistry(Path("/"), sources,
                                  logical_artifacts=(compiled.materials[key].path for key in self.eligible))

    def _require(self, target: str):
        selected = resolve_material(self.compiled, target)
        if selected is None:
            raise _UnqualifiedContent()
        material, unit = selected
        pending, checked = [material.id], set()
        while pending:
            identity = pending.pop()
            if identity in checked:
                continue
            if identity not in self.eligible:
                raise _UnqualifiedContent()
            checked.add(identity)
            owner = self.compiled.materials[identity]
            pending.extend((*owner.requires, *owner.specializes))
        return material, unit

    def _child(self, kind: str, identity: str) -> dict:
        return {"kind": "snapshot-child-handle", "snapshot": self.snapshot,
                "child_kind": kind, "child_id": identity, "schema_version": 5}

    def _next_read(self, identity: str) -> dict:
        return {"operation": "read", "target": identity, "snapshot": self.snapshot}

    def _result(self, kind: str, **fields) -> dict:
        return {"kind": kind, "purpose": "application", "snapshot": self.snapshot, **fields}

    def read(self, target: str, detail: str = "compact"):
        material, unit = self._require(target)
        identity = unit.id if unit is not None else material.id
        value = self._result(
            "application-read-result",
            policy={"id": identity, "handle": self._child("policy", identity),
                    "role": material.role, "level": material.level},
            content=unit.content if unit is not None else material.content,
            scope={"kind": "structured", "heading_path": list(unit.heading_path)} if unit else {"kind": "whole-artifact"},
            requires=list(material.requires), specializes=list(material.specializes),
            next_operations=[self._next_read(item) for item in dict.fromkeys((*material.requires, *material.specializes))],
        )
        if detail == "full":
            value["related"] = self.relationships(identity, None, Direction.BOTH, False)
        return c.ApplicationReadResult.from_value(value)

    def _scope_targets(self, target: str) -> tuple[str, ...]:
        module = self.compiled.corpus.resolve_module(target)
        if module is None:
            return (target,)
        return (module.module_id, *(unit.id for unit in
                self.compiled.corpus.policy_unit_corpus.for_module(module.module_id)))

    def relationships(self, target: str, groups, direction: Direction, transitive: bool) -> list[dict]:
        selected = {}
        for identity in self._scope_targets(target):
            if identity not in self.graph.nodes:
                continue
            if transitive:
                pairs = ((step.edge, step.direction) for group in groups
                         for step in self.graph.traverse_group(identity, group, direction, transitive=True).steps)
            else:
                views = (self.graph.incoming(identity, groups) if direction is Direction.INCOMING
                         else self.graph.outgoing(identity, groups) if direction is Direction.OUTGOING
                         else self.graph.incident(identity, groups))
                pairs = ((view.edge, view.direction) for view in views)
            for edge, way in pairs:
                key = f"{way.value}:{edge.id}"
                selected[key] = {"handle": self._child("relationship", key),
                                 "source": edge.source, "target": edge.target,
                                 "relation": edge.relation, "groups": list(edge.groups), "direction": way.value}
        return [selected[key] for key in sorted(selected)]

    def related(self, target: str, groups: tuple[str, ...], direction: str, transitive: bool):
        material, unit = self._require(target)
        identity = unit.id if unit else material.id
        relationships = self.relationships(identity, groups, Direction.parse(direction), transitive)
        neighbors = sorted({entry[key] for entry in relationships for key in ("source", "target")} - set(self._scope_targets(identity)))
        return c.ApplicationRelatedResult.from_value(self._result(
            "application-related-result", target=identity, relationships=relationships,
            next_operations=[self._next_read(item) for item in neighbors],
        ))

    def inspect(self, handle):
        if handle.child_kind == "policy":
            return self.read(handle.child_id, "full")
        way, _, edge_id = handle.child_id.partition(":")
        if way not in {"incoming", "outgoing"}:
            raise _UnqualifiedContent()
        edge = self.graph.edge(edge_id)
        self._require(edge.source)
        self._require(edge.target)
        target = edge.target if way == "incoming" else edge.source
        relationships = [entry for entry in self.relationships(target, tuple(edge.groups), Direction.parse(way), False)
                         if entry["handle"]["child_id"] == handle.child_id]
        return c.ApplicationRelatedResult.from_value(self._result(
            "application-related-result", target=target, relationships=relationships,
            next_operations=[self._next_read(edge.source), self._next_read(edge.target)],
        ))

    def routing_facts(self):
        from .agent_navigation import fact_definitions
        self._require("router")
        return c.ApplicationRoutingFactsResult.from_value(self._result(
            "application-routing-facts-result", facts=fact_definitions(self.compiled.router), next_operations=[],
        ))

    def route(self, engine, call):
        from .agent_navigation import fact_definitions
        self._require("router")
        _facts, _rules, _ordered, entries, unresolved = engine._routing_selection(self.compiled, call)
        reading = []
        for entry in entries:
            if entry.state != "selected":
                continue
            self._require(entry.target)
            reading.append({"target": entry.target, "scope": entry.scope.as_contract(),
                            "authority": entry.authority, "state": "selected"})
        facts = {fact["id"]: fact for fact in fact_definitions(self.compiled.router)}
        return c.ApplicationRouteResult.from_value(self._result(
            "application-route-result", status="needs-facts" if unresolved else "complete",
            reading_plan=reading, unresolved_questions=[{"fact": facts[key]} for key in sorted(unresolved)],
            next_operations=[self._next_read(entry["target"]) for entry in reading],
        ))


def application_dispatch(engine: StandardsEngine, operation: str, call):
    call_type = APPLICATION_CALLS.get(operation)
    if call_type is None:
        return application_rejection("APPLICATION.OPERATION_UNAVAILABLE", "unsupported")
    try:
        # Native callers obey the same input schema as the transport facade.
        checked = call_type.from_value(call.as_contract())
    except (ContractError, AttributeError, TypeError, ValueError):
        return application_rejection("APPLICATION.INPUT_INVALID", "invalid")
    try:
        values = checked.as_contract()
        if operation == "inspect":
            snapshot = checked.handle.snapshot
        elif "snapshot" in values:
            snapshot = c.SnapshotHandle.from_value(values["snapshot"])
        else:
            captured = engine._capture_snapshot(c.CreateSnapshotCall(kind="create-snapshot"))
            if isinstance(captured, c.RejectedResult):
                code = "APPLICATION.UNSUPPORTED_CAPTURE" if captured.outcome == "unsupported" else "APPLICATION.INTERNAL_UNAVAILABLE"
                return application_rejection(code, captured.outcome)
            snapshot = c.SnapshotHandle.from_value(captured.as_contract()["snapshot"]["snapshot"])
        compiled = engine._compiled_snapshot(engine._snapshot_id(snapshot))
        view = ApplicationView(compiled, snapshot)
        if operation == "query":
            values = checked.request.as_contract()
            operation = values.pop("kind")
            checked = checked.request
        if operation == "read_many":
            from .agent_navigation import read_many
            return read_many(engine, checked, compiled, application_view=view)
        if operation == "read":
            return view.read(values["target"], values.get("detail", "compact"))
        if operation == "related":
            return view.related(values["target"], tuple(values["groups"]), values["direction"], values["transitive"])
        if operation == "route":
            return view.route(engine, checked)
        if operation == "routing_facts":
            return view.routing_facts()
        return view.inspect(checked.handle)
    except (_UnqualifiedContent, GraphError):
        return application_rejection()
    except engine._domain_errors() as error:
        failure = getattr(error, "failure", None)
        if getattr(failure, "outcome", None) == "unsupported":
            return application_rejection("APPLICATION.UNSUPPORTED_CAPTURE", "unsupported")
        return application_rejection("APPLICATION.INTERNAL_UNAVAILABLE")


def qualified_operations(contract: dict, purpose: Purpose | str) -> list[dict]:
    """Select canonical operation roots before projecting schemas or examples."""
    selected = Purpose(purpose)
    result = []
    for operation in contract["operations"]:
        if selected is Purpose.AUTHORING:
            result.append(operation)
            continue
        variant = operation.get("variants", {}).get("application")
        if variant is not None:
            result.append({"id": operation["id"], "capability": operation["capability"], **variant})
    return result
