from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping, Sequence

from tools.standards_authority.standards_authority import GitIndexError, indexed_paths

from .errors import AnalysisError, AnalysisFailure
from .keys import analysis_key_bytes, raw_digest


SUITE_INPUT_CONTRACT = "standards-analysis:suite-input-manifest:v2"
SUITE_INPUT_SCHEMA_VERSION = 2

def _error(
    code: str,
    message: str,
    *,
    path: str | None = None,
    field: str | None = None,
    observed: str | None = None,
    unavailable: bool = False,
) -> AnalysisError:
    return AnalysisError(
        AnalysisFailure(
            code,
            "unavailable" if unavailable else "invalid",
            message,
            path=path,
            field=field,
            observed=observed,
        )
    )


def _repository_path(root: Path, value: str) -> Path:
    logical = PurePosixPath(value)
    candidate = (root / Path(*logical.parts)).resolve(strict=False)
    if (
        not value
        or logical.is_absolute()
        or ".." in logical.parts
        or value.startswith("./")
        or str(logical) != value
        or not candidate.is_relative_to(root)
    ):
        raise _error(
            "SUITE_INPUT.PATH",
            "suite inputs must be normalized contained repository paths",
            path=value,
        )
    return candidate


def file_digest(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def repository_index_paths(root: Path) -> tuple[str, ...]:
    try:
        return indexed_paths(root)
    except GitIndexError as error:
        raise _error(
            "SUITE_INPUT." + error.code.removeprefix("GIT."),
            str(error),
            unavailable=error.outcome == "unavailable",
        ) from error


def repository_index_digest(paths: Sequence[str]) -> str:
    return raw_digest(
        analysis_key_bytes(
            {
                "domain": "standards-analysis:repository-index:v1",
                "paths": list(paths),
            }
        )
    )


@dataclass(frozen=True, slots=True, order=True)
class SuiteInputUse:
    suite: str
    check: str
    role: str

    def as_projection(self) -> dict[str, str]:
        return {"suite": self.suite, "check": self.check, "role": self.role}


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
class SuiteInputManifest:
    registry_path: str
    registry_digest: str
    suites: tuple[tuple[str, str, str], ...]
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
            "suites": [
                {"id": suite_id, "path": path, "digest": digest}
                for suite_id, path, digest in self.suites
            ],
            "files": [item.as_projection() for item in self.files],
            "repository_index": (
                self.repository_index.as_projection()
                if self.repository_index is not None
                else None
            ),
        }


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


def _exact(
    value: Mapping[str, object],
    *,
    required: set[str],
    allowed: set[str],
    path: str,
    field: str,
) -> None:
    missing = sorted(required - set(value))
    extra = sorted(set(value) - allowed)
    if missing or extra:
        raise _error(
            "SUITE_INPUT.FIELDS",
            "suite-input manifest fields are invalid",
            path=path,
            field=field,
            observed=(missing or extra)[0],
        )


