"""Bounded reuse of pure identity and compilation products of exact material.

An MCP process owns one cache for its repository, purpose and installed code.
Its serial calls borrow results; stores, handles, decisions and responses remain
per-call. Capacity overflow changes only whether the result is retained.
"""
from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass, replace
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


@dataclass(frozen=True, slots=True)
class _SnapshotMaterial:
    """Two pure products of one exact capture, charged as one retained entry."""

    identity: tuple[Callable[[CapturedContent], str], str] | None = None
    compilation: tuple[Callable[[FrozenContentSource], CompiledSnapshot], CompiledSnapshot] | None = None


class CompiledSnapshotCache:
    """Retain a bounded mix of snapshot and exact draft material for one owner.

    Snapshot entries bind the exact capture and check the codec/compiler identity.
    Draft keys bind the complete logical revision and installed replay recipe. Equality
    distinguishes different material even after a Python hash collision. Current
    lifecycle, root and access decisions remain with the caller, which performs
    complete durable validation before reusing material for a handle. Successful
    capture admission may seed its independently proved compilation; retention
    never establishes current snapshot existence or permission.
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
        self._identity_hits = self._identity_misses = self._identity_uncached = 0

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
        key = ("snapshot", capture)
        entry = self._entries.get(key)
        material = cast(_SnapshotMaterial, entry[0]) if entry is not None else _SnapshotMaterial()
        if material.compilation is not None and material.compilation[0] is compiler:
            self._hits += 1
            self._entries.move_to_end(key)
            return material.compilation[1]
        self._misses += 1
        result = compiler(FrozenContentSource(
            (str(item.path), item.content) for item in capture.files
        ))
        if not self.retain_verified(capture, compiler, result):
            self._uncached += 1
        return result

    def retain_verified(
        self, capture: CapturedContent,
        compiler: Callable[[FrozenContentSource], CompiledSnapshot],
        compiled: CompiledSnapshot,
    ) -> bool:
        """Retain a caller-proved pure compilation under the existing budget.

        Ordinary compilation and the Engine's admitted live/frozen capture proof
        use the same retention owner. The caller binds the result to this exact
        capture and compiler, with a frozen source and no live recorder/reader.
        No snapshot identity, existence, lifecycle or authorization is cached;
        later handle observations must still validate their durable material.
        """
        if self._closed:
            raise ValueError("Compilation cache is closed.")
        if not isinstance(compiler, FunctionType) or compiler.__closure__:
            return False
        key = ("snapshot", capture)
        entry = self._entries.get(key)
        material = cast(_SnapshotMaterial, entry[0]) if entry is not None else _SnapshotMaterial()
        return self._retain(key, replace(material, compilation=(compiler, compiled)))

    def identify_content(
        self, capture: CapturedContent, calculate: Callable[[CapturedContent], str],
    ) -> str:
        """Reuse the Snapshot owner's codec only for exactly equal loaded material.

        The caller still reads and validates durable bytes and compares this result
        with the stored content ID. This proof is neither a lifecycle observation
        nor evidence that a snapshot exists. Identity and compilation share one
        capture entry, LRU and byte budget; no extra cache can outlive this owner.
        """
        if self._closed:
            raise ValueError("Compilation cache is closed.")
        if not isinstance(calculate, FunctionType) or calculate.__closure__:
            self._identity_misses += 1
            self._identity_uncached += 1
            return calculate(capture)
        key = ("snapshot", capture)
        entry = self._entries.get(key)
        material = cast(_SnapshotMaterial, entry[0]) if entry is not None else _SnapshotMaterial()
        if material.identity is not None and material.identity[0] is calculate:
            self._identity_hits += 1
            self._entries.move_to_end(key)
            return material.identity[1]
        self._identity_misses += 1
        if entry is not None:
            # Extending a proof must keep the capture already owned by this entry.
            # A fresh equal load must not replace that key while its compilation
            # still shares the original bytes, retaining a duplicate byte set.
            key = next(retained for retained in self._entries if retained == key)
        identity = calculate(capture)
        if not self._retain(key, replace(material, identity=(calculate, identity))):
            self._identity_uncached += 1
        return identity

    def project_verified(
        self,
        revision: ProposalRevision,
        base: CompiledSnapshot,
        compiler: LogicalAuthoringCompiler,
        *,
        predecessor: LogicalProjection | None = None,
    ) -> LogicalProjection:
        """Construct exact verified drafts from cached output or a matching prefix.

        Prefix admission remains with the logical compiler. The optional local
        predecessor and existing retained entries supply computation, not authority.
        The caller reads the stored revision/root and verifies base content before
        entering. Prospective revisions may also be compiled before publication;
        a cached pure projection is never evidence that a revision was published.
        Snapshot and projection entries share one LRU and one retention budget.
        """
        from .authoring import ProposalRevision
        from .logical_authoring import LogicalProgram

        if self._closed:
            raise ValueError("Compilation cache is closed.")
        if self._purpose is not Purpose.AUTHORING:
            raise ValueError("Proposal material requires authoring purpose.")
        implementation = compiler.compilation_identity
        eligible = (
            implementation is not None
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
        if key is not None and predecessor is None and revision.ordinal > 1:
            previous = ProposalRevision(
                revision.proposal, revision.ordinal - 1, revision.base_snapshot,
                revision.base_repository_paths, revision.change_sets[:-1],
            )
            previous_key = (
                "proposal", base.source.files,
                encode_identity_value(previous.identity_material()), implementation,
            )
            # Borrow from the existing bounded store, without retaining another
            # entry or promoting a computational prefix over the final result.
            previous_entry = self._entries.get(previous_key)
            if previous_entry is not None:
                predecessor = cast("LogicalProjection", previous_entry[0])
        result = compiler.compile(
            base.source, LogicalProgram(revision.change_sets),
            base_snapshot=str(revision.base_snapshot),
            base_repository_paths=revision.base_repository_paths,
            compiled_base=base,
            predecessor=predecessor,
        )
        if key is None:
            self._uncached += 1
        else:
            # Operation-local borrowing can skip a base cache lookup. Successful
            # projection construction used that exact base, not just its prefix.
            # Make an already retained base recent before inserting the result;
            # this neither pins missing material nor increases either budget.
            for base_key, (material, _) in self._entries.items():
                if (isinstance(material, _SnapshotMaterial)
                        and material.compilation is not None
                        and material.compilation[1] is base):
                    self._entries.move_to_end(base_key)
                    break
            # Keep the retained intent independent of the cold caller's maps too.
            if not self._retain(key, replace(result, semantic_proposals=deepcopy(result.semantic_proposals))):
                self._uncached += 1
        return result

    def _lookup(self, key: tuple[object, ...]) -> object | None:
        existing = self._entries.get(key)
        if existing is None:
            self._misses += 1
            return None
        self._hits += 1
        self._entries.move_to_end(key)
        return existing[0]

    def _retain(self, key: tuple[object, ...], result: object) -> bool:
        size = (
            _retained_size((key, result), self._max_bytes)
            if self._max_entries and self._max_bytes else None
        )
        if size is None:
            return False
        previous = self._entries.pop(key, None)
        if previous is not None:
            self._bytes -= previous[1]
        while self._entries and (
            len(self._entries) >= self._max_entries or self._bytes + size > self._max_bytes
        ):
            _, (_, removed_size) = self._entries.popitem(last=False)
            self._bytes -= removed_size
            self._evictions += 1
        self._entries[key] = (result, size)
        self._bytes += size
        return True

    @property
    def statistics(self) -> dict[str, int]:
        """Diagnostics for owned entries, distinct from transient or RSS memory."""
        return {
            "entries": len(self._entries), "accounted_bytes": self._bytes,
            "hits": self._hits, "misses": self._misses,
            "evictions": self._evictions, "uncached": self._uncached,
            "identity_hits": self._identity_hits, "identity_misses": self._identity_misses,
            "identity_uncached": self._identity_uncached,
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
