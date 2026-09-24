"""Bounded pure compilation reuse after the caller verifies captured content.

An MCP process owns one cache for its repository, purpose and installed code.
Its serial calls borrow results; stores, handles, decisions and responses remain
per-call. Capacity overflow changes only whether the result is retained.
"""
from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import replace
from enum import Enum
from pathlib import Path, PurePath
import re
import sys
from types import FunctionType, MappingProxyType
from typing import TYPE_CHECKING, cast

from tools.standards_identity.standards_identity import encode_identity_value
from tools.standards_metadata.standards_metadata import FrozenContentSource
from tools.standards_snapshots.standards_snapshots import CapturedContent

from .context_projection import Purpose

if TYPE_CHECKING:
    from .authoring import ProposalRevision
    from .engine import CompiledSnapshot
    from .logical_authoring import LogicalAuthoringCompiler, LogicalProjection


class CompiledSnapshotCache:
    """Retain a bounded mix of snapshot and exact draft material for one owner.

    Snapshot keys bind the exact verified capture and compiler. Draft keys also
    bind the complete logical revision and installed replay recipe. Equality
    distinguishes different material even after a Python hash collision. Current
    lifecycle, root and access decisions remain with the caller, which performs
    complete durable validation before consulting this pure reuse mechanism.
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
            tuple[object, ...], tuple[object, int]
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
        key = ("snapshot", capture, compiler)
        existing = self._lookup(key)
        if existing is not None:
            return cast("CompiledSnapshot", existing)
        result = compiler(FrozenContentSource(
            (str(item.path), item.content) for item in capture.files
        ))
        self._retain(key, result)
        return result

    def project_verified(
        self,
        revision: ProposalRevision,
        base: CompiledSnapshot,
        compiler: LogicalAuthoringCompiler,
    ) -> LogicalProjection:
        """Reuse only the replay of exact, independently verified draft inputs.

        The caller reads the stored revision/root and verifies base content before
        entering. Prospective revisions may also be compiled before publication;
        a cached pure projection is never evidence that a revision was published.
        Snapshot and projection entries share one LRU and one retention budget.
        """
        from .logical_authoring import LogicalProgram

        if self._closed:
            raise ValueError("Compilation cache is closed.")
        if self._purpose is not Purpose.AUTHORING:
            raise ValueError("Proposal material requires authoring purpose.")
        implementation = compiler.compilation_identity
        eligible = (
            implementation is not None
            and all(isinstance(item, FunctionType) and not item.__closure__
                    for item in implementation)
            and type(base.source) is FrozenContentSource
        )
        key = None
        if eligible and self._max_entries and self._max_bytes:
            # Exact values rather than a mutable proposal head or a claimed ID.
            # The existing canonical codec binds the whole program, membership,
            # original base, ordinal and proposal identity without a new format.
            key = (
                "proposal", base.source.files,
                encode_identity_value(revision.identity_material()),
                implementation,
            )
            existing = self._lookup(key)
            if existing is not None:
                retained = cast("LogicalProjection", existing)
                # Semantic intent maps historically belong to each operation.
                # Preserve that ownership while sharing read-only compiled data.
                return replace(retained, semantic_proposals=deepcopy(retained.semantic_proposals))
        else:
            self._misses += 1
        result = compiler.compile(
            base.source, LogicalProgram(revision.change_sets),
            base_snapshot=str(revision.base_snapshot),
            base_repository_paths=revision.base_repository_paths,
            compiled_base=base,
        )
        if key is None:
            self._uncached += 1
        else:
            # Keep the retained intent independent of the cold caller's maps too.
            self._retain(key, replace(result, semantic_proposals=deepcopy(result.semantic_proposals)))
        return result

    def _lookup(self, key: tuple[object, ...]) -> object | None:
        existing = self._entries.get(key)
        if existing is None:
            self._misses += 1
            return None
        self._hits += 1
        self._entries.move_to_end(key)
        return existing[0]

    def _retain(self, key: tuple[object, ...], result: object) -> None:
        size = (
            _retained_size((key, result), self._max_bytes)
            if self._max_entries and self._max_bytes else None
        )
        if size is None:
            self._uncached += 1
            return
        while self._entries and (
            len(self._entries) >= self._max_entries or self._bytes + size > self._max_bytes
        ):
            _, (_, removed_size) = self._entries.popitem(last=False)
            self._bytes -= removed_size
            self._evictions += 1
        self._entries[key] = (result, size)
        self._bytes += size

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
