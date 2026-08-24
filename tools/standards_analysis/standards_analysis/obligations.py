from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Mapping

from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    PolicyUnit,
    PolicyUnitTombstone,
    canonical_json_bytes,
    digest_bytes,
    project_unmapped_module,
)

from .changes import ChangedPolicyUnit, ClassifiedChange, ReviewScope
from .coverage import CoverageIndex
from .errors import AnalysisError, AnalysisFailure
from .impact import ImpactSelection, ImpactTrace
from .serialization import identity


OBLIGATION_DOMAIN = "coding-standards:obligation:v2"
ABSENT_DIGEST = digest_bytes(canonical_json_bytes({"state": "absent"}))


@dataclass(frozen=True, slots=True)
class DecisionDependency:
    dependency_class: str
    identity: str
    digest: str

    def as_contract(self) -> dict[str, str]:
        return {
            "class": self.dependency_class,
            "identity": self.identity,
            "digest": self.digest,
        }


@dataclass(frozen=True, slots=True)
class DecisionContract:
    id: str
    version: int
    dependency_classes: tuple[str, ...]

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "decision-contract",
            "id": self.id,
            "version": self.version,
            "dependency_classes": list(self.dependency_classes),
        }


@dataclass(frozen=True, slots=True)
class ConsumerReviewContract:
    id: str
    version: int
    permitted_dispositions: tuple[str, ...]
    evidence_contract: str
    authorization_capability: str
    semantics: str

    def __post_init__(self) -> None:
        if (
            not self.id
            or self.version < 1
            or not self.permitted_dispositions
            or len(set(self.permitted_dispositions))
            != len(self.permitted_dispositions)
            or not self.evidence_contract
            or not self.authorization_capability
            or not self.semantics
        ):
            raise AnalysisError(
                AnalysisFailure(
                    "CONSUMER_REVIEW.CONTRACT_INVALID",
                    "invalid",
                    "consumer review contract is incomplete or contradictory",
                    field="review_contract",
                    observed=self.id,
                )
            )

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "consumer-review-contract",
            "id": self.id,
            "version": self.version,
            "permitted_dispositions": list(self.permitted_dispositions),
            "evidence_contract": self.evidence_contract,
            "authorization_capability": self.authorization_capability,
            "semantics": self.semantics,
        }


CONSUMER_REVIEW_CONTRACT = ConsumerReviewContract(
    "decision-contract.consumer-review.v1",
    1,
    ("updated", "reviewed-no-change", "not-applicable", "blocked"),
    "evidence-reference.v1",
    "standards.review.consumer",
    "review the exact consumer scope for every definitely applicable selector",
)


UNMAPPED_DECISION_CONTRACT = DecisionContract(
    "decision-contract.unmapped-normative-change.v1",
    1,
    (
        "analysis-contract",
        "module-locator",
        "policy-unit",
        "representation",
    ),
)
APPLICABILITY_DECISION_CONTRACT = DecisionContract(
    "decision-contract.applicability-resolution.v1",
    1,
    (
        "applicability-contract",
        "applicability-fact",
        "question",
        "relationship",
    ),
)
COVERAGE_DECISION_CONTRACT = DecisionContract(
    "decision-contract.audit-coverage.v1",
    1,
    (
        "audit",
        "policy-unit",
        "provider-contract",
    ),
)
UNMAPPED_CONTRACT_DIGEST = digest_bytes(
    canonical_json_bytes(UNMAPPED_DECISION_CONTRACT.as_contract())
)
APPLICABILITY_CONTRACT_DIGEST = digest_bytes(
    canonical_json_bytes(APPLICABILITY_DECISION_CONTRACT.as_contract())
)
COVERAGE_CONTRACT_DIGEST = digest_bytes(
    canonical_json_bytes(COVERAGE_DECISION_CONTRACT.as_contract())
)
@dataclass(frozen=True, slots=True)
class DecisionFingerprint:
    decision_kind: str
    decision_contract: str
    dependencies: tuple[DecisionDependency, ...]
    schema_version: int = 1

    def as_contract(self) -> dict[str, object]:
        return {
            "decision_kind": self.decision_kind,
            "decision_contract": self.decision_contract,
            "schema_version": self.schema_version,
            "dependencies": [item.as_contract() for item in self.dependencies],
        }


