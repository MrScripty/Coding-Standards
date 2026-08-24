from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping, Protocol

from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    ApplicabilityProgram,
    FactContract,
    FactSchema,
    index_programs,
)

from .changes import ClassifiedChange, SemanticProposal
from .errors import AnalysisError, AnalysisFailure
from .impact import ImpactSelection
from .serialization import canonical_json_bytes, identity


CONTEXT_DOMAIN = "coding-standards:analysis-context:v1"
REQUIREMENT_DOMAIN = "coding-standards:fact-requirement:v1"
OBSERVATION_DOMAIN = "coding-standards:fact-observation:v1"
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
EVIDENCE_CONTRACT = "evidence-reference.v1"


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
class EvidenceReference:
    id: str
    digest: str
    provider_contract: str
    provider_contract_version: str

    def __post_init__(self) -> None:
        if (
            not self.id
            or not self.provider_contract
            or not self.provider_contract_version
            or DIGEST_PATTERN.fullmatch(self.digest) is None
        ):
            raise _error(
                "FACT.EVIDENCE",
                "evidence requires an ID, provider contract, and SHA-256 digest",
                observed=self.id,
            )

    def as_contract(self) -> dict[str, str]:
        return {
            "id": self.id,
            "digest": self.digest,
            "provider_contract": self.provider_contract,
            "provider_contract_version": self.provider_contract_version,
        }


@dataclass(frozen=True, slots=True)
class AuthorizationReference:
    id: str
    capability: str
    digest: str

    def __post_init__(self) -> None:
        if (
            not self.id
            or not self.capability
            or DIGEST_PATTERN.fullmatch(self.digest) is None
        ):
            raise _error(
                "FACT.AUTHORIZATION",
                "authorization requires an ID, capability, and SHA-256 digest",
                observed=self.id,
            )

    def as_contract(self) -> dict[str, str]:
        return {
            "id": self.id,
            "capability": self.capability,
            "digest": self.digest,
        }


@dataclass(frozen=True, slots=True)
class AnalysisContext:
    id: str
    subjects: tuple[Mapping[str, object], ...]
    semantic_proposals: tuple[Mapping[str, object], ...]
    kind: str = "standards-change"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "subjects", tuple(_freeze(item) for item in self.subjects)
        )
        object.__setattr__(
            self,
            "semantic_proposals",
            tuple(_freeze(item) for item in self.semantic_proposals),
        )

    @property
    def handle(self) -> dict[str, object]:
        return {
            "kind": "analysis-context-handle",
            "id": self.id,
            "context_kind": self.kind,
            "schema_version": 1,
        }

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "analysis-context",
            "handle": self.handle,
            "subjects": [_thaw(item) for item in self.subjects],
            "semantic_proposals": [_thaw(item) for item in self.semantic_proposals],
        }


def build_analysis_context(
    changes: Iterable[ClassifiedChange],
    semantic_proposals: Iterable[SemanticProposal] = (),
) -> AnalysisContext:
    subjects = tuple(
        sorted(
            (unit.as_contract() for change in changes for unit in change.changed_units),
            key=canonical_json_bytes,
        )
    )
    if not subjects:
        raise _error(
            "FACT.CONTEXT_EMPTY",
            "a standards-change context requires changed policy subjects",
        )
    proposals = tuple(
        sorted(
            (
                {
                    "policy": item.policy,
                    "accepted_semantic_revision": item.accepted_semantic_revision,
                    "proposed_semantic_revision": item.proposed_semantic_revision,
                    "intent": item.intent,
                    "structural_digest": item.structural_digest,
                }
                for item in semantic_proposals
            ),
            key=canonical_json_bytes,
        )
    )
    projection = {
        "handle": {"context_kind": "standards-change"},
        "subjects": list(subjects),
        "semantic_proposals": list(proposals),
    }
    return AnalysisContext(
        identity(CONTEXT_DOMAIN, "standards-change", projection),
        subjects,
        proposals,
    )


@dataclass(frozen=True, slots=True)
class FactRequirement:
    id: str
    fact: str
    fact_semantic_revision: int
    fact_contract_digest: str
    context: Mapping[str, object]
    value_contract: Mapping[str, object]
    answer_contract: str
    evidence_contract: str
    authorization_capability: str
    prompt: str
    dependent_programs: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "context", _freeze(self.context))
        object.__setattr__(self, "value_contract", _freeze(self.value_contract))
        object.__setattr__(
            self,
            "dependent_programs",
            tuple(sorted(set(self.dependent_programs))),
        )

    @property
    def handle(self) -> dict[str, object]:
        return {
            "kind": "fact-requirement-handle",
            "id": self.id,
            "schema_version": 1,
        }

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "fact-requirement",
            "handle": self.handle,
            "fact": self.fact,
            "fact_semantic_revision": self.fact_semantic_revision,
            "fact_contract_digest": self.fact_contract_digest,
            "context": _thaw(self.context),
            "value_contract": _thaw(self.value_contract),
            "answer_contract": self.answer_contract,
            "evidence_contract": self.evidence_contract,
            "authorization_capability": self.authorization_capability,
            "prompt": self.prompt,
            "dependent_programs": list(self.dependent_programs),
        }


