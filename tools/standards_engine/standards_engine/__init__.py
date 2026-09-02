"""Generated Standards Engine contract and domain composition."""

from ._generated_contract import *  # noqa: F403
from ._generated_contract import __all__ as _contract_all
from .engine import StandardsEngine
from .rendering import render_text
from .tools import AgentToolFacade

__all__ = (
    *_contract_all,
    "AgentToolFacade",
    "StandardsEngine",
    "render_text",
)