@dataclass(frozen=True, slots=True)
class Obligation:
    id: str
    kind: str
    target: str
    scope: ReviewScope
    reasons: tuple[Mapping[str, object], ...]
    state: str
    permitted_submissions: tuple[str, ...]
    fingerprint: DecisionFingerprint
    applicability: str = "not-declared"
    review_contract: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "reasons",
            tuple(_freeze_reason(reason) for reason in self.reasons),
        )
        if self.review_contract is not None:
            object.__setattr__(
                self,
                "review_contract",
                _freeze_reason(self.review_contract),
            )

    def as_contract(self) -> dict[str, object]:
        value: dict[str, object] = {
            "id": self.id,
            "kind": self.kind,
            "target": self.target,
            "scope": self.scope.as_contract(),
            "reasons": [_thaw_reason(reason) for reason in self.reasons],
            "state": self.state,
            "applicability": self.applicability,
            "permitted_submissions": list(self.permitted_submissions),
            "fingerprint": self.fingerprint.as_contract(),
        }
        if self.review_contract is not None:
            value["review_contract"] = _thaw_reason(self.review_contract)
        return value


@dataclass(frozen=True, slots=True)
class ApplicabilityQuestion:
    id: str
    fact: str
    prompt: str
    state: str = "required"
    permitted_answers: tuple[str, ...] = ("known", "known-absent", "unknown")

    def as_contract(self) -> dict[str, object]:
        return {
            "id": self.id,
            "kind": "applicability-fact",
            "prompt": self.prompt,
            "state": self.state,
            "permitted_answers": list(self.permitted_answers),
        }


@dataclass(frozen=True, slots=True)
class ApplicabilityResolutionWork:
    questions: tuple[ApplicabilityQuestion, ...]
    obligations: tuple[Obligation, ...]


@dataclass(frozen=True, slots=True)
class ConsumerTraceReference:
    id: str
    graph: str
    applicability: str

    def as_contract(self) -> dict[str, str]:
        return {
            "id": self.id,
            "graph": self.graph,
            "applicability": self.applicability,
        }


@dataclass(frozen=True, slots=True)
class ConsumerSelectionReason:
    source: str
    edge: str
    relation: str
    evidence_owner: str
    traces: tuple[ConsumerTraceReference, ...]

    def as_contract(self) -> dict[str, object]:
        return {
            "kind": "policy-impact-edge",
            "source": self.source,
            "edge": self.edge,
            "relation": self.relation,
            "evidence_owner": self.evidence_owner,
            "traces": [trace.as_contract() for trace in self.traces],
        }


@dataclass(frozen=True, slots=True)
class ConsumerSelection:
    target: str
    scope: ReviewScope
    review_contract: ConsumerReviewContract
    reasons: tuple[ConsumerSelectionReason, ...]
    evidence_owners: tuple[str, ...]
    fingerprint: DecisionFingerprint


