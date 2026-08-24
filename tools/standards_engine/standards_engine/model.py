from __future__ import annotations

from . import _generated_contract as _generated


for _name in _generated.__all__:
    globals()[_name] = getattr(_generated, _name)

InspectionResult = _generated.ContractInspectionResult

__all__ = (*_generated.__all__, "InspectionResult")
