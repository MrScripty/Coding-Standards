"""Pure proposal inputs retained for one explicitly composed authoring operation."""
from __future__ import annotations

from typing import TYPE_CHECKING

from tools.repository_git.repository_git import RepositoryRevision
from tools.standards_analysis.standards_analysis import AnalysisError, AnalysisFailure
from tools.standards_snapshots.standards_snapshots import SnapshotId

if TYPE_CHECKING:
    from .authoring import ProposalRevision
    from .engine import CompiledSnapshot, StandardsEngine
    from .logical_authoring import LogicalProjection


class ProposalMaterials:
    """Borrow one verified base and the most recent exact proposal projection.

    Focused composition passes this value explicitly through preflight, revision
    validation and analysis. Each access observes current snapshot lifecycle;
    callers still read current revisions, heads and authorization independently.
    No entry survives the operation or supplies publication/recovery authority.
    """

    def __init__(self, engine: StandardsEngine) -> None:
        self._engine = engine
        self._base: tuple[SnapshotId, CompiledSnapshot] | None = None
        self._projection: tuple[ProposalRevision, LogicalProjection] | None = None

    def __enter__(self) -> ProposalMaterials:
        return self

    def __exit__(self, *_: object) -> None:
        self._base = None
        self._projection = None

    def compiled(self, snapshot: SnapshotId) -> CompiledSnapshot:
        if self._base is None:
            compiled = self._engine._compiled_snapshot(snapshot)
            self._base = (snapshot, compiled)
        elif self._base[0] != snapshot:
            raise AnalysisError(
                AnalysisFailure(
                    "ANALYSIS.MATERIAL_INPUT_MISMATCH", "invalid",
                    "Operation material belongs to a different base snapshot.",
                )
            )
        else:
            self._engine._snapshots.snapshot(snapshot)
        return self._base[1]

    def repository_paths(self, snapshot: SnapshotId) -> tuple[str, ...]:
        # Verify captured bytes before using this root's source-revision fact.
        self.compiled(snapshot)
        summary = self._engine._snapshots.snapshot(snapshot)
        paths = self._engine._repository.revision_paths(
            RepositoryRevision(summary.source_revision)
        )
        return tuple(str(path) for path in paths)

    def projection(self, revision: ProposalRevision) -> LogicalProjection:
        accepted = self.compiled(revision.base_snapshot)
        if self._projection is not None and self._projection[0] == revision:
            return self._projection[1]
        projection = self._engine._proposal_projection(revision, accepted, reuse=True)
        # A revision change replaces, rather than accumulates, retained output.
        self._projection = (revision, projection)
        return projection

    def validate_revision(self, revision: ProposalRevision) -> None:
        self.projection(revision)
