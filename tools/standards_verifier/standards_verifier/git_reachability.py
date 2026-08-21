from __future__ import annotations

import csv
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


_OID = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
_DISPOSITIONS = frozenset({"retained", "archived", "discard-authorized"})
_HEADER = ("oid", "commit_disposition", "reference", "authority")


@dataclass(frozen=True)
class ReachabilityRecord:
    oid: str
    commit_disposition: str
    reference: str
    authority: str


class ReachabilityError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

    def render(self) -> str:
        return f"{self.code}: {self.message}"


def _repository_path(repository: Path, path: Path) -> Path:
    root = repository.resolve()
    resolved = (root / path).resolve() if not path.is_absolute() else path.resolve()
    if not resolved.is_relative_to(root):
        raise ReachabilityError(
            "GIT_REACHABILITY.PATH_ESCAPE",
            f"manifest escapes repository: {path}",
        )
    return resolved


def load_manifest(repository: Path, manifest: Path) -> tuple[ReachabilityRecord, ...]:
    path = _repository_path(repository, manifest)
    try:
        handle = path.open(newline="", encoding="utf-8")
    except OSError as error:
        raise ReachabilityError(
            "GIT_REACHABILITY.MANIFEST_UNAVAILABLE",
            f"cannot read manifest {path}: {error}",
        ) from error

    with handle:
        reader = csv.reader(handle, delimiter="\t", strict=True)
        try:
            header = tuple(next(reader))
        except (StopIteration, csv.Error) as error:
            raise ReachabilityError(
                "GIT_REACHABILITY.INVALID_MANIFEST",
                "manifest is empty or malformed",
            ) from error
        if header != _HEADER:
            raise ReachabilityError(
                "GIT_REACHABILITY.INVALID_MANIFEST",
                f"expected header {_HEADER!r}, observed {header!r}",
            )

        records: list[ReachabilityRecord] = []
        seen: set[str] = set()
        try:
            for line_number, row in enumerate(reader, start=2):
                if len(row) != len(_HEADER):
                    raise ReachabilityError(
                        "GIT_REACHABILITY.INVALID_MANIFEST",
                        f"line {line_number} has {len(row)} fields; expected {len(_HEADER)}",
                    )
                record = ReachabilityRecord(*row)
                if not _OID.fullmatch(record.oid):
                    raise ReachabilityError(
                        "GIT_REACHABILITY.INVALID_OID",
                        f"line {line_number} has invalid OID {record.oid!r}",
                    )
                if record.oid in seen:
                    raise ReachabilityError(
                        "GIT_REACHABILITY.DUPLICATE_OID",
                        f"line {line_number} repeats {record.oid}",
                    )
                if record.commit_disposition not in _DISPOSITIONS:
                    raise ReachabilityError(
                        "GIT_REACHABILITY.INVALID_DISPOSITION",
                        f"line {line_number} has unsupported disposition {record.commit_disposition!r}",
                    )
                if record.commit_disposition == "discard-authorized":
                    if record.reference != "none" or record.authority in {"", "none"}:
                        raise ReachabilityError(
                            "GIT_REACHABILITY.INVALID_DISCARD",
                            f"line {line_number} requires reference=none and explicit authority",
                        )
                elif not record.reference.startswith("refs/") or record.authority != "none":
                    raise ReachabilityError(
                        "GIT_REACHABILITY.INVALID_REFERENCE",
                        f"line {line_number} requires a full refs/... name and authority=none",
                    )
                seen.add(record.oid)
                records.append(record)
        except csv.Error as error:
            raise ReachabilityError(
                "GIT_REACHABILITY.INVALID_MANIFEST",
                f"malformed TSV: {error}",
            ) from error

    if not records:
        raise ReachabilityError(
            "GIT_REACHABILITY.INVALID_MANIFEST",
            "manifest must contain at least one protected OID",
        )
    return tuple(records)


def _git(repository: Path, arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def verify_manifest(repository: Path, manifest: Path) -> tuple[ReachabilityRecord, ...]:
    repository = repository.resolve()
    if _git(repository, ("rev-parse", "--is-inside-work-tree")).returncode != 0:
        raise ReachabilityError(
            "GIT_REACHABILITY.NOT_REPOSITORY",
            f"not a Git worktree: {repository}",
        )

    records = load_manifest(repository, manifest)
    for record in records:
        commit = _git(repository, ("cat-file", "-e", f"{record.oid}^{{commit}}"))
        if commit.returncode != 0:
            raise ReachabilityError(
                "GIT_REACHABILITY.UNKNOWN_COMMIT",
                f"commit object is unavailable: {record.oid}",
            )
        if record.commit_disposition == "discard-authorized":
            continue

        valid_reference = _git(repository, ("check-ref-format", record.reference))
        if valid_reference.returncode != 0:
            raise ReachabilityError(
                "GIT_REACHABILITY.INVALID_REFERENCE",
                f"reference name is invalid: {record.reference}",
            )
        resolved = _git(repository, ("rev-parse", "--verify", f"{record.reference}^{{commit}}"))
        if resolved.returncode != 0:
            raise ReachabilityError(
                "GIT_REACHABILITY.UNKNOWN_REFERENCE",
                f"reference is unavailable: {record.reference}",
            )
        reference_oid = resolved.stdout.strip()
        if record.commit_disposition == "archived":
            if reference_oid != record.oid:
                raise ReachabilityError(
                    "GIT_REACHABILITY.ARCHIVE_MISMATCH",
                    f"{record.reference} resolves to {reference_oid}, expected {record.oid}",
                )
            continue

        reachable = _git(
            repository,
            ("merge-base", "--is-ancestor", record.oid, record.reference),
        )
        if reachable.returncode != 0:
            raise ReachabilityError(
                "GIT_REACHABILITY.UNREACHABLE",
                f"{record.oid} is not reachable from {record.reference}",
            )
    return records
