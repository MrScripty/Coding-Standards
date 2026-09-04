from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file


PLAN_STATUSES = frozenset(
    {
        "Planned",
        "Active",
        "Blocked",
        "Implemented",
        "Verifying",
        "Accepted",
        "Deferred",
        "Superseded",
    }
)
ACCEPTANCE_STATUSES = frozenset({"pending", "partial", "blocked", "satisfied"})
OBJECTIVE_STATUSES = frozenset({"pending", "blocked", "satisfied"})
REQUIRED_HEADINGS = (
    "## Objective",
    "## Objective Acceptance",
    "## Binding Decisions",
    "## Milestones",
    "## Blockers",
    "## Re-Plan Triggers",
    "## Final Acceptance",
)
REQUIRED_FIELDS = (
    "Plan status",
    "Current phase",
    "Next slice",
    "Acceptance status",
    "Execution ledger",
    "Issues",
)
DESIGN_PROBES = (
    "Independent concepts and dimensions",
    "State, identity, value, time, policy, and mechanism",
    "Caller and composition-root knowledge",
    "Representative change paths and forced owners",
    "Stable Interfaces versus hidden knowledge",
    "Independent evolution, testing, failure, and replacement",
    "Necessary complexity and containment",
    "Deletion and cumulative machinery result",
)


def _field_values(content: str, field: str) -> list[str]:
    prefix = f"**{field}:** "
    return [
        line.removeprefix(prefix).replace("`", "")
        for line in content.splitlines()
        if line.startswith(prefix)
    ]


def _section(content: str, heading: str) -> list[str]:
    lines = content.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return []
    result: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        result.append(line)
    return result


def _objective_rows(content: str) -> list[tuple[str, str, str]]:
    lines = _section(content, "## Objective Acceptance")
    status_column = 0
    evidence_column = 0
    rows: list[tuple[str, str, str]] = []
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if not cells:
            continue
        identity = cells[0]
        if identity == "ID":
            for index, cell in enumerate(cells):
                if cell == "Status":
                    status_column = index
                if cell == "Evidence":
                    evidence_column = index
            continue
        if not identity or set(identity) == {"-"}:
            continue
        status = (
            cells[status_column].replace("`", "") if status_column < len(cells) else ""
        )
        evidence = (
            cells[evidence_column].replace("`", "")
            if evidence_column < len(cells)
            else ""
        )
        rows.append((identity, status, evidence or "<missing>"))
    return rows


def validate_plan(content: str) -> str | None:
    lines = content.splitlines()
    for heading in REQUIRED_HEADINGS:
        if lines.count(heading) != 1:
            return f"expected one {heading} heading"

    fields: dict[str, str] = {}
    for field in REQUIRED_FIELDS:
        values = _field_values(content, field)
        if len(values) != 1:
            return f"expected one {field} field"
        fields[field] = values[0]

    status = fields["Plan status"]
    acceptance_status = fields["Acceptance status"]
    if status not in PLAN_STATUSES:
        return f"invalid plan status {status}"
    if acceptance_status not in ACCEPTANCE_STATUSES:
        return f"invalid acceptance status {acceptance_status}"
    if any(
        line in {"## Execution Notes", "## History", "## Daily Log"}
        for line in lines
    ):
        return "execution history belongs in the ledger"

    milestone_pattern = re.compile(r"^\*\*Status:\*\* `([^`]*)`")
    for line in lines:
        match = milestone_pattern.match(line)
        if match is not None and match.group(1) not in PLAN_STATUSES:
            return f"invalid milestone status {match.group(1)}"

    if status == "Accepted":
        if acceptance_status != "satisfied":
            return f"accepted plan has {acceptance_status} acceptance"
        unfinished = {"Planned", "Active", "Blocked", "Implemented", "Verifying"}
        for line in lines:
            match = milestone_pattern.match(line)
            if match is not None and match.group(1) in unfinished:
                return "accepted plan has unfinished milestone"
    elif acceptance_status == "satisfied":
        return "satisfied acceptance requires Accepted plan status"

    objective_rows = _objective_rows(content)
    if not objective_rows:
        return "expected at least one objective-acceptance row"
    for objective_id, objective_status, objective_evidence in objective_rows:
        if objective_status not in OBJECTIVE_STATUSES:
            return f"objective {objective_id} has invalid status {objective_status}"
        if objective_status == "satisfied" and objective_evidence in {
            "<missing>",
            "pending",
        }:
            return f"satisfied objective {objective_id} requires evidence"
        if status == "Accepted" and objective_status != "satisfied":
            return f"accepted plan has unsatisfied objective {objective_id}"

    final_acceptance = [
        match.group(1)
        for line in lines
        if (match := re.fullmatch(r"- Acceptance status: `([^`]*)`", line))
    ]
    final_status = [
        match.group(1)
        for line in lines
        if (match := re.fullmatch(r"- Final status: `([^`]*)`", line))
    ]
    if len(final_acceptance) > 1 or len(final_status) > 1:
        return "final acceptance projections must be unique"
    if status == "Accepted" and (
        len(final_acceptance) != 1 or len(final_status) != 1
    ):
        return "accepted plan requires both final acceptance projections"
    if final_acceptance and final_acceptance[0] != acceptance_status:
        return "final acceptance status does not match header"
    if final_status and final_status[0] != status:
        return "final plan status does not match header"

    if status in {"Planned", "Active", "Blocked", "Implemented", "Verifying"}:
        design_heading = "## Simplicity And Ownership Review"
        if lines.count(design_heading) != 1:
            return f"expected one {design_heading} heading"
        design_lines = _section(content, design_heading)
        applicability_lines = [
            line.removeprefix("**Applicability:** ").replace("`", "")
            for line in design_lines
            if line.startswith("**Applicability:** ")
        ]
        if len(applicability_lines) != 1:
            return "composed-design review requires one Applicability field"
        applicability = applicability_lines[0]
        if applicability not in {"applicable", "not-applicable"}:
            return f"invalid composed-design Applicability {applicability}"
        if applicability == "not-applicable":
            reasons = [
                line.removeprefix("**Reason:**").replace("`", "").strip()
                for line in design_lines
                if line.startswith("**Reason:**")
            ]
            if (
                len(reasons) != 1
                or not reasons[0]
                or re.fullmatch(r"\[.*\]", reasons[0]) is not None
                or reasons[0] in {"TBD", "pending"}
            ):
                return "not-applicable composed-design review requires a concrete Reason"
        else:
            for probe in DESIGN_PROBES:
                prefix = f"- {probe}:"
                answers = [
                    line.removeprefix(prefix).replace("`", "").strip()
                    for line in design_lines
                    if line.startswith(prefix)
                ]
                if (
                    len(answers) != 1
                    or not answers[0]
                    or re.fullmatch(r"\[.*\]", answers[0]) is not None
                    or answers[0] in {"TBD", "pending"}
                ):
                    return f"applicable composed-design review requires {probe}"
    return None


