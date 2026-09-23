"""Compose captured standard and operational-aid material for review and use."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, TYPE_CHECKING

from tools.standards_metadata.standards_metadata import (
    CanonicalStandardsCorpus, ContentSource, MetadataError, MetadataFailure,
    PolicyUnit, PolicyUnitTombstone, SupportingContent, content_digest,
)
from tools.standards_policy_impact.standards_policy_impact import CompiledPolicyImpactSet, thaw

if TYPE_CHECKING:
    from .engine import CompiledSnapshot


@dataclass(frozen=True, slots=True)
class ContentMaterial:
    id: str
    role: str
    level: str
    path: str
    content: str
    binding: str
    requires: tuple[str, ...] = ()
    specializes: tuple[str, ...] = ()


def material_error(message: str) -> MetadataError:
    return MetadataError(MetadataFailure("SUPPORT.INVALID_BINDING", "invalid", message))


def build_materials(source: ContentSource, corpus: CanonicalStandardsCorpus,
                    impact: CompiledPolicyImpactSet, router: object,
                    supporting: SupportingContent) -> Mapping[str, ContentMaterial]:
    """Capture complete eligible source units; policy reads inherit their module."""
    from .agent_navigation import fact_definitions
    materials = {}
    for module in corpus.modules:
        text = source.read_bytes(module.path).decode("utf-8")
        record = {
            "id": module.module_id, "role": module.role, "level": module.level,
            "content": text,
            "policy_units": [unit.as_declaration() for unit in corpus.policy_unit_corpus.for_module(module.module_id)],
        }
        if module.module_id == "router":
            record["routing"] = {
                "facts": fact_definitions(router),
                "base_modules": list(router.base_modules),
                "rules": [{"id": rule.id, "target": rule.target,
                           "when": rule.program.as_expression()} for rule in router.rules],
            }
        materials[module.module_id] = ContentMaterial(
            module.module_id, module.role, module.level, module.path,
            text, content_digest(record), module.requires, module.specializes,
        )
    for artifact in impact.artifacts.values():
        if artifact.artifact_kind not in {"prompt", "template"}:
            continue
        if artifact.id in materials:
            raise material_error("Operational aids and standards have distinct identities.")
        text = source.read_bytes(artifact.repository_path).decode("utf-8")
        # Operational aids consume selected policy owners. Binding their owners'
        # exact content prevents a stale prompt from outliving a material rule edit.
        owners = []
        for semantics in impact.semantics.values():
            if semantics.consumer != artifact.id:
                continue
            owner = corpus.resolve_policy_unit(semantics.source)
            if not isinstance(owner, PolicyUnit):
                raise material_error("Operational-aid relationships require active policy owners.")
            owners.append({"policy": owner.id, "binding": owner.representation_digest,
                           "declaration": owner.as_declaration(),
                           "source_scope": thaw(semantics.source_scope),
                           "consumer_scope": thaw(semantics.consumer_scope),
                           "relation": semantics.relation,
                           "applicability": semantics.applicability_program.as_expression()})
        binding = content_digest({"id": artifact.id, "kind": artifact.artifact_kind,
                                  "authority": artifact.authority, "content": text,
                                  "owners": sorted(owners, key=lambda item: (item["policy"], item["relation"]))})
        materials[artifact.id] = ContentMaterial(
            artifact.id, artifact.artifact_kind, "REFERENCE", artifact.repository_path,
            text, binding,
        )
    for target in supporting.exposure:
        if target not in materials:
            raise material_error("Application exposure requires a complete registered content unit.")
    for record in supporting.provenance.values():
        if record.id in materials or corpus.resolve_policy_unit(record.id) is not None:
            raise material_error("Decision provenance has a distinct identity namespace.")
        subject = corpus.resolve_module(record.subject) or corpus.resolve_policy_unit(record.subject)
        if (subject is None or isinstance(subject, PolicyUnitTombstone)) and not record.retired:
            raise material_error("Active provenance requires a canonical subject.")
        identity = getattr(subject, "module_id", getattr(subject, "id", None))
        if subject is not None and identity != record.subject:
            raise material_error("Provenance subjects use canonical identities rather than aliases.")
    return MappingProxyType(materials)


def subject_binding(compiled: CompiledSnapshot, subject: str) -> str:
    module = compiled.corpus.resolve_module(subject)
    if module is not None and module.module_id == subject:
        return compiled.materials[subject].binding
    unit = compiled.corpus.resolve_policy_unit(subject)
    if isinstance(unit, PolicyUnit) and unit.id == subject:
        return content_digest({"id": unit.id, "content": unit.content,
                               "declaration": unit.as_declaration()})
    raise material_error("Provenance requires an active canonical standard or policy unit.")


def record_state(compiled: CompiledSnapshot, record: object) -> str:
    if record.retired:
        return "retired"
    return "current" if record.subject_binding == subject_binding(compiled, record.subject) else "needs-review"


def resolve_material(compiled: CompiledSnapshot, target: str) -> tuple[ContentMaterial, PolicyUnit | None] | None:
    module = compiled.corpus.resolve_module(target)
    if module is not None:
        return compiled.materials[module.module_id], None
    unit = compiled.corpus.resolve_policy_unit(target)
    if isinstance(unit, PolicyUnit):
        return compiled.materials[unit.module], unit
    artifact = compiled.policy_impact.artifacts.get(target)
    if artifact is None:
        artifact = next((item for item in compiled.policy_impact.artifacts.values()
                         if target in item.aliases), None)
    if artifact is not None and artifact.id in compiled.materials:
        return compiled.materials[artifact.id], None
    return None


def review_authorities(compiled: CompiledSnapshot):
    """Bind local support review to material without relabelling it as policy."""
    from tools.standards_analysis.standards_analysis import SupportingContentAuthority
    result = []
    for record in compiled.supporting.provenance.values():
        representation = content_digest(record.as_contract())
        subject = {"state": "retired"} if record.retired else {"binding": subject_binding(compiled, record.subject)}
        result.append(SupportingContentAuthority(
            record.id, representation, content_digest({"record": record.as_contract(), "subject": subject})))
    for entry in compiled.supporting.exposure.values():
        material = compiled.materials[entry.target]
        result.append(SupportingContentAuthority(
            f"application-exposure:{entry.target}", content_digest(entry.as_contract()),
            content_digest({"declaration": entry.as_contract(), "material": material.binding})))
    for material in compiled.materials.values():
        if material.role in {"prompt", "template"}:
            result.append(SupportingContentAuthority(
                f"operational-aid:{material.id}", content_digest(material.content), material.binding))
    return tuple(sorted(result, key=lambda item: item.id))


def read_supporting(compiled: CompiledSnapshot, projection, target: str):
    """Authoring-only read forms for records and registered operational aids."""
    record = compiled.supporting.provenance.get(target)
    if record is not None:
        return {"kind": "provenance-read-result", "authority": projection.authority.as_contract(),
                "record": record.as_contract(), "state": record_state(compiled, record), "next_operations": []}
    selected = resolve_material(compiled, target)
    if selected is None or selected[0].role not in {"prompt", "template"}:
        return None
    material = selected[0]
    return {"kind": "operational-read-result", "authority": projection.authority.as_contract(),
            "target": projection.authoring_target(material.id), "canonical_id": material.id,
            "role": material.role, "content": material.content,
            "application_exposure": compiled.supporting.exposure_state(material.id, material.binding),
            "next_operations": []}
