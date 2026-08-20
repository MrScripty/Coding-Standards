#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


if sys.version_info < (3, 11):
    print(
        "GRAPH.RUNTIME_VERSION: graph query requires Python 3.11 or newer",
        file=sys.stderr,
    )
    raise SystemExit(3)

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tools/standards_verifier"))

from tools.graph_engine.graph_engine.cli import main
from standards_verifier.repository_graph import load_repository_registry


if __name__ == "__main__":
    raise SystemExit(
        main(
            default_repo_root=REPO_ROOT,
            registry_loader=load_repository_registry,
        )
    )