@dataclass(frozen=True, slots=True)
class PlanContractCheck:
    id: str
    path: str
    expected: str
    message: str | None

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return present_inputs("plan-contract", self.path)

    def run(self, context: CheckContext) -> list[Diagnostic]:
        source = contained_file(
            context.repo_root,
            self.path,
            suite=context.suite_id,
            check=self.id,
        )
        try:
            observed = validate_plan(source.read_text(encoding="utf-8"))
        except UnicodeError as error:
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
        if self.expected == "valid" and observed is not None:
            return [
                Diagnostic(
                    "ASSERT.PLAN_CONTRACT",
                    "invalid",
                    observed,
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected="valid",
                    observed="invalid",
                )
            ]
        if self.expected == "invalid" and observed is None:
            return [
                Diagnostic(
                    "ASSERT.PLAN_CONTRACT",
                    "invalid",
                    "invalid plan fixture was accepted",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected="invalid",
                    observed="valid",
                )
            ]
        if (
            self.expected == "invalid"
            and self.message is not None
            and observed != self.message
        ):
            return [
                Diagnostic(
                    "ASSERT.PLAN_DIAGNOSTIC",
                    "invalid",
                    "invalid plan produced the wrong diagnostic",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.path,
                    expected=self.message,
                    observed=observed,
                )
            ]
        return []


def parse_plan_contract_check(raw: dict[str, Any], suite_id: str) -> PlanContractCheck:
    allowed = {"id", "type", "path", "expected", "message"}
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "plan_contract check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    path = raw.get("path")
    expected = raw.get("expected")
    message = raw.get("message")
    if type(check_id) is not str or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    if type(path) is not str or not path:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "path must be a non-empty string",
                suite=suite_id,
                check=check_id,
                field="path",
            )
        )
    if expected not in {"valid", "invalid"}:
        raise EngineError(
            Diagnostic(
                "CONFIG.ENUM",
                "invalid",
                "expected must be valid or invalid",
                suite=suite_id,
                check=check_id,
                field="expected",
            )
        )
    if message is not None and (type(message) is not str or not message):
        raise EngineError(
            Diagnostic(
                "CONFIG.STRING",
                "invalid",
                "message must be a non-empty string",
                suite=suite_id,
                check=check_id,
                field="message",
            )
        )
    if expected == "valid" and message is not None:
        raise EngineError(
            Diagnostic(
                "CONFIG.CONTRADICTORY_EXPECTATION",
                "invalid",
                "valid plans cannot declare an invalid diagnostic",
                suite=suite_id,
                check=check_id,
                field="message",
            )
        )
    return PlanContractCheck(check_id, path, expected, message)