def _value_contract(fact: FactContract) -> dict[str, object]:
    value: dict[str, object] = {
        "type": fact.type,
        "states": ["known", "known-absent"],
        "nullable": fact.nullable,
    }
    if fact.values:
        value["values"] = list(fact.values)
    return value


def build_fact_requirement(
    fact: FactContract,
    context: AnalysisContext,
    dependent_programs: Iterable[str],
) -> FactRequirement:
    if fact.context_kind != context.kind:
        raise _error(
            "FACT.CONTEXT_KIND",
            "fact contract does not apply to this analysis context",
            observed=fact.id,
        )
    dependents = tuple(sorted(set(dependent_programs)))
    value_contract = _value_contract(fact)
    projection = {
        "fact": fact.id,
        "fact_semantic_revision": fact.semantic_revision,
        "fact_contract_digest": fact.digest,
        "context": context.handle,
        "value_contract": value_contract,
        "answer_contract": fact.answer_contract,
        "evidence_contract": fact.evidence_contract,
        "authorization_capability": fact.authorization_capability,
    }
    return FactRequirement(
        identity(REQUIREMENT_DOMAIN, "fact-requirement", projection),
        fact.id,
        fact.semantic_revision,
        fact.digest,
        context.handle,
        value_contract,
        fact.answer_contract,
        fact.evidence_contract,
        fact.authorization_capability,
        fact.prompt,
        dependents,
    )


def generate_fact_requirements(
    selections: Iterable[ImpactSelection],
    context: AnalysisContext,
    fact_schema: FactSchema,
) -> tuple[FactRequirement, ...]:
    programs: dict[str, ApplicabilityProgram] = {}
    unresolved: set[str] = set()
    for selection in selections:
        for candidate in selection.candidates:
            if not candidate.unresolved_facts:
                continue
            unresolved.update(candidate.unresolved_facts)
            for trace in candidate.traces:
                semantics = trace.policy_semantics
                if semantics is None or trace.applicability != "unknown":
                    continue
                programs[f"{trace.graph}:{candidate.edge_id}"] = (
                    semantics.applicability_program
                )
    index = index_programs(programs)
    requirements = []
    for fact_id in sorted(unresolved):
        fact = fact_schema.resolve(fact_id)
        if fact is None or fact.id != fact_id:
            raise _error(
                "FACT.CONTRACT_UNAVAILABLE",
                "unresolved fact has no canonical semantic contract",
                outcome="unavailable",
                observed=fact_id,
            )
        requirements.append(
            build_fact_requirement(fact, context, index.dependents(fact_id))
        )
    return tuple(requirements)


@dataclass(frozen=True, slots=True)
class FactObservation:
    id: str
    requirement: Mapping[str, object]
    value: Mapping[str, object]
    evidence: tuple[EvidenceReference, ...]
    authorization: AuthorizationReference

    def __post_init__(self) -> None:
        object.__setattr__(self, "requirement", _freeze(self.requirement))
        object.__setattr__(self, "value", _freeze(self.value))

    @property
    def handle(self) -> dict[str, object]:
        return {
            "kind": "fact-observation-handle",
            "id": self.id,
            "schema_version": 1,
        }

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "fact-observation",
            "handle": self.handle,
            "requirement": _thaw(self.requirement),
            "value": _thaw(self.value),
            "evidence": [item.as_contract() for item in self.evidence],
            "authorization": self.authorization.as_contract(),
        }


@dataclass(frozen=True, slots=True)
class ObservationClaim:
    value: Mapping[str, object]
    evidence: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _freeze(self.value))


@dataclass(frozen=True, slots=True)
class NoObservation:
    """A deterministic provider result that supplies no fact value."""


@dataclass(frozen=True, slots=True)
class ProviderUnavailable:
    reason: str

    def __post_init__(self) -> None:
        if not self.reason:
            raise _error(
                "FACT.PROVIDER_UNAVAILABLE_REASON",
                "provider unavailability requires a reason",
            )


class FactObservationProvider(Protocol):
    id: str
    contract_version: str
    input_contract: str
    immutable_inputs: tuple[Mapping[str, object], ...]

    def observe(
        self,
        requirement: FactRequirement,
        accepted_snapshot: Mapping[str, object],
        proposed_snapshot: Mapping[str, object],
    ) -> ObservationClaim | NoObservation | ProviderUnavailable: ...


