from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

from tools.graph_engine.graph_engine import (
    Direction,
    Edge,
    EdgeRegistry,
    GraphError,
)
from tools.standards_analysis.standards_analysis import (
    POLICY_UNIT_REGISTRY,
    AnalysisError,
    AnalysisFailure,
    PolicyUnit,
    PolicyUnitCorpus,
    PolicyUnitTombstone,
    compile_snapshot,
    digest_bytes,
    identity,
    load_policy_unit_corpus,
    markdown_structural_digest,
)
from tools.standards_graph.standards_graph import (
    POLICY_IMPACT_MANIFEST,
    standards_navigation_registry,
)
from tools.standards_metadata.standards_metadata import (
    CANONICAL_MODULE_CORPUS,
    CanonicalModuleCorpus,
    ModuleMetadata,
    load_canonical_module_corpus,
)

from .model import (
    InspectCall,
    InspectionResult,
    NavigationInspectionResult,
    PolicyInspectionResult,
    QueryCall,
    QueryResult,
    ReadRequest,
    ReadResult,
    RejectedResult,
    RelatedRequest,
    RelatedResult,
    RelationshipInspectionResult,
    SnapshotInspectionResult,
)


NAVIGATION_DOMAIN = "coding-standards:navigation:v1"


class StandardsEngine:
    """Snapshot-bound facade over canonical metadata and declared relationships."""

    def __init__(
        self,
        root: Path,
        snapshot,
        modules: CanonicalModuleCorpus,
        policies: PolicyUnitCorpus,
        graph: EdgeRegistry,
    ) -> None:
        self._root = root.resolve()
        self._snapshot = snapshot
        self._modules = modules
        self._policies = policies
        self._graph = graph
        self._navigation: dict[str, dict[str, object]] = {}

    @classmethod
    def open_repository(cls, root: Path) -> StandardsEngine:
        repo_root = root.resolve()
        initial_modules = load_canonical_module_corpus(repo_root)
        initial_policies = load_policy_unit_corpus(repo_root, initial_modules)
        scope = tuple(
            sorted(
                {
                    CANONICAL_MODULE_CORPUS,
                    POLICY_UNIT_REGISTRY,
                    POLICY_IMPACT_MANIFEST,
                    *initial_modules.members,
                    *initial_policies.sources,
                }
            )
        )
        before = compile_snapshot(repo_root, scope)
        modules = load_canonical_module_corpus(repo_root)
        policies = load_policy_unit_corpus(repo_root, modules)
        graph = standards_navigation_registry(repo_root, modules.modules)
        after = compile_snapshot(repo_root, scope)
        if (
            before.handle != after.handle
            or initial_modules.members != modules.members
            or initial_policies.sources != policies.sources
        ):
            raise AnalysisError(
                before_source_changed_failure()
            )
        return cls(repo_root, after, modules, policies, graph)

    @property
    def snapshot(self) -> Mapping[str, object]:
        return self._snapshot.handle

    def query(self, call: QueryCall) -> QueryResult:
        stale = self._require_snapshot(call.snapshot)
        if stale is not None:
            return stale
        if isinstance(call.request, ReadRequest):
            if not isinstance(call.request.target, str) or not call.request.target:
                return self._invalid_request("read target must be a non-empty string")
            return self._read(call.request)
        if isinstance(call.request, RelatedRequest):
            invalid = self._validate_related_request(call.request)
            if invalid is not None:
                return invalid
            return self._related(call.request)
        return self._reject(
            "NAVIGATION.UNSUPPORTED_REQUEST",
            "unsupported",
            "The query request kind is not implemented.",
        )

    def inspect(self, call: InspectCall) -> InspectionResult:
        handle = dict(call.handle)
        kind = handle.get("kind")
        if kind == "snapshot-handle":
            stale = self._require_snapshot(handle)
            if stale is not None:
                return stale
            return SnapshotInspectionResult.from_value(
                {"kind": "snapshot-inspection-result", "snapshot": self._snapshot.inspection}
            )
        if kind == "policy-handle":
            stale = self._require_snapshot_value(handle.get("snapshot"))
            if stale is not None:
                return stale
            return self._inspect_policy(str(handle.get("id", "")))
        if kind == "relationship-handle":
            stale = self._require_snapshot_value(handle.get("snapshot"))
            if stale is not None:
                return stale
            return self._inspect_relationship(str(handle.get("id", "")))
        if kind == "navigation-handle":
            stale = self._require_snapshot_value(handle.get("snapshot"))
            if stale is not None:
                return stale
            navigation_id = str(handle.get("id", ""))
            value = self._navigation.get(navigation_id)
            if value is None:
                return self._reject(
                    "NAVIGATION.UNKNOWN_HANDLE",
                    "unavailable",
                    "The navigation result is not available from this engine instance.",
                    target=navigation_id,
                )
            return NavigationInspectionResult.from_value(
                {
                    "kind": "navigation-inspection-result",
                    "navigation": value,
                    "provenance": self._snapshot.inspection["versions"],
                }
            )
        return self._reject(
            "NAVIGATION.UNSUPPORTED_HANDLE",
            "unsupported",
            "The handle kind is not inspectable by the navigation slice.",
        )

    def _read(self, request: ReadRequest) -> QueryResult:
        target = self._resolve_policy(request.target)
        if isinstance(target, RejectedResult):
            return target
        selected, module = target
        if isinstance(selected, PolicyUnit):
            canonical_id = selected.id
            content = selected.content
            scope = {"kind": "structured", "heading_path": list(selected.heading_path)}
        else:
            canonical_id = module.module_id
            content = (self._root / module.path).read_text(encoding="utf-8")
            scope = {"kind": "whole-artifact"}
        policy = self._policy_summary(canonical_id, module, scope)
        related = self._direct_relationships(module.module_id, None, Direction.BOTH)
        identity_value = {
            "handle": {"snapshot": self._snapshot.handle},
            "policy": policy,
            "content": content,
            "requires": list(module.requires),
            "specializes": list(module.specializes),
            "related": related,
        }
        handle = self._navigation_handle(identity_value)
        value = {
            "kind": "read-result",
            "handle": handle,
            "policy": policy,
            "content": content,
            "requires": list(module.requires),
            "specializes": list(module.specializes),
            "related": related,
            "next_operations": [
                {"operation": "query", "request_kind": "related", "target": canonical_id},
                {"operation": "inspect", "request_kind": "inspect", "target": canonical_id},
            ],
            "summary": f"Read canonical standard {canonical_id}.",
        }
        self._navigation[str(handle["id"])] = value
        return ReadResult.from_value(value)

    def _related(self, request: RelatedRequest) -> QueryResult:
        try:
            direction = Direction.parse(request.direction)
            graph_target = self._graph_target(request.target)
            relationships = (
                self._transitive_relationships(
                    graph_target,
                    request.groups,
                    direction,
                )
                if request.transitive
                else self._direct_relationships(graph_target, request.groups, direction)
            )
        except GraphError as error:
            return self._graph_rejection(error)
        identity_value = {
            "handle": {"snapshot": self._snapshot.handle},
            "target": graph_target,
            "relationships": relationships,
        }
        handle = self._navigation_handle(identity_value)
        value = {
            "kind": "related-result",
            "handle": handle,
            "target": graph_target,
            "relationships": relationships,
            "next_operations": [
                {"operation": "inspect", "request_kind": "inspect", "target": request.target}
            ],
            "summary": f"Found {len(relationships)} declared relationships.",
        }
        self._navigation[str(handle["id"])] = value
        return RelatedResult.from_value(value)

    def _validate_related_request(
        self,
        request: RelatedRequest,
    ) -> RejectedResult | None:
        if not isinstance(request.target, str) or not request.target:
            return self._invalid_request("related target must be a non-empty string")
        if (
            not isinstance(request.groups, tuple)
            or not request.groups
            or any(not isinstance(group, str) or not group for group in request.groups)
            or len(set(request.groups)) != len(request.groups)
        ):
            return self._reject(
                "NAVIGATION.INVALID_GROUP_SELECTION",
                "invalid",
                "Related queries require unique non-empty named groups.",
            )
        if request.direction not in {"incoming", "outgoing", "both"}:
            return self._invalid_request(
                "related direction must be incoming, outgoing, or both"
            )
        if not isinstance(request.transitive, bool):
            return self._invalid_request("related transitive must be a boolean")
        return None

    def _resolve_policy(
        self,
        requested: str,
    ) -> tuple[PolicyUnit | ModuleMetadata, ModuleMetadata] | RejectedResult:
        selected = self._policies.resolve(requested)
        if isinstance(selected, PolicyUnitTombstone):
            return self._reject(
                "NAVIGATION.RETIRED_POLICY",
                "unavailable",
                "The policy identity is retired.",
                target=requested,
            )
        if isinstance(selected, PolicyUnit):
            module = self._modules.resolve(selected.module)
            assert module is not None
            return selected, module
        module = self._modules.resolve(requested)
        if module is not None and requested == module.module_id:
            return module, module
        return self._reject(
            "NAVIGATION.UNKNOWN_POLICY",
            "unavailable",
            "The canonical policy or module identity is not registered.",
            target=requested,
        )

    def _graph_target(self, requested: str) -> str:
        selected = self._policies.resolve(requested)
        if isinstance(selected, PolicyUnit):
            return selected.module
        if isinstance(selected, PolicyUnitTombstone):
            return selected.id
        module = self._modules.resolve(requested)
        return module.module_id if module is not None and requested == module.module_id else requested

    def _direct_relationships(
        self,
        target: str,
        groups: Iterable[str] | None,
        direction: Direction,
    ) -> list[dict[str, object]]:
        if direction is Direction.INCOMING:
            views = self._graph.incoming(target, groups)
        elif direction is Direction.OUTGOING:
            views = self._graph.outgoing(target, groups)
        else:
            views = self._graph.incident(target, groups)
        return [self._relationship(view.edge, view.direction) for view in views]

    def _transitive_relationships(
        self,
        target: str,
        groups: Iterable[str],
        direction: Direction,
    ) -> list[dict[str, object]]:
        selected: dict[tuple[str, str], dict[str, object]] = {}
        for group in groups:
            traversal = self._graph.traverse_group(
                target,
                group,
                direction,
                transitive=True,
            )
            for step in traversal.steps:
                key = (step.edge.id, step.direction.value)
                selected[key] = self._relationship(step.edge, step.direction)
        return [selected[key] for key in sorted(selected)]

    def _relationship(self, edge: Edge, direction: Direction) -> dict[str, object]:
        return {
            "handle": {
                "kind": "relationship-handle",
                "id": edge.id,
                "snapshot": self._snapshot.handle,
            },
            "source": edge.source,
            "target": edge.target,
            "relation": edge.relation,
            "groups": list(edge.groups),
            "direction": direction.value,
            "traversal_eligible": edge.traversable,
            "applicability": "unknown" if "applicability" in edge.metadata else "not-declared",
        }

    def _policy_summary(
        self,
        policy_id: str,
        module: ModuleMetadata,
        scope: dict[str, object],
    ) -> dict[str, object]:
        return {
            "handle": {
                "kind": "policy-handle",
                "id": policy_id,
                "snapshot": self._snapshot.handle,
            },
            "authority": "contextual" if module.role == "reference" else "normative",
            "scope": scope,
        }

    def _navigation_handle(self, identity_value: dict[str, object]) -> dict[str, object]:
        return {
            "kind": "navigation-handle",
            "id": identity(NAVIGATION_DOMAIN, "navigation", identity_value),
            "snapshot": self._snapshot.handle,
            "schema_version": 1,
        }

    def _inspect_policy(self, requested: str) -> InspectionResult:
        target = self._resolve_policy(requested)
        if isinstance(target, RejectedResult):
            return target
        selected, module = target
        handle = {
            "kind": "policy-handle",
            "id": selected.id if isinstance(selected, PolicyUnit) else module.module_id,
            "snapshot": self._snapshot.handle,
        }
        if isinstance(selected, PolicyUnit):
            declaration = selected.as_declaration()
            representation = selected.representation_digest
            structural = selected.structural_digest
            provenance = self._provenance(selected.id, "sidecar", selected.source)
        else:
            declaration = self._module_declaration(module)
            raw = (self._root / module.path).read_bytes()
            representation = digest_bytes(raw)
            structural = markdown_structural_digest(raw)
            provenance = self._provenance(
                module.module_id,
                "canonical-document",
                module.path,
            )
        return PolicyInspectionResult.from_value(
            {
                "kind": "policy-inspection-result",
                "policy": handle,
                "declaration": declaration,
                "representation_digest": representation,
                "structural_digest": structural,
                "provenance": provenance,
            }
        )

    def _inspect_relationship(self, edge_id: str) -> InspectionResult:
        try:
            edge = self._graph.edge(edge_id)
        except GraphError as error:
            return self._graph_rejection(error)
        provenance = edge.provenance
        return RelationshipInspectionResult.from_value(
            {
                "kind": "relationship-inspection-result",
                "relationship": self._relationship(edge, Direction.OUTGOING),
                "provenance": self._provenance(
                    provenance.source_id,
                    provenance.kind,
                    provenance.locator,
                ),
            }
        )

    def _module_declaration(self, module: ModuleMetadata) -> dict[str, object]:
        return {
            "kind": "canonical-module",
            "id": module.module_id,
            "role": module.role,
            "level": module.level,
            "applies_when": module.applies_when,
            "does_not_apply_when": module.excludes,
            "requires": list(module.requires),
            "specializes": list(module.specializes),
            "verification": module.verification,
        }

    def _provenance(
        self,
        source_id: str,
        source_kind: str,
        locator: str,
    ) -> dict[str, object]:
        return {
            "source_id": source_id,
            "source_kind": source_kind,
            "locator": locator,
            "snapshot": self._snapshot.handle,
        }

    def _require_snapshot(self, observed: Mapping[str, object]) -> RejectedResult | None:
        return self._require_snapshot_value(observed)

    def _require_snapshot_value(self, observed: object) -> RejectedResult | None:
        if observed != self._snapshot.handle:
            return self._reject(
                "NAVIGATION.STALE_SNAPSHOT",
                "stale",
                "The request is not bound to this engine snapshot.",
            )
        return None

    def _graph_rejection(self, error: GraphError) -> RejectedResult:
        failure = error.failure
        outcome = "unavailable" if failure.code.startswith("GRAPH.UNKNOWN") else "invalid"
        return self._reject(
            failure.code,
            outcome,
            failure.message,
            details=dict(failure.details),
        )

    def _reject(
        self,
        code: str,
        outcome: str,
        message: str,
        *,
        target: str | None = None,
        details: Mapping[str, object] | None = None,
    ) -> RejectedResult:
        value: dict[str, object] = {
            "kind": "rejected-result",
            "code": code,
            "outcome": outcome,
            "message": message,
            "details": dict(details or {}),
            "next_operations": [],
        }
        if target:
            value["target"] = target
        return RejectedResult.from_value(value)

    def _invalid_request(self, message: str) -> RejectedResult:
        return self._reject("NAVIGATION.INVALID_REQUEST", "invalid", message)


def before_source_changed_failure() -> AnalysisFailure:
    return AnalysisFailure(
        "SNAPSHOT.SOURCE_CHANGED",
        "stale",
        "Repository inputs changed while the Standards Engine was opening.",
    )
