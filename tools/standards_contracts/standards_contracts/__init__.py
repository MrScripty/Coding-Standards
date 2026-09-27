from pathlib import Path

from .compiler import CompiledContracts, compile_contracts
from .errors import ContractError, ContractFailure, InputIssue
from .model import (
    DefinitionProjection,
    FieldProjection,
    InterfaceContract,
    OperationContract,
    OperationVariant,
    ProjectionArtifacts,
)
from .runtime import (
    ContractRuntime,
    FrozenMap,
    MISSING,
    MissingValue,
    freeze_json,
    model_as_contract,
)

from .validation_feedback import MAX_POINTER_CHARS

from .schema_structure import (
    direct_schema_references,
    local_definition_name,
    referenced_definitions,
    schema_closure,
)


def render_repository_projections() -> dict[Path, str]:
    from .projection import render_repository_projections as render

    return render()


def projection_main(argv: list[str] | None = None) -> int:
    from .projection import projection_main as run

    return run(argv)

__all__ = (
    "CompiledContracts",
    "ContractError",
    "ContractFailure",
    "InputIssue",
    "MAX_POINTER_CHARS",
    "ContractRuntime",
    "DefinitionProjection",
    "FieldProjection",
    "FrozenMap",
    "InterfaceContract",
    "MISSING",
    "MissingValue",
    "OperationContract",
    "OperationVariant",
    "ProjectionArtifacts",
    "compile_contracts",
    "freeze_json",
    "direct_schema_references",
    "local_definition_name",
    "referenced_definitions",
    "schema_closure",
    "model_as_contract",
    "projection_main",
    "render_repository_projections",
)
