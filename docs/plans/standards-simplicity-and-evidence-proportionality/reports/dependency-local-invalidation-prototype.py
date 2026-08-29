#!/usr/bin/env python3
"""Probe dependency-local policy-coverage invalidation against the live graph.

This is decision evidence for Milestone 0, not a verifier implementation.  It
compiles the repository's current policy-impact authority, derives a bounded
fingerprint for every policy-unit subject, applies representative mutations in
memory, and rejects any result that either misses a dependency or invalidates
an unrelated subject.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Mapping

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from tools.standards_analysis.standards_analysis import (  # noqa: E402
    SUITE_INPUT_CONTRACT,
    SUITE_INPUT_SCHEMA_VERSION,
    AnalysisError,
    derive_coverage_view,
    load_captured_coverage_horizon,
    load_suite_input_manifest,
)
from tools.standards_analysis.standards_analysis.suite_inputs import (  # noqa: E402
    load_captured_suite_input_manifest,
)
from tools.standards_applicability.standards_applicability import (  # noqa: E402
    LANGUAGE_VERSION,
)
from tools.standards_metadata.standards_metadata import (  # noqa: E402
    load_canonical_standards_corpus,
)
from tools.standards_policy_impact.standards_policy_impact import (  # noqa: E402
    compile_policy_impact,
)


SUITE_REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"
SUITE_INPUTS = "evaluation/standards-effectiveness/generated/suite-inputs.json"
ALGEBRA_VERSION = "dependency-local-policy-coverage:v1"


def digest(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True, slots=True)
class EdgeDependency:
    edge_id: str
    source: str
    consumer: str
    evidence_suite: str
    relationship_fingerprint: str
    consumer_fingerprint: str
    evidence_fingerprint: str

    def projection(self) -> dict[str, str]:
        return {
            "edge_id": self.edge_id,
            "source": self.source,
            "consumer": self.consumer,
            "evidence_suite": self.evidence_suite,
            "relationship_fingerprint": self.relationship_fingerprint,
            "consumer_fingerprint": self.consumer_fingerprint,
            "evidence_fingerprint": self.evidence_fingerprint,
        }


@dataclass(frozen=True, slots=True)
class LocalSnapshot:
    protocol_fingerprint: str
    units: Mapping[str, str]
    edges: Mapping[str, tuple[EdgeDependency, ...]]

    def subject_fingerprint(self, subject: str) -> str:
        return digest(
            {
                "algebra": ALGEBRA_VERSION,
                "protocol": self.protocol_fingerprint,
                "subject": subject,
                "unit": self.units[subject],
                "relationships": [
                    edge.projection() for edge in self.edges.get(subject, ())
                ],
            }
        )

    def fingerprints(self) -> dict[str, str]:
        return {
            subject: self.subject_fingerprint(subject)
            for subject in sorted(self.units)
        }


def load_suite_dependencies() -> tuple[
    dict[str, str], dict[str, tuple[str, ...]], str
]:
    with (REPO_ROOT / SUITE_REGISTRY).open("rb") as handle:
        raw = tomllib.load(handle)
    entries = raw.get("suites")
    if raw.get("schema_version") != 1 or not isinstance(entries, list):
        raise ValueError("suite registry does not use the expected schema")

    by_id: dict[str, Mapping[str, object]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("suite registry entry is not a table")
        suite_id = entry.get("id")
        if not isinstance(suite_id, str) or suite_id in by_id:
            raise ValueError("suite registry IDs must be unique strings")
        by_id[suite_id] = entry

    live_index_status = "current"
    try:
        load_suite_input_manifest(
            REPO_ROOT,
            SUITE_INPUTS,
            SUITE_REGISTRY,
            entries,
        )
    except AnalysisError as error:
        if (
            error.failure.code != "SUITE_INPUT.STALE"
            or error.failure.field != "repository_index"
        ):
            raise
        live_index_status = (
            f"stale:{error.failure.code}:{error.failure.field}"
        )

    manifest = load_captured_suite_input_manifest(
        REPO_ROOT,
        SUITE_INPUTS,
        SUITE_REGISTRY,
        entries,
    )
    suite_sources = {
        suite_id: (path, suite_digest)
        for suite_id, path, suite_digest in manifest.suites
    }

    direct: dict[str, str] = {}
    for suite_id in sorted(by_id):
        path, suite_digest = suite_sources[suite_id]
        inputs = []
        for item in manifest.files:
            uses = tuple(
                use.as_projection() for use in item.uses if use.suite == suite_id
            )
            if uses:
                inputs.append(
                    {
                        "path": item.path,
                        "state": item.state,
                        "digest": item.digest,
                        "uses": uses,
                    }
                )
        repository_index = None
        if manifest.repository_index is not None:
            uses = tuple(
                use.as_projection()
                for use in manifest.repository_index.uses
                if use.suite == suite_id
            )
            if uses:
                repository_index = {
                    "digest": manifest.repository_index.digest,
                    "uses": uses,
                }
        direct[suite_id] = digest(
            {
                "registration": dict(sorted(by_id[suite_id].items())),
                "definition": {"path": path, "digest": suite_digest},
                "inputs": inputs,
                "repository_index": repository_index,
            }
        )

    requires: dict[str, tuple[str, ...]] = {}
    for suite_id, entry in by_id.items():
        values = entry.get("requires", [])
        if not isinstance(values, list) or any(
            not isinstance(value, str) or value not in by_id for value in values
        ):
            raise ValueError(f"suite {suite_id} has invalid requirements")
        requires[suite_id] = tuple(values)

    closure_cache: dict[str, tuple[str, ...]] = {}

    def closure(suite_id: str, path: tuple[str, ...] = ()) -> tuple[str, ...]:
        cached = closure_cache.get(suite_id)
        if cached is not None:
            return cached
        if suite_id in path:
            raise ValueError(f"suite requirement cycle includes {suite_id}")
        selected = {suite_id}
        for requirement in requires[suite_id]:
            selected.update(closure(requirement, (*path, suite_id)))
        result = tuple(sorted(selected))
        closure_cache[suite_id] = result
        return result

    fingerprints = {
        suite_id: digest(
            {
                "suite": suite_id,
                "closure": [
                    {"suite": dependency, "fingerprint": direct[dependency]}
                    for dependency in closure(suite_id)
                ],
            }
        )
        for suite_id in sorted(by_id)
    }
    return (
        fingerprints,
        {suite_id: closure(suite_id) for suite_id in sorted(by_id)},
        live_index_status,
    )


def load_snapshot() -> tuple[LocalSnapshot, dict[str, object]]:
    corpus = load_canonical_standards_corpus(REPO_ROOT)
    compiled = compile_policy_impact(REPO_ROOT, corpus)
    suite_fingerprints, suite_closures, live_index_status = (
        load_suite_dependencies()
    )

    module_fingerprints = {
        module.module_id: digest(
            {
                "module": module.module_id,
                "path": module.path,
                "content": file_digest(REPO_ROOT / module.path),
            }
        )
        for module in corpus.modules
    }
    artifact_fingerprints = {
        artifact.id: digest(
            {
                "catalog": artifact.coverage_fingerprint,
                "content": file_digest(REPO_ROOT / artifact.repository_path),
            }
        )
        for artifact in compiled.artifacts.values()
    }
    consumers = {**module_fingerprints, **artifact_fingerprints}

    units = {
        unit.id: digest(
            {
                "id": unit.id,
                "module": unit.module,
                "heading_path": list(unit.heading_path),
                "semantic_revision": unit.semantic_revision,
                "representation_digest": unit.representation_digest,
                "structural_digest": unit.structural_digest,
            }
        )
        for unit in corpus.policy_units
    }
    by_subject: dict[str, list[EdgeDependency]] = {
        subject: [] for subject in units
    }
    for edge_id, semantics in compiled.semantics.items():
        suite_id = semantics.evidence_owner.removeprefix("suite:")
        by_subject[semantics.source].append(
            EdgeDependency(
                edge_id,
                semantics.source,
                semantics.consumer,
                suite_id,
                semantics.dependency_fingerprint,
                consumers[semantics.consumer],
                suite_fingerprints[suite_id],
            )
        )
    edges = {
        subject: tuple(sorted(selected, key=lambda item: item.edge_id))
        for subject, selected in sorted(by_subject.items())
    }
    protocol_fingerprint = digest(
        {
            "algebra": ALGEBRA_VERSION,
            "policy_impact_authoring_contract": compiled.authoring_contract_digest,
            "relationship_kind_contract_version": (
                compiled.relationship_kind_contract_version
            ),
            "applicability_language_version": LANGUAGE_VERSION,
            "applicability_fact_schema": compiled.fact_schema.digest,
            "suite_input_contract": SUITE_INPUT_CONTRACT,
            "suite_input_schema_version": SUITE_INPUT_SCHEMA_VERSION,
        }
    )
    snapshot = LocalSnapshot(protocol_fingerprint, units, edges)

    horizon = load_captured_coverage_horizon(REPO_ROOT, corpus, compiled)
    current_global = {
        unit.id: digest(derive_coverage_view(unit, compiled, horizon).as_projection())
        for unit in corpus.policy_units
    }
    used_evidence_suites = {
        edge.evidence_suite for selected in edges.values() for edge in selected
    }
    local_evidence_closure = {
        dependency
        for suite_id in used_evidence_suites
        for dependency in suite_closures[suite_id]
    }
    selected_member = next(
        member
        for member in horizon.members
        if member.id.startswith("suite:")
        and member.id.removeprefix("suite:") not in local_evidence_closure
    )
    selected_suite = selected_member.id.removeprefix("suite:")
    local_dependents = sorted(
        {
            edge.source
            for selected in edges.values()
            for edge in selected
            if selected_suite in suite_closures[edge.evidence_suite]
        }
    )
    if local_dependents:
        raise AssertionError(
            "global counterexample member unexpectedly has local dependents"
        )
    changed_member = replace(
        selected_member,
        fingerprint=digest(
            {
                "previous": selected_member.fingerprint,
                "mutation": "one-horizon-member-changed",
            }
        ),
    )
    changed_members = tuple(
        changed_member if member.id == selected_member.id else member
        for member in horizon.members
    )
    changed_horizon = replace(
        horizon,
        members=changed_members,
        digest=digest(
            {
                "id": horizon.id,
                "provider": horizon.provider,
                "version": horizon.version,
                "members": [member.as_projection() for member in changed_members],
            }
        ),
    )
    changed_global = {
        unit.id: digest(
            derive_coverage_view(unit, compiled, changed_horizon).as_projection()
        )
        for unit in corpus.policy_units
    }
    global_invalidated = sorted(
        subject
        for subject in current_global
        if current_global[subject] != changed_global[subject]
    )
    if len(global_invalidated) != len(units):
        raise AssertionError(
            "one global horizon member change did not invalidate every subject"
        )
    metadata: dict[str, object] = {
        "policy_units": len(units),
        "relationships": len(compiled.semantics),
        "supplemental_consumers": len(compiled.artifacts),
        "suites": len(suite_fingerprints),
        "suite_closures": sum(len(value) for value in suite_closures.values()),
        "suite_input_repository_index": live_index_status,
        "changed_global_horizon_member": selected_member.id,
        "current_global_horizon_invalidates": len(global_invalidated),
        "dependency_local_invalidates_for_same_member": len(local_dependents),
    }
    return snapshot, metadata


def changed_subjects(before: LocalSnapshot, after: LocalSnapshot) -> list[str]:
    accepted = before.fingerprints()
    proposed = after.fingerprints()
    return sorted(
        subject
        for subject in set(accepted) | set(proposed)
        if accepted.get(subject) != proposed.get(subject)
    )


def replace_subject_edges(
    snapshot: LocalSnapshot,
    subject: str,
    edges: tuple[EdgeDependency, ...],
) -> LocalSnapshot:
    selected = dict(snapshot.edges)
    selected[subject] = tuple(sorted(edges, key=lambda item: item.edge_id))
    return LocalSnapshot(snapshot.protocol_fingerprint, snapshot.units, selected)


def run_cases(snapshot: LocalSnapshot) -> tuple[list[dict[str, object]], str]:
    source = max(snapshot.edges, key=lambda item: len(snapshot.edges[item]))
    selected_edge = snapshot.edges[source][0]
    all_subjects = sorted(snapshot.units)
    cases: list[tuple[str, list[str], list[str], dict[str, object]]] = []

    changed_edge = replace(
        selected_edge,
        relationship_fingerprint=digest(
            {
                "previous": selected_edge.relationship_fingerprint,
                "mutation": "changed-edge",
            }
        ),
    )
    changed_edges = tuple(
        changed_edge if edge.edge_id == selected_edge.edge_id else edge
        for edge in snapshot.edges[source]
    )
    observed = changed_subjects(
        snapshot,
        replace_subject_edges(snapshot, source, changed_edges),
    )
    cases.append(("changed-edge", [source], observed, {"edge": selected_edge.edge_id}))

    removed_edges = tuple(
        edge for edge in snapshot.edges[source] if edge.edge_id != selected_edge.edge_id
    )
    observed = changed_subjects(
        snapshot,
        replace_subject_edges(snapshot, source, removed_edges),
    )
    cases.append(
        ("removed-consumer", [source], observed, {"edge": selected_edge.edge_id})
    )

    provider_changed = LocalSnapshot(
        digest(
            {
                "previous": snapshot.protocol_fingerprint,
                "mutation": "provider-revision",
            }
        ),
        snapshot.units,
        snapshot.edges,
    )
    cases.append(
        (
            "provider-revision",
            all_subjects,
            changed_subjects(snapshot, provider_changed),
            {"scope": "all-subjects"},
        )
    )

    reviewed_edge_ids = {
        edge.edge_id for edges in snapshot.edges.values() for edge in edges
    }
    reviewed_edge_ids.remove(selected_edge.edge_id)
    proposed_edge_ids = {
        edge.edge_id for edges in snapshot.edges.values() for edge in edges
    }
    missing_dispositions = sorted(proposed_edge_ids - reviewed_edge_ids)
    blocked_sources = sorted(
        {
            edge.source
            for edges in snapshot.edges.values()
            for edge in edges
            if edge.edge_id in missing_dispositions
        }
    )
    observed = changed_subjects(snapshot, snapshot)
    cases.append(
        (
            "missing-edge-disposition",
            [],
            observed,
            {
                "missing_edges": missing_dispositions,
                "expected_blocked": [source],
                "observed_blocked": blocked_sources,
            },
        )
    )

    consumer = selected_edge.consumer
    consumer_sources = sorted(
        {
            edge.source
            for edges in snapshot.edges.values()
            for edge in edges
            if edge.consumer == consumer
        }
    )
    consumer_edges = {
        subject: tuple(
            replace(
                edge,
                consumer_fingerprint=digest(
                    {
                        "previous": edge.consumer_fingerprint,
                        "mutation": "consumer-content",
                    }
                ),
            )
            if edge.consumer == consumer
            else edge
            for edge in edges
        )
        for subject, edges in snapshot.edges.items()
    }
    consumer_changed = LocalSnapshot(
        snapshot.protocol_fingerprint,
        snapshot.units,
        consumer_edges,
    )
    cases.append(
        (
            "consumer-content",
            consumer_sources,
            changed_subjects(snapshot, consumer_changed),
            {"consumer": consumer},
        )
    )

    sources_by_consumer: dict[str, set[str]] = {}
    for selected in snapshot.edges.values():
        for edge in selected:
            sources_by_consumer.setdefault(edge.consumer, set()).add(edge.source)
    unrelated_consumer = next(
        consumer_id
        for consumer_id in sorted(sources_by_consumer)
        if source not in sources_by_consumer[consumer_id]
    )
    unrelated_sources = sorted(sources_by_consumer[unrelated_consumer])
    unrelated_edges = {
        subject: tuple(
            replace(
                edge,
                consumer_fingerprint=digest(
                    {
                        "previous": edge.consumer_fingerprint,
                        "mutation": "unrelated-consumer-content",
                    }
                ),
            )
            if edge.consumer == unrelated_consumer
            else edge
            for edge in edges
        )
        for subject, edges in snapshot.edges.items()
    }
    unrelated_changed = LocalSnapshot(
        snapshot.protocol_fingerprint,
        snapshot.units,
        unrelated_edges,
    )
    unrelated_observed = changed_subjects(snapshot, unrelated_changed)
    cases.append(
        (
            "unrelated-consumer-content",
            unrelated_sources,
            unrelated_observed,
            {
                "consumer": unrelated_consumer,
                "representative_source": source,
                "representative_source_stable": source not in unrelated_observed,
            },
        )
    )

    suite = selected_edge.evidence_suite
    suite_sources = sorted(
        {
            edge.source
            for edges in snapshot.edges.values()
            for edge in edges
            if edge.evidence_suite == suite
        }
    )
    evidence_edges = {
        subject: tuple(
            replace(
                edge,
                evidence_fingerprint=digest(
                    {
                        "previous": edge.evidence_fingerprint,
                        "mutation": "evidence-suite-closure",
                    }
                ),
            )
            if edge.evidence_suite == suite
            else edge
            for edge in edges
        )
        for subject, edges in snapshot.edges.items()
    }
    evidence_changed = LocalSnapshot(
        snapshot.protocol_fingerprint,
        snapshot.units,
        evidence_edges,
    )
    cases.append(
        (
            "evidence-suite-closure",
            suite_sources,
            changed_subjects(snapshot, evidence_changed),
            {"suite": suite},
        )
    )

    results = []
    failures = []
    for case_id, expected, observed, evidence in cases:
        passed = expected == observed
        if case_id == "missing-edge-disposition":
            passed = (
                passed
                and bool(evidence["missing_edges"])
                and evidence["expected_blocked"] == evidence["observed_blocked"]
            )
        if case_id == "unrelated-consumer-content":
            passed = passed and bool(evidence["representative_source_stable"])
        results.append(
            {
                "id": case_id,
                "passed": passed,
                "expected_invalidated": expected,
                "observed_invalidated": observed,
                "stable_subjects": len(snapshot.units) - len(observed),
                "evidence": evidence,
            }
        )
        if not passed:
            failures.append(case_id)
    if failures:
        raise AssertionError("prototype cases failed: " + ", ".join(failures))
    return results, source


def main() -> int:
    snapshot, metadata = load_snapshot()
    cases, representative_source = run_cases(snapshot)
    result = {
        "decision": "retain-standard-prototype-supports-separate-code-review",
        "repository": str(REPO_ROOT),
        "algebra_version": ALGEBRA_VERSION,
        "representative_source": representative_source,
        "current": metadata,
        "cases": cases,
        "boundary": {
            "proves_candidate": (
                "Changes to declared policy units, relationship membership and "
                "semantics, registered consumers, evidence-suite closures, and "
                "shared interpretation protocols invalidate exactly their "
                "dependent subjects."
            ),
            "does_not_prove": (
                "That an undeclared semantic consumer exists. Explicit consumer "
                "review and reviewed-empty authority remain mandatory."
            ),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
