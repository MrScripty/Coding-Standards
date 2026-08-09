from __future__ import annotations

import argparse
import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


CHECKER_GLOB = "verify-*.sh"
REFERENCE_SUFFIXES = frozenset({".md", ".py", ".sh", ".toml", ".tsv"})
DEPENDENCY_PATTERN = re.compile(
    r"(?:\$(?:\{[A-Za-z_][A-Za-z0-9_]*\}|[A-Za-z_][A-Za-z0-9_]*)|\.\.?)/"
    r"(?:[A-Za-z0-9_.-]+/)*(?P<name>(?:verify|check)-[A-Za-z0-9_-]+\.sh)"
)
OUTPUT_PATH = Path("evaluation/standards-effectiveness/generated/checker-structure-inventory.tsv")
GENERATED_ROOT = Path("evaluation/standards-effectiveness/generated")


@dataclass(frozen=True, slots=True)
class CheckerRecord:
    checker: str
    lines: int
    inbound_count: int
    inbound_files: tuple[str, ...]
    executable_inbound_files: tuple[str, ...]
    contract_inbound_files: tuple[str, ...]
    documentation_inbound_files: tuple[str, ...]
    verifier_dependencies: tuple[str, ...]
    helper_dependencies: tuple[str, ...]
    uses_sed: bool
    uses_awk: bool
    uses_rg: bool
    uses_decision_table: bool


def repository_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in REFERENCE_SUFFIXES:
            continue
        relative = path.relative_to(root)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if relative.is_relative_to(GENERATED_ROOT):
            continue
        yield path


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def collect_inventory(root: Path) -> tuple[CheckerRecord, ...]:
    root = root.resolve()
    evaluation = root / "evaluation/standards-effectiveness"
    checker_paths = sorted(evaluation.glob(CHECKER_GLOB))
    reference_content = []
    for path in repository_files(root):
        content = _read_text(path)
        if content is not None:
            reference_content.append((path.relative_to(root).as_posix(), content))

    records = []
    for checker_path in checker_paths:
        content = checker_path.read_text(encoding="utf-8")
        checker = checker_path.relative_to(root).as_posix()
        basename = checker_path.name
        inbound = tuple(
            path
            for path, candidate in reference_content
            if path != checker and basename in candidate
        )
        executable_inbound = tuple(
            path for path in inbound if Path(path).suffix in {".py", ".sh"}
        )
        contract_inbound = tuple(
            path for path in inbound if Path(path).suffix in {".toml", ".tsv"}
        )
        documentation_inbound = tuple(
            path for path in inbound if Path(path).suffix == ".md"
        )
        dependencies = sorted(set(DEPENDENCY_PATTERN.findall(content)))
        verifier_dependencies = tuple(
            dependency for dependency in dependencies if dependency.startswith("verify-")
        )
        helper_dependencies = tuple(
            dependency for dependency in dependencies if dependency.startswith("check-")
        )
        records.append(
            CheckerRecord(
                checker=checker,
                lines=len(content.splitlines()),
                inbound_count=len(inbound),
                inbound_files=inbound,
                executable_inbound_files=executable_inbound,
                contract_inbound_files=contract_inbound,
                documentation_inbound_files=documentation_inbound,
                verifier_dependencies=verifier_dependencies,
                helper_dependencies=helper_dependencies,
                uses_sed=bool(re.search(r"(^|[^A-Za-z0-9_])sed([^A-Za-z0-9_]|$)", content)),
                uses_awk=bool(re.search(r"(^|[^A-Za-z0-9_])awk([^A-Za-z0-9_]|$)", content)),
                uses_rg=bool(re.search(r"(^|[^A-Za-z0-9_])rg([^A-Za-z0-9_]|$)", content)),
                uses_decision_table="check-decision-table.sh" in content,
            )
        )
    return tuple(records)


def render_inventory(records: Iterable[CheckerRecord]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(
        (
            "checker",
            "lines",
            "inbound_count",
            "inbound_files",
            "executable_inbound_count",
            "executable_inbound_files",
            "contract_inbound_count",
            "contract_inbound_files",
            "documentation_inbound_count",
            "documentation_inbound_files",
            "verifier_dependencies",
            "helper_dependencies",
            "uses_sed",
            "uses_awk",
            "uses_rg",
            "uses_decision_table",
        )
    )
    for record in records:
        writer.writerow(
            (
                record.checker,
                record.lines,
                record.inbound_count,
                ",".join(record.inbound_files),
                len(record.executable_inbound_files),
                ",".join(record.executable_inbound_files),
                len(record.contract_inbound_files),
                ",".join(record.contract_inbound_files),
                len(record.documentation_inbound_files),
                ",".join(record.documentation_inbound_files),
                ",".join(record.verifier_dependencies),
                ",".join(record.helper_dependencies),
                "yes" if record.uses_sed else "no",
                "yes" if record.uses_awk else "no",
                "yes" if record.uses_rg else "no",
                "yes" if record.uses_decision_table else "no",
            )
        )
    return output.getvalue()


def expected_inventory(root: Path) -> str:
    return render_inventory(collect_inventory(root))


def check_inventory(root: Path, output_path: Path = OUTPUT_PATH) -> int:
    target = root.resolve() / output_path
    if not target.is_file():
        print(
            f"INVENTORY.UNAVAILABLE [unavailable] (path={output_path.as_posix()}): generated checker inventory is absent"
        )
        return 3
    expected = expected_inventory(root)
    observed = target.read_text(encoding="utf-8")
    if observed != expected:
        print(
            f"INVENTORY.STALE [invalid] (path={output_path.as_posix()}): generated checker inventory does not match repository inputs"
        )
        return 1
    count = len(expected.splitlines()) - 1
    print(f"PASS checker-structure-inventory ({count} current Bash verifiers)")
    return 0


def write_inventory(root: Path, output_path: Path = OUTPUT_PATH) -> int:
    target = root.resolve() / output_path
    target.parent.mkdir(parents=True, exist_ok=True)
    content = expected_inventory(root)
    target.write_text(content, encoding="utf-8")
    print(f"WROTE {output_path.as_posix()} ({len(content.splitlines()) - 1} records)")
    return 0


def main(argv: Sequence[str] | None = None, *, default_repo_root: Path) -> int:
    parser = argparse.ArgumentParser(description="Generate or verify the exact Bash checker structure inventory.")
    parser.add_argument("--repo-root", type=Path, default=default_repo_root)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    return check_inventory(args.repo_root) if args.check else write_inventory(args.repo_root)
