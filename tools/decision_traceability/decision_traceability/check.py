#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Sequence


MAP_HEADER = ("trigger_path", "boundary_id", "profile", "artifact_path")
PROFILES = frozenset(("boundary-readme", "contract-readme", "adr", "runbook"))
BOUNDARY = re.compile(r"[a-z][a-z0-9.-]*\Z")


class TraceabilityError(Exception):
    def __init__(self, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True, slots=True)
class MapRow:
    trigger: str
    boundary: str
    profile: str
    artifact: str


@dataclass(frozen=True, slots=True)
class TraceabilityResult:
    matched: int
    failures: tuple[str, ...]

    @property
    def message(self) -> str:
        if self.failures:
            return (
                "Decision traceability check failed "
                f"({len(self.failures)} issue(s))."
            )
        if self.matched == 0:
            return "No configured decision-bearing paths changed."
        return "Decision traceability check passed."


def normalize_path(value: str) -> str:
    selected = value.removeprefix("./")
    path = PurePosixPath(selected)
    components = (
        selected[:-1].split("/") if selected.endswith("/") else selected.split("/")
    )
    if (
        not selected
        or path.is_absolute()
        or ":" in selected
        or any(part in {"", ".", ".."} for part in components)
    ):
        raise TraceabilityError(
            "traceability paths must be normalized repository-relative paths"
        )
    return selected


def run_traceability(
    repository: Path,
    *,
    mode: str,
    map_path: str,
    base_ref: str | None = None,
    head_ref: str | None = None,
) -> TraceabilityResult:
    root = repository.resolve()
    selected_map = normalize_path(map_path)
    _require_repository(root)
    if mode == "staged":
        if base_ref is not None or head_ref is not None:
            raise TraceabilityError("staged mode does not accept base or head refs")
        changed = _nul_paths(
            _git(
                root,
                "diff",
                "--cached",
                "--name-only",
                "--diff-filter=ACMRD",
                "-z",
                "--",
            )
        )
        current_map = _object(root, f":{selected_map}", "Git index", selected_map)
        prior_map = _optional_object(root, f"HEAD:{selected_map}")
        revision = None
    elif mode == "range":
        if not base_ref or not head_ref:
            raise TraceabilityError("range mode requires explicit base and head refs")
        _require_commit(root, base_ref, "base")
        _require_commit(root, head_ref, "head")
        changed = _nul_paths(
            _git(
                root,
                "diff",
                "--name-only",
                "--diff-filter=ACMRD",
                "-z",
                f"{base_ref}...{head_ref}",
                "--",
            )
        )
        current_map = _object(
            root,
            f"{head_ref}:{selected_map}",
            "head commit",
            selected_map,
        )
        prior_map = _optional_object(root, f"{base_ref}:{selected_map}")
        revision = head_ref
    else:
        raise TraceabilityError("traceability mode must be explicitly staged or range")

    rows = _map_rows(current_map, prior_map, selected_map)
    changed_set = frozenset(changed)
    failures = []
    matched = 0
    for row in rows:
        if not any(_matches(path, row.trigger) for path in changed):
            continue
        matched += 1
        if row.artifact not in changed_set:
            failures.append(
                f"{row.trigger} changed without required {row.profile} artifact "
                f"{row.artifact} for boundary:{row.boundary}"
            )
            continue
        content = _artifact(root, row.artifact, revision)
        if content is None:
            owner = "Git index" if revision is None else f"head commit {revision}"
            failures.append(
                f"traceability artifact is absent from {owner}: {row.artifact}"
            )
            continue
        failures.extend(_validate_artifact(row, content))
    return TraceabilityResult(matched, tuple(failures))


def _environment() -> dict[str, str]:
    selected = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith("GIT_")
    }
    selected.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
            "LANG": "C",
        }
    )
    return selected


