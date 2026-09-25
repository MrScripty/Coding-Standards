"""Focused coverage preparation with synthetic already-compiled input records.

These tests exercise real manifest loading, identities and coverage owners. The
small structural records deliberately exclude graph/corpus parser qualification.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import coverage
from tools.standards_analysis.standards_analysis.errors import AnalysisError
from tools.standards_metadata.standards_metadata.source import FrozenContentSource
from tools.standards_metadata.standards_metadata import suite_inputs
from tools.standards_metadata.tests.test_prepared_suite_dependencies import manifest_fixture


@dataclass(frozen=True)
class Unit:
    id: str
    module: str = "module.policy"
    semantic_revision: int = 1
    representation_digest: str = "sha256:" + "1" * 64
    structural_digest: str = "sha256:" + "2" * 64


@dataclass(frozen=True)
class Semantics:
    source: str
    consumer: str
    evidence_owner: str
    dependency_fingerprint: str
    applicability_program: object
    relation: str = "documentation-projection"


class CountingSemantics(dict):
    def __init__(self, values):
        super().__init__(values)
        self.passes = self.visits = 0

    def items(self):
        self.passes += 1
        for entry in super().items():
            self.visits += 1
            yield entry


def coverage_fixture(policy_count=4, edges_per_policy=3, payload=b"shared input\n"):
    files, direct = manifest_fixture(payload)
    files.update({
        "policy.md": b"# Policy\n",
        "edges.toml": b"schema_version = 1\nsources = []\n",
        "horizon.toml": (
            'schema_version = 1\nid = "audit-horizon.policy-impact-consumers"\n'
            'provider = "standards-analysis:policy-impact-consumer-horizon"\n'
            'version = 6\nsuite_registry = "registry.toml"\n'
            'suite_inputs = "manifest.json"\nedge_source_registry = "edges.toml"\n'
        ).encode(),
    })
    units = tuple(Unit(f"policy.p{index:04d}") for index in range(policy_count))
    corpus = SimpleNamespace(
        policy_units=units,
        modules=(SimpleNamespace(path="policy.md", module_id="module.policy"),),
        module_corpus=SimpleNamespace(members=("policy.md",)),
        policy_unit_corpus=SimpleNamespace(sources=()),
    )
    program = SimpleNamespace(dependency_digest="sha256:" + "3" * 64)
    semantics = {}
    for unit in units:
        for index in range(edges_per_policy):
            name = f"edge.{unit.id}.r{index:04d}"
            semantics[name] = Semantics(
                unit.id, "module.policy", ("suite:left", "suite:right", "review:consumer")[index % 3],
                suite_inputs.file_digest(name.encode()), program,
            )
    compiled = SimpleNamespace(
        semantics=semantics, artifacts={}, input_sources=(),
        fact_schema=SimpleNamespace(digest="sha256:" + "4" * 64),
        relationship_kind_contract_version=2,
        provider_contract_digest="sha256:" + "5" * 64,
    )
    return FrozenContentSource(files), corpus, compiled, direct


def prepared_fixture(policy_count=4, edges_per_policy=3, payload=b"shared input\n"):
    source, corpus, compiled, direct = coverage_fixture(policy_count, edges_per_policy, payload)
    horizon = coverage.load_coverage_horizon(source, corpus, compiled, "horizon.toml")
    return corpus, compiled, horizon


def result_projection(result):
    """Complete public coverage material, excluding internal prepared indexes."""
    horizon = result.horizon
    return {
        "horizon": {"id": horizon.id, "provider": horizon.provider, "version": horizon.version,
                    "digest": horizon.digest, "members": [m.as_projection() for m in horizon.members],
                    "input_sources": list(horizon.input_sources),
                    "suite_inputs": horizon.suite_inputs.as_projection(),
                    "consumer_members": {key: value.as_projection() for key, value in horizon.consumer_members.items()}},
        "views": {key: value.as_projection() for key, value in result.views.items()},
        "requirements": {key: value.as_projection() for key, value in result.requirements.items()},
        "requirement_ids": {key: coverage.coverage_requirement_id(result.requirements[key], view)
                            for key, view in result.views.items()},
        "input_sources": list(result.input_sources),
    }


class CoveragePreparationTest(unittest.TestCase):
    def test_bulk_views_and_requirements_equal_individual_derivation(self):
        for count in (1, 4, 32):
            corpus, compiled, horizon = prepared_fixture(count)
            with self.subTest(policies=count):
                result = coverage.compile_coverage_definitions(corpus, compiled, horizon)
                expected = {unit.id: coverage.derive_coverage_view(unit, compiled, horizon)
                            for unit in corpus.policy_units}
                self.assertEqual(result.views, expected)
                self.assertEqual(result.requirements, {
                    key: coverage.derive_coverage_requirement(view) for key, view in expected.items()})
                self.assertIs(result.horizon, horizon)
                self.assertEqual(result.input_sources, horizon.input_sources)

    def test_bulk_preparation_visits_each_relationship_once(self):
        corpus, compiled, horizon = prepared_fixture(32)
        compiled.semantics = CountingSemantics(compiled.semantics)
        result = coverage.compile_coverage_definitions(corpus, compiled, horizon)
        self.assertEqual(compiled.semantics.passes, 1)
        self.assertEqual(compiled.semantics.visits, len(compiled.semantics))
        self.assertEqual(sum(len(view.relationship_fingerprints) for view in result.views.values()), 96)

    def test_horizon_and_all_views_reuse_the_loader_dependency_preparation(self):
        source, corpus, compiled, direct = coverage_fixture(32)
        original = suite_inputs.SuiteInputManifest._derive_dependency
        calls = []
        def observed(manifest, suite_id, definitions):
            calls.append(suite_id)
            return original(manifest, suite_id, definitions)
        with patch.object(suite_inputs.SuiteInputManifest, "_derive_dependency", observed):
            horizon = coverage.load_coverage_horizon(source, corpus, compiled, "horizon.toml")
            for _ in range(2):
                coverage.compile_coverage_definitions(corpus, compiled, horizon)
        self.assertEqual(calls, [item.id for item in direct.suites])

    def test_relationship_order_and_repeated_evidence_owners_preserve_results(self):
        corpus, compiled, horizon = prepared_fixture(4, 8)
        expected = result_projection(coverage.compile_coverage_definitions(corpus, compiled, horizon))
        compiled.semantics = dict(reversed(tuple(compiled.semantics.items())))
        actual = result_projection(coverage.compile_coverage_definitions(corpus, compiled, horizon))
        self.assertEqual(actual, expected)
        for view in actual["views"].values():
            self.assertEqual(len(view["relationship_fingerprints"]), 8)
            member_ids = [member["id"] for member in view["horizon"]["members"]]
            self.assertEqual(member_ids.count("suite-dependency:left"), 1)
            self.assertEqual(member_ids.count("suite-dependency:right"), 1)

    def test_unrelated_sources_are_ignored_without_reading_their_other_fields(self):
        corpus, compiled, horizon = prepared_fixture()
        expected = result_projection(coverage.compile_coverage_definitions(corpus, compiled, horizon))
        compiled.semantics["edge.unrelated"] = SimpleNamespace(source="another.policy")
        actual = result_projection(coverage.compile_coverage_definitions(corpus, compiled, horizon))
        self.assertEqual(actual, expected)

    def test_policy_without_relationships_still_has_a_complete_view(self):
        corpus, compiled, horizon = prepared_fixture()
        missing = corpus.policy_units[-1].id
        compiled.semantics = {key: value for key, value in compiled.semantics.items() if value.source != missing}
        result = coverage.compile_coverage_definitions(corpus, compiled, horizon)
        view = result.views[missing]
        self.assertEqual(view.relationship_fingerprints, ())
        self.assertEqual(view.horizon_members, ())
        self.assertEqual(view, coverage.derive_coverage_view(corpus.policy_units[-1], compiled, horizon))

    def test_empty_corpus_does_not_scan_relationships(self):
        corpus, compiled, horizon = prepared_fixture(0)
        compiled.semantics = CountingSemantics({"unrelated": SimpleNamespace(source="other")})
        result = coverage.compile_coverage_definitions(corpus, compiled, horizon)
        self.assertEqual(result.views, {})
        self.assertEqual(result.requirements, {})
        self.assertEqual(compiled.semantics.passes, 0)

    def test_each_compilation_uses_its_own_relationship_assignment(self):
        corpus, compiled, horizon = prepared_fixture(2)
        previous = coverage.compile_coverage_definitions(corpus, compiled, horizon)
        name = next(iter(compiled.semantics))
        compiled.semantics[name] = replace(compiled.semantics[name], source=corpus.policy_units[1].id)
        current = coverage.compile_coverage_definitions(corpus, compiled, horizon)
        self.assertNotEqual(current.views, previous.views)
        self.assertEqual(len(previous.views[corpus.policy_units[0].id].relationship_fingerprints), 3)
        self.assertEqual(len(current.views[corpus.policy_units[0].id].relationship_fingerprints), 2)
        self.assertEqual(len(current.views[corpus.policy_units[1].id].relationship_fingerprints), 4)

    def test_changed_manifest_material_changes_relevant_requirement_ids(self):
        first = prepared_fixture(payload=b"first material")
        second = prepared_fixture(payload=b"second material")
        before = result_projection(coverage.compile_coverage_definitions(*first))
        after = result_projection(coverage.compile_coverage_definitions(*second))
        self.assertNotEqual(before["requirement_ids"], after["requirement_ids"])
        self.assertNotEqual(first[2].suite_inputs.dependency("left"), second[2].suite_inputs.dependency("left"))
        self.assertEqual(first[2].suite_inputs.dependency("other"), second[2].suite_inputs.dependency("other"))

    def test_direct_unprepared_manifest_keeps_the_standalone_coverage_path(self):
        corpus, compiled, horizon = prepared_fixture()
        direct_horizon = replace(horizon, suite_inputs=replace(horizon.suite_inputs))
        before = result_projection(coverage.compile_coverage_definitions(corpus, compiled, horizon))
        after = result_projection(coverage.compile_coverage_definitions(corpus, compiled, direct_horizon))
        self.assertEqual(before, after)

    def test_failures_preserve_diagnostics_and_sorted_first_failure(self):
        for change, code in (
            ({"consumer": "missing.consumer"}, "COVERAGE.CONSUMER_MISSING"),
            ({"evidence_owner": "invalid-owner"}, "COVERAGE.EVIDENCE_OWNER"),
            ({"evidence_owner": "suite:unknown"}, "COVERAGE.EVIDENCE_SUITE_MISSING"),
        ):
            corpus, compiled, horizon = prepared_fixture(1)
            names = sorted(compiled.semantics)
            compiled.semantics[names[0]] = replace(compiled.semantics[names[0]], **change)
            compiled.semantics[names[1]] = replace(compiled.semantics[names[1]], consumer="later.missing")
            compiled.semantics = dict(reversed(tuple(compiled.semantics.items())))
            failures = []
            for operation in (
                lambda: coverage.compile_coverage_definitions(corpus, compiled, horizon),
                lambda: coverage.derive_coverage_view(corpus.policy_units[0], compiled, horizon),
            ):
                with self.subTest(code=code), self.assertRaises(AnalysisError) as error:
                    operation()
                failures.append(asdict(error.exception.failure))
            self.assertEqual(failures[0], failures[1])
            self.assertEqual(failures[0]["code"], code)

    def test_single_view_semantic_overrides_are_preserved(self):
        corpus, compiled, horizon = prepared_fixture(1)
        unit = corpus.policy_units[0]
        baseline = coverage.derive_coverage_view(unit, compiled, horizon)
        overridden = coverage.derive_coverage_view(unit, compiled, horizon,
                     semantic_revision=2, representation_digest="new representation", structural_digest="new structure")
        self.assertEqual(overridden, replace(baseline, semantic_revision=2,
                         representation_digest="new representation", structural_digest="new structure"))


if __name__ == "__main__":
    unittest.main()
