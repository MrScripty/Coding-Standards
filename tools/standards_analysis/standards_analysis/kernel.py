from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Mapping

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_applicability.standards_applicability import FactContract
from tools.standards_authority.standards_authority import (
    AuthorityBoundValue,
    AuthorityReference,
    AuthorityRepository,
    ExecutionAuthorityRoot,
)
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
)
from tools.standards_metadata.standards_metadata import CanonicalStandardsCorpus
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
)

from .authority import (
    ANALYSIS_CONTEXT_CODEC,
    FACT_REQUIREMENT_CODEC,
    AnalysisContextAuthority,
    FactObservationAuthority,
    FactRequirementAuthority,
)
from .changes import (
    ChangeDescriptor,
    ClassifiedChange,
    SemanticProposal,
    classify_changes,
)
from .coverage_authority import (
    CoverageAuthorityIndex,
    StoredCoverageAttestation,
    publish_coverage_certificate,
)
from .errors import AnalysisError, AnalysisFailure
from .impact import ImpactSelection, select_impact
from .obligations import (
    COVERAGE_DECISION_CONTRACT,
    OBLIGATION_DOMAIN,
    DecisionDependency,
    DecisionFingerprint,
    Obligation,
    generate_consumer_review_obligations,
    generate_unmapped_normative_obligations,
)
from .reading import (
    ReadingPlanEntry,
    canonical_target_authority,
    compile_reading_plan,
    consumer_reading_selections,
)
from .keys import analysis_identity, analysis_key_bytes, raw_digest


@dataclass(frozen=True, slots=True)
class AnalysisMaterial:
    root: Path
    metadata: AuthorityReference
    graph_authority: AuthorityReference
    policy_impact_authority: AuthorityReference
    coverage_authority: AuthorityReference
    corpus: CanonicalStandardsCorpus
    graph: EdgeRegistry
    policy_impact: CompiledPolicyImpactSet
    coverage: CoverageAuthorityIndex

    def authority_bound(self, side: str) -> AuthorityBoundValue[object]:
        return AuthorityBoundValue(
            self,
            (
                ExecutionAuthorityRoot(side, "metadata", self.metadata),
                ExecutionAuthorityRoot(side, "graph", self.graph_authority),
                ExecutionAuthorityRoot(
                    side, "policy-impact", self.policy_impact_authority
                ),
                ExecutionAuthorityRoot(side, "coverage", self.coverage_authority),
            ),
        )


@dataclass(frozen=True, slots=True)
class StoredObservation:
    reference: AuthorityReference
    value: FactObservationAuthority


@dataclass(frozen=True, slots=True)
class MaterialRequirement:
    reference: AuthorityReference
    value: FactRequirementAuthority
    fact: FactContract
    prompt: str
    dependent_programs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CoverageProjection:
    subject: str
    view: AuthorityReference
    requirement: AuthorityReference
    certificate: AuthorityReference | None


