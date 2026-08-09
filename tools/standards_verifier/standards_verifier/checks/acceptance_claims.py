from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file


def _domain(value: Any, field: str, suite: str, check: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.CLAIM_DOMAIN",
                "invalid",
                "claim domain must contain unique non-empty strings",
                suite=suite,
                check=check,
                field=field,
            )
        )
    return tuple(value)


@dataclass(frozen=True, slots=True)
class Claim:
    kind: str
    environment: str
    mode: str


@dataclass(frozen=True, slots=True)
class AcceptanceClaimsCheck:
    id: str
    path: str
    kinds: tuple[str, ...]
    environments: tuple[str, ...]
    modes: tuple[str, ...]

    def _claims(
        self,
        value: str,
        *,
        context: CheckContext,
        row: int,
        field: str,
    ) -> tuple[Claim, ...]:
        raw_claims = value.split(";")
        if not value or any(not claim for claim in raw_claims):
            raise EngineError(
                Diagnostic(
                    "CLAIM.INVALID",
                    "invalid",
                    "claim set must contain non-empty semicolon-separated claims",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    row=row,
                    field=field,
                    observed=value,
                )
            )
        if len(set(raw_claims)) != len(raw_claims):
            raise EngineError(
                Diagnostic(
                    "CLAIM.DUPLICATE",
                    "invalid",
                    "claim set contains a duplicate claim",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    row=row,
                    field=field,
                )
            )
        claims = []
        for raw_claim in raw_claims:
            parts = raw_claim.split("@")
            if (
                len(parts) != 3
                or parts[0] not in self.kinds
                or parts[1] not in self.environments
                or parts[2] not in self.modes
            ):
                raise EngineError(
                    Diagnostic(
                        "CLAIM.INVALID",
                        "invalid",
                        "claim must match the configured kind@environment@mode grammar",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=row,
                        field=field,
                        observed=raw_claim,
                    )
                )
            claims.append(Claim(*parts))
        return tuple(claims)

    @staticmethod
    def _is_satisfied(required: Claim, observed: tuple[Claim, ...]) -> bool:
        if required in observed:
            return True
        if required.mode != "either":
            return False
        return any(
            candidate.kind == required.kind
            and candidate.environment == required.environment
            and candidate.mode in {"automated", "manual"}
            for candidate in observed
        )

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        source = contained_file(root, self.path, suite=context.suite_id, check=self.id)
        try:
            with source.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle, delimiter="\t"))
        except UnicodeDecodeError as error:
            raise EngineError(
                Diagnostic(
                    "INPUT.INVALID_UTF8",
                    "invalid",
                    str(error),
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                )
            ) from error
        expected_header = [
            "case",
            "required_claims",
            "observed_claims",
            "expected",
        ]
        if not rows or rows[0] != expected_header:
            raise EngineError(
                Diagnostic(
                    "TABLE.HEADER_CONTRACT",
                    "invalid",
                    "acceptance claim table requires its canonical header",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected="\t".join(expected_header),
                    observed="\t".join(rows[0]) if rows else "absent",
                )
            )

        diagnostics = []
        seen_cases = set()
        for line_number, values in enumerate(rows[1:], start=2):
            if len(values) != len(expected_header):
                raise EngineError(
                    Diagnostic(
                        "TABLE.ROW_WIDTH",
                        "invalid",
                        "acceptance claim row width does not match the header",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        expected=str(len(expected_header)),
                        observed=str(len(values)),
                    )
                )
            case_id, required_value, observed_value, expected = values
            if not case_id or case_id in seen_cases:
                raise EngineError(
                    Diagnostic(
                        "TABLE.DUPLICATE_CASE" if case_id else "TABLE.EMPTY_VALUE",
                        "invalid",
                        "acceptance claim case must be unique and non-empty",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        field="case",
                        observed=case_id,
                    )
                )
            seen_cases.add(case_id)
            if expected not in {"satisfied", "unsatisfied"}:
                raise EngineError(
                    Diagnostic(
                        "TABLE.VALUE_OUTSIDE_DOMAIN",
                        "invalid",
                        "acceptance claim expected value is invalid",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        field="expected",
                        expected="satisfied,unsatisfied",
                        observed=expected,
                    )
                )
            required = self._claims(
                required_value,
                context=context,
                row=line_number,
                field="required_claims",
            )
            observed = self._claims(
                observed_value,
                context=context,
                row=line_number,
                field="observed_claims",
            )
            actual = (
                "satisfied"
                if all(self._is_satisfied(claim, observed) for claim in required)
                else "unsatisfied"
            )
            if actual != expected:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.ACCEPTANCE_CLAIMS",
                        "invalid",
                        "acceptance claim satisfaction does not match",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        expected=expected,
                        observed=actual,
                    )
                )
        return diagnostics


def parse_acceptance_claims_check(
    raw: dict[str, Any], suite_id: str
) -> AcceptanceClaimsCheck:
    allowed = {"id", "type", "path", "kinds", "environments", "modes"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "acceptance claims check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    path = raw.get("path")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    if not isinstance(path, str) or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "path must be a non-empty string",
                suite=suite_id,
                check=check_id,
            )
        )
    kinds = _domain(raw.get("kinds"), "kinds", suite_id, check_id)
    environments = _domain(
        raw.get("environments"), "environments", suite_id, check_id
    )
    modes = _domain(raw.get("modes"), "modes", suite_id, check_id)
    if set(modes) != {"automated", "manual", "either"}:
        raise EngineError(
            Diagnostic(
                "CONFIG.CLAIM_MODES",
                "invalid",
                "claim modes must be exactly automated, manual, and either",
                suite=suite_id,
                check=check_id,
                observed=",".join(modes),
            )
        )
    return AcceptanceClaimsCheck(check_id, path, kinds, environments, modes)
