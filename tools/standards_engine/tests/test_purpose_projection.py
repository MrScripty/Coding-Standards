"""Focused exposure evidence over captured content and the actual SQLite store."""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import _generated_contract as c
from tools.standards_engine.standards_engine.context_projection import ApplicationView, Purpose
from tools.standards_engine.standards_engine.logical_authoring import _toml_inline
from tools.standards_engine.standards_engine.tools import _contracts
from tools.standards_engine.standards_engine.supporting import subject_binding
from tools.standards_engine.tests.test_logical_authoring import _CurrentFilesWithFreshSuiteDigests
from tools.standards_metadata.standards_metadata import (
    APPLICATION_CONTENT, DECISION_PROVENANCE, FrozenContentSource, RecordingContentSource, file_digest,
)
from tools.standards_snapshots.standards_snapshots import CapturedContent, SnapshotFile, SnapshotPath

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = "AUTHORING_ONLY_ORIGIN_673591"
PUBLIC = "APPROVED_OPERATIONAL_RULE_184237"


def refresh(files):
    key = "evaluation/standards-effectiveness/generated/suite-inputs.json"
    raw = json.loads(files[key])
    for row in raw["files"]:
        if row["state"] == "present" and row["path"] in files:
            row["digest"] = file_digest(files[row["path"]])
    for row in raw["suites"]:
        if row["path"] in files:
            row["digest"] = file_digest(files[row["path"]])
    raw["registry"]["digest"] = file_digest(files[raw["registry"]["path"]])
    files[key] = (json.dumps(raw, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    return FrozenContentSource(files)


def compile_files(files):
    return StandardsEngine._compile(refresh(dict(files)))


class PurposeProjectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capture = RecordingContentSource(_CurrentFilesWithFreshSuiteDigests(ROOT))
        StandardsEngine._compile(capture)
        cls.original = dict(capture.freeze().files)
        files = dict(cls.original)
        files["CORE-STANDARDS.md"] += ("\n" + PUBLIC + "\n").encode()
        compiled = compile_files(files)
        reference = next(module for module in compiled.corpus.modules if module.role == "reference")
        cls.reference = reference.module_id
        eligible = {"core", "router", reference.module_id}
        pending = list(eligible)
        while pending:
            material = compiled.materials[pending.pop()]
            for dependency in (*material.requires, *material.specializes):
                if dependency not in eligible:
                    eligible.add(dependency); pending.append(dependency)
        entries = [{"target": key, "binding": compiled.materials[key].binding} for key in sorted(eligible)]
        records = [{"id": "provenance.fixture", "subject": "core", "subject_binding": subject_binding(compiled, "core"),
                    "origin": "current-justification", "rationale": PRIVATE, "evidence": []}]
        files[APPLICATION_CONTENT] = ("schema_version = 1\nentries = " + _toml_inline(entries) + "\n").encode()
        files[DECISION_PROVENANCE] = ("schema_version = 1\nrecords = " + _toml_inline(records) + "\n").encode()
        cls.files = dict(refresh(files).files)
        cls.compiled = compile_files(cls.files)
        cls.temporary = tempfile.TemporaryDirectory(prefix="purpose-projection-")
        cls.store_path = Path(cls.temporary.name) / "engine.sqlite3"
        cls.engine = StandardsEngine.open_repository(ROOT, purpose="application", store_path=cls.store_path)
        captured = cls.engine._snapshots.create_snapshot(CapturedContent("test-fixture", (
            SnapshotFile(SnapshotPath.parse(path), value) for path, value in cls.files.items())))
        cls.snapshot = cls.engine._snapshot_handle(captured.snapshot)
        cls.facade = AgentToolFacade(cls.engine, _contracts(ROOT))

    @classmethod
    def tearDownClass(cls):
        cls.engine.close(); cls.temporary.cleanup()

    def read(self, **fields):
        return self.facade.read({"snapshot": self.snapshot, "target": "core", **fields})

    def test_read_has_exact_reviewed_content_and_explicit_permitted_fields(self):
        for detail in ("compact", "full"):
            value = self.read(detail=detail)
            self.assertEqual(value["kind"], "application-read-result", value)
            self.assertEqual(value["content"], self.files["CORE-STANDARDS.md"].decode())
            self.assertIn(PUBLIC, value["content"])
            self.assertNotIn(PRIVATE, json.dumps(value))
            self.assertEqual(set(value), {"kind", "purpose", "snapshot", "policy", "content", "scope", "requires", "specializes", "next_operations"} | ({"related"} if detail == "full" else set()))
            self.assertNotIn("provenance", value)

    def test_direct_hidden_read_and_privileged_request_are_bounded(self):
        for fields in ({"target": "provenance.fixture"}, {"purpose": "authoring"}, {"include_coverage": True}):
            value = self.read(**fields)
            self.assertEqual(value["kind"], "application-rejected-result")
            self.assertNotIn(PRIVATE, json.dumps(value))
        with self.assertRaises(AttributeError):
            self.engine.purpose = Purpose.AUTHORING
        with self.assertRaises(TypeError):
            StandardsEngine.open_repository(ROOT)

    def test_domain_and_facade_admit_only_application_operations_before_work(self):
        from unittest.mock import Mock
        for operation in _contracts(ROOT).interface.operations:
            if "application" in operation.variants:
                continue
            with self.subTest(operation=operation.id):
                result = getattr(self.engine, operation.id)(Mock())
                self.assertEqual(result.as_contract()["code"], "APPLICATION.OPERATION_UNAVAILABLE")
                value = getattr(self.facade, operation.id)({})
                self.assertEqual(value["code"], "APPLICATION.OPERATION_UNAVAILABLE")

    def test_native_query_and_handle_inspection_use_the_same_boundary(self):
        value = self.facade.query({"snapshot": self.snapshot, "request": {"kind": "read", "target": "core", "detail": "full"}})
        self.assertEqual(value["kind"], "application-read-result", value)
        inspected = self.facade.inspect({"handle": value["policy"]["handle"]})
        self.assertEqual(inspected["content"], value["content"])
        handle = {**value["policy"]["handle"], "child_id": "provenance.fixture"}
        self.assertEqual(self.facade.inspect({"handle": handle})["kind"], "application-rejected-result")

    def test_authoring_read_retrieves_reasoning_and_exposure_state(self):
        with StandardsEngine.open_repository(ROOT, purpose="authoring", store_path=self.store_path) as engine:
            facade = AgentToolFacade(engine, _contracts(ROOT))
            value = facade.read({"snapshot": self.snapshot, "target": "provenance.fixture"})
            self.assertEqual(value["record"]["rationale"], PRIVATE, value)
            normal = facade.read({"snapshot": self.snapshot, "target": "core"})
            self.assertEqual(normal["application_exposure"], "current")
            self.assertIn("provenance.fixture", normal["provenance"])

    def test_material_change_requires_new_exposure_but_rationale_change_does_not(self):
        files = dict(self.files)
        files["CORE-STANDARDS.md"] += b"\nMaterially changed content.\n"
        changed = compile_files(files)
        self.assertEqual(changed.supporting.exposure_state("core", changed.materials["core"].binding), "needs-review")
        files = dict(self.files)
        files[DECISION_PROVENANCE] = files[DECISION_PROVENANCE].replace(PRIVATE.encode(), b"Revised authoring reason")
        reason = compile_files(files)
        self.assertEqual(reason.materials["core"].binding, self.compiled.materials["core"].binding)
        self.assertEqual(reason.supporting.exposure_state("core", reason.materials["core"].binding), "current")

    def test_routing_retains_unknown_facts_and_blocks_missing_required_content(self):
        unknown = self.facade.route({"snapshot": self.snapshot, "facts": {}})
        self.assertEqual(unknown["status"], "needs-facts", unknown)
        self.assertTrue(unknown["unresolved_questions"])
        facts = {"routing."+key: {"type": "enum-set", "state": "known", "value": []}
                 for key in ("activities", "workflow-profiles", "applications", "boundaries", "languages", "frameworks", "topics", "details")}
        complete = self.facade.route({"snapshot": self.snapshot, "facts": facts})
        self.assertEqual(complete["status"], "complete", complete)
        facts["routing.activities"]["value"] = ["implementation"]
        blocked = self.facade.route({"snapshot": self.snapshot, "facts": facts})
        self.assertEqual(blocked["code"], "APPLICATION.CONTENT_UNAVAILABLE", blocked)

    def test_hidden_intermediate_cannot_bridge_a_permitted_traversal(self):
        from tools.graph_engine.graph_engine import (
            Direction, Edge, EdgeGroup, EdgeRegistry, GraphContribution,
            Node, Provenance, TraversalPolicy,
        )
        from tools.standards_graph.standards_graph import Provider
        provenance = Provenance("fixture", "provider", "isolated graph fixture")
        group = EdgeGroup("semantic", "Selected relationships", TraversalPolicy(
            frozenset({Direction.INCOMING, Direction.OUTGOING}), transitive=True), provenance)
        edges = (
            Edge("fixture.first", "core", "fixture.hidden", "related", ("semantic",), provenance),
            Edge("fixture.second", "fixture.hidden", self.reference, "related", ("semantic",), provenance),
        )
        graph = EdgeRegistry(Path("/"), (Provider("fixture", GraphContribution(
            tuple(Node(key, provenance=provenance) for key in ("core", "fixture.hidden", self.reference)),
            (group,), edges)),))
        self.assertEqual(len(graph.traverse_group("core", "semantic", Direction.OUTGOING, transitive=True).steps), 2)
        view = ApplicationView(replace(self.compiled, graph=graph), c.SnapshotHandle.from_value(self.snapshot))
        result = view.related("core", ("semantic",), "outgoing", True).as_contract()
        self.assertEqual(result["relationships"], [])
        self.assertEqual(result["next_operations"], [])

    def test_router_presentation_change_requires_explicit_renewal(self):
        files = dict(self.files)
        path = "evaluation/standards-effectiveness/router-projection.toml"
        old = self.compiled.router.facts[0].prompt
        self.assertIn(old.encode(), files[path])
        files[path] = files[path].replace(old.encode(), b"Describe the selected task activities.", 1)
        changed = compile_files(files)
        self.assertNotEqual(changed.materials["router"].binding, self.compiled.materials["router"].binding)
        self.assertEqual(changed.supporting.exposure_state("router", changed.materials["router"].binding), "needs-review")

    def test_unexpected_observation_failure_returns_no_private_context(self):
        with patch.object(ApplicationView, "read", side_effect=RuntimeError(PRIVATE)):
            with self.assertLogs("tools.standards_engine.standards_engine.context_projection", level="ERROR") as captured:
                value = self.read()
        self.assertEqual(value["code"], "APPLICATION.INTERNAL_UNAVAILABLE")
        self.assertNotIn(PRIVATE, json.dumps(value))
        self.assertNotIn(PRIVATE, "\n".join(captured.output))

    def test_unsupported_capture_is_preserved_and_classified(self):
        files = {path: value for path, value in self.files.items() if path not in {APPLICATION_CONTENT, DECISION_PROVENANCE}}
        captured = self.engine._snapshots.create_snapshot(CapturedContent("old-fixture", (
            SnapshotFile(SnapshotPath.parse(path), value) for path, value in files.items())))
        handle = self.engine._snapshot_handle(captured.snapshot)
        before = self.engine._snapshots.load_content(captured.snapshot)
        value = self.facade.read({"snapshot": handle, "target": "core"})
        self.assertEqual(value["code"], "APPLICATION.UNSUPPORTED_CAPTURE", value)
        self.assertEqual(self.engine._snapshots.load_content(captured.snapshot), before)

    def test_catalog_has_no_authoring_schema_closure(self):
        from tools.standards_engine.standards_engine.mcp import tool_catalog
        for advanced in (False, True):
            catalog = tool_catalog(ROOT, purpose="application", advanced=advanced)
            names = {tool["name"] for tool in catalog}
            self.assertLessEqual(names, {"route", "read", "related", "routing_facts", "query", "inspect"})
            serialized = json.dumps(catalog)
            for hidden in ("rationale", "ChangePurpose", "DecisionProvenanceRecord", "ProposalRevisionHandle"):
                self.assertNotIn(hidden, serialized)


    def test_whole_module_discovers_references_owned_by_its_policy_units(self):
        from tools.graph_engine.graph_engine import (
            Direction, Edge, EdgeGroup, EdgeRegistry, GraphContribution,
            Node, Provenance, TraversalPolicy,
        )
        from tools.standards_graph.standards_graph import Provider
        from tools.standards_metadata.standards_metadata import ApplicationExposure
        owner = "topic.code-design"
        unit = self.compiled.corpus.policy_unit_corpus.for_module(owner)[0]
        supporting = replace(self.compiled.supporting, exposure={
            **self.compiled.supporting.exposure,
            owner: ApplicationExposure(owner, self.compiled.materials[owner].binding),
        })
        provenance = Provenance("scope-fixture", "provider", "scope fixture")
        group = EdgeGroup("semantic", "Supplementary relationships", TraversalPolicy(
            frozenset({Direction.INCOMING, Direction.OUTGOING})), provenance)
        edge = Edge("scope.reference", unit.id, self.reference,
                    "reference-projection", ("semantic",), provenance)
        graph = EdgeRegistry(Path("/"), (Provider("scope-fixture", GraphContribution(
            tuple(Node(key, provenance=provenance) for key in ("core", owner, unit.id, self.reference)),
            (group,), (edge,))),))
        view = ApplicationView(replace(self.compiled, graph=graph, supporting=supporting), c.SnapshotHandle.from_value(self.snapshot))
        related = view.related(owner, ("semantic",), "outgoing", False).as_contract()
        self.assertEqual([entry["target"] for entry in related["relationships"]], [self.reference])
        self.assertEqual([entry["target"] for entry in related["next_operations"]], [self.reference])
        full = view.read(owner, "full").as_contract()
        self.assertEqual(full["related"], related["relationships"])

    def test_invalid_host_purpose_creates_no_store(self):
        with tempfile.TemporaryDirectory(prefix="invalid-purpose-") as temporary:
            store = Path(temporary) / "state" / "engine.sqlite3"
            with self.assertRaises(ValueError):
                StandardsEngine.open_repository(ROOT, purpose="request-controlled", store_path=store)
            self.assertFalse(store.parent.exists())
