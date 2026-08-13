from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .complete_checkpoint import run_retained_checkers
from .diagnostics import Diagnostic, EngineError
from .engine import Verifier
from .generated_artifacts import check_generated_artifacts
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
    parser.add_argument(
        "--complete",
        action="store_true",
        help="check generated evidence, run all suites, then fail-fast run retained Bash checkers",
    )
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
        if args.complete and (args.all or args.suites or args.list):
            raise EngineError(
                Diagnostic(
                    "SELECTION.CONFLICT",
                    "invalid",
                    "--complete cannot be combined with --all, --suite, or --list",
                )
            )
        if args.complete and args.format != "text":
            raise EngineError(
                Diagnostic(
                    "SELECTION.FORMAT_CONFLICT",
                    "invalid",
                    "--complete supports text output only while retained checkers remain",
                    field="format",
                    expected="text",
                    observed=args.format,
                )
            )
        if args.complete:
            artifact_exit = check_generated_artifacts(args.repo_root)
            if artifact_exit != 0:
                return artifact_exit
        verifier = Verifier(args.repo_root, args.registry)
        if args.list:
            if args.all or args.suites:
                raise EngineError(Diagnostic("SELECTION.CONFLICT", "invalid", "--list cannot be combined with a run selection"))
            print("\n".join(verifier.list_suites()))
            return 0
        selected = None if args.all or args.complete or not args.suites else tuple(args.suites)
        results = verifier.run(selected)
    except EngineError as error:
        print(_render_error(error.diagnostic, args.format))
        return error.exit_code

    print(_render_json(results) if args.format == "json" else _render_text(results))
    suite_exit = max((result.exit_code for result in results), default=0)
    if suite_exit != 0 or not args.complete:
        return suite_exit

    retained = run_retained_checkers(args.repo_root)
    if retained.diagnostic is not None:
        print(retained.diagnostic.render())
        return retained.exit_code
    print(f"Complete standards checkpoint passed: {retained.checker_count} retained Bash checkers")
    return 0
