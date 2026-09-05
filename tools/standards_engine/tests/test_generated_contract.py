from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tomllib
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools.standards_analysis.standards_analysis import (
    AuthorizationClaim,
    AuthorizationRequest,
    EvidenceReference,
)
from tools.standards_contracts.standards_contracts import (
    compile_contracts,
    render_repository_projections,
)
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as generated


REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO_ROOT / "tools/standards_engine/contracts/a1-contract.schema.json"
INTERFACE_PATH = REPO_ROOT / "tools/standards_engine/contracts/a1-interface.toml"


def _canonical_contracts() -> tuple[dict[str, object], dict[str, object]]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    with INTERFACE_PATH.open("rb") as source:
        interface = tomllib.load(source)
    return schema, interface


class GeneratedContractTest(unittest.TestCase):
    def test_coverage_read_is_scoped_optional_and_uses_repository_authority(self):
        from tools.standards_analysis.standards_analysis import (
            RepositoryCoverageDecisions,
            coverage_requirement_id,
        )
        from tools.standards_engine.standards_engine.tools import _contracts

        with StandardsEngine.open_repository(REPO_ROOT, durable=False) as engine:
            facade = AgentToolFacade(engine, _contracts(REPO_ROOT))
            created = facade.create_snapshot({"kind": "create-snapshot"})
            self.assertEqual(created["kind"], "create-snapshot-result", created)
            handle = created["snapshot"]["snapshot"]
            snapshot = generated.SnapshotHandle.from_value(handle)
            compiled = engine._compiled_snapshot(engine._snapshot_id(snapshot))
            units = compiled.corpus.policy_unit_corpus.for_module("workflow.planning")
            selected = units[0].id
            # Exercise the read adapter against both authoritative decisions.
            authority = RepositoryCoverageDecisions({selected: {}}, {}, ())
            with mock.patch.object(
                engine,
                "_compiled_snapshot",
                return_value=replace(compiled, repository_coverage=authority),
            ):
                query = {
                    "snapshot": handle,
                    "request": {
                        "kind": "read",
                        "target": "workflow.planning",
                    },
                }
                self.assertNotIn("coverage", facade.query(query))
                query["request"]["include_coverage"] = False
                self.assertNotIn("coverage", facade.query(query))
                query["request"]["include_coverage"] = True
                result = facade.query(query)
                self.assertEqual(result["kind"], "read-result", result)
                subjects = result["coverage"]["subjects"]
                self.assertEqual(
                    [s["subject"] for s in subjects], sorted(u.id for u in units)
                )
                for item in subjects:
                    subject = item["subject"]
                    self.assertEqual(
                        item["requirement_id"],
                        coverage_requirement_id(
                            compiled.coverage.requirements[subject],
                            compiled.coverage.views[subject],
                        ),
                    )
                    self.assertEqual(
                        item["status"],
                        "current-attestation"
                        if subject == selected
                        else "review-required",
                    )
                query["request"]["target"] = selected
                self.assertEqual(
                    facade.query(query)["coverage"]["subjects"],
                    [item for item in subjects if item["subject"] == selected],
                )
                unregistered = next(
                    module.module_id
                    for module in compiled.corpus.modules
                    if not compiled.corpus.policy_unit_corpus.for_module(
                        module.module_id
                    )
                )
                query["request"]["target"] = unregistered
                self.assertEqual(facade.query(query)["coverage"], {"subjects": []})

    def test_verification_is_exposed_without_publication_and_refresh_is_explicit(self):
        from tools.standards_verifier.standards_verifier import (
            CompleteVerificationResult,
        )
        from tools.standards_engine.standards_engine.tools import _contracts

        with StandardsEngine.open_repository(REPO_ROOT, durable=False) as engine:
            facade = AgentToolFacade(engine, _contracts(REPO_ROOT))
            with (
                mock.patch.object(
                    engine,
                    "_application_verifier",
                    return_value=CompleteVerificationResult(()),
                ) as verify,
                mock.patch(
                    "tools.standards_engine.standards_engine.engine.write_suite_input_projection"
                ) as refresh,
                mock.patch.object(engine._repository, "publish_candidate") as publish,
            ):
                result = facade.verify_repository(
                    {"kind": "verify-repository", "refresh_verification_inputs": False}
                )
                self.assertTrue(result["verification"]["passed"])
                verify.assert_called_once_with(REPO_ROOT)
                refresh.assert_not_called()
                publish.assert_not_called()
                # A low-level caller without authorization cannot refresh inputs.
                denied = facade.verify_repository(
                    {"kind": "verify-repository", "refresh_verification_inputs": True}
                )
                self.assertEqual(denied["kind"], "rejected-result")
                refresh.assert_not_called()

    def test_router_read_exposes_editable_definitions_only_when_requested(self):
        from tools.standards_engine.standards_engine.tools import _contracts

        with StandardsEngine.open_repository(REPO_ROOT, durable=False) as engine:
            facade = AgentToolFacade(engine, _contracts(REPO_ROOT))
            created = facade.create_snapshot({"kind": "create-snapshot"})
            self.assertEqual(created["kind"], "create-snapshot-result", created)
            query = {
                "snapshot": created["snapshot"]["snapshot"],
                "request": {"kind": "read", "target": "router"},
            }
            plain = facade.query(query)
            self.assertEqual(plain["kind"], "read-result", plain)
            self.assertNotIn("routing", plain)
            query["request"]["include_routing"] = True
            query["request"]["include_coverage"] = True
            detailed = facade.query(query)
            self.assertEqual(detailed["kind"], "read-result", detailed)
            self.assertTrue(detailed["routing"]["rules"])
            self.assertTrue(detailed["routing"]["facts"])
            contracts = _contracts(REPO_ROOT)
            for rule in detailed["routing"]["rules"]:
                contracts.validate(
                    "PutRoutingRuleEdit",
                    {
                        "kind": "put-routing-rule",
                        "rule": rule,
                        "rationale": "Use the Engine's editable routing definition.",
                    },
                )
            for fact in detailed["routing"]["facts"]:
                contracts.validate(
                    "PutRoutingFactEdit",
                    {
                        "kind": "put-routing-fact",
                        "fact": fact,
                        "rationale": "Use the Engine's editable fact definition.",
                    },
                )

            rule = dict(
                detailed["routing"]["rules"][0],
                when={"operator": "always"},
                condition="Exercise authoring | verify the public round trip.",
            )
            evidence = {
                "id": "CORE-STANDARDS.md",
                "digest": "sha256:"
                + hashlib.sha256(
                    (REPO_ROOT / "CORE-STANDARDS.md").read_bytes()
                ).hexdigest(),
                "provider_contract": "repository-content",
                "provider_contract_version": "1",
            }
            proposed = facade.create_proposal(
                {
                    "kind": "create-proposal",
                    "base_snapshot": query["snapshot"],
                    "change_set": {
                        "purpose": {
                            "summary": "Test routing authoring",
                            "rationale": "Read, edit, and inspect routing through the public Interface.",
                            "evidence": [evidence],
                        },
                        "edits": [
                            {
                                "kind": "put-routing-rule",
                                "rule": rule,
                                "rationale": "Exercise an unconditional route.",
                            }
                        ],
                    },
                }
            )
            self.assertEqual(proposed["kind"], "create-proposal-result", proposed)
            draft = facade.query_proposal(
                {
                    "revision": proposed["revision"],
                    "request": query["request"],
                }
            )
            self.assertEqual(draft["kind"], "proposal-read-result", draft)
            self.assertEqual(
                [item["subject"] for item in draft["coverage"]["subjects"]],
                [item["subject"] for item in detailed["coverage"]["subjects"]],
            )
            observed = next(
                item for item in draft["routing"]["rules"] if item["id"] == rule["id"]
            )
            self.assertEqual(observed["when"], {"operator": "always"})
            self.assertEqual(observed["condition"], rule["condition"])

    def test_local_facade_binds_always_allow_authorization(self) -> None:
        engine = SimpleNamespace(close=lambda: None)
        with mock.patch.object(
            StandardsEngine, "open_repository", return_value=engine
        ) as open_repository:
            facade = AgentToolFacade.open_repository(REPO_ROOT)

        self.assertIs(facade._engine, engine)
        context = open_repository.call_args.kwargs["execution_context"]
        identifier = "CORE-STANDARDS.md"
        content = (REPO_ROOT / identifier).read_bytes()
        reference = EvidenceReference(
            identifier,
            "sha256:" + hashlib.sha256(content).hexdigest(),
            "repository-content",
            "1",
        )
        request = AuthorizationRequest(
            "consumer-disposition",
            "obligation",
            "obligation:local",
            "standards.review.consumer",
            (reference,),
        )

        claim = context.authorization.authorize(request)

        self.assertIsInstance(claim, AuthorizationClaim)
        self.assertEqual(claim.action, request.action)
        self.assertEqual(claim.subject_kind, request.subject_kind)
        self.assertEqual(claim.subject_id, request.subject_id)
        self.assertEqual(claim.capability, request.capability)
        self.assertEqual(claim.submission_evidence[0].content, content)
        self.assertEqual(claim.revocation_state, "not-revoked")
        self.assertEqual(claim.decision, "allow")

    def test_local_evidence_rejects_missing_files_and_wrong_digests(self):
        from tools.standards_engine.standards_engine.tools import (
            LocalAlwaysAllowAuthorizer,
        )
        from tools.standards_analysis.standards_analysis import (
            AnalysisError,
            AuthorizationUnavailable,
        )

        authorizer = LocalAlwaysAllowAuthorizer(REPO_ROOT)
        for identifier in ("missing-review-evidence.md", "../outside.md"):
            reference = EvidenceReference(
                identifier, "sha256:" + "0" * 64, "repository-content", "1"
            )
            outcome = authorizer.authorize(
                AuthorizationRequest(
                    "review-proposal",
                    "proposal",
                    "example",
                    "standards.review.consumer",
                    (reference,),
                )
            )
            self.assertIsInstance(outcome, AuthorizationUnavailable)
        reference = EvidenceReference(
            "CORE-STANDARDS.md", "sha256:" + "0" * 64, "repository-content", "1"
        )
        with self.assertRaises(AnalysisError) as caught:
            authorizer.authorize(
                AuthorizationRequest(
                    "review-proposal",
                    "proposal",
                    "example",
                    "standards.review.consumer",
                    (reference,),
                )
            )
        self.assertEqual(
            caught.exception.failure.code, "ANALYSIS.EVIDENCE_DIGEST_MISMATCH"
        )

    def test_interface_operations_bind_generated_calls_results_and_facade(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        facade = AgentToolFacade(object(), contracts)
        expected_inputs = {
            "verify_repository": generated.VerifyRepositoryCall,
            "verify_proposal": generated.VerifyProposalCall,
            "create_snapshot": generated.CreateSnapshotCall,
            "find_snapshots": generated.FindSnapshotsCall,
            "delete_snapshot": generated.DeleteSnapshotCall,
            "undelete_snapshot": generated.UndeleteSnapshotCall,
            "query": generated.QueryCall,
            "prepare": generated.PrepareCall,
            "resolve": generated.ResolveCall,
            "inspect": generated.InspectCall,
            "create_proposal": generated.CreateProposalCall,
            "find_proposals": generated.FindProposalsCall,
            "revise_proposal": generated.ReviseProposalCall,
            "query_proposal": generated.QueryProposalCall,
            "analyze_proposal": generated.AnalyzeProposalCall,
            "review_proposal": generated.ReviewProposalCall,
            "apply_proposal": generated.ApplyProposalCall,
            "recover_application": generated.RecoverApplicationCall,
        }

        for operation in contracts.interface.operations:
            with self.subTest(operation=operation.id):
                self.assertIs(
                    getattr(generated, operation.input_definition),
                    expected_inputs[operation.id],
                )
                self.assertTrue(callable(getattr(facade, operation.id)))
                self.assertEqual(facade._operation(operation.id), operation)
                for definition in operation.result_definitions:
                    self.assertIn(definition, generated.DEFINITION_METADATA)

        class WrongQueryResult:
            __definition__ = "CompleteResult"

            @staticmethod
            def as_contract() -> dict[str, object]:
                return {"kind": "complete-result"}

        with self.assertRaisesRegex(RuntimeError, "outside the query result algebra"):
            facade._result("query", WrongQueryResult())

    def test_prepare_facade_passes_the_complete_generated_call(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        observed: list[object] = []
        rejected = generated.RejectedResult(
            "rejected-result",
            "ANALYSIS.TEST",
            "unavailable",
            "test result",
            {},
            (),
        )
        engine = SimpleNamespace(
            prepare=lambda call: observed.append(call) or rejected,
        )
        facade = AgentToolFacade(engine, contracts)
        examples = json.loads(
            (
                REPO_ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
            ).read_text(encoding="utf-8")
        )["examples"]
        arguments = next(
            item["value"] for item in examples if item["definition"] == "PrepareCall"
        )

        result = facade.prepare(arguments)

        self.assertEqual(result["code"], "ANALYSIS.TEST")
        self.assertEqual(len(observed), 1)
        self.assertIsInstance(observed[0], generated.PrepareCall)

    def test_generated_contract_projections_are_current(self) -> None:
        completed = subprocess.run(
            (
                sys.executable,
                "-P",
                "-m",
                "tools.standards_contracts.standards_contracts.projection",
                "--check",
            ),
            cwd=Path("/tmp"),
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPATH": str(REPO_ROOT),
            },
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)

    def test_compiler_owns_the_complete_public_definition_closure(self) -> None:
        schema, interface = _canonical_contracts()
        compiled = compile_contracts(schema, interface)

        self.assertEqual(set(compiled.reachable_definitions), set(schema["$defs"]))
        self.assertEqual(
            set(generated.DEFINITION_METADATA),
            set(compiled.reachable_definitions),
        )
        projections = render_repository_projections()
        for path, projection in projections.items():
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertEqual(path.read_text(encoding="utf-8"), projection)

    def test_generated_native_models_decode_complete_v20_values(self) -> None:
        request_value = {"kind": "read", "target": "workflow.planning"}
        request = generated.decode_contract("QueryRequest", request_value)
        self.assertIsInstance(request, generated.ReadRequest)
        self.assertEqual(request.as_contract(), request_value)

        result_value = {
            "kind": "rejected-result",
            "code": "AUTHORITY.UNAVAILABLE",
            "outcome": "unavailable",
            "message": "The requested immutable authority is unavailable.",
            "details": {},
            "next_operations": [],
        }
        result = generated.decode_contract("RejectedResult", result_value)
        self.assertIsInstance(result, generated.RejectedResult)
        self.assertEqual(result.as_contract(), result_value)

        with self.assertRaises(ValueError):
            generated.ReadRequest.from_value({"kind": "read"})

        recovery_value = {
            "kind": "recover-application",
            "readiness": {
                "kind": "readiness-handle",
                "id": "readiness:sha256:" + "d" * 64,
                "schema_version": 1,
            },
        }
        recovery = generated.RecoverApplicationCall.from_value(recovery_value)
        self.assertEqual(recovery.as_contract(), recovery_value)
        with self.assertRaises(ValueError):
            generated.RecoverApplicationCall.from_value(
                {**recovery_value, "application": "caller-selected"}
            )

    def test_review_call_requires_exactly_three_decisions(self) -> None:
        examples = json.loads(
            (
                REPO_ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
            ).read_text(encoding="utf-8")
        )["examples"]
        call = next(
            item["value"]
            for item in examples
            if item["definition"] == "ReviewProposalCall"
        )

        generated.ReviewProposalCall.from_value(call)
        with self.assertRaises(ValueError):
            generated.ReviewProposalCall.from_value(
                {
                    **call,
                    "decisions": [
                        *call["decisions"],
                        {
                            **call["decisions"][0],
                            "rationale": "A duplicate owner cannot add a fourth decision.",
                        },
                    ],
                }
            )

    def test_agent_tools_are_the_exact_compiler_projection(self) -> None:
        tools_path = (
            REPO_ROOT / "tools/standards_engine/contracts/generated/agent-tools.json"
        )
        projected = render_repository_projections()[tools_path]
        self.assertEqual(tools_path.read_text(encoding="utf-8"), projected)

    def test_authored_examples_satisfy_the_public_contract(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        path = REPO_ROOT / "tools/standards_engine/contracts/examples/a1-examples.json"
        corpus = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(corpus["schema_version"], 2)
        self.assertEqual(contracts.interface.interface_schema_version, 23)
        self.assertEqual(
            corpus["interface_schema_version"],
            contracts.interface.interface_schema_version,
        )
        names = [example["name"] for example in corpus["examples"]]
        self.assertTrue(names)
        self.assertEqual(len(names), len(set(names)))
        for example in corpus["examples"]:
            with self.subTest(example=example["name"]):
                self.assertEqual(set(example), {"name", "definition", "value"})
                contracts.validate(example["definition"], example["value"])

    def test_identity_fixtures_use_valid_public_handle_versions(self) -> None:
        schema, interface = _canonical_contracts()
        contracts = compile_contracts(schema, interface)
        path = REPO_ROOT / "tools/standards_engine/contracts/identity-fixtures.json"
        corpus = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(corpus["schema_version"], 2)
        self.assertEqual(corpus["identity_encoding_version"], 2)
        handles = corpus["public_handles"]
        self.assertEqual(
            {fixture["definition"] for fixture in handles},
            {
                "SnapshotHandle",
                "AnalysisHandle",
                "SnapshotChildHandle",
                "AnalysisChildHandle",
                "ProposalHandle",
                "ProposalRevisionHandle",
                "ReadinessHandle",
                "ApplicationHandle",
            },
        )
        for fixture in handles:
            with self.subTest(handle=fixture["name"]):
                contracts.validate(fixture["definition"], fixture["value"])


if __name__ == "__main__":
    unittest.main()
