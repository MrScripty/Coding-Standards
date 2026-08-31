from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.repository_git.repository_git import (
    GitRepositoryError,
    GitRepositoryFailure,
    git_output,
)

from ..diagnostics import Diagnostic, EngineError
from ..model import (
    CheckAuthorityInput,
    CheckContext,
    CheckRepositoryIndexInput,
    present_inputs,
)
from ..paths import contained_file


INVENTORY_HEADER = (
    "id",
    "path",
    "line",
    "level",
    "target_role",
    "disposition",
    "heading",
)
DISPOSITION_HEADER = ("id", "source", "target", "disposition", "rationale")
EXPECTED_HEADER = ("id", "classification", "reason")
SUMMARY_HEADER = ("metric", "value")
BASELINE_KEY = "baseline_commit"
_IDENTIFIER = re.compile(r"STD-[0-9]{4}\Z")
_OID = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?\Z")
_HUNK = re.compile(r"^@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@")
_HEADING = re.compile(r"^(#{1,6}) (.*)$")


@dataclass(frozen=True, slots=True)
class InventoryHeading:
    identifier: str
    path: str
    line: int
    level: int
    heading: str


@dataclass(frozen=True, slots=True)
class ExpectedGap:
    identifier: str
    classification: str
    reason: str


@dataclass(frozen=True, slots=True)
class BaselineMarkdownHeadingsCheck:
    id: str
    inventory: str
    dispositions: str
    expected: str
    summary: str
    classifications: tuple[tuple[str, str], ...]

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return (
            *present_inputs("heading-inventory", self.inventory),
            *present_inputs("disposition-authority", self.dispositions),
            *present_inputs("expected-gap-authority", self.expected),
            *present_inputs("baseline-authority", self.summary),
            CheckRepositoryIndexInput("markdown-source-membership"),
        )

    def run(self, context: CheckContext) -> list[Diagnostic]:
        try:
            inventory = _load_inventory(
                context.repo_root,
                self.inventory,
                suite=context.suite_id,
                check=self.id,
            )
            disposed = _load_dispositions(
                context.repo_root,
                self.dispositions,
                suite=context.suite_id,
                check=self.id,
            )
            expected = _load_expected(
                context.repo_root,
                self.expected,
                dict(self.classifications),
                inventory,
                suite=context.suite_id,
                check=self.id,
            )
            baseline = _load_baseline(
                context.repo_root,
                self.summary,
                suite=context.suite_id,
                check=self.id,
            )
            diff = _baseline_diff(context.repo_root, baseline)
        except GitRepositoryError as error:
            raise EngineError(
                Diagnostic(
                    error.failure.code,
                    error.failure.kind,
                    "baseline Markdown heading history cannot be read",
                    suite=context.suite_id,
                    check=self.id,
                    observed=error.failure.message,
                )
            ) from error

        locations = {(item.path, item.line): item for item in inventory.values()}
        observed = {
            item.identifier
            for location in _removed_heading_locations(diff)
            if (item := locations.get(location)) is not None
            and item.identifier not in disposed
        }
        expected_ids = set(expected)
        diagnostics = []
        for identifier in sorted(observed - expected_ids):
            item = inventory[identifier]
            diagnostics.append(
                Diagnostic(
                    "ASSERT.BASELINE_HEADING_UNRECORDED",
                    "invalid",
                    "removed undisposed Markdown heading lacks expected-gap authority",
                    suite=context.suite_id,
                    check=self.id,
                    path=item.path,
                    field=identifier,
                    expected="recorded",
                    observed="unrecorded",
                )
            )
        for identifier in sorted(expected_ids - observed):
            diagnostics.append(
                Diagnostic(
                    "ASSERT.BASELINE_HEADING_NOT_OBSERVED",
                    "invalid",
                    "expected source-gap identity is not observed in the baseline diff",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.expected,
                    field=identifier,
                    expected="observed",
                    observed="absent",
                )
            )
        for identifier in sorted(expected_ids & observed):
            item = inventory[identifier]
            expected_state = dict(self.classifications)[
                expected[identifier].classification
            ]
            actual_state = _current_heading_state(
                context.repo_root,
                item,
                suite=context.suite_id,
                check=self.id,
            )
            if actual_state != expected_state:
                diagnostics.append(
                    Diagnostic(
                        "ASSERT.BASELINE_HEADING_STATE",
                        "invalid",
                        "current heading state contradicts its gap classification",
                        suite=context.suite_id,
                        check=self.id,
                        path=item.path,
                        field=identifier,
                        expected=expected_state,
                        observed=actual_state,
                    )
                )
        return diagnostics


