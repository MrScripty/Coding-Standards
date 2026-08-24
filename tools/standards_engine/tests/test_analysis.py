from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from tools.standards_applicability.standards_applicability import compile_fact_schema

from tools.standards_analysis.standards_analysis import (
    AuthorizationReference,
    AnalysisInput,
    ChangeDescriptor,
    ChangeKind,
    CompleteResult,
    ConsumerDispositionSubmission,
    EvidenceReference,
    ObservationClaim,
    ProvideFactSubmission,
    PendingResult,
    ProviderUnavailable,
    ReviewScope,
    bind_analysis_kernel,
    prepare_analysis,
    advance_analysis,
)
from tools.standards_engine.contracts.validate_contracts import (
    identity as contract_identity,
    validate,
)
from tools.standards_engine.standards_engine import (
    AgentToolFacade,
    AnalysisRequest,
    DirectoryAnalysisStateStore,
    InMemoryAnalysisStateStore,
    InspectCall,
    StandardsEngine,
)
from tools.standards_policy_impact.standards_policy_impact import (
    CompiledPolicyImpactSet,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json").read_text(
        encoding="utf-8"
    )
)


def authorization(capability: str) -> AuthorizationReference:
    return AuthorizationReference(
        f"authorization.{capability}",
        capability,
        "sha256:" + "a" * 64,
    )


class StaticFactProvider:
    id = "fixture.fact-provider"
    contract_version = "1"
    input_contract = "standards-snapshots"
    immutable_inputs = ()

    def __init__(self, value: bool) -> None:
        self.value = value

    def observe(self, requirement, _accepted_snapshot, _proposed_snapshot):
        return ObservationClaim(
            {
                "type": "boolean",
                "state": "known",
                "value": self.value,
            },
            (
                EvidenceReference(
                    f"evidence.provider.{requirement.fact}",
                    "sha256:" + "6" * 64,
                    self.id,
                    self.contract_version,
                ),
            ),
        )


class UnavailableFactProvider(StaticFactProvider):
    def observe(self, requirement, _accepted_snapshot, _proposed_snapshot):
        return ProviderUnavailable(f"Evidence for {requirement.fact} is unavailable.")


def conditional_authority(engine, fact_declarations, expression):
    policy = "workflow.planning.written-plan-applicability"
    authority = engine._analysis_authority()
    original = authority.policy_impact
    fact_schema = compile_fact_schema(
        {
            "kind": "applicability-fact-schema",
            "id": "fixture.analysis.conditional-facts",
            "version": 1,
            "facts": list(fact_declarations),
        }
    )
    semantics = {
        edge_id: replace(
            item,
            applicability_program=fact_schema.compile(
                expression if item.source == policy else {"operator": "always"}
            ),
        )
        for edge_id, item in original.semantics.items()
    }
    return replace(
        authority,
        policy_impact=CompiledPolicyImpactSet(
            original.graph,
            semantics,
            fact_schema,
            original.node_catalog,
            original.declaration_sources,
            original.input_sources,
            original.declaration_digest,
            original.provider_contract_digest,
        ),
    )


def boolean_fact(identifier: str) -> dict[str, object]:
    return {
        "id": identifier,
        "semantic_revision": 1,
        "type": "boolean",
        "nullable": False,
        "aliases": [],
        "meaning": f"Whether {identifier} applies to this change.",
        "context_kind": "standards-change",
        "answer_contract": "fact-value.v1",
        "evidence_contract": "evidence-reference.v1",
        "authorization_capability": "standards.analyze",
        "prompt": f"Does {identifier} apply?",
    }


