#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


if sys.version_info < (3, 11):
    print(
        "RUNTIME.PYTHON_VERSION [unavailable]: standards-verifier requires Python 3.11 or newer",
        file=sys.stderr,
    )
    raise SystemExit(3)

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from standards_verifier.cli import main


if __name__ == "__main__":
    raise SystemExit(main(default_repo_root=REPO_ROOT))
