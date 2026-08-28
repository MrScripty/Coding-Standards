from __future__ import annotations

import base64
import hashlib
import tempfile
import tomllib
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import Iterable, Iterator, Mapping

from tools.graph_engine.graph_engine import Direction, Edge, GraphError
from tools.standards_analysis.standards_analysis import (
    ANALYSIS_ROOT_CODEC,
    AUTHORIZATION_GRANT_CODEC,
    FACT_OBSERVATION_CODEC,
    PROVIDER_AUTHORITY_CODEC,
    AnalysisExecutionContext,
    AnalysisError,
    AnalysisFailure,
    AnalysisContextAuthority,
    AnalysisEvaluation,
    AnalysisMaterial,
    AnalysisRootAuthority,
    AuthorityEvidence,
    COVERAGE_HORIZON_CODEC,
    ROUTER_PROJECTION,
    ROUTING_PROJECTION_CODEC,
    CoverageHorizonAuthority,
    CoverageAttestationAuthority,
    CoverageCertificateAuthority,
    CoverageRequirementAuthority,
    CoverageViewAuthority,
    DependencyCause,
    FactObservationAuthority,
    FactRequirementAuthority,
    ProviderAuthority,
    ProviderNoObservation,
    ProviderObservationClaim,
    ProviderRequest,
    C7ProviderUnavailable,
    ReadingSelection,
    StoredCoverageAttestation,
    StoredObservation,
    AuthorizationRequest,
    ReviewScope,
    RoutingBaseCause,
    RoutingProjectionAuthority,
    RoutingRuleCause,
    canonical_target_authority,
    compile_reading_plan,
    compile_coverage_definitions,
    evaluate_analysis,
    construct_authorization_grant,
    load_coverage_horizon,
    load_repository_coverage_authority,
    load_router_projection,
    publish_coverage_attestation,
    publish_coverage_definitions,
)
from tools.standards_analysis.standards_analysis import (
    ChangeDescriptor as DomainChangeDescriptor,
)
from tools.standards_analysis.standards_analysis import (
    ChangeKind as DomainChangeKind,
)
from tools.standards_analysis.standards_analysis import (
    ReviewScope as DomainReviewScope,
)
from tools.standards_analysis.standards_analysis import (
    SemanticProposal as DomainSemanticProposal,
)
from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    Truth,
)
from tools.standards_authority.standards_authority import (
    AUTHORITY_CODECS,
    CONTENT_SNAPSHOT_CODEC,
    EXECUTION_CLOSURE_CODEC,
    AuthorityError,
    AuthorityHandle,
    AuthorityReference,
    AuthorityRepository,
    CaptureRequest,
    ContentSnapshot,
    ExecutionAuthorityRoot,
    ExecutionClosure,
    MemoryObjectStore,
    NativeCaptureSource,
    RepositoryPath,
    open_default_store,
)
from tools.standards_contracts.standards_contracts import MissingValue
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
)
from tools.standards_metadata.standards_metadata import (
    CANONICAL_MODULE_CORPUS,
    CANONICAL_STANDARDS_CORPUS_CODEC,
    METADATA_CODECS,
    POLICY_UNIT_REGISTRY,
    CanonicalCorpusAuthority,
    ModuleMetadata,
    PolicyUnit,
    PolicyUnitTombstone,
    load_canonical_standards_corpus,
    markdown_structural_digest,
)
from tools.standards_policy_impact.standards_policy_impact import (
    COMPILED_POLICY_IMPACT_CODEC,
    DEFAULT_REGISTRY,
    POLICY_IMPACT_CODECS,
    CompiledPolicyImpactAuthority,
    compile_policy_impact,
    thaw,
)
from tools.standards_graph.standards_graph import (
    METADATA_REQUIRES,
    STANDARDS_GRAPH_CODEC,
    STANDARDS_GRAPH_CODECS,
    StandardsGraphAuthority,
    compile_standards_graph_authority,
)

from .authority import (
    ENGINE_CODECS,
    NAVIGATION_AUTHORITY_CODEC,
    OPERATION_AUTHORITY_CODEC,
    POLICY_INSPECTION_AUTHORITY_CODEC,
    RELATIONSHIP_INSPECTION_AUTHORITY_CODEC,
    STANDARDS_AUTHORITY_VIEW_CODEC,
    NavigationAuthority,
    OperationAuthorityContract,
    OperationAuthoritySelection,
    PolicyInspectionAuthority,
    RelationshipInspectionAuthority,
    SemanticAuthoritySelection,
    StandardsAuthorityView,
    operation_contracts,
    validate_execution_authority,
    validate_standards_authority_view,
)
from ._generated_contract import (
    AnalysisContext as ContractAnalysisContext,
    AnalysisContextInspectionResult,
    AnalysisRequest,
    AnalysisState,
    CertificateInspectionResult,
    CompleteResult,
    ConsumerDispositionSubmission,
    ConsumerCoverageCertificate,
    ContentSnapshotHandle,
    ContentSnapshotInspectionResult,
    CoverageAttestation as ContractCoverageAttestation,
    CoverageAttestationInspectionResult,
    CoverageAttestationSubmission,
    CoverageAuditRequirement,
    CoverageAuthorityView,
    CoverageAuthorityViewInspectionResult,
    CoverageRequirementInspectionResult,
    FactObservation as ContractFactObservation,
    FactObservationInspectionResult,
    FactRequirement as ContractFactRequirement,
    FactRequirementInspectionResult,
    InspectCall,
    InspectionResult,
    NavigationInspectionResult,
    NavigationResult,
    PendingResult,
    ImpactDispositionSubmission,
    PolicyInspectionResult,
    QueryCall,
    ReadRequest,
    ReadResult,
    RejectedResult,
    RelatedRequest,
    RelatedResult,
    RelationshipInspectionResult,
    RouteRequest,
    RouteResult,
    ProvideFactSubmission,
    StandardsAuthorityView as ContractStandardsAuthorityView,
    StandardsAuthorityViewHandle,
)


INTERFACE_SCHEMA = "tools/standards_engine/contracts/a1-contract.schema.json"
INTERFACE_CONTRACT = "tools/standards_engine/contracts/a1-interface.toml"
ATTESTATION_REGISTRY = (
    "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml"
)
AUTHORIZATION_AUTHORITY = (
    "evaluation/standards-effectiveness/policy-coverage/authorization-authority.toml"
)
REVOCATION_AUTHORITY = (
    "evaluation/standards-effectiveness/policy-coverage/revocations.toml"
)
SUPPORTED_OPERATION_KEYS = frozenset(
    {("route", 2), ("read", 2), ("related", 2), ("analysis", 2)}
)


