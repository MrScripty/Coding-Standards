from __future__ import annotations

import copy
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from types import SimpleNamespace
from pathlib import Path

from tools.standards_engine.standards_engine import AgentToolFacade
from tools.standards_engine.standards_engine.authoring import AuthoringError
from tools.standards_engine.standards_engine.navigation_indexes import (
    CATALOG,
    ROUTES,
    SUITES,
    load_indexes,
)
from tools.standards_metadata.standards_metadata import FrozenContentSource
from tools.standards_analysis.standards_analysis import (
    NavigationIndexAuthority,
    generate_navigation_index_obligations,
)
from tools.standards_engine.tests.test_agent_workflow import (
    ROOT,
    decisions,
    evidence,
    prepare_repository,
)


class NavigationIndexAuthorityTest(unittest.TestCase):
    def test_old_captured_index_without_route_inventory_remains_readable(self):
        source = FrozenContentSource(
            {
                CATALOG: b'schema_version = 1\n[[indexes]]\nid = "navigation.old"\npath = "old.md"\ndestinations = []\n',
                "old.md": b"# Old index\n",
                SUITES: b"suites = []\n",
            }
        )
        index = load_indexes(source, SimpleNamespace(resolve_module=lambda _: None))[0]
        self.assertEqual(index.routes, ())

    def test_declared_routes_bind_their_owner_content_and_exact_declarations(self):
        module = SimpleNamespace(module_id="topic.owner", path="owner.md")
        corpus = SimpleNamespace(
            resolve_module=lambda value: (
                module if value in {"topic.owner", "owner.md"} else None
            )
        )
        files = {
            CATALOG: b'schema_version = 1\n[[indexes]]\nid = "navigation.old"\npath = "old.md"\ndestinations = []\n',
            "old.md": b"# Old index\n",
            SUITES: b"suites = []\n",
            "owner.md": b"# Section\nOriginal policy\n",
            ROUTES: b"source\troute\tdestination\nold.md\towner\towner.md#section\n",
        }
        before = load_indexes(FrozenContentSource(files), corpus)[0]
        files["owner.md"] = b"# Section\nChanged policy\n"
        after = load_indexes(FrozenContentSource(files), corpus)[0]
        self.assertEqual(
            before.review.representation_digest, after.review.representation_digest
        )
        self.assertNotEqual(before.review.review_digest, after.review.review_digest)
        files[ROUTES] = b"source\troute\tdestination\nold.md\towner\towner.md\n"
        retargeted = load_indexes(FrozenContentSource(files), corpus)[0]
        self.assertNotEqual(
            after.review.representation_digest, retargeted.review.representation_digest
        )

    def test_absent_catalog_exposes_no_authoring_capability(self):
        self.assertEqual(load_indexes(FrozenContentSource({}), None), ())

    def test_registration_cannot_make_a_normative_standard_writable(self):
        source = FrozenContentSource(
            {
                CATALOG: b'schema_version = 1\n[[indexes]]\nid = "navigation.core"\npath = "CORE-STANDARDS.md"\ndestinations = []\n'
            }
        )
        corpus = SimpleNamespace(
            resolve_module=lambda value: (
                object() if value == "CORE-STANDARDS.md" else None
            )
        )
        with self.assertRaises(AuthoringError) as rejected:
            load_indexes(source, corpus)
        self.assertEqual(rejected.exception.failure.code, "NAVIGATION.INVALID_CATALOG")

    def test_bad_catalog_and_non_utf8_content_are_typed_rejections(self):
        corpus = SimpleNamespace(resolve_module=lambda _: None)
        cases = [
            {CATALOG: b"not TOML"},
            {CATALOG: b"schema_version = true\nindexes = []\n"},
            {
                CATALOG: b'schema_version = 1\n[[indexes]]\nid = "navigation.old"\npath = "old.md"\ndestinations = []\n',
                "old.md": b"\xff",
            },
        ]
        for files in cases:
            with self.subTest(files=files), self.assertRaises(AuthoringError):
                load_indexes(FrozenContentSource(files), corpus)

    def test_review_fingerprint_binds_destination_authority_without_inventing_policy_changes(
        self,
    ):
        before = NavigationIndexAuthority(
            "navigation.old", "sha256:" + "1" * 64, "sha256:" + "2" * 64
        )
        after = NavigationIndexAuthority(
            "navigation.old", "sha256:" + "3" * 64, "sha256:" + "4" * 64
        )
        later_destination = NavigationIndexAuthority(
            after.id, after.representation_digest, "sha256:" + "5" * 64
        )
        first = generate_navigation_index_obligations((before,), (after,))[0]
        second = generate_navigation_index_obligations((before,), (later_destination,))[
            0
        ]
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(first.permitted_submissions, ("impact-disposition",))
        self.assertEqual(
            generate_navigation_index_obligations((after,), (later_destination,)), ()
        )


class NavigationIndexFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="navigation-index-test-")
        cls.root = Path(cls.temporary.name) / "repository"
        prepare_repository(cls.root)
        for relative in (
            "tools/standards_engine/navigation-indexes.toml",
            "tools/standards_engine/contracts/examples/a1-examples.json",
            "tools/standards_engine/standards_engine/_generated_contract.py",
        ):
            shutil.copyfile(ROOT / relative, cls.root / relative)
        cls.seed_legacy_fixture()
        subprocess.run(["git", "add", "--all"], cwd=cls.root, check=True)
        with AgentToolFacade.open_repository(cls.root) as fixture_facade:
            refreshed = fixture_facade.verify_repository(
                {"kind": "verify-repository", "refresh_verification_inputs": True}
            )
            assert refreshed["verification"]["passed"], refreshed
        subprocess.run(["git", "add", "--all"], cwd=cls.root, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "test: admit navigation fixture",
            ],
            cwd=cls.root,
            check=True,
        )
        cls.facade = AgentToolFacade.open_repository(cls.root)
        directory = cls.facade.read({"target": "navigation-indexes"})
        assert directory["kind"] == "navigation-indexes-result", directory
        cls.frontend = next(
            x for x in directory["indexes"] if x["id"] == "navigation.frontend"
        )
        cls.snapshot = directory["authority"]
        cls.indexes = {entry["id"]: entry for entry in directory["indexes"]}
        cls.entry = next(
            x for x in directory["indexes"] if x["id"] == "navigation.tooling"
        )

    @classmethod
    def seed_legacy_fixture(cls):
        """Own the obsolete test input even after the real index is corrected."""
        from tools.standards_engine.standards_engine.logical_authoring import (
            _toml_inline,
        )

        required = set()
        registry = tomllib.loads((cls.root / SUITES).read_text())
        for suite in registry["suites"]:
            path = cls.root / suite["path"]
            document = tomllib.loads(path.read_text())
            changed = False
            for check in document["checks"]:
                if (
                    check["type"] != "markdown_targets"
                    or check["path"] != "TOOLING-STANDARDS.md"
                ):
                    continue
                check["required"] = [
                    "FRONTEND-STANDARDS.md"
                    if target == "profiles/applications/frontend.md"
                    else target
                    for target in check["required"]
                ]
                required.update(check["required"])
                changed = True
            if changed:
                lines = [
                    f"{key} = {_toml_inline(value)}"
                    for key, value in document.items()
                    if key != "checks"
                ]
                for check in document["checks"]:
                    lines.extend(("", "[[checks]]"))
                    lines.extend(
                        f"{key} = {_toml_inline(value)}" for key, value in check.items()
                    )
                path.write_text("\n".join(lines) + "\n")
        (cls.root / "TOOLING-STANDARDS.md").write_text(
            "# Legacy Tooling Fixture\n\nObsolete fixture scheduling defaults.\n\n"
            + "\n".join(f"- [Destination]({path})" for path in sorted(required))
            + "\n"
        )
        coding = cls.root / "CODING-STANDARDS.md"
        obsolete = "CORE-STANDARDS.md#code-and-terminology-discipline"
        if obsolete not in coding.read_text():
            coding.write_text(
                coding.read_text()
                + f"\n- Obsolete fixture terminology: [Core]({obsolete})\n"
            )

    @classmethod
    def tearDownClass(cls):
        cls.facade.close()
        cls.temporary.cleanup()

    def change(self):
        return {
            "purpose": {
                "summary": "Normalize the isolated Tooling index",
                "rationale": "Remove fixture legacy instructions in favor of the canonical Tooling owner.",
                "evidence": [evidence(self.root)],
            },
            "edits": [
                {
                    "kind": "rewrite-navigation-index",
                    "entrypoint": self.entry["entrypoint"],
                    "destinations": [
                        "profile.application.frontend",
                        "profile.language.typescript",
                        "reference.recipes.documentation",
                        "reference.recipes.implementation",
                        "reference.recipes.tooling",
                        "topic.dependencies",
                        "workflow.commit",
                        "workflow.documentation",
                        "workflow.implementation",
                        "workflow.tooling",
                        "workflow.verification",
                    ],
                    "retargets": [
                        {
                            "entrypoint": self.frontend["entrypoint"],
                            "standard": "profile.application.frontend",
                        }
                    ],
                    "rationale": "These canonical owners own tooling and evidence in this fixture.",
                }
            ],
        }

    def propose(self, change=None):
        return self.facade.propose(
            {"snapshot": self.snapshot, "change_set": change or self.change()}
        )


