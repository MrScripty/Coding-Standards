#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
CHECKER = Path(__file__).with_name("decision_traceability") / "check.py"
FIXTURES = REPOSITORY / "evaluation/standards-effectiveness/fixtures/traceability"


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments),
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout


def _run(root: Path, *arguments: str, expected: int = 0) -> None:
    completed = subprocess.run(
        (sys.executable, "-P", str(CHECKER), *arguments),
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != expected:
        raise RuntimeError(
            f"expected exit {expected}, observed {completed.returncode}: "
            f"{completed.stderr or completed.stdout}"
        )


def _repository(parent: Path, name: str) -> Path:
    target = parent / name
    shutil.copytree(FIXTURES, target)
    _git(target, "init", "-q")
    _git(target, "config", "user.email", "fixtures@example.invalid")
    _git(target, "config", "user.name", "Standards Fixtures")
    _git(target, "add", ".")
    _git(target, "commit", "-qm", "test: add baseline")
    return target


def run_contract() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)

        staged = _repository(root, "staged")
        _run(staged, "--map", "map.tsv", expected=2)
        with (staged / "src/api/public.ts").open("a", encoding="utf-8") as target:
            target.write("\nexport const stagedChange = true;\n")
        _git(staged, "add", "src/api/public.ts")
        (staged / "map.tsv").write_text(
            "trigger_path\tboundary_id\tprofile\tartifact_path\n",
            encoding="utf-8",
        )
        _run(staged, "--mode", "staged", "--map", "map.tsv", expected=1)
        _git(staged, "restore", "map.tsv")
        _run(staged, "--mode", "staged", "--map", "map.tsv", expected=1)
        with (staged / "src/api/README.md").open("a", encoding="utf-8") as target:
            target.write("\nStaged contract update.\n")
        _run(staged, "--mode", "staged", "--map", "map.tsv", expected=1)
        _git(staged, "add", "src/api/README.md")
        _run(staged, "--mode", "staged", "--map", "map.tsv")
        with (staged / "src/engine/policy.ts").open("a", encoding="utf-8") as target:
            target.write("\nexport const unstagedChange = true;\n")
        _run(staged, "--mode", "staged", "--map", "map.tsv")

        ranged = _repository(root, "range")
        base = _git(ranged, "rev-parse", "HEAD").strip()
        with (ranged / "src/engine/policy.ts").open("a", encoding="utf-8") as target:
            target.write("\nexport const rangeChange = true;\n")
        with (ranged / "docs/adr/ADR-001-engine.md").open(
            "a", encoding="utf-8"
        ) as target:
            target.write("\nRange decision update.\n")
        _git(ranged, "add", "src/engine/policy.ts", "docs/adr/ADR-001-engine.md")
        _git(ranged, "commit", "-qm", "test: update mapped engine decision")
        (ranged / "map.tsv").write_text(
            "trigger_path\tboundary_id\tprofile\tartifact_path\n"
            "# unstaged map must not alter range mode\n",
            encoding="utf-8",
        )
        (ranged / "docs/adr/ADR-001-engine.md").write_text(
            "# unstaged artifact must not alter range mode\n", encoding="utf-8"
        )
        _run(
            ranged,
            "--mode",
            "range",
            "--map",
            "map.tsv",
            "--base-ref",
            base,
            "--head-ref",
            "HEAD",
        )

        unrelated = _repository(root, "unrelated")
        base = _git(unrelated, "rev-parse", "HEAD").strip()
        with (unrelated / "src/engine/policy.ts").open(
            "a", encoding="utf-8"
        ) as target:
            target.write("\nexport const invalidChange = true;\n")
        with (unrelated / "docs/adr/ADR-002-global.md").open(
            "a", encoding="utf-8"
        ) as target:
            target.write("\nUnrelated update.\n")
        _git(
            unrelated,
            "add",
            "src/engine/policy.ts",
            "docs/adr/ADR-002-global.md",
        )
        _git(unrelated, "commit", "-qm", "test: update unrelated decision")
        _run(
            unrelated,
            "--mode",
            "range",
            "--map",
            "map.tsv",
            "--base-ref",
            base,
            "--head-ref",
            "HEAD",
            expected=1,
        )

        removed = _repository(root, "removed-row")
        _git(removed, "rm", "-q", "src/engine/policy.ts")
        (removed / "map.tsv").write_text(
            "trigger_path\tboundary_id\tprofile\tartifact_path\n"
            "src/api/public.ts\tapi\tcontract-readme\tsrc/api/README.md\n",
            encoding="utf-8",
        )
        _git(removed, "add", "map.tsv")
        _run(removed, "--mode", "staged", "--map", "map.tsv", expected=1)

        invalid_header = _repository(root, "invalid-header")
        (invalid_header / "map.tsv").write_text(
            "trigger\tboundary_id\tprofile\tartifact_path\n",
            encoding="utf-8",
        )
        _git(invalid_header, "add", "map.tsv")
        _run(
            invalid_header,
            "--mode",
            "staged",
            "--map",
            "map.tsv",
            expected=2,
        )

        invalid_profile = _repository(root, "invalid-profile")
        (invalid_profile / "map.tsv").write_text(
            "trigger_path\tboundary_id\tprofile\tartifact_path\n"
            "src/api/public.ts\tapi\tunknown\tsrc/api/README.md\n",
            encoding="utf-8",
        )
        _git(invalid_profile, "add", "map.tsv")
        _run(
            invalid_profile,
            "--mode",
            "staged",
            "--map",
            "map.tsv",
            expected=2,
        )


def main() -> int:
    try:
        run_contract()
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"Decision traceability contract failed: {error}", file=sys.stderr)
        return 1
    print("Decision traceability Python contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
