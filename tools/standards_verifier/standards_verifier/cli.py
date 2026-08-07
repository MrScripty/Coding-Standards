from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .diagnostics import Diagnostic, EngineError
from .engine import Verifier
from .model import SuiteResult


def _parser(default_repo_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run strict declarative standards verification suites.")
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    parser.add_argument(
        "--registry",
        default="evaluation/standards-effectiveness/suite-registry.toml",
        help="repository-relative suite registry path",
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--all", action="store_true", help="run every registered suite")
    selection.add_argument("--suite", action="append", dest="suites", help="run one suite and its dependencies; repeatable")
    parser.add_argument("--list", action="store_true", help="list registered suite IDs")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def _render_text(results: list[SuiteResult]) -> str:
    lines = []
    for result in results:
        if result.status == "passed":
            lines.append(f"PASS {result.id} ({result.check_count} checks)")
        else:
            lines.append(f"{result.status.upper()} {result.id} ({result.check_count} checks)")
            lines.extend(f"  {diagnostic.render()}" for diagnostic in result.diagnostics)
    passed = sum(result.status == "passed" for result in results)
    failed = sum(result.status == "failed" for result in results)
    blocked = sum(result.status == "blocked" for result in results)
    lines.append(f"SUMMARY selected={len(results)} passed={passed} failed={failed} blocked={blocked}")
    return "\n".join(lines)


def _render_json(results: list[SuiteResult]) -> str:
    return json.dumps(
        {
            "results": [result.as_dict() for result in results],
            "summary": {
                "selected": len(results),
                "passed": sum(result.status == "passed" for result in results),
                "failed": sum(result.status == "failed" for result in results),
                "blocked": sum(result.status == "blocked" for result in results),
            },
        },
        indent=2,
        sort_keys=True,
    )


def _render_error(diagnostic: Diagnostic, output_format: str) -> str:
    if output_format == "json":
        return json.dumps({"error": diagnostic.as_dict()}, indent=2, sort_keys=True)
    return diagnostic.render()


def main(argv: Sequence[str] | None = None, *, default_repo_root: Path) -> int:
    args = _parser(default_repo_root).parse_args(argv)
    try:
        verifier = Verifier(args.repo_root, args.registry)
        if args.list:
            if args.all or args.suites:
                raise EngineError(Diagnostic("SELECTION.CONFLICT", "invalid", "--list cannot be combined with a run selection"))
            print("\n".join(verifier.list_suites()))
            return 0
        selected = None if args.all or not args.suites else tuple(args.suites)
        results = verifier.run(selected)
    except EngineError as error:
        print(_render_error(error.diagnostic, args.format))
        return error.exit_code

    print(_render_json(results) if args.format == "json" else _render_text(results))
    return max((result.exit_code for result in results), default=0)