class StandardsEngine:
    def __init__(
        self,
        repository: AuthorityRepository,
        view: AuthorityHandle,
        analysis_views: tuple[AuthorityHandle, AuthorityHandle] | None = None,
        execution_context: AnalysisExecutionContext | None = None,
    ) -> None:
        self._repository = repository
        self._view = view
        self._analysis_views = analysis_views
        self._execution_context = execution_context or AnalysisExecutionContext()

    @classmethod
    def open_repository(
        cls,
        root: Path,
        *,
        repository: AuthorityRepository | None = None,
        durable: bool = True,
        execution_context: AnalysisExecutionContext | None = None,
    ) -> StandardsEngine:
        repo_root = root.resolve()
        initial_corpus = load_canonical_standards_corpus(repo_root)
        initial_impact = compile_policy_impact(repo_root, initial_corpus, DEFAULT_REGISTRY)
        initial_horizon = load_coverage_horizon(
            repo_root, initial_corpus, initial_impact
        )
        scope = _authority_scope(
            repo_root, initial_corpus, initial_impact.input_sources, initial_horizon.input_sources
        )
        snapshot = NativeCaptureSource(repo_root).capture(
            CaptureRequest(RepositoryPath(path.split("/")) for path in scope)
        )
        with _snapshot_workspace(snapshot) as workspace:
            corpus = load_canonical_standards_corpus(workspace)
            policy_impact = compile_policy_impact(workspace, corpus, DEFAULT_REGISTRY)
            router = load_router_projection(workspace, corpus.module_corpus)
            horizon = load_coverage_horizon(workspace, corpus, policy_impact)
        if (
            corpus.module_corpus.members != initial_corpus.module_corpus.members
            or corpus.policy_unit_corpus.sources
            != initial_corpus.policy_unit_corpus.sources
            or policy_impact.input_sources != initial_impact.input_sources
            or horizon.input_sources != initial_horizon.input_sources
        ):
            raise RuntimeError("captured authority closure differs from discovery")

        selected_repository = repository
        if selected_repository is None:
            store = open_default_store(repo_root) if durable else MemoryObjectStore()
            selected_repository = AuthorityRepository(store, _codec_sets())

        snapshot_handle = selected_repository.publish(CONTENT_SNAPSHOT_CODEC, snapshot)
        metadata_snapshot = selected_repository.publish(
            CONTENT_SNAPSHOT_CODEC,
            _snapshot_subset(
                snapshot,
                {
                    CANONICAL_MODULE_CORPUS,
                    POLICY_UNIT_REGISTRY,
                    *corpus.module_corpus.members,
                    *corpus.policy_unit_corpus.sources,
                },
            ),
        )
        policy_snapshot = selected_repository.publish(
            CONTENT_SNAPSHOT_CODEC,
            _snapshot_subset(snapshot, policy_impact.input_sources),
        )
        routing_snapshot = selected_repository.publish(
            CONTENT_SNAPSHOT_CODEC,
            _snapshot_subset(snapshot, {ROUTER_PROJECTION, router.source}),
        )
        horizon_snapshot = selected_repository.publish(
            CONTENT_SNAPSHOT_CODEC,
            _snapshot_subset(snapshot, horizon.input_sources),
        )
        metadata_handle = selected_repository.publish(
            CANONICAL_STANDARDS_CORPUS_CODEC,
            CanonicalCorpusAuthority(metadata_snapshot.reference, corpus),
        )
        policy_handle = selected_repository.publish(
            COMPILED_POLICY_IMPACT_CODEC,
            CompiledPolicyImpactAuthority(
                policy_snapshot.reference,
                metadata_handle.reference,
                policy_impact,
            ),
        )
        graph_handle = selected_repository.publish(
            STANDARDS_GRAPH_CODEC,
            compile_standards_graph_authority(
                metadata_handle.reference,
                policy_handle.reference,
                corpus,
                policy_impact,
            ),
        )
        routing_handle = selected_repository.publish(
            ROUTING_PROJECTION_CODEC,
            RoutingProjectionAuthority(
                routing_snapshot.reference, metadata_handle.reference, router
            ),
        )
        horizon_handle = selected_repository.publish(
            COVERAGE_HORIZON_CODEC,
            CoverageHorizonAuthority(
                horizon_snapshot.reference,
                metadata_handle.reference,
                policy_handle.reference,
                graph_handle.reference,
                horizon,
            ),
        )
        operation_handles = {
            contract.operation: selected_repository.publish(
                OPERATION_AUTHORITY_CODEC, contract
            )
            for contract in operation_contracts()
        }
        view_value = StandardsAuthorityView(
            snapshot_handle.reference,
            (
                OperationAuthoritySelection(operation, handle.reference)
                for operation, handle in operation_handles.items()
            ),
            (
                SemanticAuthoritySelection("metadata", metadata_handle.reference),
                SemanticAuthoritySelection("routing", routing_handle.reference),
                SemanticAuthoritySelection("graph", graph_handle.reference),
                SemanticAuthoritySelection("policy-impact", policy_handle.reference),
                SemanticAuthoritySelection("coverage", horizon_handle.reference),
            ),
        )
        validate_standards_authority_view(
            view_value, selected_repository.codec_context(), SUPPORTED_OPERATION_KEYS
        )
        view_handle = selected_repository.publish(
            STANDARDS_AUTHORITY_VIEW_CODEC, view_value
        )
        return cls(
            selected_repository,
            view_handle,
            execution_context=execution_context,
        )

    @classmethod
    def open_analysis(
        cls,
        base_root: Path,
        proposed_root: Path,
        *,
        repository: AuthorityRepository | None = None,
        durable: bool = True,
        execution_context: AnalysisExecutionContext | None = None,
    ) -> StandardsEngine:
        selected = repository
        if selected is None:
            store = (
                open_default_store(proposed_root.resolve())
                if durable
                else MemoryObjectStore()
            )
            selected = AuthorityRepository(store, _codec_sets())
        base = cls.open_repository(
            base_root,
            repository=selected,
            durable=durable,
            execution_context=execution_context,
        )
        proposed = cls.open_repository(
            proposed_root,
            repository=selected,
            durable=durable,
            execution_context=execution_context,
        )
        return cls(
            selected,
            proposed._view,
            (base._view, proposed._view),
            execution_context,
        )

    @property
    def view(self) -> StandardsAuthorityViewHandle:
        return StandardsAuthorityViewHandle.from_value(_handle(self._view))

    @property
    def snapshot(self) -> ContentSnapshotHandle:
        view = self._resolved_view()
        return ContentSnapshotHandle.from_value(_handle_ref(view.content))

    @property
    def analysis_views(
        self,
    ) -> tuple[StandardsAuthorityViewHandle, StandardsAuthorityViewHandle]:
        if self._analysis_views is None:
            raise RuntimeError("engine was not composed for analysis")
        return tuple(
            StandardsAuthorityViewHandle.from_value(_handle(item))
            for item in self._analysis_views
        )  # type: ignore[return-value]

    def covered_policy_units(self) -> frozenset[str]:
        """Return policy units backed by current repository coverage authority."""
        view = self._resolved_view()
        snapshot = self._repository.resolve_reference(view.content).value
        assert isinstance(snapshot, ContentSnapshot)
        with _snapshot_workspace(snapshot) as workspace:
            material = self._analysis_material(view, workspace)
        return frozenset(
            subject
            for subject in material.coverage.subjects
            if material.coverage.certificate_for(subject) is not None
        )

    def query(self, call: QueryCall) -> NavigationResult | RejectedResult:
        try:
            view_handle = _authority_handle(call.view)
            resolved = self._repository.resolve(view_handle)
            if not isinstance(resolved.value, StandardsAuthorityView):
                return self._reject(
                    "NAVIGATION.INVALID_VIEW",
                    "invalid",
                    "The supplied handle does not resolve to a standards authority view.",
                )
            validate_standards_authority_view(
                resolved.value,
                self._repository.codec_context(),
                SUPPORTED_OPERATION_KEYS,
            )
            request = call.request
            if isinstance(request, RouteRequest):
                return self._route(resolved.value, request)
            if isinstance(request, ReadRequest):
                return self._read(resolved.value, request)
            if isinstance(request, RelatedRequest):
                return self._related(resolved.value, request)
            return self._reject(
                "NAVIGATION.UNSUPPORTED_REQUEST",
                "unsupported",
                "The query request kind is unsupported.",
            )
        except AuthorityError as error:
            return self._authority_rejection(error)
        except ApplicabilityError as error:
            failure = error.failure
            return self._reject(failure.code, failure.outcome, failure.message)
        except GraphError as error:
            return self._reject(
                error.failure.code,
                "invalid",
                error.failure.message,
            )

    def prepare(
        self, request: AnalysisRequest
    ) -> PendingResult | CompleteResult | RejectedResult:
        try:
            base, proposed = self._analysis_view_pair(request)
            prior = None
            if not isinstance(request.prior_analysis, MissingValue):
                resolved = self._repository.resolve(
                    _authority_handle(request.prior_analysis)
                )
                if not isinstance(resolved.value, AnalysisRootAuthority):
                    return self._reject(
                        "ANALYSIS.INVALID_PRIOR",
                        "invalid",
                        "The prior analysis handle does not resolve to analysis state.",
                    )
                prior = resolved.value
            observations, dispositions, attestations = self._prior_decisions(prior)
            with self._analysis_materials(base, proposed) as (accepted, candidate):
                descriptors = tuple(_domain_change(item) for item in request.changes)
                proposals = tuple(
                    _domain_proposal(item) for item in request.semantic_proposals
                )
                evaluation = self._evaluate_with_providers(
                    accepted,
                    candidate,
                    descriptors,
                    proposals,
                    observations,
                    dispositions,
                    attestations,
                )
            return self._persist_analysis_roots(
                self._analysis_static_roots(base, proposed), evaluation
            )
        except AnalysisError as error:
            failure = error.failure
            return self._reject(failure.code, failure.outcome, failure.message)
        except AuthorityError as error:
            return self._authority_rejection(error)

    def resolve(
        self, analysis: object, submission: object
    ) -> PendingResult | CompleteResult | RejectedResult:
        try:
            resolved = self._repository.resolve(_authority_handle(analysis))
            if not isinstance(resolved.value, AnalysisRootAuthority):
                return self._reject(
                    "ANALYSIS.INVALID_HANDLE",
                    "invalid",
                    "The supplied handle does not identify analysis state.",
                )
            state = resolved.value
            observations, dispositions, attestations = self._prior_decisions(state)
            with self._analysis_materials_from_state(state) as (
                accepted,
                proposed,
                static,
            ):
                context_projection = _wire(
                    self._repository.resolve_reference(state.context).value.projection
                )
                assert isinstance(context_projection, dict)
                descriptors = tuple(
                    _domain_change_from_mapping(item)
                    for item in context_projection["changes"]
                )
                proposals = tuple(
                    _domain_proposal_from_mapping(item)
                    for item in context_projection["semantic_proposals"]
                )
                current = evaluate_analysis(
                    self._repository,
                    accepted,
                    proposed,
                    descriptors,
                    proposals,
                    observations,
                    dispositions,
                    attestations,
                )
                observations, dispositions, attestations = self._apply_submission(
                    submission,
                    current,
                    observations,
                    dispositions,
                    attestations,
                    proposed,
                )
                successor = self._evaluate_with_providers(
                    accepted,
                    proposed,
                    descriptors,
                    proposals,
                    observations,
                    dispositions,
                    attestations,
                )
            return self._persist_analysis_roots(static, successor)
        except AnalysisError as error:
            failure = error.failure
            return self._reject(failure.code, failure.outcome, failure.message)
        except AuthorityError as error:
            return self._authority_rejection(error)

    def inspect(self, call: InspectCall) -> InspectionResult | RejectedResult:
        try:
            handle = call.handle
            authority = _authority_handle(handle)
            resolved = self._repository.resolve(authority)
            value = resolved.value
            if isinstance(value, ContentSnapshot):
                return ContentSnapshotInspectionResult.from_value(
                    {
                        "kind": "content-snapshot-inspection-result",
                        "content_snapshot": _snapshot_projection(authority, value),
                    }
                )
            if isinstance(value, StandardsAuthorityView):
                return ContractStandardsAuthorityView.from_value(
                    _view_projection(authority, value)
                )
            if isinstance(value, ExecutionClosure):
                return _execution_closure_projection(authority, value)
            if isinstance(value, NavigationAuthority):
                result = self._navigation_projection(authority, value)
                return NavigationInspectionResult.from_value(
                    {"kind": "navigation-inspection-result", "navigation": result}
                )
            if isinstance(value, PolicyInspectionAuthority):
                projection = _wire(value.projection)
                assert isinstance(projection, dict)
                return PolicyInspectionResult.from_value(
                    {
                        "kind": "policy-inspection-result",
                        "policy": _handle(authority),
                        **projection,
                    }
                )
            if isinstance(value, RelationshipInspectionAuthority):
                projection = _wire(value.projection)
                assert isinstance(projection, dict)
                relationship = dict(projection["relationship"])
                relationship["handle"] = _handle(authority)
                return RelationshipInspectionResult.from_value(
                    {
                        "kind": "relationship-inspection-result",
                        **projection,
                        "relationship": relationship,
                    }
                )
            if isinstance(value, AnalysisContextAuthority):
                return AnalysisContextInspectionResult.from_value(
                    {
                        "kind": "analysis-context-inspection-result",
                        "context": self._analysis_context_projection(authority, value),
                    }
                )
            if isinstance(value, FactRequirementAuthority):
                return FactRequirementInspectionResult.from_value(
                    {
                        "kind": "fact-requirement-inspection-result",
                        "requirement": self._fact_requirement_projection(
                            authority, value
                        ),
                    }
                )
            if isinstance(value, FactObservationAuthority):
                return FactObservationInspectionResult.from_value(
                    {
                        "kind": "fact-observation-inspection-result",
                        "observation": self._fact_observation_projection(
                            authority, value
                        ),
                    }
                )
            if isinstance(value, CoverageViewAuthority):
                return CoverageAuthorityViewInspectionResult.from_value(
                    {
                        "kind": "coverage-authority-view-inspection-result",
                        "coverage_view": self._coverage_view_projection(
                            authority, value
                        ),
                    }
                )
            if isinstance(value, CoverageRequirementAuthority):
                return CoverageRequirementInspectionResult.from_value(
                    {
                        "kind": "coverage-requirement-inspection-result",
                        "requirement": self._coverage_requirement_projection(
                            authority, value
                        ),
                    }
                )
            if isinstance(value, CoverageAttestationAuthority):
                return CoverageAttestationInspectionResult.from_value(
                    {
                        "kind": "coverage-attestation-inspection-result",
                        "attestation": self._coverage_attestation_projection(
                            authority, value
                        ),
                    }
                )
            if isinstance(value, CoverageCertificateAuthority):
                return CertificateInspectionResult.from_value(
                    {
                        "kind": "certificate-inspection-result",
                        "certificate": self._coverage_certificate_projection(
                            authority, value
                        ),
                    }
                )
            if isinstance(value, AnalysisRootAuthority):
                return AnalysisState.from_value(
                    self._analysis_state_projection(authority, value)
                )
            return self._reject(
                "NAVIGATION.UNSUPPORTED_HANDLE",
                "unsupported",
                "The authority object has no public inspection projection.",
            )
        except AuthorityError as error:
            return self._authority_rejection(error)

    def _analysis_view_pair(
        self, request: AnalysisRequest
    ) -> tuple[StandardsAuthorityView, StandardsAuthorityView]:
        if request.contract_version != 3:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.UNSUPPORTED_CONTRACT",
                    "unsupported",
                    "The analysis request contract revision is unsupported.",
                )
            )
        base_handle = _authority_handle(request.base_view)
        proposed_handle = _authority_handle(request.proposed_view)
        base = self._repository.resolve(base_handle).value
        proposed = self._repository.resolve(proposed_handle).value
        if not isinstance(base, StandardsAuthorityView) or not isinstance(
            proposed, StandardsAuthorityView
        ):
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.INVALID_VIEW",
                    "invalid",
                    "Analysis requires two standards authority views.",
                )
            )
        for view in (base, proposed):
            validate_standards_authority_view(
                view, self._repository.codec_context(), SUPPORTED_OPERATION_KEYS
            )
        base_contract = next(
            item.authority
            for item in base.operation_contracts
            if item.operation == "analysis"
        )
        proposed_contract = next(
            item.authority
            for item in proposed.operation_contracts
            if item.operation == "analysis"
        )
        if base_contract != proposed_contract:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.OPERATION_CONTRACT_MISMATCH",
                    "unsupported",
                    "Accepted and proposed views select different analysis contracts.",
                )
            )
        return base, proposed

    @contextmanager
    def _analysis_materials(
        self,
        base: StandardsAuthorityView,
        proposed: StandardsAuthorityView,
    ) -> Iterator[tuple[AnalysisMaterial, AnalysisMaterial]]:
        with ExitStack() as stack:
            base_snapshot = self._repository.resolve_reference(base.content).value
            proposed_snapshot = self._repository.resolve_reference(proposed.content).value
            assert isinstance(base_snapshot, ContentSnapshot)
            assert isinstance(proposed_snapshot, ContentSnapshot)
            base_root = stack.enter_context(_snapshot_workspace(base_snapshot))
            proposed_root = stack.enter_context(_snapshot_workspace(proposed_snapshot))
            yield (
                self._analysis_material(base, base_root),
                self._analysis_material(proposed, proposed_root),
            )

    def _analysis_material(
        self, view: StandardsAuthorityView, root: Path
    ) -> AnalysisMaterial:
        references = {item.role: item.authority for item in view.authorities}
        return self._analysis_material_from_roles(
            references, root, include_repository_claims=True
        )

    def _analysis_material_from_roles(
        self,
        references: Mapping[str, AuthorityReference],
        root: Path,
        *,
        include_repository_claims: bool = False,
    ) -> AnalysisMaterial:
        metadata = self._repository.resolve_reference(references["metadata"]).value
        impact = self._repository.resolve_reference(references["policy-impact"]).value
        graph = self._repository.resolve_reference(references["graph"]).value
        horizon = self._repository.resolve_reference(references["coverage"]).value
        assert isinstance(metadata, CanonicalCorpusAuthority)
        assert isinstance(impact, CompiledPolicyImpactAuthority)
        assert isinstance(graph, StandardsGraphAuthority)
        assert isinstance(horizon, CoverageHorizonAuthority)
        definitions = compile_coverage_definitions(
            metadata.corpus, impact.compiled, horizon.horizon
        )
        coverage = publish_coverage_definitions(
            self._repository,
            definitions,
            metadata=references["metadata"],
            policy_impact=references["policy-impact"],
            graph=references["graph"],
            horizon=references["coverage"],
        )
        if include_repository_claims:
            coverage = load_repository_coverage_authority(
                root,
                self._repository,
                coverage,
            )
        return AnalysisMaterial(
            root,
            references["metadata"],
            references["graph"],
            references["policy-impact"],
            references["coverage"],
            metadata.corpus,
            graph.registry(),
            impact.compiled,
            coverage,
        )

    @contextmanager
    def _analysis_materials_from_state(
        self, state: AnalysisRootAuthority
    ) -> Iterator[
        tuple[
            AnalysisMaterial,
            AnalysisMaterial,
            tuple[
                AuthorityReference,
                Mapping[str, AuthorityReference],
                Mapping[str, AuthorityReference],
            ],
        ]
    ]:
        closure = self._repository.resolve_reference(state.closure).value
        if not isinstance(closure, ExecutionClosure) or closure.operation != "analysis":
            raise RuntimeError("analysis state closure is unavailable or contradictory")
        operation = tuple(
            item.reference
            for item in closure.roots
            if item.role == "operation-contract"
        )
        if len(operation) != 1:
            raise RuntimeError("analysis closure must select one operation contract")
        contract = self._repository.resolve_reference(operation[0]).value
        assert isinstance(contract, OperationAuthorityContract)
        validate_execution_authority(
            closure, operation[0], contract, ("accepted", "proposed")
        )
        selected: dict[str, dict[str, AuthorityReference]] = {
            "accepted": {},
            "proposed": {},
        }
        for root in closure.roots:
            if root.side in selected and root.role in {
                "metadata",
                "graph",
                "policy-impact",
                "coverage",
            }:
                selected[root.side][root.role] = root.reference
        expected = {"metadata", "graph", "policy-impact", "coverage"}
        if any(set(roles) != expected for roles in selected.values()):
            raise RuntimeError("analysis closure static role set is incomplete")
        static = operation[0], selected["accepted"], selected["proposed"]
        with ExitStack() as stack:
            workspaces = {}
            for side, roles in selected.items():
                metadata = self._repository.resolve_reference(roles["metadata"]).value
                assert isinstance(metadata, CanonicalCorpusAuthority)
                snapshot = self._repository.resolve_reference(metadata.content).value
                assert isinstance(snapshot, ContentSnapshot)
                workspaces[side] = stack.enter_context(_snapshot_workspace(snapshot))
            yield (
                self._analysis_material_from_roles(
                    selected["accepted"], workspaces["accepted"]
                ),
                self._analysis_material_from_roles(
                    selected["proposed"], workspaces["proposed"]
                ),
                static,
            )

    def _prior_decisions(
        self, prior: AnalysisRootAuthority | None
    ) -> tuple[
        tuple[StoredObservation, ...],
        tuple[Mapping[str, object], ...],
        tuple[StoredCoverageAttestation, ...],
    ]:
        if prior is None:
            return (), (), ()
        observations = []
        for reference in prior.observations:
            value = self._repository.resolve_reference(reference).value
            if not isinstance(value, FactObservationAuthority):
                raise RuntimeError("analysis observation resolved to the wrong owner type")
            observations.append(StoredObservation(reference, value))
        attestations = []
        for reference in prior.attestations:
            value = self._repository.resolve_reference(reference).value
            if not isinstance(value, CoverageAttestationAuthority):
                raise RuntimeError("analysis attestation resolved to the wrong owner type")
            attestations.append(StoredCoverageAttestation(reference, value))
        projection = _wire(prior.projection)
        assert isinstance(projection, dict)
        dispositions = tuple(
            item
            for raw in projection["dispositions"]
            for item in (dict(raw),)
        )
        return tuple(observations), dispositions, tuple(attestations)

    def _evaluate_with_providers(
        self,
        accepted: AnalysisMaterial,
        proposed: AnalysisMaterial,
        descriptors: tuple[DomainChangeDescriptor, ...],
        proposals: tuple[DomainSemanticProposal, ...],
        observations: tuple[StoredObservation, ...],
        dispositions: tuple[Mapping[str, object], ...],
        attestations: tuple[StoredCoverageAttestation, ...],
    ) -> AnalysisEvaluation:
        while True:
            evaluation = evaluate_analysis(
                self._repository,
                accepted,
                proposed,
                descriptors,
                proposals,
                observations,
                dispositions,
                attestations,
            )
            selected = self._provider_observation(
                evaluation, accepted, proposed
            )
            if selected is None:
                return evaluation
            by_requirement = {item.value.requirement: item for item in observations}
            if selected.value.requirement in by_requirement:
                raise AnalysisError(
                    AnalysisFailure(
                        "FACT.PROVIDER_CONFLICT",
                        "invalid",
                        "A provider attempted to replace an existing observation.",
                    )
                )
            by_requirement[selected.value.requirement] = selected
            observations = tuple(
                sorted(by_requirement.values(), key=lambda item: item.reference)
            )

    def _provider_observation(
        self,
        evaluation: AnalysisEvaluation,
        accepted: AnalysisMaterial,
        proposed: AnalysisMaterial,
    ) -> StoredObservation | None:
        if not self._execution_context.providers:
            return None
        static_inputs = tuple(
            sorted(
                {
                    accepted.metadata,
                    accepted.graph_authority,
                    accepted.policy_impact_authority,
                    accepted.coverage_authority,
                    proposed.metadata,
                    proposed.graph_authority,
                    proposed.policy_impact_authority,
                    proposed.coverage_authority,
                    evaluation.context,
                }
            )
        )
        for requirement in evaluation.pending_requirements:
            claims = []
            inputs = tuple(sorted({*static_inputs, requirement.reference}))
            request = ProviderRequest(
                requirement.reference, requirement.fact.id, inputs
            )
            for provider in self._execution_context.providers:
                outcome = provider.observe(request)
                if isinstance(outcome, C7ProviderUnavailable):
                    raise AnalysisError(
                        AnalysisFailure(
                            "FACT.PROVIDER_UNAVAILABLE",
                            "unavailable",
                            outcome.reason,
                        )
                    )
                if isinstance(outcome, ProviderNoObservation):
                    continue
                if not isinstance(outcome, ProviderObservationClaim):
                    raise AnalysisError(
                        AnalysisFailure(
                            "FACT.PROVIDER_RESULT_INVALID",
                            "invalid",
                            "Provider returned an unrecognized typed outcome.",
                        )
                    )
                evidence = tuple(sorted(item.reference for item in outcome.evidence))
                if any(
                    item.provider_contract != provider.evidence_contract
                    or item.provider_contract_version
                    != str(provider.semantic_revision)
                    for item in evidence
                ):
                    raise AnalysisError(
                        AnalysisFailure(
                            "FACT.PROVIDER_EVIDENCE_CONTRACT",
                            "invalid",
                            "Provider evidence does not match its declared contract.",
                        )
                    )
                claims.append((provider, outcome, evidence, inputs))
            if len(claims) > 1:
                raise AnalysisError(
                    AnalysisFailure(
                        "FACT.PROVIDER_CONFLICT",
                        "invalid",
                        "Several providers claimed one fact requirement.",
                    )
                )
            if not claims:
                continue
            provider, claim, evidence, inputs = claims[0]
            value = _contract_value(claim.value)
            proposed.policy_impact.fact_schema.bind(
                {requirement.fact.id: value}
            )
            provider_value = ProviderAuthority(
                provider.provider_id,
                provider.semantic_revision,
                provider.input_contract,
                provider.evidence_contract,
                inputs,
            )
            grant = self._authorization(
                "provide-fact",
                "fact-requirement",
                requirement.reference.semantic_id,
                requirement.fact.authorization_capability,
                evidence,
            )
            provider_handle = self._repository.publish(
                PROVIDER_AUTHORITY_CODEC, provider_value
            )
            observation = FactObservationAuthority(
                requirement.reference,
                grant.reference,
                provider_handle.reference,
                _identity(
                    {
                        "value": value,
                        "evidence": [
                            _evidence_projection(item) for item in evidence
                        ],
                    }
                ),
            )
            handle = self._repository.publish(FACT_OBSERVATION_CODEC, observation)
            return StoredObservation(handle.reference, observation)
        return None

    def _apply_submission(
        self,
        submission: object,
        current: AnalysisEvaluation,
        observations: tuple[StoredObservation, ...],
        dispositions: tuple[Mapping[str, object], ...],
        attestations: tuple[StoredCoverageAttestation, ...],
        proposed: AnalysisMaterial,
    ) -> tuple[
        tuple[StoredObservation, ...],
        tuple[Mapping[str, object], ...],
        tuple[StoredCoverageAttestation, ...],
    ]:
        if current.complete:
            raise AnalysisError(
                AnalysisFailure(
                    "SUBMISSION.NOT_APPLICABLE",
                    "invalid",
                    "A complete analysis has no current work.",
                )
            )
        if isinstance(submission, ProvideFactSubmission):
            reference = AuthorityReference(
                "fact-requirement", submission.requirement.id
            )
            matches = tuple(
                item
                for item in current.pending_requirements
                if item.reference == reference
            )
            if len(matches) != 1:
                raise _submission_not_applicable("fact requirement")
            requirement = matches[0]
            evidence = _authority_evidence(submission.evidence)
            grant = self._authorization(
                "provide-fact",
                "fact-requirement",
                reference.semantic_id,
                requirement.fact.authorization_capability,
                evidence,
            )
            value = _contract_value(submission.value)
            proposed.policy_impact.fact_schema.bind({requirement.fact.id: value})
            observation = FactObservationAuthority(
                reference,
                grant.reference,
                None,
                _identity(
                    {
                        "value": value,
                        "evidence": [_evidence_projection(item) for item in evidence],
                    }
                ),
            )
            handle = self._repository.publish(FACT_OBSERVATION_CODEC, observation)
            selected = {item.value.requirement: item for item in observations}
            selected[reference] = StoredObservation(handle.reference, observation)
            return (
                tuple(sorted(selected.values(), key=lambda item: item.reference)),
                dispositions,
                attestations,
            )

        obligation_id = getattr(submission, "obligation_id", "")
        matches = tuple(
            item
            for item in current.obligations
            if item.id == obligation_id and item.state != "resolved"
        )
        if len(matches) != 1:
            raise _submission_not_applicable("obligation")
        obligation = matches[0]
        if submission.kind not in obligation.permitted_submissions:
            raise _submission_not_applicable("submission kind")

        if isinstance(submission, CoverageAttestationSubmission):
            coverage = next(
                item for item in current.coverage if item.subject == obligation.target
            )
            if submission.claim.requirement.id != coverage.requirement.semantic_id:
                raise AnalysisError(
                    AnalysisFailure(
                        "SUBMISSION.CONTEXT_MISMATCH",
                        "invalid",
                        "Coverage claim does not bind the current requirement.",
                    )
                )
            evidence = _authority_evidence(
                (*submission.claim.evidence, *submission.claim.explicit_exclusions)
            )
            grant = self._authorization(
                "coverage-attestation",
                "coverage-requirement",
                coverage.requirement.semantic_id,
                "standards.review.audit",
                evidence,
            )
            attestation = publish_coverage_attestation(
                self._repository,
                requirement=coverage.requirement,
                authorization=grant.reference,
                conclusion=submission.claim.conclusion,
                evidence=_authority_evidence(submission.claim.evidence),
                explicit_exclusions=_authority_evidence(
                    submission.claim.explicit_exclusions
                ),
                rationale=submission.claim.rationale,
                auditor_provenance=submission.claim.auditor_provenance,
            )
            selected = {item.value.requirement: item for item in attestations}
            selected[coverage.requirement] = attestation
            return (
                observations,
                dispositions,
                tuple(sorted(selected.values(), key=lambda item: item.reference)),
            )

        if not isinstance(
            submission, (ConsumerDispositionSubmission, ImpactDispositionSubmission)
        ):
            raise _submission_not_applicable("submission")
        if submission.fingerprint.as_contract() != obligation.fingerprint.as_contract():
            raise AnalysisError(
                AnalysisFailure(
                    "SUBMISSION.CONTEXT_MISMATCH",
                    "invalid",
                    "Disposition dependencies do not match current work.",
                )
            )
        evidence = _authority_evidence(submission.evidence)
        subject_kind = (
            "consumer-obligation"
            if isinstance(submission, ConsumerDispositionSubmission)
            else "impact-obligation"
        )
        capability = (
            str(obligation.review_contract["authorization_capability"])
            if obligation.review_contract is not None
            else "standards.review.impact"
        )
        grant = self._authorization(
            submission.kind,
            subject_kind,
            obligation.id,
            capability,
            evidence,
        )
        record = {
            "obligation_id": obligation.id,
            "kind": submission.kind,
            "result": submission.result,
            "rationale": submission.rationale,
            "evidence": [_evidence_projection(item) for item in evidence],
            "authorization": _authority_reference(grant.reference),
            "fingerprint": submission.fingerprint.as_contract(),
        }
        selected = {str(item["obligation_id"]): item for item in dispositions}
        selected[obligation.id] = record
        return observations, tuple(selected[key] for key in sorted(selected)), attestations

    def _authorization(
        self,
        action: str,
        subject_kind: str,
        subject_id: str,
        capability: str,
        evidence: tuple[AuthorityEvidence, ...],
    ) -> AuthorityHandle:
        grant = construct_authorization_grant(
            self._execution_context,
            AuthorizationRequest(
                action, subject_kind, subject_id, capability, evidence
            ),
        )
        return self._repository.publish(AUTHORIZATION_GRANT_CODEC, grant)

    @staticmethod
    def _analysis_static_roots(
        base: StandardsAuthorityView, proposed: StandardsAuthorityView
    ) -> tuple[
        AuthorityReference,
        Mapping[str, AuthorityReference],
        Mapping[str, AuthorityReference],
    ]:
        operation = next(
            item.authority
            for item in proposed.operation_contracts
            if item.operation == "analysis"
        )
        return (
            operation,
            {item.role: item.authority for item in base.authorities},
            {item.role: item.authority for item in proposed.authorities},
        )

    def _persist_analysis_roots(
        self,
        static: tuple[
            AuthorityReference,
            Mapping[str, AuthorityReference],
            Mapping[str, AuthorityReference],
        ],
        evaluation: AnalysisEvaluation,
    ) -> PendingResult | CompleteResult:
        operation, base_roles, proposed_roles = static
        roots = [ExecutionAuthorityRoot("current", "operation-contract", operation)]
        for side, roles in (("accepted", base_roles), ("proposed", proposed_roles)):
            roots.extend(
                ExecutionAuthorityRoot(side, role, roles[role])
                for role in ("metadata", "graph", "policy-impact", "coverage")
            )
        roots.append(
            ExecutionAuthorityRoot("current", "context", evaluation.context)
        )
        roots.extend(
            ExecutionAuthorityRoot("current", "requirement", item.reference)
            for item in evaluation.requirements
        )
        roots.extend(
            ExecutionAuthorityRoot("current", "observation", item.reference)
            for item in evaluation.observations
        )
        roots.extend(
            ExecutionAuthorityRoot("current", "coverage-view", item.view)
            for item in evaluation.coverage
        )
        roots.extend(
            ExecutionAuthorityRoot("current", "coverage-requirement", item.requirement)
            for item in evaluation.coverage
        )
        roots.extend(
            ExecutionAuthorityRoot(
                "current", "coverage-certificate", item.certificate
            )
            for item in evaluation.coverage
            if item.certificate is not None
        )
        roots.extend(
            ExecutionAuthorityRoot("current", "coverage-attestation", item.reference)
            for item in evaluation.attestations
        )
        trust = self._analysis_trust_roots(evaluation)
        roots.extend(trust)
        closure_value = ExecutionClosure("analysis", roots)
        contract = self._repository.resolve_reference(operation).value
        assert isinstance(contract, OperationAuthorityContract)
        validate_execution_authority(
            closure_value, operation, contract, ("accepted", "proposed")
        )
        closure = self._repository.publish(EXECUTION_CLOSURE_CODEC, closure_value)
        state = AnalysisRootAuthority(
            closure.reference,
            evaluation.context,
            tuple(item.reference for item in evaluation.observations),
            tuple(item.reference for item in evaluation.attestations),
            _identity(
                {
                    "dispositions": [dict(item) for item in evaluation.dispositions]
                }
            ),
        )
        handle = self._repository.publish(ANALYSIS_ROOT_CODEC, state)
        return self._analysis_result(handle, closure, evaluation)

    def _analysis_trust_roots(
        self, evaluation: AnalysisEvaluation
    ) -> tuple[ExecutionAuthorityRoot, ...]:
        roots: set[ExecutionAuthorityRoot] = set()
        for item in evaluation.observations:
            roots.add(
                ExecutionAuthorityRoot(
                    "current", "authorization-grant", item.value.authorization
                )
            )
            if item.value.provider is not None:
                roots.add(
                    ExecutionAuthorityRoot(
                        "current", "provider-authority", item.value.provider
                    )
                )
        for item in evaluation.attestations:
            roots.add(
                ExecutionAuthorityRoot(
                    "current", "authorization-grant", item.value.authorization
                )
            )
        for disposition in evaluation.dispositions:
            raw = disposition.get("authorization")
            if isinstance(raw, Mapping):
                roots.add(
                    ExecutionAuthorityRoot(
                        "current",
                        "authorization-grant",
                        AuthorityReference(str(raw["object_kind"]), str(raw["id"])),
                    )
                )
        return tuple(sorted(roots))

    def _analysis_result(
        self,
        handle: AuthorityHandle,
        closure: AuthorityHandle,
        evaluation: AnalysisEvaluation,
    ) -> PendingResult | CompleteResult:
        context = self._analysis_context_projection(
            AuthorityHandle(
                evaluation.context.object_kind, evaluation.context.semantic_id
            ),
            evaluation.context_value,
        )
        changes = [item.descriptor.as_contract() for item in evaluation.changes]
        changed_units = [
            unit.as_contract()
            for change in evaluation.changes
            for unit in change.changed_units
        ]
        reading_plan = [item.as_contract() for item in evaluation.reading_plan]
        if not evaluation.complete:
            requirements = [
                {
                    "requirement": self._fact_requirement_projection(
                        AuthorityHandle(
                            item.reference.object_kind,
                            item.reference.semantic_id,
                        ),
                        item.value,
                    ),
                    "prompt": item.prompt,
                    "dependent_programs": list(item.dependent_programs),
                }
                for item in evaluation.pending_requirements
            ]
            obligations = [
                item.as_contract()
                for item in evaluation.obligations
                if item.state != "resolved"
            ]
            return PendingResult.from_value(
                {
                    "kind": "pending-result",
                    "handle": _handle(handle),
                    "status": "needs-action",
                    "context": context,
                    "changes": changes,
                    "changed_units": changed_units,
                    "obligations": obligations,
                    "fact_requirements": requirements,
                    "reading_plan": reading_plan,
                    "next_operations": _analysis_next_operations(
                        handle, evaluation.pending_requirements, evaluation.obligations
                    ),
                    "authority": _handle(closure),
                    "summary": "The bounded analysis requires additional decisions.",
                }
            )
        consumer_ids = sorted(
            item.id
            for item in evaluation.reached_obligations
            if item.kind == "consumer-review"
        )
        disposition_ids = sorted(
            str(item["obligation_id"])
            for item in evaluation.dispositions
            if item["kind"] == "consumer-disposition"
        )
        required_facts = sorted(item.reference.semantic_id for item in evaluation.requirements)
        observed = {
            item.value.requirement.semantic_id for item in evaluation.observations
        }
        observed_facts = sorted(set(required_facts) & observed)
        certificates = [
            _handle_ref(item.certificate)
            for item in evaluation.coverage
            if item.certificate is not None
        ]
        subjects = sorted(item.subject for item in evaluation.coverage)
        certificate_subjects = sorted(
            item.subject for item in evaluation.coverage if item.certificate is not None
        )
        return CompleteResult.from_value(
            {
                "kind": "complete-result",
                "handle": _handle(handle),
                "status": "complete",
                "context": context,
                "changes": changes,
                "changed_units": changed_units,
                "coverage_certificates": certificates,
                "fact_observations": [
                    self._fact_observation_projection(
                        AuthorityHandle(
                            item.reference.object_kind, item.reference.semantic_id
                        ),
                        item.value,
                    )
                    for item in evaluation.observations
                ],
                "dispositions": [dict(item) for item in evaluation.dispositions],
                "reading_plan": reading_plan,
                "completion": {
                    "required_coverage_subjects": subjects,
                    "certificate_subjects": certificate_subjects,
                    "reached_consumer_obligations": consumer_ids,
                    "disposition_obligations": disposition_ids,
                    "required_fact_requirements": required_facts,
                    "observed_fact_requirements": observed_facts,
                    "non_consumer_obligations_resolved": True,
                    "applicability_resolved": True,
                    "authorization_valid": True,
                    "evidence_valid": True,
                },
                "authority": _handle(closure),
                "summary": "The bounded read-only impact analysis is complete.",
            }
        )

    def _route(
        self, view: StandardsAuthorityView, request: RouteRequest
    ) -> RouteResult | RejectedResult:
        try:
            values = self._view_values(view)
            corpus = values["metadata"].corpus
            router = values["routing"].projection
            graph = values["graph"].registry()
            facts = router.fact_schema.bind(dict(request.facts))
            selected = set(router.base_modules)
            unresolved: dict[str, set[str]] = {}
            rule_results = []
            for rule in router.rules:
                result = rule.program.evaluate(facts)
                if result.truth is Truth.TRUE:
                    selected.add(rule.target)
                    rule_results.append((rule, "selected"))
                elif result.truth is Truth.UNKNOWN:
                    rule_results.append((rule, "unresolved"))
                    for fact in result.unresolved_facts:
                        unresolved.setdefault(fact, set()).add(rule.target)
            ordered = graph.dependency_order(METADATA_REQUIRES, selected=selected)
            closure_nodes = set(ordered)
            preferred = (
                *(item for item in ("core", "router") if item in closure_nodes),
                *sorted(closure_nodes - selected - {"core", "router"}),
                *sorted(selected - {"core", "router"}),
            )
            ordered = graph.dependency_order(
                METADATA_REQUIRES, selected=selected, preferred_order=preferred
            )
            closure_nodes = set(ordered)
            rank = {target: index for index, target in enumerate(ordered)}
            scope = ReviewScope("whole-artifact")
            selections = [
                ReadingSelection(
                    target,
                    scope,
                    RoutingBaseCause(router.id),
                    "selected",
                    0 if target in {"core", "router"} else 2,
                    rank[target],
                )
                for target in router.base_modules
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
                    item.edge
                    for item in graph.incoming(target, (METADATA_REQUIRES,))
                )
                if edge.source in closure_nodes
            )
            entries = compile_reading_plan(
                selections,
                lambda target: canonical_target_authority(target, corpus, graph),
            )
        except (GraphError, ValueError) as error:
            return self._reject("NAVIGATION.INVALID_ROUTE", "invalid", str(error))

        reading_plan = [item.as_contract() for item in entries]
        questions = [
            self._route_question(router, fact) for fact in sorted(unresolved)
        ]
        closure = self._operation_closure(view, "route")
        semantic = {
            "reading_plan": reading_plan,
            "unresolved_questions": questions,
        }
        navigation = self._repository.publish(
            NAVIGATION_AUTHORITY_CODEC,
            NavigationAuthority(
                "route", _identity(request.as_contract()), _identity(semantic), closure.reference
            ),
        )
        value = {
            "kind": "route-result",
            "handle": _handle(navigation),
            "authority": _handle(closure),
            **semantic,
            "next_operations": [
                {
                    "operation": "query",
                    "request_kind": "read",
                    "target": item["target"],
                    "view": _handle(self._view),
                }
                for item in reading_plan
                if item["state"] == "selected"
            ],
            "summary": f"Selected {len(ordered)} standards with {len(questions)} unresolved fact categories.",
        }
        return RouteResult.from_value(value)

    def _read(
        self, view: StandardsAuthorityView, request: ReadRequest
    ) -> ReadResult | RejectedResult:
        values = self._view_values(view)
        corpus = values["metadata"].corpus
        selected = _resolve_policy(corpus, request.target)
        if selected is None:
            return self._reject(
                "NAVIGATION.UNKNOWN_POLICY", "unavailable", "The policy is unavailable."
            )
        policy, module = selected
        closure = self._operation_closure(view, "read")
        policy_projection, policy_handle = self._policy_inspection(
            view, closure, policy, module
        )
        relationships = self._relationships(
            view, closure, policy, module, None, Direction.BOTH, False
        )
        if isinstance(policy, PolicyUnit):
            content = policy.content
            scope = {"kind": "structured", "heading_path": list(policy.heading_path)}
        else:
            snapshot = self._repository.resolve_reference(view.content).value
            content = _snapshot_files(snapshot)[module.path].decode("utf-8")
            scope = {"kind": "whole-artifact"}
        summary = {
            "handle": _handle(policy_handle),
            "authority": "contextual" if module.role == "reference" else "normative",
            "scope": scope,
        }
        semantic = {
            "policy": summary,
            "content": content,
            "requires": list(module.requires),
            "specializes": list(module.specializes),
            "related": relationships,
        }
        navigation = self._repository.publish(
            NAVIGATION_AUTHORITY_CODEC,
            NavigationAuthority(
                "read", _identity(request.as_contract()), _identity(semantic), closure.reference
            ),
        )
        target = policy.id if isinstance(policy, PolicyUnit) else module.module_id
        return ReadResult.from_value(
            {
                "kind": "read-result",
                "handle": _handle(navigation),
                "authority": _handle(closure),
                **semantic,
                "next_operations": [
                    {
                        "operation": "query",
                        "request_kind": "related",
                        "target": target,
                        "view": _handle(self._view),
                    },
                    {
                        "operation": "inspect",
                        "request_kind": "inspect",
                        "target": policy_projection["policy"]["id"],
                        "view": _handle(self._view),
                    },
                ],
                "summary": f"Read canonical standard {target}.",
            }
        )

    def _related(
        self, view: StandardsAuthorityView, request: RelatedRequest
    ) -> RelatedResult | RejectedResult:
        values = self._view_values(view)
        corpus = values["metadata"].corpus
        selected = _resolve_policy(corpus, request.target)
        if selected is None:
            return self._reject(
                "NAVIGATION.UNKNOWN_POLICY", "unavailable", "The policy is unavailable."
            )
        policy, module = selected
        closure = self._operation_closure(view, "related")
        relationships = self._relationships(
            view,
            closure,
            policy,
            module,
            tuple(request.groups),
            Direction.parse(request.direction),
            request.transitive,
        )
        target = policy.id if isinstance(policy, PolicyUnit) else module.module_id
        units = corpus.policy_unit_corpus.for_module(module.module_id)
        mapping = (
            {"state": "exact-policy-unit", "policy_units": [policy.id]}
            if isinstance(policy, PolicyUnit)
            else {
                "state": "policy-units-present" if units else "incomplete",
                **({} if units else {"reason": "no-policy-units"}),
                "policy_units": [item.id for item in units],
            }
        )
        semantic = {
            "target": target,
            "policy_unit_mapping": mapping,
            "relationships": relationships,
        }
        navigation = self._repository.publish(
            NAVIGATION_AUTHORITY_CODEC,
            NavigationAuthority(
                "related", _identity(request.as_contract()), _identity(semantic), closure.reference
            ),
        )
        return RelatedResult.from_value(
            {
                "kind": "related-result",
                "handle": _handle(navigation),
                "authority": _handle(closure),
                **semantic,
                "next_operations": [],
                "summary": f"Found {len(relationships)} declared relationships.",
            }
        )

    def _operation_closure(
        self, view: StandardsAuthorityView, operation: str
    ) -> AuthorityHandle:
        operation_reference = next(
            item.authority for item in view.operation_contracts if item.operation == operation
        )
        contract = self._repository.resolve_reference(operation_reference).value
        assert isinstance(contract, OperationAuthorityContract)
        roles = {item.role: item.authority for item in view.authorities}
        roots = [
            ExecutionAuthorityRoot("current", "operation-contract", operation_reference)
        ]
        roots.extend(
            ExecutionAuthorityRoot("current", requirement.role, roles[requirement.role])
            for requirement in contract.required_view_roles
        )
        closure = ExecutionClosure(operation, roots)
        validate_execution_authority(
            closure, operation_reference, contract, ("current",)
        )
        return self._repository.publish(EXECUTION_CLOSURE_CODEC, closure)

    def _view_values(self, view: StandardsAuthorityView) -> dict[str, object]:
        return {
            item.role: self._repository.resolve_reference(item.authority).value
            for item in view.authorities
        }

    def _relationships(
        self,
        view: StandardsAuthorityView,
        closure: AuthorityHandle,
        selected: PolicyUnit | ModuleMetadata,
        module: ModuleMetadata,
        groups: tuple[str, ...] | None,
        direction: Direction,
        transitive: bool,
    ) -> list[dict[str, object]]:
        values = self._view_values(view)
        graph = values["graph"].registry()
        targets = (
            (selected.id,)
            if isinstance(selected, PolicyUnit)
            else (
                module.module_id,
                *(item.id for item in values["metadata"].corpus.policy_unit_corpus.for_module(module.module_id)),
            )
        )
        chosen: dict[tuple[str, str], dict[str, object]] = {}
        for target in targets:
            if transitive:
                steps = [
                    step
                    for group in groups or ()
                    for step in graph.traverse_group(
                        target, group, direction, transitive=True
                    ).steps
                ]
                pairs = ((item.edge, item.direction) for item in steps)
            else:
                views = (
                    graph.incoming(target, groups)
                    if direction is Direction.INCOMING
                    else graph.outgoing(target, groups)
                    if direction is Direction.OUTGOING
                    else graph.incident(target, groups)
                )
                pairs = ((item.edge, item.direction) for item in views)
            for edge, selected_direction in pairs:
                projection, handle = self._relationship_inspection(
                    view, closure, edge, selected_direction
                )
                summary = dict(projection["relationship"])
                summary["handle"] = _handle(handle)
                chosen[(edge.id, selected_direction.value)] = summary
        return [chosen[key] for key in sorted(chosen)]

    def _policy_inspection(
        self,
        view: StandardsAuthorityView,
        closure: AuthorityHandle,
        selected: PolicyUnit | ModuleMetadata,
        module: ModuleMetadata,
    ) -> tuple[dict[str, object], AuthorityHandle]:
        metadata_reference = next(
            item.authority for item in view.authorities if item.role == "metadata"
        )
        snapshot = self._repository.resolve_reference(view.content).value
        if isinstance(selected, PolicyUnit):
            declaration = selected.as_declaration()
            representation = selected.representation_digest
            structural = selected.structural_digest
            source_id, source_kind, locator = selected.id, "sidecar", selected.source
        else:
            raw = _snapshot_files(snapshot)[module.path]
            declaration = _module_declaration(module)
            representation = f"sha256:{hashlib.sha256(raw).hexdigest()}"
            structural = markdown_structural_digest(raw)
            source_id, source_kind, locator = module.module_id, "canonical-document", module.path
        projection = {
            "declaration": declaration,
            "representation_digest": representation,
            "structural_digest": structural,
            "provenance": {
                "source_id": source_id,
                "source_kind": source_kind,
                "locator": locator,
                "content_snapshot": _handle_ref(view.content),
            },
        }
        authority = self._repository.publish(
            POLICY_INSPECTION_AUTHORITY_CODEC,
            PolicyInspectionAuthority(
                source_id,
                _identity(projection),
                closure.reference,
                metadata_reference,
            ),
        )
        return {
            "kind": "policy-inspection-result",
            "policy": _handle(authority),
            **projection,
        }, authority

    def _relationship_inspection(
        self,
        view: StandardsAuthorityView,
        closure: AuthorityHandle,
        edge: Edge,
        direction: Direction,
    ) -> tuple[dict[str, object], AuthorityHandle]:
        values = self._view_values(view)
        graph_reference = next(item.authority for item in view.authorities if item.role == "graph")
        impact_reference = next(item.authority for item in view.authorities if item.role == "policy-impact")
        impact = values["policy-impact"].compiled
        semantics = impact.semantics.get(edge.id)
        summary = {
            "source": edge.source,
            "target": edge.target,
            "relation": edge.relation,
            "groups": list(edge.groups),
            "direction": direction.value,
            "traversal_eligible": edge.traversable,
            "applicability": "unknown" if semantics is not None else "not-declared",
        }
        projection = {
            "kind": "relationship-inspection-result",
            "relationship": summary,
            "policy_semantics": None
            if semantics is None
            else {
                "relationship_kind": semantics.relation,
                "applicability": semantics.applicability_program.as_expression(),
                "source_scope": thaw(semantics.source_scope),
                "consumer_scope": thaw(semantics.consumer_scope),
                "propagation": semantics.propagation,
                "evidence_owner": semantics.evidence_owner,
                "rationale": semantics.rationale,
            },
            "provenance": {
                "source_id": edge.provenance.source_id,
                "source_kind": edge.provenance.kind,
                "locator": edge.provenance.locator,
                "content_snapshot": _handle_ref(view.content),
            },
        }
        authority = self._repository.publish(
            RELATIONSHIP_INSPECTION_AUTHORITY_CODEC,
            RelationshipInspectionAuthority(
                edge.id,
                _identity(projection),
                closure.reference,
                graph_reference,
                impact_reference,
            ),
        )
        return {
            **projection,
            "relationship": {"handle": _handle(authority), **summary},
        }, authority

    def _navigation_projection(
        self, handle: AuthorityHandle, value: NavigationAuthority
    ) -> dict[str, object]:
        semantic = _wire(value.semantic_result)
        assert isinstance(semantic, dict)
        base = {
            "kind": f"{value.operation}-result",
            "handle": _handle(handle),
            "authority": _handle_ref(value.authority),
            **semantic,
            "next_operations": [],
        }
        if value.operation == "route":
            return RouteResult.from_value(base).as_contract()
        if value.operation == "read":
            return ReadResult.from_value(base).as_contract()
        return RelatedResult.from_value(base).as_contract()

    @staticmethod
    def _analysis_context_projection(
        handle: AuthorityHandle, value: AnalysisContextAuthority
    ) -> dict[str, object]:
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        return ContractAnalysisContext.from_value(
            {
                "kind": "analysis-context",
                "handle": _handle(handle),
                **projection,
            }
        ).as_contract()

    @staticmethod
    def _fact_requirement_projection(
        handle: AuthorityHandle, value: FactRequirementAuthority
    ) -> dict[str, object]:
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        return ContractFactRequirement.from_value(
            {
                "kind": "fact-requirement",
                "handle": _handle(handle),
                "context": _handle_ref(value.context),
                **projection,
                "authority_dependencies": [
                    _authority_reference(item)
                    for item in sorted((value.context, value.policy_impact))
                ],
            }
        ).as_contract()

    @staticmethod
    def _fact_observation_projection(
        handle: AuthorityHandle, value: FactObservationAuthority
    ) -> dict[str, object]:
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        public = {
            "kind": "fact-observation",
            "handle": _handle(handle),
            "requirement": _handle_ref(value.requirement),
            **projection,
            "authorization": _authority_reference(value.authorization),
        }
        if value.provider is not None:
            public["provider_authority"] = _authority_reference(value.provider)
        return ContractFactObservation.from_value(public).as_contract()

    @staticmethod
    def _coverage_view_projection(
        handle: AuthorityHandle, value: CoverageViewAuthority
    ) -> dict[str, object]:
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        dependencies = sorted(
            (value.metadata, value.policy_impact, value.graph, value.horizon)
        )
        return CoverageAuthorityView.from_value(
            {
                "kind": "coverage-authority-view",
                "handle": _handle(handle),
                **projection,
                "authority_dependencies": [
                    _authority_reference(item) for item in dependencies
                ],
            }
        ).as_contract()

    @staticmethod
    def _coverage_requirement_projection(
        handle: AuthorityHandle, value: CoverageRequirementAuthority
    ) -> dict[str, object]:
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        return CoverageAuditRequirement.from_value(
            {
                "kind": "coverage-audit-requirement",
                "handle": _handle(handle),
                "coverage_view": _handle_ref(value.coverage_view),
                **projection,
            }
        ).as_contract()

    @staticmethod
    def _coverage_attestation_projection(
        handle: AuthorityHandle, value: CoverageAttestationAuthority
    ) -> dict[str, object]:
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        return ContractCoverageAttestation.from_value(
            {
                "kind": "coverage-attestation",
                "handle": _handle(handle),
                "requirement": _handle_ref(value.requirement),
                **projection,
                "authorization": _authority_reference(value.authorization),
            }
        ).as_contract()

    @staticmethod
    def _coverage_certificate_projection(
        handle: AuthorityHandle, value: CoverageCertificateAuthority
    ) -> dict[str, object]:
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        dependencies = sorted(
            (value.coverage_view, value.requirement, value.attestation)
        )
        return ConsumerCoverageCertificate.from_value(
            {
                "kind": "consumer-coverage-certificate",
                "handle": _handle(handle),
                "coverage_view": _handle_ref(value.coverage_view),
                "requirement": _handle_ref(value.requirement),
                "attestation": _handle_ref(value.attestation),
                **projection,
                "authority_dependencies": [
                    _authority_reference(item) for item in dependencies
                ],
            }
        ).as_contract()

    def _analysis_state_projection(
        self, handle: AuthorityHandle, value: AnalysisRootAuthority
    ) -> dict[str, object]:
        context = self._repository.resolve_reference(value.context).value
        assert isinstance(context, AnalysisContextAuthority)
        observations = []
        for reference in value.observations:
            observation = self._repository.resolve_reference(reference).value
            assert isinstance(observation, FactObservationAuthority)
            observations.append(
                self._fact_observation_projection(
                    AuthorityHandle(reference.object_kind, reference.semantic_id),
                    observation,
                )
            )
        attestations = []
        for reference in value.attestations:
            attestation = self._repository.resolve_reference(reference).value
            assert isinstance(attestation, CoverageAttestationAuthority)
            attestations.append(
                self._coverage_attestation_projection(
                    AuthorityHandle(reference.object_kind, reference.semantic_id),
                    attestation,
                )
            )
        projection = _wire(value.projection)
        assert isinstance(projection, dict)
        return {
            "kind": "analysis-state",
            "handle": _handle(handle),
            "context": self._analysis_context_projection(
                AuthorityHandle(
                    value.context.object_kind, value.context.semantic_id
                ),
                context,
            ),
            "fact_observations": observations,
            "dispositions": projection["dispositions"],
            "coverage_attestations": attestations,
            "authority": _handle_ref(value.closure),
        }

    def _resolved_view(self) -> StandardsAuthorityView:
        value = self._repository.resolve(self._view).value
        assert isinstance(value, StandardsAuthorityView)
        return value

    @staticmethod
    def _route_question(router: object, fact_id: str) -> dict[str, object]:
        fact = next(item for item in router.facts if item.id == fact_id)
        answers = [*fact.values, "none"]
        return {
            "id": f"question.{fact_id}",
            "kind": "applicability-fact",
            "prompt": fact.prompt,
            "state": "required",
            "permitted_answers": answers,
        }

    @staticmethod
    def _reject(code: str, outcome: str, message: str) -> RejectedResult:
        return RejectedResult.from_value(
            {
                "kind": "rejected-result",
                "code": code,
                "outcome": outcome,
                "message": message,
                "details": {},
                "next_operations": [],
            }
        )

    def _authority_rejection(self, error: AuthorityError) -> RejectedResult:
        failure = error.failure
        return self._reject(failure.code, failure.kind, failure.message)