def observe_fact(
    requirement: FactRequirement,
    fact: FactContract,
    value: Mapping[str, object],
    evidence: Iterable[EvidenceReference],
    authorization: AuthorizationReference,
    evidence_provider_contracts: Mapping[str, str],
) -> FactObservation:
    if fact.id != requirement.fact or fact.digest != requirement.fact_contract_digest:
        raise _error(
            "FACT.CONTRACT_STALE",
            "fact requirement does not match the supplied fact contract",
            outcome="stale",
            observed=requirement.id,
        )
    if authorization.capability != requirement.authorization_capability:
        raise _error(
            "FACT.AUTHORIZATION_CAPABILITY",
            "authorization does not grant the fact contract capability",
            outcome="unauthorized",
            observed=authorization.capability,
        )
    if requirement.evidence_contract != EVIDENCE_CONTRACT:
        raise _error(
            "FACT.EVIDENCE_CONTRACT_UNSUPPORTED",
            "fact requirement uses an unsupported evidence contract",
            outcome="unsupported",
            observed=requirement.evidence_contract,
        )
    selected_evidence = tuple(evidence)
    if not selected_evidence:
        raise _error("FACT.EVIDENCE_REQUIRED", "fact observations require evidence")
    if len({item.id for item in selected_evidence}) != len(selected_evidence):
        raise _error("FACT.EVIDENCE_DUPLICATE", "fact evidence IDs must be unique")
    unavailable = sorted(
        item.provider_contract
        for item in selected_evidence
        if evidence_provider_contracts.get(item.provider_contract)
        != item.provider_contract_version
    )
    if unavailable:
        raise _error(
            "FACT.EVIDENCE_PROVIDER_UNAVAILABLE",
            "fact evidence uses an unregistered provider contract version",
            outcome="unavailable",
            observed=unavailable[0],
        )
    try:
        bound = fact.bind(value).as_contract()
    except ApplicabilityError as error:
        failure = error.failure
        raise _error(
            "FACT.VALUE_INVALID",
            failure.message,
            outcome=failure.outcome,
            observed=failure.observed,
        ) from error
    projection = {
        "requirement": requirement.handle,
        "value": bound,
        "evidence": [item.as_contract() for item in selected_evidence],
        "authorization": authorization.as_contract(),
    }
    return FactObservation(
        identity(OBSERVATION_DOMAIN, "fact-observation", projection),
        requirement.handle,
        bound,
        selected_evidence,
        authorization,
    )


def validate_observation(
    observation: FactObservation,
    requirement: FactRequirement,
    fact: FactContract,
    authorization: AuthorizationReference,
    evidence_provider_contracts: Mapping[str, str],
) -> FactObservation:
    if dict(observation.requirement) != requirement.handle:
        raise _error(
            "FACT.OBSERVATION_STALE",
            "observation does not bind the exact derived requirement",
            outcome="stale",
            observed=observation.id,
        )
    if observation.authorization.as_contract() != authorization.as_contract():
        raise _error(
            "FACT.AUTHORIZATION_STALE",
            "observation authorization is no longer current",
            outcome="stale",
            observed=observation.authorization.id,
        )
    rebuilt = observe_fact(
        requirement,
        fact,
        observation.value,
        observation.evidence,
        authorization,
        evidence_provider_contracts,
    )
    if rebuilt.id != observation.id:
        raise _error(
            "FACT.OBSERVATION_IDENTITY",
            "observation identity does not match its canonical content",
            outcome="invalid",
            observed=observation.id,
        )
    return observation


@dataclass(frozen=True, slots=True)
class FactResolution:
    reused: tuple[FactObservation, ...]
    unresolved: tuple[FactRequirement, ...]


def resolve_fact_requirements(
    requirements: Iterable[FactRequirement],
    observations: Iterable[FactObservation],
) -> FactResolution:
    selected_requirements = tuple(sorted(requirements, key=lambda item: item.id))
    if len({item.id for item in selected_requirements}) != len(selected_requirements):
        raise _error("FACT.REQUIREMENT_DUPLICATE", "fact requirements must be unique")
    by_requirement: dict[str, FactObservation] = {}
    for observation in observations:
        requirement_id = str(observation.requirement.get("id", ""))
        previous = by_requirement.get(requirement_id)
        if previous is not None and previous.id != observation.id:
            raise _error(
                "FACT.OBSERVATION_CONFLICT",
                "one requirement has conflicting observations",
                observed=requirement_id,
            )
        by_requirement[requirement_id] = observation
    reused = []
    unresolved = []
    for requirement in selected_requirements:
        observation = by_requirement.get(requirement.id)
        if observation is None:
            unresolved.append(requirement)
        elif dict(observation.requirement) != requirement.handle:
            raise _error(
                "FACT.OBSERVATION_STALE",
                "observation requirement handle is stale or malformed",
                outcome="stale",
                observed=requirement.id,
            )
        else:
            reused.append(observation)
    return FactResolution(tuple(reused), tuple(unresolved))


__all__ = (
    "AnalysisContext",
    "AuthorizationReference",
    "CONTEXT_DOMAIN",
    "EvidenceReference",
    "FactObservation",
    "FactObservationProvider",
    "FactRequirement",
    "FactResolution",
    "OBSERVATION_DOMAIN",
    "NoObservation",
    "ObservationClaim",
    "ProviderUnavailable",
    "REQUIREMENT_DOMAIN",
    "build_analysis_context",
    "build_fact_requirement",
    "generate_fact_requirements",
    "observe_fact",
    "resolve_fact_requirements",
    "validate_observation",
)
