from __future__ import annotations

import hashlib
import json
import tempfile
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from tools.graph_engine.graph_engine import Direction, Edge, EdgeRegistry, GraphError
from tools.repository_git.repository_git import (
    GitRepository,
    GitRepositoryError,
    RepositoryPath,
    RepositoryRevision,
)
from tools.standards_analysis.standards_analysis import (
    ANALYSIS_CONTRACT_VERSION,
    AnalysisEvaluation,
    AnalysisExecutionContext,
    AnalysisMaterial,
    AnalysisState as DomainAnalysisState,
    AnalysisError,
    AnalysisFailure,
    AuthorizationRequest,
    CoverageDefinitionIndex,
    DependencyCause,
    EvidenceReference,
    HORIZON_VERSION,
    ImmutableProviderInput,
    ProviderNoObservation,
    ProviderObservationClaim,
    ProviderRequest,
    ProviderUnavailable,
    ProjectedRevisionMaterialRef,
    ReadingSelection,
    RepositoryCoverageDecisions,
    ReviewScope,
    RouterProjection,
    SnapshotMaterialRef,
    RoutingBaseCause,
    RoutingRuleCause,
    analysis_value_digest,
    canonical_target_authority,
    child_id as analysis_child_id,
    compile_coverage_definitions,
    compile_reading_plan,
    derive_change_descriptors,
    evaluate_analysis,
    construct_authorization_record,
    load_coverage_horizon,
    load_repository_coverage_decisions,
    load_router_projection,
    plain_record,
)
from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    LANGUAGE_VERSION,
    Truth,
)
from tools.standards_contracts.standards_contracts import MissingValue
from tools.standards_graph.standards_graph import (
    METADATA_REQUIRES,
    standards_navigation_registry,
)
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    ContentSource,
    FrozenContentSource,
    MetadataError,
    MetadataFailure,
    ModuleMetadata,
    PolicyUnit,
    RecordingContentSource,
    load_canonical_standards_corpus,
    markdown_structural_digest,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
    PolicyImpactError,
    compile_policy_impact,
    thaw,
)
from tools.standards_snapshots.standards_snapshots import (
    ChildHandle,
    CapturedContent,
    FindSnapshotsRequest,
    SnapshotError,
    SnapshotFile,
    SnapshotId,
    SnapshotModule,
    SnapshotPath,
    SnapshotSummary,
)

from ._generated_contract import (
    AnalyzeProposalCall,
    AnalysisChildHandle,
    AnalysisChildInspectionResult,
    AnalysisHandle,
    AnalysisInspectionResult,
    CompleteResult,
    ConsumerDispositionSubmission,
    CoverageAttestationSubmission,
    CreateSnapshotCall,
    CreateSnapshotResult,
    CreateProposalCall,
    CreateProposalResult,
    DeleteSnapshotCall,
    DeleteSnapshotResult,
    FindSnapshotsCall,
    FindSnapshotsResult,
    FindProposalsCall,
    FindProposalsResult,
    InspectCall,
    ImpactDispositionSubmission,
    InspectionResult,
    PendingResult,
    PrepareCall,
    ProvideFactSubmission,
    PolicyInspectionResult,
    QueryCall,
    QueryProposalCall,
    QueryProposalResult,
    QueryResult,
    ReviewProposalCall,
    ReviewProposalResult,
    ProposalReadResult,
    ProposalRelatedResult,
    ProposalRevisionHandle,
    ProposalRouteResult,
    ReadRequest,
    ReadResult,
    RejectedResult,
    RelatedRequest,
    RelatedResult,
    RelationshipInspectionResult,
    ReviseProposalCall,
    ReviseProposalResult,
    ResolveCall,
    RouteRequest,
    RouteResult,
    SnapshotChildHandle,
    SnapshotHandle,
    SnapshotInspectionResult,
    UndeleteSnapshotCall,
    UndeleteSnapshotResult,
)
from .authoring import (
    AuthoringError,
    AuthoringModule,
    CANONICAL_TARGET_BRANCH,
    FindProposalsRequest,
    Mutation,
    ProposalId,
    ProposalRevision,
    REVIEW_CAPABILITIES,
    ProposalSummary as AuthoringProposalSummary,
    review_decision_subject,
)


DEFAULT_STORE = ".standards-engine/snapshots-v1.sqlite3"


@dataclass(frozen=True, slots=True)
class CompiledSnapshot:
    source: ContentSource
    corpus: CanonicalStandardsCorpus
    policy_impact: CompiledPolicyImpactSet
    graph: EdgeRegistry
    router: RouterProjection
    coverage: CoverageDefinitionIndex
    repository_coverage: RepositoryCoverageDecisions

    def semantic_signature(self) -> tuple[object, ...]:
        return (
            self.corpus,
            self.policy_impact,
            self.router,
            tuple(self.graph.nodes.items()),
            tuple(self.graph.groups.items()),
            tuple(self.graph.edges.items()),
            self.coverage,
            self.repository_coverage,
        )


class _GitRevisionSource:
    def __init__(self, repository: GitRepository, revision: RepositoryRevision) -> None:
        self._repository = repository
        self._revision = revision

    def read_bytes(self, path: str) -> bytes:
        try:
            return self._repository.read_file(
                self._revision, RepositoryPath.parse(path)
            )
        except GitRepositoryError as error:
            if error.failure.kind != "unavailable":
                raise
            raise MetadataError(
                MetadataFailure(
                    "INPUT.UNAVAILABLE",
                    "unavailable",
                    error.failure.message,
                    path=path,
                )
            ) from error


class _ProjectedRevisionSource:
    """Exact replacement overlay over one immutable snapshot capture."""

    def __init__(self, base: FrozenContentSource, revision: ProposalRevision) -> None:
        self._base = base
        self._replacements = {
            str(mutation.path): mutation.value.encode("utf-8")
            for mutation in revision.mutations
        }

    def read_bytes(self, path: str) -> bytes:
        normalized = str(SnapshotPath.parse(path))
        replacement = self._replacements.get(normalized)
        if replacement is not None:
            return replacement
        return self._base.read_bytes(normalized)


@dataclass(frozen=True, slots=True)
class _QueryProjection:
    """Authority-specific public projection over shared navigation semantics."""

    authority: SnapshotHandle | ProposalRevisionHandle
    anchor: str
    operation: str
    result_prefix: str

    @classmethod
    def snapshot(cls, handle: SnapshotHandle) -> _QueryProjection:
        return cls(handle, "snapshot", "query", "")

    @classmethod
    def proposal(cls, handle: ProposalRevisionHandle) -> _QueryProjection:
        return cls(handle, "revision", "query_proposal", "proposal-")

    def result(self, request_kind: str) -> dict[str, object]:
        return {
            "kind": f"{self.result_prefix}{request_kind}-result",
            self.anchor: self.authority.as_contract(),
        }

    def next_operation(
        self, request_kind: str, target: str | None = None
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "operation": self.operation,
            "request_kind": request_kind,
            self.anchor: self.authority.as_contract(),
        }
        if target is not None:
            value["target"] = target
        return value

    def policy_summary(
        self, identity: str, authority: str, scope: dict[str, object]
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "authority": (
                authority
                if isinstance(self.authority, SnapshotHandle)
                else "projection"
            ),
            "scope": scope,
        }
        if isinstance(self.authority, SnapshotHandle):
            value["handle"] = self._snapshot_child_handle("policy", identity)
        else:
            value["id"] = identity
        return value

    def reading_plan_entry(self, value: dict[str, object]) -> dict[str, object]:
        if isinstance(self.authority, SnapshotHandle):
            return value
        return {**value, "authority": "projection"}

    def read_summary(self, identity: str) -> str:
        material = (
            "canonical" if isinstance(self.authority, SnapshotHandle) else "projected"
        )
        return f"Read {material} standard {identity}."

    def relationship_summary(
        self, identity: str, value: dict[str, object]
    ) -> dict[str, object]:
        if isinstance(self.authority, SnapshotHandle):
            return {
                "handle": self._snapshot_child_handle("relationship", identity),
                **value,
            }
        return value

    def inspect_operation(self, identity: str) -> dict[str, object] | None:
        if not isinstance(self.authority, SnapshotHandle):
            return None
        return {
            "operation": "inspect",
            "request_kind": "inspect",
            "handle": self._snapshot_child_handle("policy", identity),
        }

    def _snapshot_child_handle(
        self, child_kind: str, child_id: str
    ) -> dict[str, object]:
        if not isinstance(self.authority, SnapshotHandle):
            raise RuntimeError("proposal projections do not mint snapshot children")
        return {
            "kind": "snapshot-child-handle",
            "snapshot": self.authority.as_contract(),
            "child_kind": child_kind,
            "child_id": child_id,
            "schema_version": 5,
        }


