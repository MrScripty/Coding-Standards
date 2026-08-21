#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence


if sys.version_info < (3, 11):
    print(
        "GIT_REACHABILITY.RUNTIME_VERSION: Python 3.11 or newer is required",
        file=sys.stderr,
    )
    raise SystemExit(3)

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools/standards_verifier"))

from standards_verifier.git_reachability import ReachabilityError, verify_manifest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify an explicit protected commit set against retained Git refs.",
    )
    parser.add_argument("--repository", type=Path, default=REPO_ROOT)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        records = verify_manifest(args.repository, args.manifest)
    except ReachabilityError as error:
        print(error.render(), file=sys.stderr)
        return 2
    protected = sum(record.commit_disposition != "discard-authorized" for record in records)
    discarded = len(records) - protected
    print(
        f"Verified protected OID set: total={len(records)} "
        f"protected={protected} discard_authorized={discarded}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
