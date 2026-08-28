from .capture import CaptureSource, GitCaptureSource, GitlinkSource, NativeCaptureSource
from .closure import (
    AuthorityBoundValue,
    ExecutionAuthorityRoot,
    ExecutionClosure,
    ExecutionClosureCodec,
    Operation,
)
from .envelope import decode_envelope, encode_envelope
from .errors import (
    AuthorityError,
    AuthorityFailure,
    FailureKind,
    invalid,
    unavailable,
    unsupported,
)
from .model import (
    AuthorityCodec,
    AuthorityEnvelope,
    AuthorityHandle,
    AuthorityReference,
    CodecContext,
    CodecSet,
    PutResult,
    RecoveryReceipt,
)
from .platform import open_default_store
from .recovery import SQLiteRecovery, default_store_path, verify_sqlite_capabilities
from .repository import AuthorityRepository, ResolvedAuthority
from .snapshot import (
    CONTENT_SNAPSHOT_CODEC,
    CaptureRequest,
    ContentSnapshot,
    ContentSnapshotCodec,
    RepositoryPath,
    SnapshotFile,
)
from .store import MemoryObjectStore, ObjectStore, SQLiteObjectStore

EXECUTION_CLOSURE_CODEC = ExecutionClosureCodec(
    {
        "content-snapshot",
        "canonical-standards-corpus",
        "compiled-policy-impact",
        "standards-graph",
        "routing-projection",
        "coverage-horizon",
        "analysis-context",
        "fact-requirement",
        "provider-authority",
        "authorization-grant",
        "fact-observation",
        "coverage-view",
        "coverage-requirement",
        "coverage-attestation",
        "coverage-certificate",
        "analysis-root",
        "operation-authority-contract",
        "standards-authority-view",
        "navigation-result",
        "policy-inspection",
        "relationship-inspection",
    }
)
AUTHORITY_CODECS = CodecSet(
    "standards-authority", (CONTENT_SNAPSHOT_CODEC, EXECUTION_CLOSURE_CODEC)
)

__all__ = (
    "AUTHORITY_CODECS",
    "CONTENT_SNAPSHOT_CODEC",
    "AuthorityBoundValue",
    "AuthorityCodec",
    "AuthorityEnvelope",
    "AuthorityError",
    "AuthorityFailure",
    "AuthorityHandle",
    "AuthorityReference",
    "AuthorityRepository",
    "CaptureRequest",
    "CaptureSource",
    "CodecContext",
    "CodecSet",
    "ContentSnapshot",
    "ContentSnapshotCodec",
    "ExecutionAuthorityRoot",
    "ExecutionClosure",
    "ExecutionClosureCodec",
    "EXECUTION_CLOSURE_CODEC",
    "FailureKind",
    "GitCaptureSource",
    "GitlinkSource",
    "MemoryObjectStore",
    "NativeCaptureSource",
    "ObjectStore",
    "Operation",
    "PutResult",
    "RecoveryReceipt",
    "RepositoryPath",
    "ResolvedAuthority",
    "SQLiteObjectStore",
    "SQLiteRecovery",
    "SnapshotFile",
    "decode_envelope",
    "default_store_path",
    "encode_envelope",
    "invalid",
    "open_default_store",
    "unavailable",
    "unsupported",
    "verify_sqlite_capabilities",
)