def _domain_change(value: object) -> DomainChangeDescriptor:
    accepted_module = getattr(value, "accepted_module")
    proposed_module = getattr(value, "proposed_module")
    scope = getattr(value, "scope")
    return DomainChangeDescriptor(
        DomainChangeKind(getattr(value, "kind")),
        tuple(getattr(value, "accepted_ids")),
        tuple(getattr(value, "proposed_ids")),
        DomainReviewScope(
            getattr(scope, "kind"), tuple(getattr(scope, "heading_path", ()))
        ),
        None if isinstance(accepted_module, MissingValue) else accepted_module,
        None if isinstance(proposed_module, MissingValue) else proposed_module,
    )


def _domain_proposal(value: object) -> DomainSemanticProposal:
    return DomainSemanticProposal(
        getattr(value, "policy"),
        getattr(value, "accepted_semantic_revision"),
        int(getattr(value, "proposed_semantic_revision")),
        getattr(value, "intent"),
        getattr(value, "structural_digest"),
    )


def _domain_change_from_mapping(value: object) -> DomainChangeDescriptor:
    if not isinstance(value, Mapping):
        raise TypeError("stored change must be an object")
    scope = value["scope"]
    if not isinstance(scope, Mapping):
        raise TypeError("stored review scope must be an object")
    return DomainChangeDescriptor(
        DomainChangeKind(str(value["kind"])),
        tuple(str(item) for item in value["accepted_ids"]),
        tuple(str(item) for item in value["proposed_ids"]),
        DomainReviewScope(
            str(scope["kind"]),
            tuple(str(item) for item in scope.get("heading_path", ())),
        ),
        str(value["accepted_module"]) if "accepted_module" in value else None,
        str(value["proposed_module"]) if "proposed_module" in value else None,
    )


