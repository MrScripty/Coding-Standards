"""Bounded pure compilation reuse after the caller verifies captured content.

An MCP process owns one cache for its repository, purpose and installed code.
Its serial calls borrow results; stores, handles, decisions and responses remain
per-call. Capacity overflow changes only whether the result is retained.
"""
from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable, Mapping
from enum import Enum
from pathlib import Path, PurePath
import re
import sys
from types import FunctionType, MappingProxyType
from typing import TYPE_CHECKING

from tools.standards_metadata.standards_metadata import FrozenContentSource
from tools.standards_snapshots.standards_snapshots import CapturedContent

from .context_projection import Purpose

if TYPE_CHECKING:
    from .engine import CompiledSnapshot


class CompiledSnapshotCache:
    """Retain at most a representative base/proposed pair for one serial owner.

    A key contains the exact *already verified* capture and compiler callable.
    Equality includes bytes, paths and source revision; a Python hash collision
    cannot identify different material. No snapshot lifecycle or access decision
    is stored here. Each caller performs its complete durable read first.
    """

    def __init__(
        self, root: Path, purpose: Purpose | str, *,
        max_entries: int = 2, max_bytes: int = 32 * 1024 * 1024,
    ) -> None:
        if any(type(value) is not int or value < 0 for value in (max_entries, max_bytes)):
            raise ValueError("Compilation cache bounds must be nonnegative integers.")
        self._root = root.resolve()
        self._purpose = Purpose(purpose)
        self._max_entries = max_entries
        self._max_bytes = max_bytes
        self._entries: OrderedDict[
            tuple[CapturedContent, Callable], tuple[CompiledSnapshot, int]
        ] = OrderedDict()
        self._bytes = 0
        self._closed = False
        self._hits = self._misses = self._evictions = self._uncached = 0

    def require_scope(self, root: Path, purpose: Purpose | str) -> None:
        if self._closed:
            raise ValueError("Compilation cache is closed.")
        if root.resolve() != self._root or Purpose(purpose) is not self._purpose:
            raise ValueError("Compilation cache belongs to another repository or purpose.")

    def compile_verified(
        self, capture: CapturedContent,
        compiler: Callable[[FrozenContentSource], CompiledSnapshot],
    ) -> CompiledSnapshot:
        if self._closed:
            raise ValueError("Compilation cache is closed.")
        # Stateful or closure-based compiler adapters remain valid cold callers.
        # Retention is reserved for the installed, stateless compiler function.
        if not isinstance(compiler, FunctionType) or compiler.__closure__:
            self._misses += 1
            self._uncached += 1
            return compiler(FrozenContentSource(
                (str(item.path), item.content) for item in capture.files
            ))
        key = (capture, compiler)
        existing = self._entries.get(key)
        if existing is not None:
            self._hits += 1
            self._entries.move_to_end(key)
            return existing[0]
        self._misses += 1
        result = compiler(FrozenContentSource(
            (str(item.path), item.content) for item in capture.files
        ))
        size = (
            _retained_size((key, result), self._max_bytes)
            if self._max_entries and self._max_bytes else None
        )
        if size is None:
            self._uncached += 1
            return result
        while self._entries and (
            len(self._entries) >= self._max_entries or self._bytes + size > self._max_bytes
        ):
            _, (_, removed_size) = self._entries.popitem(last=False)
            self._bytes -= removed_size
            self._evictions += 1
        self._entries[key] = (result, size)
        self._bytes += size
        return result

    @property
    def statistics(self) -> dict[str, int]:
        """Diagnostics for owned entries, distinct from transient or RSS memory."""
        return {
            "entries": len(self._entries), "accounted_bytes": self._bytes,
            "hits": self._hits, "misses": self._misses,
            "evictions": self._evictions, "uncached": self._uncached,
        }

    def close(self) -> None:
        self._entries.clear()
        self._bytes = 0
        self._closed = True


def _retained_size(root: object, limit: int) -> int | None:
    """Conservatively charge the reachable data graph once per entry.

    sys.getsizeof includes Python container/native pattern storage. Mapping
    proxies additionally charge a same-population dictionary table. Shared data
    between entries is charged independently, so accounting may overestimate.
    Imported classes/functions are implementation state, not entry-owned data.
    Unknown native objects or closures make an entry ineligible for retention.
    The bounded LRU bookkeeping and active-operation memory are separate.
    """
    pending = [root]
    seen: set[int] = set()
    total = 0
    while pending:
        value = pending.pop()
        identity = id(value)
        if identity in seen:
            continue
        seen.add(identity)
        if isinstance(value, type):
            continue
        if isinstance(value, FunctionType):
            if value.__closure__:
                return None
            continue
        total += sys.getsizeof(value)
        if total > limit:
            return None
        if value is None or type(value) in (bool, int, float, str, bytes):
            continue
        if isinstance(value, Enum):
            pending.append(value.value)
        elif isinstance(value, Mapping):
            if isinstance(value, MappingProxyType):
                # Owned compiler models construct these from ordinary dictionaries.
                total += sys.getsizeof(dict.fromkeys(value))
            elif type(value) is not dict:
                # The Mapping protocol does not describe its backing allocation.
                return None
            pending.extend(value.keys())
            pending.extend(value.values())
        elif isinstance(value, (tuple, list, set, frozenset)):
            pending.extend(value)
        elif isinstance(value, re.Pattern):
            pending.append(value.pattern)
        elif isinstance(value, PurePath) or type(value).__module__.startswith("tools."):
            if isinstance(value, PurePath):
                # Materialize pathlib's lazy value caches before charging slots.
                str(value), value.parts, hash(value)
            if hasattr(value, "__dict__"):
                pending.append(vars(value))
            for cls in type(value).__mro__:
                slots = cls.__dict__.get("__slots__", ())
                if isinstance(slots, str):
                    slots = (slots,)
                for slot in slots:
                    if slot not in ("__dict__", "__weakref__") and hasattr(value, slot):
                        pending.append(getattr(value, slot))
        else:
            return None
    return total if total <= limit else None
