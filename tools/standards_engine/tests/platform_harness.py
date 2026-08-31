from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from tools.standards_analysis.standards_analysis import (
    AnalysisExecutionContext,
    AuthorizationAuthorityContract,
    AuthorizationClaim,
    EvidenceContractKey,
    EvidenceReference,
    ResolvedEvidence,
)
from tools.standards_engine.standards_engine import (
    AgentToolFacade,
    AnalysisChildInspectionResult,
    AnalysisInspectionResult,
    CreateSnapshotResult,
    DeleteSnapshotResult,
    FindSnapshotsResult,
    PendingResult,
    PolicyInspectionResult,
    ReadResult,
    ResolveCall,
    SnapshotInspectionResult,
    StandardsEngine,
    UndeleteSnapshotResult,
)
from tools.standards_engine.standards_engine.tools import _contracts


SCHEMA_VERSION = 1
POLICY_ID = "workflow.planning"
POLICY_UNIT_ID = "workflow.planning.written-plan-applicability"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PUBLIC_OPERATIONS = (
    "create_snapshot",
    "find_snapshots",
    "delete_snapshot",
    "undelete_snapshot",
    "query",
    "prepare",
    "resolve",
    "inspect",
)


class HarnessError(RuntimeError):
    pass


def _reference(identifier: str) -> EvidenceReference:
    content = identifier.encode("utf-8")
    return EvidenceReference(
        identifier,
        f"sha256:{hashlib.sha256(content).hexdigest()}",
        "repository-content",
        "1",
    )


class HarnessAuthorizer:
    contract = AuthorizationAuthorityContract(
        "issuer.platform-harness",
        1,
        "principal.platform-harness",
        "authorization-grant.v1",
        (EvidenceContractKey("repository-content", "1"),),
        "revocation.platform-harness",
        1,
        "authorization-revocation.v1",
        (EvidenceContractKey("repository-content", "1"),),
    )

    def authorize(self, request: Any) -> AuthorizationClaim:
        return AuthorizationClaim(
            request.action,
            request.subject_kind,
            request.subject_id,
            request.capability,
            tuple(
                ResolvedEvidence(item, item.id.encode("utf-8"))
                for item in request.evidence
            ),
            (
                ResolvedEvidence(
                    _reference("platform-harness-authorization"),
                    b"platform-harness-authorization",
                ),
            ),
            (
                ResolvedEvidence(
                    _reference("platform-harness-revocation"),
                    b"platform-harness-revocation",
                ),
            ),
            "not-revoked",
            "allow",
        )