class StandardsEngine:
    """Composition root for immutable snapshots and generated A1c values."""

    def __init__(
        self,
        repository: GitRepository,
        snapshots: SnapshotModule,
        *,
        execution_context: AnalysisExecutionContext | None = None,
        temporary_store: tempfile.TemporaryDirectory[str] | None = None,
    ) -> None:
        self._repository = repository
        self._snapshots = snapshots
        self._authoring = AuthoringModule(snapshots)
        self._execution_context = execution_context or AnalysisExecutionContext()
        self._temporary_store = temporary_store

    @classmethod
    def open_repository(
        cls,
        root: Path,
        *,
        durable: bool = True,
        store_path: Path | None = None,
        execution_context: AnalysisExecutionContext | None = None,
    ) -> StandardsEngine:
        selected_root = root.resolve()
        temporary = None
        if store_path is None:
            if durable:
                store_path = selected_root / DEFAULT_STORE
            else:
                temporary = tempfile.TemporaryDirectory(prefix="coding-standards-a1c-")
                store_path = Path(temporary.name) / "snapshots.sqlite3"
        return cls(
            GitRepository(selected_root),
            SnapshotModule.open(store_path.resolve()),
            execution_context=execution_context,
            temporary_store=temporary,
        )

    def close(self) -> None:
        self._snapshots.close()
        if self._temporary_store is not None:
            self._temporary_store.cleanup()
            self._temporary_store = None

    def __enter__(self) -> StandardsEngine:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def create_snapshot(
        self, call: CreateSnapshotCall
    ) -> CreateSnapshotResult | RejectedResult:
        del call
        try:
            revision = self._repository.current_revision()
            recording = RecordingContentSource(
                _GitRevisionSource(self._repository, revision)
            )
            first = self._compile(recording)
            frozen = recording.freeze()
            replay = RecordingContentSource(frozen)
            try:
                second = self._compile(replay)
            except MetadataError as error:
                if error.failure.code != "INPUT.UNAVAILABLE":
                    raise
                return self._reject(
                    "SNAPSHOT.CLOSURE_MISMATCH",
                    "invalid",
                    "Frozen snapshot replay requested uncaptured authority.",
                )
            if (
                recording.requested_paths != replay.requested_paths
                or first.semantic_signature() != second.semantic_signature()
            ):
                return self._reject(
                    "SNAPSHOT.CLOSURE_MISMATCH",
                    "invalid",
                    "Frozen snapshot replay changed requested authority or canonical output.",
                )
            summary = self._snapshots.create_snapshot(
                CapturedContent(
                    revision.oid,
                    (
                        SnapshotFile(SnapshotPath.parse(path), content)
                        for path, content in frozen.files
                    ),
                )
            )
            return CreateSnapshotResult.from_value(
                {"kind": "create-snapshot-result", "snapshot": self._summary(summary)}
            )
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def find_snapshots(
        self, call: FindSnapshotsCall
    ) -> FindSnapshotsResult | RejectedResult:
        try:
            lifecycle = "active" if isinstance(call.lifecycle, MissingValue) else call.lifecycle
            after = None if isinstance(call.after, MissingValue) else self._snapshot_id(call.after)
            limit = 50 if isinstance(call.limit, MissingValue) else int(call.limit)
            page = self._snapshots.find_snapshots(
                FindSnapshotsRequest(lifecycle, after, limit)
            )
            value: dict[str, object] = {
                "kind": "find-snapshots-result",
                "snapshots": [self._summary(item) for item in page.snapshots],
            }
            if page.continuation is not None:
                value["continuation"] = self._snapshot_handle(page.continuation)
            return FindSnapshotsResult.from_value(value)
        except SnapshotError as error:
            return self._domain_rejection(error)

    def create_proposal(
        self, call: CreateProposalCall
    ) -> CreateProposalResult | RejectedResult:
        try:
            summary, revision = self._authoring.create_proposal(
                self._snapshot_id(call.base_snapshot),
                (
                    Mutation(SnapshotPath.parse(item.path), item.value)
                    for item in call.mutations
                ),
                (item.as_contract() for item in call.semantic_proposals),
            )
            return CreateProposalResult.from_value(
                {
                    "kind": "create-proposal-result",
                    "proposal": self._proposal_handle(summary.proposal),
                    "revision": self._proposal_revision_handle(revision.revision_id),
                }
            )
        except (AuthoringError, SnapshotError) as error:
            return self._domain_rejection(error)

    def find_proposals(
        self, call: FindProposalsCall
    ) -> FindProposalsResult | RejectedResult:
        try:
            after = (
                None
                if isinstance(call.after, MissingValue)
                else ProposalId(call.after.id)
            )
            limit = 50 if isinstance(call.limit, MissingValue) else int(call.limit)
            page = self._authoring.find_proposals(FindProposalsRequest(after, limit))
            value: dict[str, object] = {
                "kind": "find-proposals-result",
                "proposals": [self._proposal_summary(item) for item in page.proposals],
            }
            if page.continuation is not None:
                value["continuation"] = self._proposal_handle(page.continuation)
            return FindProposalsResult.from_value(value)
        except (AuthoringError, SnapshotError) as error:
            return self._domain_rejection(error)

    def revise_proposal(
        self, call: ReviseProposalCall
    ) -> ReviseProposalResult | RejectedResult:
        try:
            summary, revision = self._authoring.revise_proposal(
                call.expected_revision.id,
                (
                    Mutation(SnapshotPath.parse(item.path), item.value)
                    for item in call.mutations
                ),
                (item.as_contract() for item in call.semantic_proposals),
            )
            return ReviseProposalResult.from_value(
                {
                    "kind": "revise-proposal-result",
                    "proposal": self._proposal_handle(summary.proposal),
                    "revision": self._proposal_revision_handle(revision.revision_id),
                }
            )
        except (AuthoringError, SnapshotError) as error:
            return self._domain_rejection(error)

    def delete_snapshot(
        self, call: DeleteSnapshotCall
    ) -> DeleteSnapshotResult | RejectedResult:
        try:
            result = self._snapshots.delete_snapshot(self._snapshot_id(call.snapshot))
            return DeleteSnapshotResult.from_value(
                {
                    "kind": "delete-snapshot-result",
                    "snapshot": self._snapshot_handle(result.snapshot),
                    "purge_deadline": result.purge_deadline,
                }
            )
        except SnapshotError as error:
            return self._domain_rejection(error)

    def undelete_snapshot(
        self, call: UndeleteSnapshotCall
    ) -> UndeleteSnapshotResult | RejectedResult:
        try:
            summary = self._snapshots.undelete_snapshot(self._snapshot_id(call.snapshot))
            return UndeleteSnapshotResult.from_value(
                {"kind": "undelete-snapshot-result", "snapshot": self._summary(summary)}
            )
        except SnapshotError as error:
            return self._domain_rejection(error)

    def query(self, call: QueryCall) -> QueryResult | RejectedResult:
        try:
            compiled = self._compiled_snapshot(self._snapshot_id(call.snapshot))
            if isinstance(call.request, RouteRequest):
                return self._route(call.snapshot, compiled, call.request)
            if isinstance(call.request, ReadRequest):
                return self._read(call.snapshot, compiled, call.request)
            if isinstance(call.request, RelatedRequest):
                return self._related(call.snapshot, compiled, call.request)
            return self._reject(
                "NAVIGATION.UNSUPPORTED_REQUEST",
                "unsupported",
                "The query request kind is unsupported.",
            )
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def query_proposal(
        self, call: QueryProposalCall
    ) -> QueryProposalResult | RejectedResult:
        try:
            revision = self._authoring.read_revision(call.revision.id)
            compiled = self._compiled_revision(revision)
            projection = _QueryProjection.proposal(call.revision)
            if isinstance(call.request, RouteRequest):
                return ProposalRouteResult.from_value(
                    self._route_value(projection, compiled, call.request)
                )
            if isinstance(call.request, ReadRequest):
                value = self._read_value(projection, compiled, call.request)
                return (
                    value
                    if isinstance(value, RejectedResult)
                    else ProposalReadResult.from_value(value)
                )
            if isinstance(call.request, RelatedRequest):
                value = self._related_value(projection, compiled, call.request)
                return (
                    value
                    if isinstance(value, RejectedResult)
                    else ProposalRelatedResult.from_value(value)
                )
            return self._reject(
                "NAVIGATION.UNSUPPORTED_REQUEST",
                "unsupported",
                "The query request kind is unsupported.",
            )
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def analyze_proposal(
        self, call: AnalyzeProposalCall
    ) -> PendingResult | CompleteResult | RejectedResult:
        try:
            revision = self._authoring.read_revision(call.revision.id)
            accepted = self._compiled_snapshot(revision.base_snapshot)
            proposed = self._compiled_revision(revision)
            semantic_proposals = tuple(
                self._plain(item) for item in revision.semantic_proposals
            )
            changes = derive_change_descriptors(
                accepted.corpus.policy_unit_corpus,
                proposed.corpus.policy_unit_corpus,
                (str(item["policy"]) for item in semantic_proposals),
            )
            attestations, authorizations = self._repository_decisions(
                changes, accepted, proposed
            )
            state = DomainAnalysisState(
                revision.base_snapshot,
                ProjectedRevisionMaterialRef(
                    revision.revision_id,
                    revision.base_snapshot,
                ),
                (item.as_contract() for item in changes),
                semantic_proposals,
                coverage_attestations=attestations,
                authorization_records=authorizations,
                domain_contracts=self._domain_contracts(),
                execution_contracts=self._execution_context.contract_view(),
            )
            return self._evaluate_publish_project(
                state,
                self._evaluate_compiled(state, accepted, proposed, revision),
            )
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def review_proposal(
        self, call: ReviewProposalCall
    ) -> ReviewProposalResult | RejectedResult:
        try:
            state = self._load_analysis(call.analysis)
            evaluation = self._evaluate(state)
            if not evaluation.complete:
                return self._reject(
                    "AUTHORING.ANALYSIS_INCOMPLETE",
                    "unavailable",
                    "Proposal review requires a complete analysis.",
                )
            if any(
                self._plain(item).get("result") == "requires-change"
                for item in state.dispositions
            ):
                return self._reject(
                    "AUTHORING.REVIEW_NOT_READY",
                    "unavailable",
                    "The completed analysis records a required proposal change.",
                )
            proposed = state.proposed_material
            if not isinstance(proposed, ProjectedRevisionMaterialRef):
                return self._reject(
                    "AUTHORING.ANALYSIS_NOT_PROPOSAL",
                    "invalid",
                    "Proposal review requires analysis of an immutable proposal revision.",
                )
            revision = self._authoring.read_revision(proposed.revision_id)
            target = self._repository.branch_revision(CANONICAL_TARGET_BRANCH)
            base = self._snapshots.snapshot(revision.base_snapshot)
            if target.oid != base.source_revision:
                return self._reject(
                    "AUTHORING.TARGET_STALE",
                    "unavailable",
                    "The configured main branch no longer matches the proposal base.",
                )
            decisions = tuple(item.as_contract() for item in call.decisions)
            authorizations = tuple(
                construct_authorization_record(
                    self._execution_context,
                    AuthorizationRequest(
                        "review-proposal",
                        "proposal-review-decision",
                        review_decision_subject(
                            state.analysis_id,
                            revision.revision_id,
                            decision,
                        ),
                        REVIEW_CAPABILITIES[str(decision["owner"])],
                        self._evidence(call.decisions[index].evidence),
                    ),
                ).as_contract()
                for index, decision in enumerate(decisions)
            )
            prior = (
                None
                if isinstance(call.prior_readiness, MissingValue)
                else call.prior_readiness.id
            )
            readiness = self._authoring.review_proposal(
                state.analysis_id,
                revision.revision_id,
                decisions,
                authorizations,
                target,
                prior_readiness=prior,
            )
            return ReviewProposalResult.from_value(
                {
                    "kind": "review-proposal-result",
                    "readiness": self._readiness_handle(readiness.readiness_id),
                    "revision": self._proposal_revision_handle(revision.revision_id),
                    "status": "ready",
                }
            )
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def prepare(
        self, call: PrepareCall
    ) -> PendingResult | CompleteResult | RejectedResult:
        try:
            request = call.request
            base_snapshot = self._snapshot_id(request.base_snapshot)
            proposed_snapshot = self._snapshot_id(request.proposed_snapshot)
            base = self._compiled_snapshot(base_snapshot)
            proposed = self._compiled_snapshot(proposed_snapshot)
            attestations, authorizations = self._repository_decisions(
                request.changes, base, proposed
            )
            state = DomainAnalysisState(
                base_snapshot,
                SnapshotMaterialRef(proposed_snapshot),
                (item.as_contract() for item in request.changes),
                (item.as_contract() for item in request.semantic_proposals),
                coverage_attestations=attestations,
                authorization_records=authorizations,
                domain_contracts=self._domain_contracts(),
                execution_contracts=self._execution_context.contract_view(),
            )
            if not isinstance(request.prior_analysis, MissingValue):
                state = self._reuse_prior(state, request.prior_analysis)
            return self._evaluate_publish_project(
                state,
                self._evaluate_compiled(state, base, proposed),
            )
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def resolve(
        self, call: ResolveCall
    ) -> PendingResult | CompleteResult | RejectedResult:
        try:
            state = self._load_analysis(call.analysis)
            successor = self._apply_submission(self._evaluate(state), call)
            return self._evaluate_publish_project(successor)
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def inspect(self, call: InspectCall) -> InspectionResult | RejectedResult:
        try:
            handle = call.handle
            if isinstance(handle, SnapshotHandle):
                summary = self._snapshots.snapshot(
                    self._snapshot_id(handle), include_quarantined=True
                )
                return SnapshotInspectionResult.from_value(
                    {"kind": "snapshot-inspection-result", "snapshot": self._summary(summary)}
                )
            if isinstance(handle, SnapshotChildHandle):
                return self._inspect_snapshot_child(handle)
            if isinstance(handle, AnalysisHandle):
                return AnalysisInspectionResult.from_value(
                    {
                        "kind": "analysis-inspection-result",
                        "state": self._state_projection(self._load_analysis(handle)),
                    }
                )
            if isinstance(handle, AnalysisChildHandle):
                payload = self._snapshots.inspect_child(
                    ChildHandle(
                        handle.analysis.id,
                        handle.child_kind,
                        handle.child_id,
                    )
                )
                return AnalysisChildInspectionResult.from_value(
                    {
                        "kind": "analysis-child-inspection-result",
                        "handle": handle.as_contract(),
                        "artifact": json.loads(payload),
                    }
                )
            return self._reject(
                "INSPECTION.UNSUPPORTED_HANDLE",
                "unsupported",
                "The handle kind has no available projection.",
            )
        except self._domain_errors() as error:
            return self._domain_rejection(error)

    def _compiled_snapshot(self, snapshot: SnapshotId) -> CompiledSnapshot:
        capture = self._snapshots.load_content(snapshot)
        return self._compile(
            FrozenContentSource((str(item.path), item.content) for item in capture.files)
        )

    def _compiled_revision(self, revision: ProposalRevision) -> CompiledSnapshot:
        capture = self._snapshots.load_content(revision.base_snapshot)
        base = FrozenContentSource(
            (str(item.path), item.content) for item in capture.files
        )
        return self._compile(_ProjectedRevisionSource(base, revision))

    @staticmethod
    def _compile(source: ContentSource) -> CompiledSnapshot:
        corpus = load_canonical_standards_corpus(source)
        impact = compile_policy_impact(source, corpus)
        graph = standards_navigation_registry(
            source, corpus, compiled_policy_impact=impact
        )
        router = load_router_projection(source, corpus.module_corpus)
        coverage = compile_coverage_definitions(
            corpus, impact, load_coverage_horizon(source, corpus, impact)
        )
        repository_coverage = load_repository_coverage_decisions(source, coverage)
        return CompiledSnapshot(
            source,
            corpus,
            impact,
            graph,
            router,
            coverage,
            repository_coverage,
        )

    @staticmethod
    def _repository_decisions(
        changes: Iterable[object],
        base: CompiledSnapshot,
        proposed: CompiledSnapshot,
    ) -> tuple[tuple[Mapping[str, object], ...], tuple[Mapping[str, object], ...]]:
        attestations: dict[str, Mapping[str, object]] = {}
        authorizations: dict[str, Mapping[str, object]] = {}
        for change in changes:
            subjects = change.proposed_ids or change.accepted_ids
            for subject in subjects:
                selected = (
                    proposed.repository_coverage
                    if subject in proposed.coverage.views
                    else base.repository_coverage
                )
                attestation = selected.attestations.get(subject)
                if attestation is None:
                    continue
                requirement = str(attestation["requirement_id"])
                attestations[requirement] = attestation
                authorization_id = str(attestation["authorization_id"])
                authorizations[authorization_id] = selected.authorization_records[
                    authorization_id
                ]
        return (
            tuple(attestations[key] for key in sorted(attestations)),
            tuple(authorizations[key] for key in sorted(authorizations)),
        )

    def _evaluate(self, state: DomainAnalysisState) -> AnalysisEvaluation:
        accepted = self._compiled_snapshot(state.base_snapshot)
        proposed_ref = state.proposed_material
        if isinstance(proposed_ref, SnapshotMaterialRef):
            proposed = self._compiled_snapshot(proposed_ref.snapshot)
            revision = None
        else:
            revision = self._authoring.read_revision(proposed_ref.revision_id)
            if revision.base_snapshot != state.base_snapshot:
                raise AnalysisError(
                    AnalysisFailure(
                        "ANALYSIS.MATERIAL_BASE_MISMATCH",
                        "invalid",
                        "Proposal revision and analysis base snapshots differ.",
                    )
                )
            proposed = self._compiled_revision(revision)
        return self._evaluate_compiled(state, accepted, proposed, revision)

    def _evaluate_compiled(
        self,
        state: DomainAnalysisState,
        accepted: CompiledSnapshot,
        proposed: CompiledSnapshot,
        revision: ProposalRevision | None = None,
    ) -> AnalysisEvaluation:
        proposed_ref = state.proposed_material
        if isinstance(proposed_ref, ProjectedRevisionMaterialRef):
            if revision is None or revision.revision_id != proposed_ref.revision_id:
                raise AnalysisError(
                    AnalysisFailure(
                        "ANALYSIS.MATERIAL_INPUT_MISMATCH",
                        "invalid",
                        "Resolved proposal revision does not match the analysis state.",
                    )
                )
            self._validate_projected_inputs(state, revision, accepted, proposed)
        return evaluate_analysis(
            state,
            self._analysis_material(SnapshotMaterialRef(state.base_snapshot), accepted),
            self._analysis_material(proposed_ref, proposed),
        )

    @staticmethod
    def _analysis_material(
        reference: SnapshotMaterialRef | ProjectedRevisionMaterialRef,
        compiled: CompiledSnapshot,
    ) -> AnalysisMaterial:
        return AnalysisMaterial(
            reference,
            compiled.source,
            compiled.corpus,
            compiled.graph,
            compiled.policy_impact,
            compiled.coverage,
        )

    @classmethod
    def _validate_projected_inputs(
        cls,
        state: DomainAnalysisState,
        revision: ProposalRevision,
        accepted: CompiledSnapshot,
        proposed: CompiledSnapshot,
    ) -> None:
        semantic_proposals = tuple(cls._plain(item) for item in revision.semantic_proposals)
        changes = derive_change_descriptors(
            accepted.corpus.policy_unit_corpus,
            proposed.corpus.policy_unit_corpus,
            (str(item["policy"]) for item in semantic_proposals),
        )
        retained_changes = tuple(cls._plain(item) for item in state.changes)
        retained_semantic = tuple(cls._plain(item) for item in state.semantic_proposals)
        if cls._canonical_records(retained_changes) != cls._canonical_records(
            item.as_contract() for item in changes
        ) or cls._canonical_records(retained_semantic) != cls._canonical_records(
            semantic_proposals
        ):
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.MATERIAL_INPUT_MISMATCH",
                    "invalid",
                    "Stored analysis inputs do not match the exact proposal revision.",
                )
            )

    @staticmethod
    def _canonical_records(values: Iterable[Mapping[str, object]]) -> tuple[str, ...]:
        return tuple(
            sorted(
                json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                for value in values
            )
        )

    def _evaluate_publish_project(
        self,
        state: DomainAnalysisState,
        evaluation: AnalysisEvaluation | None = None,
    ) -> PendingResult | CompleteResult:
        evaluation = self._evaluate(state) if evaluation is None else evaluation
        state, evaluation = self._apply_providers(state, evaluation)
        self._snapshots.publish_aggregate(
            state.aggregate(self._analysis_children(evaluation))
        )
        return self._analysis_result(evaluation)

    def _apply_providers(
        self,
        state: DomainAnalysisState,
        evaluation: AnalysisEvaluation,
    ) -> tuple[DomainAnalysisState, AnalysisEvaluation]:
        while evaluation.pending_requirements:
            applied = False
            for requirement in evaluation.pending_requirements:
                available_inputs = {
                    ("accepted", "snapshot"): ImmutableProviderInput(
                        "accepted",
                        "snapshot",
                        str(state.base_snapshot),
                        analysis_value_digest(str(state.base_snapshot)),
                    ),
                    ("current", "requirement"): ImmutableProviderInput(
                        "current",
                        "requirement",
                        requirement.id,
                        analysis_value_digest(dict(requirement.projection)),
                    ),
                }
                proposed_ref = state.proposed_material
                if isinstance(proposed_ref, SnapshotMaterialRef):
                    available_inputs[("proposed", "snapshot")] = ImmutableProviderInput(
                        "proposed",
                        "snapshot",
                        str(proposed_ref.snapshot),
                        analysis_value_digest(str(proposed_ref.snapshot)),
                    )
                else:
                    available_inputs[("proposed", "revision")] = ImmutableProviderInput(
                        "proposed",
                        "revision",
                        proposed_ref.revision_id,
                        analysis_value_digest(proposed_ref.as_contract()),
                    )
                for provider in self._execution_context.providers:
                    try:
                        inputs = tuple(
                            available_inputs[(role.side, role.role)]
                            for role in provider.contract.input_roles
                        )
                    except KeyError as error:
                        raise AnalysisError(
                            AnalysisFailure(
                                "ANALYSIS.PROVIDER_INPUT_UNSUPPORTED",
                                "unsupported",
                                "Provider requests an unsupported immutable input.",
                            )
                        ) from error
                    outcome = provider.observe(
                        ProviderRequest(
                            requirement.id,
                            requirement.fact.id,
                            inputs,
                        )
                    )
                    if isinstance(outcome, ProviderNoObservation):
                        continue
                    if isinstance(outcome, ProviderUnavailable):
                        raise AnalysisError(
                            AnalysisFailure(
                                "ANALYSIS.PROVIDER_UNAVAILABLE",
                                "unavailable",
                                outcome.reason,
                            )
                        )
                    if not isinstance(outcome, ProviderObservationClaim):
                        raise AnalysisError(
                            AnalysisFailure(
                                "ANALYSIS.PROVIDER_INVALID",
                                "invalid",
                                "Fact provider returned an unrecognized outcome.",
                            )
                        )
                    if provider.contract.evidence_contract != requirement.fact.evidence_contract:
                        raise AnalysisError(
                            AnalysisFailure(
                                "ANALYSIS.EVIDENCE_CONTRACT_MISMATCH",
                                "invalid",
                                "Provider evidence contract does not match the fact.",
                            )
                        )
                    evidence = tuple(item.reference for item in outcome.evidence)
                    requirement.fact.bind(outcome.value)
                    authorization = construct_authorization_record(
                        self._execution_context,
                        AuthorizationRequest(
                            "provide-fact",
                            "fact-requirement",
                            requirement.id,
                            requirement.fact.authorization_capability,
                            evidence,
                        ),
                    )
                    provider_reference = {
                        "id": provider.contract.provider_id,
                        "contract": provider.contract.input_contract,
                        "contract_version": str(
                            provider.contract.semantic_revision
                        ),
                        "input_digest": analysis_value_digest(
                            [
                                {
                                    "side": item.side,
                                    "role": item.role,
                                    "identity": item.identity,
                                    "digest": item.digest,
                                }
                                for item in inputs
                            ]
                        ),
                    }
                    observation = {
                        "requirement_id": requirement.id,
                        "value": outcome.value,
                        "evidence": [item.as_contract() for item in evidence],
                        "authorization_id": authorization.reference["id"],
                        "provider": provider_reference,
                    }
                    state = state.with_decisions(
                        fact_observations=(
                            *state.fact_observations,
                            observation,
                        ),
                        authorization_records=(
                            *state.authorization_records,
                            authorization.as_contract(),
                        ),
                    )
                    evaluation = self._evaluate(state)
                    applied = True
                    break
                if applied:
                    break
            if not applied:
                break
        return state, evaluation

    def _load_analysis(self, handle: AnalysisHandle) -> DomainAnalysisState:
        record = self._snapshots.load_aggregate(handle.id)
        if record.kind != "analysis-state" or record.aggregate_id != handle.id:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.INVALID_STATE",
                    "invalid",
                    "Stored aggregate is not an AnalysisState.",
                )
            )
        state = DomainAnalysisState.decode(record.payload)
        if state.analysis_id != handle.id:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.IDENTITY_MISMATCH",
                    "invalid",
                    "Stored analysis bytes do not match the handle.",
                )
            )
        stored_contracts = tuple(
            sorted(
                (str(value["id"]), str(value["version"]))
                for item in state.domain_contracts
                for value in (self._plain(item),)
            )
        )
        current_contracts = tuple(
            sorted((value["id"], value["version"]) for value in self._domain_contracts())
        )
        if stored_contracts != current_contracts:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.DOMAIN_CONTRACT_UNSUPPORTED",
                    "unsupported",
                    "Stored analysis domain contracts are unsupported.",
                )
            )
        return state

    def _reuse_prior(
        self,
        state: DomainAnalysisState,
        prior: AnalysisHandle,
    ) -> DomainAnalysisState:
        previous = self._load_analysis(prior)
        if previous.execution_contracts != state.execution_contracts:
            return state
        authorizations = {
            str(value["reference"]["id"]): record
            for record in previous.authorization_records
            for value in (self._plain(record),)
        }
        current = state
        for field in (
            "fact_observations",
            "coverage_attestations",
            "dispositions",
        ):
            for decision in getattr(previous, field):
                value = self._plain(decision)
                authorization = authorizations.get(str(value["authorization_id"]))
                candidate = current.with_decisions(
                    **{
                        field: (*getattr(current, field), decision),
                        "authorization_records": (
                            current.authorization_records
                            if authorization is None
                            else (*current.authorization_records, authorization)
                        ),
                    }
                )
                try:
                    self._evaluate(candidate)
                except AnalysisError as error:
                    if error.failure.code == "ANALYSIS.INVALID_RETAINED_DECISION":
                        continue
                    raise
                current = candidate
        return current

    def _apply_submission(
        self,
        evaluation: AnalysisEvaluation,
        call: ResolveCall,
    ) -> DomainAnalysisState:
        state = evaluation.state
        submission = call.submission
        if isinstance(submission, ProvideFactSubmission):
            self._current_child(submission.requirement, state, "fact-requirement")
            requirement = next(
                (
                    item
                    for item in evaluation.pending_requirements
                    if item.id == submission.requirement.child_id
                ),
                None,
            )
            if requirement is None:
                self._not_applicable()
            evidence = self._evidence(submission.evidence)
            requirement.fact.bind(submission.value.as_contract())
            authorization = construct_authorization_record(
                self._execution_context,
                AuthorizationRequest(
                    "provide-fact",
                    "fact-requirement",
                    requirement.id,
                    requirement.fact.authorization_capability,
                    evidence,
                ),
            )
            observation = {
                "requirement_id": requirement.id,
                "value": submission.value.as_contract(),
                "evidence": [item.as_contract() for item in evidence],
                "authorization_id": authorization.reference["id"],
            }
            return state.with_decisions(
                fact_observations=(*state.fact_observations, observation),
                authorization_records=(
                    *state.authorization_records,
                    authorization.as_contract(),
                ),
            )

        if isinstance(submission, CoverageAttestationSubmission):
            claim = submission.claim
            self._current_child(claim.requirement, state, "coverage-requirement")
            coverage = next(
                (
                    item
                    for item in evaluation.coverage
                    if item.requirement_id == claim.requirement.child_id
                ),
                None,
            )
            if coverage is None:
                self._not_applicable()
            obligation = next(
                (
                    item
                    for item in evaluation.obligations
                    if item.kind == "audit-coverage"
                    and item.target == coverage.subject
                    and item.state == "required"
                ),
                None,
            )
            if obligation is None:
                self._not_applicable()
            evidence = self._evidence(claim.evidence)
            authorization = construct_authorization_record(
                self._execution_context,
                AuthorizationRequest(
                    "coverage-attestation",
                    "coverage-requirement",
                    coverage.requirement_id,
                    "standards.review.audit",
                    evidence,
                ),
            )
            attestation = {
                "requirement_id": coverage.requirement_id,
                "conclusion": claim.conclusion,
                "evidence": [item.as_contract() for item in evidence],
                "explicit_exclusions": [
                    item.as_contract()
                    for item in self._evidence(claim.explicit_exclusions)
                ],
                "rationale": claim.rationale,
                "auditor_provenance": claim.auditor_provenance,
                "schema_version": 4,
                "authorization_id": authorization.reference["id"],
            }
            return state.with_decisions(
                coverage_attestations=(
                    *state.coverage_attestations,
                    attestation,
                ),
                authorization_records=(
                    *state.authorization_records,
                    authorization.as_contract(),
                ),
            )

        obligation_handle = submission.obligation
        self._current_child(obligation_handle, state, "obligation")
        obligation = next(
            (
                item
                for item in evaluation.obligations
                if self._obligation_child_id(item.id) == obligation_handle.child_id
                and item.state == "required"
            ),
            None,
        )
        if obligation is None:
            self._not_applicable()
        if not isinstance(
            submission,
            (ConsumerDispositionSubmission, ImpactDispositionSubmission),
        ):
            self._not_applicable()
        if submission.fingerprint.as_contract() != obligation.fingerprint.as_contract():
            self._not_applicable()
        evidence = self._evidence(submission.evidence)
        capability = (
            str(obligation.review_contract["authorization_capability"])
            if obligation.review_contract is not None
            else "standards.review.impact"
        )
        authorization = construct_authorization_record(
            self._execution_context,
            AuthorizationRequest(
                submission.kind,
                "obligation",
                obligation.id,
                capability,
                evidence,
            ),
        )
        disposition = {
            "obligation_id": obligation.id,
            "kind": submission.kind,
            "result": submission.result,
            "rationale": submission.rationale,
            "evidence": [item.as_contract() for item in evidence],
            "authorization_id": authorization.reference["id"],
            "fingerprint": submission.fingerprint.as_contract(),
        }
        return state.with_decisions(
            dispositions=(*state.dispositions, disposition),
            authorization_records=(
                *state.authorization_records,
                authorization.as_contract(),
            ),
        )

    def _analysis_result(
        self, evaluation: AnalysisEvaluation
    ) -> PendingResult | CompleteResult:
        state = evaluation.state
        handle = self._analysis_handle(state.analysis_id)
        context = self._context_projection(evaluation)
        changed_units = [
            unit.as_contract()
            for change in evaluation.changes
            for unit in change.changed_units
        ]
        if not evaluation.complete:
            requirements = [
                self._requirement_work(state, item)
                for item in evaluation.pending_requirements
            ]
            obligations = [
                self._obligation_projection(state, item)
                for item in evaluation.obligations
            ]
            next_operations = [
                {
                    "operation": "resolve",
                    "request_kind": "provide-fact",
                    "target": item.fact.id,
                    "work": self._analysis_child_handle(
                        state.analysis_id, "fact-requirement", item.id
                    ),
                    "analysis": handle,
                }
                for item in evaluation.pending_requirements
            ]
            next_operations.extend(
                {
                    "operation": "resolve",
                    "request_kind": item.permitted_submissions[0],
                    "target": item.target,
                    "work": self._obligation_work_handle(evaluation, item),
                    "analysis": handle,
                }
                for item in evaluation.obligations
                if item.state == "required"
            )
            return PendingResult.from_value(
                {
                    "kind": "pending-result",
                    "handle": handle,
                    "status": "needs-action",
                    "context": context,
                    "changes": [self._plain(item) for item in state.changes],
                    "changed_units": changed_units,
                    "obligations": obligations,
                    "fact_requirements": requirements,
                    "reading_plan": [
                        item.as_contract() for item in evaluation.reading_plan
                    ],
                    "next_operations": next_operations,
                    "summary": "The bounded analysis requires additional decisions.",
                }
            )
        certificates = [
            self._certificate_projection(state, item)
            for item in evaluation.coverage
            if item.certificate is not None
        ]
        return CompleteResult.from_value(
            {
                "kind": "complete-result",
                "handle": handle,
                "status": "complete",
                "context": context,
                "changes": [self._plain(item) for item in state.changes],
                "changed_units": changed_units,
                "coverage_certificates": certificates,
                "fact_observations": self._observation_projections(state),
                "dispositions": self._disposition_projections(state),
                "reading_plan": [
                    item.as_contract() for item in evaluation.reading_plan
                ],
                "completion": {
                    "required_coverage_subjects": [
                        item.subject for item in evaluation.coverage
                    ],
                    "certificate_subjects": [
                        item.subject
                        for item in evaluation.coverage
                        if item.certificate is not None
                    ],
                    "reached_consumer_obligations": [
                        item.id
                        for item in evaluation.reached_obligations
                        if item.kind == "consumer-review"
                    ],
                    "disposition_obligations": [
                        str(self._plain(item)["obligation_id"])
                        for item in state.dispositions
                    ],
                    "required_fact_requirements": [
                        f"fact-requirement:{item.id}" for item in evaluation.requirements
                    ],
                    "observed_fact_requirements": [
                        f"fact-requirement:{self._plain(item)['requirement_id']}"
                        for item in state.fact_observations
                        if self._plain(item)["requirement_id"]
                        in {value.id for value in evaluation.requirements}
                    ],
                    "non_consumer_obligations_resolved": True,
                    "applicability_resolved": True,
                    "authorization_valid": True,
                    "evidence_valid": True,
                },
                "summary": "The bounded analysis is complete.",
            }
        )

    def _analysis_children(
        self,
        evaluation: AnalysisEvaluation,
    ) -> tuple[tuple[str, str, dict[str, object]], ...]:
        state = evaluation.state
        children: list[tuple[str, str, dict[str, object]]] = [
            ("context", evaluation.context_id, self._context_projection(evaluation))
        ]
        children.extend(
            (
                "fact-requirement",
                item.id,
                self._requirement_projection(state, item),
            )
            for item in evaluation.requirements
        )
        children.extend(
            (
                "obligation",
                self._obligation_child_id(item.id),
                self._obligation_projection(state, item),
            )
            for item in evaluation.obligations
        )
        children.extend(
            (
                "coverage-requirement",
                item.requirement_id,
                self._coverage_requirement_projection(state, item),
            )
            for item in evaluation.coverage
        )
        children.extend(
            (
                "coverage-certificate",
                item.certificate_id,
                self._certificate_projection(state, item),
            )
            for item in evaluation.coverage
            if item.certificate_id is not None
        )
        children.extend(
            (
                "fact-observation",
                value["handle"]["child_id"],
                value,
            )
            for value in self._observation_projections(state)
        )
        return tuple(children)

    def _obligation_work_handle(
        self,
        evaluation: AnalysisEvaluation,
        obligation: object,
    ) -> dict[str, object]:
        if obligation.kind == "audit-coverage":
            coverage = next(
                item
                for item in evaluation.coverage
                if item.subject == obligation.target
            )
            return self._analysis_child_handle(
                evaluation.state.analysis_id,
                "coverage-requirement",
                coverage.requirement_id,
            )
        return self._analysis_child_handle(
            evaluation.state.analysis_id,
            "obligation",
            self._obligation_child_id(obligation.id),
        )

    def _state_projection(self, state: DomainAnalysisState) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": "analysis-state",
            "handle": self._analysis_handle(state.analysis_id),
            "base_snapshot": self._snapshot_handle(state.base_snapshot),
            "changes": [self._plain(item) for item in state.changes],
            "semantic_proposals": [
                self._plain(item) for item in state.semantic_proposals
            ],
            "fact_observations": self._observation_projections(state),
            "dispositions": self._disposition_projections(state),
            "coverage_attestations": self._attestation_projections(state),
            "authorization_records": [
                self._plain(item) for item in state.authorization_records
            ],
            "domain_contracts": [
                self._plain(item) for item in state.domain_contracts
            ],
            "execution_contracts": self._plain(state.execution_contracts),
            "contract_version": 5,
        }
        proposed_ref = state.proposed_material
        value["proposed_reference"] = (
            self._snapshot_handle(proposed_ref.snapshot)
            if isinstance(proposed_ref, SnapshotMaterialRef)
            else self._proposal_revision_handle(proposed_ref.revision_id)
        )
        return value

    def _context_projection(
        self,
        evaluation: AnalysisEvaluation,
    ) -> dict[str, object]:
        return {
            "kind": "analysis-context",
            "handle": self._analysis_child_handle(
                evaluation.state.analysis_id,
                "context",
                evaluation.context_id,
            ),
            **dict(evaluation.context),
        }

    def _requirement_projection(
        self,
        state: DomainAnalysisState,
        requirement: object,
    ) -> dict[str, object]:
        value = dict(requirement.projection)
        context_id = str(value.pop("context_id"))
        return {
            "kind": "fact-requirement",
            "handle": self._analysis_child_handle(
                state.analysis_id,
                "fact-requirement",
                requirement.id,
            ),
            **value,
            "context": self._analysis_child_handle(
                state.analysis_id,
                "context",
                context_id,
            ),
        }

    def _requirement_work(
        self,
        state: DomainAnalysisState,
        requirement: object,
    ) -> dict[str, object]:
        return {
            "requirement": self._requirement_projection(state, requirement),
            "prompt": requirement.prompt,
            "dependent_programs": list(requirement.dependent_programs),
        }

    def _obligation_projection(
        self,
        state: DomainAnalysisState,
        obligation: object,
    ) -> dict[str, object]:
        value = obligation.as_contract()
        identifier = str(value.pop("id"))
        value["handle"] = self._analysis_child_handle(
            state.analysis_id,
            "obligation",
            self._obligation_child_id(identifier),
        )
        return value

    def _coverage_requirement_projection(
        self,
        state: DomainAnalysisState,
        coverage: object,
    ) -> dict[str, object]:
        value = dict(coverage.requirement)
        value.pop("view_digest")
        return {
            "kind": "coverage-requirement",
            "handle": self._analysis_child_handle(
                state.analysis_id,
                "coverage-requirement",
                coverage.requirement_id,
            ),
            **value,
        }

    def _certificate_projection(
        self,
        state: DomainAnalysisState,
        coverage: object,
    ) -> dict[str, object]:
        if coverage.certificate is None or coverage.certificate_id is None:
            raise RuntimeError("certificate projection requires a certificate")
        value = dict(coverage.certificate)
        value.pop("attestation_digest")
        requirement_id = str(value.pop("requirement_id"))
        return {
            "kind": "coverage-certificate",
            "handle": self._analysis_child_handle(
                state.analysis_id,
                "coverage-certificate",
                coverage.certificate_id,
            ),
            "requirement": self._analysis_child_handle(
                state.analysis_id,
                "coverage-requirement",
                requirement_id,
            ),
            **value,
        }

    def _observation_projections(
        self,
        state: DomainAnalysisState,
    ) -> list[dict[str, object]]:
        authorizations = self._authorization_references(state)
        result = []
        for record in state.fact_observations:
            value = self._plain(record)
            identifier = analysis_child_id(value)
            projected = {
                "kind": "fact-observation",
                "handle": self._analysis_child_handle(
                    state.analysis_id,
                    "fact-observation",
                    identifier,
                ),
                "requirement": self._analysis_child_handle(
                    state.analysis_id,
                    "fact-requirement",
                    str(value["requirement_id"]),
                ),
                "value": value["value"],
                "evidence": value["evidence"],
                "authorization": authorizations[str(value["authorization_id"])],
            }
            if value.get("provider") is not None:
                projected["provider"] = value["provider"]
            result.append(projected)
        return result

    def _disposition_projections(
        self,
        state: DomainAnalysisState,
    ) -> list[dict[str, object]]:
        authorizations = self._authorization_references(state)
        result = []
        for record in state.dispositions:
            value = self._plain(record)
            obligation_id = str(value["obligation_id"])
            result.append(
                {
                    "obligation": self._analysis_child_handle(
                        state.analysis_id,
                        "obligation",
                        self._obligation_child_id(obligation_id),
                    ),
                    "kind": value["kind"],
                    "result": value["result"],
                    "rationale": value["rationale"],
                    "evidence": value["evidence"],
                    "authorization": authorizations[
                        str(value["authorization_id"])
                    ],
                    "fingerprint": value["fingerprint"],
                }
            )
        return result

    def _attestation_projections(
        self,
        state: DomainAnalysisState,
    ) -> list[dict[str, object]]:
        authorizations = self._authorization_references(state)
        result = []
        for record in state.coverage_attestations:
            value = self._plain(record)
            result.append(
                {
                    "kind": "coverage-attestation",
                    "requirement": self._analysis_child_handle(
                        state.analysis_id,
                        "coverage-requirement",
                        str(value["requirement_id"]),
                    ),
                    "conclusion": value["conclusion"],
                    "evidence": value["evidence"],
                    "explicit_exclusions": value["explicit_exclusions"],
                    "rationale": value["rationale"],
                    "auditor_provenance": value["auditor_provenance"],
                    "schema_version": value["schema_version"],
                    "authorization": authorizations[
                        str(value["authorization_id"])
                    ],
                }
            )
        return result

    def _authorization_references(
        self,
        state: DomainAnalysisState,
    ) -> dict[str, dict[str, object]]:
        return {
            str(value["reference"]["id"]): dict(value["reference"])
            for record in state.authorization_records
            for value in (self._plain(record),)
        }

    @staticmethod
    def _domain_contracts() -> tuple[dict[str, str], ...]:
        return (
            {
                "id": "standards-analysis",
                "version": str(ANALYSIS_CONTRACT_VERSION),
            },
            {"id": "standards-applicability", "version": str(LANGUAGE_VERSION)},
            {"id": "standards-coverage", "version": str(HORIZON_VERSION)},
            {"id": "standards-graph", "version": "1"},
            {"id": "standards-identity", "version": "2"},
            {"id": "standards-metadata", "version": "1"},
            {"id": "standards-policy-impact", "version": "2"},
        )

    @staticmethod
    def _plain(value: object) -> dict[str, object]:
        return plain_record(value)

    @staticmethod
    def _analysis_handle(analysis_id: str) -> dict[str, object]:
        return {
            "kind": "analysis-handle",
            "id": analysis_id,
            "schema_version": 6,
        }

    @classmethod
    def _analysis_child_handle(
        cls,
        analysis_id: str,
        child_kind: str,
        child_id: str,
    ) -> dict[str, object]:
        return {
            "kind": "analysis-child-handle",
            "analysis": cls._analysis_handle(analysis_id),
            "child_kind": child_kind,
            "child_id": child_id,
            "schema_version": 6,
        }

    @staticmethod
    def _obligation_child_id(obligation_id: str) -> str:
        prefix = "obligation:"
        if not obligation_id.startswith(prefix):
            raise RuntimeError("obligation identity has an invalid domain")
        return obligation_id.removeprefix(prefix)

    @staticmethod
    def _current_child(
        handle: AnalysisChildHandle,
        state: DomainAnalysisState,
        kind: str,
    ) -> None:
        if handle.analysis.id != state.analysis_id or handle.child_kind != kind:
            StandardsEngine._not_applicable()

    @staticmethod
    def _evidence(values: object) -> tuple[EvidenceReference, ...]:
        return tuple(
            EvidenceReference(
                str(item.id),
                str(item.digest),
                str(item.provider_contract),
                str(item.provider_contract_version),
            )
            for item in values
        )

    @staticmethod
    def _not_applicable() -> None:
        raise AnalysisError(
            AnalysisFailure(
                "SUBMISSION.NOT_APPLICABLE",
                "invalid",
                "The submission does not address current analysis work.",
            )
        )

    def _route(
        self,
        snapshot: SnapshotHandle,
        compiled: CompiledSnapshot,
        request: RouteRequest,
    ) -> RouteResult:
        return RouteResult.from_value(
            self._route_value(_QueryProjection.snapshot(snapshot), compiled, request)
        )

    def _route_value(
        self,
        projection: _QueryProjection,
        compiled: CompiledSnapshot,
        request: RouteRequest,
    ) -> dict[str, object]:
        facts = compiled.router.fact_schema.bind(request.as_contract()["facts"])
        selected = set(compiled.router.base_modules)
        unresolved: set[str] = set()
        rule_results: list[tuple[object, str]] = []
        for rule in compiled.router.rules:
            result = rule.program.evaluate(facts)
            if result.truth is Truth.TRUE:
                selected.add(rule.target)
                rule_results.append((rule, "selected"))
            elif result.truth is Truth.UNKNOWN:
                rule_results.append((rule, "unresolved"))
                unresolved.update(result.unresolved_facts)
        ordered = compiled.graph.dependency_order(METADATA_REQUIRES, selected=selected)
        closure = set(ordered)
        preferred = (
            *(item for item in ("core", "router") if item in closure),
            *sorted(closure - selected - {"core", "router"}),
            *sorted(selected - {"core", "router"}),
        )
        ordered = compiled.graph.dependency_order(
            METADATA_REQUIRES, selected=selected, preferred_order=preferred
        )
        closure = set(ordered)
        rank = {target: index for index, target in enumerate(ordered)}
        scope = ReviewScope("whole-artifact")
        selections = [
            ReadingSelection(
                target,
                scope,
                RoutingBaseCause(compiled.router.id),
                "selected",
                0 if target in {"core", "router"} else 2,
                rank[target],
            )
            for target in compiled.router.base_modules
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
                for item in compiled.graph.incoming(target, (METADATA_REQUIRES,))
            )
            if edge.source in closure
        )
        entries = compile_reading_plan(
            selections,
            lambda target: canonical_target_authority(
                target, compiled.corpus, compiled.graph
            ),
        )
        reading_plan = [
            projection.reading_plan_entry(item.as_contract()) for item in entries
        ]
        questions = [
            self._route_question(compiled.router, fact) for fact in sorted(unresolved)
        ]
        return {
            **projection.result("route"),
            "reading_plan": reading_plan,
            "unresolved_questions": questions,
            "next_operations": [
                projection.next_operation("read", str(item["target"]))
                for item in reading_plan
                if item["state"] == "selected"
            ],
            "summary": (
                f"Selected {len(ordered)} standards with "
                f"{len(questions)} unresolved fact categories."
            ),
        }

    def _read(
        self,
        snapshot: SnapshotHandle,
        compiled: CompiledSnapshot,
        request: ReadRequest,
    ) -> ReadResult | RejectedResult:
        value = self._read_value(_QueryProjection.snapshot(snapshot), compiled, request)
        return (
            value if isinstance(value, RejectedResult) else ReadResult.from_value(value)
        )

    def _read_value(
        self,
        projection: _QueryProjection,
        compiled: CompiledSnapshot,
        request: ReadRequest,
    ) -> dict[str, object] | RejectedResult:
        selected = _resolve_policy(compiled.corpus, request.target)
        if selected is None:
            return self._reject(
                "NAVIGATION.UNKNOWN_POLICY", "unavailable", "The policy is unavailable."
            )
        policy, module = selected
        relationships = self._relationships(
            projection, compiled, policy, module, None, Direction.BOTH, False
        )
        if isinstance(policy, PolicyUnit):
            content = policy.content
            scope = {"kind": "structured", "heading_path": list(policy.heading_path)}
            target = policy.id
        else:
            content = compiled.source.read_bytes(module.path).decode("utf-8")
            scope = {"kind": "whole-artifact"}
            target = module.module_id
        next_operations = [projection.next_operation("related", target)]
        inspection = projection.inspect_operation(target)
        if inspection is not None:
            next_operations.append(inspection)
        return {
            **projection.result("read"),
            "policy": projection.policy_summary(
                target,
                "contextual" if module.role == "reference" else "normative",
                scope,
            ),
            "content": content,
            "requires": list(module.requires),
            "specializes": list(module.specializes),
            "related": relationships,
            "next_operations": next_operations,
            "summary": projection.read_summary(target),
        }

    def _related(
        self,
        snapshot: SnapshotHandle,
        compiled: CompiledSnapshot,
        request: RelatedRequest,
    ) -> RelatedResult | RejectedResult:
        value = self._related_value(
            _QueryProjection.snapshot(snapshot), compiled, request
        )
        return (
            value
            if isinstance(value, RejectedResult)
            else RelatedResult.from_value(value)
        )

    def _related_value(
        self,
        projection: _QueryProjection,
        compiled: CompiledSnapshot,
        request: RelatedRequest,
    ) -> dict[str, object] | RejectedResult:
        selected = _resolve_policy(compiled.corpus, request.target)
        if selected is None:
            return self._reject(
                "NAVIGATION.UNKNOWN_POLICY", "unavailable", "The policy is unavailable."
            )
        policy, module = selected
        relationships = self._relationships(
            projection,
            compiled,
            policy,
            module,
            tuple(request.groups),
            Direction.parse(request.direction),
            request.transitive,
        )
        target = policy.id if isinstance(policy, PolicyUnit) else module.module_id
        units = compiled.corpus.policy_unit_corpus.for_module(module.module_id)
        mapping = (
            {"state": "exact-policy-unit", "policy_units": [policy.id]}
            if isinstance(policy, PolicyUnit)
            else {
                "state": "policy-units-present" if units else "incomplete",
                **({} if units else {"reason": "no-policy-units"}),
                "policy_units": [item.id for item in units],
            }
        )
        return {
            **projection.result("related"),
            "target": target,
            "policy_unit_mapping": mapping,
            "relationships": relationships,
            "next_operations": [],
            "summary": f"Found {len(relationships)} declared relationships.",
        }

    def _relationships(
        self,
        projection: _QueryProjection,
        compiled: CompiledSnapshot,
        selected: PolicyUnit | ModuleMetadata,
        module: ModuleMetadata,
        groups: tuple[str, ...] | None,
        direction: Direction,
        transitive: bool,
    ) -> list[dict[str, object]]:
        targets = (
            (selected.id,)
            if isinstance(selected, PolicyUnit)
            else (
                module.module_id,
                *(item.id for item in compiled.corpus.policy_unit_corpus.for_module(module.module_id)),
            )
        )
        chosen: dict[tuple[str, str], dict[str, object]] = {}
        for target in targets:
            if transitive:
                steps = [
                    step
                    for group in groups or ()
                    for step in compiled.graph.traverse_group(
                        target, group, direction, transitive=True
                    ).steps
                ]
                pairs = ((item.edge, item.direction) for item in steps)
            else:
                views = (
                    compiled.graph.incoming(target, groups)
                    if direction is Direction.INCOMING
                    else compiled.graph.outgoing(target, groups)
                    if direction is Direction.OUTGOING
                    else compiled.graph.incident(target, groups)
                )
                pairs = ((item.edge, item.direction) for item in views)
            for edge, selected_direction in pairs:
                chosen[(edge.id, selected_direction.value)] = self._relationship_summary(
                    projection, compiled, edge, selected_direction
                )
        return [chosen[key] for key in sorted(chosen)]

    def _relationship_summary(
        self,
        projection: _QueryProjection,
        compiled: CompiledSnapshot,
        edge: Edge,
        direction: Direction,
    ) -> dict[str, object]:
        semantics = compiled.policy_impact.semantics.get(edge.id)
        return projection.relationship_summary(
            f"{direction.value}:{edge.id}",
            {
                "source": edge.source,
                "target": edge.target,
                "relation": edge.relation,
                "groups": list(edge.groups),
                "direction": direction.value,
                "traversal_eligible": edge.traversable,
                "applicability": "unknown" if semantics is not None else "not-declared",
            },
        )

    def _inspect_snapshot_child(
        self, handle: SnapshotChildHandle
    ) -> PolicyInspectionResult | RelationshipInspectionResult | RejectedResult:
        compiled = self._compiled_snapshot(self._snapshot_id(handle.snapshot))
        if handle.child_kind == "policy":
            selected = _resolve_policy(compiled.corpus, handle.child_id)
            if selected is None:
                return self._reject(
                    "INSPECTION.UNKNOWN_POLICY",
                    "unavailable",
                    "The policy child is unavailable.",
                )
            policy, module = selected
            if isinstance(policy, PolicyUnit):
                declaration = policy.as_declaration()
                representation = policy.representation_digest
                structural = policy.structural_digest
                source_path = policy.source
            else:
                raw = compiled.source.read_bytes(module.path)
                declaration = _module_declaration(module)
                representation = "sha256:" + hashlib.sha256(raw).hexdigest()
                structural = markdown_structural_digest(raw)
                source_path = module.path
            return PolicyInspectionResult.from_value(
                {
                    "kind": "policy-inspection-result",
                    "policy": handle.as_contract(),
                    "declaration": declaration,
                    "representation_digest": representation,
                    "structural_digest": structural,
                    "provenance": {
                        "snapshot": handle.snapshot.as_contract(),
                        "path": source_path.split("/"),
                    },
                }
            )
        if handle.child_kind == "relationship":
            direction_value, separator, edge_id = handle.child_id.partition(":")
            if not separator or direction_value not in {"incoming", "outgoing"}:
                return self._reject(
                    "INSPECTION.INVALID_RELATIONSHIP_HANDLE",
                    "invalid",
                    "The relationship child identity is malformed.",
                )
            try:
                edge = compiled.graph.edge(edge_id)
            except GraphError:
                return self._reject(
                    "INSPECTION.UNKNOWN_RELATIONSHIP",
                    "unavailable",
                    "The relationship child is unavailable.",
                )
            direction = Direction.parse(direction_value)
            semantics = compiled.policy_impact.semantics.get(edge.id)
            return RelationshipInspectionResult.from_value(
                {
                    "kind": "relationship-inspection-result",
                    "relationship": self._relationship_summary(
                        _QueryProjection.snapshot(handle.snapshot),
                        compiled,
                        edge,
                        direction,
                    ),
                    "policy_semantics": (
                        None
                        if semantics is None
                        else {
                            "relationship_kind": semantics.relation,
                            "applicability": semantics.applicability_program.as_expression(),
                            "source_scope": thaw(semantics.source_scope),
                            "consumer_scope": thaw(semantics.consumer_scope),
                            "propagation": semantics.propagation,
                            "evidence_owner": semantics.evidence_owner,
                            "rationale": semantics.rationale,
                        }
                    ),
                    "provenance": {
                        "snapshot": handle.snapshot.as_contract(),
                        "path": edge.provenance.locator.split("/"),
                    },
                }
            )
        return self._reject(
            "INSPECTION.UNSUPPORTED_HANDLE",
            "unsupported",
            "The snapshot child kind is unsupported.",
        )

    @staticmethod
    def _route_question(router: RouterProjection, fact_id: str) -> dict[str, object]:
        fact = next(item for item in router.facts if item.id == fact_id)
        return {
            "id": f"question.{fact_id}",
            "kind": "applicability-fact",
            "prompt": fact.prompt,
            "state": "required",
            "permitted_answers": [*fact.values, "none"],
        }

    @staticmethod
    def _snapshot_handle(snapshot: SnapshotId) -> dict[str, object]:
        return {"kind": "snapshot-handle", "id": str(snapshot), "schema_version": 5}

    @staticmethod
    def _proposal_handle(proposal: ProposalId) -> dict[str, object]:
        return {"kind": "proposal-handle", "id": str(proposal), "schema_version": 1}

    @staticmethod
    def _proposal_revision_handle(revision: str) -> dict[str, object]:
        return {
            "kind": "proposal-revision-handle",
            "id": revision,
            "schema_version": 1,
        }

    @staticmethod
    def _readiness_handle(readiness: str) -> dict[str, object]:
        return {
            "kind": "readiness-handle",
            "id": readiness,
            "schema_version": 1,
        }

    @classmethod
    def _proposal_summary(cls, summary: AuthoringProposalSummary) -> dict[str, object]:
        return {
            "proposal": cls._proposal_handle(summary.proposal),
            "head_revision": cls._proposal_revision_handle(summary.head_revision),
        }

    @classmethod
    def _summary(cls, summary: SnapshotSummary) -> dict[str, object]:
        value: dict[str, object] = {
            "snapshot": cls._snapshot_handle(summary.snapshot),
            "lifecycle": summary.lifecycle,
            "source_revision": summary.source_revision,
            "created_at": summary.created_at,
        }
        if summary.purge_deadline is not None:
            value["purge_deadline"] = summary.purge_deadline
        return value

    @staticmethod
    def _snapshot_id(handle: SnapshotHandle) -> SnapshotId:
        return SnapshotId(handle.id)

    @staticmethod
    def _domain_errors() -> tuple[type[Exception], ...]:
        return (
            SnapshotError,
            AuthoringError,
            GitRepositoryError,
            MetadataError,
            PolicyImpactError,
            AnalysisError,
            ApplicabilityError,
            GraphError,
        )

    @classmethod
    def _domain_rejection(cls, error: Exception) -> RejectedResult:
        failure = getattr(error, "failure", None)
        if failure is None:
            raise error
        outcome = getattr(failure, "outcome", getattr(failure, "kind", "invalid"))
        return cls._reject(failure.code, outcome, failure.message)

    @classmethod
    def _analysis_unavailable(cls) -> RejectedResult:
        return cls._reject(
            "ANALYSIS.CUTOVER_INCOMPLETE",
            "unavailable",
            "The immutable A1c analysis aggregate is not yet available.",
        )

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


def _resolve_policy(
    corpus: CanonicalStandardsCorpus, requested: str
) -> tuple[PolicyUnit | ModuleMetadata, ModuleMetadata] | None:
    unit = corpus.resolve_policy_unit(requested)
    if isinstance(unit, PolicyUnit):
        module = corpus.resolve_module(unit.module)
        if module is None:
            return None
        return unit, module
    module = corpus.resolve_module(requested)
    if module is None:
        return None
    return module, module


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


__all__ = ("DEFAULT_STORE", "StandardsEngine")
