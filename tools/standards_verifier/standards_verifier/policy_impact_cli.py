from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .config import load_registry
from .diagnostics import EngineError
from .policy_impact import DEFAULT_MANIFEST, load_policy_impact


def _parser(default_repo_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report reviewed semantic consumers for one audited policy owner."
    )
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--registry",
        default="evaluation/standards-effectiveness/suite-registry.toml",
    )
    return parser


def main(argv: Sequence[str] | None = None, *, default_repo_root: Path) -> int:
    args = _parser(default_repo_root).parse_args(argv)
    try:
        entries = load_registry(args.repo_root, args.registry)
        impact = load_policy_impact(
            args.repo_root,
            args.manifest,
            {entry.id: entry.path for entry in entries},
        )
        edges = impact.consumers_for(args.owner)
    except EngineError as error:
        print(error.diagnostic.render())
        return error.exit_code

    print("owner\tconsumer\trelation\tapplicability\tevidence_owner")
    for edge in edges:
        print(
            "\t".join(
                (
                    edge.owner,
                    edge.consumer,
                    edge.relation,
                    edge.applicability,
                    edge.evidence_owner,
                )
            )
        )
    return 0
