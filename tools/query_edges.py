#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from tools.standards_verifier.standards_verifier import repository_graph_main


REPO_ROOT = Path(__file__).resolve().parents[1]


if sys.version_info < (3, 11):
    print(
        "GRAPH.RUNTIME_VERSION: graph query requires Python 3.11 or newer",
        file=sys.stderr,
    )
    raise SystemExit(3)


if __name__ == "__main__":
    raise SystemExit(repository_graph_main(default_repo_root=REPO_ROOT))
