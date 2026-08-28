"""Generated A1b contract and immutable authority composition."""

from ._generated_contract import *  # noqa: F403
from ._generated_contract import __all__ as _contract_all
from .authority import ENGINE_CODECS
from .engine import StandardsEngine
from .rendering import render_text
from .tools import AgentToolFacade

__all__ = (
    *_contract_all,
    "AgentToolFacade",
    "ENGINE_CODECS",
    "StandardsEngine",
    "render_text",
)
