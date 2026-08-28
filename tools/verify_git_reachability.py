#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from tools.standards_verifier.standards_verifier import git_reachability_main


REPO_ROOT = Path(__file__).resolve().parents[1]


if sys.version_info < (3, 11):
    print(
        "GIT_REACHABILITY.RUNTIME_VERSION: Python 3.11 or newer is required",
        file=sys.stderr,
    )
    raise SystemExit(3)


if __name__ == "__main__":
    raise SystemExit(git_reachability_main(default_repo_root=REPO_ROOT))