def _environment() -> dict[str, object]:
    return {
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "operating_system": platform.system(),
        "platform_release": platform.release(),
        "python": platform.python_version(),
        "sqlite": sqlite3.sqlite_version,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return f"sha256:{digest.hexdigest()}"


class _FacadeSession:
    def __init__(self, engine: StandardsEngine) -> None:
        self._facade = AgentToolFacade(engine, _contracts(REPOSITORY_ROOT))
        self._operations: set[str] = set()

    @property
    def operations(self) -> list[str]:
        return [
            operation.replace("_", "-")
            for operation in PUBLIC_OPERATIONS
            if operation in self._operations
        ]

    def call(self, operation: str, arguments: object) -> dict[str, object]:
        self._operations.add(operation)
        return getattr(self._facade, operation)(arguments)


def _expect(value: dict[str, object], expected: type, operation: str) -> Any:
    if value.get("kind") == "rejected-result":
        raise HarnessError(
            f"{operation} rejected with {value.get('code')} "
            f"({value.get('outcome')}): {value.get('message')}"
        )
    try:
        return expected.from_value(value)
    except (TypeError, ValueError) as error:
        raise HarnessError(
            f"{operation} did not return a valid {expected.__name__}: {error}"
        ) from error


def _analysis_request(snapshot: dict[str, object]) -> dict[str, object]:
    return {
        "kind": "analysis-request",
        "base_snapshot": snapshot,
        "proposed_snapshot": snapshot,
        "changes": [
            {
                "kind": "modification",
                "accepted_ids": [POLICY_UNIT_ID],
                "proposed_ids": [POLICY_UNIT_ID],
                "scope": {"kind": "whole-artifact"},
            }
        ],
        "semantic_proposals": [],
        "contract_version": 4,
    }


def _disposition(result: PendingResult) -> ResolveCall:
    operation = next(
        (
            item
            for item in result.next_operations
            if item.request_kind == "consumer-disposition"
        ),
        None,
    )
    if operation is None:
        raise HarnessError("prepare produced no consumer-disposition operation")
    obligation = next(
        (item for item in result.obligations if item.handle == operation.work),
        None,
    )
    if obligation is None:
        raise HarnessError("resolve operation did not reference a current obligation")
    evidence = _reference("platform-harness-review")
    return ResolveCall.from_value(
        {
            "analysis": result.handle.as_contract(),
            "submission": {
                "kind": "consumer-disposition",
                "obligation": operation.work.as_contract(),
                "result": "reviewed-no-change",
                "rationale": "The selected consumer was reviewed by the harness.",
                "evidence": [evidence.as_contract()],
                "fingerprint": obligation.fingerprint.as_contract(),
            },
        }
    )


def produce(repository: Path, store: Path, manifest_path: Path) -> dict[str, object]:
    if store.exists() or manifest_path.exists():
        raise HarnessError("produce requires absent store and manifest paths")
    store.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    engine = StandardsEngine.open_repository(
        repository,
        store_path=store,
        execution_context=AnalysisExecutionContext(HarnessAuthorizer()),
    )
    facade = _FacadeSession(engine)
    try:
        created = _expect(
            facade.call("create_snapshot", {"kind": "create-snapshot"}),
            CreateSnapshotResult,
            "create-snapshot",
        )
        snapshot = created.snapshot.snapshot
        found = _expect(
            facade.call("find_snapshots", {"kind": "find-snapshots"}),
            FindSnapshotsResult,
            "find-snapshots",
        )
        if not any(item.snapshot == snapshot for item in found.snapshots):
            raise HarnessError("created snapshot is absent from active discovery")
        read = _expect(
            facade.call(
                "query",
                {
                    "snapshot": snapshot.as_contract(),
                    "request": {"kind": "read", "target": POLICY_ID},
                },
            ),
            ReadResult,
            "query/read",
        )
        _expect(
            facade.call("inspect", {"handle": read.policy.handle.as_contract()}),
            PolicyInspectionResult,
            "inspect/policy",
        )
        prepared = _expect(
            facade.call(
                "prepare",
                {"request": _analysis_request(snapshot.as_contract())},
            ),
            PendingResult,
            "prepare",
        )
        child = prepared.obligations[0].handle
        resolved = _expect(
            facade.call("resolve", _disposition(prepared).as_contract()),
            PendingResult,
            "resolve",
        )
        _expect(
            facade.call("inspect", {"handle": resolved.handle.as_contract()}),
            AnalysisInspectionResult,
            "inspect/resolved-analysis",
        )
    finally:
        engine.close()

    manifest: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "producer": _environment(),
        "store": {"sha256": _sha256(store), "size": store.stat().st_size},
        "snapshot": snapshot.as_contract(),
        "policy": read.policy.handle.as_contract(),
        "analysis": prepared.handle.as_contract(),
        "analysis_child": child.as_contract(),
        "resolved_analysis": resolved.handle.as_contract(),
        "read": {
            "target": POLICY_ID,
            "content_sha256": (
                f"sha256:{hashlib.sha256(read.content.encode('utf-8')).hexdigest()}"
            ),
        },
        "operations": facade.operations,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {
        "kind": "a1c-platform-produce-result",
        "environment": manifest["producer"],
        "manifest": str(manifest_path),
        "store": str(store),
        "store_sha256": manifest["store"]["sha256"],
    }


def _load_manifest(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise HarnessError(f"manifest is unavailable or invalid: {error}") from error
    required = {
        "schema_version",
        "producer",
        "store",
        "snapshot",
        "policy",
        "analysis",
        "analysis_child",
        "resolved_analysis",
        "read",
        "operations",
    }
    if type(value) is not dict or set(value) != required:
        raise HarnessError("manifest fields do not match the platform contract")
    if value["schema_version"] != SCHEMA_VERSION:
        raise HarnessError("manifest schema version is unsupported")
    return value


def _verify_store(store: Path, manifest: dict[str, object]) -> None:
    expected = manifest["store"]
    if type(expected) is not dict or set(expected) != {"sha256", "size"}:
        raise HarnessError("manifest store identity is invalid")
    if not store.is_file():
        raise HarnessError("closed store is unavailable")
    if store.stat().st_size != expected["size"] or _sha256(store) != expected["sha256"]:
        raise HarnessError("closed store bytes do not match the portable manifest")


def _temporary_repository(root: Path) -> Path:
    repository = root / "unrelated-repository"
    repository.mkdir()
    commands = (
        ("init", "-q"),
        ("config", "user.email", "platform-harness@example.invalid"),
        ("config", "user.name", "Platform Harness"),
    )
    for arguments in commands:
        subprocess.run(("git", *arguments), cwd=repository, check=True)
    (repository / "unrelated.txt").write_text("unrelated\n", encoding="utf-8")
    subprocess.run(("git", "add", "unrelated.txt"), cwd=repository, check=True)
    subprocess.run(
        ("git", "commit", "-q", "-m", "fixture"), cwd=repository, check=True
    )
    return repository


def _concurrent_probe(
    repository: Path, store: Path, manifest_path: Path
) -> dict[str, object]:
    environment = dict(os.environ)
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": str(REPOSITORY_ROOT),
        }
    )
    completed = subprocess.run(
        (
            sys.executable,
            "-P",
            str(Path(__file__).resolve()),
            "probe",
            "--repository",
            str(repository),
            "--store",
            str(store),
            "--manifest",
            str(manifest_path),
        ),
        cwd=repository,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise HarnessError(
            "concurrent cold probe failed: "
            + (completed.stderr or completed.stdout).strip()
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise HarnessError("concurrent cold probe returned invalid evidence") from error
    return result


def probe(repository: Path, store: Path, manifest_path: Path) -> dict[str, object]:
    manifest = _load_manifest(manifest_path)
    engine = StandardsEngine.open_repository(repository, store_path=store)
    facade = _FacadeSession(engine)
    try:
        snapshot = manifest["snapshot"]
        read = _expect(
            facade.call(
                "query",
                {
                    "snapshot": snapshot,
                    "request": {"kind": "read", "target": POLICY_ID},
                },
            ),
            ReadResult,
            "concurrent query/read",
        )
        _expect(
            facade.call("inspect", {"handle": manifest["analysis"]}),
            AnalysisInspectionResult,
            "concurrent inspect/analysis",
        )
    finally:
        engine.close()
    return {
        "kind": "a1c-platform-concurrent-probe-result",
        "content_sha256": (
            f"sha256:{hashlib.sha256(read.content.encode('utf-8')).hexdigest()}"
        ),
    }


def consume(store: Path, manifest_path: Path) -> dict[str, object]:
    manifest = _load_manifest(manifest_path)
    _verify_store(store, manifest)
    with tempfile.TemporaryDirectory() as temporary:
        repository = _temporary_repository(Path(temporary))
        engine = StandardsEngine.open_repository(repository, store_path=store)
        facade = _FacadeSession(engine)
        try:
            snapshot = manifest["snapshot"]
            found = _expect(
                facade.call("find_snapshots", {"kind": "find-snapshots"}),
                FindSnapshotsResult,
                "find-snapshots",
            )
            if snapshot not in [item.snapshot.as_contract() for item in found.snapshots]:
                raise HarnessError("transferred snapshot is absent from active discovery")
            read = _expect(
                facade.call(
                    "query",
                    {
                        "snapshot": snapshot,
                        "request": {"kind": "read", "target": POLICY_ID},
                    },
                ),
                ReadResult,
                "query/read",
            )
            observed_digest = (
                f"sha256:{hashlib.sha256(read.content.encode('utf-8')).hexdigest()}"
            )
            if observed_digest != manifest["read"]["content_sha256"]:
                raise HarnessError("transferred read content changed")
            _expect(
                facade.call("inspect", {"handle": snapshot}),
                SnapshotInspectionResult,
                "inspect/snapshot",
            )
            _expect(
                facade.call("inspect", {"handle": manifest["policy"]}),
                PolicyInspectionResult,
                "inspect/policy",
            )
            _expect(
                facade.call("inspect", {"handle": manifest["analysis"]}),
                AnalysisInspectionResult,
                "inspect/analysis",
            )
            _expect(
                facade.call("inspect", {"handle": manifest["analysis_child"]}),
                AnalysisChildInspectionResult,
                "inspect/analysis-child",
            )
            _expect(
                facade.call("inspect", {"handle": manifest["resolved_analysis"]}),
                AnalysisInspectionResult,
                "inspect/resolved-analysis",
            )
            concurrent = _concurrent_probe(repository, store, manifest_path)
            _expect(
                facade.call(
                    "delete_snapshot",
                    {"kind": "delete-snapshot", "snapshot": snapshot},
                ),
                DeleteSnapshotResult,
                "delete-snapshot",
            )
            unavailable = facade.call(
                "query",
                {
                    "snapshot": snapshot,
                    "request": {"kind": "read", "target": POLICY_ID},
                },
            )
            if (
                unavailable.get("kind") != "rejected-result"
                or unavailable.get("outcome") != "unavailable"
            ):
                raise HarnessError("quarantined snapshot did not become typed unavailable")
            quarantined = _expect(
                facade.call(
                    "find_snapshots",
                    {"kind": "find-snapshots", "lifecycle": "quarantined"},
                ),
                FindSnapshotsResult,
                "find-snapshots/quarantined",
            )
            if snapshot not in [item.snapshot.as_contract() for item in quarantined.snapshots]:
                raise HarnessError("deleted snapshot is absent from quarantine discovery")
            _expect(
                facade.call(
                    "undelete_snapshot",
                    {"kind": "undelete-snapshot", "snapshot": snapshot},
                ),
                UndeleteSnapshotResult,
                "undelete-snapshot",
            )
            _expect(
                facade.call(
                    "query",
                    {
                        "snapshot": snapshot,
                        "request": {"kind": "read", "target": POLICY_ID},
                    },
                ),
                ReadResult,
                "query/read-after-undelete",
            )
            _expect(
                facade.call("inspect", {"handle": manifest["analysis"]}),
                AnalysisInspectionResult,
                "inspect/analysis-after-undelete",
            )
        finally:
            engine.close()
    return {
        "kind": "a1c-platform-consume-result",
        "consumer": _environment(),
        "producer": manifest["producer"],
        "store_sha256": manifest["store"]["sha256"],
        "concurrent_probe": concurrent,
        "operations": [
            operation.replace("_", "-")
            for operation in PUBLIC_OPERATIONS
            if operation.replace("_", "-")
            in set(manifest["operations"]) | set(facade.operations)
        ],
        "canonical_source_repository_used": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the A1c platform harness.")
    commands = parser.add_subparsers(dest="command", required=True)
    producer = commands.add_parser("produce")
    producer.add_argument("--repository", type=Path, required=True)
    producer.add_argument("--store", type=Path, required=True)
    producer.add_argument("--manifest", type=Path, required=True)
    consumer = commands.add_parser("consume")
    consumer.add_argument("--store", type=Path, required=True)
    consumer.add_argument("--manifest", type=Path, required=True)
    child = commands.add_parser("probe")
    child.add_argument("--repository", type=Path, required=True)
    child.add_argument("--store", type=Path, required=True)
    child.add_argument("--manifest", type=Path, required=True)
    return parser


def main(arguments: list[str] | None = None) -> int:
    options = _parser().parse_args(arguments)
    try:
        if options.command == "produce":
            result = produce(options.repository, options.store, options.manifest)
        elif options.command == "consume":
            result = consume(options.store, options.manifest)
        else:
            result = probe(options.repository, options.store, options.manifest)
    except (HarnessError, OSError, subprocess.SubprocessError, ValueError) as error:
        print(
            json.dumps(
                {"kind": "a1c-platform-harness-error", "message": str(error)},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
