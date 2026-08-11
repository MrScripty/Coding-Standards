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

from standards_verifier.numeric_audit import check_snapshot, write_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Freeze or verify the derived numeric-comparison audit baseline."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check:
        return check_snapshot(args.repo_root)
    return write_snapshot(args.repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
