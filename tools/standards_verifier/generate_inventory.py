#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from tools.standards_verifier.standards_verifier import generated_artifacts_main


REPO_ROOT = Path(__file__).resolve().parents[2]


if sys.version_info < (3, 11):
    print(
        "RUNTIME.PYTHON_VERSION [unavailable]: standards-verifier requires Python 3.11 or newer",
        file=sys.stderr,
    )
    raise SystemExit(3)


if __name__ == "__main__":
    raise SystemExit(generated_artifacts_main(default_repo_root=REPO_ROOT))
