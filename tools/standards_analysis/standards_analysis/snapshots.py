from __future__ import annotations

import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

from .errors import AnalysisError, AnalysisFailure
from .serialization import digest_bytes, identity


SNAPSHOT_DOMAIN = "coding-standards:snapshot:v1"


@dataclass(frozen=True, slots=True)
class AnalysisVersions:
    metadata_api_version: str = "1"
    graph_engine_contract_version: str = "1"
    graph_engine_implementation_version: str = "1"
    analyzer_implementation_version: str = "1"
    parser_versions: tuple[tuple[str, str], ...] = (("markdown-heading", "1"),)
    evidence_provider_contract_versions: tuple[tuple[str, str], ...] = (
        ("policy-impact-consumer-horizon", "2"),
        ("repository-content", "1"),
    )

    def as_contract(self) -> dict[str, object]:
        return {
            "analysis_contract_version": 5,
            "analysis_schema_version": 2,
            "result_schema_version": 1,
            "interface_schema_version": 8,
            "applicability_version": 3,
            "authorization_contract_version": "authorization-authority.v1",
            "metadata_api_version": self.metadata_api_version,
            "graph_engine_contract_version": self.graph_engine_contract_version,
            "graph_engine_implementation_version": self.graph_engine_implementation_version,
            "analyzer_implementation_version": self.analyzer_implementation_version,
            "parser_versions": dict(self.parser_versions),
            "evidence_provider_contract_versions": dict(
                self.evidence_provider_contract_versions
            ),
        }


@dataclass(frozen=True, slots=True)
class Snapshot:
    handle: dict[str, object]
    inspection: dict[str, object]


def _reject(code: str, message: str, *, path: str | None = None) -> AnalysisError:
    return AnalysisError(AnalysisFailure(code, "invalid", message, path=path))


def _path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or value.startswith("./")
        or str(path) != value
    ):
        raise _reject(
            "SNAPSHOT.PATH",
            "snapshot paths must be normalized repository-relative paths",
            path=value,
        )
    return path


