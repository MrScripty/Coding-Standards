from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Iterable, Mapping

from tools.graph_engine.graph_engine import EdgeRegistry
from tools.standards_applicability.standards_applicability import FactContract
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    ContentSource,
)
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
    CoverageDefinitionIndex,
    CoverageRequirementDefinition,
    CoverageViewDefinition,
    coverage_requirement_projection,
)
from .errors import AnalysisError, AnalysisFailure
from .impact import ImpactSelection, select_impact
from .keys import (
    analysis_identity,
    analysis_key_bytes,
    analysis_value_digest,
    raw_digest,
)
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
from .state import (
    AnalysisState,
    ProposedMaterialRef,
    SnapshotMaterialRef,
    child_id,
    plain_record,
)


@dataclass(frozen=True, slots=True)
class AnalysisMaterial:
    reference: ProposedMaterialRef
    root: ContentSource
    corpus: CanonicalStandardsCorpus
    graph: EdgeRegistry
    policy_impact: CompiledPolicyImpactSet
    coverage: CoverageDefinitionIndex


@dataclass(frozen=True, slots=True)
class MaterialRequirement:
    id: str
    fact: FactContract
    prompt: str
    dependent_programs: tuple[str, ...]
    projection: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class CoverageProjection:
    subject: str
    requirement_id: str
    requirement: Mapping[str, object]
    view: CoverageViewDefinition
    certificate_id: str | None
    certificate: Mapping[str, object] | None


@dataclass(frozen=True, slots=True)
class AnalysisEvaluation:
    state: AnalysisState
    context_id: str
    context: Mapping[str, object]
    changes: tuple[ClassifiedChange, ...]
    requirements: tuple[MaterialRequirement, ...]
    pending_requirements: tuple[MaterialRequirement, ...]
    obligations: tuple[Obligation, ...]
    reached_obligations: tuple[Obligation, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    coverage: tuple[CoverageProjection, ...]

    @property
    def complete(self) -> bool:
        return not self.pending_requirements and all(
            item.state == "resolved" for item in self.obligations
        )


def parse_change(value: Mapping[str, object]) -> ChangeDescriptor:
    scope = value.get("scope")
    if not isinstance(scope, Mapping):
        raise _error("CHANGE.SCOPE", "change scope is missing")
    heading_path = scope.get("heading_path", ())
    return ChangeDescriptor(
        ChangeKind(str(value["kind"])),
        tuple(str(item) for item in value["accepted_ids"]),
        tuple(str(item) for item in value["proposed_ids"]),
        ReviewScope(str(scope["kind"]), tuple(str(item) for item in heading_path)),
        None if value.get("accepted_module") is None else str(value["accepted_module"]),
        None if value.get("proposed_module") is None else str(value["proposed_module"]),
    )


def parse_semantic_proposal(value: Mapping[str, object]) -> SemanticProposal:
    accepted = value["accepted_semantic_revision"]
    return SemanticProposal(
        str(value["policy"]),
        None if accepted is None else int(accepted),
        int(value["proposed_semantic_revision"]),
        str(value["intent"]),
        str(value["structural_digest"]),
    )


def evaluate_analysis(
    state: AnalysisState,
    accepted: AnalysisMaterial,
    proposed: AnalysisMaterial,
) -> AnalysisEvaluation:
    if (
        accepted.reference != SnapshotMaterialRef(state.base_snapshot)
        or proposed.reference != state.proposed_material
    ):
        raise _error(
            "ANALYSIS.MATERIAL_MISMATCH",
            "Analysis material does not match the state material references.",
        )
    descriptors = tuple(parse_change(plain_record(item)) for item in state.changes)
    proposals = tuple(
        parse_semantic_proposal(plain_record(item)) for item in state.semantic_proposals
    )
    changes = classify_changes(
        accepted.corpus.policy_unit_corpus,
        proposed.corpus.policy_unit_corpus,
        descriptors,
        proposals,
        accepted_module_ids=(item.module_id for item in accepted.corpus.modules),
        proposed_module_ids=(item.module_id for item in proposed.corpus.modules),
    )
    context = {
        "subjects": sorted(
            (unit.as_contract() for change in changes for unit in change.changed_units),
            key=analysis_key_bytes,
        ),
        "changes": [item.as_contract() for item in descriptors],
        "semantic_proposals": [_proposal(item) for item in proposals],
    }
    context_id = child_id(context)
    if (
        accepted.policy_impact.fact_schema.digest
        != proposed.policy_impact.fact_schema.digest
    ):
        raise _error(
            "FACT_SCHEMA_EVOLUTION_UNSUPPORTED",
            "accepted and proposed fact schemas differ",
            outcome="unsupported",
        )

    observations = {
        str(item["requirement_id"]): item
        for item in (plain_record(record) for record in state.fact_observations)
    }
    raw_facts: dict[str, object] = {}
    applied: set[str] = set()
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
        requirements = _requirements(context_id, proposed.policy_impact, selections)
        newly_applied = False
        for requirement in requirements:
            observation = observations.get(requirement.id)
            if observation is None or requirement.id in applied:
                continue
            raw_facts[requirement.fact.id] = observation["value"]
            applied.add(requirement.id)
            newly_applied = True
            break
        if not newly_applied:
            break

    pending = tuple(item for item in requirements if item.id not in applied)
    valid_requirement_ids = {
        _requirement(context_id, fact, ()).id
        for fact in proposed.policy_impact.fact_schema.definitions
    }
    if set(observations) - valid_requirement_ids:
        raise _error(
            "ANALYSIS.INVALID_RETAINED_DECISION",
            "Analysis state contains a dependency-invalid fact observation.",
        )

    coverage = _coverage(state, accepted, proposed, changes)
    covered_subjects = {
        item.subject for item in coverage if item.certificate_id is not None
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
                if not (
                    item.kind == "audit-coverage" and item.target in covered_subjects
                )
            }.values(),
            key=lambda item: item.id,
        )
    )
    supplied_dispositions = tuple(plain_record(item) for item in state.dispositions)
    valid_dispositions = _valid_dispositions(supplied_dispositions, reached)
    if len(valid_dispositions) != len(supplied_dispositions):
        raise _error(
            "ANALYSIS.INVALID_RETAINED_DECISION",
            "Analysis state contains a dependency-invalid disposition.",
        )
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
    return AnalysisEvaluation(
        state,
        context_id,
        MappingProxyType(context),
        changes,
        requirements,
        pending,
        current,
        reached,
        _reading_plan(reached, accepted, proposed),
        coverage,
    )