def _domain_proposal_from_mapping(value: object) -> DomainSemanticProposal:
    if not isinstance(value, Mapping):
        raise TypeError("stored semantic proposal must be an object")
    accepted = value["accepted_semantic_revision"]
    return DomainSemanticProposal(
        str(value["policy"]),
        None if accepted is None else int(accepted),
        int(value["proposed_semantic_revision"]),
        str(value["intent"]),
        str(value["structural_digest"]),
    )


def _authority_evidence(values: Iterable[object]) -> tuple[AuthorityEvidence, ...]:
    selected = tuple(
        sorted(
            AuthorityEvidence(
                str(getattr(item, "provider_contract")),
                str(getattr(item, "provider_contract_version")),
                str(getattr(item, "id")),
                str(getattr(item, "digest")),
            )
            for item in values
        )
    )
    keys = tuple(
        (item.provider_contract, item.provider_contract_version, item.id)
        for item in selected
    )
    if len(set(keys)) != len(keys):
        raise AnalysisError(
            AnalysisFailure(
                "ANALYSIS.DUPLICATE_EVIDENCE",
                "invalid",
                "Evidence logical keys must be unique.",
            )
        )
    return selected


def _evidence_projection(value: AuthorityEvidence) -> dict[str, str]:
    return {
        "id": value.id,
        "digest": value.digest,
        "provider_contract": value.provider_contract,
        "provider_contract_version": value.provider_contract_version,
    }


