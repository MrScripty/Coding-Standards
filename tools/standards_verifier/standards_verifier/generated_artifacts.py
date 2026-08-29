from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .inventory import check_inventory, write_inventory
from .migration_graph import check_graph, write_graph
from .numeric_retirements import check_retirements
from .suite_inputs import check_suite_input_projection, write_suite_input_projection


MIGRATION_TERMINAL_TRIGGER = "zero-bash-accepted"


def check_generated_artifacts(root: Path) -> int:
    suite_inputs_result = check_suite_input_projection(root)
    if suite_inputs_result != 0:
        return suite_inputs_result
    inventory_result = check_inventory(root)
    if inventory_result != 0:
        return inventory_result
    graph_result = check_graph(root)
    if graph_result != 0:
        return graph_result
    return check_retirements(root)


def write_generated_artifacts(root: Path) -> int:
    suite_inputs_result = write_suite_input_projection(root)
    if suite_inputs_result != 0:
        return suite_inputs_result
    graph_result = write_graph(root)
    if graph_result != 0:
        return graph_result
    return write_inventory(root)


def main(argv: Sequence[str] | None = None, *, default_repo_root: Path) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify repository verification artifacts."
    )
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        return check_generated_artifacts(args.repo_root)
    return write_generated_artifacts(args.repo_root)
