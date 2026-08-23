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

from .changes import ClassifiedChange, ReviewScope
from .coverage import CoverageIndex
from .errors import AnalysisError, AnalysisFailure
from .impact import ImpactSelection
from .serialization import identity


OBLIGATION_DOMAIN = "coding-standards:obligation:v1"
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
    source: str
    target: str
    scope: ReviewScope
    reason: Mapping[str, str]
    state: str
    permitted_submissions: tuple[str, ...]
    fingerprint: DecisionFingerprint
    applicability: str = "not-declared"

    def __post_init__(self) -> None:
        object.__setattr__(self, "reason", MappingProxyType(dict(self.reason)))

    def as_contract(self) -> dict[str, object]:
        return {
            "id": self.id,
            "kind": self.kind,
            "source": self.source,
            "target": self.target,
            "scope": self.scope.as_contract(),
            "reason": dict(self.reason),
            "state": self.state,
            "applicability": self.applicability,
            "permitted_submissions": list(self.permitted_submissions),
            "fingerprint": self.fingerprint.as_contract(),
        }


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
            "source": subject,
            "target": subject,
            "scope": scope.as_contract(),
            "reason": reason,
            "fingerprint": fingerprint.as_contract(),
        }
        obligations.append(
            Obligation(
                identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                "audit-coverage",
                subject,
                subject,
                scope,
                reason,
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
            if candidate.applicability != "unknown":
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
            policy_traces = tuple(
                trace
                for trace in candidate.traces
                if trace.policy_semantics is not None
                and trace.applicability == "unknown"
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
                    "source": source,
                    "target": target,
                    "scope": candidate.conservative_review_scope.as_contract(),
                    "reason": reason,
                    "fingerprint": fingerprint.as_contract(),
                }
                obligations.append(
                    Obligation(
                        identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                        "applicability-resolution",
                        source,
                        target,
                        candidate.conservative_review_scope,
                        reason,
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
            "source": module_id,
            "target": module_id,
            "scope": {"kind": "whole-artifact"},
            "reason": reason,
            "fingerprint": fingerprint.as_contract(),
        }
        obligations.append(
            Obligation(
                identity(OBLIGATION_DOMAIN, "obligation", identity_value),
                "unmapped-normative-change",
                module_id,
                module_id,
                ReviewScope("whole-artifact"),
                reason,
                "required",
                ("impact-disposition",),
                fingerprint,
            )
        )
    return tuple(obligations)
