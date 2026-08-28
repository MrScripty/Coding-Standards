from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from tools.graph_engine.graph_engine import graph_query_main

from .cli import main as _verifier_main
from .generated_artifacts import main as _generated_artifacts_main
from .git_reachability import ReachabilityError, verify_manifest
from .numeric_audit import write_snapshot
from .numeric_retirements import check_retirements, record_retirements
from .repository_graph import load_repository_registry


def repository_graph_main(
    argv: Sequence[str] | None = None,
    *,
    default_repo_root: Path,
) -> int:
    return graph_query_main(
        argv,
        default_repo_root=default_repo_root,
        registry_loader=load_repository_registry,
    )


def git_reachability_main(
    argv: Sequence[str] | None = None,
    *,
    default_repo_root: Path,
) -> int:
    parser = argparse.ArgumentParser(
        description="Verify an explicit protected commit set against retained Git refs.",
    )
    parser.add_argument("--repository", type=Path, default=default_repo_root)
    parser.add_argument("--manifest", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        records = verify_manifest(arguments.repository, arguments.manifest)
    except ReachabilityError as error:
        print(error.render(), file=sys.stderr)
        return 2
    protected = sum(
        record.commit_disposition != "discard-authorized" for record in records
    )
    print(
        f"Verified protected OID set: total={len(records)} "
        f"protected={protected} "
        f"discard_authorized={len(records) - protected}"
    )
    return 0


def verifier_main(
    argv: Sequence[str] | None = None,
    *,
    default_repo_root: Path,
) -> int:
    return _verifier_main(argv, default_repo_root=default_repo_root)


def generated_artifacts_main(
    argv: Sequence[str] | None = None,
    *,
    default_repo_root: Path,
) -> int:
    return _generated_artifacts_main(argv, default_repo_root=default_repo_root)


def numeric_audit_main(
    argv: Sequence[str] | None = None,
    *,
    default_repo_root: Path,
) -> int:
    parser = argparse.ArgumentParser(
        description="Freeze the immutable numeric-comparison audit baseline."
    )
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    parser.add_argument("--write", action="store_true", required=True)
    arguments = parser.parse_args(argv)
    return write_snapshot(arguments.repo_root)


def numeric_retirements_main(
    argv: Sequence[str] | None = None,
    *,
    default_repo_root: Path,
) -> int:
    parser = argparse.ArgumentParser(
        description="Record or verify package-scoped numeric candidate retirements."
    )
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--package-id")
    arguments = parser.parse_args(argv)
    if arguments.check:
        if arguments.package_id is not None:
            parser.error("--package-id is valid only with --write")
        return check_retirements(arguments.repo_root)
    if arguments.package_id is None:
        parser.error("--write requires --package-id")
    return record_retirements(arguments.repo_root, arguments.package_id)


__all__ = (
    "generated_artifacts_main",
    "git_reachability_main",
    "numeric_audit_main",
    "numeric_retirements_main",
    "repository_graph_main",
    "verifier_main",
)