def parse_baseline_markdown_headings_check(
    raw: dict[str, Any], suite_id: str
) -> BaselineMarkdownHeadingsCheck:
    allowed = {
        "id",
        "type",
        "inventory",
        "dispositions",
        "expected",
        "summary",
        "classifications",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "baseline_markdown_headings check contains unknown fields",
                suite=suite_id,
                field=sorted(unknown)[0],
            )
        )
    check_id = raw.get("id")
    if type(check_id) is not str or not check_id:
        raise EngineError(
            Diagnostic(
                "CONFIG.CHECK_ID",
                "invalid",
                "check id must be a non-empty string",
                suite=suite_id,
            )
        )
    paths = {}
    for field in ("inventory", "dispositions", "expected", "summary"):
        value = raw.get(field)
        if type(value) is not str or not value:
            raise EngineError(
                Diagnostic(
                    "CONFIG.PATH",
                    "invalid",
                    f"{field} must be a non-empty path",
                    suite=suite_id,
                    check=check_id,
                    field=field,
                )
            )
        paths[field] = value
    classifications = raw.get("classifications")
    if (
        type(classifications) is not dict
        or not classifications
        or any(
            type(name) is not str
            or not name
            or type(state) is not str
            or state not in {"present", "absent"}
            for name, state in classifications.items()
        )
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.BASELINE_HEADING_CLASSIFICATIONS",
                "invalid",
                "classifications must map non-empty names to present or absent",
                suite=suite_id,
                check=check_id,
                field="classifications",
            )
        )
    return BaselineMarkdownHeadingsCheck(
        check_id,
        paths["inventory"],
        paths["dispositions"],
        paths["expected"],
        paths["summary"],
        tuple(sorted(classifications.items())),
    )


def _load_tsv(
    root: Path,
    path: str,
    header: tuple[str, ...],
    *,
    suite: str,
    check: str,
) -> tuple[tuple[str, ...], ...]:
    source = contained_file(root, path, suite=suite, check=check)
    try:
        lines = source.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise EngineError(
            Diagnostic(
                "INPUT.INVALID_UTF8",
                "invalid",
                str(error),
                suite=suite,
                check=check,
                path=path,
            )
        ) from error
    if not lines or tuple(lines[0].split("\t")) != header:
        raise EngineError(
            Diagnostic(
                "INPUT.TSV_HEADER",
                "invalid",
                "TSV input has an unexpected header",
                suite=suite,
                check=check,
                path=path,
                expected="\t".join(header),
                observed=lines[0] if lines else "empty",
            )
        )
    rows = tuple(tuple(line.split("\t")) for line in lines[1:])
    if any(len(row) != len(header) for row in rows):
        raise EngineError(
            Diagnostic(
                "INPUT.TSV_ROW",
                "invalid",
                "TSV input row has an unexpected field count",
                suite=suite,
                check=check,
                path=path,
            )
        )
    return rows


def _load_inventory(
    root: Path, path: str, *, suite: str, check: str
) -> dict[str, InventoryHeading]:
    result = {}
    locations = set()
    for row in _load_tsv(root, path, INVENTORY_HEADER, suite=suite, check=check):
        identifier, source, line, level, _role, _disposition, heading = row
        try:
            line_number = int(line)
            heading_level = int(level)
        except ValueError as error:
            raise _evidence_error(
                suite, check, path, "inventory line or level is invalid"
            ) from error
        location = (source, line_number)
        if (
            not _IDENTIFIER.fullmatch(identifier)
            or not source
            or line_number < 1
            or heading_level not in range(1, 7)
            or not heading
            or identifier in result
            or location in locations
        ):
            raise _evidence_error(
                suite,
                check,
                path,
                "heading inventory row is invalid or duplicated",
            )
        result[identifier] = InventoryHeading(
            identifier, source, line_number, heading_level, heading
        )
        locations.add(location)
    return result


