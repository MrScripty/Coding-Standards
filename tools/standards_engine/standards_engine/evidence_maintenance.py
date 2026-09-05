"""Explicit maintenance of evidence registrations, without policy certification."""

from __future__ import annotations

import json
import tomllib
from collections.abc import Mapping

from .logical_authoring import _invalid, _toml_inline

REGISTRY = "evaluation/standards-effectiveness/suite-registry.toml"
CATALOG = "evaluation/standards-effectiveness/policy-impact-node-catalog.toml"
ATTESTATIONS = (
    "evaluation/standards-effectiveness/policy-coverage/attestation-sources.toml"
)
IMPACT = "evaluation/standards-effectiveness/policy-impact-registry.toml"


def _load(files: Mapping[str, bytes], path: str) -> dict:
    return tomllib.loads(files[path].decode("utf-8"))


def _dump(value: Mapping) -> bytes:
    """Use tables for top-level records and inline values within each record."""
    lines = []
    for key, item in value.items():
        if isinstance(item, list) and item and all(isinstance(x, dict) for x in item):
            for record in item:
                lines.extend(("", f"[[{key}]]"))
                lines.extend(f"{k} = {_toml_inline(v)}" for k, v in record.items())
        else:
            lines.append(f"{key} = {_toml_inline(item)}")
    return ("\n".join(lines) + "\n").encode()


