"""Admitted intent survives failed writes and explicit cold recovery.

Focused faults use real proposal, candidate and SQLite owners; their verifier
substitute is not the system qualification. The cold MCP test in
``test_consumer_publication`` executes the actual complete verifier.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from tools.standards_engine.standards_engine import AgentToolFacade
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.tests.test_agent_workflow import (
    decisions, prepare_repository, reference_change,
)
from tools.standards_verifier.standards_verifier import CompleteVerificationResult


class RecoveryContractTests(unittest.TestCase):
    def test_focused_and_native_calls_accept_explicit_completion(self):
        readiness = {"kind": "readiness-handle", "id": "readiness:sha256:" + "1" * 64,
                     "schema_version": 1}
        # Use the canonical example shape for readiness rather than a stored ID.
        for model, raw in (
            (c.RecoverCall, {"context": readiness}),
            (c.RecoverApplicationCall, {"kind": "recover-application", "readiness": readiness}),
        ):
            with self.subTest(model=model.__name__):
                value = model.from_value({**raw, "action": "complete-publication"})
                self.assertEqual(value.as_contract()["action"], "complete-publication")


class PublicationRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="admitted-recovery-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repository"
        prepare_repository(self.root)
        self.author = AgentToolFacade.open_repository(self.root, purpose="authoring")
        self.addCleanup(lambda: self.author.close())
        self.engine = self.author._engine
        self.verification = mock.patch.object(
            self.engine, "_application_verifier",
            return_value=CompleteVerificationResult((), None, 0),
        ).start()
        self.addCleanup(mock.patch.stopall)
        proposed = self.author.propose({"change_set": reference_change(self.root, "recovery")})
        self.assertEqual(proposed.get("status"), "complete", proposed)
        ready = self.author.review({"context": proposed["context"], "decisions": decisions(self.root)})
        self.assertEqual(ready.get("status"), "ready", ready)
        self.context = ready["context"]
        self.expected = self.engine._repository.branch_revision("main")
        self.lock = self.root / ".git/refs/heads/main.lock"
        self.lock.write_bytes(b"owned test lock\n")
        failed = self.author.apply({"context": self.context})
        self.assertEqual(failed.get("status"), "recovery-required", failed)
        self.failed = failed
        self.application = self.engine._authoring.read_selected_application(self.context["id"])
        self.assertEqual(self.engine._repository.branch_revision("main"), self.expected)

    def test_observe_then_complete_preserves_the_selected_application(self):
        observed = self.author.recover({"context": self.context})
        self.assertEqual(observed["status"], "recovery-required", observed)
        self.assertEqual(observed["outcome"]["code"], "APPLICATION.RECOVERY_TARGET_UNCERTAIN")
        self.lock.unlink()
        completed = self.author.recover({"context": self.context, "action": "complete-publication"})
        self.assertEqual(completed.get("status"), "applied", completed)
        self.assertEqual(completed["outcome"]["application"]["id"], self.application.application_id)
        self.assertEqual(self.engine._repository.branch_revision("main"), self.application.candidate)
        self.assertEqual(self.engine._authoring.read_selected_application(self.context["id"]), self.application)

    def test_native_completion_and_repeated_recovery_are_idempotent(self):
        self.lock.unlink()
        completed = self.author.recover_application({
            "kind": "recover-application", "readiness": self.context,
            "action": "complete-publication",
        })
        self.assertEqual(completed["status"], "applied", completed)
        counts = self.engine._snapshots._store.counts()
        with mock.patch.object(self.engine._repository, "publish_candidate") as publish:
            repeated = self.author.recover({"context": self.context, "action": "complete-publication"})
            self.assertEqual(repeated["status"], "applied", repeated)
            publish.assert_not_called()
        self.assertEqual(self.engine._snapshots._store.counts(), counts)
        rejected = self.author.apply({"context": self.context})
        self.assertEqual(rejected["code"], "WORKFLOW.OPERATION_NOT_AVAILABLE")

    def test_failed_write_remains_recoverable_with_bounded_git_diagnostics(self):
        details = self.failed["outcome"]["details"]
        self.assertEqual(details["git_operation"], "update-ref")
        self.assertEqual(details["git_exit_code"], 128)
        self.assertEqual(details["git_reason"], "path-exists")
        self.assertEqual(details["git_stderr_excerpt"], "File exists")
        self.assertNotIn(str(self.root), str(self.failed))
        self.assertNotIn("remove the file manually", str(self.failed))
        with mock.patch.object(self.engine._repository, "publish_candidate",
                               wraps=self.engine._repository.publish_candidate) as publish:
            failed = self.author.recover({"context": self.context, "action": "complete-publication"})
            self.assertEqual(failed["status"], "recovery-required", failed)
            self.assertEqual(publish.call_count, 1)
        self.assertEqual(self.engine._authoring.read_selected_application(self.context["id"]), self.application)
        self.assertIsNone(self.engine._authoring.application_outcome(self.application))

    def test_default_observation_uses_no_candidate_or_publication(self):
        with (mock.patch.object(self.engine, "_application_candidate") as candidate,
              mock.patch.object(self.engine._repository, "publish_candidate") as publish):
            result = self.author.recover({"context": self.context})
            self.assertEqual(result["status"], "recovery-required", result)
            candidate.assert_not_called()
            publish.assert_not_called()

    def test_diverged_target_is_preserved_without_reconstruction(self):
        self.lock.unlink()
        tree = subprocess.check_output(["git", "rev-parse", "main^{tree}"], cwd=self.root).decode().strip()
        competing = subprocess.check_output([
            "git", "-c", "user.name=Recovery Test", "-c", "user.email=recovery@example.invalid",
            "commit-tree", tree, "-p", self.expected.oid, "-m", "test: competing revision",
        ], cwd=self.root).decode().strip()
        subprocess.run(["git", "update-ref", "refs/heads/main", competing, self.expected.oid], cwd=self.root, check=True)
        with mock.patch.object(self.engine, "_application_candidate") as candidate:
            result = self.author.recover({"context": self.context, "action": "complete-publication"})
            self.assertEqual(result["outcome"]["code"], "APPLICATION.RECOVERY_TARGET_DIVERGED", result)
            candidate.assert_not_called()
        self.assertEqual(self.engine._repository.branch_revision("main").oid, competing)
        self.assertIsNone(self.engine._authoring.application_outcome(self.application))

    def test_reconstructed_candidate_mismatch_preserves_admission(self):
        from contextlib import contextmanager
        from tools.repository_git.repository_git import RepositoryRevision
        original = self.engine._application_candidate

        @contextmanager
        def changed_candidate(*args):
            with original(*args) as candidate:
                yield replace(candidate, revision=RepositoryRevision("f" * 40))

        self.lock.unlink()
        with (mock.patch.object(self.engine, "_application_candidate", side_effect=changed_candidate),
              mock.patch.object(self.engine._repository, "publish_candidate") as publish):
            result = self.author.recover({"context": self.context, "action": "complete-publication"})
            self.assertEqual(result["outcome"]["details"]["cause_code"], "APPLICATION.RECOVERY_CANDIDATE_MISMATCH", result)
            publish.assert_not_called()
        self.assertEqual(self.engine._authoring.read_selected_application(self.context["id"]), self.application)

    def test_current_publication_authorization_is_required_and_rechecked(self):
        from tools.standards_analysis.standards_analysis import AuthorizationDenied
        delegate = self.engine._execution_context.authorization

        class SelectiveAuthorizer:
            contract = delegate.contract
            denied = False
            requests = []

            def authorize(self, request):
                self.requests.append(request.capability)
                if self.denied and request.capability == "standards.proposal.apply":
                    return AuthorizationDenied("Current application permission is absent.")
                return delegate.authorize(request)

        authorizer = SelectiveAuthorizer()
        self.engine._execution_context = replace(self.engine._execution_context, authorization=authorizer)
        self.lock.unlink()
        for late in (False, True):
            with self.subTest(revoked_after_verification=late):
                authorizer.denied = not late
                def verify(root):
                    authorizer.denied = True
                    return CompleteVerificationResult((), None, 0)
                self.verification.side_effect = verify if late else None
                with mock.patch.object(self.engine._repository, "publish_candidate") as publish:
                    result = self.author.recover({"context": self.context, "action": "complete-publication"})
                    self.assertEqual(result["status"], "recovery-required", result)
                    self.assertEqual(result["outcome"]["details"]["cause_code"], "ANALYSIS.UNAUTHORIZED", result)
                    publish.assert_not_called()
                self.assertEqual(self.engine._repository.branch_revision("main"), self.expected)
        self.assertIn("standards.proposal.recover", authorizer.requests)
        self.assertIn("standards.proposal.apply", authorizer.requests)

    def test_failed_verification_preserves_the_selected_application(self):
        self.lock.unlink()
        self.verification.side_effect = OSError("private verifier location")
        with mock.patch.object(self.engine._repository, "publish_candidate") as publish:
            result = self.author.recover({"context": self.context, "action": "complete-publication"})
            self.assertEqual(result["status"], "recovery-required", result)
            self.assertEqual(result["outcome"]["details"]["cause_code"], "APPLICATION.VERIFICATION_UNAVAILABLE")
            self.assertNotIn("private verifier location", str(result))
            publish.assert_not_called()

    def test_outcome_persistence_failure_recovers_without_republication(self):
        from tools.standards_snapshots.standards_snapshots import SnapshotError, SnapshotFailure
        self.lock.unlink()
        error = SnapshotError(SnapshotFailure("unavailable", "STORE.FIXTURE_UNAVAILABLE", "private fixture"))
        with mock.patch.object(self.engine._authoring, "record_applied", side_effect=error):
            result = self.author.recover({"context": self.context, "action": "complete-publication"})
        self.assertEqual(result["outcome"]["code"], "APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE", result)
        self.assertEqual(self.engine._repository.branch_revision("main"), self.application.candidate)
        with (mock.patch.object(self.engine._repository, "publish_candidate") as publish,
              mock.patch.object(self.engine, "_application_candidate") as candidate):
            recovered = self.author.recover({"context": self.context})
            self.assertEqual(recovered["status"], "applied", recovered)
            publish.assert_not_called()
            candidate.assert_not_called()

    def test_competing_same_candidate_is_reconciled(self):
        self.lock.unlink()
        original = self.engine._repository.publish_candidate

        def concurrent_completion(candidate, expected):
            self.assertEqual(original(candidate, expected), "updated")
            return "stale"  # The competing request won before this one's CAS.

        with mock.patch.object(self.engine._repository, "publish_candidate", side_effect=concurrent_completion):
            recovered = self.author.recover({"context": self.context, "action": "complete-publication"})
        self.assertEqual(recovered["status"], "applied", recovered)
        self.assertEqual(recovered["outcome"]["application"]["id"], self.application.application_id)

    def test_application_purpose_cannot_request_completion(self):
        app = AgentToolFacade.open_repository(self.root, purpose="application")
        try:
            denied = app.recover({"context": self.context, "action": "complete-publication"})
        finally:
            app.close()
        self.assertEqual(denied["code"], "APPLICATION.OPERATION_UNAVAILABLE", denied)
        self.assertEqual(self.engine._repository.branch_revision("main"), self.expected)

    def test_recovery_reconstructs_a_candidate_that_was_never_imported(self):
        from tools.repository_git.repository_git import GitRepositoryError, GitRepositoryFailure
        self.lock.unlink()
        proposed = self.author.propose({"change_set": reference_change(self.root, "failed-fetch")})
        ready = self.author.review({"context": proposed["context"], "decisions": decisions(self.root)})
        with mock.patch.object(self.engine._repository, "publish_candidate", side_effect=GitRepositoryError(
            GitRepositoryFailure("unavailable", "REPOSITORY_GIT.COMMAND_UNAVAILABLE", "private fetch failure")
        )):
            failed = self.author.apply({"context": ready["context"]})
        self.assertEqual(failed["status"], "recovery-required", failed)
        selected = self.engine._authoring.read_selected_application(ready["context"]["id"])
        missing = subprocess.run(["git", "cat-file", "-e", selected.candidate.oid], cwd=self.root, capture_output=True)
        self.assertNotEqual(missing.returncode, 0)
        recovered = self.author.recover({"context": ready["context"], "action": "complete-publication"})
        self.assertEqual(recovered["status"], "applied", recovered)
        self.assertEqual(recovered["outcome"]["application"]["id"], selected.application_id)
        self.assertEqual(self.engine._repository.branch_revision("main"), selected.candidate)

    def test_stale_readiness_is_not_substituted_with_new_proposal_content(self):
        self.lock.unlink()
        changed = self.author.revise_proposal({
            "kind": "revise-proposal",
            "expected_revision": self.engine._proposal_revision_handle(self.application.revision_id),
            "change_set": reference_change(self.root, "recovery", revision=True),
        })
        self.assertEqual(changed["kind"], "revise-proposal-result", changed)
        with mock.patch.object(self.engine, "_application_candidate") as candidate:
            result = self.author.recover({"context": self.context, "action": "complete-publication"})
            self.assertEqual(result["status"], "recovery-required", result)
            self.assertEqual(result["outcome"]["details"]["cause_code"], "AUTHORING.READINESS_STALE", result)
            candidate.assert_not_called()
        self.assertEqual(self.engine._authoring.read_selected_application(self.context["id"]), self.application)