def generate_consumer_review_obligations(
    selections: Iterable[ImpactSelection],
    *,
    review_contracts: Mapping[str, ConsumerReviewContract] | None = None,
) -> tuple[Obligation, ...]:
    selected = tuple(selections)
    contracts = dict(review_contracts or {})
    _validate_review_contracts(contracts)
    changed_by_policy: dict[str, ChangedPolicyUnit] = {}
    for selection in selected:
        for unit in selection.change.changed_units:
            current = changed_by_policy.setdefault(unit.policy, unit)
            if current != unit:
                raise AnalysisError(
                    AnalysisFailure(
                        "CONSUMER_REVIEW.CHANGE_CONFLICT",
                        "invalid",
                        "one policy selector is bound to conflicting classified changes",
                        field="source",
                        observed=unit.policy,
                    )
                )
    grouped: dict[
        tuple[str, bytes, str],
        dict[tuple[str, str, str, str], list[ImpactTrace]],
    ] = {}
    scopes: dict[tuple[str, bytes, str], ReviewScope] = {}
    contracts_by_key: dict[tuple[str, bytes, str], ConsumerReviewContract] = {}
    traces_by_id: dict[str, ImpactTrace] = {}
    for selection in selected:
        for candidate in selection.candidates:
            for trace in candidate.traces:
                semantics = trace.policy_semantics
                if semantics is None or trace.applicability != "true":
                    continue
                review_contract = contracts.get(
                    semantics.relation,
                    CONSUMER_REVIEW_CONTRACT,
                )
                scope = _consumer_scope(semantics.consumer_scope)
                key = (
                    semantics.consumer,
                    canonical_json_bytes(scope.as_contract()),
                    review_contract.id,
                )
                reason_key = (
                    semantics.source,
                    trace.edge_id,
                    semantics.relation,
                    semantics.evidence_owner,
                )
                grouped.setdefault(key, {}).setdefault(reason_key, []).append(trace)
                scopes[key] = scope
                contracts_by_key[key] = review_contract
                current_trace = traces_by_id.setdefault(trace.id, trace)
                if current_trace != trace:
                    raise AnalysisError(
                        AnalysisFailure(
                            "CONSUMER_REVIEW.TRACE_ID_CONFLICT",
                            "invalid",
                            "one impact-trace identity describes conflicting traces",
                            field="trace_id",
                            observed=trace.id,
                        )
                    )

    obligations: list[Obligation] = []
    for key in sorted(grouped, key=lambda item: (item[0], item[1], item[2])):
        target, _scope_bytes, _contract = key
        review_contract = contracts_by_key[key]
        reasons = tuple(
            ConsumerSelectionReason(
                source,
                edge,
                relation,
                evidence_owner,
                tuple(
                    ConsumerTraceReference(
                        trace.id,
                        trace.graph,
                        trace.applicability,
                    )
                    for trace in sorted(
                        {item.id: item for item in grouped[key][reason_key]}.values(),
                        key=lambda item: (item.graph, item.id),
                    )
                ),
            )
            for reason_key in sorted(grouped[key])
            for source, edge, relation, evidence_owner in (reason_key,)
        )
        scope = scopes[key]
        evidence_owners = tuple(
            sorted({reason.evidence_owner for reason in reasons})
        )
        fingerprint = _consumer_fingerprint(
            target,
            scope,
            review_contract,
            reasons,
            changed_by_policy,
            traces_by_id,
            evidence_owners,
        )
        aggregate = ConsumerSelection(
            target,
            scope,
            review_contract,
            reasons,
            evidence_owners,
            fingerprint,
        )
        reason_values = tuple(reason.as_contract() for reason in aggregate.reasons)
        identity_value = {
            "kind": "consumer-review",
            "target": aggregate.target,
            "scope": aggregate.scope.as_contract(),
            "reasons": list(reason_values),
            "fingerprint": aggregate.fingerprint.as_contract(),
        }
        obligations.append(
            Obligation(
                identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                "consumer-review",
                aggregate.target,
                aggregate.scope,
                reason_values,
                "required",
                ("consumer-disposition",),
                aggregate.fingerprint,
                "true",
                aggregate.review_contract.as_contract(),
            )
        )
    return tuple(obligations)


def _validate_review_contracts(
    contracts: Mapping[str, ConsumerReviewContract],
) -> None:
    by_id: dict[str, ConsumerReviewContract] = {}
    for relation, contract in contracts.items():
        if not relation:
            raise AnalysisError(
                AnalysisFailure(
                    "CONSUMER_REVIEW.CONTRACT_RELATION_INVALID",
                    "invalid",
                    "review-contract mappings require a relationship identity",
                    field="relation",
                )
            )
        current = by_id.setdefault(contract.id, contract)
        if current != contract:
            raise AnalysisError(
                AnalysisFailure(
                    "CONSUMER_REVIEW.CONTRACT_ID_CONFLICT",
                    "invalid",
                    "one review-contract identity has conflicting definitions",
                    field="review_contract",
                    observed=contract.id,
                )
            )


