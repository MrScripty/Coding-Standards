"""Shared bounded packet values and safe portable names."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

from tools.repository_git.repository_git import GitRepositoryError, RepositoryPath

FORMAT = 1
MEMBER_LIMIT = 64 * 1024 * 1024
TOTAL_LIMIT = 256 * 1024 * 1024
COUNT_LIMIT = 4096
REQUEST_LIMIT = 1024 * 1024
SHA = re.compile(r"sha256:[0-9a-f]{64}\Z")
VERSION = "0.1.0"


class PacketError(Exception):
    def __init__(self, kind: str, message: str):
        self.kind = kind
        super().__init__(message)


def fail(message: str, kind: str = "invalid") -> None:
    raise PacketError(kind, message)


def encoded(value: object) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def markdown(value: str) -> str:
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", value)


def safe_name(name: str) -> str:
    try:
        path = RepositoryPath.parse(name)
    except GitRepositoryError:
        fail("unsafe portable member name", "unsupported")
    for component in path.components:
        if component.endswith((" ", ".")) or any(
            ord(c) < 32 or ord(c) == 127 or c in '<>:"|?*' for c in component
        ):
            fail("unsafe portable member name", "unsupported")
        if component.split(".")[0].casefold() in {
            "con",
            "prn",
            "aux",
            "nul",
            *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10)),
        }:
            fail("unsafe portable member name", "unsupported")
    return str(path)


def check_names(names: list[str]) -> None:
    folded: set[str] = set()
    for name in names:
        safe_name(name)
        key = unicodedata.normalize("NFC", name).casefold()
        if key in folded:
            fail("duplicate or case-colliding packet member")
        folded.add(key)


def no_symlink_ancestors(path: Path) -> None:
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        if current.is_symlink():
            fail("filesystem path traverses a symlink", "unsupported")
