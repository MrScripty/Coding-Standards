from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Iterable, Mapping, Protocol

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
    AnalysisAuthority,
    AnalysisError,
    AnalysisFailure,
    AnalysisInput,
    AnalysisResult,
    AnalysisState,
    AuthorizationReference,
    ChangeDescriptor as DomainChangeDescriptor,
    ChangeKind,
    ConsumerDispositionSubmission as DomainConsumerDispositionSubmission,
    CoverageAttestation as DomainCoverageAttestation,
    CoverageAttestationSubmission as DomainCoverageAttestationSubmission,
    CoverageEvidence,
    DecisionDependency,
    DecisionFingerprint,
    FactObservationProvider,
    EvidenceReference,
    ImpactDispositionSubmission as DomainImpactDispositionSubmission,
    ProvideFactSubmission as DomainProvideFactSubmission,
    CoverageIndex,
    DependencyCause,
    ROUTER_PROJECTION,
    ReadingSelection,
    ReviewScope,
    SemanticProposal as DomainSemanticProposal,
    RoutingBaseCause,
    RoutingRuleCause,
    RouteRule,
    RouterProjection,
    advance_analysis,
    analysis_state_from_contract,
    bind_analysis_kernel,
    bind_projection_kernel,
    canonical_json_bytes,
    canonical_target_authority,
    compile_reading_plan,
    compile_snapshot,
    compile_coverage,
    identity,
    load_router_projection,
    prepare_analysis,
    project_analysis,
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
    AnalysisState as AnalysisStateResult,
    AnalysisContextInspectionResult,
    AnalysisRequest,
    CertificateInspectionResult,
    CompleteResult,
    CoverageAttestationInspectionResult,
    CoverageAuthorityViewInspectionResult,
    CoverageRequirementInspectionResult,
    FactObservationInspectionResult,
    FactRequirementInspectionResult,
    InspectCall,
    InspectionResult,
    NavigationInspectionResult,
    PendingResult,
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


NAVIGATION_DOMAIN = "coding-standards:navigation:v3"
INTERFACE_SCHEMA = "tools/standards_engine/contracts/a1-contract.schema.json"


class AnalysisStateStore(Protocol):
    def put(self, state: AnalysisState) -> Mapping[str, object]: ...

    def get(
        self,
        handle: Mapping[str, object],
    ) -> AnalysisState | None: ...

    def values(self) -> tuple[AnalysisState, ...]: ...


class InMemoryAnalysisStateStore:
    def __init__(self) -> None:
        self._states: dict[str, AnalysisState] = {}

    def put(self, state: AnalysisState) -> Mapping[str, object]:
        existing_state = self._states.get(state.id)
        if existing_state is not None and existing_state != state:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.STATE_IDENTITY_COLLISION",
                    "invalid",
                    "one analysis-state handle resolved to different content",
                )
            )
        self._states[state.id] = state
        return state.handle

    def get(
        self,
        handle: Mapping[str, object],
    ) -> AnalysisState | None:
        state = self._states.get(str(handle.get("id", "")))
        if state is None or state.handle != dict(handle):
            return None
        return state

    def values(self) -> tuple[AnalysisState, ...]:
        return tuple(self._states[key] for key in sorted(self._states))