def _contract_value(value: object) -> object:
    as_contract = getattr(value, "as_contract", None)
    if callable(as_contract):
        return as_contract()
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError("generated contract value has no wire projection")


def _submission_not_applicable(target: str) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(
            "SUBMISSION.NOT_APPLICABLE",
            "invalid",
            f"Submission does not identify current {target} work.",
        )
    )


def _analysis_next_operations(
    analysis: AuthorityHandle,
    requirements: Iterable[object],
    obligations: Iterable[object],
) -> list[dict[str, object]]:
    handle = _handle(analysis)
    result = [
        {
            "operation": "resolve",
            "request_kind": "provide-fact",
            "requirement_id": item.reference.semantic_id,
            "analysis": handle,
        }
        for item in requirements
    ]
    for obligation in obligations:
        if obligation.state == "resolved":
            continue
        for request_kind in obligation.permitted_submissions:
            result.append(
                {
                    "operation": "resolve",
                    "request_kind": request_kind,
                    "obligation_id": obligation.id,
                    "analysis": handle,
                }
            )
    return result


def _codec_sets() -> tuple[object, ...]:
    from tools.standards_analysis.standards_analysis import ANALYSIS_CODECS

    return (
        AUTHORITY_CODECS,
        METADATA_CODECS,
        POLICY_IMPACT_CODECS,
        STANDARDS_GRAPH_CODECS,
        ANALYSIS_CODECS,
        ENGINE_CODECS,
    )


