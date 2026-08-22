from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


OUTCOMES = frozenset({"invalid", "unavailable", "unsupported"})
EXIT_CODE_BY_OUTCOME = {
    "invalid": 2,
    "unavailable": 3,
    "unsupported": 4,
}


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    outcome: str
    message: str
    suite: str | None = None
    check: str | None = None
    path: str | None = None
    row: int | None = None
    field: str | None = None
    expected: str | None = None
    observed: str | None = None

    def __post_init__(self) -> None:
        if self.outcome not in OUTCOMES:
            raise ValueError(f"unknown diagnostic outcome: {self.outcome}")

    def as_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}

    def render(self) -> str:
        context = []
        for label, value in (
            ("suite", self.suite),
            ("check", self.check),
            ("path", self.path),
            ("row", self.row),
            ("field", self.field),
        ):
            if value is not None:
                context.append(f"{label}={value}")
        location = f" ({', '.join(context)})" if context else ""
        comparison = ""
        if self.expected is not None or self.observed is not None:
            comparison = f"; expected={self.expected!r}, observed={self.observed!r}"
        return f"{self.code} [{self.outcome}]{location}: {self.message}{comparison}"


class EngineError(Exception):
    def __init__(self, diagnostic: Diagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic
        self.exit_code = EXIT_CODE_BY_OUTCOME[diagnostic.outcome]