def _text(value: object, *, path: str, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise _error(
            "SUITE_INPUT.VALUE",
            "suite-input field must be a non-empty string",
            path=path,
            field=field,
        )
    return value


def _uses(
    value: object,
    *,
    path: str,
    field: str,
    suite_ids: set[str],
) -> tuple[SuiteInputUse, ...]:
    if not isinstance(value, list) or not value:
        raise _error(
            "SUITE_INPUT.USE",
            "suite input must identify at least one owning check",
            path=path,
            field=field,
        )
    uses = []
    for index, raw in enumerate(value):
        use_field = f"{field}[{index}]"
        if not isinstance(raw, dict):
            raise _error(
                "SUITE_INPUT.USE",
                "suite input use must be an object",
                path=path,
                field=use_field,
            )
        _exact(
            raw,
            required={"suite", "check", "role"},
            allowed={"suite", "check", "role"},
            path=path,
            field=use_field,
        )
        use = SuiteInputUse(
            _text(raw["suite"], path=path, field=f"{use_field}.suite"),
            _text(raw["check"], path=path, field=f"{use_field}.check"),
            _text(raw["role"], path=path, field=f"{use_field}.role"),
        )
        if use.suite not in suite_ids:
            raise _error(
                "SUITE_INPUT.USE",
                "suite input use names an unregistered suite",
                path=path,
                field=use_field,
                observed=use.suite,
            )
        uses.append(use)
    normalized = tuple(sorted(set(uses)))
    if tuple(uses) != normalized:
        raise _error(
            "SUITE_INPUT.USE_ORDER",
            "suite input uses must be sorted and unique",
            path=path,
            field=field,
        )
    return normalized


def _load_suite_input_manifest(
    root: Path,
    manifest_path: str,
    registry_path: str,
    registry_entries: Sequence[Mapping[str, object]],
    *,
    validate_repository_index: bool,
) -> SuiteInputManifest:
    source = _repository_path(root, manifest_path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise _error(
            "SUITE_INPUT.UNAVAILABLE",
            "suite-input manifest is unavailable",
            path=manifest_path,
            unavailable=True,
        ) from error
    except (json.JSONDecodeError, UnicodeError) as error:
        raise _error(
            "SUITE_INPUT.INVALID_JSON", str(error), path=manifest_path
        ) from error
    if not isinstance(raw, dict):
        raise _error(
            "SUITE_INPUT.ROOT",
            "suite-input manifest root must be an object",
            path=manifest_path,
        )
    _exact(
        raw,
        required={
            "schema_version",
            "contract",
            "registry",
            "suites",
            "files",
            "repository_index",
        },
        allowed={
            "schema_version",
            "contract",
            "registry",
            "suites",
            "files",
            "repository_index",
        },
        path=manifest_path,
        field="manifest",
    )
    if (
        type(raw["schema_version"]) is not int
        or raw["schema_version"] != SUITE_INPUT_SCHEMA_VERSION
        or raw["contract"] != SUITE_INPUT_CONTRACT
    ):
        raise _error(
            "SUITE_INPUT.VERSION",
            "suite-input manifest contract is unsupported",
            path=manifest_path,
        )

    registry = raw["registry"]
    if not isinstance(registry, dict):
        raise _error(
            "SUITE_INPUT.REGISTRY",
            "suite-input registry binding must be an object",
            path=manifest_path,
        )
    _exact(
        registry,
        required={"path", "digest"},
        allowed={"path", "digest"},
        path=manifest_path,
        field="registry",
    )
    registry_source = _repository_path(root, registry_path)
    if not registry_source.is_file():
        raise _error(
            "SUITE_INPUT.UNAVAILABLE",
            "suite registry is unavailable",
            path=registry_path,
            unavailable=True,
        )
    registry_digest = file_digest(registry_source.read_bytes())
    if (
        registry.get("path") != registry_path
        or registry.get("digest") != registry_digest
    ):
        raise _error(
            "SUITE_INPUT.STALE",
            "suite-input manifest does not bind the current suite registry",
            path=manifest_path,
            field="registry",
        )

    expected_suites = []
    for entry in registry_entries:
        suite_id = _text(entry.get("id"), path=registry_path, field="id")
        suite_path = _text(entry.get("path"), path=registry_path, field="path")
        suite_source = _repository_path(root, suite_path)
        if not suite_source.is_file():
            raise _error(
                "SUITE_INPUT.UNAVAILABLE",
                "registered suite is unavailable",
                path=suite_path,
                unavailable=True,
            )
        expected_suites.append(
            (suite_id, suite_path, file_digest(suite_source.read_bytes()))
        )
    projected_suites = raw["suites"]
    if not isinstance(projected_suites, list):
        raise _error(
            "SUITE_INPUT.SUITES",
            "suite-input manifest suites must be an array",
            path=manifest_path,
        )
    expected_projection = [
        {"id": suite_id, "path": path, "digest": digest}
        for suite_id, path, digest in expected_suites
    ]
    if projected_suites != expected_projection:
        raise _error(
            "SUITE_INPUT.STALE",
            "suite-input manifest does not bind current suite definitions",
            path=manifest_path,
            field="suites",
        )

    suite_ids = {suite_id for suite_id, _, _ in expected_suites}
    raw_files = raw["files"]
    if not isinstance(raw_files, list):
        raise _error(
            "SUITE_INPUT.FILES",
            "suite-input manifest files must be an array",
            path=manifest_path,
        )
    files = []
    previous_path: str | None = None
    for index, item in enumerate(raw_files):
        field = f"files[{index}]"
        if not isinstance(item, dict):
            raise _error(
                "SUITE_INPUT.FILE",
                "suite file input must be an object",
                path=manifest_path,
                field=field,
            )
        state = item.get("state")
        required = {"path", "state", "uses", "digest"}
        if state == "absent":
            required.remove("digest")
        _exact(
            item,
            required=required,
            allowed={"path", "state", "uses", "digest"},
            path=manifest_path,
            field=field,
        )
        input_path = _text(item["path"], path=manifest_path, field=f"{field}.path")
        if previous_path is not None and input_path <= previous_path:
            raise _error(
                "SUITE_INPUT.ORDER",
                "suite file inputs must be sorted and unique by path",
                path=manifest_path,
                field=field,
            )
        previous_path = input_path
        if state not in {"present", "absent"}:
            raise _error(
                "SUITE_INPUT.STATE",
                "suite input state must be present or absent",
                path=manifest_path,
                field=field,
            )
        uses = _uses(
            item["uses"], path=manifest_path, field=f"{field}.uses", suite_ids=suite_ids
        )
        candidate = _repository_path(root, input_path)
        if state == "present":
            if not candidate.is_file():
                raise _error(
                    "SUITE_INPUT.UNAVAILABLE",
                    "required suite input is unavailable",
                    path=input_path,
                    unavailable=True,
                )
            digest = file_digest(candidate.read_bytes())
            if item.get("digest") != digest:
                raise _error(
                    "SUITE_INPUT.STALE",
                    "suite-input manifest has a stale content digest",
                    path=manifest_path,
                    field=field,
                    observed=input_path,
                )
        else:
            if candidate.exists() or candidate.is_symlink():
                raise _error(
                    "SUITE_INPUT.ABSENCE",
                    "suite input asserted absent is present",
                    path=input_path,
                )
            digest = None
        files.append(SuiteFileInput(input_path, state, digest, uses))

    raw_index = raw["repository_index"]
    index: RepositoryIndexObservation | None
    if raw_index is None:
        index = None
    else:
        if not isinstance(raw_index, dict):
            raise _error(
                "SUITE_INPUT.INDEX",
                "repository-index observation must be an object or null",
                path=manifest_path,
            )
        _exact(
            raw_index,
            required={"digest", "uses"},
            allowed={"digest", "uses"},
            path=manifest_path,
            field="repository_index",
        )
        digest = _text(
            raw_index["digest"], path=manifest_path, field="repository_index.digest"
        )
        uses = _uses(
            raw_index["uses"],
            path=manifest_path,
            field="repository_index.uses",
            suite_ids=suite_ids,
        )
        if validate_repository_index:
            observed = repository_index_digest(repository_index_paths(root))
            if digest != observed:
                raise _error(
                    "SUITE_INPUT.STALE",
                    "suite-input manifest has a stale repository-index digest",
                    path=manifest_path,
                    field="repository_index",
                )
        index = RepositoryIndexObservation(digest, uses)

    return SuiteInputManifest(
        registry_path,
        registry_digest,
        tuple(expected_suites),
        tuple(files),
        index,
    )


def load_suite_input_manifest(
    root: Path,
    manifest_path: str,
    registry_path: str,
    registry_entries: Sequence[Mapping[str, object]],
) -> SuiteInputManifest:
    return _load_suite_input_manifest(
        root,
        manifest_path,
        registry_path,
        registry_entries,
        validate_repository_index=True,
    )


def load_captured_suite_input_manifest(
    root: Path,
    manifest_path: str,
    registry_path: str,
    registry_entries: Sequence[Mapping[str, object]],
) -> SuiteInputManifest:
    return _load_suite_input_manifest(
        root,
        manifest_path,
        registry_path,
        registry_entries,
        validate_repository_index=False,
    )


def absent_input_fingerprint(item: SuiteFileInput) -> str:
    return raw_digest(
        analysis_key_bytes(
            {
                "path": item.path,
                "state": item.state,
                "uses": [use.as_projection() for use in item.uses],
            }
        )
    )
