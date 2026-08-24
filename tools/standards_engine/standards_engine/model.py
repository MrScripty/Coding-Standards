from __future__ import annotations

from tools.standards_analysis.standards_analysis import AnalysisState

from ._generated_contract import (
    AnalysisRequest,
    AnalysisContextInspectionResult,
    CertificateInspectionResult,
    ContractInspectionResult,
    ContractResult,
    CoverageAttestationInspectionResult,
    CoverageAuthorityViewInspectionResult,
    CoverageRequirementInspectionResult,
    FactObservationInspectionResult,
    FactRequirementInspectionResult,
    InspectCall,
    NavigationInspectionResult,
    PolicyInspectionResult,
    PrepareCall,
    QueryCall,
    QueryRequest,
    QueryResult,
    ReadRequest,
    ReadResult,
    RejectedResult,
    RelatedRequest,
    RelatedResult,
    ResolveCall,
    RouteRequest,
    RouteResult,
    RelationshipInspectionResult,
    SnapshotInspectionResult,
)


InspectionResult = AnalysisState | ContractInspectionResult


__all__ = (
    "AnalysisRequest",
    "AnalysisContextInspectionResult",
    "CertificateInspectionResult",
    "ContractResult",
    "CoverageAttestationInspectionResult",
    "CoverageAuthorityViewInspectionResult",
    "CoverageRequirementInspectionResult",
    "FactObservationInspectionResult",
    "FactRequirementInspectionResult",
    "InspectCall",
    "InspectionResult",
    "NavigationInspectionResult",
    "PolicyInspectionResult",
    "PrepareCall",
    "QueryCall",
    "QueryRequest",
    "QueryResult",
    "ReadRequest",
    "ReadResult",
    "RejectedResult",
    "RelatedRequest",
    "RelatedResult",
    "ResolveCall",
    "RouteRequest",
    "RouteResult",
    "RelationshipInspectionResult",
    "SnapshotInspectionResult",
)
