#!/usr/bin/env python3
"""Generate and validate the standards-change planning visualization."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import sys
import tomllib


REPORTS = Path(__file__).resolve().parent
OUTPUT = REPORTS / "standards-graph-change-visualization.html"
PLANNED_UNITS = REPORTS / "planned-policy-units.tsv"
DISPOSITIONS = REPORTS / "policy-impact-dispositions.tsv"
CURRENT_INVENTORY = REPORTS / "current-policy-consumer-inventory.tsv"
PLANNED_NODES = REPORTS / "planned-node-catalog-additions.tsv"

UNIT_HEADERS = [
    "change_id",
    "action",
    "policy_unit",
    "module",
    "heading",
    "current_revision",
    "planned_revision",
    "family",
    "rationale",
]
EDGE_HEADERS = [
    "change_id",
    "family",
    "source",
    "consumer",
    "relation",
    "disposition",
    "consumer_change",
    "rationale",
]
INVENTORY_HEADERS = [
    "policy_unit",
    "current_revision",
    "current_edge_count",
    "planned_action",
    "declaration_source",
    "disposition_state",
    "note",
]
NODE_HEADERS = [
    "node_id",
    "artifact_kind",
    "repository_path",
    "lifecycle",
    "family",
    "rationale",
]
ACTIONS = {"add", "revise", "conditional-revise", "retain"}
DISPOSITION_VALUES = {
    "add",
    "conditional-add",
    "update",
    "conditional-update",
    "reviewed-no-change",
    "remove",
}


def repository_root() -> Path:
    for candidate in [REPORTS, *REPORTS.parents]:
        if (candidate / "evaluation/standards-effectiveness/policy-impact-registry.toml").is_file():
            return candidate
    raise ValueError("cannot locate repository root")


def load_tsv(path: Path, headers: list[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != headers:
            raise ValueError(f"{path}: expected headers {headers}, got {reader.fieldnames}")
        rows = list(reader)
    for line_number, row in enumerate(rows, start=2):
        missing = [name for name in headers if not row[name].strip()]
        if missing:
            raise ValueError(f"{path}:{line_number}: empty fields {missing}")
    return rows


def load_current(
    root: Path,
) -> tuple[
    list[dict[str, object]],
    list[dict[str, str]],
    set[str],
    dict[str, dict[str, str]],
]:
    unit_registry_path = root / "evaluation/standards-effectiveness/policy-units/registry.toml"
    unit_registry = tomllib.loads(unit_registry_path.read_text(encoding="utf-8"))
    units: list[dict[str, object]] = []
    for source in unit_registry["sources"]:
        document = tomllib.loads((root / source).read_text(encoding="utf-8"))
        for unit in document["policy_unit"]:
            units.append(
                {
                    "id": unit["id"],
                    "module": unit["module"],
                    "heading": " / ".join(unit["heading_path"]),
                    "revision": unit["semantic_revision"],
                }
            )

    impact_registry_path = root / "evaluation/standards-effectiveness/policy-impact-registry.toml"
    impact_registry = tomllib.loads(impact_registry_path.read_text(encoding="utf-8"))
    edges: list[dict[str, str]] = []
    for source in impact_registry["declaration_sources"]:
        document = tomllib.loads((root / source).read_text(encoding="utf-8"))
        for relationship in document.get("relationships", []):
            edges.append(
                {
                    "source": relationship["source"],
                    "consumer": relationship["consumer"],
                    "relation": relationship["relation"],
                    "rationale": relationship["rationale"],
                    "declaration": source,
                }
            )
    corpus_path = root / "evaluation/standards-effectiveness/canonical-module-corpus.toml"
    corpus = tomllib.loads(corpus_path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for member in corpus["members"]:
        for line in (root / member).read_text(encoding="utf-8").splitlines():
            if line.startswith("- ID: `"):
                modules.add(line.split("`")[1])
                break

    catalog_path = root / "evaluation/standards-effectiveness/policy-impact-node-catalog.toml"
    catalog = tomllib.loads(catalog_path.read_text(encoding="utf-8"))
    catalog_nodes: dict[str, dict[str, str]] = {}
    for node in catalog["nodes"]:
        metadata = dict(node["metadata"])
        catalog_nodes[node["id"]] = metadata
        for alias in node.get("aliases", []):
            catalog_nodes[alias] = metadata

    return (
        sorted(units, key=lambda row: str(row["id"])),
        sorted(edges, key=lambda row: (row["source"], row["consumer"], row["relation"])),
        modules,
        catalog_nodes,
    )


def edge_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["source"], row["consumer"], row["relation"]


def is_standards_impact(row: dict[str, str], canonical_modules: set[str]) -> bool:
    """Return whether a relationship routes one standard to another standard."""
    return row["consumer"] in canonical_modules


def validate(
    current_units: list[dict[str, object]],
    current_edges: list[dict[str, str]],
    planned_units: list[dict[str, str]],
    dispositions: list[dict[str, str]],
    inventory: list[dict[str, str]],
    planned_nodes: list[dict[str, str]],
    root: Path,
    canonical_modules: set[str],
    current_catalog_nodes: dict[str, dict[str, str]],
    state: str,
) -> list[str]:
    notes: list[str] = []
    current_unit_map = {str(row["id"]): row for row in current_units}
    current_edge_map = {edge_key(row): row for row in current_edges}
    current_impact_edges = [
        row for row in current_edges if is_standards_impact(row, canonical_modules)
    ]
    if len(current_edge_map) != len(current_edges):
        raise ValueError("current policy graph contains duplicate edge keys")

    unit_ids: set[str] = set()
    change_ids: set[str] = set()
    phase_by_change: dict[str, str] = {}
    for row in planned_units:
        action = row["action"]
        if action not in ACTIONS:
            raise ValueError(f"{row['policy_unit']}: unknown action {action}")
        if row["policy_unit"] in unit_ids:
            raise ValueError(f"duplicate planned unit {row['policy_unit']}")
        unit_ids.add(row["policy_unit"])
        change_ids.add(row["change_id"])
        current = current_unit_map.get(row["policy_unit"])
        if current is not None and (
            current["module"] != row["module"] or current["heading"] != row["heading"]
        ):
            raise ValueError(
                f"{row['policy_unit']}: live module/heading disagrees with the planning manifest"
            )
        if state == "planning":
            if action == "add" and current is not None:
                raise ValueError(f"{row['policy_unit']}: add already exists")
            if action != "add" and current is None:
                raise ValueError(f"{row['policy_unit']}: revision has no current unit")
            if action != "add" and str(current["revision"]) != row["current_revision"]:
                raise ValueError(
                    f"{row['policy_unit']}: current revision is {current['revision']}, "
                    f"plan says {row['current_revision']}"
                )
            phase_by_change[row["change_id"]] = "pre"
        elif state == "accepted":
            if action == "conditional-revise":
                raise ValueError(
                    f"{row['policy_unit']}: accepted state cannot retain a conditional action"
                )
            if current is None:
                raise ValueError(f"{row['policy_unit']}: accepted unit is missing")
            if str(current["revision"]) != row["planned_revision"]:
                raise ValueError(
                    f"{row['policy_unit']}: accepted revision is {current['revision']}, "
                    f"plan says {row['planned_revision']}"
                )
            phase_by_change[row["change_id"]] = "post"
        else:
            if action == "conditional-revise":
                if current is None or str(current["revision"]) != row["current_revision"]:
                    raise ValueError(
                        f"{row['policy_unit']}: unresolved conditional must remain at its current revision"
                    )
                phase_by_change[row["change_id"]] = "pre"
            elif action == "retain":
                if current is None or str(current["revision"]) != row["current_revision"]:
                    raise ValueError(
                        f"{row['policy_unit']}: retained unit does not match its current revision"
                    )
                phase_by_change[row["change_id"]] = "post"
            elif action == "add":
                if current is None:
                    phase_by_change[row["change_id"]] = "pre"
                elif str(current["revision"]) == row["planned_revision"]:
                    phase_by_change[row["change_id"]] = "post"
                else:
                    raise ValueError(f"{row['policy_unit']}: transition add has an unexpected revision")
            else:
                if current is None:
                    raise ValueError(f"{row['policy_unit']}: transition revision has no current unit")
                if str(current["revision"]) == row["current_revision"]:
                    phase_by_change[row["change_id"]] = "pre"
                elif str(current["revision"]) == row["planned_revision"]:
                    phase_by_change[row["change_id"]] = "post"
                else:
                    raise ValueError(f"{row['policy_unit']}: transition has an unexpected revision")
        if action in {"revise", "conditional-revise"}:
            if int(row["planned_revision"]) != int(row["current_revision"]) + 1:
                raise ValueError(f"{row['policy_unit']}: planned revision must increment once")
        if action == "retain" and row["planned_revision"] != row["current_revision"]:
            raise ValueError(f"{row['policy_unit']}: retained revision must not change")

    disposition_keys: set[tuple[str, str, str]] = set()
    dispositions_by_source: Counter[str] = Counter()
    for row in dispositions:
        if row["disposition"] not in DISPOSITION_VALUES:
            raise ValueError(f"{edge_key(row)}: unknown disposition {row['disposition']}")
        key = edge_key(row)
        if key in disposition_keys:
            raise ValueError(f"duplicate planned edge disposition {key}")
        disposition_keys.add(key)
        dispositions_by_source[row["source"]] += 1
        if row["change_id"] not in change_ids:
            raise ValueError(f"{key}: unknown change id {row['change_id']}")
        unit = next(item for item in planned_units if item["change_id"] == row["change_id"])
        if unit["policy_unit"] != row["source"]:
            raise ValueError(f"{key}: change id belongs to {unit['policy_unit']}")
        if unit["family"] != row["family"]:
            raise ValueError(f"{key}: family disagrees with planned unit")
        exists = key in current_edge_map
        is_add = row["disposition"] in {"add", "conditional-add"}
        if state == "planning":
            if is_add == exists:
                edge_state = "already exists" if exists else "does not exist"
                raise ValueError(f"{key}: {row['disposition']} but edge {edge_state}")
        elif state == "accepted":
            if row["disposition"].startswith("conditional-"):
                raise ValueError(f"{key}: accepted state cannot retain a conditional disposition")
            should_exist = row["disposition"] != "remove"
            if exists != should_exist:
                edge_state = "exists" if exists else "is missing"
                raise ValueError(
                    f"{key}: accepted disposition is {row['disposition']} but edge {edge_state}"
                )
        else:
            phase = phase_by_change[row["change_id"]]
            if row["disposition"].startswith("conditional-") and phase != "pre":
                raise ValueError(f"{key}: applied transition cannot retain a conditional disposition")
            if row["disposition"] in {"add", "conditional-add"}:
                should_exist = phase == "post"
            elif row["disposition"] == "remove":
                should_exist = phase == "pre"
            else:
                should_exist = True
            if exists != should_exist:
                edge_state = "exists" if exists else "is missing"
                raise ValueError(
                    f"{key}: transition source is {phase} but edge {edge_state}"
                )
        conditional = row["disposition"].startswith("conditional-")
        if conditional != (row["consumer_change"] == "conditional"):
            raise ValueError(f"{key}: conditional disposition/change mismatch")

    for unit in planned_units:
        if dispositions_by_source[unit["policy_unit"]] == 0:
            raise ValueError(f"{unit['policy_unit']}: no planned relationship disposition")

    planned_node_ids: set[str] = set()
    planned_paths: set[str] = set()
    for row in planned_nodes:
        node_phases = {
            phase_by_change[edge["change_id"]]
            for edge in dispositions
            if edge["consumer"] == row["node_id"]
            and edge["disposition"] in {"add", "conditional-add"}
        }
        if len(node_phases) != 1:
            raise ValueError(
                f"{row['node_id']}: catalog consumers span incompatible phases {sorted(node_phases)}"
            )
        node_phase = next(iter(node_phases))
        node_exists = row["node_id"] in current_catalog_nodes
        if node_exists != (node_phase == "post"):
            catalog_state = "registered" if node_exists else "missing"
            raise ValueError(
                f"{row['node_id']}: source phase is {node_phase} but catalog node is {catalog_state}"
            )
        if node_exists:
            metadata = current_catalog_nodes[row["node_id"]]
            if metadata.get("repository_path") != row["repository_path"]:
                raise ValueError(f"{row['node_id']}: catalog repository path disagrees with plan")
            if metadata.get("artifact_kind") != row["artifact_kind"]:
                raise ValueError(f"{row['node_id']}: catalog artifact kind disagrees with plan")
        if row["node_id"] in planned_node_ids:
            raise ValueError(f"duplicate planned node {row['node_id']}")
        if row["repository_path"] in planned_paths:
            raise ValueError(f"duplicate planned node path {row['repository_path']}")
        planned_node_ids.add(row["node_id"])
        planned_paths.add(row["repository_path"])
        if row["lifecycle"] not in {"existing-register", "planned-create"}:
            raise ValueError(f"{row['node_id']}: unknown lifecycle {row['lifecycle']}")
        exists = (root / row["repository_path"]).is_file()
        if row["lifecycle"] == "existing-register" and not exists:
            raise ValueError(f"{row['node_id']}: existing artifact path is missing")
        if node_phase == "post" and not exists:
            raise ValueError(f"{row['node_id']}: accepted artifact path is missing")
        if row["family"] not in {unit["family"] for unit in planned_units}:
            raise ValueError(f"{row['node_id']}: unknown family {row['family']}")

    known_consumers = canonical_modules | set(current_catalog_nodes) | planned_node_ids
    unknown_consumers = {
        row["consumer"]
        for row in dispositions
        if row["disposition"] in {"add", "conditional-add"}
        and row["consumer"] not in known_consumers
    }
    if unknown_consumers:
        raise ValueError(f"planned relationships have uncataloged consumers: {sorted(unknown_consumers)}")
    unused_planned_nodes = planned_node_ids - {row["consumer"] for row in dispositions}
    if unused_planned_nodes:
        raise ValueError(f"planned catalog nodes have no relationship: {sorted(unused_planned_nodes)}")

    revised = {
        row["policy_unit"]
        for row in planned_units
        if row["action"] in {"revise", "conditional-revise", "retain"}
    }
    impact_sources = revised if state == "planning" else {row["policy_unit"] for row in planned_units}
    if state == "planning":
        expected_revised_edges = {
            edge_key(row) for row in current_impact_edges if row["source"] in impact_sources
        }
        disposed_revised_edges = {
            edge_key(row)
            for row in dispositions
            if row["disposition"] not in {"add", "conditional-add"}
            and is_standards_impact(row, canonical_modules)
        }
    elif state == "accepted":
        expected_revised_edges = {
            edge_key(row) for row in current_impact_edges if row["source"] in impact_sources
        }
        disposed_revised_edges = {
            edge_key(row)
            for row in dispositions
            if row["source"] in impact_sources
            and is_standards_impact(row, canonical_modules)
        }
    else:
        expected_revised_edges = {
            edge_key(row) for row in current_impact_edges if row["source"] in impact_sources
        }
        disposed_revised_edges = {
            edge_key(row)
            for row in dispositions
            if row["source"] in impact_sources
            and edge_key(row) in current_edge_map
            and is_standards_impact(row, canonical_modules)
        }
    missing = expected_revised_edges - disposed_revised_edges
    extra = disposed_revised_edges - expected_revised_edges
    if missing or extra:
        raise ValueError(
            "revised-owner disposition mismatch: "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )

    inventory_rows = {row["policy_unit"]: row for row in inventory if row["policy_unit"] != "TOTAL"}
    if set(inventory_rows) != revised:
        raise ValueError("current inventory owners do not match revised planned owners")
    baseline_edges = [
        row
        for row in reconstruct_baseline_edges(current_edges, dispositions, state)
        if is_standards_impact(row, canonical_modules)
    ]
    current_counts = Counter(row["source"] for row in baseline_edges)
    for policy_unit, row in inventory_rows.items():
        if int(row["current_edge_count"]) != current_counts[policy_unit]:
            raise ValueError(f"{policy_unit}: current edge count changed")
    total_rows = [row for row in inventory if row["policy_unit"] == "TOTAL"]
    baseline_revised_edges = {edge_key(row) for row in baseline_edges if row["source"] in revised}
    if len(total_rows) != 1 or int(total_rows[0]["current_edge_count"]) != len(baseline_revised_edges):
        raise ValueError("inventory TOTAL does not match revised-owner current edges")

    impact_dispositions = [
        row for row in dispositions if is_standards_impact(row, canonical_modules)
    ]
    counts = Counter(row["disposition"] for row in impact_dispositions)
    baseline_units = reconstruct_baseline_units(current_units, planned_units, state)
    notes.append(f"{len(baseline_units)} baseline policy units")
    notes.append(f"{len(baseline_edges)} baseline relationships")
    notes.append(f"{len(planned_units)} planned policy-unit dispositions")
    notes.append(f"{len(baseline_revised_edges)} existing relationships dispositioned")
    notes.append(
        f"{counts['add'] + counts['conditional-add']} planned standards-impact relationships"
    )
    notes.append(f"{len(planned_nodes)} planned catalog-node additions")
    return notes


def reconstruct_baseline_units(
    current_units: list[dict[str, object]],
    planned_units: list[dict[str, str]],
    state: str,
) -> list[dict[str, object]]:
    if state == "planning":
        return current_units
    additions = {row["policy_unit"] for row in planned_units if row["action"] == "add"}
    revisions = {
        row["policy_unit"]: int(row["current_revision"])
        for row in planned_units
        if row["action"] == "revise"
    }
    baseline: list[dict[str, object]] = []
    for unit in current_units:
        if unit["id"] in additions:
            continue
        restored = dict(unit)
        if unit["id"] in revisions:
            restored["revision"] = revisions[str(unit["id"])]
        baseline.append(restored)
    return baseline


def reconstruct_baseline_edges(
    current_edges: list[dict[str, str]],
    dispositions: list[dict[str, str]],
    state: str,
) -> list[dict[str, str]]:
    if state == "planning":
        return current_edges
    added = {
        edge_key(row)
        for row in dispositions
        if row["disposition"] in {"add", "conditional-add"}
    }
    baseline = [row for row in current_edges if edge_key(row) not in added]
    for row in dispositions:
        if row["disposition"] == "remove":
            baseline.append(
                {
                    "source": row["source"],
                    "consumer": row["consumer"],
                    "relation": row["relation"],
                    "rationale": row["rationale"],
                    "declaration": "reconstructed-from-reviewed-delta",
                }
            )
    return sorted(baseline, key=lambda row: (row["source"], row["consumer"], row["relation"]))


def render(
    current_units: list[dict[str, object]],
    current_edges: list[dict[str, str]],
    planned_units: list[dict[str, str]],
    dispositions: list[dict[str, str]],
    planned_nodes: list[dict[str, str]],
    notes: list[str],
    state: str,
) -> str:
    disposition_counts = Counter(row["disposition"] for row in dispositions)
    added_units = sum(row["action"] == "add" for row in planned_units)
    proposed_edge_count = (
        len(current_edges)
        + disposition_counts["add"]
        + disposition_counts["conditional-add"]
        - disposition_counts["remove"]
    )
    payload = {
        "baselineCommit": "351e7852",
        "renderState": state,
        "currentUnits": current_units,
        "currentEdges": current_edges,
        "plannedUnits": planned_units,
        "dispositions": dispositions,
        "plannedNodes": planned_nodes,
        "notes": notes,
        "summary": {
            "currentUnitCount": len(current_units),
            "proposedUnitCount": len(current_units) + added_units,
            "currentEdgeCount": len(current_edges),
            "proposedEdgeCount": proposed_edge_count,
            "addedUnits": added_units,
            "revisedUnits": sum(row["action"] == "revise" for row in planned_units),
            "conditionalUnits": sum(row["action"] == "conditional-revise" for row in planned_units),
            "retainedUnits": sum(row["action"] == "retain" for row in planned_units),
            "addEdges": disposition_counts["add"],
            "updateEdges": disposition_counts["update"],
            "reviewedEdges": disposition_counts["reviewed-no-change"],
            "conditionalEdges": disposition_counts["conditional-update"]
            + disposition_counts["conditional-add"],
            "catalogNodeAdditions": len(planned_nodes),
        },
    }
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Standards Graph Change Plan</title>
<style>
:root {{ color-scheme: dark; --ink:#ecf2ef; --muted:#9baca6; --panel:#13231f; --panel2:#172b26; --line:#29443b; --mint:#65d6a6; --gold:#f4bd63; --blue:#74b9ff; --violet:#bd9cff; --rose:#ff7f91; --gray:#71817b; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:radial-gradient(circle at 15% -10%,#24483b 0,transparent 34rem),#091310; color:var(--ink); font:14px/1.45 Inter,ui-sans-serif,system-ui,-apple-system,sans-serif; }}
main {{ width:min(1500px,calc(100% - 32px)); margin:0 auto; padding:38px 0 64px; }}
h1 {{ max-width:900px; margin:0; font-size:clamp(30px,5vw,62px); line-height:.98; letter-spacing:-.045em; }}
h2 {{ margin:0 0 14px; font-size:20px; }}
p {{ color:var(--muted); }}
.eyebrow {{ color:var(--mint); font-size:12px; font-weight:800; letter-spacing:.15em; text-transform:uppercase; margin-bottom:12px; }}
.lede {{ max-width:860px; font-size:17px; }}
.cards {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin:28px 0; }}
.card,.panel {{ background:linear-gradient(145deg,rgba(23,43,38,.96),rgba(13,27,23,.96)); border:1px solid var(--line); border-radius:16px; box-shadow:0 15px 45px rgba(0,0,0,.18); }}
.card {{ padding:18px; }} .card b {{ display:block; font-size:28px; letter-spacing:-.04em; }} .card span {{ color:var(--muted); }}
.delta {{ color:var(--mint); font-size:12px; font-weight:700; margin-left:6px; }}
.panel {{ margin-top:16px; padding:20px; }}
.toolbar {{ display:grid; grid-template-columns:repeat(5,minmax(140px,1fr)); gap:10px; margin-bottom:14px; }}
label {{ color:var(--muted); font-size:12px; }} select,input {{ width:100%; margin-top:5px; border:1px solid var(--line); border-radius:9px; background:#0b1713; color:var(--ink); padding:9px 10px; }}
.check {{ display:flex; align-items:end; padding-bottom:9px; gap:8px; }} .check input {{ width:auto; margin:0; }}
.legend {{ display:flex; flex-wrap:wrap; gap:12px; color:var(--muted); margin:7px 0 15px; }} .dot {{ display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:5px; }}
.graph-wrap {{ overflow:auto; max-height:760px; border:1px solid var(--line); border-radius:12px; background:#0a1512; }}
svg {{ display:block; min-width:100%; }}
.edge {{ fill:none; stroke-width:1.5; opacity:.62; }} .edge:hover {{ opacity:1; stroke-width:3; }}
.node rect {{ fill:#142a23; stroke:#36584d; rx:7; }} .node text {{ fill:var(--ink); font-size:11px; }} .source rect {{ fill:#203d33; stroke:#65d6a6; }}
.graph-empty {{ padding:48px; color:var(--muted); text-align:center; }}
.unit-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }}
.unit {{ border:1px solid var(--line); border-radius:11px; padding:13px; background:#0d1c18; }} .unit code {{ color:var(--mint); overflow-wrap:anywhere; }} .unit p {{ margin:7px 0 0; font-size:12px; }}
.tag {{ display:inline-block; border:1px solid var(--line); border-radius:999px; padding:2px 7px; margin:0 5px 5px 0; font-size:11px; color:var(--muted); }}
.warning {{ border-left:3px solid var(--gold); padding:10px 13px; background:rgba(244,189,99,.08); color:#efd7ae; margin:12px 0; }}
.ok {{ border-left-color:var(--mint); background:rgba(101,214,166,.08); color:#bdebd7; }}
.table-wrap {{ overflow:auto; max-height:660px; border:1px solid var(--line); border-radius:12px; }}
table {{ width:100%; border-collapse:collapse; font-size:12px; }} th {{ position:sticky; top:0; background:#173027; text-align:left; color:#cfe2da; }} th,td {{ padding:9px 10px; border-bottom:1px solid #20372f; vertical-align:top; }} td code {{ color:#b9e5d3; overflow-wrap:anywhere; }}
.pill {{ white-space:nowrap; border-radius:999px; padding:3px 7px; font-weight:700; font-size:10px; }}
.footer {{ margin-top:18px; color:var(--muted); font-size:12px; }}
@media(max-width:900px) {{ .cards,.unit-grid {{ grid-template-columns:1fr 1fr; }} .toolbar {{ grid-template-columns:1fr 1fr; }} }}
@media(max-width:560px) {{ main {{ width:min(100% - 20px,1500px); }} .cards,.unit-grid,.toolbar {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body>
<main>
  <div class="eyebrow"><span id="render-state"></span> · baseline <span id="baseline"></span></div>
  <h1>Where the standards graph changes—and where it deliberately does not.</h1>
  <p class="lede">A before/after view of standards pointing to other standards that may need inspection when their meaning changes. Application code is not an impact-graph consumer. Catalog nodes shown separately are repository conformance evidence, not graph edges or enforcement imposed on adopters.</p>
  <section class="cards" id="cards"></section>
  <section class="panel">
    <h2>Policy-unit change</h2>
    <div class="unit-grid" id="units"></div>
    <h2 style="margin-top:22px">Catalog-node additions</h2>
    <div id="nodes"></div>
  </section>
  <section class="panel">
    <h2>Relationship map</h2>
    <div class="toolbar">
      <label>Family<select id="family"></select></label>
      <label>Source<select id="source"></select></label>
      <label>Disposition<select id="disposition"></select></label>
      <label>Relation<select id="relation"></select></label>
      <label>Search<input id="search" type="search" placeholder="owner, consumer, rationale"></label>
    </div>
    <label class="check"><input id="unchanged" type="checkbox"> Include all unchanged current-graph relationships</label>
    <div class="legend" id="legend"></div>
    <div id="status"></div>
    <div class="graph-wrap" id="graph"></div>
  </section>
  <section class="panel">
    <h2>Filtered relationship dispositions</h2>
    <div class="table-wrap"><table><thead><tr><th>Family</th><th>Owner</th><th>Consumer</th><th>Relation</th><th>Disposition</th><th>Reason</th></tr></thead><tbody id="rows"></tbody></table></div>
  </section>
  <p class="footer">“Reviewed—no change” means the target standard was inspected and needs no text edit; the relationship remains so a future source change routes an agent back to it. Fixtures, suites, prompts, templates, generated artifacts, and application implementations are excluded from the relationship map. Re-run the generator after accepted graph changes; use <code>--check</code> to detect stale HTML.</p>
</main>
<script>
const DATA={data_json};
const colors={{"add":"#65d6a6","update":"#74b9ff","reviewed-no-change":"#71817b","conditional-update":"#f4bd63","conditional-add":"#f4bd63","remove":"#ff7f91","unchanged":"#3c5049"}};
const labels={{"add":"Add","update":"Update","reviewed-no-change":"Reviewed—no change","conditional-update":"Conditional update","conditional-add":"Conditional add","remove":"Remove","unchanged":"Unchanged current"}};
const $=id=>document.getElementById(id);
const esc=value=>String(value).replace(/[&<>\"']/g,ch=>({{"&":"&amp;","<":"&lt;",">":"&gt;",'\"':"&quot;","'":"&#39;"}}[ch]));
$('baseline').textContent=DATA.baselineCommit;
$('render-state').textContent=DATA.renderState==='accepted'?'Accepted change record':(DATA.renderState==='transition'?'Transition change record':'Planning evidence');
const s=DATA.summary;
$('cards').innerHTML=[
  [`${{s.currentUnitCount}} → ${{s.proposedUnitCount}}`,`policy units`,`+${{s.addedUnits}} new · ${{s.revisedUnits}} revised · ${{s.conditionalUnits}} conditional · ${{s.retainedUnits}} retained`],
  [`${{s.currentEdgeCount}} → ${{s.proposedEdgeCount}}`,`standards-impact relationships`,`+${{s.addEdges}} edges · +${{s.catalogNodeAdditions}} separate evidence nodes`],
  [s.updateEdges,`standards updates`,`affected standards revised`],
  [s.reviewedEdges,`reviewed, unchanged`,`affected standards requiring no text edit`]
].map(([n,l,d])=>`<div class="card"><b>${{n}}</b><span>${{l}}</span><div class="delta">${{d}}</div></div>`).join('');
$('units').innerHTML=DATA.plannedUnits.map(u=>`<article class="unit"><span class="tag">${{esc(u.family)}}</span><span class="tag">${{esc(u.action)}}</span><code>${{esc(u.policy_unit)}}</code><p><b>${{esc(u.heading)}}</b> · revision ${{esc(u.current_revision)}} → ${{esc(u.planned_revision)}}</p><p>${{esc(u.rationale)}}</p></article>`).join('');
$('nodes').innerHTML=DATA.plannedNodes.map(n=>`<span class="tag" title="${{esc(n.rationale)}}">${{esc(n.family)}} · ${{esc(n.lifecycle)}} · ${{esc(n.node_id)}}</span>`).join('');
const allCurrent=DATA.currentEdges.map(e=>({{...e,family:'current',change_id:'-',disposition:'unchanged',consumer_change:'no'}}));
const deltaKeys=new Set(DATA.dispositions.map(e=>[e.source,e.consumer,e.relation].join('↔')));
const unchangedCurrent=allCurrent.filter(e=>!deltaKeys.has([e.source,e.consumer,e.relation].join('↔')));
function options(id,values,allLabel,selected='all'){{ const el=$(id); el.innerHTML=`<option value="all">${{allLabel}}</option>`+[...new Set(values)].sort().map(v=>`<option value="${{esc(v)}}">${{esc(v)}}</option>`).join(''); el.value=selected; }}
options('family',DATA.dispositions.map(e=>e.family),'All planned families','N1');
options('source',DATA.dispositions.map(e=>e.source),'All owners');
options('disposition',DATA.dispositions.map(e=>e.disposition),'All dispositions');
options('relation',DATA.dispositions.map(e=>e.relation),'All relations');
$('legend').innerHTML=Object.entries(labels).filter(([k])=>k!=='unchanged').map(([k,v])=>`<span><i class="dot" style="background:${{colors[k]}}"></i>${{v}}</span>`).join('');
function filtered(){{
  const rows=[...DATA.dispositions,...($('unchanged').checked?unchangedCurrent:[])]; const q=$('search').value.toLowerCase();
  return rows.filter(r=>($('family').value==='all'||r.family===$('family').value||r.family==='current')&&($('source').value==='all'||r.source===$('source').value)&&($('disposition').value==='all'||r.disposition===$('disposition').value)&&($('relation').value==='all'||r.relation===$('relation').value)&&(!q||[r.source,r.consumer,r.relation,r.rationale||''].join(' ').toLowerCase().includes(q)));
}}
function drawGraph(rows){{
  if(!rows.length){{ $('graph').innerHTML='<div class="graph-empty">No relationships match these filters.</div>'; return; }}
  const sources=[...new Set(rows.map(r=>r.source))].sort(); const consumers=[...new Set(rows.map(r=>r.consumer))].sort();
  const rowH=38, height=Math.max(560,consumers.length*rowH+50,sources.length*90+50), width=1220, leftX=24, rightX=760, sourceW=380, consumerW=430;
  const sy=new Map(sources.map((v,i)=>[v,35+(i+1)*((height-70)/(sources.length+1))]));
  const cy=new Map(consumers.map((v,i)=>[v,35+i*rowH]));
  const edgeSvg=rows.map(r=>{{ const y1=sy.get(r.source),y2=cy.get(r.consumer); const dash=r.disposition.startsWith('conditional')?' stroke-dasharray="7 5"':''; return `<path class="edge" d="M ${{leftX+sourceW}} ${{y1}} C 560 ${{y1}}, 610 ${{y2}}, ${{rightX}} ${{y2}}" stroke="${{colors[r.disposition]||colors.unchanged}}"${{dash}}><title>${{esc(r.source)}} → ${{esc(r.consumer)}}\n${{esc(labels[r.disposition]||r.disposition)}} · ${{esc(r.relation)}}</title></path>`; }}).join('');
  const sourceSvg=sources.map(v=>`<g class="node source" transform="translate(${{leftX}},${{sy.get(v)-15}})"><rect width="${{sourceW}}" height="30"></rect><text x="10" y="19">${{esc(v.length>54?v.slice(0,52)+'…':v)}}</text><title>${{esc(v)}}</title></g>`).join('');
  const consumerSvg=consumers.map(v=>`<g class="node" transform="translate(${{rightX}},${{cy.get(v)-15}})"><rect width="${{consumerW}}" height="30"></rect><text x="10" y="19">${{esc(v.length>61?v.slice(0,59)+'…':v)}}</text><title>${{esc(v)}}</title></g>`).join('');
  $('graph').innerHTML=`<svg viewBox="0 0 ${{width}} ${{height}}" width="${{width}}" height="${{height}}" role="img" aria-label="Policy owners connected to affected consumers">${{edgeSvg}}${{sourceSvg}}${{consumerSvg}}</svg>`;
}}
function renderRows(rows){{
  $('status').innerHTML=`<div class="${{rows.some(r=>r.disposition.startsWith('conditional'))?'warning':'warning ok'}}">Showing ${{rows.length}} relationships across ${{new Set(rows.map(r=>r.source)).size}} owners and ${{new Set(rows.map(r=>r.consumer)).size}} consumers.${{rows.some(r=>r.disposition.startsWith('conditional'))?' Conditional edges remain unresolved until their named milestone audit selects a final disposition.':' Every shown planned edge has a non-conditional disposition.'}}</div>`;
  $('rows').innerHTML=rows.map(r=>`<tr><td>${{esc(r.family)}}</td><td><code>${{esc(r.source)}}</code></td><td><code>${{esc(r.consumer)}}</code></td><td>${{esc(r.relation)}}</td><td><span class="pill" style="color:${{colors[r.disposition]}};background:${{colors[r.disposition]}}18">${{esc(labels[r.disposition]||r.disposition)}}</span></td><td>${{esc(r.rationale||'Current relationship outside the planned delta.')}}</td></tr>`).join('');
  drawGraph(rows);
}}
function refresh(){{ renderRows(filtered()); }}
['family','source','disposition','relation','search','unchanged'].forEach(id=>$(id).addEventListener(id==='search'?'input':'change',refresh));
refresh();
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when output is stale")
    parser.add_argument(
        "--state",
        choices=("planning", "transition", "accepted"),
        default="planning",
        help="validate against the pre-change, milestone-transition, or accepted graph",
    )
    args = parser.parse_args()
    root = repository_root()
    current_units, current_edges, canonical_modules, current_catalog_nodes = load_current(root)
    planned_units = load_tsv(PLANNED_UNITS, UNIT_HEADERS)
    dispositions = load_tsv(DISPOSITIONS, EDGE_HEADERS)
    inventory = load_tsv(CURRENT_INVENTORY, INVENTORY_HEADERS)
    planned_nodes = load_tsv(PLANNED_NODES, NODE_HEADERS)
    notes = validate(
        current_units,
        current_edges,
        planned_units,
        dispositions,
        inventory,
        planned_nodes,
        root,
        canonical_modules,
        current_catalog_nodes,
        args.state,
    )
    baseline_units = reconstruct_baseline_units(current_units, planned_units, args.state)
    baseline_edges = [
        row
        for row in reconstruct_baseline_edges(current_edges, dispositions, args.state)
        if is_standards_impact(row, canonical_modules)
    ]
    impact_dispositions = [
        row for row in dispositions if is_standards_impact(row, canonical_modules)
    ]
    rendered = render(
        baseline_units,
        baseline_edges,
        planned_units,
        impact_dispositions,
        planned_nodes,
        notes,
        args.state,
    )
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print(f"stale: {OUTPUT.relative_to(root)}", file=sys.stderr)
            return 1
        print(f"current: {OUTPUT.relative_to(root)}")
        return 0
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(root)}")
    for note in notes:
        print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