def replace_once(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    content = path.read_text(encoding="utf-8")
    if content.count(old) != 1:
        raise AssertionError(f"fixture source {relative!r} did not match exactly once")
    path.write_text(content.replace(old, new), encoding="utf-8")


def clear_coverage_attestations(root: Path) -> None:
    empty = "schema_version = 1\nattestations = []\n"
    for owner in ("workflow.planning", "workflow.commit"):
        path = (
            root
            / "evaluation/standards-effectiveness/policy-coverage/attestations"
            / f"{owner}.toml"
        )
        path.write_text(empty, encoding="utf-8")


def add_fixture_policy(root: Path) -> None:
    declaration = """

[[policy_unit]]
id = "workflow.planning.fixture-addition"
module = "workflow.planning"
heading_path = ["Fixture Addition"]
semantic_revision = 1
"""
    policy = """

## Fixture Addition

    This policy exists only in the typed analysis integration fixture.
"""
    sidecar = root / "evaluation/standards-effectiveness/policy-units/planning.toml"
    sidecar.write_text(
        sidecar.read_text(encoding="utf-8") + declaration,
        encoding="utf-8",
    )
    replace_once(
        root,
        "workflows/planning.md",
        "## Completion\n",
        policy.lstrip("\n") + "\n## Completion\n",
    )
    clear_coverage_attestations(root)


def remove_fixture_policy(root: Path) -> None:
    declaration = """[[policy_unit]]
id = "workflow.planning.projection-completeness"
module = "workflow.planning"
heading_path = ["Policy Projection Completeness"]
semantic_revision = 1

"""
    tombstone = """[[tombstone]]
id = "workflow.planning.projection-completeness"
retired_semantic_revision = 1
successors = []
evidence = "review.typed-agent-removal"

"""
    relationship = """[[relationships]]
source = "workflow.planning.projection-completeness"
consumer = "policy-semantic-impact"
relation = "enforcement-suite-projection"
applicability = { operator = "always" }
evidence_owner = "suite:policy-semantic-impact"
rationale = "Suite enforces the reviewed Planning semantic-impact structure and negative contracts."

"""
    policy = """## Policy Projection Completeness

A normative change updates every affected distribution and enforcement surface.
Before changing an audited policy owner, query the neutral repository graph's
`policy-impact` edge group from the owner's logical ID or repository-path alias
and review every returned consumer. Audit and add explicit edges for a
previously uncovered owner before its next normative change. One registered
source declares each edge; the neutral graph engine derives bidirectional
indexes and exposes the same declaration from either endpoint without owning
policy semantics. Group membership does not copy an edge, domain validation
remains group-specific, and traversal requires explicit permission. The graph
manifest owns current semantic relations; a change report owns change-specific
dispositions. Do not infer missing semantic consumers from hyperlinks, lexical
similarity, routing prerequisites, suite ownership, or another graph; correct
the authoritative declaration explicitly.

When a rule prescribes a machine protocol, concrete representation, or
automated gate, its applicable prompts, templates, fixtures, and executable
support agree before the rule becomes mandatory. Do not require a template,
prompt, fixture, or executable mechanism for a semantic policy that does not
use that surface.

Diagnostic outcomes must remain semantically distinguishable. A manual process
may record classifications in prose or a table; a tool may use typed values.
Planning does not require one serialized diagnostic representation.

"""
    sidecar = "evaluation/standards-effectiveness/policy-units/planning.toml"
    replace_once(root, sidecar, declaration, tombstone)
    replace_once(
        root,
        "evaluation/standards-effectiveness/policy-impact/workflow.planning.toml",
        relationship,
        "",
    )
    replace_once(root, "workflows/planning.md", policy, "")
    clear_coverage_attestations(root)


def fixture_repository(root: Path, change: str) -> Path:
    selected = root / "proposed"
    shutil.copytree(
        REPO_ROOT,
        selected,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )
    {"addition": add_fixture_policy, "removal": remove_fixture_policy}[change](selected)
    return selected


def coverage_attestation(obligation: dict[str, object]) -> dict[str, object]:
    fingerprint = obligation["fingerprint"]
    requirement_id = next(
        item["identity"]
        for item in fingerprint["dependencies"]
        if item["class"] == "audit"
    )
    evidence = {
        "id": "review.typed-agent-coverage",
        "digest": "sha256:" + "7" * 64,
        "provider_contract": "repository-content",
        "provider_contract_version": "1",
    }
    value = {
        "kind": "coverage-attestation",
        "handle": {
            "kind": "coverage-attestation-handle",
            "id": "coverage-attestation:sha256:" + "0" * 64,
            "schema_version": 1,
        },
        "requirement": {
            "kind": "coverage-requirement-handle",
            "id": requirement_id,
            "schema_version": 1,
        },
        "conclusion": "complete",
        "evidence": [evidence],
        "explicit_exclusions": [],
        "rationale": "The bounded fixture horizon was reviewed completely.",
        "auditor_provenance": "standards.review.audit:typed-agent-fixture",
        "schema_version": 1,
    }
    value["handle"]["id"] = contract_identity(SCHEMA, "CoverageAttestation", value)
    return value


class AnalysisWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = StandardsEngine.open_analysis(
            REPO_ROOT,
            REPO_ROOT,
            authorizations=(
                authorization("standards.analyze"),
                authorization("standards.review.consumer"),
                authorization("standards.review.impact"),
                authorization("standards.review.audit"),
            ),
        )

    def test_prepare_and_resolve_complete_by_exact_obligation_handles(self) -> None:
        policy = "workflow.planning.written-plan-applicability"
        snapshot = self.engine.snapshot
        result = self.engine.prepare(
            AnalysisRequest(
                snapshot,
                snapshot,
                (
                    ChangeDescriptor(
                        ChangeKind.MODIFICATION,
                        (policy,),
                        (policy,),
                        ReviewScope("whole-artifact"),
                    ),
                ),
                (),
            )
        )

        self.assertIsInstance(result, PendingResult)
        packet = result
        validate(
            SCHEMA,
            SCHEMA["$defs"]["PendingResult"],
            packet.as_contract(),
            "$packet",
        )
        while isinstance(packet, PendingResult):
            obligation = next(
                item for item in packet.obligations if item.state == "required"
            )
            self.assertEqual(
                obligation.permitted_submissions,
                ("consumer-disposition",),
            )
            packet = self.engine.resolve(
                packet.handle,
                ConsumerDispositionSubmission(
                    obligation.id,
                    "reviewed-no-change",
                    "The unchanged fixture authority needs no consumer edit.",
                    (
                        EvidenceReference(
                            "review.analysis-fixture",
                            "sha256:" + "b" * 64,
                            "repository-content",
                            "1",
                        ),
                    ),
                    obligation.fingerprint,
                ),
            )

        self.assertIsInstance(packet, CompleteResult)
        value = packet.as_contract()
        validate(
            SCHEMA,
            SCHEMA["$defs"]["CompleteResult"],
            value,
            "$report",
        )
        self.assertEqual(
            set(value["completion"]["reached_consumer_obligations"]),
            set(value["completion"]["disposition_obligations"]),
        )
        state = self.engine.inspect(InspectCall(packet.handle))
        validate(
            SCHEMA,
            SCHEMA["$defs"]["AnalysisState"],
            state.as_contract(),
            "$state",
        )
        self.assertEqual(
            state.id,
            contract_identity(SCHEMA, "AnalysisState", state.as_contract()),
        )

        reused = self.engine.prepare(
            AnalysisRequest(
                snapshot,
                snapshot,
                (
                    ChangeDescriptor(
                        ChangeKind.MODIFICATION,
                        (policy,),
                        (policy,),
                        ReviewScope("whole-artifact"),
                    ),
                ),
                (),
                packet.handle,
            )
        )
        self.assertIsInstance(reused, CompleteResult)
        self.assertEqual(reused.id, packet.id)
        self.assertEqual(value["fact_observations"], [])

    def test_one_fact_requirement_re_evaluates_every_dependent_relationship(
        self,
    ) -> None:
        policy = "workflow.planning.written-plan-applicability"
        authority = self.engine._analysis_authority()
        original = authority.policy_impact
        fact_schema = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": "fixture.analysis.facts",
                "version": 1,
                "facts": [
                    {
                        "id": "change.requires_review",
                        "semantic_revision": 1,
                        "type": "boolean",
                        "nullable": False,
                        "aliases": [],
                        "meaning": "Whether this standards change requires consumer review.",
                        "context_kind": "standards-change",
                        "answer_contract": "fact-value.v1",
                        "evidence_contract": "evidence-reference.v1",
                        "authorization_capability": "standards.analyze",
                        "prompt": "Does this standards change require consumer review?",
                    }
                ],
            }
        )
        semantics = {
            edge_id: replace(
                item,
                applicability_program=fact_schema.compile(
                    {
                        "operator": "equals",
                        "fact": "change.requires_review",
                        "value": True,
                    }
                    if item.source == policy
                    else {"operator": "always"}
                ),
            )
            for edge_id, item in original.semantics.items()
        }
        conditional = CompiledPolicyImpactSet(
            original.graph,
            semantics,
            fact_schema,
            original.node_catalog,
            original.declaration_sources,
            original.input_sources,
            original.declaration_digest,
            original.provider_contract_digest,
        )
        authority = replace(authority, policy_impact=conditional)
        request = AnalysisInput(
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (policy,),
                    (policy,),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (),
        )
        analyze_authorization = authorization("standards.analyze")
        state, first = prepare_analysis(
            authority,
            authority,
            request,
            authorizations=(analyze_authorization,),
        )

        self.assertIsInstance(first, PendingResult)
        self.assertEqual(first.obligations, ())
        self.assertEqual(len(first.fact_requirements), 1)
        requirement = first.fact_requirements[0]
        self.assertGreater(len(requirement.dependent_programs), 2)

        initial_state = state
        kernel = bind_analysis_kernel(
            authority,
            authority,
            state,
            authorizations=(analyze_authorization,),
        )
        state, second = advance_analysis(
            kernel,
            state,
            ProvideFactSubmission(
                requirement.handle,
                {"type": "boolean", "state": "known", "value": True},
                (
                    EvidenceReference(
                        "evidence.analysis-fixture",
                        "sha256:" + "c" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
            ),
            analyze_authorization,
        )

        self.assertIsInstance(second, PendingResult)
        self.assertEqual(second.fact_requirements, ())
        self.assertGreater(len(second.obligations), 1)
        inspection_cases = (
            (
                first.context.handle,
                "AnalysisContextInspectionResult",
                "context",
                first.context.as_contract(),
            ),
            (
                requirement.handle,
                "FactRequirementInspectionResult",
                "requirement",
                requirement.as_contract(),
            ),
            (
                state.observations[0].handle,
                "FactObservationInspectionResult",
                "observation",
                state.observations[0].as_contract(),
            ),
        )
        with tempfile.TemporaryDirectory() as temporary:
            store = DirectoryAnalysisStateStore(Path(temporary))
            store.put(initial_state)
            store.put(state)
            cold_engine = StandardsEngine.open_repository(
                REPO_ROOT,
                analysis_store=store,
            )
            cold_engine._policy_impact = conditional
            cold_engine._authorizations = {
                analyze_authorization.capability: analyze_authorization
            }
            for handle, definition, field, expected in inspection_cases:
                with self.subTest(definition=definition):
                    inspected = cold_engine.inspect(InspectCall(handle)).as_contract()
                    validate(SCHEMA, SCHEMA["$defs"][definition], inspected, "$inspect")
                    self.assertEqual(inspected[field], expected)
        repeated_state, repeated = advance_analysis(
            kernel,
            initial_state,
            ProvideFactSubmission(
                requirement.handle,
                {"type": "boolean", "state": "known", "value": True},
                (
                    EvidenceReference(
                        "evidence.analysis-fixture",
                        "sha256:" + "c" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
            ),
            analyze_authorization,
        )
        self.assertEqual(repeated_state.id, state.id)
        self.assertEqual(repeated.as_contract(), second.as_contract())

        false_state, false_result = prepare_analysis(
            authority,
            authority,
            request,
            authorizations=(analyze_authorization,),
        )
        false_requirement = false_result.fact_requirements[0]
        false_kernel = bind_analysis_kernel(
            authority,
            authority,
            false_state,
            authorizations=(analyze_authorization,),
        )
        false_state, false_result = advance_analysis(
            false_kernel,
            false_state,
            ProvideFactSubmission(
                false_requirement.handle,
                {"type": "boolean", "state": "known", "value": False},
                (
                    EvidenceReference(
                        "evidence.analysis-no-review",
                        "sha256:" + "e" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
            ),
            analyze_authorization,
        )
        self.assertIsInstance(false_result, CompleteResult)
        reused_state, reused_result = prepare_analysis(
            authority,
            authority,
            request,
            false_state,
            authorizations=(analyze_authorization,),
        )
        self.assertIsInstance(reused_result, CompleteResult)
        self.assertEqual(reused_result.id, false_result.id)
        self.assertEqual(
            reused_state.observations,
            false_state.observations,
        )
        changed_authority_state, changed_authority_result = prepare_analysis(
            authority,
            authority,
            request,
            false_state,
            authorizations=(
                AuthorizationReference(
                    analyze_authorization.id,
                    analyze_authorization.capability,
                    "sha256:" + "9" * 64,
                ),
            ),
        )
        self.assertIsInstance(changed_authority_result, PendingResult)
        self.assertEqual(len(changed_authority_result.fact_requirements), 1)
        self.assertEqual(changed_authority_state.observations, ())

    def test_state_identity_distinguishes_equal_work_with_different_evidence(
        self,
    ) -> None:
        policy = "workflow.planning.written-plan-applicability"
        authority = self.engine._analysis_authority()
        original = authority.policy_impact
        fact_schema = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": "fixture.analysis.identity-facts",
                "version": 1,
                "facts": [
                    {
                        "id": "change.requires_review",
                        "semantic_revision": 1,
                        "type": "boolean",
                        "nullable": False,
                        "aliases": [],
                        "meaning": "Whether consumer review is required.",
                        "context_kind": "standards-change",
                        "answer_contract": "fact-value.v1",
                        "evidence_contract": "evidence-reference.v1",
                        "authorization_capability": "standards.analyze",
                        "prompt": "Is consumer review required?",
                    }
                ],
            }
        )
        conditional = CompiledPolicyImpactSet(
            original.graph,
            {
                edge_id: replace(
                    item,
                    applicability_program=fact_schema.compile(
                        {
                            "operator": "equals",
                            "fact": "change.requires_review",
                            "value": True,
                        }
                        if item.source == policy
                        else {"operator": "always"}
                    ),
                )
                for edge_id, item in original.semantics.items()
            },
            fact_schema,
            original.node_catalog,
            original.declaration_sources,
            original.input_sources,
            original.declaration_digest,
            original.provider_contract_digest,
        )
        authority = replace(authority, policy_impact=conditional)
        request = AnalysisInput(
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (policy,),
                    (policy,),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (),
        )
        analyze = authorization("standards.analyze")
        first_state, first = prepare_analysis(
            authority, authority, request, authorizations=(analyze,)
        )
        second_state, second = prepare_analysis(
            authority, authority, request, authorizations=(analyze,)
        )
        first_requirement = first.fact_requirements[0]
        second_requirement = second.fact_requirements[0]
        first_kernel = bind_analysis_kernel(
            authority,
            authority,
            first_state,
            authorizations=(analyze,),
        )
        second_kernel = bind_analysis_kernel(
            authority,
            authority,
            second_state,
            authorizations=(analyze,),
        )
        first_state, first_result = advance_analysis(
            first_kernel,
            first_state,
            ProvideFactSubmission(
                first_requirement.handle,
                {"type": "boolean", "state": "known", "value": True},
                (
                    EvidenceReference(
                        "evidence.first",
                        "sha256:" + "1" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
            ),
            analyze,
        )
        second_state, second_result = advance_analysis(
            second_kernel,
            second_state,
            ProvideFactSubmission(
                second_requirement.handle,
                {"type": "boolean", "state": "known", "value": True},
                (
                    EvidenceReference(
                        "evidence.second",
                        "sha256:" + "2" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
            ),
            analyze,
        )
        self.assertEqual(
            tuple(item.id for item in first_result.obligations),
            tuple(item.id for item in second_result.obligations),
        )
        self.assertNotEqual(first_state.id, second_state.id)
        self.assertNotEqual(first_result.id, second_result.id)

    def test_prior_analysis_reuse_resolves_through_shared_store(self) -> None:
        store = InMemoryAnalysisStateStore()
        capabilities = (
            authorization("standards.analyze"),
            authorization("standards.review.consumer"),
            authorization("standards.review.impact"),
            authorization("standards.review.audit"),
        )
        first_engine = StandardsEngine.open_analysis(
            REPO_ROOT,
            REPO_ROOT,
            authorizations=capabilities,
            analysis_store=store,
        )
        policy = "workflow.planning.written-plan-applicability"
        request = AnalysisRequest(
            first_engine.snapshot,
            first_engine.snapshot,
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (policy,),
                    (policy,),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (),
        )
        result = first_engine.prepare(request)
        initial_packet = result
        while isinstance(result, PendingResult):
            obligation = next(
                item for item in result.obligations if item.state == "required"
            )
            result = first_engine.resolve(
                result.handle,
                ConsumerDispositionSubmission(
                    obligation.id,
                    "reviewed-no-change",
                    "The consumer remains correct.",
                    (
                        EvidenceReference(
                            "review.shared-store",
                            "sha256:" + "7" * 64,
                            "repository-content",
                            "1",
                        ),
                    ),
                    obligation.fingerprint,
                ),
            )
        second_engine = StandardsEngine.open_analysis(
            REPO_ROOT,
            REPO_ROOT,
            authorizations=capabilities,
            analysis_store=store,
        )
        seeded = second_engine.prepare(
            replace(request, prior_analysis=initial_packet.handle)
        )
        self.assertIsInstance(seeded, PendingResult)
        self.assertEqual(seeded.id, initial_packet.id)
        reused = second_engine.prepare(replace(request, prior_analysis=result.handle))
        self.assertIsInstance(reused, CompleteResult)
        self.assertEqual(reused.id, result.id)
        self.assertEqual(reused.as_contract(), result.as_contract())
        inspected = second_engine.inspect(InspectCall(reused.handle))
        self.assertEqual(inspected.id, reused.handle["id"])

    def test_analysis_resolves_in_a_new_engine_without_supersession(self) -> None:
        store = InMemoryAnalysisStateStore()
        capabilities = (
            authorization("standards.analyze"),
            authorization("standards.review.consumer"),
            authorization("standards.review.impact"),
            authorization("standards.review.audit"),
        )
        first_engine = StandardsEngine.open_analysis(
            REPO_ROOT,
            REPO_ROOT,
            authorizations=capabilities,
            analysis_store=store,
        )
        policy = "workflow.planning.written-plan-applicability"
        packet = first_engine.prepare(
            AnalysisRequest(
                first_engine.snapshot,
                first_engine.snapshot,
                (
                    ChangeDescriptor(
                        ChangeKind.MODIFICATION,
                        (policy,),
                        (policy,),
                        ReviewScope("whole-artifact"),
                    ),
                ),
                (),
            )
        )
        second_engine = StandardsEngine.open_analysis(
            REPO_ROOT,
            REPO_ROOT,
            authorizations=capabilities,
            analysis_store=store,
        )
        obligation = next(
            item for item in packet.obligations if item.state == "required"
        )
        result = second_engine.resolve(
            packet.handle,
            ConsumerDispositionSubmission(
                obligation.id,
                "reviewed-no-change",
                "The consumer remains correct.",
                (
                    EvidenceReference(
                        "review.cold-process",
                        "sha256:" + "4" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
                obligation.fingerprint,
            ),
        )
        self.assertIn(
            result.as_contract()["kind"],
            {"pending-result", "complete-result"},
        )
        repeated = first_engine.resolve(
            packet.handle,
            ConsumerDispositionSubmission(
                obligation.id,
                "reviewed-no-change",
                "The consumer remains correct.",
                (
                    EvidenceReference(
                        "review.cold-process",
                        "sha256:" + "4" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
                obligation.fingerprint,
            ),
        )
        self.assertEqual(repeated.as_contract(), result.as_contract())

    def test_analysis_reconstructs_and_advances_in_a_cold_process(self) -> None:
        capabilities = (
            authorization("standards.analyze"),
            authorization("standards.review.consumer"),
            authorization("standards.review.impact"),
            authorization("standards.review.audit"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            store_root = Path(temporary) / "states"
            tool = AgentToolFacade.open_analysis(
                REPO_ROOT,
                REPO_ROOT,
                authorizations=capabilities,
                analysis_store=DirectoryAnalysisStateStore(store_root),
            )
            policy = "workflow.planning.written-plan-applicability"
            pending = tool.prepare(
                {
                    "request": {
                        "kind": "analysis-request",
                        "base_snapshot": dict(tool.snapshot),
                        "proposed_snapshot": dict(tool.snapshot),
                        "changes": [
                            {
                                "kind": "modification",
                                "accepted_ids": [policy],
                                "proposed_ids": [policy],
                                "scope": {"kind": "whole-artifact"},
                            }
                        ],
                        "semantic_proposals": [],
                        "contract_version": 2,
                    }
                }
            )
            obligation = next(
                item for item in pending["obligations"] if item["state"] == "required"
            )
            resolve_call = {
                "analysis": pending["handle"],
                "submission": {
                    "kind": "consumer-disposition",
                    "obligation_id": obligation["id"],
                    "result": "reviewed-no-change",
                    "rationale": "The exact consumer was reviewed.",
                    "evidence": [
                        {
                            "id": "review.cold-process-persistent",
                            "digest": "sha256:" + "5" * 64,
                            "provider_contract": "repository-content",
                            "provider_contract_version": "1",
                        }
                    ],
                    "fingerprint": obligation["fingerprint"],
                },
            }
            call_path = Path(temporary) / "resolve.json"
            call_path.write_text(json.dumps(resolve_call), encoding="utf-8")
            script = """
import json
import sys
from pathlib import Path
from tools.standards_analysis.standards_analysis import AuthorizationReference
from tools.standards_engine.standards_engine import AgentToolFacade, DirectoryAnalysisStateStore

repo = Path(sys.argv[1])
store = DirectoryAnalysisStateStore(Path(sys.argv[2]))
authorizations = tuple(
    AuthorizationReference(
        f"authorization.{capability}",
        capability,
        "sha256:" + "a" * 64,
    )
    for capability in (
        "standards.analyze",
        "standards.review.consumer",
        "standards.review.impact",
        "standards.review.audit",
    )
)
tool = AgentToolFacade.open_analysis(
    repo,
    repo,
    authorizations=authorizations,
    analysis_store=store,
)
arguments = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
print(json.dumps(tool.resolve(arguments), sort_keys=True, separators=(",", ":")))
"""
            completed = subprocess.run(
                (
                    sys.executable,
                    "-c",
                    script,
                    str(REPO_ROOT),
                    str(store_root),
                    str(call_path),
                ),
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            cold_result = json.loads(completed.stdout)
            local_result = tool.resolve(resolve_call)

            self.assertEqual(cold_result, local_result)
            self.assertNotEqual(
                cold_result["handle"]["id"],
                pending["handle"]["id"],
            )

    def test_provider_claim_is_canonically_recorded_by_analysis(self) -> None:
        policy = "workflow.planning.written-plan-applicability"
        authority = conditional_authority(
            self.engine,
            (boolean_fact("change.provider-answer"),),
            {
                "operator": "equals",
                "fact": "change.provider-answer",
                "value": True,
            },
        )
        state, result = prepare_analysis(
            authority,
            authority,
            AnalysisInput(
                (
                    ChangeDescriptor(
                        ChangeKind.MODIFICATION,
                        (policy,),
                        (policy,),
                        ReviewScope("whole-artifact"),
                    ),
                ),
                (),
            ),
            authorizations=(authorization("standards.analyze"),),
            providers=(StaticFactProvider(False),),
        )
        self.assertIsInstance(result, CompleteResult)
        self.assertEqual(len(state.observations), 1)
        self.assertEqual(
            state.observations[0].value["value"],
            False,
        )

    def test_provider_unavailability_is_not_treated_as_no_observation(self) -> None:
        policy = "workflow.planning.written-plan-applicability"
        authority = conditional_authority(
            self.engine,
            (boolean_fact("change.provider-answer"),),
            {
                "operator": "equals",
                "fact": "change.provider-answer",
                "value": True,
            },
        )
        with self.assertRaisesRegex(Exception, "unavailable"):
            prepare_analysis(
                authority,
                authority,
                AnalysisInput(
                    (
                        ChangeDescriptor(
                            ChangeKind.MODIFICATION,
                            (policy,),
                            (policy,),
                            ReviewScope("whole-artifact"),
                        ),
                    ),
                    (),
                ),
                authorizations=(authorization("standards.analyze"),),
                providers=(UnavailableFactProvider(False),),
            )

    def test_decision_order_normalizes_and_dormant_observations_survive(self) -> None:
        policy = "workflow.planning.written-plan-applicability"
        authority = conditional_authority(
            self.engine,
            (
                boolean_fact("change.a-review"),
                boolean_fact("change.b-review"),
            ),
            {
                "operator": "any",
                "expressions": [
                    {
                        "operator": "equals",
                        "fact": "change.a-review",
                        "value": True,
                    },
                    {
                        "operator": "equals",
                        "fact": "change.b-review",
                        "value": True,
                    },
                ],
            },
        )
        analyze = authorization("standards.analyze")
        request = AnalysisInput(
            (
                ChangeDescriptor(
                    ChangeKind.MODIFICATION,
                    (policy,),
                    (policy,),
                    ReviewScope("whole-artifact"),
                ),
            ),
            (),
        )

        def transition(order, values):
            state, result = prepare_analysis(
                authority,
                authority,
                request,
                authorizations=(analyze,),
            )
            kernel = bind_analysis_kernel(
                authority,
                authority,
                state,
                authorizations=(analyze,),
            )
            for fact in order:
                requirement = next(
                    item for item in result.fact_requirements if item.fact == fact
                )
                state, result = advance_analysis(
                    kernel,
                    state,
                    ProvideFactSubmission(
                        requirement.handle,
                        {
                            "type": "boolean",
                            "state": "known",
                            "value": values[fact],
                        },
                        (
                            EvidenceReference(
                                f"evidence.{fact}",
                                "sha256:"
                                + ("1" if fact.endswith("a-review") else "2") * 64,
                                "repository-content",
                                "1",
                            ),
                        ),
                    ),
                    analyze,
                )
            return state, result

        left, left_result = transition(
            ("change.a-review", "change.b-review"),
            {"change.a-review": False, "change.b-review": False},
        )
        right, right_result = transition(
            ("change.b-review", "change.a-review"),
            {"change.a-review": False, "change.b-review": False},
        )
        self.assertEqual(left.id, right.id)
        self.assertEqual(left_result.as_contract(), right_result.as_contract())

        dormant, dormant_result = transition(
            ("change.b-review", "change.a-review"),
            {"change.a-review": True, "change.b-review": False},
        )
        self.assertIsInstance(dormant_result, PendingResult)
        self.assertEqual(dormant_result.fact_requirements, ())
        self.assertEqual(len(dormant.observations), 2)

    def test_short_circuited_fact_is_not_stored_as_derived_state(self) -> None:
        policy = "workflow.planning.written-plan-applicability"
        authority = conditional_authority(
            self.engine,
            (
                boolean_fact("change.a-review"),
                boolean_fact("change.b-review"),
            ),
            {
                "operator": "any",
                "expressions": [
                    {
                        "operator": "equals",
                        "fact": "change.a-review",
                        "value": True,
                    },
                    {
                        "operator": "equals",
                        "fact": "change.b-review",
                        "value": True,
                    },
                ],
            },
        )
        analyze = authorization("standards.analyze")
        state, pending = prepare_analysis(
            authority,
            authority,
            AnalysisInput(
                (
                    ChangeDescriptor(
                        ChangeKind.MODIFICATION,
                        (policy,),
                        (policy,),
                        ReviewScope("whole-artifact"),
                    ),
                ),
                (),
            ),
            authorizations=(analyze,),
        )
        self.assertEqual(
            tuple(sorted(item.fact for item in pending.fact_requirements)),
            ("change.a-review", "change.b-review"),
        )
        selected = next(
            item for item in pending.fact_requirements if item.fact == "change.a-review"
        )
        kernel = bind_analysis_kernel(
            authority,
            authority,
            state,
            authorizations=(analyze,),
        )
        state, result = advance_analysis(
            kernel,
            state,
            ProvideFactSubmission(
                selected.handle,
                {"type": "boolean", "state": "known", "value": True},
                (
                    EvidenceReference(
                        "evidence.short-circuit",
                        "sha256:" + "5" * 64,
                        "repository-content",
                        "1",
                    ),
                ),
            ),
            analyze,
        )
        self.assertIsInstance(result, PendingResult)
        self.assertEqual(result.fact_requirements, ())
        self.assertEqual(
            tuple(str(item.requirement["id"]) for item in state.observations),
            (selected.id,),
        )
        self.assertNotIn("current_requirements", state.as_contract())
        self.assertNotIn("requirement_history", state.as_contract())

    def test_agent_adapter_uses_structured_prepare_and_resolve(self) -> None:
        capabilities = (
            authorization("standards.analyze"),
            authorization("standards.review.consumer"),
            authorization("standards.review.impact"),
            authorization("standards.review.audit"),
        )
        tool = AgentToolFacade.open_analysis(
            REPO_ROOT,
            REPO_ROOT,
            authorizations=capabilities,
        )
        policy = "workflow.planning.written-plan-applicability"
        result = tool.prepare(
            {
                "request": {
                    "kind": "analysis-request",
                    "base_snapshot": dict(tool.snapshot),
                    "proposed_snapshot": dict(tool.snapshot),
                    "changes": [
                        {
                            "kind": "modification",
                            "accepted_ids": [policy],
                            "proposed_ids": [policy],
                            "scope": {"kind": "whole-artifact"},
                        }
                    ],
                    "semantic_proposals": [],
                    "contract_version": 2,
                }
            }
        )

        while result["kind"] == "pending-result":
            obligation = next(
                item for item in result["obligations"] if item["state"] == "required"
            )
            result = tool.resolve(
                {
                    "analysis": result["handle"],
                    "submission": {
                        "kind": "consumer-disposition",
                        "obligation_id": obligation["id"],
                        "result": "reviewed-no-change",
                        "rationale": "The fixture authority is unchanged.",
                        "evidence": [
                            {
                                "id": "review.agent-analysis-fixture",
                                "digest": "sha256:" + "d" * 64,
                                "provider_contract": "repository-content",
                                "provider_contract_version": "1",
                            }
                        ],
                        "fingerprint": obligation["fingerprint"],
                    },
                }
            )

        self.assertEqual(result["kind"], "complete-result")
        self.assertTrue(result["completion"]["authorization_valid"])

    def test_agent_adapter_completes_real_addition_and_removal_snapshots(self) -> None:
        capabilities = (
            authorization("standards.analyze"),
            authorization("standards.review.consumer"),
            authorization("standards.review.impact"),
            authorization("standards.review.audit"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            proposed_root = fixture_repository(Path(temporary), "addition")
            tool = AgentToolFacade.open_analysis(
                REPO_ROOT,
                proposed_root,
                authorizations=capabilities,
            )
            proposed_snapshot = next(
                item for item in tool.snapshots if item != tool.snapshot
            )
            policy = "workflow.planning.fixture-addition"
            read = tool.query(
                {
                    "snapshot": proposed_snapshot,
                    "request": {"kind": "read", "target": policy},
                }
            )
            inspected = tool.inspect({"handle": read["policy"]["handle"]})
            result = tool.prepare(
                {
                    "request": {
                        "kind": "analysis-request",
                        "base_snapshot": dict(tool.snapshot),
                        "proposed_snapshot": dict(proposed_snapshot),
                        "changes": [
                            {
                                "kind": "addition",
                                "accepted_ids": [],
                                "proposed_ids": [policy],
                                "proposed_module": "workflow.planning",
                                "scope": {"kind": "whole-artifact"},
                            }
                        ],
                        "semantic_proposals": [
                            {
                                "policy": policy,
                                "accepted_semantic_revision": None,
                                "proposed_semantic_revision": 1,
                                "intent": "Exercise a complete typed addition.",
                                "structural_digest": inspected["structural_digest"],
                            }
                        ],
                        "contract_version": 2,
                    }
                }
            )

            self.assertEqual(result["kind"], "pending-result")
            self.assertEqual(
                [item["change_kind"] for item in result["changed_units"]],
                ["addition"],
            )
            obligation = result["obligations"][0]
            self.assertEqual(obligation["kind"], "audit-coverage")
            result = tool.resolve(
                {
                    "analysis": result["handle"],
                    "submission": {
                        "kind": "coverage-attestation",
                        "obligation_id": obligation["id"],
                        "attestation": coverage_attestation(obligation),
                    },
                }
            )
            self.assertEqual(result["kind"], "complete-result")

        with tempfile.TemporaryDirectory() as temporary:
            proposed_root = fixture_repository(Path(temporary), "removal")
            tool = AgentToolFacade.open_analysis(
                REPO_ROOT,
                proposed_root,
                authorizations=capabilities,
            )
            proposed_snapshot = next(
                item for item in tool.snapshots if item != tool.snapshot
            )
            policy = "workflow.planning.projection-completeness"
            result = tool.prepare(
                {
                    "request": {
                        "kind": "analysis-request",
                        "base_snapshot": dict(tool.snapshot),
                        "proposed_snapshot": dict(proposed_snapshot),
                        "changes": [
                            {
                                "kind": "removal",
                                "accepted_ids": [policy],
                                "proposed_ids": [],
                                "accepted_module": "workflow.planning",
                                "scope": {"kind": "whole-artifact"},
                            }
                        ],
                        "semantic_proposals": [],
                        "contract_version": 2,
                    }
                }
            )

            self.assertEqual(result["kind"], "pending-result")
            self.assertEqual(
                [item["change_kind"] for item in result["changed_units"]],
                ["removal"],
            )
            obligation = next(
                item
                for item in result["obligations"]
                if item["kind"] == "consumer-review"
            )
            stale_fingerprint = json.loads(json.dumps(obligation["fingerprint"]))
            stale_fingerprint["dependencies"][0]["digest"] = "sha256:" + "8" * 64
            rejected = tool.resolve(
                {
                    "analysis": result["handle"],
                    "submission": {
                        "kind": "consumer-disposition",
                        "obligation_id": obligation["id"],
                        "result": "reviewed-no-change",
                        "rationale": "This submission has stale dependencies.",
                        "evidence": [
                            {
                                "id": "review.typed-removal-stale",
                                "digest": "sha256:" + "9" * 64,
                                "provider_contract": "repository-content",
                                "provider_contract_version": "1",
                            }
                        ],
                        "fingerprint": stale_fingerprint,
                    },
                }
            )
            self.assertEqual(rejected["code"], "SUBMISSION.CONTEXT_MISMATCH")

            result = tool.resolve(
                {
                    "analysis": result["handle"],
                    "submission": {
                        "kind": "consumer-disposition",
                        "obligation_id": obligation["id"],
                        "result": "reviewed-no-change",
                        "rationale": "The accepted consumer was reviewed.",
                        "evidence": [
                            {
                                "id": "review.typed-removal-complete",
                                "digest": "sha256:" + "b" * 64,
                                "provider_contract": "repository-content",
                                "provider_contract_version": "1",
                            }
                        ],
                        "fingerprint": obligation["fingerprint"],
                    },
                }
            )
            self.assertEqual(result["kind"], "complete-result")


if __name__ == "__main__":
    unittest.main()
