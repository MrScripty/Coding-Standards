from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..diagnostics import Diagnostic, EngineError
from ..model import CheckAuthorityInput, CheckContext, present_inputs
from ..paths import contained_file
from .markdown_links import local_markdown_targets


@dataclass(frozen=True, slots=True)
class MarkdownTargetsCheck:
    """Check navigation destinations independently of link labels and prose."""

    id: str
    path: str
    required: tuple[str, ...]

    def authority_inputs(
        self, context: CheckContext
    ) -> tuple[CheckAuthorityInput, ...]:
        return present_inputs("markdown", self.path) + present_inputs(
            "target", *self.required
        )

    def run(self, context: CheckContext) -> list[Diagnostic]:
        for path in self.required:
            contained_file(
                context.repo_root, path, suite=context.suite_id, check=self.id
            )
        actual = {
            target.repository_path
            for target in local_markdown_targets(context, self.id, self.path)
        }
        return [
            Diagnostic(
                "ASSERT.MARKDOWN_TARGET_MISSING",
                "invalid",
                "required navigation destination is missing",
                suite=context.suite_id,
                check=self.id,
                path=self.path,
                expected=target,
            )
            for target in self.required
            if target not in actual
        ]


def parse_markdown_targets_check(
    raw: dict[str, Any], suite_id: str
) -> MarkdownTargetsCheck:
    if (
        set(raw) != {"id", "type", "path", "required"}
        or not isinstance(raw["id"], str)
        or not raw["id"]
        or not isinstance(raw["path"], str)
        or not raw["path"]
        or not isinstance(raw["required"], list)
        or not raw["required"]
        or any(not isinstance(item, str) or not item for item in raw["required"])
        or len(set(raw["required"])) != len(raw["required"])
    ):
        raise EngineError(
            Diagnostic(
                "CONFIG.MARKDOWN_TARGETS",
                "invalid",
                "navigation check requires a path and unique target paths",
                suite=suite_id,
            )
        )
    return MarkdownTargetsCheck(raw["id"], raw["path"], tuple(raw["required"]))
