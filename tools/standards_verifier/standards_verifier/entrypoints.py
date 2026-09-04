from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from tools.graph_engine.graph_engine import graph_query_main

from .cli import main as _verifier_main
from .git_reachability import ReachabilityError, verify_manifest
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


__all__ = (
    "git_reachability_main",
    "repository_graph_main",
    "verifier_main",
)
