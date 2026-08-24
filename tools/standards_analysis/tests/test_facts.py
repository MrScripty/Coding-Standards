from __future__ import annotations

import unittest

from tools.standards_applicability.standards_applicability import compile_fact_schema
from tools.standards_analysis.standards_analysis import (
    AnalysisError,
    AuthorizationReference,
    ChangeDescriptor,
    ChangeKind,
    EvidenceReference,
    ReviewScope,
    build_analysis_context,
    build_fact_requirement,
    classify_changes,
    observe_fact,
    resolve_fact_requirements,
    validate_observation,
)
from tools.standards_metadata.standards_metadata import PolicyUnit, PolicyUnitCorpus


SCOPE = ReviewScope("whole-artifact")


def unit(representation: str) -> PolicyUnit:
    return PolicyUnit(
        "workflow.test.policy",
        "workflow.test",
        ("Policy",),
        1,
        (),
        (),
        (),
        "module.md",
        "## Policy\n\nText.\n",
        "sha256:" + representation * 64,
        "sha256:" + "c" * 64,
        "units.toml",
    )


def context(representation: str = "b"):
    before = unit("a")
    after = unit(representation)
    changes = classify_changes(
        PolicyUnitCorpus("registry.toml", (), (before,), ()),
        PolicyUnitCorpus("registry.toml", (), (after,), ()),
        (
            ChangeDescriptor(
                ChangeKind.MODIFICATION,
                (before.id,),
                (after.id,),
                SCOPE,
            ),
        ),
    )
    return build_analysis_context(changes)


def schema(*, prompt: str = "Is review required?", aliases=(), revision: int = 1):
    return compile_fact_schema(
        {
            "kind": "applicability-fact-schema",
            "id": "facts.test",
            "version": 1,
            "facts": [
                {
                    "id": "change.requires-review",
                    "semantic_revision": revision,
                    "type": "boolean",
                    "nullable": False,
                    "aliases": list(aliases),
                    "meaning": "Whether this standards change requires review.",
                    "context_kind": "standards-change",
                    "answer_contract": "fact-value.v1",
                    "evidence_contract": "evidence-reference.v1",
                    "authorization_capability": "standards.analyze",
                    "prompt": prompt,
                }
            ],
        }
    )


def evidence():
    return EvidenceReference(
        "evidence.review",
        "sha256:" + "e" * 64,
        "repository-content",
        "1",
    )


def authorization():
    return AuthorizationReference(
        "authorization.review",
        "standards.analyze",
        "sha256:" + "f" * 64,
    )


class FactAuthorityTest(unittest.TestCase):
    def test_prompt_aliases_and_dependents_do_not_change_requirement_identity(self) -> None:
        first = schema(prompt="First wording.", aliases=("review",))
        second = schema(prompt="Second wording.", aliases=("needs-review",))
        first_requirement = build_fact_requirement(
            first.resolve("change.requires-review"),
            context(),
            ("proposed:edge.one",),
        )
        second_requirement = build_fact_requirement(
            second.resolve("change.requires-review"),
            context(),
            ("proposed:edge.two", "accepted:edge.three"),
        )

        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first_requirement.id, second_requirement.id)
        self.assertNotEqual(
            first_requirement.dependent_programs,
            second_requirement.dependent_programs,
        )

    def test_fact_or_context_semantics_change_requirement_identity(self) -> None:
        current = schema()
        revised = schema(revision=2)
        first = build_fact_requirement(
            current.resolve("change.requires-review"), context(), ()
        )
        changed_contract = build_fact_requirement(
            revised.resolve("change.requires-review"), context(), ()
        )
        changed_context = build_fact_requirement(
            current.resolve("change.requires-review"), context("d"), ()
        )

        self.assertNotEqual(first.id, changed_contract.id)
        self.assertNotEqual(first.id, changed_context.id)

    def test_observation_reuses_only_the_exact_requirement(self) -> None:
        selected_schema = schema()
        fact = selected_schema.resolve("change.requires-review")
        requirement = build_fact_requirement(fact, context(), ())
        observation = observe_fact(
            requirement,
            fact,
            {"type": "boolean", "state": "known", "value": True},
            (evidence(),),
            authorization(),
            {"repository-content": "1"},
        )
        resolution = resolve_fact_requirements((requirement,), (observation,))
        changed = build_fact_requirement(fact, context("d"), ())
        changed_resolution = resolve_fact_requirements((changed,), (observation,))

        self.assertEqual(resolution.reused, (observation,))
        self.assertEqual(resolution.unresolved, ())
        self.assertEqual(changed_resolution.reused, ())
        self.assertEqual(changed_resolution.unresolved, (changed,))

    def test_invalid_value_authorization_and_conflicting_observations_reject(self) -> None:
        selected_schema = schema()
        fact = selected_schema.resolve("change.requires-review")
        requirement = build_fact_requirement(fact, context(), ())
        with self.assertRaises(AnalysisError):
            observe_fact(
                requirement,
                fact,
                {"type": "boolean", "state": "known", "value": "yes"},
                (evidence(),),
                authorization(),
                {"repository-content": "1"},
            )
        with self.assertRaises(AnalysisError) as caught:
            observe_fact(
                requirement,
                fact,
                {"type": "boolean", "state": "known", "value": True},
                (evidence(),),
                AuthorizationReference(
                    "authorization.wrong",
                    "standards.review.consumer",
                    "sha256:" + "a" * 64,
                ),
                {"repository-content": "1"},
            )
        self.assertEqual(caught.exception.failure.outcome, "unauthorized")

        first = observe_fact(
            requirement,
            fact,
            {"type": "boolean", "state": "known", "value": True},
            (evidence(),),
            authorization(),
            {"repository-content": "1"},
        )
        second = observe_fact(
            requirement,
            fact,
            {"type": "boolean", "state": "known", "value": False},
            (evidence(),),
            authorization(),
            {"repository-content": "1"},
        )
        with self.assertRaises(AnalysisError) as caught:
            resolve_fact_requirements((requirement,), (first, second))
        self.assertEqual(caught.exception.failure.code, "FACT.OBSERVATION_CONFLICT")

    def test_observation_revalidates_provider_and_current_authorization(self) -> None:
        selected_schema = schema()
        fact = selected_schema.resolve("change.requires-review")
        requirement = build_fact_requirement(fact, context(), ())
        current = authorization()
        observation = observe_fact(
            requirement,
            fact,
            {"type": "boolean", "state": "known", "value": True},
            (evidence(),),
            current,
            {"repository-content": "1"},
        )
        self.assertEqual(
            validate_observation(
                observation,
                requirement,
                fact,
                current,
                {"repository-content": "1"},
            ),
            observation,
        )
        with self.assertRaises(AnalysisError) as caught:
            validate_observation(
                observation,
                requirement,
                fact,
                current,
                {"repository-content": "2"},
            )
        self.assertEqual(
            caught.exception.failure.code,
            "FACT.EVIDENCE_PROVIDER_UNAVAILABLE",
        )
        with self.assertRaises(AnalysisError) as caught:
            validate_observation(
                observation,
                requirement,
                fact,
                AuthorizationReference(
                    current.id,
                    current.capability,
                    "sha256:" + "b" * 64,
                ),
                {"repository-content": "1"},
            )
        self.assertEqual(
            caught.exception.failure.code,
            "FACT.AUTHORIZATION_STALE",
        )


if __name__ == "__main__":
    unittest.main()