def _authority_scope(
    root: Path,
    corpus: object,
    policy_inputs: Iterable[str],
    horizon_inputs: Iterable[str],
) -> tuple[str, ...]:
    with (root / ATTESTATION_REGISTRY).open("rb") as source:
        registry = tomllib.load(source)
    attestation_sources = tuple(registry.get("sources", ()))
    attestation_inputs = set(attestation_sources)
    for source_path in attestation_sources:
        with (root / source_path).open("rb") as source:
            declaration = tomllib.load(source)
        for attestation in declaration.get("attestations", ()):
            if not isinstance(attestation, Mapping):
                continue
            for field in ("evidence", "explicit_exclusions"):
                values = attestation.get(field, ())
                if isinstance(values, list):
                    attestation_inputs.update(
                        item for item in values if isinstance(item, str)
                    )
    with (root / AUTHORIZATION_AUTHORITY).open("rb") as source:
        authorization = tomllib.load(source)
    authorization_inputs = {
        AUTHORIZATION_AUTHORITY,
        REVOCATION_AUTHORITY,
        *(
            item
            for item in authorization.get("authorization_evidence", ())
            if isinstance(item, str)
        ),
    }
    return tuple(
        sorted(
            {
                CANONICAL_MODULE_CORPUS,
                POLICY_UNIT_REGISTRY,
                ROUTER_PROJECTION,
                "STANDARDS-ROUTER.md",
                INTERFACE_SCHEMA,
                INTERFACE_CONTRACT,
                ATTESTATION_REGISTRY,
                *authorization_inputs,
                *corpus.module_corpus.members,
                *corpus.policy_unit_corpus.sources,
                *policy_inputs,
                *horizon_inputs,
                *attestation_inputs,
            }
        )
    )


