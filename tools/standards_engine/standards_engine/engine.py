from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

from tools.graph_engine.graph_engine import (
    Direction,
    Edge,
    EdgeRegistry,
    GraphError,
)
from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    Truth,
)
from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    AnalysisFailure,
    CoverageIndex,
    DependencyCause,
    ROUTER_PROJECTION,
    ReadingSelection,
    ReviewScope,
    RoutingBaseCause,
    RoutingRuleCause,
    RouteRule,
    RouterProjection,
    canonical_target_authority,
    compile_reading_plan,
    compile_snapshot,
    compile_coverage,
    identity,
    load_router_projection,
)
from tools.standards_graph.standards_graph import (
    POLICY_IMPACT_REGISTRY,
    METADATA_REQUIRES,
    standards_navigation_registry,
)
from tools.standards_metadata.standards_metadata import (
    CANONICAL_MODULE_CORPUS,
    POLICY_UNIT_REGISTRY,
    CanonicalStandardsCorpus,
    ModuleMetadata,
    PolicyUnit,
    PolicyUnitTombstone,
    digest_bytes,
    load_canonical_standards_corpus,
    markdown_structural_digest,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    compile_policy_impact,
    thaw,
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
    RouteRequest,
    RouteResult,
    RelationshipInspectionResult,
    SnapshotInspectionResult,
)


NAVIGATION_DOMAIN = "coding-standards:navigation:v2"
INTERFACE_SCHEMA = "tools/standards_engine/contracts/a1-contract.schema.json"


