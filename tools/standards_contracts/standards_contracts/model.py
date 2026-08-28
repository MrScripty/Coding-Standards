from __future__ import annotations

import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class OperationContract:
    id: str
    input_definition: str
    result_definitions: tuple[str, ...]
    capability: str | None
    capability_by_submission: Mapping[str, str]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "capability_by_submission",
            MappingProxyType(dict(self.capability_by_submission)),
        )


@dataclass(frozen=True, slots=True)
class InterfaceContract:
    schema_version: int
    interface_schema_version: int
    request_contract_version: int
    result_projection_version: int
    operations: tuple[OperationContract, ...]


@dataclass(frozen=True, slots=True)
class FieldProjection:
    contract_name: str
    python_name: str
    annotation: str
    required: bool
    title: str | None
    description: str | None
    has_default: bool
    default_annotation: object


@dataclass(frozen=True, slots=True)
class DefinitionProjection:
    name: str
    annotation: str
    fields: tuple[FieldProjection, ...]
    title: str | None
    description: str | None
    has_default: bool
    default_annotation: object

    @property
    def is_object_model(self) -> bool:
        return bool(self.fields)


@dataclass(frozen=True, slots=True)
class ProjectionArtifacts:
    python_source: str
    agent_tools_json: str
    definitions: tuple[DefinitionProjection, ...]

    @property
    def agent_tools(self) -> Mapping[str, object]:
        return json.loads(self.agent_tools_json)


__all__ = (
    "DefinitionProjection",
    "FieldProjection",
    "InterfaceContract",
    "OperationContract",
    "ProjectionArtifacts",
)
