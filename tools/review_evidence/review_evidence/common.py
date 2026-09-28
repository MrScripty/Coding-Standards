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
    if len(name.encode("utf-8")) > 65535:
        fail("portable member name exceeds ZIP limit", "unsupported")
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
    # A trie validates each component once without materializing every full
    # prefix (quadratic space for a deep but otherwise valid portable path).
    namespace: dict[str, tuple[str, bool, dict]] = {}
    for name in names:
        components = safe_name(name).split("/")
        level = namespace
        for index, component in enumerate(components):
            key = unicodedata.normalize("NFC", component).casefold()
            is_file = index == len(components) - 1
            previous = level.get(key)
            if previous is not None:
                spelling, was_file, children = previous
                if spelling != component or was_file or is_file:
                    fail("duplicate or conflicting portable packet path")
            else:
                children = {}
                level[key] = component, is_file, children
            level = children


def no_symlink_ancestors(path: Path) -> None:
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        if current.is_symlink():
            fail("filesystem path traverses a symlink", "unsupported")