class StandardsEngine:
    """Snapshot-bound facade over canonical metadata and declared relationships."""

    def __init__(
        self,
        root: Path,
        snapshot,
        corpus: CanonicalStandardsCorpus,
        graph: EdgeRegistry,
        router: RouterProjection,
        policy_impact: CompiledPolicyImpactSet,
        coverage: CoverageIndex,
    ) -> None:
        self._root = root.resolve()
        self._snapshot = snapshot
        self._corpus = corpus
        self._modules = corpus.module_corpus
        self._policies = corpus.policy_unit_corpus
        self._graph = graph
        self._router = router
        self._policy_impact = policy_impact
        self._coverage = coverage
        self._navigation: dict[str, dict[str, object]] = {}

    @classmethod
    def open_repository(cls, root: Path) -> StandardsEngine:
        repo_root = root.resolve()
        initial_corpus = load_canonical_standards_corpus(repo_root)
        initial_policy_impact = compile_policy_impact(
            repo_root,
            initial_corpus,
            POLICY_IMPACT_REGISTRY,
        )
        initial_coverage = compile_coverage(
            repo_root,
            initial_corpus,
            initial_policy_impact,
        )
        scope = tuple(
            sorted(
                {
                    CANONICAL_MODULE_CORPUS,
                    POLICY_UNIT_REGISTRY,
                    ROUTER_PROJECTION,
                    INTERFACE_SCHEMA,
                    *initial_policy_impact.input_sources,
                    *initial_coverage.input_sources,
                    *initial_corpus.module_corpus.members,
                    *initial_corpus.policy_unit_corpus.sources,
                }
            )
        )
        before = compile_snapshot(repo_root, scope)
        corpus = load_canonical_standards_corpus(repo_root)
        policy_impact = compile_policy_impact(
            repo_root,
            corpus,
            POLICY_IMPACT_REGISTRY,
        )
        coverage = compile_coverage(
            repo_root,
            corpus,
            policy_impact,
            derived_from_snapshot=str(before.handle["id"]),
        )
        graph = standards_navigation_registry(
            repo_root,
            corpus,
            compiled_policy_impact=policy_impact,
        )
        router = load_router_projection(repo_root, corpus.module_corpus)
        after = compile_snapshot(repo_root, scope)
        if (
            before.handle != after.handle
            or initial_corpus.module_corpus.members
            != corpus.module_corpus.members
            or initial_corpus.policy_unit_corpus.sources
            != corpus.policy_unit_corpus.sources
            or initial_policy_impact.declaration_digest
            != policy_impact.declaration_digest
            or initial_coverage.horizon.digest != coverage.horizon.digest
            or {
                subject: certificate.handle
                for subject, certificate in initial_coverage.certificates.items()
            }
            != {
                subject: certificate.handle
                for subject, certificate in coverage.certificates.items()
            }
        ):
            raise AnalysisError(
                before_source_changed_failure()
            )
        return cls(
            repo_root,
            after,
            corpus,
            graph,
            router,
            policy_impact,
            coverage,
        )

    @property
    def snapshot(self) -> Mapping[str, object]:
        return self._snapshot.handle

    def query(self, call: QueryCall) -> QueryResult:
        stale = self._require_snapshot(call.snapshot)
        if stale is not None:
            return stale
        if isinstance(call.request, RouteRequest):
            if not isinstance(call.request.facts, Mapping):
                return self._invalid_request("route facts must be an object")
            return self._route(call.request)
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

    def _route(self, request: RouteRequest) -> QueryResult:
        try:
            facts = self._router.fact_schema.bind(request.facts)
            selected = set(self._router.base_modules)
            unresolved: dict[str, set[str]] = {}
            rule_results: list[tuple[RouteRule, str]] = []
            for rule in self._router.rules:
                result = rule.program.evaluate(facts)
                if result.truth is Truth.TRUE:
                    selected.add(rule.target)
                    rule_results.append((rule, "selected"))
                elif result.truth is Truth.UNKNOWN:
                    rule_results.append((rule, "unresolved"))
                    for fact in result.unresolved_facts:
                        unresolved.setdefault(fact, set()).add(rule.target)
            ordered = self._graph.dependency_order(
                METADATA_REQUIRES,
                selected=selected,
            )
            closure = set(ordered)
            preferred = (
                *(item for item in ("core", "router") if item in closure),
                *sorted(closure - selected - {"core", "router"}),
                *sorted(selected - {"core", "router"}),
            )
            ordered = self._graph.dependency_order(
                METADATA_REQUIRES,
                selected=selected,
                preferred_order=preferred,
            )
        except (AnalysisError, ApplicabilityError) as error:
            failure = error.failure
            return self._reject(
                failure.code,
                failure.outcome,
                failure.message,
                details={
                    key: value
                    for key, value in {
                        "field": failure.field,
                        "observed": failure.observed,
                    }.items()
                    if value is not None
                },
            )
        except GraphError as error:
            return self._graph_rejection(error)

        closure = set(ordered)
        rank = {target: index for index, target in enumerate(ordered)}
        scope = ReviewScope("whole-artifact")
        selections = [
            ReadingSelection(
                target,
                scope,
                RoutingBaseCause(self._router.id),
                "selected",
                0 if target in {"core", "router"} else 2,
                rank[target],
            )
            for target in self._router.base_modules
        ]
        selections.extend(
            ReadingSelection(
                rule.target,
                scope,
                RoutingRuleCause(rule.id, rule.program.referenced_facts),
                state,
                2,
                rank.get(rule.target, len(rank)),
            )
            for rule, state in rule_results
        )
        selections.extend(
            ReadingSelection(
                target,
                scope,
                DependencyCause("requires", edge.id, edge.source),
                "selected",
                0 if target in {"core", "router"} else 1,
                rank[target],
            )
            for target in ordered
            for edge in (
                view.edge
                for view in self._graph.incoming(
                    target,
                    (METADATA_REQUIRES,),
                )
            )
            if edge.source in closure
        )
        try:
            entries = compile_reading_plan(
                selections,
                lambda target: canonical_target_authority(
                    target,
                    self._corpus,
                    self._graph,
                ),
            )
        except AnalysisError as error:
            failure = error.failure
            return self._reject(
                failure.code,
                failure.outcome,
                failure.message,
                details={"observed": failure.observed}
                if failure.observed is not None
                else {},
            )
        reading_plan = [entry.as_contract() for entry in entries]
        questions = [self._route_question(fact) for fact in sorted(unresolved)]
        identity_value = {
            "handle": {"snapshot": self._snapshot.handle},
            "reading_plan": reading_plan,
            "unresolved_questions": questions,
        }
        handle = self._navigation_handle(identity_value)
        next_operations = [
            {"operation": "query", "request_kind": "read", "target": item["target"]}
            for item in reading_plan
            if item["state"] == "selected"
        ]
        if questions:
            next_operations.append({"operation": "query", "request_kind": "route"})
        value = {
            "kind": "route-result",
            "handle": handle,
            "reading_plan": reading_plan,
            "unresolved_questions": questions,
            "next_operations": next_operations,
            "summary": (
                f"Selected {len(ordered)} standards with {len(questions)} "
                "unresolved routing fact categories."
            ),
        }
        self._navigation[str(handle["id"])] = value
        return RouteResult.from_value(value)
    def _route_question(self, fact_id: str) -> dict[str, object]:
        route_fact = next(item for item in self._router.facts if item.definition.id == fact_id)
        return {
            "id": f"question.{fact_id}",
            "kind": "applicability-fact",
            "prompt": route_fact.question,
            "state": "required",
            "permitted_answers": [*route_fact.definition.values, "none"],
        }

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
        related = self._relationships_for_policy(
            selected,
            module,
            None,
            Direction.BOTH,
            transitive=False,
        )
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
            selected = self._resolve_policy(request.target)
            if isinstance(selected, RejectedResult):
                return selected
            policy, module = selected
            graph_target = policy.id if isinstance(policy, PolicyUnit) else module.module_id
            relationships = self._relationships_for_policy(
                policy,
                module,
                request.groups,
                direction,
                transitive=request.transitive,
            )
        except GraphError as error:
            return self._graph_rejection(error)
        policy_unit_mapping = self._policy_unit_mapping(policy, module)
        identity_value = {
            "handle": {"snapshot": self._snapshot.handle},
            "target": graph_target,
            "policy_unit_mapping": policy_unit_mapping,
            "relationships": relationships,
        }
        handle = self._navigation_handle(identity_value)
        value = {
            "kind": "related-result",
            "handle": handle,
            "target": graph_target,
            "policy_unit_mapping": policy_unit_mapping,
            "relationships": relationships,
            "next_operations": [
                {"operation": "inspect", "request_kind": "inspect", "target": request.target}
            ],
            "summary": f"Found {len(relationships)} declared relationships.",
        }
        self._navigation[str(handle["id"])] = value
        return RelatedResult.from_value(value)

    def _policy_unit_mapping(
        self,
        selected: PolicyUnit | ModuleMetadata,
        module: ModuleMetadata,
    ) -> dict[str, object]:
        if isinstance(selected, PolicyUnit):
            return {"state": "exact-policy-unit", "policy_units": [selected.id]}
        units = self._policies.for_module(module.module_id)
        if not units:
            return {
                "state": "incomplete",
                "reason": "no-policy-units",
                "policy_units": [],
            }
        return {
            "state": "policy-units-present",
            "policy_units": [unit.id for unit in units],
        }

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

    def _relationships_for_policy(
        self,
        selected: PolicyUnit | ModuleMetadata,
        module: ModuleMetadata,
        groups: Iterable[str] | None,
        direction: Direction,
        *,
        transitive: bool,
    ) -> list[dict[str, object]]:
        targets = (
            (selected.id,)
            if isinstance(selected, PolicyUnit)
            else (
                module.module_id,
                *(unit.id for unit in self._policies.for_module(module.module_id)),
            )
        )
        relationships: dict[tuple[str, str], dict[str, object]] = {}
        for target in targets:
            selected_relationships = (
                self._transitive_relationships(target, groups or (), direction)
                if transitive
                else self._direct_relationships(target, groups, direction)
            )
            for relationship in selected_relationships:
                handle = relationship["handle"]
                assert isinstance(handle, dict)
                key = (str(handle["id"]), str(relationship["direction"]))
                relationships[key] = relationship
        return [relationships[key] for key in sorted(relationships)]

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
            "schema_version": 2,
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
        semantics = self._policy_impact.semantics.get(edge_id)
        return RelationshipInspectionResult.from_value(
            {
                "kind": "relationship-inspection-result",
                "relationship": self._relationship(edge, Direction.OUTGOING),
                "policy_semantics": (
                    None
                    if semantics is None
                    else {
                        "edge_id": semantics.edge_id,
                        "source": semantics.source,
                        "consumer": semantics.consumer,
                        "relation": semantics.relation,
                        "applicability_program": (
                            semantics.applicability_program.as_projection()
                        ),
                        "source_scope": thaw(semantics.source_scope),
                        "consumer_scope": thaw(semantics.consumer_scope),
                        "propagation": semantics.propagation,
                        "evidence_owner": semantics.evidence_owner,
                        "rationale": semantics.rationale,
                        "declaration_source": semantics.declaration_source,
                        "dependency_fingerprint": semantics.dependency_fingerprint,
                    }
                ),
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