def _consumer_scope(value: Mapping[str, object] | None) -> ReviewScope:
    if value is None or value.get("kind") == "whole-artifact":
        return ReviewScope("whole-artifact")
    if value.get("kind") == "structured":
        headings = value.get("heading_path")
        if isinstance(headings, tuple) and all(
            isinstance(item, str) and item for item in headings
        ):
            return ReviewScope("structured", headings)
    raise AnalysisError(
        AnalysisFailure(
            "CONSUMER_REVIEW.SCOPE_INVALID",
            "invalid",
            "compiled consumer scope is not a canonical review scope",
            field="consumer_scope",
        )
    )


def _consumer_fingerprint(
    target: str,
    scope: ReviewScope,
    contract: ConsumerReviewContract,
    reasons: tuple[ConsumerSelectionReason, ...],
    changed_by_policy: Mapping[str, ChangedPolicyUnit],
    traces_by_id: Mapping[str, ImpactTrace],
    evidence_owners: tuple[str, ...],
) -> DecisionFingerprint:
    dependencies: list[DecisionDependency] = [
        DecisionDependency(
            "analysis-contract",
            f"consumer-review-key:{target}",
            digest_bytes(
                canonical_json_bytes(
                    {
                        "target": target,
                        "scope": scope.as_contract(),
                        "review_contract": contract.id,
                    }
                )
            ),
        ),
        DecisionDependency(
            "provider-contract",
            contract.id,
            digest_bytes(canonical_json_bytes(contract.as_contract())),
        ),
    ]
    for source in sorted({reason.source for reason in reasons}):
        changed = changed_by_policy.get(source)
        if changed is None:
            raise AnalysisError(
                AnalysisFailure(
                    "CONSUMER_REVIEW.SOURCE_UNBOUND",
                    "invalid",
                    "consumer selector is not bound to a classified policy change",
                    field="source",
                    observed=source,
                )
            )
        dependencies.append(
            DecisionDependency(
                "policy-unit",
                source,
                digest_bytes(canonical_json_bytes(changed.as_contract())),
            )
        )
    for reason in reasons:
        selected_traces = tuple(traces_by_id[item.id] for item in reason.traces)
        dependencies.append(
            DecisionDependency(
                "relationship",
                reason.edge,
                digest_bytes(
                    canonical_json_bytes(
                        {
                            "reason": reason.as_contract(),
                            "semantic_dependencies": sorted(
                                {
                                    trace.policy_semantics.dependency_fingerprint
                                    for trace in selected_traces
                                    if trace.policy_semantics is not None
                                }
                            ),
                        }
                    )
                ),
            )
        )
    fact_values: dict[str, set[str]] = {}
    for reason in reasons:
        for reference in reason.traces:
            for fact, digest in traces_by_id[reference.id].applicability_facts:
                fact_values.setdefault(fact, set()).add(digest)
    dependencies.extend(
        DecisionDependency(
            "applicability-fact",
            fact,
            digest_bytes(canonical_json_bytes(sorted(fact_values[fact]))),
        )
        for fact in sorted(fact_values)
    )
    dependencies.extend(
        DecisionDependency(
            "evidence",
            owner,
            digest_bytes(canonical_json_bytes({"evidence_owner": owner})),
        )
        for owner in evidence_owners
    )
    return DecisionFingerprint(
        "consumer-review",
        contract.id,
        tuple(
            sorted(
                dependencies,
                key=lambda item: (item.dependency_class, item.identity),
            )
        ),
    )


def _freeze_reason(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze_reason(item) for key, item in value.items()}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_reason(item) for item in value)
    return value


