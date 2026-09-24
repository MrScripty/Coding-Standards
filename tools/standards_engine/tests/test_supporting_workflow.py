"""Real proposal, review, publication and readback in an isolated Git repository."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.standards_engine.standards_engine import AgentToolFacade
from tools.standards_engine.tests.test_agent_workflow import prepare_repository, evidence, decisions
from tools.standards_metadata.standards_metadata import load_canonical_standards_corpus

RULE = "topic.purpose-fixture"
REFERENCE = "reference.testing.purpose-fixture"
REASON = "provenance.purpose-fixture"
PRIVATE = "PRIVATE_DECISION_RECORD_506187"
PUBLIC = "Observe the operation's owned completion before releasing its resource."


def standard(identity, *, reference=False):
    return {"kind": "create-standard", "standard": {
        "id": identity, "title": "Purpose Boundary Fixture", "role": "reference" if reference else "topic",
        "level": "REFERENCE" if reference else "MUST", "applies_when": "The isolated fixture is selected.",
        "does_not_apply_when": "The fixture is outside the selected task.",
        "verification": "The isolated Engine workflow verifies the selected result.",
        "body": "## Owned completion\n\n" + PUBLIC + "\n",
    }, "requires": [], "specializes": [], "policy_units": []}


class SupportingWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="supporting-workflow-")
        cls.root = Path(cls.temporary.name) / "repository"
        prepare_repository(cls.root)
        # Fixture publication has one explicit local accepted branch regardless
        # of which implementation branch supplied the test code.
        if subprocess.check_output(["git", "branch", "--show-current"], cwd=cls.root).decode().strip() != "main":
            subprocess.run(["git", "branch", "-m", "main"], cwd=cls.root, check=True)
        cls.author = AgentToolFacade.open_repository(cls.root, purpose="authoring")
        cls.app = AgentToolFacade.open_repository(cls.root, purpose="application")

    @classmethod
    def tearDownClass(cls):
        cls.author.close(); cls.app.close(); cls.temporary.cleanup()

    def change(self, edits):
        return {"purpose": {"summary": "Exercise purpose-separated content publication",
                            "rationale": "This isolated fixture proves the Engine mechanism, not editorial quality.",
                            "evidence": [evidence(self.root)]}, "edits": edits}

    def resolve(self, proposed):
        seen = set()
        while proposed.get("status") == "needs-action":
            self.assertNotIn(json.dumps(proposed["context"], sort_keys=True), seen, proposed)
            seen.add(json.dumps(proposed["context"], sort_keys=True))
            outcome = proposed["outcome"]
            self.assertFalse(outcome.get("fact_requirements"), outcome)
            obligation = next(item for item in outcome["obligations"] if item["state"] == "required")
            self.assertIn("impact-disposition", obligation["permitted_submissions"], obligation)
            proposed = self.author.resolve_workflow({"context": proposed["context"], "submission": {
                "kind": "impact-disposition", "obligation": obligation["handle"], "result": "confirmed",
                "rationale": "The fixture owner confirms this exact isolated support/content change.",
                "evidence": [evidence(self.root)], "fingerprint": obligation["fingerprint"],
            }})
        self.assertEqual(proposed.get("status"), "complete", proposed)
        return proposed

    def publish(self, proposed):
        complete = self.resolve(proposed)
        ready = self.author.review({"context": complete["context"], "decisions": decisions(self.root)})
        self.assertEqual(ready.get("status"), "ready", ready)
        applied = self.author.apply({"context": ready["context"]})
        self.assertEqual(applied.get("status"), "applied", applied)
        return applied

    def test_coordinated_publication_and_provenance_only_revision(self):
        snapshot = self.author.create_snapshot({"kind": "create-snapshot"})["snapshot"]["snapshot"]
        empty = self.app.read({"snapshot": snapshot, "target": "core"})
        self.assertEqual(empty["code"], "APPLICATION.CONTENT_UNAVAILABLE", empty)
        aids = []
        for target in ("prompts/planning.md", "templates/PLAN-TEMPLATE.md"):
            aid = self.author.read({"snapshot": snapshot, "target": target})
            self.assertEqual(aid["kind"], "operational-read-result", aid)
            aids.append(aid)
        record = {"id": REASON, "subject": RULE, "origin": "current-justification", "rationale": PRIVATE, "evidence": [evidence(self.root)]}
        edits = [{"kind": "approve-application-content", "target": RULE},
                 {"kind": "put-provenance", "record": record},
                 standard(REFERENCE, reference=True), standard(RULE),
                 {"kind": "approve-application-content", "target": REFERENCE}]
        for aid in aids:
            lines = aid["content"].splitlines()
            edits.extend([
                {"kind": "revise-operational-artifact", "target": aid["target"],
                 "title": lines[0].lstrip("# "), "body": "\n".join(lines[1:]).lstrip() + "\n\n" + PUBLIC + "\n"},
                {"kind": "approve-application-content", "target": aid["target"]},
            ])
        proposed = self.author.propose({"snapshot": snapshot, "change_set": self.change(edits)})
        self.assertEqual(proposed.get("status"), "needs-action", proposed)
        draft = self.author.query_proposal({"revision": proposed["revision"], "request": {"kind": "read", "target": REASON}})
        self.assertEqual(draft["record"]["rationale"], PRIVATE, draft)
        self.assertEqual(self.app.read({"target": RULE})["kind"], "application-rejected-result")
        self.assertEqual(self.app.query_proposal({"revision": proposed["revision"], "request": {"kind": "read", "target": REASON}})["code"], "APPLICATION.OPERATION_UNAVAILABLE")
        self.publish(proposed)
        first = self.app.read({"target": RULE, "detail": "full"})
        self.assertEqual(first["kind"], "application-read-result", first)
        self.assertIn(PUBLIC, first["content"])
        self.assertNotIn(PRIVATE, json.dumps(first))
        # Reads in this interval observe the same accepted publication.
        published_snapshot = first["snapshot"]
        self.assertNotEqual(published_snapshot, snapshot)
        self.assertEqual(self.app.read({"snapshot": published_snapshot, "target": REFERENCE})["kind"], "application-read-result")
        for aid in aids:
            exposed = self.app.read({"snapshot": published_snapshot, "target": aid["canonical_id"]})
            self.assertEqual(exposed["kind"], "application-read-result", exposed)
            self.assertIn(PUBLIC, exposed["content"])
        before = subprocess.check_output(["git", "show", "main:topics/purpose-fixture.md"], cwd=self.root)
        revisions_before = {unit.id: unit.semantic_revision for unit in
                            load_canonical_standards_corpus(self.root).policy_units}
        old_snapshot = first["snapshot"]
        next_change = self.author.propose({"snapshot": published_snapshot, "change_set": self.change([
            {"kind": "put-provenance", "record": {**record, "rationale": PRIVATE + "_REVISED"}},
        ])})
        self.assertEqual(len(next_change["outcome"]["obligations"]), 1, next_change)
        self.publish(next_change)
        after = subprocess.check_output(["git", "show", "main:topics/purpose-fixture.md"], cwd=self.root)
        self.assertEqual(before, after)
        revisions_after = {unit.id: unit.semantic_revision for unit in
                           load_canonical_standards_corpus(self.root).policy_units}
        self.assertEqual(revisions_before, revisions_after)
        historical = self.author.read({"snapshot": old_snapshot, "target": REASON})
        current = self.author.read({"target": REASON})
        self.assertEqual(historical["record"]["rationale"], PRIVATE)
        self.assertEqual(current["record"]["rationale"], PRIVATE + "_REVISED")
        self.assertNotEqual(current["snapshot"], old_snapshot)
        self.assertEqual(self.app.read({"snapshot": current["snapshot"], "target": RULE})["content"], first["content"])
        self.assertEqual(self.app.read({"snapshot": current["snapshot"], "target": REASON})["kind"], "application-rejected-result")
