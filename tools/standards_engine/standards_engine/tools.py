from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

from tools.standards_analysis.standards_analysis import (
    AuthorizationReference,
    ChangeDescriptor,
    ChangeKind,
    ConsumerDispositionSubmission,
    CoverageAttestation,
    CoverageAttestationSubmission,
    CoverageEvidence,
    DecisionDependency,
    DecisionFingerprint,
    EvidenceReference,
    FactObservationProvider,
    ImpactDispositionSubmission,
    ProvideFactSubmission,
    ReviewScope,
    SemanticProposal,
)
from tools.standards_engine.contracts.validate_contracts import ContractError, validate

from .engine import AnalysisStateStore, StandardsEngine
from .model import (
    AnalysisRequest,
    InspectCall,
    QueryCall,
    ReadRequest,
    RelatedRequest,
    RouteRequest,
)


INTERFACE_SCHEMA = "tools/standards_engine/contracts/a1-contract.schema.json"


class AgentToolFacade:
    """Validated structured transport over the native Standards Engine API."""

    def __init__(self, engine: StandardsEngine, schema: Mapping[str, object]) -> None:
        self._engine = engine
        self._schema = schema

    @classmethod
    def open_repository(cls, root: Path) -> AgentToolFacade:
        repo_root = root.resolve()
        schema = json.loads((repo_root / INTERFACE_SCHEMA).read_text(encoding="utf-8"))
        return cls(StandardsEngine.open_repository(repo_root), schema)

    @classmethod
    def open_analysis(
        cls,
        base_root: Path,
        proposed_root: Path,
        *,
        authorizations: tuple[AuthorizationReference, ...] = (),
        analysis_store: AnalysisStateStore | None = None,
        fact_providers: Iterable[FactObservationProvider] = (),
    ) -> AgentToolFacade:
        repo_root = proposed_root.resolve()
        schema = json.loads((repo_root / INTERFACE_SCHEMA).read_text(encoding="utf-8"))
        return cls(
            StandardsEngine.open_analysis(
                base_root,
                proposed_root,
                authorizations=authorizations,
                analysis_store=analysis_store,
                fact_providers=fact_providers,
            ),
            schema,
        )

    @property
    def snapshot(self) -> Mapping[str, object]:
        return self._engine.snapshot

    @property
    def snapshots(self) -> tuple[Mapping[str, object], ...]:
        return self._engine.snapshots

    def query(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("QueryCall", value)
            request = self._mapping(value["request"])
            kind = request["kind"]
            if kind == "route":
                typed = RouteRequest(self._mapping(request["facts"]))
            elif kind == "read":
                typed = ReadRequest(str(request["target"]))
            elif kind == "related":
                typed = RelatedRequest(
                    str(request["target"]),
                    tuple(request["groups"]),
                    str(request["direction"]),
                    bool(request["transitive"]),
                )
            else:
                return self._rejected("INTERFACE.UNSUPPORTED_REQUEST", "unsupported")
            result = self._engine.query(
                QueryCall(self._mapping(value["snapshot"]), typed)
            )
            output = result.as_contract()
            self._validate_result(output)
            return output
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))

    def prepare(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("PrepareCall", value)
            request = self._mapping(value["request"])
            result = self._engine.prepare(self._analysis_request(request))
            output = result.as_contract()
            self._validate_result(output)
            return output
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))

    def resolve(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("ResolveCall", value)
            submission = self._submission(self._mapping(value["submission"]))
            result = self._engine.resolve(
                self._mapping(value["analysis"]),
                submission,
            )
            output = result.as_contract()
            self._validate_result(output)
            return output
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))

    def inspect(self, arguments: object) -> dict[str, object]:
        try:
            value = self._mapping(arguments)
            self._validate("InspectCall", value)
            result = self._engine.inspect(InspectCall(self._mapping(value["handle"])))
            output = result.as_contract()
            self._validate_result(output)
            return output
        except (ContractError, KeyError, TypeError, ValueError) as error:
            return self._rejected("INTERFACE.INVALID_ARGUMENTS", "invalid", str(error))

    def _validate(self, definition: str, value: object) -> None:
        validate(
            self._schema,
            self._schema["$defs"][definition],
            value,
            "$arguments",
        )

    def _validate_result(self, value: dict[str, object]) -> None:
        definition = {
            "route-result": "RouteResult",
            "read-result": "ReadResult",
            "related-result": "RelatedResult",
            "snapshot-inspection-result": "SnapshotInspectionResult",
            "policy-inspection-result": "PolicyInspectionResult",
            "relationship-inspection-result": "RelationshipInspectionResult",
            "navigation-inspection-result": "NavigationInspectionResult",
            "pending-result": "PendingResult",
            "complete-result": "CompleteResult",
            "analysis-state": "AnalysisState",
            "rejected-result": "RejectedResult",
        }[str(value["kind"])]
        self._validate(definition, value)

    @classmethod
    def _analysis_request(cls, value: Mapping[str, object]) -> AnalysisRequest:
        return AnalysisRequest(
            cls._mapping(value["base_snapshot"]),
            cls._mapping(value["proposed_snapshot"]),
            tuple(cls._change(cls._mapping(item)) for item in value["changes"]),
            tuple(
                SemanticProposal(
                    str(item["policy"]),
                    item["accepted_semantic_revision"],
                    int(item["proposed_semantic_revision"]),
                    str(item["intent"]),
                    str(item["structural_digest"]),
                )
                for raw in value["semantic_proposals"]
                for item in (cls._mapping(raw),)
            ),
            cls._optional_mapping(value.get("prior_analysis")),
            int(value["contract_version"]),
        )

    @classmethod
    def _change(cls, value: Mapping[str, object]) -> ChangeDescriptor:
        return ChangeDescriptor(
            ChangeKind(str(value["kind"])),
            tuple(str(item) for item in value["accepted_ids"]),
            tuple(str(item) for item in value["proposed_ids"]),
            cls._scope(cls._mapping(value["scope"])),
            None if "accepted_module" not in value else str(value["accepted_module"]),
            None if "proposed_module" not in value else str(value["proposed_module"]),
        )

    @staticmethod
    def _scope(value: Mapping[str, object]) -> ReviewScope:
        return ReviewScope(
            str(value["kind"]),
            tuple(str(item) for item in value.get("heading_path", [])),
        )

    @classmethod
    def _submission(cls, value: Mapping[str, object]):
        kind = value["kind"]
        if kind == "provide-fact":
            return ProvideFactSubmission(
                cls._mapping(value["requirement"]),
                cls._mapping(value["value"]),
                cls._evidence(value["evidence"]),
            )
        if kind in {"consumer-disposition", "impact-disposition"}:
            selected = (
                ConsumerDispositionSubmission
                if kind == "consumer-disposition"
                else ImpactDispositionSubmission
            )
            return selected(
                str(value["obligation_id"]),
                str(value["result"]),
                str(value["rationale"]),
                cls._evidence(value["evidence"]),
                cls._fingerprint(cls._mapping(value["fingerprint"])),
            )
        if kind == "coverage-attestation":
            attestation = cls._mapping(value["attestation"])
            handle = cls._mapping(attestation["handle"])
            requirement = cls._mapping(attestation["requirement"])
            return CoverageAttestationSubmission(
                str(value["obligation_id"]),
                CoverageAttestation(
                    str(handle["id"]),
                    str(requirement["id"]),
                    str(attestation["conclusion"]),
                    tuple(
                        CoverageEvidence(
                            item.id,
                            item.digest,
                            item.provider_contract,
                            item.provider_contract_version,
                        )
                        for item in cls._evidence(attestation["evidence"])
                    ),
                    tuple(
                        CoverageEvidence(
                            item.id,
                            item.digest,
                            item.provider_contract,
                            item.provider_contract_version,
                        )
                        for item in cls._evidence(
                            attestation["explicit_exclusions"],
                            required=False,
                        )
                    ),
                    str(attestation["rationale"]),
                    str(attestation["auditor_provenance"]),
                    int(attestation["schema_version"]),
                    "agent-submission",
                ),
            )
        raise ValueError(f"unsupported submission kind {kind!r}")

    @classmethod
    def _fingerprint(cls, value: Mapping[str, object]) -> DecisionFingerprint:
        return DecisionFingerprint(
            str(value["decision_kind"]),
            str(value["decision_contract"]),
            tuple(
                DecisionDependency(
                    str(item["class"]),
                    str(item["identity"]),
                    str(item["digest"]),
                )
                for raw in value["dependencies"]
                for item in (cls._mapping(raw),)
            ),
            int(value["schema_version"]),
        )

    @classmethod
    def _evidence(
        cls,
        values: object,
        *,
        required: bool = True,
    ) -> tuple[EvidenceReference, ...]:
        selected = tuple(
            EvidenceReference(
                str(item["id"]),
                str(item["digest"]),
                str(item["provider_contract"]),
                str(item["provider_contract_version"]),
            )
            for raw in values
            for item in (cls._mapping(raw),)
        )
        if required and not selected:
            raise ValueError("evidence is required")
        return selected

    @staticmethod
    def _mapping(value: object) -> dict[str, object]:
        if not isinstance(value, Mapping):
            raise TypeError("structured tool arguments must be an object")
        return dict(value)

    @staticmethod
    def _optional_mapping(value: object) -> dict[str, object] | None:
        if value is None:
            return None
        return AgentToolFacade._mapping(value)

    @staticmethod
    def _rejected(
        code: str,
        outcome: str,
        message: str = "Structured tool arguments do not satisfy the interface contract.",
    ) -> dict[str, object]:
        return {
            "kind": "rejected-result",
            "code": code,
            "outcome": outcome,
            "message": message,
            "details": {},
            "next_operations": [],
        }
