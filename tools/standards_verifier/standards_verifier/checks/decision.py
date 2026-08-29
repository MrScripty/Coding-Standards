from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file
from .predicates import Predicate, parse_predicate


@dataclass(frozen=True, slots=True)
class Rule:
    outcome: str
    when: Predicate


@dataclass(frozen=True, slots=True)
class DecisionOutput:
    column: str
    default: str
    rules: tuple[Rule, ...]


@dataclass(frozen=True, slots=True)
class DecisionCheck:
    id: str
    path: str
    input_columns: tuple[str, ...] | None
    outputs: tuple[DecisionOutput, ...]
    domains: dict[str, tuple[str, ...]]

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return present_inputs("decision-table", self.path)

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
        if len(rows) < 2:
            raise EngineError(
                Diagnostic(
                    "TABLE.EMPTY",
                    "invalid",
                    "decision table requires a header and at least one row",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                )
            )

        header = rows[0]
        if (
            not header
            or any(not column for column in header)
            or len(set(header)) != len(header)
        ):
            raise EngineError(
                Diagnostic(
                    "TABLE.INVALID_HEADER",
                    "invalid",
                    "decision table header must contain unique non-empty columns",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                )
            )
        multi_output = self.input_columns is not None
        if multi_output:
            assert self.input_columns is not None
            expected_header = [
                "case",
                *self.input_columns,
                *(output.column for output in self.outputs),
            ]
            valid_header = header == expected_header
            header_message = (
                "multi-output decision table columns must exactly match case, "
                "declared inputs, and declared outputs"
            )
        else:
            expected_column = self.outputs[0].column
            valid_header = header[0] == "case" and header[-1] == expected_column
            header_message = (
                "decision table must start with case and end with the configured "
                "expected column"
            )
        if not valid_header:
            raise EngineError(
                Diagnostic(
                    "TABLE.HEADER_CONTRACT",
                    "invalid",
                    header_message,
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
        rule_fields = set().union(
            *(rule.when.fields() for output in self.outputs for rule in output.rules)
        )
        allowed_rule_fields = set(self.input_columns) if multi_output else set(header)
        unknown_rule_fields = rule_fields - allowed_rule_fields
        if unknown_rule_fields:
            code = (
                "DECISION.NON_INPUT_FIELD" if multi_output else "DECISION.UNKNOWN_FIELD"
            )
            message = (
                "multi-output decision rule references a non-input field"
                if multi_output
                else "decision rule references an unknown table field"
            )
            raise EngineError(
                Diagnostic(
                    code,
                    "invalid",
                    message,
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    field=sorted(unknown_rule_fields)[0],
                )
            )

        for output in self.outputs:
            expected_domain = self.domains[output.column]
            if expected_domain == ("*",) or output.default not in expected_domain:
                raise EngineError(
                    Diagnostic(
                        "DECISION.DEFAULT_OUTCOME",
                        "invalid",
                        "default outcome must belong to the expected domain",
                        suite=context.suite_id,
                        check=self.id,
                        field=output.column,
                        observed=output.default,
                    )
                )
            for rule in output.rules:
                if rule.outcome not in expected_domain:
                    raise EngineError(
                        Diagnostic(
                            "DECISION.RULE_OUTCOME",
                            "invalid",
                            "rule outcome must belong to the expected domain",
                            suite=context.suite_id,
                            check=self.id,
                            field=output.column,
                            observed=rule.outcome,
                        )
                    )

        diagnostics = []
        seen_cases = set()
        for line_number, values in enumerate(rows[1:], start=2):
            if len(values) != len(header):
                raise EngineError(
                    Diagnostic(
                        "TABLE.ROW_WIDTH",
                        "invalid",
                        "decision row width does not match the header",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        expected=str(len(header)),
                        observed=str(len(values)),
                    )
                )
            row = dict(zip(header, values, strict=True))
            case_id = row["case"]
            if not case_id:
                raise EngineError(
                    Diagnostic(
                        "TABLE.EMPTY_VALUE",
                        "invalid",
                        "decision value is empty",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        field="case",
                    )
                )
            if case_id in seen_cases:
                raise EngineError(
                    Diagnostic(
                        "TABLE.DUPLICATE_CASE",
                        "invalid",
                        "decision case is duplicated",
                        suite=context.suite_id,
                        check=self.id,
                        path=self.path,
                        row=line_number,
                        observed=case_id,
                    )
                )
            seen_cases.add(case_id)
            for field, value in row.items():
                domain = self.domains[field]
                allowed = bool(value) if domain == ("*",) else value in domain
                if not allowed:
                    raise EngineError(
                        Diagnostic(
                            "TABLE.VALUE_OUTSIDE_DOMAIN",
                            "invalid",
                            "decision value is outside its configured domain",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=line_number,
                            field=field,
                            observed=value,
                        )
                    )

            for output in self.outputs:
                actual = output.default
                for rule in output.rules:
                    if rule.when.evaluate(row):
                        actual = rule.outcome
                        break
                if actual != row[output.column]:
                    diagnostics.append(
                        Diagnostic(
                            code="ASSERT.DECISION_OUTCOME",
                            outcome="invalid",
                            message=f"decision outcome mismatch for case {case_id}",
                            suite=context.suite_id,
                            check=self.id,
                            path=self.path,
                            row=line_number,
                            field=output.column if multi_output else None,
                            expected=row[output.column],
                            observed=actual,
                        )
                    )
        return diagnostics


def parse_decision_check(raw: dict[str, Any], suite_id: str) -> DecisionCheck:
    allowed = {
        "id",
        "type",
        "path",
        "expected_column",
        "default",
        "input_columns",
        "outputs",
        "domains",
        "rules",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "decision check contains unknown fields",
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
    for field, value in (("path", path),):
        if not isinstance(value, str) or not value:
            raise EngineError(
                Diagnostic(
                    "CONFIG.STRING",
                    "invalid",
                    "field must be a non-empty string",
                    suite=suite_id,
                    check=check_id,
                    field=field,
                )
            )

    raw_domains = raw.get("domains")
    if not isinstance(raw_domains, dict) or not raw_domains:
        raise EngineError(
            Diagnostic(
                "CONFIG.DOMAINS",
                "invalid",
                "domains must be a non-empty TOML table",
                suite=suite_id,
                check=check_id,
            )
        )
    domains = {}
    for field, values in raw_domains.items():
        if (
            not isinstance(field, str)
            or not field
            or not isinstance(values, list)
            or not values
            or any(not isinstance(value, str) or not value for value in values)
            or len(set(values)) != len(values)
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.DOMAIN",
                    "invalid",
                    "each domain requires unique non-empty string values",
                    suite=suite_id,
                    check=check_id,
                    field=str(field),
                )
            )
        if "*" in values and (field != "case" or values != ["*"]):
            raise EngineError(
                Diagnostic(
                    "CONFIG.DOMAIN_WILDCARD",
                    "invalid",
                    "wildcard is allowed only as the complete case domain",
                    suite=suite_id,
                    check=check_id,
                    field=field,
                )
            )
        domains[field] = tuple(values)

    multi_output = "input_columns" in raw or "outputs" in raw
    single_fields = {"expected_column", "default", "rules"}
    if multi_output and single_fields & set(raw):
        raise EngineError(
            Diagnostic(
                "CONFIG.DECISION_MODE",
                "invalid",
                "single-output and multi-output decision fields are mutually exclusive",
                suite=suite_id,
                check=check_id,
            )
        )

    if not multi_output:
        expected = raw.get("expected_column")
        default = raw.get("default")
        for field, value in (("expected_column", expected), ("default", default)):
            if not isinstance(value, str) or not value:
                raise EngineError(
                    Diagnostic(
                        "CONFIG.STRING",
                        "invalid",
                        "field must be a non-empty string",
                        suite=suite_id,
                        check=check_id,
                        field=field,
                    )
                )
        rules = _parse_rules(raw.get("rules"), suite_id, check_id)
        return DecisionCheck(
            check_id,
            path,
            None,
            (DecisionOutput(expected, default, rules),),
            domains,
        )

    raw_inputs = raw.get("input_columns")
    if (
        not isinstance(raw_inputs, list)
        or not raw_inputs
        or any(not isinstance(value, str) or not value for value in raw_inputs)
        or len(set(raw_inputs)) != len(raw_inputs)
        or "case" in raw_inputs
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.DECISION_INPUTS",
                "invalid",
                "multi-output decision requires unique non-empty input columns excluding case",
                suite=suite_id,
                check=check_id,
            )
        )

    raw_outputs = raw.get("outputs")
    if not isinstance(raw_outputs, list) or len(raw_outputs) < 2:
        raise EngineError(
            Diagnostic(
                "CONFIG.DECISION_OUTPUTS",
                "invalid",
                "multi-output decision requires at least two output contracts",
                suite=suite_id,
                check=check_id,
            )
        )
    outputs = []
    seen_output_columns = set()
    for raw_output in raw_outputs:
        if not isinstance(raw_output, dict) or set(raw_output) != {
            "column",
            "default",
            "rules",
        }:
            raise EngineError(
                Diagnostic(
                    "CONFIG.DECISION_OUTPUT",
                    "invalid",
                    "decision output requires exactly column, default, and rules",
                    suite=suite_id,
                    check=check_id,
                )
            )
        column = raw_output.get("column")
        default = raw_output.get("default")
        if (
            not isinstance(column, str)
            or not column
            or not isinstance(default, str)
            or not default
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.DECISION_OUTPUT",
                    "invalid",
                    "decision output column and default must be non-empty strings",
                    suite=suite_id,
                    check=check_id,
                )
            )
        if column == "case" or column in raw_inputs or column in seen_output_columns:
            raise EngineError(
                Diagnostic(
                    "CONFIG.DECISION_OUTPUT",
                    "invalid",
                    "decision output columns must be unique and separate from inputs",
                    suite=suite_id,
                    check=check_id,
                    field=column,
                )
            )
        seen_output_columns.add(column)
        rules = _parse_rules(raw_output.get("rules"), suite_id, check_id)
        rule_fields = set().union(*(rule.when.fields() for rule in rules))
        invalid_fields = rule_fields - set(raw_inputs)
        if invalid_fields:
            raise EngineError(
                Diagnostic(
                    "DECISION.NON_INPUT_FIELD",
                    "invalid",
                    "multi-output decision rule references a non-input field",
                    suite=suite_id,
                    check=check_id,
                    field=sorted(invalid_fields)[0],
                )
            )
        outputs.append(DecisionOutput(column, default, rules))

    expected_columns = {"case", *raw_inputs, *seen_output_columns}
    if set(domains) != expected_columns:
        raise EngineError(
            Diagnostic(
                "CONFIG.DECISION_COLUMNS",
                "invalid",
                "multi-output domains must exactly match case, inputs, and outputs",
                suite=suite_id,
                check=check_id,
                expected=",".join(sorted(expected_columns)),
                observed=",".join(sorted(domains)),
            )
        )
    return DecisionCheck(
        check_id,
        path,
        tuple(raw_inputs),
        tuple(outputs),
        domains,
    )


def _parse_rules(raw_rules: Any, suite_id: str, check_id: str) -> tuple[Rule, ...]:
    if not isinstance(raw_rules, list) or not raw_rules:
        raise EngineError(
            Diagnostic(
                "CONFIG.RULES",
                "invalid",
                "decision check requires at least one ordered rule",
                suite=suite_id,
                check=check_id,
            )
        )
    rules = []
    for raw_rule in raw_rules:
        if (
            not isinstance(raw_rule, dict)
            or set(raw_rule) != {"outcome", "when"}
            or not isinstance(raw_rule.get("outcome"), str)
        ):
            raise EngineError(
                Diagnostic(
                    "CONFIG.RULE",
                    "invalid",
                    "rule requires exactly outcome and when",
                    suite=suite_id,
                    check=check_id,
                )
            )
        rules.append(
            Rule(
                raw_rule["outcome"],
                parse_predicate(raw_rule["when"], suite_id, check_id),
            )
        )
    return tuple(rules)
