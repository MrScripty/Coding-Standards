from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Mapping

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_metadata.standards_metadata import CanonicalStandardsCorpus
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
)

from .changes import (
    ChangeDescriptor,
    ChangeKind,
    ClassifiedChange,
    ReviewScope,
    SemanticProposal,
    classify_changes,
)
from .coverage import (
    ConsumerCoverageCertificate,
    CoverageAttestation,
    CoverageEvidence,
    CoverageIndex,
    certify_coverage,
)
from .errors import AnalysisError, AnalysisFailure
from .facts import (
    AnalysisContext,
    AuthorizationReference,
    EvidenceReference,
    FactObservation,
    FactObservationProvider,
    FactRequirement,
    NoObservation,
    ObservationClaim,
    ProviderUnavailable,
    build_analysis_context,
    build_fact_requirement,
    generate_fact_requirements,
    observe_fact,
    validate_observation,
)
from .impact import select_impact
from .obligations import (
    DecisionDependency,
    DecisionFingerprint,
    Obligation,
    generate_consumer_review_obligations,
    generate_coverage_obligations,
    generate_unmapped_normative_obligations,
)
from .reading import (
    ReadingPlanEntry,
    canonical_target_authority,
    compile_reading_plan,
    consumer_reading_selections,
)
from .results import (
    AnalysisResult,
    CompleteResult,
    ConsumerDispositionSubmission,
    CoverageAttestationSubmission,
    CoverageDecision,
    DispositionRecord,
    ImpactDispositionSubmission,
    PendingResult,
    ProvideFactSubmission,
    Submission,
    build_pending_result,
)
from .serialization import canonical_json_bytes, identity
from .snapshots import AnalysisVersions


ANALYSIS_DOMAIN = "coding-standards:analysis:v3"
AUTHORIZATION_VIEW_DOMAIN = "coding-standards:authorization-authority-view:v1"
PROVIDER_VIEW_DOMAIN = "coding-standards:provider-authority-view:v1"
AUTHORIZATION_CONTRACT = "authorization-authority.v1"
PROVIDER_VIEW_CONTRACT = "provider-authority.v1"


def _error(
    code: str,
    message: str,
    *,
    outcome: str = "invalid",
    observed: str | None = None,
) -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, outcome, message, observed=observed))


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze(item) for key, item in sorted(value.items())}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class AnalysisAuthority:
    root: Path
    snapshot: Mapping[str, object]
    corpus: CanonicalStandardsCorpus
    graph: EdgeRegistry
    policy_impact: CompiledPolicyImpactSet
    coverage: CoverageIndex


@dataclass(frozen=True, slots=True)
class AnalysisInput:
    changes: tuple[ChangeDescriptor, ...]
    semantic_proposals: tuple[SemanticProposal, ...]


@dataclass(frozen=True, slots=True)
class AuthorizationAuthorityView:
    id: str
    authorizations: tuple[AuthorizationReference, ...]
    issuers: tuple[str, ...]
    capabilities: tuple[str, ...]
    revocation_digest: str
    contract_version: str = AUTHORIZATION_CONTRACT

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "authorization-authority-view",
            "id": self.id,
            "contract_version": self.contract_version,
            "issuers": list(self.issuers),
            "capabilities": list(self.capabilities),
            "revocation_digest": self.revocation_digest,
            "authorizations": [item.as_contract() for item in self.authorizations],
        }


def build_authorization_view(
    authorizations: Iterable[AuthorizationReference],
) -> AuthorizationAuthorityView:
    selected = tuple(sorted(authorizations, key=lambda item: item.capability))
    if len({item.capability for item in selected}) != len(selected):
        raise _error(
            "ANALYSIS.AUTHORIZATION_DUPLICATE",
            "analysis authorizations must be unique by capability",
        )
    projection = {
        "contract_version": AUTHORIZATION_CONTRACT,
        "issuers": ["trusted-engine-context"],
        "capabilities": [item.capability for item in selected],
        "authorizations": [item.as_contract() for item in selected],
    }
    revocation_digest = identity(
        AUTHORIZATION_VIEW_DOMAIN,
        "authorization-revocation",
        projection["authorizations"],
    ).replace("authorization-revocation:", "")
    identity_projection = {
        **projection,
        "revocation_digest": revocation_digest,
    }
    return AuthorizationAuthorityView(
        identity(
            AUTHORIZATION_VIEW_DOMAIN,
            "authorization-authority-view",
            identity_projection,
        ),
        selected,
        ("trusted-engine-context",),
        tuple(item.capability for item in selected),
        revocation_digest,
    )


@dataclass(frozen=True, slots=True)
class ProviderContractView:
    id: str
    contract_version: str
    input_contract: str
    immutable_inputs: tuple[Mapping[str, object], ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "immutable_inputs",
            tuple(_freeze(item) for item in self.immutable_inputs),
        )

    def as_contract(self) -> dict[str, object]:
        return {
            "id": self.id,
            "contract_version": self.contract_version,
            "input_contract": self.input_contract,
            "immutable_inputs": [_thaw(item) for item in self.immutable_inputs],
        }


@dataclass(frozen=True, slots=True)
class ProviderAuthorityView:
    id: str
    evidence_contracts: tuple[tuple[str, str], ...]
    providers: tuple[ProviderContractView, ...]
    contract_version: str = PROVIDER_VIEW_CONTRACT

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "provider-authority-view",
            "id": self.id,
            "contract_version": self.contract_version,
            "evidence_contracts": [
                {"id": key, "version": value} for key, value in self.evidence_contracts
            ],
            "providers": [item.as_contract() for item in self.providers],
        }

    def evidence_versions(self) -> dict[str, str]:
        return dict(self.evidence_contracts)


