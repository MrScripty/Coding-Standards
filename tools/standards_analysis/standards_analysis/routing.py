from __future__ import annotations

import tomllib
import re
from dataclasses import dataclass
from pathlib import PurePosixPath

from tools.standards_applicability.standards_applicability import (
    ApplicabilityError,
    ApplicabilityProgram,
    FactContract,
    FactSchema,
    compile_fact_schema,
)
from tools.standards_metadata.standards_metadata import (
    CanonicalModuleCorpus,
    ContentSource,
    ContentSourceInput,
    MetadataError,
    content_source,
)

from .errors import AnalysisError, AnalysisFailure


ROUTER_PROJECTION = "evaluation/standards-effectiveness/router-projection.toml"


@dataclass(frozen=True, slots=True)
class RouteRule:
    id: str
    target: str
    program: ApplicabilityProgram


@dataclass(frozen=True, slots=True)
class RouterProjection:
    id: str
    owner: str
    source: str
    base_modules: tuple[str, ...]
    facts: tuple[FactContract, ...]
    rules: tuple[RouteRule, ...]
    fact_schema: FactSchema


def _error(message: str, *, path: str, field: str | None = None) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure("ROUTER_PROJECTION.INVALID", "invalid", message, path, field)
    )


def _applicability_error(error: ApplicabilityError, *, path: str) -> AnalysisError:
    failure = error.failure
    return AnalysisError(
        AnalysisFailure(
            "ROUTER_PROJECTION.INVALID",
            failure.outcome,
            failure.message,
            path,
            failure.field,
            failure.observed,
        )
    )


def _strings(value: object, *, path: str, field: str, non_empty: bool = False) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or (non_empty and not value)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise _error("field must contain unique non-empty strings", path=path, field=field)
    return tuple(value)


def load_router_projection(
    source: ContentSourceInput,
    modules: CanonicalModuleCorpus,
    path: str = ROUTER_PROJECTION,
) -> RouterProjection:
    selected_source = content_source(source)
    try:
        raw = tomllib.loads(selected_source.read_bytes(path).decode("utf-8"))
    except MetadataError as error:
        raise _error(error.failure.message, path=error.failure.path or path) from error
    except UnicodeDecodeError as error:
        raise _error(str(error), path=path) from error
    except tomllib.TOMLDecodeError as error:
        raise _error(str(error), path=path) from error
    if set(raw) != {"schema_version", "id", "owner", "source", "base_modules", "facts", "rules"}:
        raise _error("projection contains missing or unknown fields", path=path)
    if raw["schema_version"] != 2 or raw["owner"] != "router" or raw["source"] != "STANDARDS-ROUTER.md":
        raise _error("projection authority header is invalid", path=path)
    projection_id = raw["id"]
    if not isinstance(projection_id, str) or not projection_id:
        raise _error("projection id must be a non-empty string", path=path, field="id")
    known_modules = {module.module_id for module in modules.modules}
    base_modules = _strings(raw["base_modules"], path=path, field="base_modules", non_empty=True)
    if set(base_modules) - known_modules:
        raise _error("base route contains an unknown module", path=path, field="base_modules")

    facts_raw = raw["facts"]
    if not isinstance(facts_raw, list) or not facts_raw:
        raise _error("projection must declare facts", path=path, field="facts")
    fact_declarations: list[dict[str, object]] = []
    for index, item in enumerate(facts_raw):
        field = f"facts[{index}]"
        expected = {
            "id",
            "semantic_revision",
            "type",
            "nullable",
            "values",
            "aliases",
            "meaning",
            "context_kind",
            "answer_contract",
            "evidence_contract",
            "authorization_capability",
            "prompt",
        }
        if not isinstance(item, dict) or set(item) != expected:
            raise _error("fact declaration shape is invalid", path=path, field=field)
        fact_declarations.append(item)
    try:
        fact_schema = compile_fact_schema(
            {
                "kind": "applicability-fact-schema",
                "id": f"{projection_id}.facts",
                "version": 2,
                "facts": fact_declarations,
            }
        )
    except ApplicabilityError as error:
        raise _applicability_error(error, path=path) from error

    rules_raw = raw["rules"]
    if not isinstance(rules_raw, list) or not rules_raw:
        raise _error("projection must declare rules", path=path, field="rules")
    rules: list[RouteRule] = []
    rule_ids: set[str] = set()
    targets: set[str] = set()
    for index, item in enumerate(rules_raw):
        field = f"rules[{index}]"
        if not isinstance(item, dict) or set(item) != {"id", "target", "when"}:
            raise _error("route rule shape is invalid", path=path, field=field)
        rule_id = item["id"]
        target = item["target"]
        when = item["when"]
        if not isinstance(rule_id, str) or not rule_id or rule_id in rule_ids:
            raise _error("route rule ids must be unique and non-empty", path=path, field=f"{field}.id")
        if not isinstance(target, str) or target not in known_modules or target in targets:
            raise _error("each route target must be a unique canonical module", path=path, field=f"{field}.target")
        if not isinstance(when, dict):
            raise _error("route rule expression must be an object", path=path, field=f"{field}.when")
        try:
            program = fact_schema.compile(when)
        except ApplicabilityError as error:
            raise _applicability_error(error, path=path) from error
        rule_ids.add(rule_id)
        targets.add(target)
        rules.append(RouteRule(rule_id, target, program))
    projected_targets = {rule.target for rule in rules}
    router_targets = _router_table_targets(
        selected_source,
        modules,
        str(raw["source"]),
    )
    if projected_targets != router_targets:
        raise _error(
            "projection targets do not exactly match Router selection tables",
            path=path,
            field="rules.target",
        )
    return RouterProjection(
        projection_id,
        "router",
        "STANDARDS-ROUTER.md",
        base_modules,
        fact_schema.definitions,
        tuple(rules),
        fact_schema,
    )


def _router_table_targets(
    source: ContentSource,
    modules: CanonicalModuleCorpus,
    source_path: str,
) -> set[str]:
    try:
        text = source.read_bytes(source_path).decode("utf-8")
    except MetadataError as error:
        raise _error(
            error.failure.message,
            path=error.failure.path or source_path,
        ) from error
    except UnicodeDecodeError as error:
        raise _error(str(error), path=source_path) from error
    start_marker = "## Workflow Selection"
    end_marker = "## S1 Rust Library Bug-Fix Route"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise _error("Router selection section boundaries are ambiguous", path=source_path)
    selection = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
    by_path = {module.path: module.module_id for module in modules.modules}
    targets: set[str] = set()
    for destination in re.findall(r"\[[^]]+\]\(([^)#]+)(?:#[^)]*)?\)", selection):
        logical = PurePosixPath(destination)
        if (
            not destination
            or logical.is_absolute()
            or ".." in logical.parts
            or destination.startswith("./")
            or str(logical) != destination
        ):
            raise _error("Router selection link escapes the repository", path=source_path)
        module_id = by_path.get(str(logical))
        if module_id is None:
            raise _error(
                "Router selection link does not resolve to a canonical module",
                path=source_path,
                field=destination,
            )
        targets.add(module_id)
    if not targets:
        raise _error("Router selection tables contain no canonical targets", path=source_path)
    return targets