def _thaw_reason(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw_reason(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_reason(item) for item in value]
    return value


def generate_coverage_obligations(
    changes: Iterable[ClassifiedChange],
    accepted: CoverageIndex,
    proposed: CoverageIndex,
) -> tuple[Obligation, ...]:
    selected: dict[str, tuple[CoverageIndex, ReviewScope]] = {}
    for change in changes:
        descriptor = change.descriptor
        index = proposed if descriptor.proposed_ids else accepted
        subjects = descriptor.proposed_ids or descriptor.accepted_ids
        for subject in subjects:
            selected[subject] = (index, descriptor.scope)

    obligations: list[Obligation] = []
    for subject in sorted(selected):
        index, scope = selected[subject]
        requirement = index.requirements.get(subject)
        view = index.views.get(subject)
        if requirement is None or view is None:
            raise AnalysisError(
                AnalysisFailure(
                    "COVERAGE.SUBJECT_UNAVAILABLE",
                    "unavailable",
                    "changed policy has no current coverage requirement",
                    field="subject",
                    observed=subject,
                )
            )
        if index.certificate_for(subject) is not None:
            continue
        dependencies = (
            DecisionDependency(
                "audit",
                requirement.handle,
                digest_bytes(canonical_json_bytes(requirement.as_projection())),
            ),
            DecisionDependency(
                "policy-unit",
                subject,
                digest_bytes(
                    canonical_json_bytes(
                        {
                            "coverage_view": view.handle,
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
                COVERAGE_CONTRACT_DIGEST,
            ),
        )
        fingerprint = DecisionFingerprint(
            "audit-coverage",
            COVERAGE_DECISION_CONTRACT.id,
            dependencies,
        )
        reason = {"kind": "audit-coverage", "source": subject}
        identity_value = {
            "kind": "audit-coverage",
            "target": subject,
            "scope": scope.as_contract(),
            "reasons": [reason],
            "fingerprint": fingerprint.as_contract(),
        }
        obligations.append(
            Obligation(
                identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                "audit-coverage",
                subject,
                scope,
                (reason,),
                "required",
                ("coverage-attestation",),
                fingerprint,
            )
        )
    return tuple(obligations)


def generate_applicability_resolution_work(
    selections: Iterable[ImpactSelection],
) -> ApplicabilityResolutionWork:
    question_by_fact: dict[str, ApplicabilityQuestion] = {}
    obligations: list[Obligation] = []
    for selection in selections:
        for candidate in selection.candidates:
            policy_traces = tuple(
                trace
                for trace in candidate.traces
                if trace.policy_semantics is not None
                and trace.applicability == "unknown"
            )
            if not policy_traces:
                continue
            if candidate.conservative_review_scope is None:
                raise AnalysisError(
                    AnalysisFailure(
                        "IMPACT.UNKNOWN_SCOPE_MISSING",
                        "invalid",
                        "unknown applicability requires conservative review scope",
                        field="edge_id",
                        observed=candidate.edge_id,
                    )
                )
            if not policy_traces or not candidate.unresolved_facts:
                raise AnalysisError(
                    AnalysisFailure(
                        "IMPACT.UNKNOWN_FACTS_MISSING",
                        "invalid",
                        "unknown applicability requires exact unresolved facts",
                        field="edge_id",
                        observed=candidate.edge_id,
                    )
                )
            source = policy_traces[0].source
            target = policy_traces[0].target
            if any(
                (trace.source, trace.target) != (source, target)
                for trace in policy_traces
            ):
                raise AnalysisError(
                    AnalysisFailure(
                        "IMPACT.RELATIONSHIP_IDENTITY_CONFLICT",
                        "invalid",
                        "one impact candidate cannot identify several relationships",
                        field="edge_id",
                        observed=candidate.edge_id,
                    )
                )
            for fact in candidate.unresolved_facts:
                schema_digests = {
                    trace.policy_semantics.applicability_program.schema_digest
                    for trace in policy_traces
                    if trace.policy_semantics is not None
                    and fact
                    in trace.policy_semantics.applicability_program.referenced_facts
                }
                program_digests = {
                    trace.policy_semantics.applicability_program.dependency_digest
                    for trace in policy_traces
                    if trace.policy_semantics is not None
                    and fact
                    in trace.policy_semantics.applicability_program.referenced_facts
                }
                relationship_digests = {
                    trace.policy_semantics.dependency_fingerprint
                    for trace in policy_traces
                    if trace.policy_semantics is not None
                    and fact
                    in trace.policy_semantics.applicability_program.referenced_facts
                }
                if not schema_digests or not program_digests or not relationship_digests:
                    raise AnalysisError(
                        AnalysisFailure(
                            "IMPACT.UNRESOLVED_FACT_UNBOUND",
                            "invalid",
                            "unresolved fact is not bound to candidate semantics",
                            field="fact",
                            observed=fact,
                        )
                    )
                question = question_by_fact.setdefault(
                    fact,
                    ApplicabilityQuestion(
                        f"question.applicability.{fact}",
                        fact,
                        f"Provide the typed value for applicability fact `{fact}`.",
                    ),
                )
                question_digest = digest_bytes(
                    canonical_json_bytes(
                        {
                            "fact": fact,
                            "question": question.as_contract(),
                            "schema_digests": sorted(schema_digests),
                        }
                    )
                )
                dependencies = (
                    DecisionDependency(
                        "applicability-contract",
                        APPLICABILITY_DECISION_CONTRACT.id,
                        APPLICABILITY_CONTRACT_DIGEST,
                    ),
                    DecisionDependency(
                        "applicability-fact",
                        fact,
                        digest_bytes(
                            canonical_json_bytes(
                                {
                                    "schema_digests": sorted(schema_digests),
                                    "program_digests": sorted(program_digests),
                                }
                            )
                        ),
                    ),
                    DecisionDependency(
                        "question",
                        question.id,
                        question_digest,
                    ),
                    DecisionDependency(
                        "relationship",
                        candidate.edge_id,
                        digest_bytes(
                            canonical_json_bytes(sorted(relationship_digests))
                        ),
                    ),
                )
                fingerprint = DecisionFingerprint(
                    "applicability-resolution",
                    APPLICABILITY_DECISION_CONTRACT.id,
                    dependencies,
                )
                reason = {
                    "kind": "question",
                    "source": source,
                    "fact": fact,
                    "edge": candidate.edge_id,
                    "question": question.id,
                }
                identity_value = {
                    "kind": "applicability-resolution",
                    "target": target,
                    "scope": candidate.conservative_review_scope.as_contract(),
                    "reasons": [reason],
                    "fingerprint": fingerprint.as_contract(),
                }
                obligations.append(
                    Obligation(
                        identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                        "applicability-resolution",
                        target,
                        candidate.conservative_review_scope,
                        (reason,),
                        "required",
                        ("fact-answer",),
                        fingerprint,
                        "unknown",
                    )
                )
    return ApplicabilityResolutionWork(
        tuple(question_by_fact[fact] for fact in sorted(question_by_fact)),
        tuple(sorted(obligations, key=lambda item: item.id)),
    )


def _authority_digest(value: PolicyUnit | PolicyUnitTombstone | None) -> str:
    if value is None:
        return ABSENT_DIGEST
    if isinstance(value, PolicyUnitTombstone):
        projection: dict[str, object] = {
            "state": "retired",
            "id": value.id,
            "retired_semantic_revision": value.retired_semantic_revision,
            "successors": list(value.successors),
            "evidence": value.evidence,
        }
    else:
        projection = {
            "state": "active",
            "id": value.id,
            "module": value.module,
            "heading_path": list(value.heading_path),
            "semantic_revision": value.semantic_revision,
            "aliases": list(value.aliases),
            "predecessors": list(value.predecessors),
            "successors": list(value.successors),
            "representation_digest": value.representation_digest,
            "structural_digest": value.structural_digest,
        }
    return digest_bytes(canonical_json_bytes(projection))


def _module_policy_ids(
    accepted: CanonicalStandardsCorpus,
    proposed: CanonicalStandardsCorpus,
    module_id: str,
) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                unit.id
                for corpus in (accepted, proposed)
                for unit in corpus.policy_unit_corpus.for_module(module_id)
            }
        )
    )


def generate_unmapped_normative_obligations(
    accepted_root: Path,
    accepted: CanonicalStandardsCorpus,
    proposed_root: Path,
    proposed: CanonicalStandardsCorpus,
    changes: Iterable[ClassifiedChange],
) -> tuple[Obligation, ...]:
    selected = tuple(changes)
    claimed = {
        policy_id
        for change in selected
        for policy_id in (
            *change.descriptor.accepted_ids,
            *change.descriptor.proposed_ids,
        )
    }
    accepted_modules = {module.module_id: module for module in accepted.modules}
    proposed_modules = {module.module_id: module for module in proposed.modules}
    obligations: list[Obligation] = []

    for module_id in sorted(set(accepted_modules) | set(proposed_modules)):
        before_module = accepted_modules.get(module_id)
        after_module = proposed_modules.get(module_id)
        if all(
            module is None or module.role == "reference"
            for module in (before_module, after_module)
        ):
            continue

        before_projection = (
            None
            if before_module is None
            else project_unmapped_module(accepted_root, accepted, module_id)
        )
        after_projection = (
            None
            if after_module is None
            else project_unmapped_module(proposed_root, proposed, module_id)
        )
        dependencies = [
            DecisionDependency(
                "representation",
                f"{module_id}:accepted-unmapped",
                ABSENT_DIGEST if before_projection is None else before_projection.digest,
            ),
            DecisionDependency(
                "representation",
                f"{module_id}:proposed-unmapped",
                ABSENT_DIGEST if after_projection is None else after_projection.digest,
            ),
            DecisionDependency(
                "module-locator",
                f"{module_id}:accepted-module",
                ABSENT_DIGEST
                if before_module is None
                else digest_bytes(canonical_json_bytes({"path": before_module.path})),
            ),
            DecisionDependency(
                "module-locator",
                f"{module_id}:proposed-module",
                ABSENT_DIGEST
                if after_module is None
                else digest_bytes(canonical_json_bytes({"path": after_module.path})),
            ),
        ]
        changed_outside_units = (
            before_projection is None
            or after_projection is None
            or before_projection.digest != after_projection.digest
            or before_module.path != after_module.path
        )
        unclaimed_change = False
        for policy_id in _module_policy_ids(accepted, proposed, module_id):
            before_policy = accepted.resolve_policy_unit(policy_id)
            after_policy = proposed.resolve_policy_unit(policy_id)
            before_digest = _authority_digest(before_policy)
            after_digest = _authority_digest(after_policy)
            if before_digest == after_digest or policy_id in claimed:
                continue
            unclaimed_change = True
            dependencies.extend(
                (
                    DecisionDependency(
                        "policy-unit",
                        f"{policy_id}:accepted",
                        before_digest,
                    ),
                    DecisionDependency(
                        "policy-unit",
                        f"{policy_id}:proposed",
                        after_digest,
                    ),
                )
            )
        if not changed_outside_units and not unclaimed_change:
            continue

        dependencies.append(
            DecisionDependency(
                "analysis-contract",
                UNMAPPED_DECISION_CONTRACT.id,
                UNMAPPED_CONTRACT_DIGEST,
            )
        )
        fingerprint = DecisionFingerprint(
            "unmapped-normative-change",
            UNMAPPED_DECISION_CONTRACT.id,
            tuple(
                sorted(
                    dependencies,
                    key=lambda item: (item.dependency_class, item.identity),
                )
            ),
        )
        reason = {"kind": "unmapped-normative-change", "source": module_id}
        identity_value = {
            "kind": "unmapped-normative-change",
            "target": module_id,
            "scope": {"kind": "whole-artifact"},
            "reasons": [reason],
            "fingerprint": fingerprint.as_contract(),
        }
        obligations.append(
            Obligation(
                identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                "unmapped-normative-change",
                module_id,
                ReviewScope("whole-artifact"),
                (reason,),
                "required",
                ("impact-disposition",),
                fingerprint,
            )
        )
    return tuple(obligations)