def build_provider_view(
    providers: Iterable[FactObservationProvider],
    base_snapshot: Mapping[str, object],
    proposed_snapshot: Mapping[str, object],
) -> ProviderAuthorityView:
    selected = tuple(sorted(providers, key=lambda item: item.id))
    if len({item.id for item in selected}) != len(selected):
        raise _error(
            "FACT.PROVIDER_DUPLICATE",
            "fact observation providers must have unique identities",
        )
    records = []
    versions = dict(AnalysisVersions().evidence_provider_contract_versions)
    for provider in selected:
        input_contract = getattr(provider, "input_contract", None)
        immutable_inputs = getattr(provider, "immutable_inputs", None)
        if input_contract != "standards-snapshots" or immutable_inputs is None:
            raise _error(
                "FACT.PROVIDER_INPUT_CONTRACT",
                "fact providers must declare their immutable input contract",
                observed=provider.id,
            )
        previous = versions.get(provider.id)
        if previous is not None and previous != provider.contract_version:
            raise _error(
                "FACT.PROVIDER_CONTRACT_CONFLICT",
                "fact provider conflicts with a registered provider contract",
                observed=provider.id,
            )
        versions[provider.id] = provider.contract_version
        input_values = {
            canonical_json_bytes(item): dict(item)
            for item in (
                dict(base_snapshot),
                dict(proposed_snapshot),
                *(dict(item) for item in immutable_inputs),
            )
        }
        records.append(
            ProviderContractView(
                provider.id,
                provider.contract_version,
                input_contract,
                tuple(input_values[key] for key in sorted(input_values)),
            )
        )
    evidence_contracts = tuple(sorted(versions.items()))
    projection = {
        "contract_version": PROVIDER_VIEW_CONTRACT,
        "evidence_contracts": [
            {"id": key, "version": value} for key, value in evidence_contracts
        ],
        "providers": [item.as_contract() for item in records],
    }
    return ProviderAuthorityView(
        identity(
            PROVIDER_VIEW_DOMAIN,
            "provider-authority-view",
            projection,
        ),
        evidence_contracts,
        tuple(records),
    )


@dataclass(frozen=True, slots=True)
class AnalysisState:
    id: str
    base_snapshot: Mapping[str, object]
    proposed_snapshot: Mapping[str, object]
    changes: tuple[ChangeDescriptor, ...]
    semantic_proposals: tuple[SemanticProposal, ...]
    authorization_view: AuthorizationAuthorityView
    provider_view: ProviderAuthorityView
    observations: tuple[FactObservation, ...]
    dispositions: tuple[DispositionRecord, ...]
    coverage_decisions: tuple[CoverageDecision, ...]
    provenance: AnalysisVersions

    def __post_init__(self) -> None:
        object.__setattr__(self, "base_snapshot", _freeze(self.base_snapshot))
        object.__setattr__(
            self,
            "proposed_snapshot",
            _freeze(self.proposed_snapshot),
        )

    @property
    def handle(self) -> dict[str, object]:
        return {
            "kind": "analysis-handle",
            "id": self.id,
            "schema_version": 3,
        }

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "analysis-state",
            "handle": self.handle,
            "base_snapshot": _thaw(self.base_snapshot),
            "proposed_snapshot": _thaw(self.proposed_snapshot),
            "changes": [item.as_contract() for item in self.changes],
            "semantic_proposals": [
                _semantic_proposal_contract(item) for item in self.semantic_proposals
            ],
            "authorization_view": self.authorization_view.as_contract(),
            "provider_view": self.provider_view.as_contract(),
            "fact_observations": [item.as_contract() for item in self.observations],
            "dispositions": [item.as_contract() for item in self.dispositions],
            "coverage_decisions": [
                item.as_contract() for item in self.coverage_decisions
            ],
            "provenance": self.provenance.as_contract(),
        }


@dataclass(frozen=True, slots=True)
class AnalysisKernel:
    accepted: AnalysisAuthority
    proposed: AnalysisAuthority
    authorization_view: AuthorizationAuthorityView
    provider_view: ProviderAuthorityView
    providers: tuple[FactObservationProvider, ...]

    def project(self, state: AnalysisState) -> AnalysisResult:
        normalized, evaluation = _normalize(self, state, invoke_providers=False)
        if normalized.id != state.id:
            raise _error(
                "ANALYSIS.STATE_INVALID",
                "stored analysis state is not normalized under its authorities",
                observed=state.id,
            )
        return _project(normalized, evaluation)

    def advance(
        self,
        state: AnalysisState,
        submission: Submission,
        authorization: AuthorizationReference,
    ) -> tuple[AnalysisState, AnalysisResult]:
        current = self.project(state)
        candidate = _apply_submission(
            self,
            state,
            current,
            submission,
            authorization,
        )
        normalized, evaluation = _normalize(
            self,
            candidate,
            invoke_providers=True,
        )
        return normalized, _project(normalized, evaluation)