def _run_git(root: Path, *arguments: str, check: bool = True) -> str:
    completed = subprocess.run(
        ("git", "-C", str(root), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )
    if check and completed.returncode != 0:
        raise AnalysisError(
            AnalysisFailure(
                "SNAPSHOT.GIT",
                "unavailable",
                "Git snapshot information is unavailable",
                observed=completed.stderr.strip() or completed.stdout.strip(),
            )
        )
    return completed.stdout


def _is_git(root: Path) -> bool:
    completed = subprocess.run(
        ("git", "-C", str(root), "rev-parse", "--is-inside-work-tree"),
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0 and completed.stdout.strip() == "true"


def _clean_git(
    root: Path,
    scope: tuple[str, ...],
    index: dict[str, tuple[str, str]],
) -> bool:
    output = _run_git(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--ignored=matching",
        "--",
        *scope,
    )
    for record in output.split("\0"):
        if not record:
            continue
        status, path = record[:2], record[3:]
        indexed = index.get(path.rstrip("/"))
        if (
            status == "!!"
            and indexed is not None
            and indexed[0] == "160000"
            and not (root / path.rstrip("/")).exists()
        ):
            continue
        return False
    return True


def _handle(identity_value: dict[str, object]) -> dict[str, object]:
    return {
        "kind": "snapshot-handle",
        "id": identity(SNAPSHOT_DOMAIN, "snapshot", identity_value),
        "schema_version": 1,
    }


def _gitlinks(root: Path, scope: tuple[str, ...]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for line in _run_git(root, "ls-files", "--stage").splitlines():
        metadata, path = line.split("\t", 1)
        mode, object_id, _stage = metadata.split(" ")
        if mode != "160000" or not _selected(path, scope):
            continue
        checkout = root / path
        checked_out = object_id
        state = "clean"
        if checkout.exists() and (checkout / ".git").exists():
            observed = _run_git(checkout, "rev-parse", "HEAD", check=False).strip()
            if observed:
                checked_out = observed
                dirty = bool(
                    _run_git(
                        checkout,
                        "status",
                        "--porcelain=v1",
                        "--untracked-files=all",
                        check=False,
                    ).strip()
                )
                diverged = observed != object_id
                state = (
                    "dirty-and-diverged"
                    if dirty and diverged
                    else "dirty"
                    if dirty
                    else "diverged"
                    if diverged
                    else "clean"
                )
        result.append(
            {
                "path": path,
                "entry_type": "gitlink",
                "mode": int(mode, 8),
                "tracking": "tracked",
                "recorded_gitlink": object_id,
                "checked_out_revision": checked_out,
                "worktree_state": state,
                "inclusion": "included",
                "reason": "declared-analysis-scope",
            }
        )
    return sorted(result, key=lambda item: str(item["path"]))


def _selected(path: str, scope: tuple[str, ...]) -> bool:
    candidate = PurePosixPath(path)
    return any(
        candidate == item or item in candidate.parents
        for item in map(PurePosixPath, scope)
    )


def _compile_git(
    root: Path,
    scope: tuple[str, ...],
    exclusions: tuple[tuple[str, str], ...],
    versions: AnalysisVersions,
) -> Snapshot:
    tree = _run_git(root, "rev-parse", "HEAD^{tree}").strip()
    commit = _run_git(root, "rev-parse", "HEAD^{commit}").strip()
    submodules = _gitlinks(root, scope)
    exclusion_values = [{"path": path, "reason": reason} for path, reason in exclusions]
    identity_value = {
        "tree": tree,
        "scope": list(scope),
        "exclusions": exclusion_values,
        "submodules": submodules,
    }
    handle = _handle(identity_value)
    return Snapshot(
        handle,
        {
            "kind": "git-snapshot-inspection",
            "handle": handle,
            "tree": tree,
            "commit": commit,
            "scope": list(scope),
            "exclusions": exclusion_values,
            "submodules": submodules,
            "versions": versions.as_contract(),
        },
    )


def _nested_repository(root: Path, path: Path) -> bool:
    return path != root and path.is_dir() and (path / ".git").exists()


def _walk(root: Path, selected: PurePosixPath) -> Iterable[tuple[str, Path]]:
    candidate = root / Path(*selected.parts)
    if not candidate.exists() and not candidate.is_symlink():
        raise AnalysisError(
            AnalysisFailure(
                "SNAPSHOT.INPUT_UNAVAILABLE",
                "unavailable",
                "snapshot scope does not exist",
                path=str(selected),
            )
        )
    if not candidate.is_symlink() and not candidate.resolve(
        strict=False
    ).is_relative_to(root):
        raise _reject(
            "SNAPSHOT.SYMLINK_ESCAPE",
            "snapshot inputs cannot be read through a symlink that escapes the source root",
            path=str(selected),
        )
    if (
        candidate.is_symlink()
        or not candidate.is_dir()
        or _nested_repository(root, candidate)
    ):
        yield str(selected), candidate
        return
    yield str(selected), candidate
    for directory, names, files in os.walk(candidate, followlinks=False):
        names.sort()
        files.sort()
        base = Path(directory)
        if base == root and ".git" in names:
            names.remove(".git")
        nested = {name for name in names if _nested_repository(root, base / name)}
        for name in (*names, *files):
            path = base / name
            relative = path.relative_to(root).as_posix()
            yield relative, path
        names[:] = [name for name in names if name not in nested]


def _index(root: Path) -> dict[str, tuple[str, str]]:
    if not _is_git(root):
        return {}
    result: dict[str, tuple[str, str]] = {}
    for line in _run_git(root, "ls-files", "--stage").splitlines():
        metadata, path = line.split("\t", 1)
        mode, object_id, stage = metadata.split(" ")
        if stage == "0":
            result[path] = (mode, object_id)
    return result


def _nested_state(path: Path) -> tuple[str | None, str, str]:
    revision = _run_git(path, "rev-parse", "HEAD", check=False).strip() or None
    dirty = bool(
        _run_git(
            path,
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            check=False,
        ).strip()
    )
    tree = _run_git(path, "rev-parse", "HEAD^{tree}", check=False).strip()
    state = "dirty" if dirty else "clean"
    identity_value = f"tree:{tree}" if tree and not dirty else ""
    return revision, state, identity_value


def _nested_snapshot(path: Path) -> Snapshot:
    return compile_snapshot(path, (".",))


def _entry(
    root: Path,
    display_path: str,
    path: Path,
    git_source: bool,
    index: dict[str, tuple[str, str]],
    exclusion: str | None,
) -> dict[str, object]:
    info = path.lstat()
    common = {
        "path": display_path,
        "mode": stat.S_IMODE(info.st_mode),
        "tracking": "tracked"
        if display_path in index
        else "untracked"
        if git_source
        else "not-applicable",
        "inclusion": "excluded" if exclusion is not None else "included",
        "reason": exclusion or "declared-analysis-scope",
    }
    if path.is_symlink():
        target = os.readlink(path)
        resolved = (path.parent / target).resolve(strict=False)
        resolution = "not-followed" if resolved.is_relative_to(root) else "inert-escape"
        return {
            **common,
            "entry_type": "symlink",
            "symlink_target": target,
            "symlink_resolution": resolution,
        }
    indexed = index.get(display_path)
    if indexed is not None and indexed[0] == "160000":
        recorded = indexed[1]
        if (path / ".git").exists():
            revision, state, nested_identity = _nested_state(path)
        else:
            revision, state, nested_identity = None, "clean", f"commit:{recorded}"
        diverged = revision is not None and revision != recorded
        if state == "dirty" and diverged:
            state = "dirty-and-diverged"
        elif diverged:
            state = "diverged"
        result: dict[str, object] = {
            **common,
            "entry_type": "gitlink",
            "mode": int(indexed[0], 8),
            "recorded_gitlink": recorded,
            "checked_out_revision": revision or recorded,
            "worktree_state": state,
        }
        if state in {"dirty", "dirty-and-diverged"}:
            nested = _nested_snapshot(path)
            result["nested_snapshot"] = nested.handle
            result["nested_identity"] = str(nested.handle["id"])
        else:
            result["nested_identity"] = (
                nested_identity or f"commit:{revision or recorded}"
            )
        return result
    if _nested_repository(root, path):
        revision, state, nested_identity = _nested_state(path)
        result = {
            **common,
            "entry_type": "nested-repository",
            "worktree_state": state,
        }
        if revision is not None:
            result["checked_out_revision"] = revision
        if state == "dirty" or not nested_identity:
            nested = _nested_snapshot(path)
            result["nested_snapshot"] = nested.handle
            result["nested_identity"] = str(nested.handle["id"])
        else:
            result["nested_identity"] = nested_identity
        return result
    if path.is_dir():
        return {**common, "entry_type": "directory"}
    if exclusion is not None:
        return {**common, "entry_type": "file"}
    return {
        **common,
        "entry_type": "file",
        "content_digest": digest_bytes(path.read_bytes()),
    }


def _compile_manifest(
    root: Path,
    scope: tuple[str, ...],
    exclusions: tuple[tuple[str, str], ...],
    versions: AnalysisVersions,
) -> Snapshot:
    excluded = {path: reason for path, reason in exclusions}
    git_source = _is_git(root)
    index = _index(root)
    indexed: dict[str, dict[str, object]] = {}
    for selected in scope:
        for display_path, path in _walk(root, PurePosixPath(selected)):
            reason = next(
                (
                    value
                    for excluded_path, value in excluded.items()
                    if PurePosixPath(display_path) == PurePosixPath(excluded_path)
                    or PurePosixPath(excluded_path)
                    in PurePosixPath(display_path).parents
                ),
                None,
            )
            indexed[display_path] = _entry(
                root,
                display_path,
                path,
                git_source,
                index,
                reason,
            )
    missing_exclusions = set(excluded) - set(indexed)
    if missing_exclusions:
        raise _reject(
            "SNAPSHOT.EXCLUSION_UNRESOLVED",
            "every exclusion must resolve within declared scope",
            path=sorted(missing_exclusions)[0],
        )
    entries = [indexed[path] for path in sorted(indexed)]
    source_kind = "dirty-git" if git_source else "non-git"
    identity_value = {
        "source_kind": source_kind,
        "scope": list(scope),
        "entries": entries,
    }
    handle = _handle(identity_value)
    return Snapshot(
        handle,
        {
            "kind": "manifest-snapshot-inspection",
            "handle": handle,
            "source_kind": source_kind,
            "scope": list(scope),
            "entries": entries,
            "versions": versions.as_contract(),
        },
    )


def compile_snapshot(
    root: Path,
    scope: Iterable[str],
    *,
    exclusions: Iterable[tuple[str, str]] = (),
    versions: AnalysisVersions | None = None,
) -> Snapshot:
    resolved_root = root.resolve()
    selected = tuple(str(_path(value)) for value in scope)
    if not selected or len(set(selected)) != len(selected):
        raise _reject("SNAPSHOT.SCOPE", "snapshot scope must be unique and non-empty")
    git_source = _is_git(resolved_root)
    index = _index(resolved_root) if git_source else {}
    for value in selected:
        candidate = resolved_root / Path(*PurePosixPath(value).parts)
        indexed = index.get(value)
        unavailable_gitlink = indexed is None or indexed[0] != "160000"
        if (
            not candidate.exists()
            and not candidate.is_symlink()
            and unavailable_gitlink
        ):
            raise AnalysisError(
                AnalysisFailure(
                    "SNAPSHOT.INPUT_UNAVAILABLE",
                    "unavailable",
                    "snapshot scope does not exist",
                    path=value,
                )
            )
    omitted = tuple((str(_path(path)), reason) for path, reason in exclusions)
    if any(not reason for _, reason in omitted) or len(
        {path for path, _ in omitted}
    ) != len(omitted):
        raise _reject(
            "SNAPSHOT.EXCLUSIONS",
            "snapshot exclusions require unique paths and non-empty reasons",
        )
    selected_versions = versions or AnalysisVersions()
    if git_source and _clean_git(resolved_root, selected, index):
        return _compile_git(resolved_root, selected, omitted, selected_versions)
    return _compile_manifest(resolved_root, selected, omitted, selected_versions)