class NavigationIndexWorkflowTest(NavigationIndexFixture):
    def test_invalid_selections_do_not_create_an_applicable_candidate(self):
        variants = []
        for destinations in (
            [],
            ["workflow.tooling", "workflow.tooling"],
            ["TOOLING-STANDARDS.md"],
            ["topic.missing"],
            ["../CORE-STANDARDS.md"],
        ):
            change = self.change()
            change["edits"][0]["destinations"] = destinations
            variants.append(change)
        forged = self.change()
        forged["edits"][0]["entrypoint"] = copy.deepcopy(self.entry["entrypoint"])
        forged["edits"][0]["entrypoint"]["id"] = "sha256:" + "0" * 64
        variants.append(forged)
        raw = self.change()
        raw["edits"][0]["body"] = "arbitrary text"
        variants.append(raw)
        for change in variants:
            with self.subTest(change=change):
                result = self.propose(change)
                self.assertEqual(
                    (
                        result["outcome"]
                        if result["kind"] == "workflow-result"
                        else result
                    )["kind"],
                    "rejected-result",
                    result,
                )

    def test_cross_snapshot_handle_is_not_an_authorization_to_retarget(self):
        other = self.facade.read({"target": "navigation-indexes"})
        result = self.facade.propose(
            {"snapshot": other["authority"], "change_set": self.change()}
        )
        self.assertEqual(
            (result["outcome"] if result["kind"] == "workflow-result" else result)[
                "code"
            ],
            "NAVIGATION.STALE_TARGET",
            result,
        )

    def test_retarget_dispositions_cannot_remove_unrelated_assertions(self):
        variants = []
        unused = self.change()
        unused["edits"][0]["retargets"][0]["entrypoint"] = self.entry["entrypoint"]
        variants.append((unused, "NAVIGATION.UNUSED_RETARGET"))
        duplicate = self.change()
        duplicate["edits"][0]["retargets"] *= 2
        variants.append((duplicate, "INTERFACE.INVALID_ARGUMENTS"))
        unselected = self.change()
        unselected["edits"][0]["retargets"][0]["standard"] = "topic.security"
        variants.append((unselected, "NAVIGATION.INVALID_RETARGET"))
        for change, code in variants:
            with self.subTest(code=code):
                result = self.propose(change)
                outcome = (
                    result["outcome"] if result["kind"] == "workflow-result" else result
                )
                self.assertEqual(outcome["code"], code, result)

    def test_discovery_captures_exact_content_without_claiming_policy_authority(self):
        request = {"snapshot": self.snapshot, "target": "navigation.tooling"}
        before = self.facade.read(request)
        path = self.root / "TOOLING-STANDARDS.md"
        original = path.read_bytes()
        try:
            path.write_text("uncommitted unrelated bytes\n")
            self.assertEqual(self.facade.read(request), before)
        finally:
            path.write_bytes(original)
        self.assertNotIn("policy", before)
        self.assertIn("scheduling defaults", before["indexes"][0]["content"])

    def test_fresh_mcp_process_exposes_snapshot_bound_navigation(self):
        from tools.standards_engine.tests.test_mcp import request

        messages = [
            request(
                "initialize",
                {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "navigation-test", "version": "1"},
                },
            ),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            request(
                "tools/call",
                {
                    "name": "read",
                    "arguments": {
                        "target": "navigation.tooling",
                        "snapshot": self.snapshot,
                    },
                },
                identifier=2,
            ),
        ]
        process = subprocess.run(
            [
                sys.executable,
                "-P",
                "-m",
                "tools.standards_engine.standards_engine.mcp",
                "--repo-root",
                str(self.root),
            ],
            input="".join(json.dumps(message) + "\n" for message in messages),
            text=True,
            capture_output=True,
            cwd="/tmp",
            env={**os.environ, "PYTHONPATH": str(ROOT)},
            timeout=30,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout.splitlines()[-1])["result"][
            "structuredContent"
        ]
        self.assertEqual(result["kind"], "navigation-indexes-result", result)
        self.assertEqual(result["authority"], self.snapshot)
        self.assertIn("scheduling defaults", result["indexes"][0]["content"])

    def test_z_exact_index_proposal_requires_review_and_applies_through_engine(self):
        original = (self.root / "TOOLING-STANDARDS.md").read_bytes()
        proposed = self.propose()
        self.assertEqual(proposed["status"], "needs-action", proposed)
        obligations = proposed["outcome"]["obligations"]
        self.assertEqual(len(obligations), 1, proposed)
        obligation = obligations[0]
        self.assertEqual(obligation["target"], "navigation.tooling")
        self.assertEqual(obligation["reasons"][0]["kind"], "navigation-index-change")
        self.assertEqual(
            self.facade.review(
                {"context": proposed["context"], "decisions": decisions(self.root)}
            )["code"],
            "WORKFLOW.OPERATION_NOT_AVAILABLE",
        )
        preview = self.facade.query_proposal(
            {
                "revision": proposed["revision"],
                "request": {"kind": "read", "target": "navigation.tooling"},
            }
        )
        self.assertEqual(preview["authority"], proposed["revision"])
        content = preview["indexes"][0]["content"]
        self.assertNotIn("scheduling defaults", content)
        self.assertIn("](workflows/tooling.md)", content)
        self.assertEqual((self.root / "TOOLING-STANDARDS.md").read_bytes(), original)
        resolved = self.facade.resolve_workflow(
            {
                "context": proposed["context"],
                "submission": {
                    "kind": "impact-disposition",
                    "obligation": obligation["handle"],
                    "result": "confirmed",
                    "rationale": "The exact candidate is navigation-only and retains every declared canonical destination.",
                    "evidence": [evidence(self.root)],
                    "fingerprint": obligation["fingerprint"],
                },
            }
        )
        self.assertEqual(resolved["status"], "complete", resolved)
        ready = self.facade.review(
            {"context": resolved["context"], "decisions": decisions(self.root)}
        )
        self.assertEqual(ready["status"], "ready", ready)
        checked = self.facade.verify_proposal(
            {
                "kind": "verify-proposal",
                "revision": proposed["revision"],
                "readiness": ready["context"],
            }
        )
        self.assertTrue(checked["verification"]["passed"], checked)
        applied = self.facade.apply({"context": ready["context"]})
        self.assertEqual(applied["status"], "applied", applied)
        self.assertEqual(
            self.facade.read({"target": "navigation.tooling"})["indexes"][0]["content"],
            content,
        )
        # Historical authority remains exact after publication.
        self.assertEqual(
            self.facade.read(
                {"snapshot": self.snapshot, "target": "navigation.tooling"}
            )["indexes"][0]["content"].encode(),
            original,
        )
        current = self.facade.read({"target": "navigation.tooling"})
        unchanged = self.change()
        unchanged["edits"][0]["entrypoint"] = current["indexes"][0]["entrypoint"]
        unchanged["edits"][0].pop("retargets")
        rejected = self.facade.propose(
            {"snapshot": current["authority"], "change_set": unchanged}
        )
        self.assertEqual(rejected["code"], "AUTHORING.NO_EFFECT", rejected)