def _snapshot_subset(
    snapshot: ContentSnapshot,
    paths: Iterable[str],
) -> ContentSnapshot:
    indexed = {str(item.path): item for item in snapshot.files}
    selected = tuple(sorted(set(paths)))
    missing = tuple(path for path in selected if path not in indexed)
    if missing:
        raise RuntimeError(
            f"captured authority snapshot is missing owner input {missing[0]!r}"
        )
    return ContentSnapshot(indexed[path] for path in selected)


@contextmanager
def _snapshot_workspace(snapshot: ContentSnapshot) -> Iterator[Path]:
    with tempfile.TemporaryDirectory(prefix="standards-authority-") as directory:
        root = Path(directory)
        for item in snapshot.files:
            target = root.joinpath(*item.path.components)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(item.content)
        yield root


def _resolve_policy(corpus: object, requested: str) -> tuple[object, ModuleMetadata] | None:
    selected = corpus.policy_unit_corpus.resolve(requested)
    if isinstance(selected, PolicyUnitTombstone):
        return None
    if isinstance(selected, PolicyUnit):
        module = corpus.module_corpus.resolve(selected.module)
        assert module is not None
        return selected, module
    module = corpus.module_corpus.resolve(requested)
    return (module, module) if module is not None and module.module_id == requested else None


