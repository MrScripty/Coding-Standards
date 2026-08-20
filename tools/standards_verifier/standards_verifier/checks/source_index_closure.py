from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckContext
from ..paths import contained_file, contained_path, repository_path
from .markdown import scan_headings
from .markdown_links import LINK_PATTERN
from .table import read_table_rows


MANIFEST_HEADER = (
    "order",
    "source",
    "canonical_owner",
    "current_shape",
    "treatment",
    "retention_evidence",
    "risk",
    "concurrency",
    "gate",
)
CORPUS_HEADER = (
    "path",
    "kind",
    "normative",
    "target_role",
    "preliminary_disposition",
    "baseline_source",
)
OWNER_MAP_HEADER = (
    "id",
    "current_path",
    "line",
    "future_owner",
    "disposition",
    "heading",
)
DISPOSITIONS_HEADER = ("id", "source", "target", "disposition", "rationale")
FIXTURE_FILES = frozenset(
    {"contract.tsv", "headings.tsv", "prohibited.tsv", "routes.tsv"}
)
REQUIRED_NON_AUTHORITY = (
    "non-normative navigation",
    "owns no",
    "fallback authority",
    "Router's typed",
    "instead of using prior wording",
)
GENERIC_PROHIBITED = (
    "Migration authority",
    "remains canonical only",
    "This file remains canonical",
    "Conflicts for moved rules",
    "not yet moved",
    "Existing files retain authority",
)


def _configuration_path(value: Any, field: str, suite: str, check: str) -> str:
    if not isinstance(value, str) or not value:
        raise EngineError(
            Diagnostic(
                "CONFIG.PATH",
                "invalid",
                "field must be a non-empty repository-relative path",
                suite=suite,
                check=check,
                field=field,
            )
        )
    repository_path(value, suite=suite, check=check)
    return value


