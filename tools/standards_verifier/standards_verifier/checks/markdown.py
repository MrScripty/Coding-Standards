from __future__ import annotations

import re
from dataclasses import dataclass


ATX_HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)")
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")


@dataclass(frozen=True, slots=True)
class MarkdownHeading:
    line_number: int
    level: int
    text: str


def scan_headings(content: str) -> tuple[MarkdownHeading, ...]:
    headings = []
    fence_character: str | None = None
    fence_length = 0
    for line_number, line in enumerate(content.splitlines(), start=1):
        fence = FENCE_OPEN.match(line)
        if fence_character is not None:
            if (
                fence is not None
                and fence.group(1)[0] == fence_character
                and len(fence.group(1)) >= fence_length
                and not line[fence.end() :].strip()
            ):
                fence_character = None
                fence_length = 0
            continue
        if fence is not None:
            fence_character = fence.group(1)[0]
            fence_length = len(fence.group(1))
            continue
        heading = ATX_HEADING.match(line)
        if heading is not None:
            headings.append(
                MarkdownHeading(line_number, len(heading.group(1)), line)
            )
    return tuple(headings)


def heading_level(text: str) -> int | None:
    heading = ATX_HEADING.match(text)
    if heading is None:
        return None
    return len(heading.group(1))
