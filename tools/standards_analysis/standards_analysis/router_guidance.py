"""Exact Router selection rows shared by compilation, reading and authoring.

Router uses top-level, two-column pipe tables with inline module links in the
last cell. Display headings and non-table examples have no executable meaning.
This is the Router's narrow authored format, not a general Markdown parser.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import re

from tools.standards_metadata.standards_metadata import CanonicalModuleCorpus
from .errors import AnalysisError, AnalysisFailure

_LINK = re.compile(r"\[[^]\n]+\]\(([^)#\s]+)(?:#[^)\s]*)?\)")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_SEPARATOR = re.compile(r"^:?-{3,}:?$")


@dataclass(frozen=True, slots=True)
class RoutingSelectionRow:
    start: int
    end: int
    condition: str
    targets: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RouterGuidance:
    rows: tuple[RoutingSelectionRow, ...]
    insertion_offset: int

    @property
    def targets(self) -> frozenset[str]:
        return frozenset(target for row in self.rows for target in row.targets)


def _cells(line: str) -> tuple[str, ...] | None:
    # Escaped pipes are cell data, including an even/odd run of backslashes.
    stripped = line.rstrip("\r\n").strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    cells, cell = [], []
    escaped = False
    for char in stripped[1:-1]:
        if char == "|" and not escaped:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        escaped = char == "\\" and not escaped
    cells.append("".join(cell).strip())
    return tuple(cells)


def parse_router_guidance(
    text: str, modules: CanonicalModuleCorpus, *, source_path: str = "STANDARDS-ROUTER.md",
) -> RouterGuidance:
    """Return exact selection spans and canonical targets, excluding references."""
    def invalid(message: str, field: str | None = None) -> AnalysisError:
        return AnalysisError(AnalysisFailure(
            "ROUTER_PROJECTION.INVALID", "invalid", message, source_path, field,
        ))

    by_path = {module.path: module for module in modules.modules}
    lines = text.splitlines(keepends=True)
    offsets, visible = [0], []
    fence: str | None = None
    fence_length = 0
    comment = False
    for line in lines:
        offsets.append(offsets[-1] + len(line))
        marker = _FENCE.match(line)
        if fence is not None:
            visible.append(False)
            if marker and marker[1][0] == fence and len(marker[1]) >= fence_length and not line[marker.end():].strip():
                fence = None
            continue
        if comment:
            visible.append(False)
            comment = "-->" not in line
            continue
        if marker:
            fence, fence_length = marker[1][0], len(marker[1])
            visible.append(False)
        elif "<!--" in line:
            comment = "-->" not in line.split("<!--", 1)[1]
            visible.append(False)
        else:
            visible.append(not line.startswith(("    ", "\t")))

    rows: list[RoutingSelectionRow] = []
    insertion = -1
    index = 0
    while index + 1 < len(lines):
        header = _cells(lines[index]) if visible[index] else None
        separator = _cells(lines[index + 1]) if visible[index + 1] else None
        if (header is None or len(header) != 2 or separator is None or len(separator) != 2
                or not all(_SEPARATOR.fullmatch(cell) for cell in separator)):
            index += 1
            continue
        table_start = len(rows)
        index += 2
        while index < len(lines) and visible[index]:
            cells = _cells(lines[index])
            if cells is None:
                break
            if len(cells) != 2:
                raise invalid("Router selection rows require two cells.")
            # Inline code is explanatory content, not a destination declaration.
            destination_cell = re.sub(r"(`+).*?\1", "", cells[1])
            targets = []
            for destination in _LINK.findall(destination_cell):
                path = PurePosixPath(destination)
                if (path.is_absolute() or ".." in path.parts or destination.startswith("./")
                        or str(path) != destination):
                    raise invalid("Router selection link must be repository-relative.", destination)
                module = by_path.get(destination)
                if module is None:
                    raise invalid("Router selection link must resolve to a canonical module.", destination)
                if module.role != "reference":
                    targets.append(module.module_id)
            if len(targets) != len(set(targets)):
                raise invalid("A selection row declares each target once.")
            if targets:
                rows.append(RoutingSelectionRow(
                    offsets[index], offsets[index + 1],
                    re.sub(r"\\([\\|])", r"\1", cells[0]), tuple(targets),
                ))
            index += 1
        if len(rows) > table_start:
            insertion = offsets[index]
    if not rows:
        raise invalid("Router selection tables contain no canonical targets.")
    return RouterGuidance(tuple(rows), insertion)
