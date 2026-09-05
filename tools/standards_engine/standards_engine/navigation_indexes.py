"""Registered navigation authoring; callers select identities, never file bytes."""

from __future__ import annotations

import json
import posixpath
import re
import tomllib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from urllib.parse import quote

from tools.repository_git.repository_git import RepositoryPath
from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus,
    ContentSource,
    MetadataError,
    file_digest,
)
from tools.standards_analysis.standards_analysis import (
    NavigationIndexAuthority,
)

from .authoring import _invalid, _unavailable

CATALOG = "tools/standards_engine/navigation-indexes.toml"
DIRECTORY = "navigation-indexes"
SUITES = "evaluation/standards-effectiveness/suite-registry.toml"


def _navigation_checks(source):
    registry = tomllib.loads(source.read_bytes(SUITES).decode("utf-8"))
    result = []
    for suite in registry["suites"]:
        document = tomllib.loads(source.read_bytes(suite["path"]).decode("utf-8"))
        for check in document["checks"]:
            if check["type"] == "markdown_targets":
                result.append((suite["path"], check))
    return result


def _digest(value: object) -> str:
    return file_digest(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    )


@dataclass(frozen=True, slots=True)
class NavigationIndex:
    id: str
    path: str
    content: str
    destinations: tuple[str, ...]
    review: NavigationIndexAuthority


def load_indexes(
    source: ContentSource, corpus: CanonicalStandardsCorpus
) -> tuple[NavigationIndex, ...]:
    try:
        content = source.read_bytes(CATALOG)
    except MetadataError as error:
        if error.failure.code != "INPUT.UNAVAILABLE":
            raise
        # Old captured authority has no navigation authoring capability. Never
        # consult a newer worktree or infer registrations from historical prose.
        return ()
    try:
        catalog = tomllib.loads(content.decode("utf-8"))
    except (ValueError, UnicodeError) as error:
        raise _invalid(
            "NAVIGATION.INVALID_CATALOG", "Invalid navigation registration."
        ) from error
    if (
        set(catalog) != {"schema_version", "indexes"}
        or type(catalog["schema_version"]) is not int
        or catalog["schema_version"] != 1
    ):
        raise _invalid(
            "NAVIGATION.INVALID_CATALOG", "Unsupported navigation registration shape."
        )
    if not isinstance(catalog["indexes"], list):
        raise _invalid(
            "NAVIGATION.INVALID_CATALOG", "Navigation indexes must be a list."
        )
    identities, paths, result = set(), set(), []
    enforcement = None
    for row in catalog["indexes"]:
        if not isinstance(row, dict) or set(row) != {"id", "path", "destinations"}:
            raise _invalid(
                "NAVIGATION.INVALID_CATALOG", "Invalid navigation index registration."
            )
        identity, path, destinations = row["id"], row["path"], row["destinations"]
        if not isinstance(identity, str) or not re.fullmatch(
            r"navigation\.[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)*", identity
        ):
            raise _invalid("NAVIGATION.INVALID_CATALOG", "Invalid navigation identity.")
        if (
            not isinstance(path, str)
            or str(RepositoryPath.parse(path)) != path
            or not path.endswith(".md")
        ):
            raise _invalid(
                "NAVIGATION.INVALID_CATALOG", "Invalid registered Markdown location."
            )
        if (
            identity in identities
            or path in paths
            or corpus.resolve_module(identity)
            or corpus.resolve_module(path)
        ):
            raise _invalid(
                "NAVIGATION.INVALID_CATALOG",
                "Navigation registration overlaps another index or standard.",
            )
        if (
            not isinstance(destinations, list)
            or any(not isinstance(x, str) for x in destinations)
            or len(set(destinations)) != len(destinations)
        ):
            raise _invalid(
                "NAVIGATION.INVALID_CATALOG", "Invalid navigation destinations."
            )
        authorities = []
        for destination in destinations:
            module = corpus.resolve_module(destination)
            if module is None or module.module_id != destination:
                raise _invalid(
                    "NAVIGATION.UNKNOWN_DESTINATION",
                    "Navigation requires active canonical standard IDs.",
                )
            authorities.append(
                (destination, module.path, file_digest(source.read_bytes(module.path)))
            )
        try:
            body = source.read_bytes(path).decode("utf-8")
        except UnicodeError as error:
            raise _invalid(
                "NAVIGATION.INVALID_CONTENT",
                "A registered index must contain UTF-8 Markdown.",
            ) from error
        if not body.strip():
            raise _invalid(
                "NAVIGATION.INVALID_CONTENT", "A registered index must not be empty."
            )
        if enforcement is None:
            enforcement = _navigation_checks(source)
        representation = _digest(
            {
                "registration": row,
                "content": body,
                "enforcement": [
                    (suite, check)
                    for suite, check in enforcement
                    if check["path"] == path
                ],
            }
        )
        review = NavigationIndexAuthority(
            identity,
            representation,
            _digest({"index": representation, "destinations": authorities}),
        )
        result.append(
            NavigationIndex(identity, path, body, tuple(destinations), review)
        )
        identities.add(identity)
        paths.add(path)
    return tuple(sorted(result, key=lambda item: item.id))


