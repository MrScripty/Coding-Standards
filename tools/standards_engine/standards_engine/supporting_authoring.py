"""Supporting-content edits staged inside the existing atomic logical change."""
from __future__ import annotations

from dataclasses import replace
from typing import Mapping

from tools.standards_metadata.standards_metadata import (
    APPLICATION_CONTENT, DECISION_PROVENANCE, ApplicationExposure, DecisionProvenance,
    FrozenContentSource, load_supporting_content,
)
from .supporting import subject_binding

SUPPORT_EDIT_KINDS = frozenset({"put-provenance", "retire-provenance",
                              "approve-application-content", "withdraw-application-content",
                              "revise-operational-artifact"})


def parse_edit(raw: Mapping[str, object]):
    from .logical_authoring import (_exact, _mapping, _text, _semantic_id,
                                    _relationship_consumer, _structured, _evidence_list, _invalid)
    kind = raw["kind"]
    if kind == "put-provenance":
        _exact(raw, {"kind", "record"}, kind)
        record = _mapping(raw["record"], "provenance")
        optional = {"assumptions", "limits", "alternatives", "reconsideration", "supersedes"}
        required = {"id", "subject", "origin", "rationale", "evidence"}
        if not required <= record.keys() or set(record) - required - optional:
            raise _invalid("AUTHORING.INVALID_PROVENANCE", "Provenance fields are incomplete or unsupported.")
        identity = _semantic_id(record["id"], "provenance ID")
        _semantic_id(record["subject"], "provenance subject")
        if record["origin"] not in {"documented-original", "reconstructed-history", "current-justification", "unrecorded"}:
            raise _invalid("AUTHORING.INVALID_PROVENANCE", "Select a declared provenance origin.")
        if record["origin"] == "unrecorded" and record["rationale"] == "":
            pass
        else:
            _text(record["rationale"], "rationale")
        if not isinstance(record["evidence"], list):
            raise _invalid("AUTHORING.INVALID_PROVENANCE", "Evidence must be a reference array.")
        if record["evidence"]:
            record["evidence"] = [item.as_contract() for item in _evidence_list(record["evidence"], "provenance evidence")]
        for field in optional & record.keys():
            if not isinstance(record[field], list):
                raise _invalid("AUTHORING.INVALID_PROVENANCE", "Optional sections must be arrays.")
            for value in record[field]:
                _text(value, field)
        return _structured({"kind": kind, "record": record}, target=identity, facet="provenance")
    if kind == "retire-provenance":
        _exact(raw, {"kind", "id"}, kind)
        return _structured(raw, target=_semantic_id(raw["id"], "provenance ID"), facet="provenance")
    if kind in {"approve-application-content", "withdraw-application-content"}:
        _exact(raw, {"kind", "target"}, kind)
        target = _relationship_consumer(raw["target"])
        return _structured(raw, target=target if isinstance(target, str) else target["id"], facet="application-exposure")
    _exact(raw, {"kind", "target", "title", "body"}, kind)
    target = _relationship_consumer(raw["target"])
    if isinstance(target, str):
        raise _invalid("AUTHORING.TARGET_HANDLE_REQUIRED", "Operational aids use a returned authoring target.")
    title = _text(raw["title"], "title")
    if "\n" in title or "\r" in title:
        raise _invalid("AUTHORING.INVALID_TITLE", "Operational titles occupy one line.")
    _text(raw["body"], "body")
    return _structured(raw, target=target["id"], facet="operational-aid")


def _write(files, records, entries):
    from .logical_authoring import _toml_inline
    files[DECISION_PROVENANCE] = ("schema_version = 1\nrecords = " +
        _toml_inline([records[key].as_contract() for key in sorted(records)]) + "\n").encode("utf-8")
    files[APPLICATION_CONTENT] = ("schema_version = 1\nentries = " +
        _toml_inline([entries[key].as_contract() for key in sorted(entries)]) + "\n").encode("utf-8")


def begin_edits(files, edits, base, snapshot):
    """Prepare private staging for retirements/repointing before owner edits."""
    from .logical_authoring import _resolve_consumer, _invalid
    if not edits:
        return
    support = load_supporting_content(FrozenContentSource(files))
    records, entries = dict(support.provenance), dict(support.exposure)
    changed = False
    for edit in edits:
        kind = edit["kind"]
        if kind in {"retire-provenance", "put-provenance"}:
            identity = edit["id"] if kind == "retire-provenance" else edit["record"]["id"]
            if identity in records:
                records[identity] = replace(records[identity], retired=True)
                changed = True
            elif kind == "retire-provenance":
                raise _invalid("AUTHORING.PROVENANCE_UNAVAILABLE", "Retirement requires an existing provenance record.")
        elif kind == "withdraw-application-content":
            target = _resolve_consumer(edit["target"], base, snapshot)
            if target not in entries:
                raise _invalid("AUTHORING.EXPOSURE_UNAVAILABLE", "Withdrawal requires an existing exposure declaration.")
            del entries[target]
            changed = True
    if changed:
        _write(files, records, entries)


def finish_edits(files, edits, base, snapshot, compile_current):
    from .logical_authoring import _resolve_consumer, _invalid, _unsupported
    if not edits:
        return
    for edit in edits:
        if edit["kind"] != "revise-operational-artifact":
            continue
        target = _resolve_consumer(edit["target"], base, snapshot)
        artifact = base.policy_impact.artifacts.get(target)
        if artifact is None or artifact.artifact_kind not in {"prompt", "template"}:
            raise _unsupported("AUTHORING.OPERATIONAL_TARGET_REQUIRED", "Select a registered prompt or template.")
        # Registration owns the path. Requests supply neither paths nor raw files.
        files[artifact.repository_path] = f"# {edit['title']}\n\n{edit['body'].rstrip()}\n".encode("utf-8")
    current = compile_current(files)
    records, entries = dict(current.supporting.provenance), dict(current.supporting.exposure)
    for edit in edits:
        if edit["kind"] == "put-provenance":
            raw = dict(edit["record"])
            raw["subject_binding"] = subject_binding(current, raw["subject"])
            record = DecisionProvenance.from_mapping(raw)
            records[record.id] = record
        elif edit["kind"] == "approve-application-content":
            target = _resolve_consumer(edit["target"], base, snapshot)
            material = current.materials.get(target)
            if material is None:
                raise _invalid("AUTHORING.EXPOSURE_TARGET_REQUIRED", "Qualify a complete module or registered operational aid.")
            entries[target] = ApplicationExposure(target, material.binding)
    if edits:
        _write(files, records, entries)
    # The caller compiles the entire final set, including same-set references,
    # before publishing an immutable proposal revision.