def revise_evidence(
    files: Mapping[str, bytes], plan: Mapping, current_requirements: set[str]
) -> dict[str, bytes]:
    """Project an explicit maintenance plan; the Engine verifies before writing."""
    result = dict(files)
    registry = _load(files, REGISTRY)
    suites = {s["id"]: s for s in registry["suites"]}
    retired = set(plan["retire_suites"])
    missing = retired - suites.keys()
    if missing:
        raise _invalid("EVIDENCE.UNKNOWN_SUITE", f"Unknown suites: {sorted(missing)}")
    changes = {}
    for item in plan["retire_checks"]:
        sid, cid = item["suite"], item["check"]
        if sid not in suites or sid in retired:
            raise _invalid(
                "EVIDENCE.UNKNOWN_SUITE",
                f"Check retirement has no retained suite: {sid}",
            )
        suite = changes.setdefault(sid, _load(files, suites[sid]["path"]))
        found = [c for c in suite["checks"] if c["id"] == cid]
        if len(found) != 1:
            raise _invalid(
                "EVIDENCE.UNKNOWN_CHECK",
                f"Unknown or repeated check retirement: {sid}/{cid}",
            )
        suite["checks"].remove(found[0])
    for sid, suite in changes.items():
        if not suite["checks"]:
            retired.add(sid)
    for item in plan["suite_descriptions"]:
        sid = item["suite"]
        if sid not in suites or sid in retired:
            raise _invalid(
                "EVIDENCE.UNKNOWN_SUITE", f"Description has no retained suite: {sid}"
            )
        changes.setdefault(sid, _load(files, suites[sid]["path"]))["description"] = (
            item["description"]
        )
    for sid, suite in changes.items():
        if sid not in retired:
            result[suites[sid]["path"]] = _dump(suite)

    def retained_dependencies(sid: str, seen: frozenset[str] = frozenset()) -> set[str]:
        if sid in seen:
            raise _invalid("EVIDENCE.SUITE_CYCLE", "Suite dependencies contain a cycle")
        if sid not in retired:
            return {sid}
        return set().union(
            *(
                retained_dependencies(dep, seen | {sid})
                for dep in suites[sid]["requires"]
            )
        )

    for sid in retired:
        result.pop(suites[sid]["path"])
    registry["suites"] = [
        dict(
            s,
            requires=sorted(
                set().union(*(retained_dependencies(d) for d in s["requires"]))
            ),
        )
        for s in registry["suites"]
        if s["id"] not in retired
    ]
    if registry != _load(files, REGISTRY):
        result[REGISTRY] = _dump(registry)
    retained = {s["id"] for s in registry["suites"]}
    replacement = plan["replacement_evidence_owner"]
    if not replacement.startswith("suite:") or replacement[6:] not in retained:
        raise _invalid(
            "EVIDENCE.INVALID_OWNER",
            "Replacement evidence owner must be a retained suite",
        )

    retired_inputs = set(plan["retire_inputs"])
    for path in retired_inputs:
        if (
            not path.startswith("evaluation/standards-effectiveness/fixtures/")
            or path not in files
            or ".." in path.split("/")
        ):
            raise _invalid(
                "EVIDENCE.INVALID_RETIREMENT",
                "Only existing evidence fixture inputs may be retired",
            )
        for s in registry["suites"]:
            if path in result[s["path"]].decode():
                raise _invalid(
                    "EVIDENCE.INPUT_IN_USE",
                    f"Retained suite {s['id']} still uses {path}",
                )
        result.pop(path)
    catalog = _load(files, CATALOG)
    removed_nodes = {
        n["id"]
        for n in catalog["nodes"]
        if n["id"] in retired or n["metadata"]["repository_path"] in retired_inputs
    }
    catalog["nodes"] = [n for n in catalog["nodes"] if n["id"] not in removed_nodes]
    nodes = {n["id"] for n in catalog["nodes"]}
    impact_registry = _load(files, IMPACT)
    declarations = {p: _load(files, p) for p in impact_registry["declaration_sources"]}
    for doc in declarations.values():
        doc["relationships"] = [
            r for r in doc["relationships"] if r["consumer"] not in removed_nodes
        ]
        for r in doc["relationships"]:
            if r["evidence_owner"].removeprefix("suite:") in retired:
                r["evidence_owner"] = replacement
                r["rationale"] = plan["replacement_evidence_rationale"]
    # Caller names exact relationships; no lexical discovery of policy meaning.
    for edit in plan["relationship_updates"]:
        matches = [
            r
            for doc in declarations.values()
            for r in doc["relationships"]
            if (r["source"], r["consumer"], r["relation"])
            == (edit["source_policy"], edit["consumer"], edit["relation"])
        ]
        if len(matches) != 1:
            raise _invalid(
                "EVIDENCE.UNKNOWN_RELATIONSHIP",
                "Evidence relationship must resolve exactly once",
            )
        matches[0]["evidence_owner"] = edit["evidence_owner"]
        matches[0]["rationale"] = edit["rationale"]
    for edit in plan["consumer_registrations"]:
        path = edit["path"]
        if path not in files or path in retired_inputs:
            raise _invalid(
                "EVIDENCE.CONSUMER_UNAVAILABLE",
                f"Consumer must be present in the selected repository: {path}",
            )
        if path in nodes:
            raise _invalid(
                "EVIDENCE.CONSUMER_EXISTS", f"Consumer is already registered: {path}"
            )
        catalog["nodes"].append(
            {
                "id": path,
                "metadata": {
                    "repository_path": path,
                    "artifact_kind": edit["artifact_kind"],
                    "authority": "evidence",
                },
            }
        )
        nodes.add(path)
        for policy in edit["source_policies"]:
            candidates = [
                doc
                for doc in declarations.values()
                if any(r["source"] == policy for r in doc["relationships"])
            ]
            if len(candidates) != 1:
                raise _invalid(
                    "EVIDENCE.UNKNOWN_POLICY",
                    "Consumer registration requires one existing policy declaration owner",
                )
            candidates[0]["relationships"].append(
                {
                    "source": policy,
                    "consumer": path,
                    "relation": edit["relation"],
                    "applicability": {"operator": "always"},
                    "evidence_owner": edit["evidence_owner"],
                    "rationale": edit["rationale"],
                }
            )
    if catalog != _load(files, CATALOG):
        result[CATALOG] = _dump(catalog)
    for path, doc in declarations.items():
        if doc != _load(files, path):
            result[path] = _dump(doc)

    # Keep the unrelated evidence-owner precondition valid in retained graph
    # compiler fixtures. Intentional malformed owners/consumers remain unchanged.
    fixture_prefix = (
        "evaluation/standards-effectiveness/fixtures/policy-impact/declarations/"
    )
    for path in files:
        if (
            not path.startswith(fixture_prefix)
            or not path.endswith(".toml")
            or path not in result
        ):
            continue
        doc = _load(result, path)
        before = _dump(doc)
        for relationship in doc.get("relationships", []):
            if relationship.get("evidence_owner", "").removeprefix("suite:") in retired:
                relationship["evidence_owner"] = replacement
        if _dump(doc) != before:
            result[path] = _dump(doc)

    if plan["prune_stale_certificates"]:
        registry = _load(files, ATTESTATIONS)
        kept = []
        for path in registry["sources"]:
            doc = _load(files, path)
            claims = [
                c
                for c in doc["attestations"]
                if c["requirement_id"] in current_requirements
            ]
            if claims:
                kept.append(path)
                if claims != doc["attestations"]:
                    doc["attestations"] = claims
                    result[path] = _dump(doc)
            else:
                result.pop(path)
        registry["sources"] = kept
        kept = []
        for path in registry.get("engine_sources", []):
            receipt = json.loads(files[path])
            if receipt["claim"]["requirement_id"] in current_requirements:
                kept.append(path)
            else:
                result.pop(path)
        if "engine_sources" in registry:
            registry["engine_sources"] = kept
        if registry != _load(files, ATTESTATIONS):
            result[ATTESTATIONS] = _dump(registry)
    return result