@dataclass(frozen=True, slots=True)
class _Evaluation:
    accepted: AnalysisAuthority
    proposed: AnalysisAuthority
    changes: tuple[ClassifiedChange, ...]
    context: AnalysisContext
    requirements: tuple[FactRequirement, ...]
    pending_requirements: tuple[FactRequirement, ...]
    obligations: tuple[Obligation, ...]
    reached: tuple[Obligation, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    certificates: tuple[ConsumerCoverageCertificate, ...]


def prepare_analysis(
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
    request: AnalysisInput,
    prior_state: AnalysisState | None = None,
    *,
    authorizations: Iterable[AuthorizationReference] = (),
    providers: Iterable[FactObservationProvider] = (),
) -> tuple[AnalysisState, AnalysisResult]:
    selected_providers = tuple(sorted(providers, key=lambda item: item.id))
    authorization_view = build_authorization_view(authorizations)
    provider_view = build_provider_view(
        selected_providers,
        accepted.snapshot,
        proposed.snapshot,
    )
    kernel = AnalysisKernel(
        accepted,
        proposed,
        authorization_view,
        provider_view,
        selected_providers,
    )
    same_inputs = (
        prior_state is not None
        and dict(prior_state.base_snapshot) == dict(accepted.snapshot)
        and dict(prior_state.proposed_snapshot) == dict(proposed.snapshot)
        and prior_state.changes == request.changes
        and prior_state.semantic_proposals == request.semantic_proposals
    )
    state = _build_state(
        accepted.snapshot,
        proposed.snapshot,
        request.changes,
        request.semantic_proposals,
        authorization_view,
        provider_view,
        () if prior_state is None else prior_state.observations,
        () if prior_state is None or not same_inputs else prior_state.dispositions,
        () if prior_state is None else prior_state.coverage_decisions,
    )
    normalized, evaluation = _normalize(kernel, state, invoke_providers=True)
    return normalized, _project(normalized, evaluation)


def bind_analysis_kernel(
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
    state: AnalysisState,
    *,
    authorizations: Iterable[AuthorizationReference] = (),
    providers: Iterable[FactObservationProvider] = (),
) -> AnalysisKernel:
    selected_providers = tuple(sorted(providers, key=lambda item: item.id))
    authorization_view = build_authorization_view(authorizations)
    provider_view = build_provider_view(
        selected_providers,
        accepted.snapshot,
        proposed.snapshot,
    )
    if dict(state.base_snapshot) != dict(accepted.snapshot) or dict(
        state.proposed_snapshot
    ) != dict(proposed.snapshot):
        raise _error(
            "AUTHORITY.CONTEXT_MISMATCH",
            "analysis state does not bind the supplied authority snapshots",
            observed=state.id,
        )
    if (
        state.authorization_view.id != authorization_view.id
        or state.provider_view.id != provider_view.id
    ):
        raise _error(
            "AUTHORITY.CONTEXT_MISMATCH",
            "analysis state does not bind the supplied execution authority",
            observed=state.id,
        )
    return AnalysisKernel(
        accepted,
        proposed,
        authorization_view,
        provider_view,
        selected_providers,
    )


def bind_projection_kernel(
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
    state: AnalysisState,
) -> AnalysisKernel:
    """Bind pure reprojection to the immutable authority views stored in state."""
    if dict(state.base_snapshot) != dict(accepted.snapshot) or dict(
        state.proposed_snapshot
    ) != dict(proposed.snapshot):
        raise _error(
            "AUTHORITY.CONTEXT_MISMATCH",
            "analysis state does not bind the supplied authority snapshots",
            observed=state.id,
        )
    return AnalysisKernel(
        accepted,
        proposed,
        state.authorization_view,
        state.provider_view,
        (),
    )


def project_analysis(
    kernel: AnalysisKernel,
    state: AnalysisState,
) -> AnalysisResult:
    return kernel.project(state)


def advance_analysis(
    kernel: AnalysisKernel,
    state: AnalysisState,
    submission: Submission,
    authorization: AuthorizationReference,
) -> tuple[AnalysisState, AnalysisResult]:
    return kernel.advance(state, submission, authorization)


def analysis_state_from_contract(value: Mapping[str, object]) -> AnalysisState:
    """Reconstruct and verify one persisted immutable analysis state."""
    try:
        handle = _required_mapping(value, "handle")
        provenance = _required_mapping(value, "provenance")
        if (
            handle.get("schema_version") != 3
            or provenance.get("analysis_schema_version") != 3
            or provenance.get("interface_schema_version") != 10
        ):
            raise _error(
                "ANALYSIS.UNSUPPORTED_VERSION",
                "persisted analysis state version is unsupported",
                outcome="unsupported",
                observed=str(handle.get("schema_version")),
            )
        authorization_value = _required_mapping(value, "authorization_view")
        provider_value = _required_mapping(value, "provider_view")
        authorization_view = _authorization_view_from_contract(authorization_value)
        provider_view = _provider_view_from_contract(provider_value)
        state = _build_state(
            _required_mapping(value, "base_snapshot"),
            _required_mapping(value, "proposed_snapshot"),
            tuple(_change_from_contract(item) for item in value["changes"]),
            tuple(
                _semantic_proposal_from_contract(item)
                for item in value["semantic_proposals"]
            ),
            authorization_view,
            provider_view,
            tuple(
                _observation_from_contract(item) for item in value["fact_observations"]
            ),
            tuple(_disposition_from_contract(item) for item in value["dispositions"]),
            tuple(
                _coverage_decision_from_contract(item)
                for item in value["coverage_decisions"]
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise _error(
            "ANALYSIS.STATE_INVALID",
            "persisted analysis state is malformed",
            observed=str(error),
        ) from error
    if (
        value.get("kind") != "analysis-state"
        or handle != state.handle
        or value.get("provenance") != state.provenance.as_contract()
        or value != state.as_contract()
    ):
        raise _error(
            "ANALYSIS.STATE_IDENTITY_MISMATCH",
            "persisted analysis state does not match its content address",
            observed=str(handle.get("id", "")),
        )
    return state


def _normalize(
    kernel: AnalysisKernel,
    state: AnalysisState,
    *,
    invoke_providers: bool,
) -> tuple[AnalysisState, _Evaluation]:
    _verify_state_authority(kernel, state)
    accepted, proposed, coverage_decisions = _apply_attestations(
        kernel.accepted,
        kernel.proposed,
        state.coverage_decisions,
        kernel.authorization_view,
    )
    changes = classify_changes(
        accepted.corpus.policy_unit_corpus,
        proposed.corpus.policy_unit_corpus,
        state.changes,
        state.semantic_proposals,
    )
    context = build_analysis_context(changes, state.semantic_proposals)
    observations = _valid_observations(kernel, state.observations, context)
    state = _build_state(
        state.base_snapshot,
        state.proposed_snapshot,
        state.changes,
        state.semantic_proposals,
        state.authorization_view,
        state.provider_view,
        observations,
        state.dispositions,
        coverage_decisions,
    )
    while True:
        evaluation = _evaluate(kernel, state, accepted, proposed, changes, context)
        if not invoke_providers:
            break
        observation = _provider_observation(
            kernel,
            evaluation.pending_requirements,
            state.observations,
        )
        if observation is None:
            break
        state = _build_state(
            state.base_snapshot,
            state.proposed_snapshot,
            state.changes,
            state.semantic_proposals,
            state.authorization_view,
            state.provider_view,
            _replace_observation(state.observations, observation),
            state.dispositions,
            state.coverage_decisions,
        )
    dispositions = _valid_dispositions(kernel, state.dispositions, evaluation.reached)
    normalized = _build_state(
        state.base_snapshot,
        state.proposed_snapshot,
        state.changes,
        state.semantic_proposals,
        state.authorization_view,
        state.provider_view,
        state.observations,
        dispositions,
        state.coverage_decisions,
    )
    if dispositions != state.dispositions:
        evaluation = _evaluate(
            kernel,
            normalized,
            accepted,
            proposed,
            changes,
            context,
        )
    return normalized, evaluation


def _evaluate(
    kernel: AnalysisKernel,
    state: AnalysisState,
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
    changes: tuple[ClassifiedChange, ...],
    context: AnalysisContext,
) -> _Evaluation:
    accepted_schema = accepted.policy_impact.fact_schema
    proposed_schema = proposed.policy_impact.fact_schema
    if accepted_schema.digest != proposed_schema.digest:
        raise _error(
            "FACT_SCHEMA_EVOLUTION_UNSUPPORTED",
            "accepted and proposed fact schemas differ",
            outcome="unsupported",
            observed=proposed_schema.digest,
        )
    raw_facts: dict[str, object] = {}
    observations = {str(item.requirement["id"]): item for item in state.observations}
    applied_requirements: set[str] = set()
    while True:
        fact_set = proposed_schema.bind(raw_facts)
        selections = tuple(
            select_impact(
                change,
                accepted.graph,
                proposed.graph,
                accepted.policy_impact,
                proposed.policy_impact,
                fact_set,
            )
            for change in changes
        )
        requirements = generate_fact_requirements(
            selections,
            context,
            proposed_schema,
        )
        newly_applied = False
        for requirement in requirements:
            observation = observations.get(requirement.id)
            if observation is None or requirement.id in applied_requirements:
                continue
            raw_facts[requirement.fact] = dict(observation.value)
            applied_requirements.add(requirement.id)
            newly_applied = True
            break
        if not newly_applied:
            break
    pending_requirements = tuple(
        item for item in requirements if item.id not in applied_requirements
    )
    material_requirement_ids = applied_requirements | {
        item.id for item in pending_requirements
    }
    material_requirements = tuple(
        sorted(
            (
                build_fact_requirement(fact, context, ())
                for fact in proposed_schema.definitions
                if build_fact_requirement(fact, context, ()).id
                in material_requirement_ids
            ),
            key=lambda item: item.id,
        )
    )
    consumer_obligations = generate_consumer_review_obligations(selections)
    coverage_obligations = generate_coverage_obligations(
        changes,
        accepted.coverage,
        proposed.coverage,
    )
    unmapped_obligations = generate_unmapped_normative_obligations(
        accepted.root,
        accepted.corpus,
        proposed.root,
        proposed.corpus,
        changes,
    )
    reached = tuple(
        sorted(
            {
                item.id: item
                for item in (
                    *consumer_obligations,
                    *coverage_obligations,
                    *unmapped_obligations,
                )
            }.values(),
            key=lambda item: item.id,
        )
    )
    records = {item.obligation_id: item for item in state.dispositions}
    current = tuple(
        replace(
            obligation,
            state=(
                "blocked"
                if records.get(obligation.id) is not None
                and records[obligation.id].result == "blocked"
                else "resolved"
                if obligation.id in records
                else "required"
            ),
        )
        for obligation in reached
    )
    reading_plan = _reading_plan(reached, accepted, proposed)
    certificates = _available_certificates(changes, accepted, proposed)
    return _Evaluation(
        accepted,
        proposed,
        changes,
        context,
        material_requirements,
        pending_requirements,
        current,
        reached,
        reading_plan,
        certificates,
    )


def _project(state: AnalysisState, evaluation: _Evaluation) -> AnalysisResult:
    outstanding = tuple(
        item for item in evaluation.obligations if item.state != "resolved"
    )
    if outstanding or evaluation.pending_requirements:
        return build_pending_result(
            state.handle,
            evaluation.changes,
            outstanding,
            evaluation.pending_requirements,
            evaluation.reading_plan,
            context=evaluation.context,
            summary="The bounded analysis requires additional decisions.",
        )
    return _complete_result(state, evaluation)


def _complete_result(
    state: AnalysisState,
    evaluation: _Evaluation,
) -> CompleteResult:
    dispositions = tuple(
        sorted(state.dispositions, key=lambda item: item.obligation_id)
    )
    consumer_ids = tuple(
        sorted(item.id for item in evaluation.reached if item.kind == "consumer-review")
    )
    disposition_ids = tuple(
        sorted(
            item.obligation_id
            for item in dispositions
            if item.kind == "consumer-disposition"
        )
    )
    if consumer_ids != disposition_ids:
        raise _error(
            "ANALYSIS.CONSUMER_SET_MISMATCH",
            "consumer obligations and dispositions are not equal",
            outcome="incomplete",
        )
    required_facts = tuple(sorted(item.id for item in evaluation.requirements))
    observation_ids = {str(item.requirement["id"]): item for item in state.observations}
    observed_facts = tuple(
        sorted(item for item in required_facts if item in observation_ids)
    )
    if required_facts != observed_facts:
        raise _error(
            "ANALYSIS.FACT_SET_MISMATCH",
            "material fact requirements and observations are not equal",
            outcome="incomplete",
        )
    certificates = _relevant_certificates(
        evaluation.changes,
        evaluation.accepted,
        evaluation.proposed,
    )
    coverage_subjects = tuple(sorted(item.subject for item in certificates))
    completion = MappingProxyType(
        {
            "required_coverage_subjects": list(coverage_subjects),
            "certificate_subjects": list(coverage_subjects),
            "reached_consumer_obligations": list(consumer_ids),
            "disposition_obligations": list(disposition_ids),
            "required_fact_requirements": list(required_facts),
            "observed_fact_requirements": list(observed_facts),
            "non_consumer_obligations_resolved": True,
            "applicability_resolved": True,
            "authorization_valid": True,
            "evidence_valid": True,
        }
    )
    return CompleteResult(
        state.handle,
        state.base_snapshot,
        state.proposed_snapshot,
        evaluation.context,
        evaluation.changes,
        certificates,
        tuple(sorted(state.observations, key=lambda item: item.id)),
        dispositions,
        evaluation.reading_plan,
        completion,
        AnalysisVersions(),
        "The bounded read-only impact analysis is complete.",
    )


def _apply_submission(
    kernel: AnalysisKernel,
    state: AnalysisState,
    current: AnalysisResult,
    submission: Submission,
    authorization: AuthorizationReference,
) -> AnalysisState:
    if not isinstance(current, PendingResult):
        raise _error(
            "SUBMISSION.NOT_APPLICABLE",
            "a complete analysis has no current work",
            observed=state.id,
        )
    if isinstance(submission, ProvideFactSubmission):
        requirement_id = str(submission.requirement["id"])
        requirement = _exact_requirement(current, requirement_id)
        fact = kernel.proposed.policy_impact.fact_schema.resolve(requirement.fact)
        if fact is None:
            raise _error(
                "FACT.CONTRACT_UNAVAILABLE",
                "fact contract is unavailable from proposed authority",
                outcome="unavailable",
                observed=requirement.fact,
            )
        observation = observe_fact(
            requirement,
            fact,
            submission.value,
            submission.evidence,
            authorization,
            state.provider_view.evidence_versions(),
        )
        return _build_state(
            state.base_snapshot,
            state.proposed_snapshot,
            state.changes,
            state.semantic_proposals,
            state.authorization_view,
            state.provider_view,
            _replace_observation(state.observations, observation),
            state.dispositions,
            state.coverage_decisions,
        )
    obligation = _exact_obligation(current, submission.obligation_id)
    expected_capability = {
        "consumer-disposition": "standards.review.consumer",
        "impact-disposition": "standards.review.impact",
        "coverage-attestation": "standards.review.audit",
    }[submission.kind]
    if authorization.capability != expected_capability:
        raise _error(
            "ANALYSIS.UNAUTHORIZED",
            "trusted authorization does not grant this review operation",
            outcome="unauthorized",
            observed=authorization.capability,
        )
    if submission.kind not in obligation.permitted_submissions:
        raise _error(
            "SUBMISSION.NOT_APPLICABLE",
            "submission kind does not address the selected obligation",
            observed=submission.kind,
        )
    if isinstance(submission, CoverageAttestationSubmission):
        _validate_attestation(kernel, state, obligation, submission.attestation)
        decisions = {item.attestation.handle: item for item in state.coverage_decisions}
        decisions[submission.attestation.handle] = CoverageDecision(
            submission.attestation,
            authorization,
        )
        return _build_state(
            state.base_snapshot,
            state.proposed_snapshot,
            state.changes,
            state.semantic_proposals,
            state.authorization_view,
            state.provider_view,
            state.observations,
            state.dispositions,
            tuple(decisions[key] for key in sorted(decisions)),
        )
    if not isinstance(
        submission,
        (ConsumerDispositionSubmission, ImpactDispositionSubmission),
    ):
        raise _error("ANALYSIS.SUBMISSION_KIND", "submission is unsupported")
    if submission.fingerprint.as_contract() != obligation.fingerprint.as_contract():
        raise _error(
            "SUBMISSION.CONTEXT_MISMATCH",
            "disposition dependencies do not match current work",
            observed=obligation.id,
        )
    if submission.result == "updated" and not _target_changed(
        kernel.accepted.coverage,
        kernel.proposed.coverage,
        obligation.target,
    ):
        raise _error(
            "ANALYSIS.UPDATED_WITHOUT_CHANGE",
            "updated disposition requires a changed target authority fingerprint",
            observed=obligation.target,
        )
    record = DispositionRecord(
        obligation.id,
        submission.kind,
        submission.result,
        submission.rationale,
        submission.evidence,
        authorization,
        submission.fingerprint,
    )
    return _build_state(
        state.base_snapshot,
        state.proposed_snapshot,
        state.changes,
        state.semantic_proposals,
        state.authorization_view,
        state.provider_view,
        state.observations,
        _replace_disposition(state.dispositions, record),
        state.coverage_decisions,
    )


def _verify_state_authority(
    kernel: AnalysisKernel,
    state: AnalysisState,
) -> None:
    if (
        dict(state.base_snapshot) != dict(kernel.accepted.snapshot)
        or dict(state.proposed_snapshot) != dict(kernel.proposed.snapshot)
        or state.authorization_view.id != kernel.authorization_view.id
        or state.provider_view.id != kernel.provider_view.id
    ):
        raise _error(
            "AUTHORITY.CONTEXT_MISMATCH",
            "analysis state authority inputs do not match the bound kernel",
            observed=state.id,
        )


def _apply_attestations(
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
    decisions: Iterable[CoverageDecision],
    authorization_view: AuthorizationAuthorityView,
) -> tuple[AnalysisAuthority, AnalysisAuthority, tuple[CoverageDecision, ...]]:
    retained = []
    expected = _authorization(authorization_view, "standards.review.audit")
    for decision in sorted(
        decisions,
        key=lambda item: item.attestation.handle,
    ):
        attestation = decision.attestation
        if (
            expected is None
            or decision.authorization.as_contract() != expected.as_contract()
        ):
            continue
        proposed_requirements = {
            item.handle for item in proposed.coverage.requirements.values()
        }
        accepted_requirements = {
            item.handle for item in accepted.coverage.requirements.values()
        }
        try:
            if attestation.requirement in proposed_requirements:
                coverage, _ = certify_coverage(proposed.coverage, attestation)
                proposed = replace(proposed, coverage=coverage)
            elif attestation.requirement in accepted_requirements:
                coverage, _ = certify_coverage(accepted.coverage, attestation)
                accepted = replace(accepted, coverage=coverage)
            else:
                continue
        except AnalysisError:
            continue
        retained.append(decision)
    return accepted, proposed, tuple(retained)


def _valid_observations(
    kernel: AnalysisKernel,
    observations: Iterable[FactObservation],
    context: AnalysisContext,
) -> tuple[FactObservation, ...]:
    requirements = {
        requirement.id: (requirement, fact)
        for fact in kernel.proposed.policy_impact.fact_schema.definitions
        for requirement in (build_fact_requirement(fact, context, ()),)
    }
    retained = []
    for observation in observations:
        selected = requirements.get(str(observation.requirement["id"]))
        if selected is None:
            continue
        requirement, fact = selected
        authorization = _authorization(
            kernel.authorization_view,
            requirement.authorization_capability,
        )
        if authorization is None:
            continue
        try:
            retained.append(
                validate_observation(
                    observation,
                    requirement,
                    fact,
                    authorization,
                    kernel.provider_view.evidence_versions(),
                )
            )
        except AnalysisError:
            continue
    return tuple(sorted(retained, key=lambda item: item.id))


def _valid_dispositions(
    kernel: AnalysisKernel,
    dispositions: Iterable[DispositionRecord],
    reached: Iterable[Obligation],
) -> tuple[DispositionRecord, ...]:
    obligations = {item.id: item for item in reached}
    contracts = kernel.provider_view.evidence_versions()
    retained = []
    for record in dispositions:
        obligation = obligations.get(record.obligation_id)
        if (
            obligation is None
            or record.fingerprint.as_contract() != obligation.fingerprint.as_contract()
        ):
            continue
        capability = {
            "consumer-disposition": "standards.review.consumer",
            "impact-disposition": "standards.review.impact",
        }[record.kind]
        authorization = _authorization(kernel.authorization_view, capability)
        if (
            authorization is None
            or authorization.as_contract() != record.authorization.as_contract()
            or any(
                contracts.get(item.provider_contract) != item.provider_contract_version
                for item in record.evidence
            )
        ):
            continue
        retained.append(record)
    return tuple(sorted(retained, key=lambda item: item.obligation_id))


def _provider_observation(
    kernel: AnalysisKernel,
    requirements: Iterable[FactRequirement],
    observations: Iterable[FactObservation],
) -> FactObservation | None:
    existing = {str(item.requirement["id"]) for item in observations}
    contracts = kernel.provider_view.evidence_versions()
    for requirement in requirements:
        if requirement.id in existing:
            continue
        authorization = _authorization(
            kernel.authorization_view,
            requirement.authorization_capability,
        )
        fact = kernel.proposed.policy_impact.fact_schema.resolve(requirement.fact)
        if authorization is None or fact is None:
            continue
        claims: dict[str, FactObservation] = {}
        for provider in kernel.providers:
            result = provider.observe(
                requirement,
                kernel.accepted.snapshot,
                kernel.proposed.snapshot,
            )
            if isinstance(result, ProviderUnavailable):
                raise _error(
                    "FACT.PROVIDER_UNAVAILABLE",
                    result.reason,
                    outcome="unavailable",
                    observed=provider.id,
                )
            if isinstance(result, NoObservation):
                continue
            if not isinstance(result, ObservationClaim):
                raise _error(
                    "FACT.PROVIDER_RESULT_INVALID",
                    "provider must return a typed deterministic result",
                    observed=provider.id,
                )
            if any(
                item.provider_contract != provider.id
                or item.provider_contract_version != provider.contract_version
                for item in result.evidence
            ):
                raise _error(
                    "FACT.PROVIDER_CLAIM_CONTRACT",
                    "provider claim evidence does not match its contract",
                    observed=provider.id,
                )
            observation = observe_fact(
                requirement,
                fact,
                result.value,
                result.evidence,
                authorization,
                contracts,
            )
            claims[observation.id] = observation
        if len(claims) > 1:
            raise _error(
                "FACT.PROVIDER_CONFLICT",
                "trusted providers returned conflicting observations",
                observed=requirement.id,
            )
        if claims:
            return next(iter(claims.values()))
    return None


def _validate_attestation(
    kernel: AnalysisKernel,
    state: AnalysisState,
    obligation: Obligation,
    attestation: CoverageAttestation,
) -> None:
    proposed_subjects = {
        policy_id for change in state.changes for policy_id in change.proposed_ids
    }
    index = (
        kernel.proposed.coverage
        if obligation.target in proposed_subjects
        else kernel.accepted.coverage
    )
    certify_coverage(index, attestation)


def _build_state(
    base_snapshot: Mapping[str, object],
    proposed_snapshot: Mapping[str, object],
    changes: Iterable[ChangeDescriptor],
    semantic_proposals: Iterable[SemanticProposal],
    authorization_view: AuthorizationAuthorityView,
    provider_view: ProviderAuthorityView,
    observations: Iterable[FactObservation],
    dispositions: Iterable[DispositionRecord],
    coverage_decisions: Iterable[CoverageDecision],
) -> AnalysisState:
    selected_changes = tuple(
        sorted(changes, key=lambda item: canonical_json_bytes(item.as_contract()))
    )
    selected_proposals = tuple(
        sorted(
            semantic_proposals,
            key=lambda item: canonical_json_bytes(_semantic_proposal_contract(item)),
        )
    )
    selected_observations = tuple(sorted(observations, key=lambda item: item.id))
    selected_dispositions = tuple(
        sorted(dispositions, key=lambda item: item.obligation_id)
    )
    selected_coverage = tuple(
        sorted(
            coverage_decisions,
            key=lambda item: item.attestation.handle,
        )
    )
    versions = AnalysisVersions()
    projection = {
        "base_snapshot": dict(base_snapshot),
        "proposed_snapshot": dict(proposed_snapshot),
        "changes": [item.as_contract() for item in selected_changes],
        "semantic_proposals": [
            _semantic_proposal_contract(item) for item in selected_proposals
        ],
        "authorization_view": authorization_view.as_contract(),
        "provider_view": provider_view.as_contract(),
        "fact_observations": [item.as_contract() for item in selected_observations],
        "dispositions": [item.as_contract() for item in selected_dispositions],
        "coverage_decisions": [item.as_contract() for item in selected_coverage],
        "provenance": _state_identity_provenance(versions),
    }
    return AnalysisState(
        identity(ANALYSIS_DOMAIN, "analysis", projection),
        base_snapshot,
        proposed_snapshot,
        selected_changes,
        selected_proposals,
        authorization_view,
        provider_view,
        selected_observations,
        selected_dispositions,
        selected_coverage,
        versions,
    )


def _semantic_proposal_contract(item: SemanticProposal) -> dict[str, object]:
    return {
        "policy": item.policy,
        "accepted_semantic_revision": item.accepted_semantic_revision,
        "proposed_semantic_revision": item.proposed_semantic_revision,
        "intent": item.intent,
        "structural_digest": item.structural_digest,
    }


def _required_mapping(
    value: Mapping[str, object],
    key: str,
) -> dict[str, object]:
    selected = value[key]
    if not isinstance(selected, Mapping):
        raise TypeError(f"{key} must be an object")
    return dict(selected)


def _mapping_value(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{label} must be an object")
    return dict(value)


def _change_from_contract(value: object) -> ChangeDescriptor:
    selected = _mapping_value(value, "change")
    scope_value = _required_mapping(selected, "scope")
    return ChangeDescriptor(
        ChangeKind(str(selected["kind"])),
        tuple(str(item) for item in selected["accepted_ids"]),
        tuple(str(item) for item in selected["proposed_ids"]),
        ReviewScope(
            str(scope_value["kind"]),
            tuple(str(item) for item in scope_value.get("heading_path", ())),
        ),
        None if "accepted_module" not in selected else str(selected["accepted_module"]),
        None if "proposed_module" not in selected else str(selected["proposed_module"]),
    )


def _semantic_proposal_from_contract(value: object) -> SemanticProposal:
    selected = _mapping_value(value, "semantic proposal")
    accepted = selected["accepted_semantic_revision"]
    return SemanticProposal(
        str(selected["policy"]),
        None if accepted is None else int(accepted),
        int(selected["proposed_semantic_revision"]),
        str(selected["intent"]),
        str(selected["structural_digest"]),
    )


def _authorization_from_contract(value: object) -> AuthorizationReference:
    selected = _mapping_value(value, "authorization")
    return AuthorizationReference(
        str(selected["id"]),
        str(selected["capability"]),
        str(selected["digest"]),
    )


def _evidence_from_contract(value: object) -> EvidenceReference:
    selected = _mapping_value(value, "evidence")
    return EvidenceReference(
        str(selected["id"]),
        str(selected["digest"]),
        str(selected["provider_contract"]),
        str(selected["provider_contract_version"]),
    )


def _coverage_evidence_from_contract(value: object) -> CoverageEvidence:
    selected = _mapping_value(value, "coverage evidence")
    return CoverageEvidence(
        str(selected["id"]),
        str(selected["digest"]),
        str(selected["provider_contract"]),
        str(selected["provider_contract_version"]),
    )


def _observation_from_contract(value: object) -> FactObservation:
    selected = _mapping_value(value, "fact observation")
    handle = _required_mapping(selected, "handle")
    return FactObservation(
        str(handle["id"]),
        _required_mapping(selected, "requirement"),
        _required_mapping(selected, "value"),
        tuple(_evidence_from_contract(item) for item in selected["evidence"]),
        _authorization_from_contract(selected["authorization"]),
    )


def _fingerprint_from_contract(value: object) -> DecisionFingerprint:
    selected = _mapping_value(value, "decision fingerprint")
    return DecisionFingerprint(
        str(selected["decision_kind"]),
        str(selected["decision_contract"]),
        tuple(
            DecisionDependency(
                str(item["class"]),
                str(item["identity"]),
                str(item["digest"]),
            )
            for raw in selected["dependencies"]
            for item in (_mapping_value(raw, "decision dependency"),)
        ),
        int(selected["schema_version"]),
    )


def _disposition_from_contract(value: object) -> DispositionRecord:
    selected = _mapping_value(value, "disposition")
    return DispositionRecord(
        str(selected["obligation_id"]),
        str(selected["kind"]),
        str(selected["result"]),
        str(selected["rationale"]),
        tuple(_evidence_from_contract(item) for item in selected["evidence"]),
        _authorization_from_contract(selected["authorization"]),
        _fingerprint_from_contract(selected["fingerprint"]),
    )


def _attestation_from_contract(value: object) -> CoverageAttestation:
    selected = _mapping_value(value, "coverage attestation")
    handle = _required_mapping(selected, "handle")
    requirement = _required_mapping(selected, "requirement")
    return CoverageAttestation(
        str(handle["id"]),
        str(requirement["id"]),
        str(selected["conclusion"]),
        tuple(_coverage_evidence_from_contract(item) for item in selected["evidence"]),
        tuple(
            _coverage_evidence_from_contract(item)
            for item in selected["explicit_exclusions"]
        ),
        str(selected["rationale"]),
        str(selected["auditor_provenance"]),
        int(selected["schema_version"]),
        "analysis-state",
    )


def _coverage_decision_from_contract(value: object) -> CoverageDecision:
    selected = _mapping_value(value, "coverage decision")
    return CoverageDecision(
        _attestation_from_contract(selected["attestation"]),
        _authorization_from_contract(selected["authorization"]),
    )


def _authorization_view_from_contract(
    value: Mapping[str, object],
) -> AuthorizationAuthorityView:
    authorizations = tuple(
        _authorization_from_contract(item) for item in value["authorizations"]
    )
    expected = build_authorization_view(authorizations)
    if value != expected.as_contract():
        raise ValueError("authorization authority view identity mismatch")
    return expected


def _provider_view_from_contract(
    value: Mapping[str, object],
) -> ProviderAuthorityView:
    evidence_contracts = tuple(
        (str(item["id"]), str(item["version"]))
        for raw in value["evidence_contracts"]
        for item in (_mapping_value(raw, "evidence contract"),)
    )
    providers = tuple(
        ProviderContractView(
            str(item["id"]),
            str(item["contract_version"]),
            str(item["input_contract"]),
            tuple(
                _mapping_value(handle, "immutable authority handle")
                for handle in item["immutable_inputs"]
            ),
        )
        for raw in value["providers"]
        for item in (_mapping_value(raw, "provider contract"),)
    )
    projection = {
        "contract_version": PROVIDER_VIEW_CONTRACT,
        "evidence_contracts": [
            {"id": key, "version": version} for key, version in evidence_contracts
        ],
        "providers": [item.as_contract() for item in providers],
    }
    expected_id = identity(
        PROVIDER_VIEW_DOMAIN,
        "provider-authority-view",
        projection,
    )
    result = ProviderAuthorityView(expected_id, evidence_contracts, providers)
    if value != result.as_contract():
        raise ValueError("provider authority view identity mismatch")
    return result


def _state_identity_provenance(
    versions: AnalysisVersions,
) -> dict[str, object]:
    value = versions.as_contract()
    return {
        key: value[key]
        for key in (
            "analysis_contract_version",
            "analysis_schema_version",
            "result_schema_version",
            "applicability_version",
            "metadata_api_version",
            "graph_engine_contract_version",
            "parser_versions",
            "evidence_provider_contract_versions",
            "authorization_contract_version",
        )
    }


def _authorization(
    view: AuthorizationAuthorityView,
    capability: str,
) -> AuthorizationReference | None:
    return next(
        (item for item in view.authorizations if item.capability == capability),
        None,
    )


def _replace_observation(
    observations: Iterable[FactObservation],
    selected: FactObservation,
) -> tuple[FactObservation, ...]:
    result = {str(item.requirement["id"]): item for item in observations}
    previous = result.get(str(selected.requirement["id"]))
    if previous is not None and previous.id != selected.id:
        raise _error(
            "FACT.OBSERVATION_CONFLICT",
            "one requirement cannot have conflicting observations",
            observed=str(selected.requirement["id"]),
        )
    result[str(selected.requirement["id"])] = selected
    return tuple(sorted(result.values(), key=lambda item: item.id))


def _replace_disposition(
    dispositions: Iterable[DispositionRecord],
    selected: DispositionRecord,
) -> tuple[DispositionRecord, ...]:
    result = {item.obligation_id: item for item in dispositions}
    previous = result.get(selected.obligation_id)
    if previous is not None and canonical_json_bytes(
        previous.as_contract()
    ) != canonical_json_bytes(selected.as_contract()):
        raise _error(
            "ANALYSIS.DISPOSITION_CONFLICT",
            "one state cannot contain conflicting dispositions",
            observed=selected.obligation_id,
        )
    result[selected.obligation_id] = selected
    return tuple(result[key] for key in sorted(result))


def _exact_requirement(
    result: PendingResult,
    requirement_id: str,
) -> FactRequirement:
    selected = tuple(
        item for item in result.fact_requirements if item.id == requirement_id
    )
    if len(selected) != 1:
        raise _error(
            "SUBMISSION.NOT_APPLICABLE",
            "submission does not identify current fact work",
            observed=requirement_id,
        )
    return selected[0]


def _exact_obligation(result: PendingResult, obligation_id: str) -> Obligation:
    selected = tuple(item for item in result.obligations if item.id == obligation_id)
    if len(selected) != 1:
        raise _error(
            "SUBMISSION.NOT_APPLICABLE",
            "submission does not identify current review work",
            observed=obligation_id,
        )
    return selected[0]


def _reading_plan(
    obligations: tuple[Obligation, ...],
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
) -> tuple[ReadingPlanEntry, ...]:
    def authority(target: str) -> str:
        try:
            return canonical_target_authority(target, proposed.corpus, proposed.graph)
        except AnalysisError:
            return canonical_target_authority(target, accepted.corpus, accepted.graph)

    return compile_reading_plan(
        consumer_reading_selections(obligations),
        authority,
    )


def _available_certificates(
    changes: Iterable[ClassifiedChange],
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
) -> tuple[ConsumerCoverageCertificate, ...]:
    selected: dict[str, ConsumerCoverageCertificate] = {}
    for change in changes:
        index = (
            proposed.coverage if change.descriptor.proposed_ids else accepted.coverage
        )
        for subject in change.descriptor.proposed_ids or change.descriptor.accepted_ids:
            certificate = index.certificate_for(subject)
            if certificate is not None:
                selected[subject] = certificate
    return tuple(selected[key] for key in sorted(selected))


def _relevant_certificates(
    changes: Iterable[ClassifiedChange],
    accepted: AnalysisAuthority,
    proposed: AnalysisAuthority,
) -> tuple[ConsumerCoverageCertificate, ...]:
    selected = _available_certificates(changes, accepted, proposed)
    subjects = {
        policy_id
        for change in changes
        for policy_id in (
            change.descriptor.proposed_ids or change.descriptor.accepted_ids
        )
    }
    if {item.subject for item in selected} != subjects:
        missing = sorted(subjects - {item.subject for item in selected})
        raise _error(
            "COVERAGE.SUBJECT_UNAUDITED",
            "completed analysis requires current coverage certificates",
            outcome="incomplete",
            observed=missing[0],
        )
    return selected


def _target_changed(
    accepted: CoverageIndex,
    proposed: CoverageIndex,
    target: str,
) -> bool:
    before = next(
        (item.fingerprint for item in accepted.horizon.members if item.id == target),
        None,
    )
    after = next(
        (item.fingerprint for item in proposed.horizon.members if item.id == target),
        None,
    )
    return before != after


__all__ = (
    "ANALYSIS_DOMAIN",
    "AnalysisAuthority",
    "AnalysisInput",
    "AnalysisKernel",
    "AnalysisState",
    "AuthorizationAuthorityView",
    "ProviderAuthorityView",
    "advance_analysis",
    "analysis_state_from_contract",
    "bind_analysis_kernel",
    "bind_projection_kernel",
    "build_authorization_view",
    "build_provider_view",
    "prepare_analysis",
    "project_analysis",
)