def _git(root: Path, *arguments: str, check: bool = True) -> bytes:
    try:
        completed = subprocess.run(
            ("git", "-C", str(root), *arguments),
            env=_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise TraceabilityError(f"Git is unavailable: {error}", 3) from error
    if check and completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip()
        raise TraceabilityError(
            f"Git operation is unavailable ({completed.returncode}): {detail}", 3
        )
    return completed.stdout


def _require_repository(root: Path) -> None:
    output = _git(root, "rev-parse", "--is-inside-work-tree")
    if output.strip() != b"true":
        raise TraceabilityError("not inside a Git repository", 3)


def _require_commit(root: Path, revision: str, label: str) -> None:
    completed = subprocess.run(
        ("git", "-C", str(root), "rev-parse", "--verify", f"{revision}^{{commit}}"),
        env=_environment(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode != 0:
        raise TraceabilityError(f"traceability {label} ref is not a commit: {revision}")


def _nul_paths(output: bytes) -> tuple[str, ...]:
    if output and not output.endswith(b"\0"):
        raise TraceabilityError("Git changed-path output is malformed", 3)
    try:
        values = output[:-1].decode("utf-8").split("\0") if output else []
    except UnicodeDecodeError as error:
        raise TraceabilityError("Git paths are not UTF-8", 3) from error
    if any(not value for value in values):
        raise TraceabilityError("Git changed-path output contains an empty path", 3)
    return tuple(values)


def _decode(content: bytes, label: str) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise TraceabilityError(f"{label} is not UTF-8") from error


def _object(root: Path, object_name: str, owner: str, path: str) -> str:
    try:
        return _decode(_git(root, "show", object_name), path)
    except TraceabilityError as error:
        raise TraceabilityError(
            f"traceability map is absent from {owner}: {path}"
        ) from error


def _optional_object(root: Path, object_name: str) -> str:
    completed = subprocess.run(
        ("git", "-C", str(root), "show", object_name),
        env=_environment(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode != 0:
        return ""
    return _decode(completed.stdout, object_name)


def _map_rows(current: str, prior: str, path: str) -> tuple[MapRow, ...]:
    current_lines = current.splitlines()
    if not current_lines or tuple(current_lines[0].split("\t")) != MAP_HEADER:
        raise TraceabilityError(f"{path}:1 has an invalid header")
    combined = list(current_lines)
    if prior:
        prior_lines = prior.splitlines()
        if not prior_lines or tuple(prior_lines[0].split("\t")) != MAP_HEADER:
            raise TraceabilityError(f"prior {path}:1 has an invalid header")
        combined.extend(prior_lines[1:])
    rows = []
    seen = set()
    for line_number, line in enumerate(combined[1:], start=2):
        if not line or line.startswith("#") or line in seen:
            continue
        seen.add(line)
        values = line.split("\t")
        if len(values) != 4:
            raise TraceabilityError(f"{path}:{line_number} has unexpected columns")
        trigger, boundary, profile, artifact = values
        try:
            trigger = normalize_path(trigger)
            artifact = normalize_path(artifact)
        except TraceabilityError as error:
            raise TraceabilityError(
                f"{path}:{line_number} contains an invalid repository path"
            ) from error
        if not BOUNDARY.fullmatch(boundary):
            raise TraceabilityError(
                f"{path}:{line_number} contains invalid boundary ID: {boundary}"
            )
        if profile not in PROFILES:
            raise TraceabilityError(
                f"{path}:{line_number} contains invalid profile: {profile}"
            )
        rows.append(MapRow(trigger, boundary, profile, artifact))
    return tuple(rows)


def _matches(path: str, trigger: str) -> bool:
    return path.startswith(trigger) if trigger.endswith("/") else path == trigger


def _artifact(root: Path, path: str, revision: str | None) -> str | None:
    object_name = f":{path}" if revision is None else f"{revision}:{path}"
    try:
        return _decode(_git(root, "show", object_name), path)
    except TraceabilityError:
        return None


def _validate_artifact(row: MapRow, content: str) -> tuple[str, ...]:
    readme_headings = (
        "## Purpose",
        "## Responsibility",
        "## Invariants",
        "## Entry Points",
    )
    required = {
        "boundary-readme": readme_headings,
        "contract-readme": readme_headings,
        "adr": (
            "## Status",
            "## Context",
            "## Decision",
            "## Alternatives",
            "## Consequences",
            "## Affected Boundaries",
        ),
        "runbook": (
            "## Preconditions",
            "## Procedure",
            "## Validation",
            "## Failure Handling",
            "## Owner",
        ),
    }[row.profile]
    lines = content.splitlines()
    failures = [
        f"{row.artifact} is missing required heading: {heading}"
        for heading in required
        if heading not in lines
    ]
    if row.profile == "contract-readme" and not any(
        heading in lines for heading in ("## Consumer Contract", "## Produced Contract")
    ):
        failures.append(
            f"{row.artifact} requires Consumer Contract or Produced Contract"
        )
    if row.profile == "adr":
        body = _section_body(lines, "## Affected Boundaries")
        if f"- `boundary:{row.boundary}`" not in body:
            failures.append(
                f"{row.artifact} does not identify boundary:{row.boundary}"
            )
    return tuple(failures)


def _section_body(lines: list[str], heading: str) -> tuple[str, ...]:
    result = []
    selected = False
    for line in lines:
        if line == heading:
            selected = True
            continue
        if selected and line.startswith("## "):
            break
        if selected:
            result.append(line)
    return tuple(result)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check explicit decision traceability."
    )
    parser.add_argument("--mode", choices=("staged", "range"))
    parser.add_argument("--map", dest="map_path")
    parser.add_argument("--base-ref")
    parser.add_argument("--head-ref")
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    parser = _parser()
    options = parser.parse_args(arguments)
    if options.mode is None or options.map_path is None:
        parser.error("--mode and --map are required")
    try:
        result = run_traceability(
            Path.cwd(),
            mode=options.mode,
            map_path=options.map_path,
            base_ref=options.base_ref,
            head_ref=options.head_ref,
        )
    except TraceabilityError as error:
        print(str(error), file=sys.stderr)
        return error.exit_code
    for failure in result.failures:
        print(failure, file=sys.stderr)
    print(result.message, file=sys.stderr if result.failures else sys.stdout)
    return 1 if result.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
