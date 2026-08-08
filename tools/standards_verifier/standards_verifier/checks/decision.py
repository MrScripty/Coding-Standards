from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file
from .predicates import Predicate, parse_predicate


@dataclass(frozen=True, slots=True)
class Rule:
    outcome: str
    when: Predicate


@dataclass(frozen=True, slots=True)
class DecisionCheck:
    id: str
    path: str
    expected_column: str
    default: str
    domains: dict[str, tuple[str, ...]]
    rules: tuple[Rule, ...]

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root
        if not isinstance(root, Path):
            raise TypeError("check context repository root must be a Path")
        source = contained_file(root, self.path, suite=context.suite_id, check=self.id)
        try:
            with source.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle, delimiter="\t"))
        except UnicodeDecodeError as error:
            raise EngineError(Diagnostic("INPUT.INVALID_UTF8", "invalid", str(error), suite=context.suite_id, check=self.id, path=self.path)) from error
        if len(rows) < 2:
            raise EngineError(Diagnostic("TABLE.EMPTY", "invalid", "decision table requires a header and at least one row", suite=context.suite_id, check=self.id, path=self.path))

        header = rows[0]
        if not header or any(not column for column in header) or len(set(header)) != len(header):
            raise EngineError(Diagnostic("TABLE.INVALID_HEADER", "invalid", "decision table header must contain unique non-empty columns", suite=context.suite_id, check=self.id, path=self.path))
        if header[0] != "case" or header[-1] != self.expected_column:
            raise EngineError(
                Diagnostic(
                    "TABLE.HEADER_CONTRACT",
                    "invalid",
                    "decision table must start with case and end with the configured expected column",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                )
            )
        if set(header) != set(self.domains):
            raise EngineError(
                Diagnostic(
                    "TABLE.DOMAIN_COLUMNS",
                    "invalid",
                    "configured domains must match decision table columns exactly",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected=",".join(sorted(header)),
                    observed=",".join(sorted(self.domains)),
                )
            )
        rule_fields = set().union(*(rule.when.fields() for rule in self.rules))
        unknown_rule_fields = rule_fields - set(header)
        if unknown_rule_fields:
            raise EngineError(Diagnostic("DECISION.UNKNOWN_FIELD", "invalid", "decision rule references an unknown table field", suite=context.suite_id, check=self.id, path=self.path, field=sorted(unknown_rule_fields)[0]))

        expected_domain = self.domains[self.expected_column]
        if expected_domain == ("*",) or self.default not in expected_domain:
            raise EngineError(Diagnostic("DECISION.DEFAULT_OUTCOME", "invalid", "default outcome must belong to the expected domain", suite=context.suite_id, check=self.id, observed=self.default))
        for rule in self.rules:
            if rule.outcome not in expected_domain:
                raise EngineError(Diagnostic("DECISION.RULE_OUTCOME", "invalid", "rule outcome must belong to the expected domain", suite=context.suite_id, check=self.id, observed=rule.outcome))

        diagnostics = []
        seen_cases = set()
        for line_number, values in enumerate(rows[1:], start=2):
            if len(values) != len(header):
                raise EngineError(Diagnostic("TABLE.ROW_WIDTH", "invalid", "decision row width does not match the header", suite=context.suite_id, check=self.id, path=self.path, row=line_number, expected=str(len(header)), observed=str(len(values))))
            row = dict(zip(header, values, strict=True))
            case_id = row["case"]
            if not case_id:
                raise EngineError(Diagnostic("TABLE.EMPTY_VALUE", "invalid", "decision value is empty", suite=context.suite_id, check=self.id, path=self.path, row=line_number, field="case"))
            if case_id in seen_cases:
                raise EngineError(Diagnostic("TABLE.DUPLICATE_CASE", "invalid", "decision case is duplicated", suite=context.suite_id, check=self.id, path=self.path, row=line_number, observed=case_id))
            seen_cases.add(case_id)
            for field, value in row.items():
                domain = self.domains[field]
                allowed = bool(value) if domain == ("*",) else value in domain
                if not allowed:
                    raise EngineError(Diagnostic("TABLE.VALUE_OUTSIDE_DOMAIN", "invalid", "decision value is outside its configured domain", suite=context.suite_id, check=self.id, path=self.path, row=line_number, field=field, observed=value))

            actual = self.default
            for rule in self.rules:
                if rule.when.evaluate(row):
                    actual = rule.outcome
                    break
            if actual != row[self.expected_column]:
                diagnostics.append(
                    Diagnostic(
                        code="ASSERT.DECISION_OUTCOME",
                        outcome="invalid",
                        message=f"decision outcome mismatch for case {case_id}",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        expected=row[self.expected_column],
                        observed=actual,
                    )
                )
        return diagnostics


def parse_decision_check(raw: dict[str, Any], suite_id: str) -> DecisionCheck:
    allowed = {"id", "type", "path", "expected_column", "default", "domains", "rules"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(Diagnostic("CONFIG.UNKNOWN_FIELD", "invalid", "decision check contains unknown fields", suite=suite_id, field=sorted(unknown)[0]))
    check_id = raw.get("id")
    path = raw.get("path")
    expected = raw.get("expected_column")
    default = raw.get("default")
    if not isinstance(check_id, str) or not check_id:
        raise EngineError(Diagnostic("CONFIG.CHECK_ID", "invalid", "check id must be a non-empty string", suite=suite_id))
    for field, value in (("path", path), ("expected_column", expected), ("default", default)):
        if not isinstance(value, str) or not value:
            raise EngineError(Diagnostic("CONFIG.STRING", "invalid", "field must be a non-empty string", suite=suite_id, check=check_id, field=field))

    raw_domains = raw.get("domains")
    if not isinstance(raw_domains, dict) or not raw_domains:
        raise EngineError(Diagnostic("CONFIG.DOMAINS", "invalid", "domains must be a non-empty TOML table", suite=suite_id, check=check_id))
    domains = {}
    for field, values in raw_domains.items():
        if not isinstance(field, str) or not field or not isinstance(values, list) or not values or any(not isinstance(value, str) or not value for value in values) or len(set(values)) != len(values):
            raise EngineError(Diagnostic("CONFIG.DOMAIN", "invalid", "each domain requires unique non-empty string values", suite=suite_id, check=check_id, field=str(field)))
        if "*" in values and (field != "case" or values != ["*"]):
            raise EngineError(Diagnostic("CONFIG.DOMAIN_WILDCARD", "invalid", "wildcard is allowed only as the complete case domain", suite=suite_id, check=check_id, field=field))
        domains[field] = tuple(values)

    raw_rules = raw.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise EngineError(Diagnostic("CONFIG.RULES", "invalid", "decision check requires at least one ordered rule", suite=suite_id, check=check_id))
    rules = []
    for raw_rule in raw_rules:
        if not isinstance(raw_rule, dict) or set(raw_rule) != {"outcome", "when"} or not isinstance(raw_rule.get("outcome"), str):
            raise EngineError(Diagnostic("CONFIG.RULE", "invalid", "rule requires exactly outcome and when", suite=suite_id, check=check_id))
        rules.append(
            Rule(
                raw_rule["outcome"],
                parse_predicate(raw_rule["when"], suite_id, check_id),
            )
        )
    return DecisionCheck(check_id, path, expected, default, domains, tuple(rules))
