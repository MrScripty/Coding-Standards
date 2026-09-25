"""Immutable computation provenance for a logical projection, not acceptance.

The compiler snapshots inputs before replay and returns continuation material
only after final compilation and cumulative analysis succeed. These values retain
no storage, lifecycle, authorization or publication decisions. A non-matching
value selects complete replay of the requested authoritative inputs.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectionInputs:
    base_files: tuple[tuple[str, bytes], ...]
    base_snapshot: str | None
    base_repository_paths: tuple[str, ...]
    # Snapshots of the existing canonical change-set representation, not live
    # edit mappings: nested authored values may still belong to their caller.
    change_sets: tuple[str, ...]
    implementation: tuple[Callable[..., object], ...]

    def prefix_length(self, successor: ProjectionInputs) -> int:
        """Return a strictly shorter exact prefix, or zero for complete replay."""
        length = len(self.change_sets)
        if (
            not 0 < length < len(successor.change_sets)
            or self.implementation != successor.implementation
            or self.base_snapshot != successor.base_snapshot
            or self.base_repository_paths != successor.base_repository_paths
            or self.base_files != successor.base_files
            or self.change_sets != successor.change_sets[:length]
        ):
            return 0
        return length


@dataclass(frozen=True, slots=True)
class ProjectionContinuation:
    inputs: ProjectionInputs
    projected_files: tuple[tuple[str, bytes], ...]
    repository_paths: tuple[str, ...]

    def prefix_length(
        self,
        successor: ProjectionInputs,
        *,
        projected_files: tuple[tuple[str, bytes], ...],
        repository_paths: tuple[str, ...],
    ) -> int:
        """Bind the offered material as well as its claimed computation inputs."""
        if (
            projected_files != self.projected_files
            or repository_paths != self.repository_paths
        ):
            return 0
        return self.inputs.prefix_length(successor)