class DirectoryAnalysisStateStore:
    """Filesystem Adapter for immutable content-addressed analysis states."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    def put(self, state: AnalysisState) -> Mapping[str, object]:
        destination = self._path(state.handle)
        payload = canonical_json_bytes(state.as_contract())
        if destination.exists():
            existing = self.get(state.handle)
            if existing != state:
                raise AnalysisError(
                    AnalysisFailure(
                        "ANALYSIS.STATE_IDENTITY_COLLISION",
                        "invalid",
                        "one analysis handle resolved to different content",
                    )
                )
            return state.handle
        descriptor, temporary_name = tempfile.mkstemp(
            dir=self._root,
            prefix=".analysis-",
            suffix=".tmp",
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, destination)
            except FileExistsError:
                existing = self.get(state.handle)
                if existing != state:
                    raise AnalysisError(
                        AnalysisFailure(
                            "ANALYSIS.STATE_IDENTITY_COLLISION",
                            "invalid",
                            "one analysis handle resolved to different content",
                        )
                    )
            return state.handle
        finally:
            temporary.unlink(missing_ok=True)

    def get(
        self,
        handle: Mapping[str, object],
    ) -> AnalysisState | None:
        try:
            source = self._path(handle)
        except AnalysisError as error:
            if error.failure.outcome == "unsupported":
                raise
            return None
        if not source.is_file():
            return None
        try:
            value = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.STATE_CORRUPT",
                    "unavailable",
                    "persisted analysis state cannot be decoded",
                    observed=str(handle.get("id", "")),
                )
            ) from error
        if not isinstance(value, Mapping):
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.STATE_CORRUPT",
                    "unavailable",
                    "persisted analysis state is not an object",
                    observed=str(handle.get("id", "")),
                )
            )
        return analysis_state_from_contract(value)

    def values(self) -> tuple[AnalysisState, ...]:
        states = []
        for source in sorted(self._root.glob("[0-9a-f]" * 64 + ".json")):
            handle = {
                "kind": "analysis-handle",
                "id": f"analysis:sha256:{source.stem}",
                "schema_version": 3,
            }
            state = self.get(handle)
            if state is not None:
                states.append(state)
        return tuple(states)

    def _path(self, handle: Mapping[str, object]) -> Path:
        identifier = str(handle.get("id", ""))
        if (
            handle.get("kind") != "analysis-handle"
            or not identifier.startswith("analysis:sha256:")
            or len(identifier) != len("analysis:sha256:") + 64
            or any(
                character not in "0123456789abcdef" for character in identifier[-64:]
            )
        ):
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.HANDLE_INVALID",
                    "invalid",
                    "analysis handle is malformed",
                    observed=identifier,
                )
            )
        if handle.get("schema_version") != 3:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.UNSUPPORTED_VERSION",
                    "unsupported",
                    "analysis handle schema version is unsupported",
                    observed=str(handle.get("schema_version")),
                )
            )
        return self._root / f"{identifier[-64:]}.json"


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
        analysis_store: AnalysisStateStore | None = None,
        fact_providers: Iterable[FactObservationProvider] = (),
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
        self._analysis_store = analysis_store or InMemoryAnalysisStateStore()
        self._fact_providers = tuple(sorted(fact_providers, key=lambda item: item.id))
        self._navigation: dict[str, dict[str, object]] = {}
        self._sources: dict[str, StandardsEngine] = {str(snapshot.handle["id"]): self}
        self._authorizations: dict[str, AuthorizationReference] = {}

    @classmethod
    def open_repository(
        cls,
        root: Path,
        *,
        analysis_store: AnalysisStateStore | None = None,
        fact_providers: Iterable[FactObservationProvider] = (),
    ) -> StandardsEngine:
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
            or initial_corpus.module_corpus.members != corpus.module_corpus.members
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
            raise AnalysisError(before_source_changed_failure())
        return cls(
            repo_root,
            after,
            corpus,
            graph,
            router,
            policy_impact,
            coverage,
            analysis_store,
            fact_providers,
        )

    @classmethod
    def open_analysis(
        cls,
        base_root: Path,
        proposed_root: Path,
        *,
        authorizations: Iterable[AuthorizationReference] = (),
        analysis_store: AnalysisStateStore | None = None,
        fact_providers: Iterable[FactObservationProvider] = (),
    ) -> StandardsEngine:
        store = analysis_store or InMemoryAnalysisStateStore()
        providers = tuple(fact_providers)
        if len({item.id for item in providers}) != len(providers):
            raise AnalysisError(
                AnalysisFailure(
                    "FACT.PROVIDER_DUPLICATE",
                    "invalid",
                    "trusted fact providers must be unique by identity",
                )
            )
        base = cls.open_repository(
            base_root,
            analysis_store=store,
            fact_providers=providers,
        )
        proposed = cls.open_repository(
            proposed_root,
            analysis_store=store,
            fact_providers=providers,
        )
        base._sources = {
            str(base.snapshot["id"]): base,
            str(proposed.snapshot["id"]): proposed,
        }
        supplied_authorizations = tuple(authorizations)
        selected = {item.capability: item for item in supplied_authorizations}
        if len(selected) != len(supplied_authorizations):
            raise AnalysisError(
                AnalysisFailure(
                    "AUTHORIZATION.DUPLICATE_CAPABILITY",
                    "invalid",
                    "trusted analysis authorizations must be unique by capability",
                )
            )
        base._authorizations = selected
        return base

    @property
    def snapshot(self) -> Mapping[str, object]:
        return self._snapshot.handle

    @property
    def snapshots(self) -> tuple[Mapping[str, object], ...]:
        return tuple(
            source.snapshot for _snapshot_id, source in sorted(self._sources.items())
        )

    def prepare(
        self,
        request: AnalysisRequest,
    ) -> PendingResult | CompleteResult | RejectedResult:
        if request.contract_version != 2:
            return self._reject(
                "ANALYSIS.UNSUPPORTED_CONTRACT",
                "unsupported",
                "The analysis request contract version is unsupported.",
            )
        accepted = self._source_for(request.base_snapshot)
        proposed = self._source_for(request.proposed_snapshot)
        if accepted is None or proposed is None:
            return self._reject(
                "ANALYSIS.STALE_SNAPSHOT",
                "stale",
                "The analysis request references an unavailable snapshot.",
            )
        prior_state = None
        if request.prior_analysis is not None:
            try:
                prior_state = self._analysis_store.get(request.prior_analysis)
            except AnalysisError as error:
                return self._analysis_rejection(error)
            if prior_state is None:
                return self._reject(
                    "ANALYSIS.PRIOR_ANALYSIS_UNAVAILABLE",
                    "unavailable",
                    "The prior immutable analysis is unavailable.",
                    target=str(request.prior_analysis.get("id", "")),
                )
        accepted_authority = accepted._analysis_authority()
        proposed_authority = proposed._analysis_authority()
        try:
            state, result = prepare_analysis(
                accepted_authority,
                proposed_authority,
                AnalysisInput(
                    tuple(self._domain_change(item) for item in request.changes),
                    tuple(
                        self._domain_semantic_proposal(item)
                        for item in request.semantic_proposals
                    ),
                ),
                prior_state,
                authorizations=self._authorizations.values(),
                providers=self._fact_providers,
            )
        except AnalysisError as error:
            return self._analysis_rejection(error)
        self._analysis_store.put(state)
        return self._contract_analysis_result(result)

    def resolve(
        self,
        analysis: Mapping[str, object],
        submission,
    ) -> PendingResult | CompleteResult | RejectedResult:
        analysis_id = str(analysis.get("id", ""))
        try:
            state = self._analysis_store.get(analysis)
        except AnalysisError as error:
            return self._analysis_rejection(error)
        if state is None:
            return self._reject(
                "ANALYSIS.UNAVAILABLE",
                "unavailable",
                "The immutable analysis is unavailable from the state store.",
                target=analysis_id,
            )
        accepted = self._source_for(state.base_snapshot)
        proposed = self._source_for(state.proposed_snapshot)
        if accepted is None or proposed is None:
            return self._reject(
                "ANALYSIS.STALE_SNAPSHOT",
                "stale",
                "The analysis references unavailable authority snapshots.",
            )
        try:
            kernel = bind_analysis_kernel(
                accepted._analysis_authority(),
                proposed._analysis_authority(),
                state,
                authorizations=self._authorizations.values(),
                providers=self._fact_providers,
            )
        except AnalysisError as error:
            return self._analysis_rejection(error)
        submission = self._domain_submission(submission)
        capability = {
            "provide-fact": "standards.analyze",
            "consumer-disposition": "standards.review.consumer",
            "impact-disposition": "standards.review.impact",
            "coverage-attestation": "standards.review.audit",
        }.get(submission.kind)
        authorization = self._authorizations.get(str(capability))
        if authorization is None:
            return self._reject(
                "ANALYSIS.UNAUTHORIZED",
                "unauthorized",
                "The trusted engine context lacks the required capability.",
                details={"capability": str(capability)},
            )
        try:
            updated, result = advance_analysis(
                kernel,
                state,
                submission,
                authorization,
            )
        except AnalysisError as error:
            return self._analysis_rejection(error)
        self._analysis_store.put(updated)
        return self._contract_analysis_result(result)

    @staticmethod
    def _contract_analysis_result(
        result: AnalysisResult,
    ) -> PendingResult | CompleteResult:
        value = result.as_contract()
        if value.get("kind") == "pending-result":
            return PendingResult.from_value(value)
        if value.get("kind") == "complete-result":
            return CompleteResult.from_value(value)
        raise RuntimeError(
            f"analysis produced unsupported result kind {value.get('kind')!r}"
        )

    def query(self, call: QueryCall) -> QueryResult:
        source = self._source_for(call.snapshot)
        if source is None:
            return self._reject(
                "NAVIGATION.STALE_SNAPSHOT",
                "stale",
                "The request is not bound to an issued engine snapshot.",
            )
        if source is not self:
            return source.query(call)
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
        if kind == "analysis-handle":
            try:
                state = self._analysis_store.get(handle)
            except AnalysisError as error:
                return self._analysis_rejection(error)
            if state is None:
                return self._reject(
                    "ANALYSIS.UNKNOWN_HANDLE",
                    "unavailable",
                    "The immutable analysis is unavailable from the state store.",
                )
            return AnalysisStateResult.from_value(state.as_contract())
        embedded = handle.get("snapshot")
        if isinstance(embedded, Mapping):
            source = self._source_for(embedded)
            if source is None:
                return self._reject(
                    "NAVIGATION.STALE_SNAPSHOT",
                    "stale",
                    "The handle references an unavailable snapshot.",
                )
            if source is not self:
                return source.inspect(call)
        if kind == "snapshot-handle":
            source = self._source_for(handle)
            if source is None:
                return self._reject(
                    "NAVIGATION.STALE_SNAPSHOT",
                    "stale",
                    "The handle references an unavailable snapshot.",
                )
            if source is not self:
                return source.inspect(call)
            stale = self._require_snapshot(handle)
            if stale is not None:
                return stale
            return SnapshotInspectionResult.from_value(
                {
                    "kind": "snapshot-inspection-result",
                    "snapshot": self._snapshot.inspection,
                }
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
        if kind == "certificate-handle":
            certificate_id = str(handle.get("id", ""))
            certificates = {
                certificate.handle: certificate
                for source in self._sources.values()
                for certificate in source._coverage.certificates.values()
            }
            certificate = certificates.get(certificate_id)
            if certificate is None:
                return self._reject(
                    "COVERAGE.UNKNOWN_CERTIFICATE",
                    "unavailable",
                    "The coverage certificate is unavailable from the bound snapshots.",
                    target=certificate_id,
                )
            return CertificateInspectionResult.from_value(
                {
                    "kind": "certificate-inspection-result",
                    "certificate": certificate.as_projection(),
                }
            )
        coverage_inspection = self._inspect_coverage_artifact(kind, handle)
        if coverage_inspection is not None:
            return coverage_inspection
        analysis_inspection = self._inspect_analysis_artifact(kind, handle)
        if analysis_inspection is not None:
            return analysis_inspection
        return self._reject(
            "NAVIGATION.UNSUPPORTED_HANDLE",
            "unsupported",
            "The handle kind is not inspectable by the navigation slice.",
        )

    def _inspect_coverage_artifact(
        self,
        kind: object,
        handle: Mapping[str, object],
    ) -> InspectionResult | None:
        identifier = str(handle.get("id", ""))
        definitions = {
            "coverage-authority-view-handle": (
                "views",
                "coverage_view",
                "coverage-authority-view-inspection-result",
                CoverageAuthorityViewInspectionResult,
            ),
            "coverage-requirement-handle": (
                "requirements",
                "requirement",
                "coverage-requirement-inspection-result",
                CoverageRequirementInspectionResult,
            ),
            "coverage-attestation-handle": (
                "attestations",
                "attestation",
                "coverage-attestation-inspection-result",
                CoverageAttestationInspectionResult,
            ),
        }
        definition = definitions.get(str(kind))
        if definition is None:
            return None
        collection_name, field, result_kind, result_type = definition
        artifacts = {
            artifact.handle: artifact
            for source in self._sources.values()
            for artifact in getattr(source._coverage, collection_name).values()
        }
        artifact = artifacts.get(identifier)
        if artifact is None:
            return self._reject(
                "COVERAGE.UNKNOWN_ARTIFACT",
                "unavailable",
                "The coverage artifact is unavailable from the bound snapshots.",
                target=identifier,
            )
        return result_type.from_value(
            {"kind": result_kind, field: artifact.as_projection()}
        )

    def _inspect_analysis_artifact(
        self,
        kind: object,
        handle: Mapping[str, object],
    ) -> InspectionResult | None:
        definitions = {
            "analysis-context-handle": (
                "context",
                "analysis-context-inspection-result",
                AnalysisContextInspectionResult,
            ),
            "fact-requirement-handle": (
                "requirement",
                "fact-requirement-inspection-result",
                FactRequirementInspectionResult,
            ),
            "fact-observation-handle": (
                "observation",
                "fact-observation-inspection-result",
                FactObservationInspectionResult,
            ),
        }
        definition = definitions.get(str(kind))
        if definition is None:
            return None
        identifier = str(handle.get("id", ""))
        candidates: list[dict[str, object]] = []
        for state in self._analysis_store.values():
            if kind == "fact-observation-handle":
                candidates.extend(
                    observation.as_contract()
                    for observation in state.observations
                    if observation.handle["id"] == identifier
                )
                continue
            result = self._project_stored_analysis(state)
            if result is None:
                continue
            if kind == "analysis-context-handle":
                context = result.context.as_contract()
                if context["handle"]["id"] == identifier:
                    candidates.append(context)
                continue
            candidates.extend(
                requirement.as_contract()
                for requirement in getattr(result, "fact_requirements", ())
                if requirement.handle["id"] == identifier
            )
        unique = {
            canonical_json_bytes(candidate): candidate for candidate in candidates
        }
        if not unique:
            return self._reject(
                "ANALYSIS.UNKNOWN_ARTIFACT",
                "unavailable",
                "The analysis artifact is unavailable from persisted immutable states.",
                target=identifier,
            )
        if len(unique) != 1:
            raise RuntimeError(
                "one analysis artifact handle resolved to different canonical content"
            )
        field, result_kind, result_type = definition
        return result_type.from_value(
            {"kind": result_kind, field: next(iter(unique.values()))}
        )

    def _project_stored_analysis(
        self,
        state: AnalysisState,
    ) -> AnalysisResult | None:
        accepted = self._source_for(state.base_snapshot)
        proposed = self._source_for(state.proposed_snapshot)
        if accepted is None or proposed is None:
            return None
        kernel = bind_projection_kernel(
            accepted._analysis_authority(),
            proposed._analysis_authority(),
            state,
        )
        return project_analysis(kernel, state)

    def _analysis_authority(self) -> AnalysisAuthority:
        return AnalysisAuthority(
            self._root,
            self._snapshot.handle,
            self._corpus,
            self._graph,
            self._policy_impact,
            self._coverage,
        )

    @staticmethod
    def _domain_change(value) -> DomainChangeDescriptor:
        if isinstance(value, DomainChangeDescriptor):
            return value
        scope = value.scope
        return DomainChangeDescriptor(
            ChangeKind(value.kind),
            tuple(value.accepted_ids),
            tuple(value.proposed_ids),
            ReviewScope(scope.kind, tuple(getattr(scope, "heading_path", ()))),
            value.accepted_module,
            value.proposed_module,
        )

    @staticmethod
    def _domain_semantic_proposal(value) -> DomainSemanticProposal:
        if isinstance(value, DomainSemanticProposal):
            return value
        return DomainSemanticProposal(
            value.policy,
            value.accepted_semantic_revision,
            value.proposed_semantic_revision,
            value.intent,
            value.structural_digest,
        )

    @classmethod
    def _domain_submission(cls, value):
        if isinstance(
            value,
            (
                DomainProvideFactSubmission,
                DomainConsumerDispositionSubmission,
                DomainImpactDispositionSubmission,
                DomainCoverageAttestationSubmission,
            ),
        ):
            return value
        if value.kind == "provide-fact":
            return DomainProvideFactSubmission(
                dict(value.requirement),
                dict(value.value),
                cls._domain_evidence(value.evidence),
            )
        if value.kind in {"consumer-disposition", "impact-disposition"}:
            selected = (
                DomainConsumerDispositionSubmission
                if value.kind == "consumer-disposition"
                else DomainImpactDispositionSubmission
            )
            return selected(
                value.obligation_id,
                value.result,
                value.rationale,
                cls._domain_evidence(value.evidence),
                DecisionFingerprint(
                    value.fingerprint.decision_kind,
                    value.fingerprint.decision_contract,
                    tuple(
                        DecisionDependency(
                            item.class_,
                            item.identity,
                            item.digest,
                        )
                        for item in value.fingerprint.dependencies
                    ),
                    value.fingerprint.schema_version,
                ),
            )
        if value.kind == "coverage-attestation":
            attestation = value.attestation
            return DomainCoverageAttestationSubmission(
                value.obligation_id,
                DomainCoverageAttestation(
                    attestation.handle.id,
                    attestation.requirement.id,
                    attestation.conclusion,
                    tuple(
                        CoverageEvidence(
                            item.id,
                            item.digest,
                            item.provider_contract,
                            item.provider_contract_version,
                        )
                        for item in attestation.evidence
                    ),
                    tuple(
                        CoverageEvidence(
                            item.id,
                            item.digest,
                            item.provider_contract,
                            item.provider_contract_version,
                        )
                        for item in attestation.explicit_exclusions
                    ),
                    attestation.rationale,
                    attestation.auditor_provenance,
                    attestation.schema_version,
                    "agent-submission",
                ),
            )
        raise RuntimeError(f"generated submission kind {value.kind!r} is unhandled")

    @staticmethod
    def _domain_evidence(values) -> tuple[EvidenceReference, ...]:
        return tuple(
            EvidenceReference(
                item.id,
                item.digest,
                item.provider_contract,
                item.provider_contract_version,
            )
            for item in values
        )

    def _source_for(
        self,
        handle: Mapping[str, object],
    ) -> StandardsEngine | None:
        return self._sources.get(str(handle.get("id", "")))

    def _analysis_rejection(self, error: AnalysisError) -> RejectedResult:
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
                    "path": failure.path,
                }.items()
                if value is not None
            },
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
            {
                "operation": "query",
                "request_kind": "read",
                "target": item["target"],
                "snapshot": self._snapshot.handle,
            }
            for item in reading_plan
            if item["state"] == "selected"
        ]
        if questions:
            next_operations.append(
                {
                    "operation": "query",
                    "request_kind": "route",
                    "snapshot": self._snapshot.handle,
                }
            )
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
        route_fact = next(item for item in self._router.facts if item.id == fact_id)
        return {
            "id": f"question.{fact_id}",
            "kind": "applicability-fact",
            "prompt": route_fact.prompt,
            "state": "required",
            "permitted_answers": [*route_fact.values, "none"],
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
            try:
                content = self._snapshot.contents[module.path].decode("utf-8")
            except KeyError as error:
                raise RuntimeError(
                    f"snapshot content is missing canonical module {module.path!r}"
                ) from error
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
                {
                    "operation": "query",
                    "request_kind": "related",
                    "target": canonical_id,
                    "snapshot": self._snapshot.handle,
                },
                {
                    "operation": "inspect",
                    "request_kind": "inspect",
                    "target": canonical_id,
                    "snapshot": self._snapshot.handle,
                },
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
            graph_target = (
                policy.id if isinstance(policy, PolicyUnit) else module.module_id
            )
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
                {
                    "operation": "inspect",
                    "request_kind": "inspect",
                    "target": request.target,
                    "snapshot": self._snapshot.handle,
                }
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
            "applicability": "unknown"
            if "applicability" in edge.metadata
            else "not-declared",
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

    def _navigation_handle(
        self, identity_value: dict[str, object]
    ) -> dict[str, object]:
        return {
            "kind": "navigation-handle",
            "id": identity(NAVIGATION_DOMAIN, "navigation", identity_value),
            "snapshot": self._snapshot.handle,
            "schema_version": 3,
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
            raw = self._snapshot.contents[module.path]
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
                        "relationship_kind": semantics.relation,
                        "applicability": (
                            semantics.applicability_program.as_expression()
                        ),
                        "source_scope": thaw(semantics.source_scope),
                        "consumer_scope": thaw(semantics.consumer_scope),
                        "propagation": semantics.propagation,
                        "evidence_owner": semantics.evidence_owner,
                        "rationale": semantics.rationale,
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

    def _require_snapshot(
        self, observed: Mapping[str, object]
    ) -> RejectedResult | None:
        return self._require_snapshot_value(observed)

    def _require_snapshot_value(self, observed: object) -> RejectedResult | None:
        if not isinstance(observed, Mapping) or dict(observed) != self._snapshot.handle:
            return self._reject(
                "NAVIGATION.STALE_SNAPSHOT",
                "stale",
                "The request is not bound to this engine snapshot.",
            )
        return None

    def _graph_rejection(self, error: GraphError) -> RejectedResult:
        failure = error.failure
        outcome = (
            "unavailable" if failure.code.startswith("GRAPH.UNKNOWN") else "invalid"
        )
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
