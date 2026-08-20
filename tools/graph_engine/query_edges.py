#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


if sys.version_info < (3, 11):
    print(
        "GRAPH.RUNTIME_VERSION: graph engine requires Python 3.11 or newer",
        file=sys.stderr,
    )
    raise SystemExit(3)

from graph_engine.cli import main


if __name__ == "__main__":
    raise SystemExit(main(default_repo_root=Path(__file__).resolve().parents[2]))