def _module_declaration(module: ModuleMetadata) -> dict[str, object]:
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


def _authority_handle(value: object) -> AuthorityHandle:
    return AuthorityHandle(_object_kind(value.kind), value.id)


def _object_kind(handle_kind: str) -> str:
    mapping = {
        "content-snapshot-handle": "content-snapshot",
        "standards-authority-view-handle": "standards-authority-view",
        "execution-closure-handle": "execution-closure",
        "navigation-handle": "navigation-result",
        "analysis-handle": "analysis-root",
        "policy-handle": "policy-inspection",
        "relationship-handle": "relationship-inspection",
        "certificate-handle": "coverage-certificate",
        "coverage-authority-view-handle": "coverage-view",
        "coverage-requirement-handle": "coverage-requirement",
        "coverage-attestation-handle": "coverage-attestation",
        "analysis-context-handle": "analysis-context",
        "fact-requirement-handle": "fact-requirement",
        "fact-observation-handle": "fact-observation",
    }
    return mapping[handle_kind]


def _handle(value: AuthorityHandle) -> dict[str, object]:
    kinds = {
        "content-snapshot": "content-snapshot-handle",
        "standards-authority-view": "standards-authority-view-handle",
        "execution-closure": "execution-closure-handle",
        "navigation-result": "navigation-handle",
        "analysis-root": "analysis-handle",
        "policy-inspection": "policy-handle",
        "relationship-inspection": "relationship-handle",
        "coverage-certificate": "certificate-handle",
        "coverage-view": "coverage-authority-view-handle",
        "coverage-requirement": "coverage-requirement-handle",
        "coverage-attestation": "coverage-attestation-handle",
        "analysis-context": "analysis-context-handle",
        "fact-requirement": "fact-requirement-handle",
        "fact-observation": "fact-observation-handle",
    }
    return {"kind": kinds[value.object_kind], "id": value.semantic_id, "schema_version": 4}


def _handle_ref(value: AuthorityReference) -> dict[str, object]:
    return _handle(AuthorityHandle(value.object_kind, value.semantic_id))


def _reference_projection(value: AuthorityReference) -> dict[str, str]:
    return {"object_kind": value.object_kind, "id": value.semantic_id}


def _authority_reference(value: AuthorityReference) -> dict[str, str]:
    return _reference_projection(value)


def _snapshot_projection(handle: AuthorityHandle, value: ContentSnapshot) -> dict[str, object]:
    return {
        "kind": "content-snapshot",
        "handle": _handle(handle),
        "payload_contract": "content-snapshot.v2",
        "files": [
            {
                "path": {"components": list(item.path.components)},
                "content_base64": base64.b64encode(item.content).decode("ascii"),
                "content_digest": "sha256:"
                + hashlib.sha256(item.content).hexdigest(),
                "byte_length": len(item.content),
            }
            for item in value.files
        ],
    }


def _view_projection(handle: AuthorityHandle, value: StandardsAuthorityView) -> dict[str, object]:
    return {
        "kind": "standards-authority-view",
        "handle": _handle(handle),
        "content": _handle_ref(value.content),
        "operation_contracts": [
            {"operation": item.operation, "authority": _reference_projection(item.authority)}
            for item in value.operation_contracts
        ],
        "authorities": [
            {"role": item.role, "authority": _reference_projection(item.authority)}
            for item in value.authorities
        ],
    }


def _execution_closure_projection(handle: AuthorityHandle, value: ExecutionClosure) -> object:
    from .model import ExecutionClosure as ContractExecutionClosure

    return ContractExecutionClosure.from_value(
        {
            "kind": "execution-closure",
            "handle": _handle(handle),
            "closure_contract": "execution-closure.v2",
            "operation": value.operation,
            "roots": [
                {
                    "side": item.side,
                    "role": item.role,
                    "authority": _reference_projection(item.reference),
                }
                for item in value.roots
            ],
        }
    )


def _snapshot_files(value: ContentSnapshot) -> dict[str, bytes]:
    return {str(item.path): item.content for item in value.files}


def _identity(value: object) -> IdentityValue:
    value_type = type(value)
    if value is None or value_type in {bool, int, str}:
        return value  # type: ignore[return-value]
    if value_type is list or value_type is tuple:
        return IdentityArray(_identity(item) for item in value)
    if isinstance(value, Mapping):
        return IdentityObject((key, _identity(value[key])) for key in sorted(value))
    raise TypeError(f"value is not an identity record: {value_type!r}")


def _wire(value: IdentityValue) -> object:
    if type(value) is IdentityArray:
        return [_wire(item) for item in value.values]
    if type(value) is IdentityObject:
        return {key: _wire(item) for key, item in value.members}
    return value


__all__ = ("StandardsEngine",)
