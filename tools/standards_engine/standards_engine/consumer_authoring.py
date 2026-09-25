"""Explicit consumer registration and proposal-owned immutable source inputs.

Requests select an existing repository file. Engine preparation binds that file
before admission; the private binding is retained in the ordinary logical edit
so replay and publication never consult the current working tree.
"""
from __future__ import annotations

import base64
import binascii
import tomllib
from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING

from tools.repository_git.repository_git import GitRepositoryError, RepositoryPath
from tools.standards_metadata.standards_metadata import (
    FrozenContentSource,
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import DEFAULT_REGISTRY

if TYPE_CHECKING:
    from .logical_authoring import LogicalProgram, StandardsChangeSet, StructuredEdit


GUIDANCE_KINDS = frozenset({"documentation", "prompt", "template"})
CONSUMER_KINDS = GUIDANCE_KINDS | {"fixture", "implementation-artifact"}


def _source(value: object) -> tuple[str, bytes]:
    from .logical_authoring import _exact, _invalid, _mapping, _text

    raw = _mapping(value, "captured consumer source")
    _exact(raw, {"snapshot", "content"}, "captured consumer source")
    snapshot = _text(raw["snapshot"], "captured source snapshot")
    encoded = raw["content"]
    if type(encoded) is not str:
        raise _invalid("AUTHORING.INVALID_CONSUMER_SOURCE", "Captured content uses canonical base64.")
    try:
        content = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as error:
        raise _invalid("AUTHORING.INVALID_CONSUMER_SOURCE", "Captured content uses canonical base64.") from error
    if base64.b64encode(content).decode("ascii") != encoded:
        raise _invalid("AUTHORING.INVALID_CONSUMER_SOURCE", "Captured content uses canonical base64.")
    return snapshot, content


def parse_registration(raw: Mapping[str, object]) -> StructuredEdit:
    from .logical_authoring import _canonical_id, _exact, _invalid, _structured, _text

    fields = {"kind", "consumer", "path", "artifact_kind", "authority"}
    # Only persisted, Engine-prepared edits have source. Public schemas omit it.
    if "source" in raw:
        fields.add("source")
        _source(raw["source"])
    _exact(raw, fields, "register-consumer edit")
    identity = _canonical_id(raw["consumer"], "consumer ID")
    path = _text(raw["path"], "consumer repository path")
    try:
        selected = str(RepositoryPath.parse(path))
    except GitRepositoryError as error:
        raise _invalid("AUTHORING.INVALID_CONSUMER_PATH", "Select a canonical repository-relative file.") from error
    if selected != path:
        raise _invalid("AUTHORING.INVALID_CONSUMER_PATH", "Select a canonical repository-relative file.")
    kind = raw["artifact_kind"]
    if type(kind) is not str or kind not in CONSUMER_KINDS:
        raise _invalid("AUTHORING.INVALID_CONSUMER_KIND", "Select a supported consumer artifact kind.")
    if type(raw["authority"]) is not str or raw["authority"] not in {"evidence", "projection"}:
        raise _invalid("AUTHORING.INVALID_CONSUMER_AUTHORITY", "Declare evidence or projection authority.")
    if kind in GUIDANCE_KINDS and not path.lower().endswith(".md"):
        raise _invalid("AUTHORING.INVALID_GUIDANCE_PATH", "Registered guidance selects an existing Markdown file.")
    return _structured(raw, target=identity, facet="consumer-registration")


def bind_sources(
    change_set: StandardsChangeSet,
    snapshot: str,
    repository_paths: tuple[str, ...],
    read_file: Callable[[str], bytes],
) -> StandardsChangeSet:
    """Bind selections through the caller-owned exact-revision read session."""
    from .logical_authoring import StandardsChangeSet, _invalid

    members = frozenset(repository_paths)
    edits = []
    for edit in change_set.edits:
        raw = edit.as_contract()
        if raw["kind"] == "register-consumer":
            if "source" in raw:
                raise _invalid("AUTHORING.CONSUMER_SOURCE_OWNED", "The Engine supplies captured source material.")
            path = str(raw["path"])
            if path not in members:
                raise _invalid("AUTHORING.CONSUMER_UNAVAILABLE", "Select a file in the proposal's original repository revision.")
            content = read_file(path)
            if type(content) is not bytes:
                raise _invalid("AUTHORING.INVALID_CONSUMER_SOURCE", "A verified source read returns exact bytes.")
            raw = {**raw, "source": {"snapshot": snapshot, "content": base64.b64encode(content).decode("ascii")}}
        edits.append(raw)
    return StandardsChangeSet.from_mapping({"purpose": change_set.purpose.as_contract(), "edits": edits})


def captured_sources(
    program: LogicalProgram,
    snapshot: str | None,
    original_files: Mapping[str, bytes],
    repository_paths: tuple[str, ...],
) -> tuple[tuple[str, bytes], ...]:
    """Recover only explicitly bound original inputs, including on cold replay."""
    from .logical_authoring import _invalid

    members = frozenset(repository_paths)
    captured: dict[str, bytes] = {}
    for change_set in program.change_sets:
        for edit in change_set.edits:
            raw = edit.as_contract()
            if raw["kind"] != "register-consumer":
                continue
            if "source" not in raw:
                raise _invalid("AUTHORING.CONSUMER_SOURCE_REQUIRED", "Consumer registration requires Engine-prepared source material.")
            bound_snapshot, content = _source(raw["source"])
            path = str(raw["path"])
            if snapshot is None or bound_snapshot != snapshot or path not in members:
                raise _invalid("AUTHORING.CONSUMER_SOURCE_MISMATCH", "Captured material must bind this proposal's original snapshot and repository membership.")
            previous = captured.get(path, original_files.get(path))
            if previous is not None and previous != content:
                raise _invalid("AUTHORING.CONSUMER_SOURCE_MISMATCH", "One original repository path has one captured content value.")
            if raw["artifact_kind"] in GUIDANCE_KINDS:
                try:
                    content.decode("utf-8")
                except UnicodeDecodeError as error:
                    raise _invalid("AUTHORING.INVALID_GUIDANCE_CONTENT", "Registered Markdown guidance is UTF-8 text.") from error
            captured[path] = content
    return tuple(sorted(captured.items()))


def register_consumer(files: dict[str, bytes], edit: Mapping[str, object]) -> None:
    """Declare one consumer; policy links and certification have other owners."""
    from .logical_authoring import _invalid, _toml_inline

    identity, path = str(edit["consumer"]), str(edit["path"])
    corpus = load_canonical_standards_corpus(FrozenContentSource(files))
    if corpus.resolve_module(identity) is not None or corpus.resolve_policy_unit(identity) is not None:
        raise _invalid("AUTHORING.CONSUMER_EXISTS", "Consumer and canonical policy identities are distinct.")
    if path in corpus.module_corpus.members:
        raise _invalid("AUTHORING.CONSUMER_IS_STANDARD", "Canonical modules retain their normative content owner.")
    registry = tomllib.loads(files[DEFAULT_REGISTRY].decode("utf-8"))
    catalog_path = registry["node_catalog"]
    catalog = tomllib.loads(files[catalog_path].decode("utf-8"))
    nodes = catalog["nodes"]
    for node in nodes:
        if identity == node["id"] or identity in node.get("aliases", ()):
            raise _invalid("AUTHORING.CONSUMER_EXISTS", "Select the existing registered consumer identity.")
        if path == node["metadata"]["repository_path"]:
            raise _invalid("AUTHORING.CONSUMER_PATH_EXISTS", "One existing file uses its declared consumer identity.")
    if path not in files:
        raise _invalid("AUTHORING.CONSUMER_SOURCE_REQUIRED", "Register a captured original consumer file.")
    nodes.append({"id": identity, "metadata": {
        "repository_path": path, "artifact_kind": edit["artifact_kind"], "authority": edit["authority"],
    }})
    # Reuse the existing TOML representation, preserving all unrelated records.
    files[catalog_path] = ("\n".join(
        f"{key} = {_toml_inline(value)}" for key, value in catalog.items()
    ) + "\n").encode("utf-8")