@dataclass(frozen=True, slots=True)
class AnalysisEvaluation:
    context: AuthorityReference
    context_value: AnalysisContextAuthority
    changes: tuple[ClassifiedChange, ...]
    requirements: tuple[MaterialRequirement, ...]
    pending_requirements: tuple[MaterialRequirement, ...]
    obligations: tuple[Obligation, ...]
    reached_obligations: tuple[Obligation, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    coverage: tuple[CoverageProjection, ...]
    observations: tuple[StoredObservation, ...]
    dispositions: tuple[Mapping[str, object], ...]
    attestations: tuple[StoredCoverageAttestation, ...]

    @property
    def complete(self) -> bool:
        return not self.pending_requirements and all(
            item.state == "resolved" for item in self.obligations
        )

    def authority_bound(self) -> AuthorityBoundValue[object]:
        roots = {
            ExecutionAuthorityRoot("current", "context", self.context),
            *(
                ExecutionAuthorityRoot("current", "requirement", item.reference)
                for item in self.requirements
            ),
            *(
                ExecutionAuthorityRoot("current", "observation", item.reference)
                for item in self.observations
            ),
            *(
                ExecutionAuthorityRoot("current", "coverage-view", item.view)
                for item in self.coverage
            ),
            *(
                ExecutionAuthorityRoot(
                    "current", "coverage-requirement", item.requirement
                )
                for item in self.coverage
            ),
            *(
                ExecutionAuthorityRoot(
                    "current", "coverage-certificate", item.certificate
                )
                for item in self.coverage
                if item.certificate is not None
            ),
            *(
                ExecutionAuthorityRoot(
                    "current", "coverage-attestation", item.reference
                )
                for item in self.attestations
            ),
        }
        for item in self.observations:
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
        for item in self.attestations:
            roots.add(
                ExecutionAuthorityRoot(
                    "current", "authorization-grant", item.value.authorization
                )
            )
        for disposition in self.dispositions:
            authorization = disposition.get("authorization")
            if isinstance(authorization, Mapping):
                roots.add(
                    ExecutionAuthorityRoot(
                        "current",
                        "authorization-grant",
                        AuthorityReference(
                            str(authorization["object_kind"]),
                            str(authorization["id"]),
                        ),
                    )
                )
        return AuthorityBoundValue(self, tuple(sorted(roots)))


def evaluate_analysis(
    repository: AuthorityRepository,
    accepted: AnalysisMaterial,
    proposed: AnalysisMaterial,
    descriptors: Iterable[ChangeDescriptor],
    semantic_proposals: Iterable[SemanticProposal],
    observations: Iterable[StoredObservation] = (),
    dispositions: Iterable[Mapping[str, object]] = (),
    attestations: Iterable[StoredCoverageAttestation] = (),
) -> AnalysisEvaluation:
    selected_descriptors = tuple(
        sorted(descriptors, key=lambda item: analysis_key_bytes(item.as_contract()))
    )
    selected_proposals = tuple(
        sorted(semantic_proposals, key=lambda item: analysis_key_bytes(_proposal(item)))
    )
    changes = classify_changes(
        accepted.corpus.policy_unit_corpus,
        proposed.corpus.policy_unit_corpus,
        selected_descriptors,
        selected_proposals,
    )
    context_value = AnalysisContextAuthority(
        proposed.metadata,
        _identity(
            {
                "subjects": sorted(
                    (
                        unit.as_contract()
                        for change in changes
                        for unit in change.changed_units
                    ),
                    key=analysis_key_bytes,
                ),
                "changes": [item.as_contract() for item in selected_descriptors],
                "semantic_proposals": [_proposal(item) for item in selected_proposals],
            }
        ),
    )
    context_handle = repository.publish(ANALYSIS_CONTEXT_CODEC, context_value)

    if accepted.policy_impact.fact_schema.digest != proposed.policy_impact.fact_schema.digest:
        raise _error(
            "FACT_SCHEMA_EVOLUTION_UNSUPPORTED",
            "accepted and proposed fact schemas differ",
            outcome="unsupported",
        )

    current_observations = {
        item.value.requirement: item
        for item in observations
        if item.value.requirement.object_kind == "fact-requirement"
    }
    raw_facts: dict[str, object] = {}
    applied: set[AuthorityReference] = set()
    requirements: tuple[MaterialRequirement, ...] = ()
    selections: tuple[ImpactSelection, ...] = ()
    while True:
        fact_set = proposed.policy_impact.fact_schema.bind(raw_facts)
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
        requirements = _requirements(
            repository,
            context_handle.reference,
            proposed.policy_impact_authority,
            proposed.policy_impact,
            selections,
        )
        newly_applied = False
        for requirement in requirements:
            observation = current_observations.get(requirement.reference)
            if observation is None or requirement.reference in applied:
                continue
            raw_facts[requirement.fact.id] = _wire(observation.value.projection)["value"]
            applied.add(requirement.reference)
            newly_applied = True
            break
        if not newly_applied:
            break

    pending = tuple(item for item in requirements if item.reference not in applied)
    material_refs = applied | {item.reference for item in pending}
    material_requirements = tuple(
        item for item in requirements if item.reference in material_refs
    )
    valid_requirement_refs = {
        _requirement(
            repository,
            context_handle.reference,
            proposed.policy_impact_authority,
            fact,
            (),
        ).reference
        for fact in proposed.policy_impact.fact_schema.definitions
    }
    retained_observations = tuple(
        sorted(
            (
                item
                for item in current_observations.values()
                if item.value.requirement in valid_requirement_refs
            ),
            key=lambda item: item.reference,
        )
    )

    coverage, retained_attestations = _coverage(
        repository,
        accepted,
        proposed,
        changes,
        attestations,
    )
    covered_subjects = {
        item.subject for item in coverage if item.certificate is not None
    }
    reached = tuple(
        sorted(
            {
                item.id: item
                for item in (
                    *generate_consumer_review_obligations(selections),
                    *_coverage_obligations(changes, coverage, accepted, proposed),
                    *generate_unmapped_normative_obligations(
                        accepted.root,
                        accepted.corpus,
                        proposed.root,
                        proposed.corpus,
                        changes,
                    ),
                )
                if not (item.kind == "audit-coverage" and item.target in covered_subjects)
            }.values(),
            key=lambda item: item.id,
        )
    )
    valid_dispositions = _valid_dispositions(dispositions, reached)
    records = {str(item["obligation_id"]): item for item in valid_dispositions}
    current = tuple(
        replace(
            obligation,
            state=(
                "blocked"
                if records.get(obligation.id, {}).get("result") == "blocked"
                else "resolved"
                if obligation.id in records
                else "required"
            ),
        )
        for obligation in reached
    )
    reading_plan = _reading_plan(reached, accepted, proposed)
    return AnalysisEvaluation(
        context_handle.reference,
        context_value,
        changes,
        material_requirements,
        pending,
        current,
        reached,
        reading_plan,
        coverage,
        retained_observations,
        valid_dispositions,
        retained_attestations,
    )


def _requirements(
    repository: AuthorityRepository,
    context: AuthorityReference,
    policy_impact: AuthorityReference,
    compiled: CompiledPolicyImpactSet,
    selections: Iterable[ImpactSelection],
) -> tuple[MaterialRequirement, ...]:
    programs: dict[str, set[str]] = {}
    for selection in selections:
        for candidate in selection.candidates:
            for fact in candidate.unresolved_facts:
                programs.setdefault(fact, set()).update(
                    f"{trace.graph}:{candidate.edge_id}"
                    for trace in candidate.traces
                    if trace.applicability == "unknown"
                )
    result = []
    for fact_id in sorted(programs):
        fact = compiled.fact_schema.resolve(fact_id)
        if fact is None or fact.id != fact_id:
            raise _error(
                "FACT.CONTRACT_UNAVAILABLE",
                "unresolved fact has no canonical semantic contract",
                outcome="unavailable",
            )
        result.append(
            _requirement(
                repository,
                context,
                policy_impact,
                fact,
                programs[fact_id],
            )
        )
    return tuple(result)


def _requirement(
    repository: AuthorityRepository,
    context: AuthorityReference,
    policy_impact: AuthorityReference,
    fact: FactContract,
    dependent_programs: Iterable[str],
) -> MaterialRequirement:
    value_contract: dict[str, object] = {
        "type": fact.type,
        "states": ["known", "known-absent"],
        "nullable": fact.nullable,
    }
    if fact.values:
        value_contract["values"] = list(fact.values)
    value = FactRequirementAuthority(
        context,
        policy_impact,
        _identity(
            {
                "fact": fact.id,
                "fact_semantic_revision": fact.semantic_revision,
                "fact_contract_digest": fact.digest,
                "value_contract": value_contract,
                "answer_contract": fact.answer_contract,
                "evidence_contract": fact.evidence_contract,
                "authorization_capability": fact.authorization_capability,
            }
        ),
    )
    handle = repository.publish(FACT_REQUIREMENT_CODEC, value)
    return MaterialRequirement(
        handle.reference,
        value,
        fact,
        fact.prompt,
        tuple(sorted(set(dependent_programs))),
    )


def _coverage(
    repository: AuthorityRepository,
    accepted: AnalysisMaterial,
    proposed: AnalysisMaterial,
    changes: Iterable[ClassifiedChange],
    attestations: Iterable[StoredCoverageAttestation],
) -> tuple[tuple[CoverageProjection, ...], tuple[StoredCoverageAttestation, ...]]:
    supplied = tuple(attestations)
    results: dict[str, CoverageProjection] = {}
    retained: dict[AuthorityReference, StoredCoverageAttestation] = {}
    for change in changes:
        material = proposed if change.descriptor.proposed_ids else accepted
        subjects = change.descriptor.proposed_ids or change.descriptor.accepted_ids
        for subject in subjects:
            published = material.coverage.subjects.get(subject)
            if published is None:
                raise _error(
                    "COVERAGE.SUBJECT_UNAVAILABLE",
                    "changed policy has no current coverage requirement",
                    outcome="unavailable",
                )
            candidates = {
                item.reference: item
                for item in (
                    *supplied,
                    *((published.attestation,) if published.attestation is not None else ()),
                )
                if item.value.requirement == published.requirement
            }
            matching = tuple(candidates.values())
            if len(matching) > 1:
                raise _error(
                    "COVERAGE.DUPLICATE_ATTESTATION",
                    "one coverage requirement has conflicting attestations",
                )
            certificate_ref = published.certificate
            if matching:
                selected = matching[0]
                if published.attestation is None or selected.reference != published.attestation.reference:
                    certificate_ref = publish_coverage_certificate(
                        repository, published, selected
                    )
                retained[selected.reference] = selected
            results[subject] = CoverageProjection(
                subject,
                published.view,
                published.requirement,
                certificate_ref,
            )
    return (
        tuple(results[key] for key in sorted(results)),
        tuple(retained[key] for key in sorted(retained)),
    )


def _coverage_obligations(
    changes: Iterable[ClassifiedChange],
    coverage: Iterable[CoverageProjection],
    accepted: AnalysisMaterial,
    proposed: AnalysisMaterial,
) -> tuple[Obligation, ...]:
    by_subject = {item.subject: item for item in coverage}
    scopes = {
        subject: change.descriptor.scope
        for change in changes
        for subject in (change.descriptor.proposed_ids or change.descriptor.accepted_ids)
    }
    obligations = []
    for subject in sorted(by_subject):
        item = by_subject[subject]
        if item.certificate is not None:
            continue
        material = proposed if subject in proposed.coverage.views else accepted
        view = material.coverage.views[subject]
        dependencies = (
            DecisionDependency(
                "audit",
                item.requirement.semantic_id,
                raw_digest(analysis_key_bytes(_reference(item.requirement))),
            ),
            DecisionDependency(
                "policy-unit",
                subject,
                raw_digest(
                    analysis_key_bytes(
                        {
                            "coverage_view": item.view.semantic_id,
                            "semantic_revision": view.semantic_revision,
                            "representation_digest": view.representation_digest,
                            "structural_digest": view.structural_digest,
                        }
                    )
                ),
            ),
            DecisionDependency(
                "provider-contract",
                COVERAGE_DECISION_CONTRACT.id,
                raw_digest(
                    analysis_key_bytes(COVERAGE_DECISION_CONTRACT.as_contract())
                ),
            ),
        )
        fingerprint = DecisionFingerprint(
            "audit-coverage", COVERAGE_DECISION_CONTRACT.id, dependencies
        )
        reason = {"kind": "audit-coverage", "source": subject}
        identifying = {
            "kind": "audit-coverage",
            "target": subject,
            "scope": scopes[subject].as_contract(),
            "reasons": [reason],
            "fingerprint": fingerprint.as_contract(),
        }
        obligations.append(
            Obligation(
                analysis_identity(
                    OBLIGATION_DOMAIN,
                    "obligation",
                    identifying,
                ),
                "audit-coverage",
                subject,
                scopes[subject],
                (reason,),
                "required",
                ("coverage-attestation",),
                fingerprint,
            )
        )
    return tuple(obligations)


def _valid_dispositions(
    dispositions: Iterable[Mapping[str, object]],
    reached: Iterable[Obligation],
) -> tuple[Mapping[str, object], ...]:
    obligations = {item.id: item for item in reached}
    retained: dict[str, Mapping[str, object]] = {}
    for raw in dispositions:
        item = dict(raw)
        obligation_id = str(item.get("obligation_id", ""))
        obligation = obligations.get(obligation_id)
        if obligation is None:
            continue
        if item.get("fingerprint") != obligation.fingerprint.as_contract():
            continue
        retained[obligation_id] = MappingProxyType(item)
    return tuple(retained[key] for key in sorted(retained))


def _reading_plan(
    obligations: tuple[Obligation, ...],
    accepted: AnalysisMaterial,
    proposed: AnalysisMaterial,
) -> tuple[ReadingPlanEntry, ...]:
    def authority(target: str) -> str:
        try:
            return canonical_target_authority(target, proposed.corpus, proposed.graph)
        except AnalysisError:
            return canonical_target_authority(target, accepted.corpus, accepted.graph)

    return compile_reading_plan(consumer_reading_selections(obligations), authority)


def _proposal(value: SemanticProposal) -> dict[str, object]:
    return {
        "policy": value.policy,
        "accepted_semantic_revision": value.accepted_semantic_revision,
        "proposed_semantic_revision": value.proposed_semantic_revision,
        "intent": value.intent,
        "structural_digest": value.structural_digest,
    }


def _reference(value: AuthorityReference) -> dict[str, str]:
    return {"object_kind": value.object_kind, "id": value.semantic_id}


def _identity(value: object) -> IdentityObject:
    selected = _identity_value(value)
    if not isinstance(selected, IdentityObject):
        raise TypeError("analysis authority projection must be an object")
    return selected


def _identity_value(value: object) -> IdentityValue:
    if value is None or type(value) in {bool, int, str}:
        return value  # type: ignore[return-value]
    if isinstance(value, (list, tuple)):
        return IdentityArray(_identity_value(item) for item in value)
    if isinstance(value, Mapping):
        if any(type(key) is not str for key in value):
            raise TypeError("analysis mapping keys must be strings")
        return IdentityObject(
            (key, _identity_value(value[key])) for key in sorted(value)
        )
    raise TypeError(f"unsupported analysis identity value {type(value)!r}")


def _wire(value: IdentityValue) -> object:
    if type(value) is IdentityArray:
        return [_wire(item) for item in value.values]
    if type(value) is IdentityObject:
        return {key: _wire(item) for key, item in value.members}
    return value


def _error(code: str, message: str, *, outcome: str = "invalid") -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, outcome, message))


__all__ = (
    "AnalysisEvaluation",
    "AnalysisMaterial",
    "CoverageProjection",
    "MaterialRequirement",
    "StoredObservation",
    "evaluate_analysis",
)
