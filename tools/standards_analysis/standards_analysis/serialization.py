from __future__ import annotations

import hashlib
from typing import Any

from tools.standards_metadata.standards_metadata.serialization import (
    canonical_json_bytes,
    digest_bytes,
)


def identity(domain: str, prefix: str, value: Any) -> str:
    payload = domain.encode("utf-8") + b"\0" + canonical_json_bytes(value)
    return f"{prefix}:sha256:{hashlib.sha256(payload).hexdigest()}"


__all__ = ("canonical_json_bytes", "digest_bytes", "identity")