def _read_utf8(path: Path, display_path: str, suite: str, check: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise EngineError(
            Diagnostic(
                "INPUT.INVALID_UTF8",
                "invalid",
                str(error),
                suite=suite,
                check=check,
                path=display_path,
            )
        ) from error


def _unique_nonempty(
    rows: list[dict[str, str]],
    fields: tuple[str, ...],
    *,
    path: str,
    suite: str,
    check: str,
) -> None:
    seen: dict[str, set[str]] = {field: set() for field in fields}
    for row_number, row in enumerate(rows, start=2):
        for field in fields:
            value = row[field]
            if not value:
                raise EngineError(
                    Diagnostic(
                        "TABLE.EMPTY_VALUE",
                        "invalid",
                        "source-index fixture values must be non-empty",
                        suite=suite,
                        check=check,
                        path=path,
                        row=row_number,
                        field=field,
                    )
                )
            if value in seen[field]:
                raise EngineError(
                    Diagnostic(
                        "TABLE.DUPLICATE_VALUE",
                        "invalid",
                        "source-index fixture values must be unique by column",
                        suite=suite,
                        check=check,
                        path=path,
                        row=row_number,
                        field=field,
                        observed=value,
                    )
                )
            seen[field].add(value)


def _one_row(
    rows: list[dict[str, str]],
    field: str,
    value: str,
    *,
    path: str,
    suite: str,
    check: str,
    label: str,
) -> dict[str, str]:
    matches = [row for row in rows if row[field] == value]
    if len(matches) != 1:
        raise EngineError(
            Diagnostic(
                "ASSERT.SOURCE_INDEX_MEMBERSHIP",
                "invalid",
                f"source requires exactly one {label} row",
                suite=suite,
                check=check,
                path=path,
                field=field,
                expected="single",
                observed="empty" if not matches else "multiple",
            )
        )
    return matches[0]


def _identifier_set(
    rows: list[dict[str, str]],
    source_field: str,
    source: str,
    *,
    path: str,
    suite: str,
    check: str,
) -> frozenset[str]:
    identifiers = [row["id"] for row in rows if row[source_field] == source]
    if not identifiers or any(not identifier for identifier in identifiers):
        raise EngineError(
            Diagnostic(
                "ASSERT.SOURCE_INDEX_IDENTIFIERS",
                "invalid",
                "source requires non-empty frozen identifier membership",
                suite=suite,
                check=check,
                path=path,
                observed=source,
            )
        )
    if len(set(identifiers)) != len(identifiers):
        raise EngineError(
            Diagnostic(
                "TABLE.DUPLICATE_KEY",
                "invalid",
                "frozen identifier occurs more than once for the source",
                suite=suite,
                check=check,
                path=path,
                field="id",
                observed=source,
            )
        )
    return frozenset(identifiers)


def _split_destination(value: str, *, label: str, suite: str, check: str) -> tuple[str, str]:
    parts = value.split("#")
    if len(parts) > 2 or not parts[0] or (len(parts) == 2 and not parts[1]):
        raise EngineError(
            Diagnostic(
                "SOURCE_INDEX.INVALID_ROUTE",
                "invalid",
                f"route {label} has an invalid path or anchor",
                suite=suite,
                check=check,
                field=label,
                observed=value,
            )
        )
    return parts[0], parts[1] if len(parts) == 2 else ""


@dataclass(frozen=True, slots=True)
class SourceIndexClosureCheck:
    id: str
    fixture_root: str
    manifest_path: str
    corpus_path: str
    owner_map_path: str
    dispositions_path: str
    router_path: str

    def run(self, context: CheckContext) -> list[Diagnostic]:
        root = context.repo_root.resolve()
        fixture_root = contained_path(
            root,
            self.fixture_root,
            suite=context.suite_id,
            check=self.id,
        )
        if not fixture_root.exists():
            raise EngineError(
                Diagnostic(
                    "INPUT.UNAVAILABLE",
                    "unavailable",
                    "source-index fixture root does not exist",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.fixture_root,
                ),
                exit_code=3,
            )
        if fixture_root.is_symlink() or not fixture_root.is_dir():
            raise EngineError(
                Diagnostic(
                    "INPUT.NOT_DIRECTORY",
                    "invalid",
                    "source-index fixture root must be a non-symlink directory",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.fixture_root,
                )
            )

        entries = sorted(fixture_root.iterdir(), key=lambda item: item.name)
        invalid_entries = [entry for entry in entries if entry.is_symlink() or not entry.is_dir()]
        if invalid_entries:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.UNREGISTERED_ENTRY",
                    "invalid",
                    "fixture root contains a non-directory or symlink entry",
                    suite=context.suite_id,
                    check=self.id,
                    path=str(invalid_entries[0].relative_to(root)),
                )
            )
        if not entries:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.EMPTY_REGISTRY",
                    "invalid",
                    "source-index fixture root requires at least one directory",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.fixture_root,
                )
            )

        manifest = read_table_rows(
            root,
            self.manifest_path,
            MANIFEST_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        corpus = read_table_rows(
            root,
            self.corpus_path,
            CORPUS_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        owner_map = read_table_rows(
            root,
            self.owner_map_path,
            OWNER_MAP_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        dispositions = read_table_rows(
            root,
            self.dispositions_path,
            DISPOSITIONS_HEADER,
            suite=context.suite_id,
            check=self.id,
        )
        router_file = contained_file(
            root,
            self.router_path,
            suite=context.suite_id,
            check=self.id,
        )
        router = _read_utf8(
            router_file,
            self.router_path,
            context.suite_id,
            self.id,
        )

        seen_sources: set[str] = set()
        for fixture_dir in entries:
            self._verify_fixture(
                context,
                fixture_dir,
                manifest,
                corpus,
                owner_map,
                dispositions,
                router,
                seen_sources,
            )
        return []

    def _verify_fixture(
        self,
        context: CheckContext,
        fixture_dir: Path,
        manifest: list[dict[str, str]],
        corpus: list[dict[str, str]],
        owner_map: list[dict[str, str]],
        dispositions: list[dict[str, str]],
        router: str,
        seen_sources: set[str],
    ) -> None:
        root = context.repo_root.resolve()
        fixture_display = fixture_dir.relative_to(root).as_posix()
        fixture_entries = {entry.name for entry in fixture_dir.iterdir()}
        if fixture_entries != FIXTURE_FILES or any(
            entry.is_symlink() or not entry.is_file() for entry in fixture_dir.iterdir()
        ):
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.FIXTURE_SHAPE",
                    "invalid",
                    "fixture directory requires exactly four regular TSV files",
                    suite=context.suite_id,
                    check=self.id,
                    path=fixture_display,
                    expected=",".join(sorted(FIXTURE_FILES)),
                    observed=",".join(sorted(fixture_entries)),
                )
            )

        def fixture_path(name: str) -> str:
            return f"{fixture_display}/{name}"

        contract_path = fixture_path("contract.tsv")
        contract_rows = read_table_rows(
            root,
            contract_path,
            ("field", "value"),
            suite=context.suite_id,
            check=self.id,
        )
        _unique_nonempty(
            contract_rows,
            ("field",),
            path=contract_path,
            suite=context.suite_id,
            check=self.id,
        )
        contract = {row["field"]: row["value"] for row in contract_rows}
        expected_fields = {"source", "title", "max_lines"}
        if set(contract) != expected_fields or any(not value for value in contract.values()):
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.CONTRACT_FIELDS",
                    "invalid",
                    "contract requires exactly source, title, and max_lines",
                    suite=context.suite_id,
                    check=self.id,
                    path=contract_path,
                    expected=",".join(sorted(expected_fields)),
                    observed=",".join(sorted(contract)),
                )
            )
        if not contract["max_lines"].isascii() or not contract["max_lines"].isdigit() or int(contract["max_lines"]) < 1:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.INVALID_LINE_BUDGET",
                    "invalid",
                    "max_lines must be a positive ASCII decimal integer",
                    suite=context.suite_id,
                    check=self.id,
                    path=contract_path,
                    field="max_lines",
                    observed=contract["max_lines"],
                )
            )

        source = contract["source"]
        if source in seen_sources:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.DUPLICATE_SOURCE",
                    "invalid",
                    "source is registered by more than one fixture directory",
                    suite=context.suite_id,
                    check=self.id,
                    path=contract_path,
                    observed=source,
                )
            )
        seen_sources.add(source)
        source_file = contained_file(
            root,
            source,
            suite=context.suite_id,
            check=self.id,
        )
        content = _read_utf8(source_file, source, context.suite_id, self.id)

        manifest_row = _one_row(
            manifest,
            "source",
            source,
            path=self.manifest_path,
            suite=context.suite_id,
            check=self.id,
            label="closure manifest",
        )
        if manifest_row["current_shape"] not in {"concise", "expanded"} or manifest_row[
            "treatment"
        ] not in {"retain-index", "rewrite-index"}:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.INVALID_MANIFEST_STATE",
                    "invalid",
                    "registered source requires an index-retention manifest state",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.manifest_path,
                    observed=f"{manifest_row['current_shape']}:{manifest_row['treatment']}",
                )
            )
        contained_file(
            root,
            manifest_row["canonical_owner"],
            suite=context.suite_id,
            check=self.id,
        )

        corpus_row = _one_row(
            corpus,
            "path",
            source,
            path=self.corpus_path,
            suite=context.suite_id,
            check=self.id,
            label="corpus",
        )
        required_corpus_fields = (
            "kind",
            "target_role",
            "preliminary_disposition",
            "baseline_source",
        )
        if corpus_row["normative"] != "derived" or any(
            not corpus_row[field] for field in required_corpus_fields
        ):
            raise EngineError(
                Diagnostic(
                    "ASSERT.SOURCE_INDEX_CORPUS",
                    "invalid",
                    "registered source requires a complete derived corpus row",
                    suite=context.suite_id,
                    check=self.id,
                    path=self.corpus_path,
                    observed=corpus_row["normative"],
                )
            )

        headings_path = fixture_path("headings.tsv")
        heading_rows = read_table_rows(
            root,
            headings_path,
            ("heading",),
            suite=context.suite_id,
            check=self.id,
        )
        _unique_nonempty(
            heading_rows,
            ("heading",),
            path=headings_path,
            suite=context.suite_id,
            check=self.id,
        )
        expected_headings = tuple(row["heading"] for row in heading_rows)
        if not expected_headings or expected_headings[0] != contract["title"]:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.TITLE_MISMATCH",
                    "invalid",
                    "contract title must equal the first expected heading",
                    suite=context.suite_id,
                    check=self.id,
                    path=headings_path,
                    expected=contract["title"],
                    observed=expected_headings[0] if expected_headings else "empty",
                )
            )
        observed_headings = tuple(heading.text for heading in scan_headings(content))
        if observed_headings != expected_headings:
            return self._raise_assertion(
                context,
                "ASSERT.SOURCE_INDEX_HEADINGS",
                "source headings do not match the complete ordered fixture",
                source,
                expected=" | ".join(expected_headings),
                observed=" | ".join(observed_headings),
            )

        line_count = source_file.read_bytes().count(b"\n")
        maximum_lines = int(contract["max_lines"])
        if line_count > maximum_lines:
            return self._raise_assertion(
                context,
                "ASSERT.SOURCE_INDEX_LINE_BUDGET",
                "source exceeds its explicit line budget",
                source,
                expected=f"at-most:{maximum_lines}",
                observed=str(line_count),
            )

        routes_path = fixture_path("routes.tsv")
        route_rows = read_table_rows(
            root,
            routes_path,
            ("route", "target", "href"),
            suite=context.suite_id,
            check=self.id,
        )
        if not route_rows:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.EMPTY_ROUTES",
                    "invalid",
                    "routes table requires at least one row",
                    suite=context.suite_id,
                    check=self.id,
                    path=routes_path,
                )
            )
        _unique_nonempty(
            route_rows,
            ("route", "target", "href"),
            path=routes_path,
            suite=context.suite_id,
            check=self.id,
        )
        destinations = {match.group(1) for match in LINK_PATTERN.finditer(content)}
        source_parent = source_file.parent
        for row in route_rows:
            target_path, target_anchor = _split_destination(
                row["target"], label="target", suite=context.suite_id, check=self.id
            )
            repository_path(target_path, suite=context.suite_id, check=self.id)
            contained_file(root, target_path, suite=context.suite_id, check=self.id)
            href_path, href_anchor = _split_destination(
                row["href"], label="href", suite=context.suite_id, check=self.id
            )
            href_posix = PurePosixPath(href_path)
            if href_posix.is_absolute():
                raise EngineError(
                    Diagnostic(
                        "SOURCE_INDEX.INVALID_ROUTE",
                        "invalid",
                        "route href must be source-relative",
                        suite=context.suite_id,
                        check=self.id,
                        path=routes_path,
                        observed=row["href"],
                    )
                )
            resolved_href = (source_parent / Path(*href_posix.parts)).resolve(strict=False)
            if not resolved_href.is_relative_to(root):
                raise EngineError(
                    Diagnostic(
                        "PATH.OUTSIDE_REPOSITORY",
                        "invalid",
                        "route href escapes the repository root",
                        suite=context.suite_id,
                        check=self.id,
                        path=routes_path,
                        observed=row["href"],
                    )
                )
            observed_target = resolved_href.relative_to(root).as_posix()
            if observed_target != target_path or href_anchor != target_anchor:
                return self._raise_assertion(
                    context,
                    "ASSERT.SOURCE_INDEX_ROUTE",
                    "route href does not resolve to its canonical target and anchor",
                    routes_path,
                    expected=row["target"],
                    observed=f"{observed_target}{'#' + href_anchor if href_anchor else ''}",
                )
            if row["href"] not in destinations:
                return self._raise_assertion(
                    context,
                    "ASSERT.SOURCE_INDEX_ROUTE",
                    "required route href is absent from the source Markdown destinations",
                    source,
                    expected=row["href"],
                    observed="absent",
                )

        prohibited_path = fixture_path("prohibited.tsv")
        prohibited_rows = read_table_rows(
            root,
            prohibited_path,
            ("literal",),
            suite=context.suite_id,
            check=self.id,
        )
        if not prohibited_rows:
            raise EngineError(
                Diagnostic(
                    "SOURCE_INDEX.EMPTY_PROHIBITIONS",
                    "invalid",
                    "prohibited table requires at least one row",
                    suite=context.suite_id,
                    check=self.id,
                    path=prohibited_path,
                )
            )
        _unique_nonempty(
            prohibited_rows,
            ("literal",),
            path=prohibited_path,
            suite=context.suite_id,
            check=self.id,
        )
        for literal in (*GENERIC_PROHIBITED, *(row["literal"] for row in prohibited_rows)):
            if literal in content:
                return self._raise_assertion(
                    context,
                    "ASSERT.SOURCE_INDEX_PROHIBITED",
                    "source retains prohibited legacy authority text",
                    source,
                    expected="absent",
                    observed=literal,
                )
        for literal in REQUIRED_NON_AUTHORITY:
            if literal not in content:
                return self._raise_assertion(
                    context,
                    "ASSERT.SOURCE_INDEX_NON_AUTHORITY",
                    "source lacks required non-authority text",
                    source,
                    expected=literal,
                    observed="absent",
                )

        owner_ids = _identifier_set(
            owner_map,
            "current_path",
            source,
            path=self.owner_map_path,
            suite=context.suite_id,
            check=self.id,
        )
        disposition_ids = _identifier_set(
            dispositions,
            "source",
            source,
            path=self.dispositions_path,
            suite=context.suite_id,
            check=self.id,
        )
        if owner_ids != disposition_ids:
            return self._raise_assertion(
                context,
                "ASSERT.SOURCE_INDEX_IDENTIFIERS",
                "owner-map and disposition identifier membership differs",
                source,
                expected=",".join(sorted(owner_ids)),
                observed=",".join(sorted(disposition_ids)),
            )
        if source in router:
            return self._raise_assertion(
                context,
                "ASSERT.SOURCE_INDEX_ROUTER",
                "Router selects a former normative source",
                self.router_path,
                expected="absent",
                observed=source,
            )

    def _raise_assertion(
        self,
        context: CheckContext,
        code: str,
        message: str,
        path: str,
        *,
        expected: str,
        observed: str,
    ) -> None:
        raise EngineError(
            Diagnostic(
                code,
                "invalid",
                message,
                suite=context.suite_id,
                check=self.id,
                path=path,
                expected=expected,
                observed=observed,
            )
        )


def parse_source_index_closure_check(
    raw: dict[str, Any], suite_id: str
) -> SourceIndexClosureCheck:
    allowed = {
        "id",
        "type",
        "fixture_root",
        "manifest_path",
        "corpus_path",
        "owner_map_path",
        "dispositions_path",
        "router_path",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise EngineError(
            Diagnostic(
                "CONFIG.UNKNOWN_FIELD",
                "invalid",
                "source_index_closure check contains unknown fields",
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
    return SourceIndexClosureCheck(
        check_id,
        _configuration_path(raw.get("fixture_root"), "fixture_root", suite_id, check_id),
        _configuration_path(raw.get("manifest_path"), "manifest_path", suite_id, check_id),
        _configuration_path(raw.get("corpus_path"), "corpus_path", suite_id, check_id),
        _configuration_path(raw.get("owner_map_path"), "owner_map_path", suite_id, check_id),
        _configuration_path(
            raw.get("dispositions_path"), "dispositions_path", suite_id, check_id
        ),
        _configuration_path(raw.get("router_path"), "router_path", suite_id, check_id),
    )
