#!/usr/bin/env python3
"""Inventory fixed Standards Engine source trees for the A1/A1b audit.

This intentionally reports descriptive measures. It does not classify a design,
dependency, Interface, test, or file as necessary or unnecessary.
"""

from __future__ import annotations

import ast
import json
import sys
from collections import Counter
from pathlib import Path


PACKAGE_NAMES = (
    "graph_engine",
    "standards_applicability",
    "standards_metadata",
    "standards_policy_impact",
    "standards_graph",
    "standards_analysis",
    "standards_identity",
    "standards_contracts",
    "standards_authority",
    "standards_engine",
    "standards_verifier",
)


def python_files(path: Path) -> list[Path]:
    return sorted(p for p in path.rglob("*.py") if "__pycache__" not in p.parts)


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def literal_names(node: ast.AST, known: dict[str, list[str]]) -> list[str]:
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        result: list[str] = []
        for item in node.elts:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                result.append(item.value)
            elif isinstance(item, ast.Starred) and isinstance(item.value, ast.Name):
                result.extend(known.get(item.value.id, []))
            elif (
                isinstance(item, ast.Starred)
                and isinstance(item.value, ast.Attribute)
                and isinstance(item.value.value, ast.Name)
                and item.value.attr == "__all__"
            ):
                result.extend(known.get(f"{item.value.value.id}.__all__", []))
        return result
    if isinstance(node, ast.Name):
        return list(known.get(node.id, []))
    return []


def module_all(path: Path, package_dir: Path) -> list[str]:
    """Resolve the local relative-import patterns used by audited package roots."""
    tree = parse(path)
    known: dict[str, list[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.level == 1:
            if node.module:
                target = package_dir / f"{node.module}.py"
                if target.exists():
                    target_all = module_all(target, package_dir)
                    for alias in node.names:
                        if alias.name == "__all__":
                            known[alias.asname or alias.name] = target_all
            else:
                for alias in node.names:
                    target = package_dir / f"{alias.name}.py"
                    if target.exists():
                        known[f"{alias.asname or alias.name}.__all__"] = module_all(
                            target, package_dir
                        )
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            value = node.value
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names = literal_names(value, known)
                    if names:
                        known[target.id] = names
    return known.get("__all__", [])


def definitions(paths: list[Path]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in paths:
        for node in ast.walk(parse(path)):
            if isinstance(node, ast.ClassDef):
                counts["classes"] += 1
            elif isinstance(node, ast.AsyncFunctionDef):
                counts["async_functions"] += 1
                if node.name.startswith("test_"):
                    counts["tests"] += 1
            elif isinstance(node, ast.FunctionDef):
                counts["functions"] += 1
                if node.name.startswith("test_"):
                    counts["tests"] += 1
    return counts


def imports(paths: list[Path]) -> list[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for path in paths:
        source = next((part for part in path.parts if part in PACKAGE_NAMES), None)
        if source is None:
            continue
        for node in ast.walk(parse(path)):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                bits = name.split(".")
                target = bits[1] if bits[0] == "tools" and len(bits) > 1 else bits[0]
                if target in PACKAGE_NAMES and target != source:
                    edges.add((source, target))
    return sorted(edges)


def schema_stats(root: Path) -> dict[str, int]:
    path = root / "tools/standards_engine/contracts/a1-contract.schema.json"
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    definitions = value.get("$defs", value.get("definitions", {}))
    return {"lines": line_count(path), "definitions": len(definitions)}


def analyze(label: str, root: Path) -> dict[str, object]:
    package_data: dict[str, object] = {}
    production_paths: list[Path] = []
    test_paths: list[Path] = []
    for package in PACKAGE_NAMES:
        package_root = root / "tools" / package
        if not package_root.exists():
            continue
        all_paths = python_files(package_root)
        package_tests = [p for p in all_paths if "tests" in p.parts]
        package_prod = [p for p in all_paths if "tests" not in p.parts]
        production_paths.extend(package_prod)
        test_paths.extend(package_tests)
        init_path = package_root / package / "__init__.py"
        exports = module_all(init_path, init_path.parent) if init_path.exists() else []
        package_data[package] = {
            "production_files": len(package_prod),
            "production_lines": sum(line_count(p) for p in package_prod),
            "test_files": len(package_tests),
            "test_lines": sum(line_count(p) for p in package_tests),
            "test_functions": definitions(package_tests)["tests"],
            "public_exports": len(set(exports)),
        }

    engine_file = root / "tools/standards_engine/standards_engine/engine.py"
    generated_file = (
        root / "tools/standards_engine/standards_engine/_generated_contract.py"
    )
    generated_exports = (
        module_all(generated_file, generated_file.parent)
        if generated_file.exists()
        else []
    )
    registry = root / "evaluation/standards-effectiveness/suite-registry.toml"
    checker_files = sorted(
        (root / "evaluation/standards-effectiveness").glob("verify-*.sh")
    )
    registry_text = registry.read_text(encoding="utf-8") if registry.exists() else ""
    production_definitions = definitions(production_paths)
    package_edges = imports(production_paths)
    return {
        "label": label,
        "packages": package_data,
        "totals": {
            "production_files": len(production_paths),
            "production_lines": sum(line_count(p) for p in production_paths),
            "test_files": len(test_paths),
            "test_lines": sum(line_count(p) for p in test_paths),
            "test_functions": definitions(test_paths)["tests"],
            "classes": production_definitions["classes"],
            "functions": production_definitions["functions"],
            "internal_import_edges": len(package_edges),
            "registered_suite_entries": registry_text.count("[[suites]]"),
            "verify_shell_files": len(checker_files),
        },
        "internal_import_edges": package_edges,
        "schema": schema_stats(root),
        "engine_lines": line_count(engine_file) if engine_file.exists() else 0,
        "generated_contract_lines": (
            line_count(generated_file) if generated_file.exists() else 0
        ),
        "generated_contract_exports": len(set(generated_exports)),
    }


def main() -> None:
    if len(sys.argv) < 3 or len(sys.argv) % 2 == 0:
        raise SystemExit(
            "usage: architecture_metrics.py LABEL ROOT [LABEL ROOT ...]"
        )
    reports = [
        analyze(sys.argv[index], Path(sys.argv[index + 1]))
        for index in range(1, len(sys.argv), 2)
    ]
    print(json.dumps(reports, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
