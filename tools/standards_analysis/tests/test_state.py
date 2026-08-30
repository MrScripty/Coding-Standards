from __future__ import annotations

import unittest

from tools.standards_analysis.standards_analysis import AnalysisError
from tools.standards_analysis.standards_analysis.state import AnalysisState
from tools.standards_snapshots.standards_snapshots import SnapshotId


BASE = SnapshotId("snapshot:v1:00000000-0000-4000-8000-000000000001")
PROPOSED = SnapshotId("snapshot:v1:00000000-0000-4000-8000-000000000002")
CHANGE = {
    "kind": "modification",
    "accepted_ids": ["policy.example"],
    "proposed_ids": ["policy.example"],
    "scope": {"kind": "whole-artifact"},
}
CONTRACTS = (
    {"id": "analysis", "version": "4"},
    {"id": "identity", "version": "2"},
)
EXECUTION = {
    "authorization_authority_digest": None,
    "providers": [],
}


def _state(**overrides: object) -> AnalysisState:
    values: dict[str, object] = {
        "base_snapshot": BASE,
        "proposed_snapshot": PROPOSED,
        "changes": (CHANGE,),
        "domain_contracts": CONTRACTS,
        "execution_contracts": EXECUTION,
    }
    values.update(overrides)
    return AnalysisState(**values)


class AnalysisStateTest(unittest.TestCase):
    def test_round_trip_preserves_canonical_identity(self) -> None:
        state = _state()

        decoded = AnalysisState.decode(state.encode())

        self.assertEqual(decoded, state)
        self.assertEqual(decoded.analysis_id, state.analysis_id)

    def test_decision_order_does_not_change_identity(self) -> None:
        first = {
            "requirement_id": "sha256:" + "a" * 64,
            "value": {"type": "boolean", "state": "known", "value": True},
        }
        second = {
            "requirement_id": "sha256:" + "b" * 64,
            "value": {"type": "boolean", "state": "known", "value": False},
        }

        left = _state(fact_observations=(first, second))
        right = _state(fact_observations=(second, first))

        self.assertEqual(left.analysis_id, right.analysis_id)
        self.assertEqual(left.encode(), right.encode())

    def test_different_decision_evidence_changes_identity(self) -> None:
        shared = {
            "requirement_id": "sha256:" + "a" * 64,
            "value": {"type": "boolean", "state": "known", "value": True},
        }

        left = _state(fact_observations=({**shared, "evidence": ["left"]},))
        right = _state(fact_observations=({**shared, "evidence": ["right"]},))

        self.assertNotEqual(left.analysis_id, right.analysis_id)

    def test_conflicting_decisions_cannot_share_one_state(self) -> None:
        requirement = "sha256:" + "a" * 64

        with self.assertRaisesRegex(AnalysisError, "conflicting decisions"):
            _state(
                fact_observations=(
                    {"requirement_id": requirement, "value": True},
                    {"requirement_id": requirement, "value": False},
                )
            )

    def test_analysis_aggregate_declares_exact_snapshot_roots(self) -> None:
        state = _state()

        aggregate = state.aggregate(())

        self.assertEqual(aggregate.aggregate_id, state.analysis_id)
        self.assertEqual(aggregate.kind, "analysis-state")
        self.assertEqual(aggregate.snapshots, (BASE, PROPOSED))
        self.assertEqual(aggregate.payload, state.encode())


if __name__ == "__main__":
    unittest.main()