def rewrite_index(
    files: dict[str, bytes],
    edit: Mapping,
    indexes: Iterable[NavigationIndex],
    corpus: CanonicalStandardsCorpus,
    base_snapshot: str | None,
) -> None:
    from .logical_authoring import authoring_target_id

    indexes = tuple(indexes)

    handle = edit["entrypoint"]
    if handle["snapshot"]["id"] != base_snapshot:
        raise _invalid(
            "NAVIGATION.STALE_TARGET",
            "Navigation target must belong to the proposal's exact base snapshot.",
        )
    index = next(
        (
            item
            for item in indexes
            if authoring_target_id(base_snapshot, item.id) == handle["id"]
        ),
        None,
    )
    if index is None:
        raise _unavailable(
            "NAVIGATION.UNKNOWN_INDEX",
            "Target is not a registered navigation index in this snapshot.",
        )
    links = []
    for destination in sorted(edit["destinations"]):
        module = corpus.resolve_module(destination)
        if module is None or module.module_id != destination:
            raise _invalid(
                "NAVIGATION.UNKNOWN_DESTINATION",
                "Select active canonical standard IDs, not paths or URLs.",
            )
        # Canonical IDs make stable, injection-free labels. The Engine owns
        # relative URL serialization; titles from arbitrary text are not inputs.
        url = quote(
            posixpath.relpath(module.path, posixpath.dirname(index.path) or "."),
            safe="/.-_",
        )
        links.append(f"- [{destination}]({url})")
    files[index.path] = (
        f"# {index.id}\n\n"
        "This is a non-normative navigation index. Policy is owned by the linked\n"
        "canonical standards. This index defines no rules or applicability defaults.\n\n"
        + "\n".join(links)
        + "\n"
    ).encode("utf-8")
    catalog = tomllib.loads(files[CATALOG].decode("utf-8"))
    rows = ["schema_version = 1"]
    for row in catalog["indexes"]:
        destinations = (
            sorted(edit["destinations"])
            if row["id"] == index.id
            else row["destinations"]
        )
        rows.extend(
            (
                "",
                "[[indexes]]",
                f"id = {json.dumps(row['id'])}",
                f"path = {json.dumps(row['path'])}",
                f"destinations = {json.dumps(destinations)}",
            )
        )
    files[CATALOG] = ("\n".join(rows) + "\n").encode("utf-8")
    _retarget_checks(
        files,
        edit.get("retargets", ()),
        index.path,
        indexes,
        corpus,
        base_snapshot,
        edit["destinations"],
    )


def _retarget_checks(
    files, retargets, source_path, indexes, corpus, snapshot, destinations
):
    """Retarget explicit legacy destinations without deleting a declared claim."""
    from tools.standards_metadata.standards_metadata import FrozenContentSource
    from .logical_authoring import authoring_target_id, _toml_inline

    replacements = {}
    for retarget in retargets:
        handle = retarget["entrypoint"]
        if handle["snapshot"]["id"] != snapshot:
            raise _invalid(
                "NAVIGATION.STALE_TARGET",
                "Retarget disposition belongs to another snapshot.",
            )
        old = next(
            (
                item
                for item in indexes
                if authoring_target_id(snapshot, item.id) == handle["id"]
            ),
            None,
        )
        module = corpus.resolve_module(retarget["standard"])
        if (
            old is None
            or module is None
            or module.module_id != retarget["standard"]
            or module.module_id not in destinations
        ):
            raise _invalid(
                "NAVIGATION.INVALID_RETARGET",
                "Retarget a registered legacy index to a selected canonical destination.",
            )
        if old.path in replacements:
            raise _invalid(
                "NAVIGATION.INVALID_RETARGET",
                "Each legacy destination needs one disposition.",
            )
        replacements[old.path] = module.path
    if not replacements:
        return
    changed, consumed = {}, set()
    for suite_path, check in _navigation_checks(FrozenContentSource(files)):
        if check["path"] != source_path:
            continue
        matches = set(check["required"]) & replacements.keys()
        if not matches:
            continue
        consumed.update(matches)
        document = changed.setdefault(
            suite_path, tomllib.loads(files[suite_path].decode("utf-8"))
        )
        target = next(item for item in document["checks"] if item["id"] == check["id"])
        target["required"] = list(
            dict.fromkeys(replacements.get(item, item) for item in check["required"])
        )
    if consumed != replacements.keys():
        raise _invalid(
            "NAVIGATION.UNUSED_RETARGET",
            "A retarget disposition names no declared destination check for this index.",
        )
    for path, document in changed.items():
        lines = [
            f"{key} = {_toml_inline(value)}"
            for key, value in document.items()
            if key != "checks"
        ]
        for check in document["checks"]:
            lines.extend(("", "[[checks]]"))
            lines.extend(
                f"{key} = {_toml_inline(value)}" for key, value in check.items()
            )
        files[path] = ("\n".join(lines) + "\n").encode("utf-8")