def _requirements(
    context_id: str,
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
        result.append(_requirement(context_id, fact, programs[fact_id]))
    return tuple(result)


def _requirement(
    context_id: str,
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
    projection = {
        "fact": fact.id,
        "fact_semantic_revision": fact.semantic_revision,
        "fact_contract_digest": fact.digest,
        "context_id": context_id,
        "value_contract": value_contract,
        "answer_contract": fact.answer_contract,
        "evidence_contract": fact.evidence_contract,
        "authorization_capability": fact.authorization_capability,
    }
    return MaterialRequirement(
        child_id(projection),
        fact,
        fact.prompt,
        tuple(sorted(set(dependent_programs))),
        MappingProxyType(projection),
    )


def _coverage(
    state: AnalysisState,
    accepted: AnalysisMaterial,
    proposed: AnalysisMaterial,
    changes: Iterable[ClassifiedChange],
) -> tuple[CoverageProjection, ...]:
    supplied = {
        str(item["requirement_id"]): item
        for item in (plain_record(record) for record in state.coverage_attestations)
    }
    results: dict[str, CoverageProjection] = {}
    consumed: set[str] = set()
    for change in changes:
        material = proposed if change.descriptor.proposed_ids else accepted
        subjects = change.descriptor.proposed_ids or change.descriptor.accepted_ids
        for subject in subjects:
            view = material.coverage.views.get(subject)
            requirement = material.coverage.requirements.get(subject)
            if view is None or requirement is None:
                raise _error(
                    "COVERAGE.SUBJECT_UNAVAILABLE",
                    "changed policy has no current coverage requirement",
                    outcome="unavailable",
                )
            requirement_projection = coverage_requirement_projection(requirement, view)
            requirement_id = child_id(requirement_projection)
            attestation = supplied.get(requirement_id)
            certificate = None
            certificate_id = None
            if attestation is not None:
                consumed.add(requirement_id)
                certificate = _coverage_certificate(
                    requirement_id, requirement, view, attestation
                )
                certificate_id = child_id(certificate)
            results[subject] = CoverageProjection(
                subject,
                requirement_id,
                MappingProxyType(requirement_projection),
                view,
                certificate_id,
                None if certificate is None else MappingProxyType(certificate),
            )
    if set(supplied) != consumed:
        raise _error(
            "ANALYSIS.INVALID_RETAINED_DECISION",
            "Analysis state contains a dependency-invalid coverage attestation.",
        )
    return tuple(results[key] for key in sorted(results))


def _coverage_certificate(
    requirement_id: str,
    requirement: CoverageRequirementDefinition,
    view: CoverageViewDefinition,
    attestation: Mapping[str, object],
) -> dict[str, object]:
    evidence = attestation.get("evidence")
    if not isinstance(evidence, list):
        raise _error("COVERAGE.INVALID_ATTESTATION", "attestation evidence is invalid")
    return {
        "requirement_id": requirement_id,
        "subject": requirement.subject,
        "owner": requirement.owner,
        "semantic_revision": requirement.semantic_revision,
        "horizon_digest": view.horizon_digest,
        "relationship_digest": analysis_value_digest(
            [
                {"edge": edge, "fingerprint": fingerprint}
                for edge, fingerprint in view.relationship_fingerprints
            ]
        ),
        "evidence_digests": sorted(str(item["digest"]) for item in evidence),
        "fact_schema_digest": view.fact_schema_digest,
        "attestation_digest": analysis_value_digest(attestation),
    }


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
        for subject in (
            change.descriptor.proposed_ids or change.descriptor.accepted_ids
        )
    }
    obligations = []
    for subject in sorted(by_subject):
        item = by_subject[subject]
        if item.certificate_id is not None:
            continue
        material = proposed if subject in proposed.coverage.views else accepted
        view = material.coverage.views[subject]
        dependencies = (
            DecisionDependency(
                "audit",
                item.requirement_id,
                raw_digest(analysis_key_bytes(item.requirement)),
            ),
            DecisionDependency(
                "policy-unit",
                subject,
                raw_digest(
                    analysis_key_bytes(
                        {
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
                analysis_identity(OBLIGATION_DOMAIN, "obligation", identifying),
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
        if (
            obligation is None
            or item.get("fingerprint") != obligation.fingerprint.as_contract()
        ):
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


def _error(code: str, message: str, *, outcome: str = "invalid") -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, outcome, message))


__all__ = (
    "AnalysisEvaluation",
    "AnalysisMaterial",
    "CoverageProjection",
    "MaterialRequirement",
    "evaluate_analysis",
    "parse_change",
    "parse_semantic_proposal",
)
