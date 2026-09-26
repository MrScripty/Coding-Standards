from pathlib import Path

from .compiler import CompiledContracts, compile_contracts
from .errors import ContractError, ContractFailure
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

from .schema_structure import (
    local_definition_name,
    map_schema_children,
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
    "local_definition_name",
    "map_schema_children",
    "referenced_definitions",
    "schema_closure",
    "model_as_contract",
    "projection_main",
    "render_repository_projections",
)