class ProtectedNavigationIndexTest(NavigationIndexFixture):
    def change(self):
        change = super().change()
        change["purpose"]["summary"] = "Correct an isolated Coding navigation fixture"
        change["purpose"]["rationale"] = (
            "Exercise preservation of declared Coding navigation routes."
        )
        change["edits"] = [
            {
                "kind": "rewrite-navigation-index",
                "entrypoint": self.indexes["navigation.coding"]["entrypoint"],
                "destinations": [
                    "core",
                    "router",
                    "topic.architecture",
                    "topic.resilience",
                    "topic.contracts",
                    "topic.dependencies",
                    "workflow.verification",
                    "workflow.implementation",
                    "workflow.build",
                    "topic.licensing",
                    "profile.language.typescript",
                    "profile.language.typescript.async",
                    "profile.application.frontend",
                    "topic.performance",
                    "topic.code-design",
                ],
                "rationale": "Remove the obsolete unlisted link while preserving every declared route.",
            }
        ]
        return change

    def test_declared_routes_reject_omitted_owners_and_unsupported_artifacts(self):
        omitted = self.change()
        omitted["edits"][0]["destinations"].remove("topic.contracts")
        result = self.propose(omitted)
        self.assertEqual(result["code"], "NAVIGATION.REQUIRED_DESTINATION", result)
        artifact = self.change()
        artifact["edits"][0]["entrypoint"] = self.indexes["navigation.plan"][
            "entrypoint"
        ]
        artifact["edits"][0]["destinations"] = ["router", "workflow.planning"]
        result = self.propose(artifact)
        self.assertEqual(
            result["code"], "NAVIGATION.ARTIFACT_ROUTE_UNSUPPORTED", result
        )

    def test_z_declared_sections_survive_verified_index_application(self):
        inventory = (self.root / ROUTES).read_bytes()
        required = [
            row["destination"]
            for row in csv.DictReader(io.StringIO(inventory.decode()), delimiter="\t")
            if row["source"] == "CODING-STANDARDS.md"
        ]
        proposed = self.propose()
        self.assertEqual(proposed["status"], "needs-action", proposed)
        self.assertEqual(len(proposed["outcome"]["obligations"]), 1)
        preview = self.facade.query_proposal(
            {
                "revision": proposed["revision"],
                "request": {"kind": "read", "target": "navigation.coding"},
            }
        )
        content = preview["indexes"][0]["content"]
        self.assertNotIn("CORE-STANDARDS.md#code-and-terminology-discipline", content)
        self.assertIn("](topics/code-design.md)", content)
        for destination in required:
            self.assertIn(f"]({destination})", content)
        obligation = proposed["outcome"]["obligations"][0]
        resolved = self.facade.resolve_workflow(
            {
                "context": proposed["context"],
                "submission": {
                    "kind": "impact-disposition",
                    "obligation": obligation["handle"],
                    "result": "confirmed",
                    "rationale": "The exact fixture retains all declared routes and canonical owners.",
                    "evidence": [evidence(self.root)],
                    "fingerprint": obligation["fingerprint"],
                },
            }
        )
        self.assertEqual(resolved["status"], "complete", resolved)
        ready = self.facade.review(
            {"context": resolved["context"], "decisions": decisions(self.root)}
        )
        self.assertEqual(ready["status"], "ready", ready)
        applied = self.facade.apply({"context": ready["context"]})
        self.assertEqual(applied["status"], "applied", applied)
        self.assertEqual(
            self.facade.read({"target": "navigation.coding"})["indexes"][0]["content"],
            content,
        )
        published_inventory = subprocess.check_output(
            ["git", "show", "main:" + ROUTES], cwd=self.root
        )
        self.assertEqual(published_inventory, inventory)


if __name__ == "__main__":
    unittest.main()
