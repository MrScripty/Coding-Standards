from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    load_router_projection,
)
from tools.standards_metadata.standards_metadata import (
    DirectoryContentSource,
    RecordingContentSource,
    load_canonical_module_corpus,
)


REPO_ROOT = Path(__file__).resolve().parents[3]


class RouterProjectionTest(unittest.TestCase):
    def test_repository_projection_compiles_registered_modules_and_programs(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        projection = load_router_projection(REPO_ROOT, modules)

        self.assertEqual(projection.owner, "router")
        self.assertEqual(projection.base_modules, ("router",))

        boundaries = next(
            fact for fact in projection.facts if fact.id == "routing.boundaries"
        )
        self.assertEqual(boundaries.semantic_revision, 2)
        self.assertIn("generated-contract", boundaries.values)

        activities = next(
            fact for fact in projection.facts if fact.id == "routing.activities"
        )
        self.assertEqual(activities.semantic_revision, 2)
        self.assertIn("uncertainty-reduction", activities.values)

        generated_contract = next(
            rule
            for rule in projection.rules
            if rule.id == "route.boundary.generated-contract"
        )
        self.assertEqual(
            generated_contract.target,
            "profile.boundary.generated-contract",
        )
        self.assertEqual(
            generated_contract.program.referenced_facts,
            ("routing.boundaries",),
        )
        self.assertEqual(
            generated_contract.program.as_expression(),
            {
                "operator": "contains",
                "fact": "routing.boundaries",
                "value": "generated-contract",
            },
        )

        development_proportionality = next(
            rule
            for rule in projection.rules
            if rule.id == "route.workflow.development-proportionality"
        )
        self.assertEqual(
            development_proportionality.target,
            "workflow.development-proportionality",
        )
        self.assertEqual(
            development_proportionality.program.referenced_facts,
            ("routing.activities",),
        )
        self.assertEqual(
            development_proportionality.program.as_expression(),
            {
                "operator": "contains",
                "fact": "routing.activities",
                "value": "uncertainty-reduction",
            },
        )

    def route_task(self, **selections: list[str]) -> set[str]:
        modules = load_canonical_module_corpus(REPO_ROOT)
        projection = load_router_projection(REPO_ROOT, modules)
        facts = projection.fact_schema.bind({
            fact.id: {"type": "enum-set", "state": "known",
                      "value": selections.get(fact.id.removeprefix("routing."), [])}
            for fact in projection.facts
        })
        selected = set(projection.base_modules)
        for rule in projection.rules:
            if rule.program.evaluate(facts).truth.value == "true":
                selected.add(rule.target)
        pending = list(selected)
        while pending:
            module = modules.resolve(pending.pop())
            assert module is not None
            for dependency in module.requires:
                if dependency not in selected:
                    selected.add(dependency)
                    pending.append(dependency)
        return selected

    def test_small_rust_fix_omits_specialized_decisions(self) -> None:
        selected = self.route_task(activities=["implementation", "verification"],
                                   applications=["library"], languages=["rust"])
        self.assertEqual(selected, {"core", "router", "workflow.implementation",
                                   "workflow.verification", "profile.application.library",
                                   "profile.language.rust"})

    def test_rust_crossings_select_language_specific_safety(self) -> None:
        selected = self.route_task(languages=["rust", "rust-unsafe"],
                                   boundaries=["interop", "language-bindings"],
                                   topics=["security"])
        self.assertTrue({"profile.language.rust.unsafe", "profile.language.rust.interop",
                         "profile.language.rust.language-bindings",
                         "profile.language.rust.security"} <= selected)
        generic = self.route_task(boundaries=["interop", "language-bindings"],
                                  topics=["security"])
        self.assertFalse(any(x.startswith("profile.language.rust") for x in generic))

    def test_activity_prerequisites_do_not_invent_publication_or_history_work(self) -> None:
        for facts in ({"boundaries": ["generated-contract"]},
                      {"activities": ["tooling"], "languages": ["rust-tooling"]}):
            with self.subTest(facts=facts):
                selected = self.route_task(**facts)
                self.assertNotIn("workflow.release", selected)
                self.assertNotIn("workflow.commit", selected)
        self.assertIn("workflow.release", self.route_task(activities=["release"]))
        self.assertIn("workflow.commit", self.route_task(activities=["commit"]))

    def test_ui_text_and_api_changes_do_not_invent_unrelated_concerns(self) -> None:
        ui = self.route_task(activities=["implementation", "verification"],
                             languages=["typescript"], applications=["frontend"])
        self.assertNotIn("topic.contracts", ui)
        self.assertIn("topic.accessibility", ui)
        api = self.route_task(languages=["rust-api"])
        self.assertFalse({"topic.architecture", "topic.dependencies", "topic.resilience",
                          "profile.application.library", "workflow.release"} & api)
        self.assertIn("topic.contracts", api)

    def test_detail_pages_are_selected_from_the_affected_decision(self) -> None:
        self.assertIn("topic.contracts.schemas",
                      self.route_task(boundaries=["generated-contract"]))
        self.assertIn("topic.contracts.protocols", self.route_task(boundaries=["ipc"]))
        self.assertIn("topic.contracts.evolution", self.route_task(boundaries=["persistence"]))
        self.assertIn("workflow.verification.oracles",
                      self.route_task(details=["workflow.verification.oracles"]))
        self.assertNotIn("workflow.verification.oracles",
                         self.route_task(activities=["verification"]))
        self.assertNotIn("topic.architecture.replay", self.route_task(topics=["architecture"]))
        self.assertIn("topic.architecture.replay",
                      self.route_task(details=["topic.architecture.replay"]))

    def test_every_normative_module_has_an_executable_route(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        projection = load_router_projection(REPO_ROOT, modules)
        reachable = self.route_task(**{
            fact.id.removeprefix("routing."): list(fact.values)
            for fact in projection.facts
        })
        self.assertEqual({m.module_id for m in modules.normative_modules} - reachable, set())

    def test_missing_detail_facts_remain_unknown(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        projection = load_router_projection(REPO_ROOT, modules)
        rule = next(r for r in projection.rules if r.target == "topic.architecture.replay")
        result = rule.program.evaluate(projection.fact_schema.bind({}))
        self.assertEqual(result.unresolved_facts, ("routing.details",))

    def test_canonical_guidance_links_resolve_current_headings(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        canonical = {m.path for m in modules.modules}
        for module in modules.normative_modules:
            source = REPO_ROOT / module.path
            # Fenced examples are not navigation links or document headings.
            text = re.sub(r"(?ms)^```.*?^```[^\n]*", "", source.read_text())
            for destination in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if ":" in destination or destination.startswith("/"):
                    continue
                path, _, anchor = destination.partition("#")
                target = (source.parent / path).resolve() if path else source
                with self.subTest(source=module.path, destination=destination):
                    self.assertTrue(target.is_file())
                    if not target.is_file():
                        continue
                    relative = target.relative_to(REPO_ROOT).as_posix()
                    self.assertFalse(relative not in canonical and
                                     (relative.startswith("languages/") or
                                      relative.endswith("-STANDARDS.md")),
                                     "Current guidance links to a retired policy owner")
                    if not anchor or target.suffix != ".md":
                        continue
                    content = re.sub(r"(?ms)^```.*?^```[^\n]*", "", target.read_text())
                    headings = re.findall(r"(?m)^#{1,6} (.+)$", content)
                    anchors = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-")
                               for h in headings}
                    anchors.update(re.findall(r'<a[^>]+(?:id|name)="([^"]+)"', content))
                    self.assertIn(anchor, anchors)

    def test_projection_rejects_target_drift_from_router_tables(self) -> None:
        modules = load_canonical_module_corpus(REPO_ROOT)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evaluation/standards-effectiveness").mkdir(parents=True)
            shutil.copy2(REPO_ROOT / "STANDARDS-ROUTER.md", root / "STANDARDS-ROUTER.md")
            projection = root / "evaluation/standards-effectiveness/router-projection.toml"
            shutil.copy2(
                REPO_ROOT / "evaluation/standards-effectiveness/router-projection.toml",
                projection,
            )
            text = projection.read_text(encoding="utf-8")
            marker = '\n[[rules]]\nid = "route.topic.security"'
            projection.write_text(text.split(marker, 1)[0] + "\n", encoding="utf-8")

            with self.assertRaises(AnalysisError) as caught:
                load_router_projection(root, modules)
            self.assertEqual(caught.exception.failure.code, "ROUTER_PROJECTION.INVALID")

    def test_repository_and_frozen_sources_produce_equal_projection(self) -> None:
        recording = RecordingContentSource(DirectoryContentSource(REPO_ROOT))
        modules = load_canonical_module_corpus(recording)
        repository_projection = load_router_projection(recording, modules)

        frozen = recording.freeze()
        frozen_modules = load_canonical_module_corpus(frozen)
        frozen_projection = load_router_projection(frozen, frozen_modules)

        self.assertEqual(repository_projection, frozen_projection)
        self.assertIn("STANDARDS-ROUTER.md", recording.requested_paths)
        self.assertIn(
            "evaluation/standards-effectiveness/router-projection.toml",
            recording.requested_paths,
        )


if __name__ == "__main__":
    unittest.main()
