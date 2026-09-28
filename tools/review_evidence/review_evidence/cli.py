"""Command entry point for local review packet construction."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from tools.repository_git.repository_git import GitRepositoryError

from .common import PacketError
from .packet import build


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="review-evidence")
    commands = parser.add_subparsers(dest="command", required=True)
    builder = commands.add_parser("build")
    builder.add_argument("--repo-root", type=Path, required=True)
    builder.add_argument("--request", type=Path, required=True)
    builder.add_argument("--evidence-root", type=Path)
    builder.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = build(args.repo_root, args.request, args.evidence_root, args.output)
        print(json.dumps(result, sort_keys=True))
        return 1 if result["material_gaps"] else 0
    except PacketError as error:
        print(json.dumps({"status": error.kind, "message": str(error)}, sort_keys=True))
        return 2
    except GitRepositoryError as error:
        print(
            json.dumps(
                {
                    "status": error.failure.kind,
                    "message": "Git material unavailable or unsupported",
                },
                sort_keys=True,
            )
        )
        return 2
    except (OSError, zipfile.BadZipFile):
        print(
            json.dumps(
                {
                    "status": "unavailable",
                    "message": "local filesystem operation failed",
                },
                sort_keys=True,
            )
        )
        return 2
    except Exception:
        print(
            json.dumps(
                {
                    "status": "unavailable",
                    "message": "unexpected packet construction failure",
                },
                sort_keys=True,
            )
        )
        return 2


__all__ = ("main",)
