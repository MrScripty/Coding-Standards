#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


if sys.version_info < (3, 11):
    print(
        "RUNTIME.PYTHON_VERSION [unavailable]: standards-verifier requires Python 3.11 or newer",
        file=sys.stderr,
    )
    raise SystemExit(3)

from standards_verifier.numeric_retirements import check_retirements, record_retirements


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record or verify package-scoped numeric candidate retirements."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--package-id")
    args = parser.parse_args()
    if args.check:
        if args.package_id is not None:
            parser.error("--package-id is valid only with --write")
        return check_retirements(args.repo_root)
    if args.package_id is None:
        parser.error("--write requires --package-id")
    return record_retirements(args.repo_root, args.package_id)


if __name__ == "__main__":
    raise SystemExit(main())
