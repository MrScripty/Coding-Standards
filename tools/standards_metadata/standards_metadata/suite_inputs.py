from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import dataclass

from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    encode_identity_value,
)

from .errors import MetadataError, MetadataFailure
from .source import ContentSource, ContentSourceInput, content_source


SUITE_INPUT_CONTRACT = "standards-metadata:suite-input-manifest:v1"
SUITE_INPUT_SCHEMA_VERSION = 1


def file_digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _failure(
    code: str,
    message: str,
    *,
    path: str,
    field: str | None = None,
    expected: str | None = None,
    observed: str | None = None,
) -> MetadataError:
    return MetadataError(
        MetadataFailure(
            code,
            "invalid",
            message,
            path=path,
            field=field,
            expected=expected,
            observed=observed,
        )
    )


def _object(value: object, *, path: str, field: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise _failure(
            "SUITE_INPUT.INVALID_OBJECT",
            "suite-input field must be an object with string keys",
            path=path,
            field=field,
        )
    return value


def _array(value: object, *, path: str, field: str) -> list[object]:
    if not isinstance(value, list):
        raise _failure(
            "SUITE_INPUT.INVALID_ARRAY",
            "suite-input field must be an array",
            path=path,
            field=field,
        )
    return value


def _text(value: object, *, path: str, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise _failure(
            "SUITE_INPUT.INVALID_TEXT",
            "suite-input field must be a non-empty string",
            path=path,
            field=field,
        )
    return value


def _exact(
    value: dict[str, object],
    fields: set[str],
    *,
    path: str,
    field: str,
) -> None:
    if set(value) != fields:
        raise _failure(
            "SUITE_INPUT.INVALID_FIELDS",
            "suite-input object has an invalid field set",
            path=path,
            field=field,
            expected=", ".join(sorted(fields)),
            observed=", ".join(sorted(value)),
        )


def _identity_digest(value: IdentityObject) -> str:
    return file_digest(encode_identity_value(value))


@dataclass(frozen=True, slots=True, order=True)
class SuiteInputUse:
    suite: str
    check: str
    role: str

    def as_projection(self) -> dict[str, str]:
        return {"suite": self.suite, "check": self.check, "role": self.role}


@dataclass(frozen=True, slots=True)
class SuiteDefinitionInput:
    id: str
    path: str
    digest: str
    requires: tuple[str, ...]

    def as_projection(self) -> dict[str, object]:
        return {
            "id": self.id,
            "path": self.path,
            "digest": self.digest,
            "requires": list(self.requires),
        }


@dataclass(frozen=True, slots=True)
class SuiteFileInput:
    path: str
    state: str
    digest: str | None
    uses: tuple[SuiteInputUse, ...]

    def as_projection(self) -> dict[str, object]:
        value: dict[str, object] = {
            "path": self.path,
            "state": self.state,
            "uses": [use.as_projection() for use in self.uses],
        }
        if self.digest is not None:
            value["digest"] = self.digest
        return value


@dataclass(frozen=True, slots=True)
class RepositoryIndexObservation:
    digest: str
    uses: tuple[SuiteInputUse, ...]

    def as_projection(self) -> dict[str, object]:
        return {
            "digest": self.digest,
            "uses": [use.as_projection() for use in self.uses],
        }


@dataclass(frozen=True, slots=True)
class SuiteDependencyProjection:
    suite: str
    suites: tuple[str, ...]
    files: tuple[str, ...]
    observes_repository_index: bool
    fingerprint: str


@dataclass(frozen=True, slots=True)
class SuiteInputManifest:
    registry_path: str
    registry_digest: str
    suites: tuple[SuiteDefinitionInput, ...]
    files: tuple[SuiteFileInput, ...]
    repository_index: RepositoryIndexObservation | None

    def as_projection(self) -> dict[str, object]:
        return {
            "schema_version": SUITE_INPUT_SCHEMA_VERSION,
            "contract": SUITE_INPUT_CONTRACT,
            "registry": {
                "path": self.registry_path,
                "digest": self.registry_digest,
            },
            "suites": [suite.as_projection() for suite in self.suites],
            "files": [item.as_projection() for item in self.files],
            "repository_index": (
                self.repository_index.as_projection()
                if self.repository_index is not None
                else None
            ),
        }

    def dependency(self, suite_id: str) -> SuiteDependencyProjection:
        definitions = {suite.id: suite for suite in self.suites}
        if suite_id not in definitions:
            raise KeyError(suite_id)
        selected: set[str] = set()
        pending = [suite_id]
        while pending:
            current = pending.pop()
            if current in selected:
                continue
            selected.add(current)
            pending.extend(definitions[current].requires)
        suite_ids = tuple(sorted(selected))
        suite_values = tuple(
            IdentityObject(
                (
                    ("id", definition.id),
                    ("path", definition.path),
                    ("digest", definition.digest),
                    ("requires", IdentityArray(definition.requires)),
                )
            )
            for definition in (definitions[item] for item in suite_ids)
        )
        file_values = []
        selected_files = []
        for item in self.files:
            uses = tuple(use for use in item.uses if use.suite in selected)
            if not uses:
                continue
            selected_files.append(item.path)
            file_values.append(
                IdentityObject(
                    (
                        ("path", item.path),
                        ("state", item.state),
                        ("digest", item.digest),
                        (
                            "uses",
                            IdentityArray(
                                IdentityObject(
                                    (
                                        ("suite", use.suite),
                                        ("check", use.check),
                                        ("role", use.role),
                                    )
                                )
                                for use in uses
                            ),
                        ),
                    )
                )
            )
        index_uses = (
            tuple(
                use
                for use in self.repository_index.uses
                if use.suite in selected
            )
            if self.repository_index is not None
            else ()
        )
        fingerprint = _identity_digest(
            IdentityObject(
                (
                    ("contract", SUITE_INPUT_CONTRACT),
                    ("schema_version", SUITE_INPUT_SCHEMA_VERSION),
                    ("suite", suite_id),
                    ("suites", IdentityArray(suite_values)),
                    ("files", IdentityArray(file_values)),
                    (
                        "repository_index",
                        None
                        if not index_uses
                        else IdentityObject(
                            (
                                ("digest", self.repository_index.digest),
                                (
                                    "uses",
                                    IdentityArray(
                                        IdentityObject(
                                            (
                                                ("suite", use.suite),
                                                ("check", use.check),
                                                ("role", use.role),
                                            )
                                        )
                                        for use in index_uses
                                    ),
                                ),
                            )
                        ),
                    ),
                )
            )
        )
        return SuiteDependencyProjection(
            suite_id,
            suite_ids,
            tuple(selected_files),
            bool(index_uses),
            fingerprint,
        )


def suite_input_manifest_bytes(manifest: SuiteInputManifest) -> bytes:
    return (
        json.dumps(
            manifest.as_projection(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _parse_use(value: object, *, path: str) -> SuiteInputUse:
    raw = _object(value, path=path, field="uses")
    _exact(raw, {"suite", "check", "role"}, path=path, field="uses")
    return SuiteInputUse(
        _text(raw["suite"], path=path, field="suite"),
        _text(raw["check"], path=path, field="check"),
        _text(raw["role"], path=path, field="role"),
    )


def _parse_manifest(raw: object, *, path: str) -> SuiteInputManifest:
    root = _object(raw, path=path, field="root")
    _exact(
        root,
        {"schema_version", "contract", "registry", "suites", "files", "repository_index"},
        path=path,
        field="root",
    )
    if root["schema_version"] != SUITE_INPUT_SCHEMA_VERSION:
        raise _failure(
            "SUITE_INPUT.UNSUPPORTED_VERSION",
            "suite-input manifest schema version is unsupported",
            path=path,
            field="schema_version",
            expected=str(SUITE_INPUT_SCHEMA_VERSION),
            observed=str(root["schema_version"]),
        )
    if root["contract"] != SUITE_INPUT_CONTRACT:
        raise _failure(
            "SUITE_INPUT.UNSUPPORTED_CONTRACT",
            "suite-input manifest contract is unsupported",
            path=path,
            field="contract",
            expected=SUITE_INPUT_CONTRACT,
            observed=str(root["contract"]),
        )
    registry = _object(root["registry"], path=path, field="registry")
    _exact(registry, {"path", "digest"}, path=path, field="registry")

    suites = []
    for value in _array(root["suites"], path=path, field="suites"):
        item = _object(value, path=path, field="suites")
        _exact(item, {"id", "path", "digest", "requires"}, path=path, field="suites")
        requires = tuple(
            _text(required, path=path, field="requires")
            for required in _array(item["requires"], path=path, field="requires")
        )
        suites.append(
            SuiteDefinitionInput(
                _text(item["id"], path=path, field="id"),
                _text(item["path"], path=path, field="path"),
                _text(item["digest"], path=path, field="digest"),
                requires,
            )
        )

    files = []
    for value in _array(root["files"], path=path, field="files"):
        item = _object(value, path=path, field="files")
        fields = set(item)
        if fields not in ({"path", "state", "uses"}, {"path", "state", "digest", "uses"}):
            raise _failure(
                "SUITE_INPUT.INVALID_FIELDS",
                "suite file input has an invalid field set",
                path=path,
                field="files",
            )
        state = _text(item["state"], path=path, field="state")
        digest = item.get("digest")
        if state == "present":
            digest = _text(digest, path=path, field="digest")
        elif state == "absent" and digest is not None:
            raise _failure(
                "SUITE_INPUT.INVALID_STATE",
                "absent suite input cannot carry a digest",
                path=path,
                field="digest",
            )
        elif state != "absent":
            raise _failure(
                "SUITE_INPUT.INVALID_STATE",
                "suite input state must be present or absent",
                path=path,
                field="state",
                observed=state,
            )
        files.append(
            SuiteFileInput(
                _text(item["path"], path=path, field="path"),
                state,
                digest,
                tuple(
                    _parse_use(use, path=path)
                    for use in _array(item["uses"], path=path, field="uses")
                ),
            )
        )

    raw_index = root["repository_index"]
    repository_index = None
    if raw_index is not None:
        item = _object(raw_index, path=path, field="repository_index")
        _exact(item, {"digest", "uses"}, path=path, field="repository_index")
        repository_index = RepositoryIndexObservation(
            _text(item["digest"], path=path, field="digest"),
            tuple(
                _parse_use(use, path=path)
                for use in _array(item["uses"], path=path, field="uses")
            ),
        )
    return SuiteInputManifest(
        _text(registry["path"], path=path, field="path"),
        _text(registry["digest"], path=path, field="digest"),
        tuple(suites),
        tuple(files),
        repository_index,
    )


def _registry_definitions(
    source: ContentSource,
    registry_path: str,
) -> tuple[SuiteDefinitionInput, ...]:
    registry_content = source.read_bytes(registry_path)
    try:
        raw = tomllib.loads(registry_content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise _failure(
            "SUITE_INPUT.INVALID_REGISTRY",
            str(error),
            path=registry_path,
        ) from error
    if set(raw) != {"schema_version", "suites"} or raw["schema_version"] != 1:
        raise _failure(
            "SUITE_INPUT.INVALID_REGISTRY",
            "suite registry must use the supported exact contract",
            path=registry_path,
        )
    entries = raw["suites"]
    if not isinstance(entries, list) or not entries:
        raise _failure(
            "SUITE_INPUT.INVALID_REGISTRY",
            "suite registry must contain suites",
            path=registry_path,
        )
    definitions = []
    seen: set[str] = set()
    for raw_entry in entries:
        if not isinstance(raw_entry, dict) or set(raw_entry) != {"id", "path", "requires"}:
            raise _failure(
                "SUITE_INPUT.INVALID_REGISTRY",
                "suite registration has an invalid field set",
                path=registry_path,
            )
        suite_id = _text(raw_entry["id"], path=registry_path, field="id")
        suite_path = _text(raw_entry["path"], path=registry_path, field="path")
        requires = tuple(
            _text(value, path=registry_path, field="requires")
            for value in _array(raw_entry["requires"], path=registry_path, field="requires")
        )
        if suite_id in seen or len(requires) != len(set(requires)):
            raise _failure(
                "SUITE_INPUT.INVALID_REGISTRY",
                "suite IDs and dependencies must be unique",
                path=registry_path,
                observed=suite_id,
            )
        seen.add(suite_id)
        definition_content = source.read_bytes(suite_path)
        try:
            definition = tomllib.loads(definition_content.decode("utf-8"))
        except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
            raise _failure(
                "SUITE_INPUT.INVALID_SUITE",
                str(error),
                path=suite_path,
            ) from error
        if definition.get("id") != suite_id:
            raise _failure(
                "SUITE_INPUT.INVALID_SUITE",
                "registered suite identity does not match its definition",
                path=suite_path,
                expected=suite_id,
                observed=str(definition.get("id")),
            )
        definitions.append(
            SuiteDefinitionInput(
                suite_id,
                suite_path,
                file_digest(definition_content),
                requires,
            )
        )
    known = {definition.id for definition in definitions}
    if any(
        dependency not in known or dependency == definition.id
        for definition in definitions
        for dependency in definition.requires
    ):
        raise _failure(
            "SUITE_INPUT.INVALID_DEPENDENCY",
            "suite dependency must name another registered suite",
            path=registry_path,
        )
    remaining = {definition.id: len(definition.requires) for definition in definitions}
    dependents: dict[str, list[str]] = {suite_id: [] for suite_id in known}
    for definition in definitions:
        for dependency in definition.requires:
            dependents[dependency].append(definition.id)
    ready = [suite_id for suite_id, count in remaining.items() if count == 0]
    visited = 0
    while ready:
        current = ready.pop()
        visited += 1
        for dependent in dependents[current]:
            remaining[dependent] -= 1
            if remaining[dependent] == 0:
                ready.append(dependent)
    if visited != len(definitions):
        raise _failure(
            "SUITE_INPUT.DEPENDENCY_CYCLE",
            "suite dependency graph must be acyclic",
            path=registry_path,
        )
    return tuple(definitions)


def load_suite_input_manifest(
    source_input: ContentSourceInput,
    path: str,
) -> SuiteInputManifest:
    source = content_source(source_input)
    content = source.read_bytes(path)
    try:
        raw = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise _failure("SUITE_INPUT.INVALID_JSON", str(error), path=path) from error
    manifest = _parse_manifest(raw, path=path)
    if suite_input_manifest_bytes(manifest) != content:
        raise _failure(
            "SUITE_INPUT.NONCANONICAL",
            "suite-input manifest must use canonical serialized form",
            path=path,
        )
    registry_content = source.read_bytes(manifest.registry_path)
    if file_digest(registry_content) != manifest.registry_digest:
        raise _failure(
            "SUITE_INPUT.STALE_REGISTRY",
            "suite-input registry digest is stale",
            path=manifest.registry_path,
        )
    expected_suites = _registry_definitions(source, manifest.registry_path)
    if manifest.suites != expected_suites:
        raise _failure(
            "SUITE_INPUT.STALE_SUITES",
            "suite-input definitions do not match the registered suites",
            path=path,
        )
    known = {suite.id for suite in manifest.suites}
    seen_paths: set[str] = set()
    for item in manifest.files:
        if item.path in seen_paths or not item.uses or tuple(sorted(item.uses)) != item.uses:
            raise _failure(
                "SUITE_INPUT.INVALID_FILE",
                "suite inputs require unique paths and sorted non-empty uses",
                path=path,
                observed=item.path,
            )
        seen_paths.add(item.path)
        if any(use.suite not in known for use in item.uses):
            raise _failure(
                "SUITE_INPUT.UNKNOWN_SUITE",
                "suite input use names an unregistered suite",
                path=path,
                observed=item.path,
            )
        if item.state == "present":
            if file_digest(source.read_bytes(item.path)) != item.digest:
                raise _failure(
                    "SUITE_INPUT.STALE_FILE",
                    "suite input content digest is stale",
                    path=item.path,
                )
        else:
            try:
                source.read_bytes(item.path)
            except MetadataError as error:
                if error.failure.outcome != "unavailable":
                    raise
            else:
                raise _failure(
                    "SUITE_INPUT.PRESENT_ABSENCE",
                    "suite input declared absent is present",
                    path=item.path,
                )
    if tuple(sorted(manifest.files, key=lambda item: item.path)) != manifest.files:
        raise _failure(
            "SUITE_INPUT.NONCANONICAL",
            "suite input files must be sorted by path",
            path=path,
        )
    if manifest.repository_index is not None:
        if (
            not manifest.repository_index.uses
            or tuple(sorted(manifest.repository_index.uses))
            != manifest.repository_index.uses
            or any(use.suite not in known for use in manifest.repository_index.uses)
        ):
            raise _failure(
                "SUITE_INPUT.INVALID_INDEX",
                "repository-index observation requires sorted registered uses",
                path=path,
            )
    for suite in manifest.suites:
        manifest.dependency(suite.id)
    return manifest


__all__ = (
    "SUITE_INPUT_CONTRACT",
    "SUITE_INPUT_SCHEMA_VERSION",
    "RepositoryIndexObservation",
    "SuiteDefinitionInput",
    "SuiteDependencyProjection",
    "SuiteFileInput",
    "SuiteInputManifest",
    "SuiteInputUse",
    "file_digest",
    "load_suite_input_manifest",
    "suite_input_manifest_bytes",
)