def _load_dispositions(
    root: Path, path: str, *, suite: str, check: str
) -> frozenset[str]:
    identifiers = []
    for row in _load_tsv(root, path, DISPOSITION_HEADER, suite=suite, check=check):
        identifier = row[0]
        if not _IDENTIFIER.fullmatch(identifier) or not all(row):
            raise _evidence_error(suite, check, path, "disposition row is invalid")
        identifiers.append(identifier)
    if len(set(identifiers)) != len(identifiers):
        raise _evidence_error(suite, check, path, "disposition identity is duplicated")
    return frozenset(identifiers)


def _load_expected(
    root: Path,
    path: str,
    classifications: dict[str, str],
    inventory: dict[str, InventoryHeading],
    *,
    suite: str,
    check: str,
) -> dict[str, ExpectedGap]:
    result = {}
    for identifier, classification, reason in _load_tsv(
        root, path, EXPECTED_HEADER, suite=suite, check=check
    ):
        if (
            not _IDENTIFIER.fullmatch(identifier)
            or identifier not in inventory
            or classification not in classifications
            or not reason
            or identifier in result
        ):
            raise _evidence_error(
                suite, check, path, "expected gap row is invalid or duplicated"
            )
        result[identifier] = ExpectedGap(identifier, classification, reason)
    return result


def _load_baseline(
    root: Path, path: str, *, suite: str, check: str
) -> str:
    rows = _load_tsv(root, path, SUMMARY_HEADER, suite=suite, check=check)
    matches = [value for metric, value in rows if metric == BASELINE_KEY]
    if len(matches) != 1 or not _OID.fullmatch(matches[0]):
        raise _evidence_error(
            suite,
            check,
            path,
            "baseline commit is absent, duplicated, or invalid",
        )
    return matches[0]


def _baseline_diff(root: Path, baseline: str) -> str:
    git_output(root, ("cat-file", "-e", f"{baseline}^{{commit}}"), max_output_bytes=256)
    output = git_output(
        root,
        ("diff", "--no-ext-diff", "--unified=0", baseline, "--", "*.md"),
    )
    try:
        return output.decode("utf-8")
    except UnicodeDecodeError as error:
        raise GitRepositoryError(
            GitRepositoryFailure(
                "unsupported",
                "REPOSITORY_GIT.PATH_ENCODING",
                f"Markdown diff is not UTF-8: {error}",
            )
        ) from error


def _removed_heading_locations(diff: str) -> frozenset[tuple[str, int]]:
    path = ""
    old_line: int | None = None
    result = set()
    for line in diff.splitlines():
        if line.startswith("--- a/"):
            path = line[6:]
            old_line = None
            continue
        if line == "--- /dev/null":
            path = ""
            old_line = None
            continue
        match = _HUNK.match(line)
        if match:
            old_line = int(match.group(1))
            continue
        if old_line is None:
            continue
        if line.startswith("-"):
            if path and _HEADING.fullmatch(line[1:]):
                result.add((path, old_line))
            old_line += 1
        elif line.startswith("+") or line.startswith("\\"):
            continue
        elif line.startswith(" "):
            old_line += 1
    return frozenset(result)


def _current_heading_state(
    root: Path,
    item: InventoryHeading,
    *,
    suite: str,
    check: str,
) -> str:
    source = contained_file(root, item.path, suite=suite, check=check)
    try:
        lines = source.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise EngineError(
            Diagnostic(
                "INPUT.INVALID_UTF8",
                "invalid",
                str(error),
                suite=suite,
                check=check,
                path=item.path,
            )
        ) from error
    expected = f"{'#' * item.level} {item.heading}"
    return "present" if expected in lines else "absent"


def _evidence_error(suite: str, check: str, path: str, message: str) -> EngineError:
    return EngineError(
        Diagnostic(
            "INPUT.BASELINE_HEADING_EVIDENCE",
            "invalid",
            message,
            suite=suite,
            check=check,
            path=path,
        )
    )
