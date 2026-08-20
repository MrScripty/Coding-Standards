from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..policy_impact import load_policy_impact


@dataclass(frozen=True, slots=True)
class PolicyImpactCase:
    id: str
    manifest: str
    expected: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PolicyImpactCheck:
    id: str
    manifest: str | None
    cases: tuple[PolicyImpactCase, ...] | None

    def run(self, context: CheckContext) -> list[Diagnostic]:
        suite_paths = dict(context.registered_suite_paths)
        if self.manifest is not None:
            load_policy_impact(
                context.repo_root,
                self.manifest,
                suite_paths,
                suite=context.suite_id,
                check=self.id,
            )
            return []

        diagnostics: list[Diagnostic] = []
        assert self.cases is not None
        for case in self.cases:
            try:
                load_policy_impact(
                    context.repo_root,
                    case.manifest,
                    suite_paths,
                    suite=context.suite_id,
                    check=self.id,
                )
                observed: tuple[str, ...] = ()
            except EngineError as error:
                observed = (error.diagnostic.code,)
            if observed != case.expected:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.POLICY_IMPACT_FIXTURE",
                        "invalid",
                        "policy-impact fixture diagnostics do not match",
                        suite=context.suite_id,
                        check=self.id,
                        field=case.id,
                        expected=",".join(case.expected) or "pass",
                        observed=",".join(observed) or "pass",
                    )
                )
        return diagnostics


def _strings(value: object, *, suite: str, check: str, field: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING_LIST",
                "invalid",
                "field must contain unique non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


def parse_policy_impact_check(raw: dict[str, Any], suite_id: str) -> PolicyImpactCheck:
    allowed = {"id", "type", "manifest", "cases"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "policy impact check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    has_manifest = "manifest" in raw
    has_cases = "cases" in raw
    if has_manifest == has_cases:
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_MODE",
                "invalid",
                "policy impact check requires exactly one of manifest or cases",
                suite=suite_id,
                check=check_id,
            )
        )
    if has_manifest:
        manifest = raw["manifest"]
        if not isinstance(manifest, str) or not manifest:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MANIFEST",
                    "invalid",
                    "manifest must be a non-empty repository path",
                    suite=suite_id,
                    check=check_id,
                )
            )
        return PolicyImpactCheck(check_id, manifest, None)

    raw_cases = raw["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise EngineError(
            Diagnostic(
                "CONFIG.POLICY_IMPACT_CASES",
                "invalid",
                "fixture mode requires at least one case",
                suite=suite_id,
                check=check_id,
            )
        )
    cases: list[PolicyImpactCase] = []
    seen: set[str] = set()
    for raw_case in raw_cases:
        if not isinstance(raw_case, dict) or set(raw_case) != {"id", "manifest", "expected"}:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_CASE",
                    "invalid",
                    "case requires exactly id, manifest, and expected",
                    suite=suite_id,
                    check=check_id,
                )
            )
        case_id = raw_case["id"]
        manifest = raw_case["manifest"]
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_CASE_ID",
                    "invalid",
                    "case ids must be unique non-empty strings",
                    suite=suite_id,
                    check=check_id,
                    observed=str(case_id),
                )
            )
        if not isinstance(manifest, str) or not manifest:
            raise EngineError(
                Diagnostic(
                    "CONFIG.POLICY_IMPACT_MANIFEST",
                    "invalid",
                    "case manifest must be a non-empty repository path",
                    suite=suite_id,
                    check=check_id,
                    field=case_id,
                )
            )
        seen.add(case_id)
        cases.append(
            PolicyImpactCase(
                case_id,
                manifest,
                _strings(
                    raw_case["expected"],
                    suite=suite_id,
                    check=check_id,
                    field=f"{case_id}.expected",
                ),
            )
        )
    return PolicyImpactCheck(check_id, None, tuple(cases))
