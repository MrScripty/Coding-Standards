from __future__ import annotations

import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Literal, TypeAlias

from tools.standards_contracts.standards_contracts import (
    ContractRuntime,
    FrozenMap,
    MISSING,
    MissingValue,
    freeze_json,
    model_as_contract,
)

_SCHEMA = json.loads('{"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"https://coding-standards.local/contracts/standards-engine/a2-v24","title":"Standards Engine A2 contract","description":"Canonical typed contract for snapshot lifecycle, controlled authoring, navigation, inspection, and immutable standards-change analysis.","oneOf":[{"$ref":"#/$defs/CreateSnapshotCall"},{"$ref":"#/$defs/CreateSnapshotResult"},{"$ref":"#/$defs/RejectedResult"},{"$ref":"#/$defs/FindSnapshotsCall"},{"$ref":"#/$defs/FindSnapshotsResult"},{"$ref":"#/$defs/DeleteSnapshotCall"},{"$ref":"#/$defs/DeleteSnapshotResult"},{"$ref":"#/$defs/UndeleteSnapshotCall"},{"$ref":"#/$defs/UndeleteSnapshotResult"},{"$ref":"#/$defs/QueryCall"},{"$ref":"#/$defs/QueryResult"},{"$ref":"#/$defs/PrepareCall"},{"$ref":"#/$defs/PendingResult"},{"$ref":"#/$defs/CompleteResult"},{"$ref":"#/$defs/ResolveCall"},{"$ref":"#/$defs/InspectCall"},{"$ref":"#/$defs/InspectionResult"},{"$ref":"#/$defs/CreateProposalCall"},{"$ref":"#/$defs/CreateProposalResult"},{"$ref":"#/$defs/FindProposalsCall"},{"$ref":"#/$defs/FindProposalsResult"},{"$ref":"#/$defs/ReviseProposalCall"},{"$ref":"#/$defs/ReviseProposalResult"},{"$ref":"#/$defs/QueryProposalCall"},{"$ref":"#/$defs/QueryProposalResult"},{"$ref":"#/$defs/AnalyzeProposalCall"},{"$ref":"#/$defs/ReviewProposalCall"},{"$ref":"#/$defs/ReviewProposalResult"},{"$ref":"#/$defs/ApplyProposalCall"},{"$ref":"#/$defs/ApplyProposalResult"},{"$ref":"#/$defs/ApplicationRecoveryRequiredResult"},{"$ref":"#/$defs/RecoverApplicationCall"},{"$ref":"#/$defs/RecoverApplicationResult"},{"$ref":"#/$defs/VerifyRepositoryCall"},{"$ref":"#/$defs/VerifyRepositoryResult"},{"$ref":"#/$defs/VerifyProposalCall"},{"$ref":"#/$defs/VerifyProposalResult"},{"$ref":"#/$defs/MaintainEvidenceCall"},{"$ref":"#/$defs/MaintainEvidenceResult"},{"$ref":"#/$defs/RouteCall"},{"$ref":"#/$defs/AgentRouteResult"},{"$ref":"#/$defs/ReadCall"},{"$ref":"#/$defs/CompactReadResult"},{"$ref":"#/$defs/ReadResult"},{"$ref":"#/$defs/RelatedCall"},{"$ref":"#/$defs/RelatedResult"},{"$ref":"#/$defs/RoutingFactsCall"},{"$ref":"#/$defs/RoutingFactsResult"},{"$ref":"#/$defs/ProposeCall"},{"$ref":"#/$defs/WorkflowResult"},{"$ref":"#/$defs/ReviseCall"},{"$ref":"#/$defs/AnalyzeCall"},{"$ref":"#/$defs/ResolveWorkflowCall"},{"$ref":"#/$defs/ReviewCall"},{"$ref":"#/$defs/ApplyCall"},{"$ref":"#/$defs/RecoverCall"},{"$ref":"#/$defs/WorkflowStatusCall"},{"$ref":"#/$defs/ResumeCall"}],"$defs":{"NonEmptyString":{"type":"string","minLength":1},"CanonicalId":{"type":"string","pattern":"^[A-Za-z0-9][A-Za-z0-9._:/-]*$"},"EdgeId":{"type":"string","minLength":1},"Digest":{"type":"string","pattern":"^sha256:[0-9a-f]{64}$"},"ObligationId":{"type":"string","pattern":"^obligation:sha256:[0-9a-f]{64}$"},"ImpactTraceId":{"type":"string","pattern":"^impact-trace:sha256:[0-9a-f]{64}$"},"FactRequirementId":{"type":"string","pattern":"^fact-requirement:sha256:[0-9a-f]{64}$"},"ScalarValue":{"oneOf":[{"type":"boolean"},{"type":"integer"},{"type":"string"},{"type":"null"}]},"FactValue":{"oneOf":[{"type":"object","required":["type","state","value"],"properties":{"type":{"const":"boolean"},"state":{"const":"known"},"value":{"type":"boolean"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"state":{"const":"known"},"value":{"type":"null"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["enum","string","canonical-id"]},"state":{"const":"known"},"value":{"type":"string"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["string-set","enum-set"]},"state":{"const":"known"},"value":{"type":"array","items":{"type":"string"},"uniqueItems":true}},"additionalProperties":false},{"type":"object","required":["type","state"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"state":{"enum":["known-absent","unknown"]}},"additionalProperties":false}]},"FactSet":{"type":"object","additionalProperties":{"$ref":"#/$defs/FactValue"}},"StructuredScope":{"type":"object","required":["kind","heading_path"],"properties":{"kind":{"const":"structured"},"heading_path":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/NonEmptyString"}}},"additionalProperties":false},"WholeArtifactScope":{"type":"object","required":["kind"],"properties":{"kind":{"const":"whole-artifact"}},"additionalProperties":false},"ReviewScope":{"oneOf":[{"$ref":"#/$defs/StructuredScope"},{"$ref":"#/$defs/WholeArtifactScope"}]},"AllExpression":{"type":"object","required":["operator","expressions"],"properties":{"operator":{"const":"all"},"expressions":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ApplicabilityExpression"}}},"additionalProperties":false},"AnyExpression":{"type":"object","required":["operator","expressions"],"properties":{"operator":{"const":"any"},"expressions":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ApplicabilityExpression"}}},"additionalProperties":false},"NotExpression":{"type":"object","required":["operator","expression"],"properties":{"operator":{"const":"not"},"expression":{"$ref":"#/$defs/ApplicabilityExpression"}},"additionalProperties":false},"EqualsExpression":{"type":"object","required":["operator","fact","value"],"properties":{"operator":{"const":"equals"},"fact":{"$ref":"#/$defs/CanonicalId"},"value":{"$ref":"#/$defs/ScalarValue"}},"additionalProperties":false},"InExpression":{"type":"object","required":["operator","fact","values"],"properties":{"operator":{"const":"in"},"fact":{"$ref":"#/$defs/CanonicalId"},"values":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ScalarValue"}}},"additionalProperties":false},"ContainsExpression":{"type":"object","required":["operator","fact","value"],"properties":{"operator":{"const":"contains"},"fact":{"$ref":"#/$defs/CanonicalId"},"value":{"$ref":"#/$defs/ScalarValue"}},"additionalProperties":false},"ExistsExpression":{"type":"object","required":["operator","fact"],"properties":{"operator":{"const":"exists"},"fact":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"AlwaysExpression":{"type":"object","required":["operator"],"properties":{"operator":{"const":"always"}},"additionalProperties":false},"ApplicabilityExpression":{"oneOf":[{"$ref":"#/$defs/AlwaysExpression"},{"$ref":"#/$defs/AllExpression"},{"$ref":"#/$defs/AnyExpression"},{"$ref":"#/$defs/NotExpression"},{"$ref":"#/$defs/EqualsExpression"},{"$ref":"#/$defs/InExpression"},{"$ref":"#/$defs/ContainsExpression"},{"$ref":"#/$defs/ExistsExpression"}]},"GeneralSelectionReason":{"type":"object","required":["kind"],"properties":{"kind":{"enum":["routing-fact","requires","specializes","changed-policy","question","audit-coverage","unmapped-normative-change","structured-scope-analysis-unsupported"]},"source":{"$ref":"#/$defs/CanonicalId"},"fact":{"$ref":"#/$defs/CanonicalId"},"edge":{"$ref":"#/$defs/EdgeId"},"question":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"PolicyImpactSelectionReason":{"type":"object","required":["kind","source","edge","relation","evidence_owner","traces"],"properties":{"kind":{"const":"policy-impact-edge"},"source":{"$ref":"#/$defs/CanonicalId"},"edge":{"$ref":"#/$defs/EdgeId"},"relation":{"$ref":"#/$defs/CanonicalId"},"evidence_owner":{"$ref":"#/$defs/CanonicalId"},"traces":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ImpactTraceReference"}}},"additionalProperties":false},"SelectionReason":{"oneOf":[{"$ref":"#/$defs/GeneralSelectionReason"},{"$ref":"#/$defs/PolicyImpactSelectionReason"}]},"ImpactTraceReference":{"type":"object","required":["id","graph","applicability"],"properties":{"id":{"$ref":"#/$defs/ImpactTraceId"},"graph":{"enum":["accepted","proposed"]},"applicability":{"enum":["true","false","unknown"]}},"additionalProperties":false},"ConsumerReviewObligationReadingReason":{"type":"object","required":["kind","obligation"],"properties":{"kind":{"const":"consumer-review-obligation"},"obligation":{"$ref":"#/$defs/ObligationId"}},"additionalProperties":false},"RoutingBaseReadingReason":{"type":"object","required":["kind","projection"],"properties":{"kind":{"const":"routing-base"},"projection":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"RoutingRuleReadingReason":{"type":"object","required":["kind","rule","facts"],"properties":{"kind":{"const":"routing-rule"},"rule":{"$ref":"#/$defs/CanonicalId"},"facts":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"RequiresReadingReason":{"type":"object","required":["kind","edge","source"],"properties":{"kind":{"const":"requires"},"edge":{"$ref":"#/$defs/EdgeId"},"source":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"SpecializesReadingReason":{"type":"object","required":["kind","edge","source"],"properties":{"kind":{"const":"specializes"},"edge":{"$ref":"#/$defs/EdgeId"},"source":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"ReadingPlanReason":{"oneOf":[{"$ref":"#/$defs/ConsumerReviewObligationReadingReason"},{"$ref":"#/$defs/RoutingBaseReadingReason"},{"$ref":"#/$defs/RoutingRuleReadingReason"},{"$ref":"#/$defs/RequiresReadingReason"},{"$ref":"#/$defs/SpecializesReadingReason"}]},"ReadingPlanEntry":{"type":"object","required":["target","scope","authority","reasons","state"],"properties":{"target":{"$ref":"#/$defs/CanonicalId"},"scope":{"$ref":"#/$defs/ReviewScope"},"authority":{"enum":["normative","projection","contextual","evidence"]},"reasons":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ReadingPlanReason"}},"state":{"enum":["selected","conditional","unresolved"]}},"additionalProperties":false},"RouteRequest":{"type":"object","required":["kind","facts"],"properties":{"kind":{"const":"route"},"facts":{"$ref":"#/$defs/FactSet"}},"additionalProperties":false},"ReadRequest":{"type":"object","required":["kind","target"],"properties":{"kind":{"const":"read"},"target":{"$ref":"#/$defs/CanonicalId"},"include_routing":{"type":"boolean"},"include_coverage":{"type":"boolean","description":"Include current repository attestation status for registered policy units in this read scope."}},"additionalProperties":false},"RelatedRequest":{"type":"object","required":["kind","target","groups","direction","transitive"],"properties":{"kind":{"const":"related"},"target":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"direction":{"enum":["incoming","outgoing","both"]},"transitive":{"type":"boolean","default":false}},"additionalProperties":false},"QueryRequest":{"oneOf":[{"$ref":"#/$defs/RouteRequest"},{"$ref":"#/$defs/ReadRequest"},{"$ref":"#/$defs/RelatedRequest"}]},"PolicyUnitDeclaration":{"type":"object","required":["kind","id","module","heading_path","semantic_revision","lifecycle"],"properties":{"kind":{"const":"policy-unit"},"id":{"$ref":"#/$defs/CanonicalId"},"module":{"$ref":"#/$defs/CanonicalId"},"heading_path":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/NonEmptyString"}},"semantic_revision":{"type":"integer","minimum":1},"lifecycle":{"const":"active"},"aliases":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"predecessors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"successors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"CanonicalModuleDeclaration":{"type":"object","required":["kind","id","role","level","applies_when","does_not_apply_when","requires","specializes","verification"],"properties":{"kind":{"const":"canonical-module"},"id":{"$ref":"#/$defs/CanonicalId"},"role":{"enum":["core","router","workflow","profile","topic","reference"]},"level":{"enum":["MUST","SHOULD","PROFILE","REFERENCE"]},"applies_when":{"$ref":"#/$defs/NonEmptyString"},"does_not_apply_when":{"$ref":"#/$defs/NonEmptyString"},"requires":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"specializes":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"verification":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PolicyRelationshipInspection":{"type":"object","required":["relationship_kind","applicability","source_scope","consumer_scope","propagation","evidence_owner","rationale"],"properties":{"relationship_kind":{"enum":["normative-consumer","router-projection","prompt-projection","template-projection","reference-projection","fixture-projection","enforcement-suite-projection","documentation-projection","implementation-projection"]},"applicability":{"$ref":"#/$defs/ApplicabilityExpression"},"source_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"consumer_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"propagation":{"const":"source-to-consumer"},"evidence_owner":{"$ref":"#/$defs/CanonicalId"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"SemanticProposal":{"type":"object","required":["policy","accepted_semantic_revision","proposed_semantic_revision","intent","structural_digest"],"properties":{"policy":{"$ref":"#/$defs/CanonicalId"},"accepted_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"proposed_semantic_revision":{"type":"integer","minimum":1},"intent":{"$ref":"#/$defs/NonEmptyString"},"structural_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"ChangeDescriptor":{"type":"object","required":["kind","accepted_ids","proposed_ids","scope"],"properties":{"kind":{"enum":["module","modification","addition","removal","move","split","merge"]},"accepted_ids":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"proposed_ids":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"scope":{"$ref":"#/$defs/ReviewScope"},"accepted_module":{"$ref":"#/$defs/CanonicalId"},"proposed_module":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"ChangedPolicyUnit":{"type":"object","required":["policy","change_kind","classification","accepted_representation_digest","proposed_representation_digest","accepted_structural_digest","proposed_structural_digest","accepted_semantic_revision","proposed_semantic_revision","semantic_state","scope"],"properties":{"policy":{"$ref":"#/$defs/CanonicalId"},"change_kind":{"enum":["modification","addition","removal","move","split-predecessor","split-successor","merge-predecessor","merge-successor"]},"classification":{"enum":["unchanged","representation-only-candidate","possibly-semantically-changed","semantically-changed","unresolved"]},"accepted_representation_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"proposed_representation_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"accepted_structural_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"proposed_structural_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"accepted_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"proposed_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"semantic_state":{"enum":["accepted-unchanged","proposed","removed","unresolved"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"Question":{"type":"object","required":["id","kind","prompt","state","permitted_answers"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"kind":{"enum":["applicability-fact","normative-classification","identity-resolution","scope-resolution"]},"prompt":{"$ref":"#/$defs/NonEmptyString"},"state":{"enum":["required","answered","blocked"]},"permitted_answers":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/NonEmptyString"}}},"additionalProperties":false},"ConsumerReviewContract":{"type":"object","required":["kind","id","version","permitted_dispositions","evidence_contract","authorization_capability","semantics"],"properties":{"kind":{"const":"consumer-review-contract"},"id":{"$ref":"#/$defs/CanonicalId"},"version":{"type":"integer","minimum":1},"permitted_dispositions":{"type":"array","minItems":1,"uniqueItems":true,"items":{"enum":["updated","reviewed-no-change","not-applicable","blocked"]}},"evidence_contract":{"$ref":"#/$defs/CanonicalId"},"authorization_capability":{"$ref":"#/$defs/CanonicalId"},"semantics":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"DecisionDependency":{"type":"object","required":["class","identity","digest"],"properties":{"class":{"enum":["policy-unit","semantic-revision","structure","representation","module-locator","applicability-fact","relationship","audit","exception","evidence","provider-contract","applicability-contract","analysis-contract"]},"identity":{"$ref":"#/$defs/NonEmptyString"},"digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"DecisionFingerprint":{"type":"object","required":["decision_kind","decision_contract","schema_version","dependencies"],"properties":{"decision_kind":{"$ref":"#/$defs/CanonicalId"},"decision_contract":{"$ref":"#/$defs/CanonicalId"},"schema_version":{"const":1},"dependencies":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/DecisionDependency"}}},"additionalProperties":false},"FactValueContract":{"type":"object","required":["type","states","nullable"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"states":{"const":["known","known-absent"]},"nullable":{"type":"boolean"},"values":{"type":"array","minItems":1,"uniqueItems":true,"items":{"type":"string"}}},"additionalProperties":false},"EvidenceReference":{"type":"object","required":["id","digest","provider_contract","provider_contract_version"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"digest":{"$ref":"#/$defs/Digest"},"provider_contract":{"$ref":"#/$defs/CanonicalId"},"provider_contract_version":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"CompletionProof":{"type":"object","required":["required_coverage_subjects","certificate_subjects","reached_consumer_obligations","disposition_obligations","required_fact_requirements","observed_fact_requirements","non_consumer_obligations_resolved","applicability_resolved","authorization_valid","evidence_valid"],"properties":{"required_coverage_subjects":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"certificate_subjects":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"reached_consumer_obligations":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/ObligationId"}},"disposition_obligations":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/ObligationId"}},"required_fact_requirements":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/FactRequirementId"}},"observed_fact_requirements":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/FactRequirementId"}},"non_consumer_obligations_resolved":{"const":true},"applicability_resolved":{"const":true},"authorization_valid":{"const":true},"evidence_valid":{"const":true}},"additionalProperties":false},"Timestamp":{"type":"integer","minimum":0},"SnapshotId":{"type":"string","pattern":"^snapshot:v1:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"},"AnalysisId":{"type":"string","pattern":"^analysis:sha256:[0-9a-f]{64}$"},"ProposalId":{"type":"string","pattern":"^proposal:v1:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"},"ProposalRevisionId":{"type":"string","pattern":"^proposal-revision:sha256:[0-9a-f]{64}$"},"ReadinessId":{"type":"string","pattern":"^readiness:sha256:[0-9a-f]{64}$"},"ApplicationId":{"type":"string","pattern":"^application:sha256:[0-9a-f]{64}$"},"ChildId":{"type":"string","pattern":"^sha256:[0-9a-f]{64}$"},"AuthorizationId":{"type":"string","pattern":"^authorization:sha256:[0-9a-f]{64}$"},"SnapshotHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"snapshot-handle"},"id":{"$ref":"#/$defs/SnapshotId"},"schema_version":{"const":5}},"additionalProperties":false},"AnalysisHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"analysis-handle"},"id":{"$ref":"#/$defs/AnalysisId"},"schema_version":{"const":6}},"additionalProperties":false},"ProposalHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"proposal-handle"},"id":{"$ref":"#/$defs/ProposalId"},"schema_version":{"const":1}},"additionalProperties":false},"ProposalRevisionHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"proposal-revision-handle"},"id":{"$ref":"#/$defs/ProposalRevisionId"},"schema_version":{"const":1}},"additionalProperties":false},"ReadinessHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"readiness-handle"},"id":{"$ref":"#/$defs/ReadinessId"},"schema_version":{"const":1}},"additionalProperties":false},"ApplicationHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"application-handle"},"id":{"$ref":"#/$defs/ApplicationId"},"schema_version":{"const":1}},"additionalProperties":false},"SnapshotChildHandle":{"type":"object","required":["kind","snapshot","child_kind","child_id","schema_version"],"properties":{"kind":{"const":"snapshot-child-handle"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"child_kind":{"enum":["policy","relationship"]},"child_id":{"$ref":"#/$defs/NonEmptyString"},"schema_version":{"const":5}},"additionalProperties":false},"AnalysisChildHandle":{"type":"object","required":["kind","analysis","child_kind","child_id","schema_version"],"properties":{"kind":{"const":"analysis-child-handle"},"analysis":{"$ref":"#/$defs/AnalysisHandle"},"child_kind":{"enum":["context","fact-requirement","fact-observation","obligation","coverage-requirement","coverage-certificate"]},"child_id":{"$ref":"#/$defs/ChildId"},"schema_version":{"const":6}},"additionalProperties":false},"AnalysisMaterialHandle":{"oneOf":[{"$ref":"#/$defs/SnapshotHandle"},{"$ref":"#/$defs/ProposalRevisionHandle"}]},"InspectableHandle":{"oneOf":[{"$ref":"#/$defs/SnapshotHandle"},{"$ref":"#/$defs/AnalysisHandle"},{"$ref":"#/$defs/SnapshotChildHandle"},{"$ref":"#/$defs/AnalysisChildHandle"}]},"ActiveSnapshotSummary":{"type":"object","required":["snapshot","lifecycle","source_revision","created_at"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"lifecycle":{"const":"active"},"source_revision":{"$ref":"#/$defs/NonEmptyString"},"created_at":{"$ref":"#/$defs/Timestamp"}},"additionalProperties":false},"QuarantinedSnapshotSummary":{"type":"object","required":["snapshot","lifecycle","source_revision","created_at","purge_deadline"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"lifecycle":{"const":"quarantined"},"source_revision":{"$ref":"#/$defs/NonEmptyString"},"created_at":{"$ref":"#/$defs/Timestamp"},"purge_deadline":{"$ref":"#/$defs/Timestamp"}},"additionalProperties":false},"SnapshotSummary":{"oneOf":[{"$ref":"#/$defs/ActiveSnapshotSummary"},{"$ref":"#/$defs/QuarantinedSnapshotSummary"}]},"CreateSnapshotCall":{"type":"object","required":["kind"],"properties":{"kind":{"const":"create-snapshot"}},"additionalProperties":false},"CreateSnapshotResult":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"create-snapshot-result"},"snapshot":{"$ref":"#/$defs/ActiveSnapshotSummary"}},"additionalProperties":false},"FindSnapshotsCall":{"type":"object","required":["kind"],"properties":{"kind":{"const":"find-snapshots"},"lifecycle":{"enum":["active","quarantined"],"default":"active"},"after":{"$ref":"#/$defs/SnapshotHandle"},"limit":{"type":"integer","minimum":1,"default":50}},"additionalProperties":false},"FindSnapshotsResult":{"type":"object","required":["kind","snapshots"],"properties":{"kind":{"const":"find-snapshots-result"},"snapshots":{"type":"array","items":{"$ref":"#/$defs/SnapshotSummary"}},"continuation":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"StandardsChangePurpose":{"type":"object","required":["summary","rationale","evidence"],"properties":{"summary":{"$ref":"#/$defs/NonEmptyString"},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}}},"additionalProperties":false},"StandardContent":{"type":"object","required":["id","title","role","level","applies_when","does_not_apply_when","verification","body"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"title":{"$ref":"#/$defs/NonEmptyString"},"role":{"enum":["core","router","workflow","profile","topic","reference"]},"level":{"enum":["MUST","SHOULD","PROFILE","REFERENCE"]},"applies_when":{"$ref":"#/$defs/NonEmptyString"},"does_not_apply_when":{"$ref":"#/$defs/NonEmptyString"},"verification":{"$ref":"#/$defs/NonEmptyString"},"body":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"NewPolicyUnit":{"type":"object","required":["id","heading_chain","semantic_revision","intent","aliases","predecessors","successors"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"heading_chain":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/NonEmptyString"}},"semantic_revision":{"const":1},"intent":{"$ref":"#/$defs/NonEmptyString"},"aliases":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"predecessors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"successors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"PreservePolicySemantics":{"type":"object","required":["kind","semantic_revision","intent"],"properties":{"kind":{"const":"preserve"},"semantic_revision":{"type":"integer","minimum":1},"intent":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"ChangePolicySemantics":{"type":"object","required":["kind","accepted_semantic_revision","proposed_semantic_revision","intent"],"properties":{"kind":{"const":"change"},"accepted_semantic_revision":{"type":"integer","minimum":1},"proposed_semantic_revision":{"type":"integer","minimum":1},"intent":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PolicySemanticIntent":{"oneOf":[{"$ref":"#/$defs/PreservePolicySemantics"},{"$ref":"#/$defs/ChangePolicySemantics"}]},"CreateStandardEdit":{"type":"object","required":["kind","standard","requires","specializes","policy_units"],"properties":{"kind":{"const":"create-standard"},"standard":{"$ref":"#/$defs/StandardContent"},"requires":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"specializes":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"policy_units":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/NewPolicyUnit"}}},"additionalProperties":false},"ReviseStandardEdit":{"type":"object","required":["kind","standard"],"properties":{"kind":{"const":"revise-standard"},"standard":{"$ref":"#/$defs/StandardContent"}},"additionalProperties":false},"RevisePolicyUnitEdit":{"type":"object","required":["kind","policy","title","body","semantics"],"properties":{"kind":{"const":"revise-policy-unit"},"policy":{"$ref":"#/$defs/CanonicalId"},"title":{"$ref":"#/$defs/NonEmptyString"},"body":{"$ref":"#/$defs/NonEmptyString"},"semantics":{"$ref":"#/$defs/PolicySemanticIntent"}},"additionalProperties":false},"MovePolicyUnitEdit":{"type":"object","required":["kind","policy","standard","semantics"],"properties":{"kind":{"const":"move-policy-unit"},"policy":{"$ref":"#/$defs/CanonicalId"},"standard":{"$ref":"#/$defs/CanonicalId"},"after_policy":{"$ref":"#/$defs/CanonicalId"},"semantics":{"$ref":"#/$defs/PolicySemanticIntent"}},"additionalProperties":false},"RetirePolicyUnitEdit":{"type":"object","required":["kind","policy","retired_semantic_revision","successors","relationship_dispositions","evidence"],"properties":{"kind":{"const":"retire-policy-unit"},"policy":{"$ref":"#/$defs/CanonicalId"},"retired_semantic_revision":{"type":"integer","minimum":1},"successors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"relationship_dispositions":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/RelationshipDisposition"}},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}}},"additionalProperties":false},"RetireStandardEdit":{"type":"object","required":["kind","standard","successors","relationship_dispositions","evidence"],"properties":{"kind":{"const":"retire-standard"},"standard":{"$ref":"#/$defs/CanonicalId"},"successors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"relationship_dispositions":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/RelationshipDisposition"}},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}}},"additionalProperties":false},"ReplaceStandardRelationshipsEdit":{"type":"object","required":["kind","standard","requires","specializes","rationale"],"properties":{"kind":{"const":"replace-standard-relationships"},"standard":{"$ref":"#/$defs/CanonicalId"},"requires":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"specializes":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"AuthoringTargetHandle":{"type":"object","required":["kind","snapshot","id","schema_version"],"properties":{"kind":{"const":"authoring-target-handle"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"id":{"$ref":"#/$defs/ChildId"},"schema_version":{"const":5}},"additionalProperties":false},"RelationshipConsumer":{"oneOf":[{"$ref":"#/$defs/CanonicalId"},{"$ref":"#/$defs/AuthoringTargetHandle"}]},"PolicyRelationship":{"type":"object","required":["source_policy","consumer","relation","applicability","source_scope","consumer_scope","evidence_owner","rationale"],"properties":{"source_policy":{"$ref":"#/$defs/CanonicalId"},"consumer":{"$ref":"#/$defs/RelationshipConsumer"},"relation":{"enum":["normative-consumer","router-projection","prompt-projection","template-projection","reference-projection","fixture-projection","enforcement-suite-projection","documentation-projection","implementation-projection"]},"applicability":{"$ref":"#/$defs/ApplicabilityExpression"},"source_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"consumer_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"evidence_owner":{"$ref":"#/$defs/CanonicalId"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PutPolicyRelationshipEdit":{"type":"object","required":["kind","relationship"],"properties":{"kind":{"const":"put-policy-relationship"},"relationship":{"$ref":"#/$defs/PolicyRelationship"}},"additionalProperties":false},"RemovePolicyRelationshipEdit":{"type":"object","required":["kind","relationship"],"properties":{"kind":{"const":"remove-policy-relationship"},"relationship":{"$ref":"#/$defs/PolicyRelationship"}},"additionalProperties":false},"ModuleRelationshipKey":{"type":"object","required":["kind","relation","source","target"],"properties":{"kind":{"const":"module-relationship"},"relation":{"enum":["requires","specializes"]},"source":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"PolicyRelationshipKey":{"type":"object","required":["kind","source_policy","consumer","relation"],"properties":{"kind":{"const":"policy-relationship"},"source_policy":{"$ref":"#/$defs/CanonicalId"},"consumer":{"$ref":"#/$defs/RelationshipConsumer"},"relation":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"RelationshipKey":{"oneOf":[{"$ref":"#/$defs/ModuleRelationshipKey"},{"$ref":"#/$defs/PolicyRelationshipKey"}]},"RelationshipDisposition":{"type":"object","required":["relationship","disposition","rationale","evidence"],"properties":{"relationship":{"$ref":"#/$defs/RelationshipKey"},"disposition":{"enum":["remove","retarget"]},"replacement_consumer":{"$ref":"#/$defs/RelationshipConsumer"},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}}},"additionalProperties":false},"StandardEdit":{"oneOf":[{"$ref":"#/$defs/CreateStandardEdit"},{"$ref":"#/$defs/ReviseStandardEdit"},{"$ref":"#/$defs/RevisePolicyUnitEdit"},{"$ref":"#/$defs/MovePolicyUnitEdit"},{"$ref":"#/$defs/RetirePolicyUnitEdit"},{"$ref":"#/$defs/RetireStandardEdit"},{"$ref":"#/$defs/ReplaceStandardRelationshipsEdit"},{"$ref":"#/$defs/PutPolicyRelationshipEdit"},{"$ref":"#/$defs/RemovePolicyRelationshipEdit"},{"$ref":"#/$defs/PutRoutingRuleEdit"},{"$ref":"#/$defs/RemoveRoutingRuleEdit"},{"$ref":"#/$defs/PutRoutingFactEdit"},{"$ref":"#/$defs/RemoveRoutingFactEdit"},{"$ref":"#/$defs/AuditPolicyUnitEdit"}]},"StandardsChangeSet":{"type":"object","required":["purpose","edits"],"properties":{"purpose":{"$ref":"#/$defs/StandardsChangePurpose"},"edits":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/StandardEdit"}}},"additionalProperties":false},"ProposalSummary":{"type":"object","required":["proposal","head_revision"],"properties":{"proposal":{"$ref":"#/$defs/ProposalHandle"},"head_revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"CreateProposalCall":{"type":"object","required":["kind","base_snapshot","change_set"],"properties":{"kind":{"const":"create-proposal"},"base_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"change_set":{"$ref":"#/$defs/StandardsChangeSet"}},"additionalProperties":false},"CreateProposalResult":{"type":"object","required":["kind","proposal","revision"],"properties":{"kind":{"const":"create-proposal-result"},"proposal":{"$ref":"#/$defs/ProposalHandle"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"FindProposalsCall":{"type":"object","required":["kind"],"properties":{"kind":{"const":"find-proposals"},"after":{"$ref":"#/$defs/ProposalHandle"},"limit":{"type":"integer","minimum":1,"default":50}},"additionalProperties":false},"FindProposalsResult":{"type":"object","required":["kind","proposals"],"properties":{"kind":{"const":"find-proposals-result"},"proposals":{"type":"array","items":{"$ref":"#/$defs/ProposalSummary"}},"continuation":{"$ref":"#/$defs/ProposalHandle"}},"additionalProperties":false},"ReviseProposalCall":{"type":"object","required":["kind","expected_revision","change_set"],"properties":{"kind":{"const":"revise-proposal"},"expected_revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"change_set":{"$ref":"#/$defs/StandardsChangeSet"}},"additionalProperties":false},"ReviseProposalResult":{"type":"object","required":["kind","proposal","revision"],"properties":{"kind":{"const":"revise-proposal-result"},"proposal":{"$ref":"#/$defs/ProposalHandle"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"DeleteSnapshotCall":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"delete-snapshot"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"DeleteSnapshotResult":{"type":"object","required":["kind","snapshot","purge_deadline"],"properties":{"kind":{"const":"delete-snapshot-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"purge_deadline":{"$ref":"#/$defs/Timestamp"}},"additionalProperties":false},"UndeleteSnapshotCall":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"undelete-snapshot"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"UndeleteSnapshotResult":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"undelete-snapshot-result"},"snapshot":{"$ref":"#/$defs/ActiveSnapshotSummary"}},"additionalProperties":false},"QueryNextOperation":{"type":"object","required":["operation","request_kind","snapshot"],"properties":{"operation":{"const":"query"},"request_kind":{"enum":["route","read","related"]},"target":{"$ref":"#/$defs/CanonicalId"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"QueryProposalNextOperation":{"type":"object","required":["operation","request_kind","revision"],"properties":{"operation":{"const":"query_proposal"},"request_kind":{"enum":["route","read","related"]},"target":{"$ref":"#/$defs/CanonicalId"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"ResolveNextOperation":{"type":"object","required":["operation","request_kind","analysis"],"properties":{"operation":{"const":"resolve"},"request_kind":{"enum":["provide-fact","consumer-disposition","impact-disposition","coverage-attestation"]},"target":{"$ref":"#/$defs/CanonicalId"},"work":{"$ref":"#/$defs/AnalysisChildHandle"},"analysis":{"$ref":"#/$defs/AnalysisHandle"}},"additionalProperties":false},"InspectNextOperation":{"type":"object","required":["operation","request_kind","handle"],"properties":{"operation":{"const":"inspect"},"request_kind":{"const":"inspect"},"handle":{"$ref":"#/$defs/InspectableHandle"}},"additionalProperties":false},"NextOperation":{"oneOf":[{"$ref":"#/$defs/QueryNextOperation"},{"$ref":"#/$defs/ResolveNextOperation"},{"$ref":"#/$defs/InspectNextOperation"}]},"QueryCall":{"type":"object","required":["snapshot","request"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"request":{"$ref":"#/$defs/QueryRequest"}},"additionalProperties":false},"QueryProposalCall":{"type":"object","required":["revision","request"],"properties":{"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"request":{"$ref":"#/$defs/QueryRequest"}},"additionalProperties":false},"AnalyzeProposalCall":{"type":"object","required":["revision"],"properties":{"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"ReviewDecision":{"type":"object","required":["owner","decision","rationale","evidence"],"properties":{"owner":{"enum":["consumer","impact","audit"]},"decision":{"const":"accept"},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}}},"additionalProperties":false},"ReviewProposalCall":{"type":"object","required":["kind","analysis","decisions"],"properties":{"kind":{"const":"review-proposal"},"analysis":{"$ref":"#/$defs/AnalysisHandle"},"decisions":{"type":"array","minItems":3,"maxItems":3,"uniqueItems":true,"items":{"$ref":"#/$defs/ReviewDecision"}},"prior_readiness":{"$ref":"#/$defs/ReadinessHandle"}},"additionalProperties":false},"ReviewProposalResult":{"type":"object","required":["kind","readiness","revision","status"],"properties":{"kind":{"const":"review-proposal-result"},"readiness":{"$ref":"#/$defs/ReadinessHandle"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"status":{"const":"ready"}},"additionalProperties":false},"ApplyProposalCall":{"type":"object","required":["kind","readiness"],"properties":{"kind":{"const":"apply-proposal"},"readiness":{"$ref":"#/$defs/ReadinessHandle"}},"additionalProperties":false},"ApplyProposalResult":{"type":"object","required":["kind","application","status"],"properties":{"kind":{"const":"apply-proposal-result"},"application":{"$ref":"#/$defs/ApplicationHandle"},"status":{"const":"applied"}},"additionalProperties":false},"RecoverApplicationCall":{"type":"object","required":["kind","readiness"],"properties":{"kind":{"const":"recover-application"},"readiness":{"$ref":"#/$defs/ReadinessHandle"}},"additionalProperties":false},"RecoverApplicationResult":{"type":"object","required":["kind","application","status"],"properties":{"kind":{"const":"recover-application-result"},"application":{"$ref":"#/$defs/ApplicationHandle"},"status":{"const":"applied"}},"additionalProperties":false},"ApplicationRecoveryRequiredResult":{"type":"object","required":["kind","application","status","code","outcome","message"],"properties":{"kind":{"const":"application-recovery-required-result"},"application":{"$ref":"#/$defs/ApplicationHandle"},"status":{"const":"recovery-required"},"code":{"enum":["APPLICATION.PUBLICATION_UNAVAILABLE","APPLICATION.OBSERVATION_UNAVAILABLE","APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE","APPLICATION.RECOVERY_TARGET_UNCERTAIN","APPLICATION.RECOVERY_TARGET_DIVERGED"]},"outcome":{"const":"unavailable"},"message":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PolicySummary":{"type":"object","required":["handle","authority","scope"],"properties":{"handle":{"$ref":"#/$defs/SnapshotChildHandle"},"authority":{"enum":["normative","projection","contextual","evidence"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"RelationshipSummary":{"type":"object","required":["handle","source","target","relation","groups","direction","traversal_eligible","applicability"],"properties":{"handle":{"$ref":"#/$defs/SnapshotChildHandle"},"source":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"},"relation":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"minItems":1,"uniqueItems":true},"direction":{"enum":["incoming","outgoing"]},"traversal_eligible":{"type":"boolean"},"applicability":{"enum":["true","false","unknown","not-declared"]}},"additionalProperties":false},"ProposalPolicySummary":{"type":"object","required":["id","authority","scope"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"authority":{"enum":["normative","projection","contextual","evidence"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"ProposalRelationshipSummary":{"type":"object","required":["source","target","relation","groups","direction","traversal_eligible","applicability"],"properties":{"source":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"},"relation":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"minItems":1,"uniqueItems":true},"direction":{"enum":["incoming","outgoing"]},"traversal_eligible":{"type":"boolean"},"applicability":{"enum":["true","false","unknown","not-declared"]}},"additionalProperties":false},"RouteResult":{"type":"object","required":["kind","snapshot","reading_plan","unresolved_questions","next_operations"],"properties":{"kind":{"const":"route-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"unresolved_questions":{"type":"array","items":{"$ref":"#/$defs/Question"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"ReadResult":{"type":"object","required":["kind","snapshot","policy","content","requires","specializes","related","next_operations"],"properties":{"kind":{"const":"read-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"policy":{"$ref":"#/$defs/PolicySummary"},"content":{"type":"string"},"requires":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"specializes":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"related":{"type":"array","items":{"$ref":"#/$defs/RelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"},"routing":{"$ref":"#/$defs/RoutingConfiguration"},"coverage":{"$ref":"#/$defs/ReadCoverage"}},"additionalProperties":false},"PolicyUnitMapping":{"type":"object","required":["state","policy_units"],"properties":{"state":{"enum":["exact-policy-unit","policy-units-present","incomplete"]},"reason":{"const":"no-policy-units"},"policy_units":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true}},"additionalProperties":false},"RelatedResult":{"type":"object","required":["kind","snapshot","target","policy_unit_mapping","relationships","next_operations"],"properties":{"kind":{"const":"related-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"target":{"$ref":"#/$defs/CanonicalId"},"authoring_target":{"$ref":"#/$defs/AuthoringTargetHandle"},"policy_unit_mapping":{"$ref":"#/$defs/PolicyUnitMapping"},"relationships":{"type":"array","items":{"$ref":"#/$defs/RelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"QueryResult":{"oneOf":[{"$ref":"#/$defs/RouteResult"},{"$ref":"#/$defs/ReadResult"},{"$ref":"#/$defs/RelatedResult"}]},"ProposalRouteResult":{"type":"object","required":["kind","revision","reading_plan","unresolved_questions","next_operations"],"properties":{"kind":{"const":"proposal-route-result"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"unresolved_questions":{"type":"array","items":{"$ref":"#/$defs/Question"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/QueryProposalNextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"ProposalReadResult":{"type":"object","required":["kind","revision","policy","content","requires","specializes","related","next_operations"],"properties":{"kind":{"const":"proposal-read-result"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"policy":{"$ref":"#/$defs/ProposalPolicySummary"},"content":{"type":"string"},"requires":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"specializes":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"related":{"type":"array","items":{"$ref":"#/$defs/ProposalRelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/QueryProposalNextOperation"}},"summary":{"type":"string"},"routing":{"$ref":"#/$defs/RoutingConfiguration"},"coverage":{"$ref":"#/$defs/ReadCoverage"}},"additionalProperties":false},"ProposalRelatedResult":{"type":"object","required":["kind","revision","target","policy_unit_mapping","relationships","next_operations"],"properties":{"kind":{"const":"proposal-related-result"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"target":{"$ref":"#/$defs/CanonicalId"},"authoring_target":{"$ref":"#/$defs/AuthoringTargetHandle"},"policy_unit_mapping":{"$ref":"#/$defs/PolicyUnitMapping"},"relationships":{"type":"array","items":{"$ref":"#/$defs/ProposalRelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/QueryProposalNextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"QueryProposalResult":{"oneOf":[{"$ref":"#/$defs/ProposalRouteResult"},{"$ref":"#/$defs/ProposalReadResult"},{"$ref":"#/$defs/ProposalRelatedResult"}]},"AnalysisRequest":{"type":"object","required":["kind","base_snapshot","proposed_snapshot","changes","semantic_proposals","contract_version"],"properties":{"kind":{"const":"analysis-request"},"base_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"proposed_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"},"minItems":1},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"},"uniqueItems":true},"prior_analysis":{"$ref":"#/$defs/AnalysisHandle"},"contract_version":{"const":5}},"additionalProperties":false},"PrepareCall":{"type":"object","required":["request"],"properties":{"request":{"$ref":"#/$defs/AnalysisRequest"}},"additionalProperties":false},"AnalysisContext":{"type":"object","required":["kind","handle","subjects","changes","semantic_proposals"],"properties":{"kind":{"const":"analysis-context"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"subjects":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"},"uniqueItems":true},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"},"minItems":1,"uniqueItems":true},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"},"uniqueItems":true}},"additionalProperties":false},"AuthorizationReference":{"type":"object","required":["id","issuer","capability","authority_digest"],"properties":{"id":{"$ref":"#/$defs/AuthorizationId"},"issuer":{"$ref":"#/$defs/CanonicalId"},"capability":{"$ref":"#/$defs/CanonicalId"},"authority_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"ProviderReference":{"type":"object","required":["id","contract","contract_version","input_digest"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"contract":{"$ref":"#/$defs/CanonicalId"},"contract_version":{"$ref":"#/$defs/NonEmptyString"},"input_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"AuthorizationRecord":{"type":"object","required":["reference","issuer_semantic_revision","principal","action","subject_kind","subject_id","authorization_evidence","revocation_authority","revocation_authority_semantic_revision","revocation_evidence"],"properties":{"reference":{"$ref":"#/$defs/AuthorizationReference"},"issuer_semantic_revision":{"type":"integer","minimum":1},"principal":{"$ref":"#/$defs/CanonicalId"},"action":{"$ref":"#/$defs/CanonicalId"},"subject_kind":{"$ref":"#/$defs/CanonicalId"},"subject_id":{"$ref":"#/$defs/NonEmptyString"},"authorization_evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true},"revocation_authority":{"$ref":"#/$defs/CanonicalId"},"revocation_authority_semantic_revision":{"type":"integer","minimum":1},"revocation_evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true}},"additionalProperties":false},"DomainContractReference":{"type":"object","required":["id","version"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"version":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"AnalysisExecutionContractView":{"type":"object","required":["authorization_authority_digest","providers"],"properties":{"authorization_authority_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"providers":{"type":"array","items":{"$ref":"#/$defs/ProviderReference"},"uniqueItems":true}},"additionalProperties":false},"FactRequirement":{"type":"object","required":["kind","handle","fact","fact_semantic_revision","fact_contract_digest","context","value_contract","answer_contract","evidence_contract","authorization_capability"],"properties":{"kind":{"const":"fact-requirement"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"fact":{"$ref":"#/$defs/CanonicalId"},"fact_semantic_revision":{"type":"integer","minimum":1},"fact_contract_digest":{"$ref":"#/$defs/Digest"},"context":{"$ref":"#/$defs/AnalysisChildHandle"},"value_contract":{"$ref":"#/$defs/FactValueContract"},"answer_contract":{"$ref":"#/$defs/CanonicalId"},"evidence_contract":{"$ref":"#/$defs/CanonicalId"},"authorization_capability":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"FactRequirementWork":{"type":"object","required":["requirement","prompt","dependent_programs"],"properties":{"requirement":{"$ref":"#/$defs/FactRequirement"},"prompt":{"$ref":"#/$defs/NonEmptyString"},"dependent_programs":{"type":"array","items":{"$ref":"#/$defs/NonEmptyString"},"minItems":1,"uniqueItems":true}},"additionalProperties":false},"FactObservation":{"type":"object","required":["kind","handle","requirement","value","evidence","authorization"],"properties":{"kind":{"const":"fact-observation"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"value":{"$ref":"#/$defs/FactValue"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true},"authorization":{"$ref":"#/$defs/AuthorizationReference"},"provider":{"$ref":"#/$defs/ProviderReference"}},"additionalProperties":false},"Obligation":{"type":"object","required":["handle","kind","target","scope","reasons","state","permitted_submissions","fingerprint"],"properties":{"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"kind":{"enum":["consumer-review","impact-review","lifecycle-impact-review","audit-coverage","unmapped-normative-change"]},"target":{"$ref":"#/$defs/CanonicalId"},"scope":{"$ref":"#/$defs/ReviewScope"},"reasons":{"type":"array","items":{"$ref":"#/$defs/SelectionReason"},"minItems":1,"uniqueItems":true},"state":{"enum":["required","resolved","blocked"]},"applicability":{"enum":["true","false","unknown","not-declared"]},"permitted_submissions":{"type":"array","items":{"enum":["consumer-disposition","impact-disposition","coverage-attestation"]},"minItems":1,"uniqueItems":true},"review_contract":{"$ref":"#/$defs/ConsumerReviewContract"},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"ProvideFactSubmission":{"type":"object","required":["kind","requirement","value","evidence"],"properties":{"kind":{"const":"provide-fact"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"value":{"$ref":"#/$defs/FactValue"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true}},"additionalProperties":false},"ConsumerDispositionSubmission":{"type":"object","required":["kind","obligation","result","rationale","evidence","fingerprint"],"properties":{"kind":{"const":"consumer-disposition"},"obligation":{"$ref":"#/$defs/AnalysisChildHandle"},"result":{"enum":["updated","reviewed-no-change","not-applicable","blocked"]},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"ImpactDispositionSubmission":{"type":"object","required":["kind","obligation","result","rationale","evidence","fingerprint"],"properties":{"kind":{"const":"impact-disposition"},"obligation":{"$ref":"#/$defs/AnalysisChildHandle"},"result":{"enum":["confirmed","resolved-no-impact","requires-change","blocked"]},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"CoverageAttestationClaim":{"type":"object","required":["requirement","conclusion","evidence","explicit_exclusions","rationale","auditor_provenance"],"properties":{"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"conclusion":{"const":"complete"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true},"explicit_exclusions":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"uniqueItems":true},"rationale":{"$ref":"#/$defs/NonEmptyString"},"auditor_provenance":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"CoverageAttestationSubmission":{"type":"object","required":["kind","claim"],"properties":{"kind":{"const":"coverage-attestation"},"claim":{"$ref":"#/$defs/CoverageAttestationClaim"}},"additionalProperties":false},"Submission":{"oneOf":[{"$ref":"#/$defs/ProvideFactSubmission"},{"$ref":"#/$defs/ConsumerDispositionSubmission"},{"$ref":"#/$defs/ImpactDispositionSubmission"},{"$ref":"#/$defs/CoverageAttestationSubmission"}]},"ResolveCall":{"type":"object","required":["analysis","submission"],"properties":{"analysis":{"$ref":"#/$defs/AnalysisHandle"},"submission":{"$ref":"#/$defs/Submission"}},"additionalProperties":false},"CoverageRequirement":{"type":"object","required":["kind","handle","subject","owner","semantic_revision","relationship_kinds","horizon","required_evidence_contract"],"properties":{"kind":{"const":"coverage-requirement"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"subject":{"$ref":"#/$defs/CanonicalId"},"owner":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"relationship_kinds":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"horizon":{"$ref":"#/$defs/CanonicalId"},"required_evidence_contract":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"CoverageAttestation":{"type":"object","required":["kind","requirement","conclusion","evidence","explicit_exclusions","rationale","auditor_provenance","schema_version","authorization"],"properties":{"kind":{"const":"coverage-attestation"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"conclusion":{"const":"complete"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1},"explicit_exclusions":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"}},"rationale":{"$ref":"#/$defs/NonEmptyString"},"auditor_provenance":{"$ref":"#/$defs/NonEmptyString"},"schema_version":{"const":4},"authorization":{"$ref":"#/$defs/AuthorizationReference"}},"additionalProperties":false},"CoverageCertificate":{"type":"object","required":["kind","handle","requirement","subject","owner","semantic_revision","horizon_digest","relationship_digest","evidence_digests","fact_schema_digest"],"properties":{"kind":{"const":"coverage-certificate"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"subject":{"$ref":"#/$defs/CanonicalId"},"owner":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"horizon_digest":{"$ref":"#/$defs/Digest"},"relationship_digest":{"$ref":"#/$defs/Digest"},"evidence_digests":{"type":"array","items":{"$ref":"#/$defs/Digest"},"uniqueItems":true},"fact_schema_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"DispositionRecord":{"type":"object","required":["obligation","kind","result","rationale","evidence","authorization","fingerprint"],"properties":{"obligation":{"$ref":"#/$defs/AnalysisChildHandle"},"kind":{"enum":["consumer-disposition","impact-disposition"]},"result":{"$ref":"#/$defs/NonEmptyString"},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"}},"authorization":{"$ref":"#/$defs/AuthorizationReference"},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"AnalysisState":{"type":"object","required":["kind","handle","base_snapshot","proposed_reference","changes","semantic_proposals","fact_observations","dispositions","coverage_attestations","authorization_records","domain_contracts","execution_contracts","contract_version"],"properties":{"kind":{"const":"analysis-state"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"base_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"proposed_reference":{"$ref":"#/$defs/AnalysisMaterialHandle"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"},"minItems":1,"uniqueItems":true},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"},"uniqueItems":true},"fact_observations":{"type":"array","items":{"$ref":"#/$defs/FactObservation"},"uniqueItems":true},"dispositions":{"type":"array","items":{"$ref":"#/$defs/DispositionRecord"},"uniqueItems":true},"coverage_attestations":{"type":"array","items":{"$ref":"#/$defs/CoverageAttestation"},"uniqueItems":true},"authorization_records":{"type":"array","items":{"$ref":"#/$defs/AuthorizationRecord"},"uniqueItems":true},"domain_contracts":{"type":"array","items":{"$ref":"#/$defs/DomainContractReference"},"minItems":1,"uniqueItems":true},"execution_contracts":{"$ref":"#/$defs/AnalysisExecutionContractView"},"contract_version":{"const":6}},"additionalProperties":false},"PendingResult":{"type":"object","required":["kind","handle","status","context","changes","changed_units","obligations","fact_requirements","reading_plan","next_operations"],"properties":{"kind":{"const":"pending-result"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"status":{"const":"needs-action"},"context":{"$ref":"#/$defs/AnalysisContext"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"}},"changed_units":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"}},"obligations":{"type":"array","items":{"$ref":"#/$defs/Obligation"}},"fact_requirements":{"type":"array","items":{"$ref":"#/$defs/FactRequirementWork"}},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"CompleteResult":{"type":"object","required":["kind","handle","status","context","changes","changed_units","coverage_certificates","fact_observations","dispositions","reading_plan","completion"],"properties":{"kind":{"const":"complete-result"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"status":{"const":"complete"},"context":{"$ref":"#/$defs/AnalysisContext"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"}},"changed_units":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"}},"coverage_certificates":{"type":"array","items":{"$ref":"#/$defs/CoverageCertificate"},"uniqueItems":true},"fact_observations":{"type":"array","items":{"$ref":"#/$defs/FactObservation"},"uniqueItems":true},"dispositions":{"type":"array","items":{"$ref":"#/$defs/DispositionRecord"}},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"completion":{"$ref":"#/$defs/CompletionProof"},"summary":{"type":"string"}},"additionalProperties":false},"RepositoryPath":{"type":"array","items":{"$ref":"#/$defs/NonEmptyString"},"minItems":1},"ProvenanceRecord":{"type":"object","required":["snapshot","path"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"path":{"$ref":"#/$defs/RepositoryPath"}},"additionalProperties":false},"SnapshotInspectionResult":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"snapshot-inspection-result"},"snapshot":{"$ref":"#/$defs/SnapshotSummary"}},"additionalProperties":false},"PolicyInspectionResult":{"type":"object","required":["kind","policy","declaration","representation_digest","structural_digest","provenance"],"properties":{"kind":{"const":"policy-inspection-result"},"policy":{"$ref":"#/$defs/SnapshotChildHandle"},"declaration":{"oneOf":[{"$ref":"#/$defs/CanonicalModuleDeclaration"},{"$ref":"#/$defs/PolicyUnitDeclaration"}]},"representation_digest":{"$ref":"#/$defs/Digest"},"structural_digest":{"$ref":"#/$defs/Digest"},"provenance":{"$ref":"#/$defs/ProvenanceRecord"}},"additionalProperties":false},"RelationshipInspectionResult":{"type":"object","required":["kind","relationship","policy_semantics","provenance"],"properties":{"kind":{"const":"relationship-inspection-result"},"relationship":{"$ref":"#/$defs/RelationshipSummary"},"policy_semantics":{"oneOf":[{"$ref":"#/$defs/PolicyRelationshipInspection"},{"type":"null"}]},"provenance":{"$ref":"#/$defs/ProvenanceRecord"}},"additionalProperties":false},"AnalysisInspectionResult":{"type":"object","required":["kind","state"],"properties":{"kind":{"const":"analysis-inspection-result"},"state":{"$ref":"#/$defs/AnalysisState"}},"additionalProperties":false},"AnalysisChildArtifact":{"oneOf":[{"$ref":"#/$defs/AnalysisContext"},{"$ref":"#/$defs/FactRequirement"},{"$ref":"#/$defs/FactObservation"},{"$ref":"#/$defs/Obligation"},{"$ref":"#/$defs/CoverageRequirement"},{"$ref":"#/$defs/CoverageCertificate"}]},"AnalysisChildInspectionResult":{"type":"object","required":["kind","handle","artifact"],"properties":{"kind":{"const":"analysis-child-inspection-result"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"artifact":{"$ref":"#/$defs/AnalysisChildArtifact"}},"additionalProperties":false},"InspectionResult":{"oneOf":[{"$ref":"#/$defs/SnapshotInspectionResult"},{"$ref":"#/$defs/PolicyInspectionResult"},{"$ref":"#/$defs/RelationshipInspectionResult"},{"$ref":"#/$defs/AnalysisInspectionResult"},{"$ref":"#/$defs/AnalysisChildInspectionResult"}]},"InspectCall":{"type":"object","required":["handle"],"properties":{"handle":{"$ref":"#/$defs/InspectableHandle"}},"additionalProperties":false},"RejectedResult":{"type":"object","required":["kind","code","outcome","message","details","next_operations"],"properties":{"kind":{"const":"rejected-result"},"code":{"$ref":"#/$defs/CanonicalId"},"outcome":{"enum":["invalid","unavailable","unsupported","unauthorized"]},"target":{"$ref":"#/$defs/NonEmptyString"},"message":{"$ref":"#/$defs/NonEmptyString"},"details":{"type":"object","additionalProperties":{"$ref":"#/$defs/ScalarValue"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}}},"additionalProperties":false},"AuthoredRoutingRule":{"type":"object","required":["id","target","when","condition"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"},"when":{"$ref":"#/$defs/ApplicabilityExpression"},"condition":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"AuthoredRoutingFact":{"type":"object","required":["id","semantic_revision","type","nullable","values","aliases","meaning","prompt"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"nullable":{"type":"boolean"},"values":{"type":"array","items":{"type":"string"},"uniqueItems":true},"aliases":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"meaning":{"$ref":"#/$defs/NonEmptyString"},"prompt":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PutRoutingRuleEdit":{"type":"object","required":["kind","rule","rationale"],"properties":{"kind":{"const":"put-routing-rule"},"rule":{"$ref":"#/$defs/AuthoredRoutingRule"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"RemoveRoutingRuleEdit":{"type":"object","required":["kind","rule","rationale"],"properties":{"kind":{"const":"remove-routing-rule"},"rule":{"$ref":"#/$defs/CanonicalId"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PutRoutingFactEdit":{"type":"object","required":["kind","fact","rationale"],"properties":{"kind":{"const":"put-routing-fact"},"fact":{"$ref":"#/$defs/AuthoredRoutingFact"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"RemoveRoutingFactEdit":{"type":"object","required":["kind","fact","rationale"],"properties":{"kind":{"const":"remove-routing-fact"},"fact":{"$ref":"#/$defs/CanonicalId"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"VerificationFailure":{"type":"object","additionalProperties":false,"required":["code","message","suite","check"],"properties":{"code":{"$ref":"#/$defs/NonEmptyString"},"message":{"$ref":"#/$defs/NonEmptyString"},"suite":{"type":["string","null"]},"check":{"type":["string","null"]}}},"VerificationReport":{"type":"object","additionalProperties":false,"required":["passed","exit_code","suites","checks","failures"],"properties":{"passed":{"type":"boolean"},"exit_code":{"enum":[0,1,2,3,4]},"suites":{"type":"integer","minimum":0},"checks":{"type":"integer","minimum":0},"failures":{"type":"array","items":{"$ref":"#/$defs/VerificationFailure"}}}},"VerifyRepositoryCall":{"type":"object","additionalProperties":false,"required":["kind","refresh_verification_inputs"],"properties":{"kind":{"const":"verify-repository"},"refresh_verification_inputs":{"type":"boolean"}}},"VerifyRepositoryResult":{"type":"object","additionalProperties":false,"required":["kind","refreshed_verification_inputs","verification"],"properties":{"kind":{"const":"verify-repository-result"},"refreshed_verification_inputs":{"type":"boolean"},"verification":{"$ref":"#/$defs/VerificationReport"}}},"VerifyProposalCall":{"type":"object","additionalProperties":false,"required":["kind","revision"],"properties":{"kind":{"const":"verify-proposal"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"readiness":{"$ref":"#/$defs/ReadinessHandle"}}},"VerifyProposalResult":{"type":"object","additionalProperties":false,"required":["kind","revision","verification"],"properties":{"kind":{"const":"verify-proposal-result"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"verification":{"$ref":"#/$defs/VerificationReport"},"readiness":{"$ref":"#/$defs/ReadinessHandle"}}},"RoutingConfiguration":{"type":"object","additionalProperties":false,"required":["facts","rules"],"properties":{"facts":{"type":"array","items":{"$ref":"#/$defs/AuthoredRoutingFact"}},"rules":{"type":"array","items":{"$ref":"#/$defs/AuthoredRoutingRule"}}}},"PolicyCoverageStatus":{"type":"object","required":["subject","requirement_id","status"],"properties":{"subject":{"$ref":"#/$defs/CanonicalId"},"requirement_id":{"$ref":"#/$defs/Digest"},"status":{"enum":["current-attestation","review-required"]},"authority":{"$ref":"#/$defs/CoverageAuditAuthority"}},"additionalProperties":false},"ReadCoverage":{"type":"object","description":"Repository attestation status bound to this snapshot or proposal. Empty subjects means no registered policy units in scope, not complete coverage. Analysis-local attestations are not repository certificates.","required":["subjects"],"properties":{"subjects":{"type":"array","items":{"$ref":"#/$defs/PolicyCoverageStatus"}}},"additionalProperties":false},"AuditPolicyUnitEdit":{"type":"object","required":["kind","policy","rationale"],"properties":{"kind":{"const":"audit-policy-unit"},"policy":{"$ref":"#/$defs/CanonicalId"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"CoverageAuditAuthority":{"type":"object","required":["issuer","principal","authorization_id"],"properties":{"issuer":{"$ref":"#/$defs/NonEmptyString"},"principal":{"$ref":"#/$defs/NonEmptyString"},"authorization_id":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"EvidenceCheckRetirement":{"type":"object","additionalProperties":false,"required":["suite","check"],"properties":{"suite":{"type":"string","minLength":1},"check":{"type":"string","minLength":1}}},"EvidenceSuiteDescription":{"type":"object","additionalProperties":false,"required":["suite","description"],"properties":{"suite":{"type":"string","minLength":1},"description":{"type":"string","minLength":1}}},"EvidenceRelationshipUpdate":{"type":"object","additionalProperties":false,"required":["source_policy","consumer","relation","evidence_owner","rationale"],"properties":{"source_policy":{"type":"string","minLength":1},"consumer":{"type":"string","minLength":1},"relation":{"type":"string","minLength":1},"evidence_owner":{"type":"string","minLength":1},"rationale":{"type":"string","minLength":1}}},"EvidenceConsumerRegistration":{"type":"object","additionalProperties":false,"required":["path","artifact_kind","source_policies","relation","evidence_owner","rationale"],"properties":{"path":{"type":"string","minLength":1},"artifact_kind":{"type":"string","enum":["implementation-artifact","fixture"]},"source_policies":{"type":"array","items":{"type":"string","minLength":1},"minItems":1,"uniqueItems":true},"relation":{"type":"string","enum":["implementation-projection","fixture-projection"]},"evidence_owner":{"type":"string","minLength":1},"rationale":{"type":"string","minLength":1}}},"EvidenceMaintenancePlan":{"type":"object","additionalProperties":false,"required":["prune_stale_certificates","retire_suites","retire_checks","retire_inputs","suite_descriptions","replacement_evidence_owner","replacement_evidence_rationale","relationship_updates","consumer_registrations"],"properties":{"prune_stale_certificates":{"type":"boolean"},"retire_suites":{"type":"array","items":{"type":"string","minLength":1},"uniqueItems":true},"retire_checks":{"type":"array","items":{"$ref":"#/$defs/EvidenceCheckRetirement"}},"retire_inputs":{"type":"array","items":{"type":"string","minLength":1},"uniqueItems":true},"suite_descriptions":{"type":"array","items":{"$ref":"#/$defs/EvidenceSuiteDescription"}},"replacement_evidence_owner":{"type":"string","minLength":1},"replacement_evidence_rationale":{"type":"string","minLength":1},"relationship_updates":{"type":"array","items":{"$ref":"#/$defs/EvidenceRelationshipUpdate"}},"consumer_registrations":{"type":"array","items":{"$ref":"#/$defs/EvidenceConsumerRegistration"}},"unregister_policy_subjects":{"type":"array","items":{"type":"string","minLength":1},"uniqueItems":true,"description":"Remove selected review-subject registrations and their source relationships while preserving normative Markdown."}}},"MaintainEvidenceCall":{"type":"object","additionalProperties":false,"required":["kind","expected_revision","evidence","plan","apply"],"properties":{"kind":{"const":"maintain-evidence"},"expected_revision":{"type":"string","minLength":1},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1},"plan":{"$ref":"#/$defs/EvidenceMaintenancePlan"},"apply":{"type":"boolean"}}},"MaintainEvidenceResult":{"type":"object","additionalProperties":false,"required":["kind","applied","changed_files","removed_files","verification"],"properties":{"kind":{"const":"maintain-evidence-result"},"applied":{"type":"boolean"},"changed_files":{"type":"array","items":{"type":"string","minLength":1}},"removed_files":{"type":"array","items":{"type":"string","minLength":1}},"verification":{"$ref":"#/$defs/VerificationReport"}}},"RouteCall":{"type":"object","required":["facts"],"properties":{"facts":{"$ref":"#/$defs/FactSet"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"ReadCall":{"type":"object","required":["target"],"properties":{"target":{"$ref":"#/$defs/CanonicalId"},"include_routing":{"type":"boolean"},"include_coverage":{"type":"boolean","description":"Include current repository attestation status for registered policy units in this read scope."},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"detail":{"enum":["compact","full"],"description":"Compact preserves exact policy and essential authority; full includes all relationship rows."}},"additionalProperties":false},"RelatedCall":{"type":"object","required":["target","groups","direction","transitive"],"properties":{"target":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"direction":{"enum":["incoming","outgoing","both"]},"transitive":{"type":"boolean","default":false},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"CompactReadResult":{"type":"object","required":["kind","snapshot","policy","content","requires","specializes","next_operations","detail"],"properties":{"kind":{"const":"compact-read-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"policy":{"$ref":"#/$defs/PolicySummary"},"content":{"type":"string"},"requires":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"specializes":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"},"routing":{"$ref":"#/$defs/RoutingConfiguration"},"coverage":{"$ref":"#/$defs/ReadCoverage"},"detail":{"const":"compact"}},"additionalProperties":false},"RoutingFactsCall":{"type":"object","additionalProperties":false,"required":[],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"}}},"RoutingFactsResult":{"type":"object","additionalProperties":false,"required":["kind","snapshot","facts"],"properties":{"kind":{"const":"routing-facts-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"facts":{"type":"array","items":{"$ref":"#/$defs/AuthoredRoutingFact"}}}},"RoutingQuestion":{"type":"object","additionalProperties":false,"required":["id","kind","prompt","state","fact"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"kind":{"const":"applicability-fact"},"prompt":{"$ref":"#/$defs/NonEmptyString"},"state":{"const":"required"},"fact":{"$ref":"#/$defs/AuthoredRoutingFact"}}},"RoutingRuleExplanation":{"type":"object","additionalProperties":false,"required":["id","target","when","state"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"},"when":{"$ref":"#/$defs/ApplicabilityExpression"},"state":{"enum":["selected","unresolved"]}}},"AgentRouteResult":{"type":"object","required":["kind","snapshot","reading_plan","unresolved_questions","next_operations","facts","rules"],"properties":{"kind":{"const":"agent-route-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"unresolved_questions":{"type":"array","items":{"$ref":"#/$defs/RoutingQuestion"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"},"facts":{"$ref":"#/$defs/FactSet"},"rules":{"type":"array","items":{"$ref":"#/$defs/RoutingRuleExplanation"}}},"additionalProperties":false},"WorkflowContext":{"oneOf":[{"$ref":"#/$defs/ProposalRevisionHandle"},{"$ref":"#/$defs/AnalysisHandle"},{"$ref":"#/$defs/ReadinessHandle"}]},"ProposeCall":{"type":"object","additionalProperties":false,"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"change_set":{"$ref":"#/$defs/StandardsChangeSet"}},"required":["change_set"]},"ReviseCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"},"change_set":{"$ref":"#/$defs/StandardsChangeSet"}},"required":["context","change_set"]},"AnalyzeCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"}},"required":["context"]},"ResolveWorkflowCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"},"submission":{"$ref":"#/$defs/Submission"}},"required":["context","submission"]},"ReviewCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"},"decisions":{"type":"array","minItems":3,"maxItems":3,"uniqueItems":true,"items":{"$ref":"#/$defs/ReviewDecision"}}},"required":["context","decisions"]},"ApplyCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"}},"required":["context"]},"RecoverCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"}},"required":["context"]},"WorkflowStatusCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"}},"required":["context"]},"ResumeCall":{"type":"object","additionalProperties":false,"properties":{"context":{"$ref":"#/$defs/WorkflowContext"}},"required":["context"]},"WorkflowContinuation":{"type":"object","additionalProperties":false,"properties":{"operation":{"enum":["revise","analyze","resolve_workflow","review","apply","recover","workflow_status","resume"]},"context":{"$ref":"#/$defs/WorkflowContext"},"required_inputs":{"type":"array","uniqueItems":true,"items":{"enum":["change_set","submission","decisions"]}}},"required":["operation","context","required_inputs"]},"WorkflowOutcome":{"oneOf":[{"$ref":"#/$defs/CreateProposalResult"},{"$ref":"#/$defs/ReviseProposalResult"},{"$ref":"#/$defs/PendingResult"},{"$ref":"#/$defs/CompleteResult"},{"$ref":"#/$defs/ReviewProposalResult"},{"$ref":"#/$defs/ApplyProposalResult"},{"$ref":"#/$defs/ApplicationRecoveryRequiredResult"},{"$ref":"#/$defs/RecoverApplicationResult"},{"$ref":"#/$defs/RejectedResult"}]},"WorkflowResult":{"type":"object","additionalProperties":false,"properties":{"kind":{"const":"workflow-result"},"context":{"$ref":"#/$defs/WorkflowContext"},"proposal":{"$ref":"#/$defs/ProposalHandle"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"status":{"enum":["draft","needs-action","complete","requires-change","ready","recovery-required","applied","rejected","stale"]},"next_operations":{"type":"array","items":{"$ref":"#/$defs/WorkflowContinuation"}},"outcome":{"$ref":"#/$defs/WorkflowOutcome"}},"required":["kind","context","proposal","revision","status","next_operations"]}}}')
DEFINITION_METADATA = freeze_json({'ActiveSnapshotSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'created_at': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AgentRouteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'unresolved_questions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rules': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AllExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expressions': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AlwaysExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisChildArtifact': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisChildHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisChildInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'artifact': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisContext': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisExecutionContractView': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'authorization_authority_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'providers': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisMaterialHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'base_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prior_analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisState': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'base_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_reference': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_observations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_attestations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_records': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'domain_contracts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'execution_contracts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalyzeCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalyzeProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnyExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expressions': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplicabilityExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ApplicationHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplicationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ApplicationRecoveryRequiredResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'application': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'code': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'outcome': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'message': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplyCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplyProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplyProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'application': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuditPolicyUnitEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthoredRoutingFact': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'type': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'nullable': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'values': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'aliases': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'meaning': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthoredRoutingRule': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'condition': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthoringTargetHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthorizationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AuthorizationRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'reference': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'issuer_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'principal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'action': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revocation_authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revocation_authority_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revocation_evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthorizationReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'issuer': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'capability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CanonicalId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CanonicalModuleDeclaration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'role': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'level': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applies_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'does_not_apply_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'verification': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChangeDescriptor': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_ids': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_ids': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_module': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_module': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChangePolicySemantics': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'intent': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChangedPolicyUnit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'change_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'classification': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChildId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CompactReadResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'routing': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'detail': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CompleteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changed_units': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_certificates': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_observations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'completion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CompletionProof': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'required_coverage_subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'certificate_subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reached_consumer_obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'disposition_obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'required_fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'observed_fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'non_consumer_obligations_resolved': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability_resolved': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_valid': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_valid': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerDispositionSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerReviewContract': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_capability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerReviewObligationReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ContainsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'conclusion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'explicit_exclusions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'auditor_provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationClaim': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'conclusion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'explicit_exclusions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'auditor_provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'claim': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAuditAuthority': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'issuer': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'principal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_id': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageCertificate': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'horizon_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_digests': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_schema_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageRequirement': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_kinds': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'horizon': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'required_evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'base_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'change_set': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateSnapshotCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateSnapshotResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateStandardEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'standard': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_units': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DecisionDependency': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'class': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'identity': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DecisionFingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'decision_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decision_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dependencies': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DeleteSnapshotCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DeleteSnapshotResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'purge_deadline': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Digest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'DispositionRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DomainContractReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EdgeId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'EqualsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EvidenceCheckRetirement': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'suite': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'check': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EvidenceConsumerRegistration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'path': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'artifact_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_policies': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EvidenceMaintenancePlan': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'prune_stale_certificates': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'retire_suites': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'retire_checks': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'retire_inputs': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'suite_descriptions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'replacement_evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'replacement_evidence_rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_updates': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer_registrations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'unregister_policy_subjects': {'title': None, 'description': 'Remove selected review-subject registrations and their source relationships while preserving normative Markdown.', 'has_default': False, 'default': None}}}, 'EvidenceReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider_contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EvidenceRelationshipUpdate': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'source_policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EvidenceSuiteDescription': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'suite': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'description': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ExistsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactObservation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirement': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_contract_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'answer_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_capability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirementId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactRequirementWork': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dependent_programs': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactSet': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactValue': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactValueContract': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'type': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'states': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'nullable': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'values': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FindProposalsCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'after': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'limit': {'title': None, 'description': None, 'has_default': True, 'default': 50}}}, 'FindProposalsResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'continuation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FindSnapshotsCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': True, 'default': 'active'}, 'after': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'limit': {'title': None, 'description': None, 'has_default': True, 'default': 50}}}, 'FindSnapshotsResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshots': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'continuation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'GeneralSelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'question': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ImpactDispositionSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ImpactTraceId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ImpactTraceReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'graph': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'values': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectableHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'InspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'MaintainEvidenceCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expected_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'apply': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'MaintainEvidenceResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applied': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changed_files': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'removed_files': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'verification': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ModuleRelationshipKey': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'MovePolicyUnitEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'standard': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'after_policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'NewPolicyUnit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'heading_chain': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'intent': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'aliases': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'predecessors': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'successors': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'NextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NonEmptyString': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NotExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expression': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Obligation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reasons': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_submissions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'review_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ObligationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'PendingResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changed_units': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyCoverageStatus': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyImpactSelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traces': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'declaration': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyRelationship': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'source_policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyRelationshipInspection': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'relationship_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'propagation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyRelationshipKey': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicySemanticIntent': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'PolicySummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyUnitDeclaration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'module': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'heading_path': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'aliases': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'predecessors': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'successors': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyUnitMapping': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reason': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_units': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PrepareCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PreservePolicySemantics': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'intent': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ProposalPolicySummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalReadResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'related': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'routing': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRelatedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authoring_target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_unit_mapping': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationships': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRelationshipSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traversal_eligible': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRevisionHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRevisionId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ProposalRouteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'unresolved_questions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'proposal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'head_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposeCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'change_set': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProvenanceRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'path': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProvideFactSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProviderReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'input_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PutPolicyRelationshipEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PutRoutingFactEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PutRoutingRuleEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rule': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QuarantinedSnapshotSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'created_at': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'purge_deadline': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryProposalNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'QueryRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'QueryResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'Question': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_answers': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'include_routing': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'include_coverage': {'title': None, 'description': 'Include current repository attestation status for registered policy units in this read scope.', 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'detail': {'title': None, 'description': 'Compact preserves exact policy and essential authority; full includes all relationship rows.', 'has_default': False, 'default': None}}}, 'ReadCoverage': {'title': None, 'description': 'Repository attestation status bound to this snapshot or proposal. Empty subjects means no registered policy units in scope, not complete coverage. Analysis-local attestations are not repository certificates.', 'has_default': False, 'default': None, 'properties': {'subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'include_routing': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'include_coverage': {'title': None, 'description': 'Include current repository attestation status for registered policy units in this read scope.', 'has_default': False, 'default': None}}}, 'ReadResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'related': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'routing': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadinessHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadinessId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ReadingPlanEntry': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reasons': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadingPlanReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RecoverApplicationCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RecoverApplicationResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'application': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RecoverCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RejectedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'code': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'outcome': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'message': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'details': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelatedCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'transitive': {'title': None, 'description': None, 'has_default': True, 'default': False}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelatedRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'transitive': {'title': None, 'description': None, 'has_default': True, 'default': False}}}, 'RelatedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authoring_target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_unit_mapping': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationships': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipConsumer': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RelationshipDisposition': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'relationship': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'disposition': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'replacement_consumer': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipKey': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RelationshipSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traversal_eligible': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RemovePolicyRelationshipEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RemoveRoutingFactEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RemoveRoutingRuleEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rule': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReplaceStandardRelationshipsEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'standard': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RepositoryPath': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RequiresReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResolveCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'submission': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResolveNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'work': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResolveWorkflowCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'submission': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResumeCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RetirePolicyUnitEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'retired_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'successors': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RetireStandardEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'standard': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'successors': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decisions': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewDecision': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decisions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prior_readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ReviseCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'change_set': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RevisePolicyUnitEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'title': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'body': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviseProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expected_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'change_set': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviseProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviseStandardEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'standard': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RouteCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RouteRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RouteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'unresolved_questions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingBaseReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'projection': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingConfiguration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rules': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingFactsCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingFactsResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingQuestion': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingRuleExplanation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingRuleReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rule': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ScalarValue': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SemanticProposal': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'intent': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotChildHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SnapshotInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SpecializesReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StandardContent': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'title': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'role': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'level': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applies_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'does_not_apply_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'verification': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'body': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StandardEdit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'StandardsChangePurpose': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StandardsChangeSet': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'purpose': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edits': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StructuredScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'heading_path': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Submission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'Timestamp': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'UndeleteSnapshotCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'UndeleteSnapshotResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'VerificationFailure': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'code': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'message': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'suite': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'check': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'VerificationReport': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'passed': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'exit_code': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'suites': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'checks': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'failures': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'VerifyProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'VerifyProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'verification': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'VerifyRepositoryCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'refresh_verification_inputs': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'VerifyRepositoryResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'refreshed_verification_inputs': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'verification': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'WholeArtifactScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'WorkflowContext': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'WorkflowContinuation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'required_inputs': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'WorkflowOutcome': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'WorkflowResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'outcome': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'WorkflowStatusCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'context': {'title': None, 'description': None, 'has_default': False, 'default': None}}}})

@dataclass(frozen=True, slots=True)
class ActiveSnapshotSummary:
    ''
    __definition__: ClassVar[str] = 'ActiveSnapshotSummary'
    __contract_fields__: ClassVar = MappingProxyType({
        'snapshot': 'snapshot',
        'lifecycle': 'lifecycle',
        'source_revision': 'source_revision',
        'created_at': 'created_at',
    })
    snapshot: SnapshotHandle
    lifecycle: Literal['active']
    source_revision: NonEmptyString
    created_at: Timestamp

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ActiveSnapshotSummary:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AgentRouteResult:
    ''
    __definition__: ClassVar[str] = 'AgentRouteResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'reading_plan': 'reading_plan',
        'unresolved_questions': 'unresolved_questions',
        'next_operations': 'next_operations',
        'summary': 'summary',
        'facts': 'facts',
        'rules': 'rules',
    })
    kind: Literal['agent-route-result']
    snapshot: SnapshotHandle
    reading_plan: tuple[ReadingPlanEntry, ...]
    unresolved_questions: tuple[RoutingQuestion, ...]
    next_operations: tuple[NextOperation, ...]
    facts: FactSet
    rules: tuple[RoutingRuleExplanation, ...]
    summary: str | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AgentRouteResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AllExpression:
    ''
    __definition__: ClassVar[str] = 'AllExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
        'expressions': 'expressions',
    })
    operator: Literal['all']
    expressions: tuple[ApplicabilityExpression, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AllExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AlwaysExpression:
    ''
    __definition__: ClassVar[str] = 'AlwaysExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
    })
    operator: Literal['always']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AlwaysExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisChildHandle:
    ''
    __definition__: ClassVar[str] = 'AnalysisChildHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'analysis': 'analysis',
        'child_kind': 'child_kind',
        'child_id': 'child_id',
        'schema_version': 'schema_version',
    })
    kind: Literal['analysis-child-handle']
    analysis: AnalysisHandle
    child_kind: Literal['context', 'fact-requirement', 'fact-observation', 'obligation', 'coverage-requirement', 'coverage-certificate']
    child_id: ChildId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisChildHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisChildInspectionResult:
    ''
    __definition__: ClassVar[str] = 'AnalysisChildInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'artifact': 'artifact',
    })
    kind: Literal['analysis-child-inspection-result']
    handle: AnalysisChildHandle
    artifact: AnalysisChildArtifact

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisChildInspectionResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisContext:
    ''
    __definition__: ClassVar[str] = 'AnalysisContext'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'subjects': 'subjects',
        'changes': 'changes',
        'semantic_proposals': 'semantic_proposals',
    })
    kind: Literal['analysis-context']
    handle: AnalysisChildHandle
    subjects: tuple[ChangedPolicyUnit, ...]
    changes: tuple[ChangeDescriptor, ...]
    semantic_proposals: tuple[SemanticProposal, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisContext:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisExecutionContractView:
    ''
    __definition__: ClassVar[str] = 'AnalysisExecutionContractView'
    __contract_fields__: ClassVar = MappingProxyType({
        'authorization_authority_digest': 'authorization_authority_digest',
        'providers': 'providers',
    })
    authorization_authority_digest: Digest | None
    providers: tuple[ProviderReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisExecutionContractView:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisHandle:
    ''
    __definition__: ClassVar[str] = 'AnalysisHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['analysis-handle']
    id: AnalysisId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisInspectionResult:
    ''
    __definition__: ClassVar[str] = 'AnalysisInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'state': 'state',
    })
    kind: Literal['analysis-inspection-result']
    state: AnalysisState

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisInspectionResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    ''
    __definition__: ClassVar[str] = 'AnalysisRequest'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'base_snapshot': 'base_snapshot',
        'proposed_snapshot': 'proposed_snapshot',
        'changes': 'changes',
        'semantic_proposals': 'semantic_proposals',
        'prior_analysis': 'prior_analysis',
        'contract_version': 'contract_version',
    })
    kind: Literal['analysis-request']
    base_snapshot: SnapshotHandle
    proposed_snapshot: SnapshotHandle
    changes: tuple[ChangeDescriptor, ...]
    semantic_proposals: tuple[SemanticProposal, ...]
    contract_version: int | float
    prior_analysis: AnalysisHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisRequest:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisState:
    ''
    __definition__: ClassVar[str] = 'AnalysisState'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'base_snapshot': 'base_snapshot',
        'proposed_reference': 'proposed_reference',
        'changes': 'changes',
        'semantic_proposals': 'semantic_proposals',
        'fact_observations': 'fact_observations',
        'dispositions': 'dispositions',
        'coverage_attestations': 'coverage_attestations',
        'authorization_records': 'authorization_records',
        'domain_contracts': 'domain_contracts',
        'execution_contracts': 'execution_contracts',
        'contract_version': 'contract_version',
    })
    kind: Literal['analysis-state']
    handle: AnalysisHandle
    base_snapshot: SnapshotHandle
    proposed_reference: AnalysisMaterialHandle
    changes: tuple[ChangeDescriptor, ...]
    semantic_proposals: tuple[SemanticProposal, ...]
    fact_observations: tuple[FactObservation, ...]
    dispositions: tuple[DispositionRecord, ...]
    coverage_attestations: tuple[CoverageAttestation, ...]
    authorization_records: tuple[AuthorizationRecord, ...]
    domain_contracts: tuple[DomainContractReference, ...]
    execution_contracts: AnalysisExecutionContractView
    contract_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisState:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalyzeCall:
    ''
    __definition__: ClassVar[str] = 'AnalyzeCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
    })
    context: WorkflowContext

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalyzeCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalyzeProposalCall:
    ''
    __definition__: ClassVar[str] = 'AnalyzeProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'revision': 'revision',
    })
    revision: ProposalRevisionHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalyzeProposalCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnyExpression:
    ''
    __definition__: ClassVar[str] = 'AnyExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
        'expressions': 'expressions',
    })
    operator: Literal['any']
    expressions: tuple[ApplicabilityExpression, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnyExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ApplicationHandle:
    ''
    __definition__: ClassVar[str] = 'ApplicationHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['application-handle']
    id: ApplicationId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ApplicationHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ApplicationRecoveryRequiredResult:
    ''
    __definition__: ClassVar[str] = 'ApplicationRecoveryRequiredResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'application': 'application',
        'status': 'status',
        'code': 'code',
        'outcome': 'outcome',
        'message': 'message',
    })
    kind: Literal['application-recovery-required-result']
    application: ApplicationHandle
    status: Literal['recovery-required']
    code: Literal['APPLICATION.PUBLICATION_UNAVAILABLE', 'APPLICATION.OBSERVATION_UNAVAILABLE', 'APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE', 'APPLICATION.RECOVERY_TARGET_UNCERTAIN', 'APPLICATION.RECOVERY_TARGET_DIVERGED']
    outcome: Literal['unavailable']
    message: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ApplicationRecoveryRequiredResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ApplyCall:
    ''
    __definition__: ClassVar[str] = 'ApplyCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
    })
    context: WorkflowContext

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ApplyCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ApplyProposalCall:
    ''
    __definition__: ClassVar[str] = 'ApplyProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'readiness': 'readiness',
    })
    kind: Literal['apply-proposal']
    readiness: ReadinessHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ApplyProposalCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ApplyProposalResult:
    ''
    __definition__: ClassVar[str] = 'ApplyProposalResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'application': 'application',
        'status': 'status',
    })
    kind: Literal['apply-proposal-result']
    application: ApplicationHandle
    status: Literal['applied']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ApplyProposalResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AuditPolicyUnitEdit:
    ''
    __definition__: ClassVar[str] = 'AuditPolicyUnitEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'policy': 'policy',
        'rationale': 'rationale',
    })
    kind: Literal['audit-policy-unit']
    policy: CanonicalId
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuditPolicyUnitEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AuthoredRoutingFact:
    ''
    __definition__: ClassVar[str] = 'AuthoredRoutingFact'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'semantic_revision': 'semantic_revision',
        'type': 'type',
        'nullable': 'nullable',
        'values': 'values',
        'aliases': 'aliases',
        'meaning': 'meaning',
        'prompt': 'prompt',
    })
    id: CanonicalId
    semantic_revision: int | float
    type: Literal['boolean', 'enum', 'string', 'string-set', 'enum-set', 'canonical-id']
    nullable: bool
    values: tuple[str, ...]
    aliases: tuple[CanonicalId, ...]
    meaning: NonEmptyString
    prompt: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuthoredRoutingFact:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AuthoredRoutingRule:
    ''
    __definition__: ClassVar[str] = 'AuthoredRoutingRule'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'target': 'target',
        'when': 'when',
        'condition': 'condition',
    })
    id: CanonicalId
    target: CanonicalId
    when: ApplicabilityExpression
    condition: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuthoredRoutingRule:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AuthoringTargetHandle:
    ''
    __definition__: ClassVar[str] = 'AuthoringTargetHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['authoring-target-handle']
    snapshot: SnapshotHandle
    id: ChildId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuthoringTargetHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AuthorizationRecord:
    ''
    __definition__: ClassVar[str] = 'AuthorizationRecord'
    __contract_fields__: ClassVar = MappingProxyType({
        'reference': 'reference',
        'issuer_semantic_revision': 'issuer_semantic_revision',
        'principal': 'principal',
        'action': 'action',
        'subject_kind': 'subject_kind',
        'subject_id': 'subject_id',
        'authorization_evidence': 'authorization_evidence',
        'revocation_authority': 'revocation_authority',
        'revocation_authority_semantic_revision': 'revocation_authority_semantic_revision',
        'revocation_evidence': 'revocation_evidence',
    })
    reference: AuthorizationReference
    issuer_semantic_revision: int | float
    principal: CanonicalId
    action: CanonicalId
    subject_kind: CanonicalId
    subject_id: NonEmptyString
    authorization_evidence: tuple[EvidenceReference, ...]
    revocation_authority: CanonicalId
    revocation_authority_semantic_revision: int | float
    revocation_evidence: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuthorizationRecord:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AuthorizationReference:
    ''
    __definition__: ClassVar[str] = 'AuthorizationReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'issuer': 'issuer',
        'capability': 'capability',
        'authority_digest': 'authority_digest',
    })
    id: AuthorizationId
    issuer: CanonicalId
    capability: CanonicalId
    authority_digest: Digest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuthorizationReference:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CanonicalModuleDeclaration:
    ''
    __definition__: ClassVar[str] = 'CanonicalModuleDeclaration'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'role': 'role',
        'level': 'level',
        'applies_when': 'applies_when',
        'does_not_apply_when': 'does_not_apply_when',
        'requires': 'requires',
        'specializes': 'specializes',
        'verification': 'verification',
    })
    kind: Literal['canonical-module']
    id: CanonicalId
    role: Literal['core', 'router', 'workflow', 'profile', 'topic', 'reference']
    level: Literal['MUST', 'SHOULD', 'PROFILE', 'REFERENCE']
    applies_when: NonEmptyString
    does_not_apply_when: NonEmptyString
    requires: tuple[CanonicalId, ...]
    specializes: tuple[CanonicalId, ...]
    verification: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CanonicalModuleDeclaration:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ChangeDescriptor:
    ''
    __definition__: ClassVar[str] = 'ChangeDescriptor'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'accepted_ids': 'accepted_ids',
        'proposed_ids': 'proposed_ids',
        'scope': 'scope',
        'accepted_module': 'accepted_module',
        'proposed_module': 'proposed_module',
    })
    kind: Literal['module', 'modification', 'addition', 'removal', 'move', 'split', 'merge']
    accepted_ids: tuple[CanonicalId, ...]
    proposed_ids: tuple[CanonicalId, ...]
    scope: ReviewScope
    accepted_module: CanonicalId | MissingValue = MISSING
    proposed_module: CanonicalId | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ChangeDescriptor:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ChangePolicySemantics:
    ''
    __definition__: ClassVar[str] = 'ChangePolicySemantics'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'accepted_semantic_revision': 'accepted_semantic_revision',
        'proposed_semantic_revision': 'proposed_semantic_revision',
        'intent': 'intent',
    })
    kind: Literal['change']
    accepted_semantic_revision: int | float
    proposed_semantic_revision: int | float
    intent: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ChangePolicySemantics:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ChangedPolicyUnit:
    ''
    __definition__: ClassVar[str] = 'ChangedPolicyUnit'
    __contract_fields__: ClassVar = MappingProxyType({
        'policy': 'policy',
        'change_kind': 'change_kind',
        'classification': 'classification',
        'accepted_representation_digest': 'accepted_representation_digest',
        'proposed_representation_digest': 'proposed_representation_digest',
        'accepted_structural_digest': 'accepted_structural_digest',
        'proposed_structural_digest': 'proposed_structural_digest',
        'accepted_semantic_revision': 'accepted_semantic_revision',
        'proposed_semantic_revision': 'proposed_semantic_revision',
        'semantic_state': 'semantic_state',
        'scope': 'scope',
    })
    policy: CanonicalId
    change_kind: Literal['modification', 'addition', 'removal', 'move', 'split-predecessor', 'split-successor', 'merge-predecessor', 'merge-successor']
    classification: Literal['unchanged', 'representation-only-candidate', 'possibly-semantically-changed', 'semantically-changed', 'unresolved']
    accepted_representation_digest: Digest | None
    proposed_representation_digest: Digest | None
    accepted_structural_digest: Digest | None
    proposed_structural_digest: Digest | None
    accepted_semantic_revision: int | float | None
    proposed_semantic_revision: int | float | None
    semantic_state: Literal['accepted-unchanged', 'proposed', 'removed', 'unresolved']
    scope: ReviewScope

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ChangedPolicyUnit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CompactReadResult:
    ''
    __definition__: ClassVar[str] = 'CompactReadResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'policy': 'policy',
        'content': 'content',
        'requires': 'requires',
        'specializes': 'specializes',
        'next_operations': 'next_operations',
        'summary': 'summary',
        'routing': 'routing',
        'coverage': 'coverage',
        'detail': 'detail',
    })
    kind: Literal['compact-read-result']
    snapshot: SnapshotHandle
    policy: PolicySummary
    content: str
    requires: tuple[CanonicalId, ...]
    specializes: tuple[CanonicalId, ...]
    next_operations: tuple[NextOperation, ...]
    detail: Literal['compact']
    summary: str | MissingValue = MISSING
    routing: RoutingConfiguration | MissingValue = MISSING
    coverage: ReadCoverage | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CompactReadResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CompleteResult:
    ''
    __definition__: ClassVar[str] = 'CompleteResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'status': 'status',
        'context': 'context',
        'changes': 'changes',
        'changed_units': 'changed_units',
        'coverage_certificates': 'coverage_certificates',
        'fact_observations': 'fact_observations',
        'dispositions': 'dispositions',
        'reading_plan': 'reading_plan',
        'completion': 'completion',
        'summary': 'summary',
    })
    kind: Literal['complete-result']
    handle: AnalysisHandle
    status: Literal['complete']
    context: AnalysisContext
    changes: tuple[ChangeDescriptor, ...]
    changed_units: tuple[ChangedPolicyUnit, ...]
    coverage_certificates: tuple[CoverageCertificate, ...]
    fact_observations: tuple[FactObservation, ...]
    dispositions: tuple[DispositionRecord, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    completion: CompletionProof
    summary: str | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CompleteResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CompletionProof:
    ''
    __definition__: ClassVar[str] = 'CompletionProof'
    __contract_fields__: ClassVar = MappingProxyType({
        'required_coverage_subjects': 'required_coverage_subjects',
        'certificate_subjects': 'certificate_subjects',
        'reached_consumer_obligations': 'reached_consumer_obligations',
        'disposition_obligations': 'disposition_obligations',
        'required_fact_requirements': 'required_fact_requirements',
        'observed_fact_requirements': 'observed_fact_requirements',
        'non_consumer_obligations_resolved': 'non_consumer_obligations_resolved',
        'applicability_resolved': 'applicability_resolved',
        'authorization_valid': 'authorization_valid',
        'evidence_valid': 'evidence_valid',
    })
    required_coverage_subjects: tuple[CanonicalId, ...]
    certificate_subjects: tuple[CanonicalId, ...]
    reached_consumer_obligations: tuple[ObligationId, ...]
    disposition_obligations: tuple[ObligationId, ...]
    required_fact_requirements: tuple[FactRequirementId, ...]
    observed_fact_requirements: tuple[FactRequirementId, ...]
    non_consumer_obligations_resolved: Literal[True]
    applicability_resolved: Literal[True]
    authorization_valid: Literal[True]
    evidence_valid: Literal[True]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CompletionProof:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ConsumerDispositionSubmission:
    ''
    __definition__: ClassVar[str] = 'ConsumerDispositionSubmission'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'obligation': 'obligation',
        'result': 'result',
        'rationale': 'rationale',
        'evidence': 'evidence',
        'fingerprint': 'fingerprint',
    })
    kind: Literal['consumer-disposition']
    obligation: AnalysisChildHandle
    result: Literal['updated', 'reviewed-no-change', 'not-applicable', 'blocked']
    rationale: NonEmptyString
    evidence: tuple[EvidenceReference, ...]
    fingerprint: DecisionFingerprint

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ConsumerDispositionSubmission:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ConsumerReviewContract:
    ''
    __definition__: ClassVar[str] = 'ConsumerReviewContract'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'version': 'version',
        'permitted_dispositions': 'permitted_dispositions',
        'evidence_contract': 'evidence_contract',
        'authorization_capability': 'authorization_capability',
        'semantics': 'semantics',
    })
    kind: Literal['consumer-review-contract']
    id: CanonicalId
    version: int | float
    permitted_dispositions: tuple[Literal['updated', 'reviewed-no-change', 'not-applicable', 'blocked'], ...]
    evidence_contract: CanonicalId
    authorization_capability: CanonicalId
    semantics: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ConsumerReviewContract:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ConsumerReviewObligationReadingReason:
    ''
    __definition__: ClassVar[str] = 'ConsumerReviewObligationReadingReason'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'obligation': 'obligation',
    })
    kind: Literal['consumer-review-obligation']
    obligation: ObligationId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ConsumerReviewObligationReadingReason:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ContainsExpression:
    ''
    __definition__: ClassVar[str] = 'ContainsExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
        'fact': 'fact',
        'value': 'value',
    })
    operator: Literal['contains']
    fact: CanonicalId
    value: ScalarValue

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ContainsExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAttestation:
    ''
    __definition__: ClassVar[str] = 'CoverageAttestation'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'requirement': 'requirement',
        'conclusion': 'conclusion',
        'evidence': 'evidence',
        'explicit_exclusions': 'explicit_exclusions',
        'rationale': 'rationale',
        'auditor_provenance': 'auditor_provenance',
        'schema_version': 'schema_version',
        'authorization': 'authorization',
    })
    kind: Literal['coverage-attestation']
    requirement: AnalysisChildHandle
    conclusion: Literal['complete']
    evidence: tuple[EvidenceReference, ...]
    explicit_exclusions: tuple[EvidenceReference, ...]
    rationale: NonEmptyString
    auditor_provenance: NonEmptyString
    schema_version: int | float
    authorization: AuthorizationReference

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAttestation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAttestationClaim:
    ''
    __definition__: ClassVar[str] = 'CoverageAttestationClaim'
    __contract_fields__: ClassVar = MappingProxyType({
        'requirement': 'requirement',
        'conclusion': 'conclusion',
        'evidence': 'evidence',
        'explicit_exclusions': 'explicit_exclusions',
        'rationale': 'rationale',
        'auditor_provenance': 'auditor_provenance',
    })
    requirement: AnalysisChildHandle
    conclusion: Literal['complete']
    evidence: tuple[EvidenceReference, ...]
    explicit_exclusions: tuple[EvidenceReference, ...]
    rationale: NonEmptyString
    auditor_provenance: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAttestationClaim:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAttestationSubmission:
    ''
    __definition__: ClassVar[str] = 'CoverageAttestationSubmission'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'claim': 'claim',
    })
    kind: Literal['coverage-attestation']
    claim: CoverageAttestationClaim

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAttestationSubmission:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAuditAuthority:
    ''
    __definition__: ClassVar[str] = 'CoverageAuditAuthority'
    __contract_fields__: ClassVar = MappingProxyType({
        'issuer': 'issuer',
        'principal': 'principal',
        'authorization_id': 'authorization_id',
    })
    issuer: NonEmptyString
    principal: NonEmptyString
    authorization_id: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAuditAuthority:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageCertificate:
    ''
    __definition__: ClassVar[str] = 'CoverageCertificate'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'requirement': 'requirement',
        'subject': 'subject',
        'owner': 'owner',
        'semantic_revision': 'semantic_revision',
        'horizon_digest': 'horizon_digest',
        'relationship_digest': 'relationship_digest',
        'evidence_digests': 'evidence_digests',
        'fact_schema_digest': 'fact_schema_digest',
    })
    kind: Literal['coverage-certificate']
    handle: AnalysisChildHandle
    requirement: AnalysisChildHandle
    subject: CanonicalId
    owner: CanonicalId
    semantic_revision: int | float
    horizon_digest: Digest
    relationship_digest: Digest
    evidence_digests: tuple[Digest, ...]
    fact_schema_digest: Digest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageCertificate:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageRequirement:
    ''
    __definition__: ClassVar[str] = 'CoverageRequirement'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'subject': 'subject',
        'owner': 'owner',
        'semantic_revision': 'semantic_revision',
        'relationship_kinds': 'relationship_kinds',
        'horizon': 'horizon',
        'required_evidence_contract': 'required_evidence_contract',
    })
    kind: Literal['coverage-requirement']
    handle: AnalysisChildHandle
    subject: CanonicalId
    owner: CanonicalId
    semantic_revision: int | float
    relationship_kinds: tuple[CanonicalId, ...]
    horizon: CanonicalId
    required_evidence_contract: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageRequirement:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CreateProposalCall:
    ''
    __definition__: ClassVar[str] = 'CreateProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'base_snapshot': 'base_snapshot',
        'change_set': 'change_set',
    })
    kind: Literal['create-proposal']
    base_snapshot: SnapshotHandle
    change_set: StandardsChangeSet

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CreateProposalCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CreateProposalResult:
    ''
    __definition__: ClassVar[str] = 'CreateProposalResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'proposal': 'proposal',
        'revision': 'revision',
    })
    kind: Literal['create-proposal-result']
    proposal: ProposalHandle
    revision: ProposalRevisionHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CreateProposalResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CreateSnapshotCall:
    ''
    __definition__: ClassVar[str] = 'CreateSnapshotCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
    })
    kind: Literal['create-snapshot']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CreateSnapshotCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CreateSnapshotResult:
    ''
    __definition__: ClassVar[str] = 'CreateSnapshotResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
    })
    kind: Literal['create-snapshot-result']
    snapshot: ActiveSnapshotSummary

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CreateSnapshotResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CreateStandardEdit:
    ''
    __definition__: ClassVar[str] = 'CreateStandardEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'standard': 'standard',
        'requires': 'requires',
        'specializes': 'specializes',
        'policy_units': 'policy_units',
    })
    kind: Literal['create-standard']
    standard: StandardContent
    requires: tuple[CanonicalId, ...]
    specializes: tuple[CanonicalId, ...]
    policy_units: tuple[NewPolicyUnit, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CreateStandardEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class DecisionDependency:
    ''
    __definition__: ClassVar[str] = 'DecisionDependency'
    __contract_fields__: ClassVar = MappingProxyType({
        'class': 'class_',
        'identity': 'identity',
        'digest': 'digest',
    })
    class_: Literal['policy-unit', 'semantic-revision', 'structure', 'representation', 'module-locator', 'applicability-fact', 'relationship', 'audit', 'exception', 'evidence', 'provider-contract', 'applicability-contract', 'analysis-contract']
    identity: NonEmptyString
    digest: Digest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> DecisionDependency:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class DecisionFingerprint:
    ''
    __definition__: ClassVar[str] = 'DecisionFingerprint'
    __contract_fields__: ClassVar = MappingProxyType({
        'decision_kind': 'decision_kind',
        'decision_contract': 'decision_contract',
        'schema_version': 'schema_version',
        'dependencies': 'dependencies',
    })
    decision_kind: CanonicalId
    decision_contract: CanonicalId
    schema_version: int | float
    dependencies: tuple[DecisionDependency, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> DecisionFingerprint:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class DeleteSnapshotCall:
    ''
    __definition__: ClassVar[str] = 'DeleteSnapshotCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
    })
    kind: Literal['delete-snapshot']
    snapshot: SnapshotHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> DeleteSnapshotCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class DeleteSnapshotResult:
    ''
    __definition__: ClassVar[str] = 'DeleteSnapshotResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'purge_deadline': 'purge_deadline',
    })
    kind: Literal['delete-snapshot-result']
    snapshot: SnapshotHandle
    purge_deadline: Timestamp

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> DeleteSnapshotResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class DispositionRecord:
    ''
    __definition__: ClassVar[str] = 'DispositionRecord'
    __contract_fields__: ClassVar = MappingProxyType({
        'obligation': 'obligation',
        'kind': 'kind',
        'result': 'result',
        'rationale': 'rationale',
        'evidence': 'evidence',
        'authorization': 'authorization',
        'fingerprint': 'fingerprint',
    })
    obligation: AnalysisChildHandle
    kind: Literal['consumer-disposition', 'impact-disposition']
    result: NonEmptyString
    rationale: NonEmptyString
    evidence: tuple[EvidenceReference, ...]
    authorization: AuthorizationReference
    fingerprint: DecisionFingerprint

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> DispositionRecord:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class DomainContractReference:
    ''
    __definition__: ClassVar[str] = 'DomainContractReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'version': 'version',
    })
    id: CanonicalId
    version: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> DomainContractReference:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class EqualsExpression:
    ''
    __definition__: ClassVar[str] = 'EqualsExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
        'fact': 'fact',
        'value': 'value',
    })
    operator: Literal['equals']
    fact: CanonicalId
    value: ScalarValue

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> EqualsExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class EvidenceCheckRetirement:
    ''
    __definition__: ClassVar[str] = 'EvidenceCheckRetirement'
    __contract_fields__: ClassVar = MappingProxyType({
        'suite': 'suite',
        'check': 'check',
    })
    suite: str
    check: str

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> EvidenceCheckRetirement:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class EvidenceConsumerRegistration:
    ''
    __definition__: ClassVar[str] = 'EvidenceConsumerRegistration'
    __contract_fields__: ClassVar = MappingProxyType({
        'path': 'path',
        'artifact_kind': 'artifact_kind',
        'source_policies': 'source_policies',
        'relation': 'relation',
        'evidence_owner': 'evidence_owner',
        'rationale': 'rationale',
    })
    path: str
    artifact_kind: Literal['implementation-artifact', 'fixture']
    source_policies: tuple[str, ...]
    relation: Literal['implementation-projection', 'fixture-projection']
    evidence_owner: str
    rationale: str

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> EvidenceConsumerRegistration:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class EvidenceMaintenancePlan:
    ''
    __definition__: ClassVar[str] = 'EvidenceMaintenancePlan'
    __contract_fields__: ClassVar = MappingProxyType({
        'prune_stale_certificates': 'prune_stale_certificates',
        'retire_suites': 'retire_suites',
        'retire_checks': 'retire_checks',
        'retire_inputs': 'retire_inputs',
        'suite_descriptions': 'suite_descriptions',
        'replacement_evidence_owner': 'replacement_evidence_owner',
        'replacement_evidence_rationale': 'replacement_evidence_rationale',
        'relationship_updates': 'relationship_updates',
        'consumer_registrations': 'consumer_registrations',
        'unregister_policy_subjects': 'unregister_policy_subjects',
    })
    prune_stale_certificates: bool
    retire_suites: tuple[str, ...]
    retire_checks: tuple[EvidenceCheckRetirement, ...]
    retire_inputs: tuple[str, ...]
    suite_descriptions: tuple[EvidenceSuiteDescription, ...]
    replacement_evidence_owner: str
    replacement_evidence_rationale: str
    relationship_updates: tuple[EvidenceRelationshipUpdate, ...]
    consumer_registrations: tuple[EvidenceConsumerRegistration, ...]
    unregister_policy_subjects: tuple[str, ...] | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> EvidenceMaintenancePlan:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class EvidenceReference:
    ''
    __definition__: ClassVar[str] = 'EvidenceReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'digest': 'digest',
        'provider_contract': 'provider_contract',
        'provider_contract_version': 'provider_contract_version',
    })
    id: CanonicalId
    digest: Digest
    provider_contract: CanonicalId
    provider_contract_version: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> EvidenceReference:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class EvidenceRelationshipUpdate:
    ''
    __definition__: ClassVar[str] = 'EvidenceRelationshipUpdate'
    __contract_fields__: ClassVar = MappingProxyType({
        'source_policy': 'source_policy',
        'consumer': 'consumer',
        'relation': 'relation',
        'evidence_owner': 'evidence_owner',
        'rationale': 'rationale',
    })
    source_policy: str
    consumer: str
    relation: str
    evidence_owner: str
    rationale: str

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> EvidenceRelationshipUpdate:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class EvidenceSuiteDescription:
    ''
    __definition__: ClassVar[str] = 'EvidenceSuiteDescription'
    __contract_fields__: ClassVar = MappingProxyType({
        'suite': 'suite',
        'description': 'description',
    })
    suite: str
    description: str

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> EvidenceSuiteDescription:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ExistsExpression:
    ''
    __definition__: ClassVar[str] = 'ExistsExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
        'fact': 'fact',
    })
    operator: Literal['exists']
    fact: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ExistsExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FactObservation:
    ''
    __definition__: ClassVar[str] = 'FactObservation'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'requirement': 'requirement',
        'value': 'value',
        'evidence': 'evidence',
        'authorization': 'authorization',
        'provider': 'provider',
    })
    kind: Literal['fact-observation']
    handle: AnalysisChildHandle
    requirement: AnalysisChildHandle
    value: FactValue
    evidence: tuple[EvidenceReference, ...]
    authorization: AuthorizationReference
    provider: ProviderReference | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactObservation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FactRequirement:
    ''
    __definition__: ClassVar[str] = 'FactRequirement'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'fact': 'fact',
        'fact_semantic_revision': 'fact_semantic_revision',
        'fact_contract_digest': 'fact_contract_digest',
        'context': 'context',
        'value_contract': 'value_contract',
        'answer_contract': 'answer_contract',
        'evidence_contract': 'evidence_contract',
        'authorization_capability': 'authorization_capability',
    })
    kind: Literal['fact-requirement']
    handle: AnalysisChildHandle
    fact: CanonicalId
    fact_semantic_revision: int | float
    fact_contract_digest: Digest
    context: AnalysisChildHandle
    value_contract: FactValueContract
    answer_contract: CanonicalId
    evidence_contract: CanonicalId
    authorization_capability: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactRequirement:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FactRequirementWork:
    ''
    __definition__: ClassVar[str] = 'FactRequirementWork'
    __contract_fields__: ClassVar = MappingProxyType({
        'requirement': 'requirement',
        'prompt': 'prompt',
        'dependent_programs': 'dependent_programs',
    })
    requirement: FactRequirement
    prompt: NonEmptyString
    dependent_programs: tuple[NonEmptyString, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactRequirementWork:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FactValueContract:
    ''
    __definition__: ClassVar[str] = 'FactValueContract'
    __contract_fields__: ClassVar = MappingProxyType({
        'type': 'type',
        'states': 'states',
        'nullable': 'nullable',
        'values': 'values',
    })
    type: Literal['boolean', 'enum', 'string', 'string-set', 'enum-set', 'canonical-id']
    states: object
    nullable: bool
    values: tuple[str, ...] | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactValueContract:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FindProposalsCall:
    ''
    __definition__: ClassVar[str] = 'FindProposalsCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'after': 'after',
        'limit': 'limit',
    })
    kind: Literal['find-proposals']
    after: ProposalHandle | MissingValue = MISSING
    limit: int | float | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FindProposalsCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FindProposalsResult:
    ''
    __definition__: ClassVar[str] = 'FindProposalsResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'proposals': 'proposals',
        'continuation': 'continuation',
    })
    kind: Literal['find-proposals-result']
    proposals: tuple[ProposalSummary, ...]
    continuation: ProposalHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FindProposalsResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FindSnapshotsCall:
    ''
    __definition__: ClassVar[str] = 'FindSnapshotsCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'lifecycle': 'lifecycle',
        'after': 'after',
        'limit': 'limit',
    })
    kind: Literal['find-snapshots']
    lifecycle: Literal['active', 'quarantined'] | MissingValue = MISSING
    after: SnapshotHandle | MissingValue = MISSING
    limit: int | float | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FindSnapshotsCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FindSnapshotsResult:
    ''
    __definition__: ClassVar[str] = 'FindSnapshotsResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshots': 'snapshots',
        'continuation': 'continuation',
    })
    kind: Literal['find-snapshots-result']
    snapshots: tuple[SnapshotSummary, ...]
    continuation: SnapshotHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FindSnapshotsResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class GeneralSelectionReason:
    ''
    __definition__: ClassVar[str] = 'GeneralSelectionReason'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'source': 'source',
        'fact': 'fact',
        'edge': 'edge',
        'question': 'question',
    })
    kind: Literal['routing-fact', 'requires', 'specializes', 'changed-policy', 'question', 'audit-coverage', 'unmapped-normative-change', 'structured-scope-analysis-unsupported']
    source: CanonicalId | MissingValue = MISSING
    fact: CanonicalId | MissingValue = MISSING
    edge: EdgeId | MissingValue = MISSING
    question: CanonicalId | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> GeneralSelectionReason:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ImpactDispositionSubmission:
    ''
    __definition__: ClassVar[str] = 'ImpactDispositionSubmission'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'obligation': 'obligation',
        'result': 'result',
        'rationale': 'rationale',
        'evidence': 'evidence',
        'fingerprint': 'fingerprint',
    })
    kind: Literal['impact-disposition']
    obligation: AnalysisChildHandle
    result: Literal['confirmed', 'resolved-no-impact', 'requires-change', 'blocked']
    rationale: NonEmptyString
    evidence: tuple[EvidenceReference, ...]
    fingerprint: DecisionFingerprint

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ImpactDispositionSubmission:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ImpactTraceReference:
    ''
    __definition__: ClassVar[str] = 'ImpactTraceReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'graph': 'graph',
        'applicability': 'applicability',
    })
    id: ImpactTraceId
    graph: Literal['accepted', 'proposed']
    applicability: Literal['true', 'false', 'unknown']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ImpactTraceReference:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class InExpression:
    ''
    __definition__: ClassVar[str] = 'InExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
        'fact': 'fact',
        'values': 'values',
    })
    operator: Literal['in']
    fact: CanonicalId
    values: tuple[ScalarValue, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> InExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class InspectCall:
    ''
    __definition__: ClassVar[str] = 'InspectCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'handle': 'handle',
    })
    handle: InspectableHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> InspectCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class InspectNextOperation:
    ''
    __definition__: ClassVar[str] = 'InspectNextOperation'
    __contract_fields__: ClassVar = MappingProxyType({
        'operation': 'operation',
        'request_kind': 'request_kind',
        'handle': 'handle',
    })
    operation: Literal['inspect']
    request_kind: Literal['inspect']
    handle: InspectableHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> InspectNextOperation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class MaintainEvidenceCall:
    ''
    __definition__: ClassVar[str] = 'MaintainEvidenceCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'expected_revision': 'expected_revision',
        'evidence': 'evidence',
        'plan': 'plan',
        'apply': 'apply',
    })
    kind: Literal['maintain-evidence']
    expected_revision: str
    evidence: tuple[EvidenceReference, ...]
    plan: EvidenceMaintenancePlan
    apply: bool

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> MaintainEvidenceCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class MaintainEvidenceResult:
    ''
    __definition__: ClassVar[str] = 'MaintainEvidenceResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'applied': 'applied',
        'changed_files': 'changed_files',
        'removed_files': 'removed_files',
        'verification': 'verification',
    })
    kind: Literal['maintain-evidence-result']
    applied: bool
    changed_files: tuple[str, ...]
    removed_files: tuple[str, ...]
    verification: VerificationReport

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> MaintainEvidenceResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ModuleRelationshipKey:
    ''
    __definition__: ClassVar[str] = 'ModuleRelationshipKey'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'relation': 'relation',
        'source': 'source',
        'target': 'target',
    })
    kind: Literal['module-relationship']
    relation: Literal['requires', 'specializes']
    source: CanonicalId
    target: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ModuleRelationshipKey:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class MovePolicyUnitEdit:
    ''
    __definition__: ClassVar[str] = 'MovePolicyUnitEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'policy': 'policy',
        'standard': 'standard',
        'after_policy': 'after_policy',
        'semantics': 'semantics',
    })
    kind: Literal['move-policy-unit']
    policy: CanonicalId
    standard: CanonicalId
    semantics: PolicySemanticIntent
    after_policy: CanonicalId | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> MovePolicyUnitEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class NewPolicyUnit:
    ''
    __definition__: ClassVar[str] = 'NewPolicyUnit'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'heading_chain': 'heading_chain',
        'semantic_revision': 'semantic_revision',
        'intent': 'intent',
        'aliases': 'aliases',
        'predecessors': 'predecessors',
        'successors': 'successors',
    })
    id: CanonicalId
    heading_chain: tuple[NonEmptyString, ...]
    semantic_revision: int | float
    intent: NonEmptyString
    aliases: tuple[CanonicalId, ...]
    predecessors: tuple[CanonicalId, ...]
    successors: tuple[CanonicalId, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> NewPolicyUnit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class NotExpression:
    ''
    __definition__: ClassVar[str] = 'NotExpression'
    __contract_fields__: ClassVar = MappingProxyType({
        'operator': 'operator',
        'expression': 'expression',
    })
    operator: Literal['not']
    expression: ApplicabilityExpression

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> NotExpression:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class Obligation:
    ''
    __definition__: ClassVar[str] = 'Obligation'
    __contract_fields__: ClassVar = MappingProxyType({
        'handle': 'handle',
        'kind': 'kind',
        'target': 'target',
        'scope': 'scope',
        'reasons': 'reasons',
        'state': 'state',
        'applicability': 'applicability',
        'permitted_submissions': 'permitted_submissions',
        'review_contract': 'review_contract',
        'fingerprint': 'fingerprint',
    })
    handle: AnalysisChildHandle
    kind: Literal['consumer-review', 'impact-review', 'lifecycle-impact-review', 'audit-coverage', 'unmapped-normative-change']
    target: CanonicalId
    scope: ReviewScope
    reasons: tuple[SelectionReason, ...]
    state: Literal['required', 'resolved', 'blocked']
    permitted_submissions: tuple[Literal['consumer-disposition', 'impact-disposition', 'coverage-attestation'], ...]
    fingerprint: DecisionFingerprint
    applicability: Literal['true', 'false', 'unknown', 'not-declared'] | MissingValue = MISSING
    review_contract: ConsumerReviewContract | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> Obligation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PendingResult:
    ''
    __definition__: ClassVar[str] = 'PendingResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'status': 'status',
        'context': 'context',
        'changes': 'changes',
        'changed_units': 'changed_units',
        'obligations': 'obligations',
        'fact_requirements': 'fact_requirements',
        'reading_plan': 'reading_plan',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['pending-result']
    handle: AnalysisHandle
    status: Literal['needs-action']
    context: AnalysisContext
    changes: tuple[ChangeDescriptor, ...]
    changed_units: tuple[ChangedPolicyUnit, ...]
    obligations: tuple[Obligation, ...]
    fact_requirements: tuple[FactRequirementWork, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    next_operations: tuple[NextOperation, ...]
    summary: str | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PendingResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyCoverageStatus:
    ''
    __definition__: ClassVar[str] = 'PolicyCoverageStatus'
    __contract_fields__: ClassVar = MappingProxyType({
        'subject': 'subject',
        'requirement_id': 'requirement_id',
        'status': 'status',
        'authority': 'authority',
    })
    subject: CanonicalId
    requirement_id: Digest
    status: Literal['current-attestation', 'review-required']
    authority: CoverageAuditAuthority | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyCoverageStatus:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyImpactSelectionReason:
    ''
    __definition__: ClassVar[str] = 'PolicyImpactSelectionReason'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'source': 'source',
        'edge': 'edge',
        'relation': 'relation',
        'evidence_owner': 'evidence_owner',
        'traces': 'traces',
    })
    kind: Literal['policy-impact-edge']
    source: CanonicalId
    edge: EdgeId
    relation: CanonicalId
    evidence_owner: CanonicalId
    traces: tuple[ImpactTraceReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyImpactSelectionReason:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyInspectionResult:
    ''
    __definition__: ClassVar[str] = 'PolicyInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'policy': 'policy',
        'declaration': 'declaration',
        'representation_digest': 'representation_digest',
        'structural_digest': 'structural_digest',
        'provenance': 'provenance',
    })
    kind: Literal['policy-inspection-result']
    policy: SnapshotChildHandle
    declaration: CanonicalModuleDeclaration | PolicyUnitDeclaration
    representation_digest: Digest
    structural_digest: Digest
    provenance: ProvenanceRecord

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyInspectionResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyRelationship:
    ''
    __definition__: ClassVar[str] = 'PolicyRelationship'
    __contract_fields__: ClassVar = MappingProxyType({
        'source_policy': 'source_policy',
        'consumer': 'consumer',
        'relation': 'relation',
        'applicability': 'applicability',
        'source_scope': 'source_scope',
        'consumer_scope': 'consumer_scope',
        'evidence_owner': 'evidence_owner',
        'rationale': 'rationale',
    })
    source_policy: CanonicalId
    consumer: RelationshipConsumer
    relation: Literal['normative-consumer', 'router-projection', 'prompt-projection', 'template-projection', 'reference-projection', 'fixture-projection', 'enforcement-suite-projection', 'documentation-projection', 'implementation-projection']
    applicability: ApplicabilityExpression
    source_scope: ReviewScope | None
    consumer_scope: ReviewScope | None
    evidence_owner: CanonicalId
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyRelationship:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyRelationshipInspection:
    ''
    __definition__: ClassVar[str] = 'PolicyRelationshipInspection'
    __contract_fields__: ClassVar = MappingProxyType({
        'relationship_kind': 'relationship_kind',
        'applicability': 'applicability',
        'source_scope': 'source_scope',
        'consumer_scope': 'consumer_scope',
        'propagation': 'propagation',
        'evidence_owner': 'evidence_owner',
        'rationale': 'rationale',
    })
    relationship_kind: Literal['normative-consumer', 'router-projection', 'prompt-projection', 'template-projection', 'reference-projection', 'fixture-projection', 'enforcement-suite-projection', 'documentation-projection', 'implementation-projection']
    applicability: ApplicabilityExpression
    source_scope: ReviewScope | None
    consumer_scope: ReviewScope | None
    propagation: Literal['source-to-consumer']
    evidence_owner: CanonicalId
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyRelationshipInspection:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyRelationshipKey:
    ''
    __definition__: ClassVar[str] = 'PolicyRelationshipKey'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'source_policy': 'source_policy',
        'consumer': 'consumer',
        'relation': 'relation',
    })
    kind: Literal['policy-relationship']
    source_policy: CanonicalId
    consumer: RelationshipConsumer
    relation: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyRelationshipKey:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicySummary:
    ''
    __definition__: ClassVar[str] = 'PolicySummary'
    __contract_fields__: ClassVar = MappingProxyType({
        'handle': 'handle',
        'authority': 'authority',
        'scope': 'scope',
    })
    handle: SnapshotChildHandle
    authority: Literal['normative', 'projection', 'contextual', 'evidence']
    scope: ReviewScope

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicySummary:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyUnitDeclaration:
    ''
    __definition__: ClassVar[str] = 'PolicyUnitDeclaration'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'module': 'module',
        'heading_path': 'heading_path',
        'semantic_revision': 'semantic_revision',
        'lifecycle': 'lifecycle',
        'aliases': 'aliases',
        'predecessors': 'predecessors',
        'successors': 'successors',
    })
    kind: Literal['policy-unit']
    id: CanonicalId
    module: CanonicalId
    heading_path: tuple[NonEmptyString, ...]
    semantic_revision: int | float
    lifecycle: Literal['active']
    aliases: tuple[CanonicalId, ...] | MissingValue = MISSING
    predecessors: tuple[CanonicalId, ...] | MissingValue = MISSING
    successors: tuple[CanonicalId, ...] | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyUnitDeclaration:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PolicyUnitMapping:
    ''
    __definition__: ClassVar[str] = 'PolicyUnitMapping'
    __contract_fields__: ClassVar = MappingProxyType({
        'state': 'state',
        'reason': 'reason',
        'policy_units': 'policy_units',
    })
    state: Literal['exact-policy-unit', 'policy-units-present', 'incomplete']
    policy_units: tuple[CanonicalId, ...]
    reason: Literal['no-policy-units'] | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyUnitMapping:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PrepareCall:
    ''
    __definition__: ClassVar[str] = 'PrepareCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'request': 'request',
    })
    request: AnalysisRequest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PrepareCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PreservePolicySemantics:
    ''
    __definition__: ClassVar[str] = 'PreservePolicySemantics'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'semantic_revision': 'semantic_revision',
        'intent': 'intent',
    })
    kind: Literal['preserve']
    semantic_revision: int | float
    intent: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PreservePolicySemantics:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalHandle:
    ''
    __definition__: ClassVar[str] = 'ProposalHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['proposal-handle']
    id: ProposalId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalPolicySummary:
    ''
    __definition__: ClassVar[str] = 'ProposalPolicySummary'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'authority': 'authority',
        'scope': 'scope',
    })
    id: CanonicalId
    authority: Literal['normative', 'projection', 'contextual', 'evidence']
    scope: ReviewScope

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalPolicySummary:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalReadResult:
    ''
    __definition__: ClassVar[str] = 'ProposalReadResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'revision': 'revision',
        'policy': 'policy',
        'content': 'content',
        'requires': 'requires',
        'specializes': 'specializes',
        'related': 'related',
        'next_operations': 'next_operations',
        'summary': 'summary',
        'routing': 'routing',
        'coverage': 'coverage',
    })
    kind: Literal['proposal-read-result']
    revision: ProposalRevisionHandle
    policy: ProposalPolicySummary
    content: str
    requires: tuple[CanonicalId, ...]
    specializes: tuple[CanonicalId, ...]
    related: tuple[ProposalRelationshipSummary, ...]
    next_operations: tuple[QueryProposalNextOperation, ...]
    summary: str | MissingValue = MISSING
    routing: RoutingConfiguration | MissingValue = MISSING
    coverage: ReadCoverage | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalReadResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalRelatedResult:
    ''
    __definition__: ClassVar[str] = 'ProposalRelatedResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'revision': 'revision',
        'target': 'target',
        'authoring_target': 'authoring_target',
        'policy_unit_mapping': 'policy_unit_mapping',
        'relationships': 'relationships',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['proposal-related-result']
    revision: ProposalRevisionHandle
    target: CanonicalId
    policy_unit_mapping: PolicyUnitMapping
    relationships: tuple[ProposalRelationshipSummary, ...]
    next_operations: tuple[QueryProposalNextOperation, ...]
    authoring_target: AuthoringTargetHandle | MissingValue = MISSING
    summary: str | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalRelatedResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalRelationshipSummary:
    ''
    __definition__: ClassVar[str] = 'ProposalRelationshipSummary'
    __contract_fields__: ClassVar = MappingProxyType({
        'source': 'source',
        'target': 'target',
        'relation': 'relation',
        'groups': 'groups',
        'direction': 'direction',
        'traversal_eligible': 'traversal_eligible',
        'applicability': 'applicability',
    })
    source: CanonicalId
    target: CanonicalId
    relation: CanonicalId
    groups: tuple[CanonicalId, ...]
    direction: Literal['incoming', 'outgoing']
    traversal_eligible: bool
    applicability: Literal['true', 'false', 'unknown', 'not-declared']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalRelationshipSummary:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalRevisionHandle:
    ''
    __definition__: ClassVar[str] = 'ProposalRevisionHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['proposal-revision-handle']
    id: ProposalRevisionId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalRevisionHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalRouteResult:
    ''
    __definition__: ClassVar[str] = 'ProposalRouteResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'revision': 'revision',
        'reading_plan': 'reading_plan',
        'unresolved_questions': 'unresolved_questions',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['proposal-route-result']
    revision: ProposalRevisionHandle
    reading_plan: tuple[ReadingPlanEntry, ...]
    unresolved_questions: tuple[Question, ...]
    next_operations: tuple[QueryProposalNextOperation, ...]
    summary: str | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalRouteResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposalSummary:
    ''
    __definition__: ClassVar[str] = 'ProposalSummary'
    __contract_fields__: ClassVar = MappingProxyType({
        'proposal': 'proposal',
        'head_revision': 'head_revision',
    })
    proposal: ProposalHandle
    head_revision: ProposalRevisionHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposalSummary:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProposeCall:
    ''
    __definition__: ClassVar[str] = 'ProposeCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'snapshot': 'snapshot',
        'change_set': 'change_set',
    })
    change_set: StandardsChangeSet
    snapshot: SnapshotHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProposeCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    ''
    __definition__: ClassVar[str] = 'ProvenanceRecord'
    __contract_fields__: ClassVar = MappingProxyType({
        'snapshot': 'snapshot',
        'path': 'path',
    })
    snapshot: SnapshotHandle
    path: RepositoryPath

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProvenanceRecord:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProvideFactSubmission:
    ''
    __definition__: ClassVar[str] = 'ProvideFactSubmission'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'requirement': 'requirement',
        'value': 'value',
        'evidence': 'evidence',
    })
    kind: Literal['provide-fact']
    requirement: AnalysisChildHandle
    value: FactValue
    evidence: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProvideFactSubmission:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ProviderReference:
    ''
    __definition__: ClassVar[str] = 'ProviderReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'contract': 'contract',
        'contract_version': 'contract_version',
        'input_digest': 'input_digest',
    })
    id: CanonicalId
    contract: CanonicalId
    contract_version: NonEmptyString
    input_digest: Digest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProviderReference:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PutPolicyRelationshipEdit:
    ''
    __definition__: ClassVar[str] = 'PutPolicyRelationshipEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'relationship': 'relationship',
    })
    kind: Literal['put-policy-relationship']
    relationship: PolicyRelationship

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PutPolicyRelationshipEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PutRoutingFactEdit:
    ''
    __definition__: ClassVar[str] = 'PutRoutingFactEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'fact': 'fact',
        'rationale': 'rationale',
    })
    kind: Literal['put-routing-fact']
    fact: AuthoredRoutingFact
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PutRoutingFactEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class PutRoutingRuleEdit:
    ''
    __definition__: ClassVar[str] = 'PutRoutingRuleEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'rule': 'rule',
        'rationale': 'rationale',
    })
    kind: Literal['put-routing-rule']
    rule: AuthoredRoutingRule
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PutRoutingRuleEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class QuarantinedSnapshotSummary:
    ''
    __definition__: ClassVar[str] = 'QuarantinedSnapshotSummary'
    __contract_fields__: ClassVar = MappingProxyType({
        'snapshot': 'snapshot',
        'lifecycle': 'lifecycle',
        'source_revision': 'source_revision',
        'created_at': 'created_at',
        'purge_deadline': 'purge_deadline',
    })
    snapshot: SnapshotHandle
    lifecycle: Literal['quarantined']
    source_revision: NonEmptyString
    created_at: Timestamp
    purge_deadline: Timestamp

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> QuarantinedSnapshotSummary:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class QueryCall:
    ''
    __definition__: ClassVar[str] = 'QueryCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'snapshot': 'snapshot',
        'request': 'request',
    })
    snapshot: SnapshotHandle
    request: QueryRequest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> QueryCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class QueryNextOperation:
    ''
    __definition__: ClassVar[str] = 'QueryNextOperation'
    __contract_fields__: ClassVar = MappingProxyType({
        'operation': 'operation',
        'request_kind': 'request_kind',
        'target': 'target',
        'snapshot': 'snapshot',
    })
    operation: Literal['query']
    request_kind: Literal['route', 'read', 'related']
    snapshot: SnapshotHandle
    target: CanonicalId | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> QueryNextOperation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class QueryProposalCall:
    ''
    __definition__: ClassVar[str] = 'QueryProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'revision': 'revision',
        'request': 'request',
    })
    revision: ProposalRevisionHandle
    request: QueryRequest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> QueryProposalCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class QueryProposalNextOperation:
    ''
    __definition__: ClassVar[str] = 'QueryProposalNextOperation'
    __contract_fields__: ClassVar = MappingProxyType({
        'operation': 'operation',
        'request_kind': 'request_kind',
        'target': 'target',
        'revision': 'revision',
    })
    operation: Literal['query_proposal']
    request_kind: Literal['route', 'read', 'related']
    revision: ProposalRevisionHandle
    target: CanonicalId | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> QueryProposalNextOperation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class Question:
    ''
    __definition__: ClassVar[str] = 'Question'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'kind': 'kind',
        'prompt': 'prompt',
        'state': 'state',
        'permitted_answers': 'permitted_answers',
    })
    id: CanonicalId
    kind: Literal['applicability-fact', 'normative-classification', 'identity-resolution', 'scope-resolution']
    prompt: NonEmptyString
    state: Literal['required', 'answered', 'blocked']
    permitted_answers: tuple[NonEmptyString, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> Question:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReadCall:
    ''
    __definition__: ClassVar[str] = 'ReadCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'target': 'target',
        'include_routing': 'include_routing',
        'include_coverage': 'include_coverage',
        'snapshot': 'snapshot',
        'detail': 'detail',
    })
    target: CanonicalId
    include_routing: bool | MissingValue = MISSING
    include_coverage: bool | MissingValue = MISSING
    snapshot: SnapshotHandle | MissingValue = MISSING
    detail: Literal['compact', 'full'] | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReadCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReadCoverage:
    'Repository attestation status bound to this snapshot or proposal. Empty subjects means no registered policy units in scope, not complete coverage. Analysis-local attestations are not repository certificates.'
    __definition__: ClassVar[str] = 'ReadCoverage'
    __contract_fields__: ClassVar = MappingProxyType({
        'subjects': 'subjects',
    })
    subjects: tuple[PolicyCoverageStatus, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReadCoverage:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReadRequest:
    ''
    __definition__: ClassVar[str] = 'ReadRequest'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'target': 'target',
        'include_routing': 'include_routing',
        'include_coverage': 'include_coverage',
    })
    kind: Literal['read']
    target: CanonicalId
    include_routing: bool | MissingValue = MISSING
    include_coverage: bool | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReadRequest:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReadResult:
    ''
    __definition__: ClassVar[str] = 'ReadResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'policy': 'policy',
        'content': 'content',
        'requires': 'requires',
        'specializes': 'specializes',
        'related': 'related',
        'next_operations': 'next_operations',
        'summary': 'summary',
        'routing': 'routing',
        'coverage': 'coverage',
    })
    kind: Literal['read-result']
    snapshot: SnapshotHandle
    policy: PolicySummary
    content: str
    requires: tuple[CanonicalId, ...]
    specializes: tuple[CanonicalId, ...]
    related: tuple[RelationshipSummary, ...]
    next_operations: tuple[NextOperation, ...]
    summary: str | MissingValue = MISSING
    routing: RoutingConfiguration | MissingValue = MISSING
    coverage: ReadCoverage | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReadResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReadinessHandle:
    ''
    __definition__: ClassVar[str] = 'ReadinessHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['readiness-handle']
    id: ReadinessId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReadinessHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReadingPlanEntry:
    ''
    __definition__: ClassVar[str] = 'ReadingPlanEntry'
    __contract_fields__: ClassVar = MappingProxyType({
        'target': 'target',
        'scope': 'scope',
        'authority': 'authority',
        'reasons': 'reasons',
        'state': 'state',
    })
    target: CanonicalId
    scope: ReviewScope
    authority: Literal['normative', 'projection', 'contextual', 'evidence']
    reasons: tuple[ReadingPlanReason, ...]
    state: Literal['selected', 'conditional', 'unresolved']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReadingPlanEntry:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RecoverApplicationCall:
    ''
    __definition__: ClassVar[str] = 'RecoverApplicationCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'readiness': 'readiness',
    })
    kind: Literal['recover-application']
    readiness: ReadinessHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RecoverApplicationCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RecoverApplicationResult:
    ''
    __definition__: ClassVar[str] = 'RecoverApplicationResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'application': 'application',
        'status': 'status',
    })
    kind: Literal['recover-application-result']
    application: ApplicationHandle
    status: Literal['applied']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RecoverApplicationResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RecoverCall:
    ''
    __definition__: ClassVar[str] = 'RecoverCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
    })
    context: WorkflowContext

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RecoverCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RejectedResult:
    ''
    __definition__: ClassVar[str] = 'RejectedResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'code': 'code',
        'outcome': 'outcome',
        'target': 'target',
        'message': 'message',
        'details': 'details',
        'next_operations': 'next_operations',
    })
    kind: Literal['rejected-result']
    code: CanonicalId
    outcome: Literal['invalid', 'unavailable', 'unsupported', 'unauthorized']
    message: NonEmptyString
    details: FrozenMap[str, ScalarValue]
    next_operations: tuple[NextOperation, ...]
    target: NonEmptyString | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RejectedResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RelatedCall:
    ''
    __definition__: ClassVar[str] = 'RelatedCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'target': 'target',
        'groups': 'groups',
        'direction': 'direction',
        'transitive': 'transitive',
        'snapshot': 'snapshot',
    })
    target: CanonicalId
    groups: tuple[CanonicalId, ...]
    direction: Literal['incoming', 'outgoing', 'both']
    transitive: bool
    snapshot: SnapshotHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RelatedCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RelatedRequest:
    ''
    __definition__: ClassVar[str] = 'RelatedRequest'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'target': 'target',
        'groups': 'groups',
        'direction': 'direction',
        'transitive': 'transitive',
    })
    kind: Literal['related']
    target: CanonicalId
    groups: tuple[CanonicalId, ...]
    direction: Literal['incoming', 'outgoing', 'both']
    transitive: bool

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RelatedRequest:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RelatedResult:
    ''
    __definition__: ClassVar[str] = 'RelatedResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'target': 'target',
        'authoring_target': 'authoring_target',
        'policy_unit_mapping': 'policy_unit_mapping',
        'relationships': 'relationships',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['related-result']
    snapshot: SnapshotHandle
    target: CanonicalId
    policy_unit_mapping: PolicyUnitMapping
    relationships: tuple[RelationshipSummary, ...]
    next_operations: tuple[NextOperation, ...]
    authoring_target: AuthoringTargetHandle | MissingValue = MISSING
    summary: str | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RelatedResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RelationshipDisposition:
    ''
    __definition__: ClassVar[str] = 'RelationshipDisposition'
    __contract_fields__: ClassVar = MappingProxyType({
        'relationship': 'relationship',
        'disposition': 'disposition',
        'replacement_consumer': 'replacement_consumer',
        'rationale': 'rationale',
        'evidence': 'evidence',
    })
    relationship: RelationshipKey
    disposition: Literal['remove', 'retarget']
    rationale: NonEmptyString
    evidence: tuple[EvidenceReference, ...]
    replacement_consumer: RelationshipConsumer | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RelationshipDisposition:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RelationshipInspectionResult:
    ''
    __definition__: ClassVar[str] = 'RelationshipInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'relationship': 'relationship',
        'policy_semantics': 'policy_semantics',
        'provenance': 'provenance',
    })
    kind: Literal['relationship-inspection-result']
    relationship: RelationshipSummary
    policy_semantics: PolicyRelationshipInspection | None
    provenance: ProvenanceRecord

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RelationshipInspectionResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RelationshipSummary:
    ''
    __definition__: ClassVar[str] = 'RelationshipSummary'
    __contract_fields__: ClassVar = MappingProxyType({
        'handle': 'handle',
        'source': 'source',
        'target': 'target',
        'relation': 'relation',
        'groups': 'groups',
        'direction': 'direction',
        'traversal_eligible': 'traversal_eligible',
        'applicability': 'applicability',
    })
    handle: SnapshotChildHandle
    source: CanonicalId
    target: CanonicalId
    relation: CanonicalId
    groups: tuple[CanonicalId, ...]
    direction: Literal['incoming', 'outgoing']
    traversal_eligible: bool
    applicability: Literal['true', 'false', 'unknown', 'not-declared']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RelationshipSummary:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RemovePolicyRelationshipEdit:
    ''
    __definition__: ClassVar[str] = 'RemovePolicyRelationshipEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'relationship': 'relationship',
    })
    kind: Literal['remove-policy-relationship']
    relationship: PolicyRelationship

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RemovePolicyRelationshipEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RemoveRoutingFactEdit:
    ''
    __definition__: ClassVar[str] = 'RemoveRoutingFactEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'fact': 'fact',
        'rationale': 'rationale',
    })
    kind: Literal['remove-routing-fact']
    fact: CanonicalId
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RemoveRoutingFactEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RemoveRoutingRuleEdit:
    ''
    __definition__: ClassVar[str] = 'RemoveRoutingRuleEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'rule': 'rule',
        'rationale': 'rationale',
    })
    kind: Literal['remove-routing-rule']
    rule: CanonicalId
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RemoveRoutingRuleEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReplaceStandardRelationshipsEdit:
    ''
    __definition__: ClassVar[str] = 'ReplaceStandardRelationshipsEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'standard': 'standard',
        'requires': 'requires',
        'specializes': 'specializes',
        'rationale': 'rationale',
    })
    kind: Literal['replace-standard-relationships']
    standard: CanonicalId
    requires: tuple[CanonicalId, ...]
    specializes: tuple[CanonicalId, ...]
    rationale: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReplaceStandardRelationshipsEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RequiresReadingReason:
    ''
    __definition__: ClassVar[str] = 'RequiresReadingReason'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'edge': 'edge',
        'source': 'source',
    })
    kind: Literal['requires']
    edge: EdgeId
    source: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RequiresReadingReason:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ResolveCall:
    ''
    __definition__: ClassVar[str] = 'ResolveCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'analysis': 'analysis',
        'submission': 'submission',
    })
    analysis: AnalysisHandle
    submission: Submission

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ResolveCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ResolveNextOperation:
    ''
    __definition__: ClassVar[str] = 'ResolveNextOperation'
    __contract_fields__: ClassVar = MappingProxyType({
        'operation': 'operation',
        'request_kind': 'request_kind',
        'target': 'target',
        'work': 'work',
        'analysis': 'analysis',
    })
    operation: Literal['resolve']
    request_kind: Literal['provide-fact', 'consumer-disposition', 'impact-disposition', 'coverage-attestation']
    analysis: AnalysisHandle
    target: CanonicalId | MissingValue = MISSING
    work: AnalysisChildHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ResolveNextOperation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ResolveWorkflowCall:
    ''
    __definition__: ClassVar[str] = 'ResolveWorkflowCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
        'submission': 'submission',
    })
    context: WorkflowContext
    submission: Submission

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ResolveWorkflowCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ResumeCall:
    ''
    __definition__: ClassVar[str] = 'ResumeCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
    })
    context: WorkflowContext

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ResumeCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RetirePolicyUnitEdit:
    ''
    __definition__: ClassVar[str] = 'RetirePolicyUnitEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'policy': 'policy',
        'retired_semantic_revision': 'retired_semantic_revision',
        'successors': 'successors',
        'relationship_dispositions': 'relationship_dispositions',
        'evidence': 'evidence',
    })
    kind: Literal['retire-policy-unit']
    policy: CanonicalId
    retired_semantic_revision: int | float
    successors: tuple[CanonicalId, ...]
    relationship_dispositions: tuple[RelationshipDisposition, ...]
    evidence: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RetirePolicyUnitEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RetireStandardEdit:
    ''
    __definition__: ClassVar[str] = 'RetireStandardEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'standard': 'standard',
        'successors': 'successors',
        'relationship_dispositions': 'relationship_dispositions',
        'evidence': 'evidence',
    })
    kind: Literal['retire-standard']
    standard: CanonicalId
    successors: tuple[CanonicalId, ...]
    relationship_dispositions: tuple[RelationshipDisposition, ...]
    evidence: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RetireStandardEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviewCall:
    ''
    __definition__: ClassVar[str] = 'ReviewCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
        'decisions': 'decisions',
    })
    context: WorkflowContext
    decisions: tuple[ReviewDecision, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviewCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviewDecision:
    ''
    __definition__: ClassVar[str] = 'ReviewDecision'
    __contract_fields__: ClassVar = MappingProxyType({
        'owner': 'owner',
        'decision': 'decision',
        'rationale': 'rationale',
        'evidence': 'evidence',
    })
    owner: Literal['consumer', 'impact', 'audit']
    decision: Literal['accept']
    rationale: NonEmptyString
    evidence: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviewDecision:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviewProposalCall:
    ''
    __definition__: ClassVar[str] = 'ReviewProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'analysis': 'analysis',
        'decisions': 'decisions',
        'prior_readiness': 'prior_readiness',
    })
    kind: Literal['review-proposal']
    analysis: AnalysisHandle
    decisions: tuple[ReviewDecision, ...]
    prior_readiness: ReadinessHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviewProposalCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviewProposalResult:
    ''
    __definition__: ClassVar[str] = 'ReviewProposalResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'readiness': 'readiness',
        'revision': 'revision',
        'status': 'status',
    })
    kind: Literal['review-proposal-result']
    readiness: ReadinessHandle
    revision: ProposalRevisionHandle
    status: Literal['ready']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviewProposalResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviseCall:
    ''
    __definition__: ClassVar[str] = 'ReviseCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
        'change_set': 'change_set',
    })
    context: WorkflowContext
    change_set: StandardsChangeSet

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviseCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RevisePolicyUnitEdit:
    ''
    __definition__: ClassVar[str] = 'RevisePolicyUnitEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'policy': 'policy',
        'title': 'title',
        'body': 'body',
        'semantics': 'semantics',
    })
    kind: Literal['revise-policy-unit']
    policy: CanonicalId
    title: NonEmptyString
    body: NonEmptyString
    semantics: PolicySemanticIntent

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RevisePolicyUnitEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviseProposalCall:
    ''
    __definition__: ClassVar[str] = 'ReviseProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'expected_revision': 'expected_revision',
        'change_set': 'change_set',
    })
    kind: Literal['revise-proposal']
    expected_revision: ProposalRevisionHandle
    change_set: StandardsChangeSet

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviseProposalCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviseProposalResult:
    ''
    __definition__: ClassVar[str] = 'ReviseProposalResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'proposal': 'proposal',
        'revision': 'revision',
    })
    kind: Literal['revise-proposal-result']
    proposal: ProposalHandle
    revision: ProposalRevisionHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviseProposalResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ReviseStandardEdit:
    ''
    __definition__: ClassVar[str] = 'ReviseStandardEdit'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'standard': 'standard',
    })
    kind: Literal['revise-standard']
    standard: StandardContent

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReviseStandardEdit:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RouteCall:
    ''
    __definition__: ClassVar[str] = 'RouteCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'facts': 'facts',
        'snapshot': 'snapshot',
    })
    facts: FactSet
    snapshot: SnapshotHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RouteCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RouteRequest:
    ''
    __definition__: ClassVar[str] = 'RouteRequest'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'facts': 'facts',
    })
    kind: Literal['route']
    facts: FactSet

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RouteRequest:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RouteResult:
    ''
    __definition__: ClassVar[str] = 'RouteResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'reading_plan': 'reading_plan',
        'unresolved_questions': 'unresolved_questions',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['route-result']
    snapshot: SnapshotHandle
    reading_plan: tuple[ReadingPlanEntry, ...]
    unresolved_questions: tuple[Question, ...]
    next_operations: tuple[NextOperation, ...]
    summary: str | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RouteResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RoutingBaseReadingReason:
    ''
    __definition__: ClassVar[str] = 'RoutingBaseReadingReason'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'projection': 'projection',
    })
    kind: Literal['routing-base']
    projection: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RoutingBaseReadingReason:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RoutingConfiguration:
    ''
    __definition__: ClassVar[str] = 'RoutingConfiguration'
    __contract_fields__: ClassVar = MappingProxyType({
        'facts': 'facts',
        'rules': 'rules',
    })
    facts: tuple[AuthoredRoutingFact, ...]
    rules: tuple[AuthoredRoutingRule, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RoutingConfiguration:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RoutingFactsCall:
    ''
    __definition__: ClassVar[str] = 'RoutingFactsCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'snapshot': 'snapshot',
    })
    snapshot: SnapshotHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RoutingFactsCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RoutingFactsResult:
    ''
    __definition__: ClassVar[str] = 'RoutingFactsResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'facts': 'facts',
    })
    kind: Literal['routing-facts-result']
    snapshot: SnapshotHandle
    facts: tuple[AuthoredRoutingFact, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RoutingFactsResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RoutingQuestion:
    ''
    __definition__: ClassVar[str] = 'RoutingQuestion'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'kind': 'kind',
        'prompt': 'prompt',
        'state': 'state',
        'fact': 'fact',
    })
    id: CanonicalId
    kind: Literal['applicability-fact']
    prompt: NonEmptyString
    state: Literal['required']
    fact: AuthoredRoutingFact

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RoutingQuestion:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RoutingRuleExplanation:
    ''
    __definition__: ClassVar[str] = 'RoutingRuleExplanation'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'target': 'target',
        'when': 'when',
        'state': 'state',
    })
    id: CanonicalId
    target: CanonicalId
    when: ApplicabilityExpression
    state: Literal['selected', 'unresolved']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RoutingRuleExplanation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class RoutingRuleReadingReason:
    ''
    __definition__: ClassVar[str] = 'RoutingRuleReadingReason'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'rule': 'rule',
        'facts': 'facts',
    })
    kind: Literal['routing-rule']
    rule: CanonicalId
    facts: tuple[CanonicalId, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RoutingRuleReadingReason:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class SemanticProposal:
    ''
    __definition__: ClassVar[str] = 'SemanticProposal'
    __contract_fields__: ClassVar = MappingProxyType({
        'policy': 'policy',
        'accepted_semantic_revision': 'accepted_semantic_revision',
        'proposed_semantic_revision': 'proposed_semantic_revision',
        'intent': 'intent',
        'structural_digest': 'structural_digest',
    })
    policy: CanonicalId
    accepted_semantic_revision: int | float | None
    proposed_semantic_revision: int | float
    intent: NonEmptyString
    structural_digest: Digest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> SemanticProposal:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class SnapshotChildHandle:
    ''
    __definition__: ClassVar[str] = 'SnapshotChildHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
        'child_kind': 'child_kind',
        'child_id': 'child_id',
        'schema_version': 'schema_version',
    })
    kind: Literal['snapshot-child-handle']
    snapshot: SnapshotHandle
    child_kind: Literal['policy', 'relationship']
    child_id: NonEmptyString
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> SnapshotChildHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class SnapshotHandle:
    ''
    __definition__: ClassVar[str] = 'SnapshotHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['snapshot-handle']
    id: SnapshotId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> SnapshotHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class SnapshotInspectionResult:
    ''
    __definition__: ClassVar[str] = 'SnapshotInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
    })
    kind: Literal['snapshot-inspection-result']
    snapshot: SnapshotSummary

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> SnapshotInspectionResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class SpecializesReadingReason:
    ''
    __definition__: ClassVar[str] = 'SpecializesReadingReason'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'edge': 'edge',
        'source': 'source',
    })
    kind: Literal['specializes']
    edge: EdgeId
    source: CanonicalId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> SpecializesReadingReason:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class StandardContent:
    ''
    __definition__: ClassVar[str] = 'StandardContent'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'title': 'title',
        'role': 'role',
        'level': 'level',
        'applies_when': 'applies_when',
        'does_not_apply_when': 'does_not_apply_when',
        'verification': 'verification',
        'body': 'body',
    })
    id: CanonicalId
    title: NonEmptyString
    role: Literal['core', 'router', 'workflow', 'profile', 'topic', 'reference']
    level: Literal['MUST', 'SHOULD', 'PROFILE', 'REFERENCE']
    applies_when: NonEmptyString
    does_not_apply_when: NonEmptyString
    verification: NonEmptyString
    body: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> StandardContent:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class StandardsChangePurpose:
    ''
    __definition__: ClassVar[str] = 'StandardsChangePurpose'
    __contract_fields__: ClassVar = MappingProxyType({
        'summary': 'summary',
        'rationale': 'rationale',
        'evidence': 'evidence',
    })
    summary: NonEmptyString
    rationale: NonEmptyString
    evidence: tuple[EvidenceReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> StandardsChangePurpose:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class StandardsChangeSet:
    ''
    __definition__: ClassVar[str] = 'StandardsChangeSet'
    __contract_fields__: ClassVar = MappingProxyType({
        'purpose': 'purpose',
        'edits': 'edits',
    })
    purpose: StandardsChangePurpose
    edits: tuple[StandardEdit, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> StandardsChangeSet:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class StructuredScope:
    ''
    __definition__: ClassVar[str] = 'StructuredScope'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'heading_path': 'heading_path',
    })
    kind: Literal['structured']
    heading_path: tuple[NonEmptyString, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> StructuredScope:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class UndeleteSnapshotCall:
    ''
    __definition__: ClassVar[str] = 'UndeleteSnapshotCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
    })
    kind: Literal['undelete-snapshot']
    snapshot: SnapshotHandle

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> UndeleteSnapshotCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class UndeleteSnapshotResult:
    ''
    __definition__: ClassVar[str] = 'UndeleteSnapshotResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'snapshot': 'snapshot',
    })
    kind: Literal['undelete-snapshot-result']
    snapshot: ActiveSnapshotSummary

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> UndeleteSnapshotResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class VerificationFailure:
    ''
    __definition__: ClassVar[str] = 'VerificationFailure'
    __contract_fields__: ClassVar = MappingProxyType({
        'code': 'code',
        'message': 'message',
        'suite': 'suite',
        'check': 'check',
    })
    code: NonEmptyString
    message: NonEmptyString
    suite: object
    check: object

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> VerificationFailure:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class VerificationReport:
    ''
    __definition__: ClassVar[str] = 'VerificationReport'
    __contract_fields__: ClassVar = MappingProxyType({
        'passed': 'passed',
        'exit_code': 'exit_code',
        'suites': 'suites',
        'checks': 'checks',
        'failures': 'failures',
    })
    passed: bool
    exit_code: int | float
    suites: int | float
    checks: int | float
    failures: tuple[VerificationFailure, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> VerificationReport:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class VerifyProposalCall:
    ''
    __definition__: ClassVar[str] = 'VerifyProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'revision': 'revision',
        'readiness': 'readiness',
    })
    kind: Literal['verify-proposal']
    revision: ProposalRevisionHandle
    readiness: ReadinessHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> VerifyProposalCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class VerifyProposalResult:
    ''
    __definition__: ClassVar[str] = 'VerifyProposalResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'revision': 'revision',
        'verification': 'verification',
        'readiness': 'readiness',
    })
    kind: Literal['verify-proposal-result']
    revision: ProposalRevisionHandle
    verification: VerificationReport
    readiness: ReadinessHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> VerifyProposalResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class VerifyRepositoryCall:
    ''
    __definition__: ClassVar[str] = 'VerifyRepositoryCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'refresh_verification_inputs': 'refresh_verification_inputs',
    })
    kind: Literal['verify-repository']
    refresh_verification_inputs: bool

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> VerifyRepositoryCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class VerifyRepositoryResult:
    ''
    __definition__: ClassVar[str] = 'VerifyRepositoryResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'refreshed_verification_inputs': 'refreshed_verification_inputs',
        'verification': 'verification',
    })
    kind: Literal['verify-repository-result']
    refreshed_verification_inputs: bool
    verification: VerificationReport

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> VerifyRepositoryResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class WholeArtifactScope:
    ''
    __definition__: ClassVar[str] = 'WholeArtifactScope'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
    })
    kind: Literal['whole-artifact']

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> WholeArtifactScope:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class WorkflowContinuation:
    ''
    __definition__: ClassVar[str] = 'WorkflowContinuation'
    __contract_fields__: ClassVar = MappingProxyType({
        'operation': 'operation',
        'context': 'context',
        'required_inputs': 'required_inputs',
    })
    operation: Literal['revise', 'analyze', 'resolve_workflow', 'review', 'apply', 'recover', 'workflow_status', 'resume']
    context: WorkflowContext
    required_inputs: tuple[Literal['change_set', 'submission', 'decisions'], ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> WorkflowContinuation:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class WorkflowResult:
    ''
    __definition__: ClassVar[str] = 'WorkflowResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'context': 'context',
        'proposal': 'proposal',
        'revision': 'revision',
        'status': 'status',
        'next_operations': 'next_operations',
        'outcome': 'outcome',
    })
    kind: Literal['workflow-result']
    context: WorkflowContext
    proposal: ProposalHandle
    revision: ProposalRevisionHandle
    status: Literal['draft', 'needs-action', 'complete', 'requires-change', 'ready', 'recovery-required', 'applied', 'rejected', 'stale']
    next_operations: tuple[WorkflowContinuation, ...]
    outcome: WorkflowOutcome | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> WorkflowResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class WorkflowStatusCall:
    ''
    __definition__: ClassVar[str] = 'WorkflowStatusCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'context': 'context',
    })
    context: WorkflowContext

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> WorkflowStatusCall:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

AnalysisChildArtifact: TypeAlias = AnalysisContext | FactRequirement | FactObservation | Obligation | CoverageRequirement | CoverageCertificate
AnalysisId: TypeAlias = str
AnalysisMaterialHandle: TypeAlias = SnapshotHandle | ProposalRevisionHandle
ApplicabilityExpression: TypeAlias = AlwaysExpression | AllExpression | AnyExpression | NotExpression | EqualsExpression | InExpression | ContainsExpression | ExistsExpression
ApplicationId: TypeAlias = str
AuthorizationId: TypeAlias = str
CanonicalId: TypeAlias = str
ChildId: TypeAlias = str
Digest: TypeAlias = str
EdgeId: TypeAlias = str
FactRequirementId: TypeAlias = str
FactValue: TypeAlias = FrozenMap[str, object]
FactSet: TypeAlias = FrozenMap[str, FactValue]
ImpactTraceId: TypeAlias = str
InspectableHandle: TypeAlias = SnapshotHandle | AnalysisHandle | SnapshotChildHandle | AnalysisChildHandle
InspectionResult: TypeAlias = SnapshotInspectionResult | PolicyInspectionResult | RelationshipInspectionResult | AnalysisInspectionResult | AnalysisChildInspectionResult
NextOperation: TypeAlias = QueryNextOperation | ResolveNextOperation | InspectNextOperation
NonEmptyString: TypeAlias = str
ObligationId: TypeAlias = str
PolicySemanticIntent: TypeAlias = PreservePolicySemantics | ChangePolicySemantics
ProposalId: TypeAlias = str
ProposalRevisionId: TypeAlias = str
QueryProposalResult: TypeAlias = ProposalRouteResult | ProposalReadResult | ProposalRelatedResult
QueryRequest: TypeAlias = RouteRequest | ReadRequest | RelatedRequest
QueryResult: TypeAlias = RouteResult | ReadResult | RelatedResult
ReadinessId: TypeAlias = str
ReadingPlanReason: TypeAlias = ConsumerReviewObligationReadingReason | RoutingBaseReadingReason | RoutingRuleReadingReason | RequiresReadingReason | SpecializesReadingReason
RelationshipConsumer: TypeAlias = CanonicalId | AuthoringTargetHandle
RelationshipKey: TypeAlias = ModuleRelationshipKey | PolicyRelationshipKey
RepositoryPath: TypeAlias = tuple[NonEmptyString, ...]
ReviewScope: TypeAlias = StructuredScope | WholeArtifactScope
ScalarValue: TypeAlias = bool | int | float | str | None
SelectionReason: TypeAlias = GeneralSelectionReason | PolicyImpactSelectionReason
SnapshotId: TypeAlias = str
SnapshotSummary: TypeAlias = ActiveSnapshotSummary | QuarantinedSnapshotSummary
StandardEdit: TypeAlias = CreateStandardEdit | ReviseStandardEdit | RevisePolicyUnitEdit | MovePolicyUnitEdit | RetirePolicyUnitEdit | RetireStandardEdit | ReplaceStandardRelationshipsEdit | PutPolicyRelationshipEdit | RemovePolicyRelationshipEdit | PutRoutingRuleEdit | RemoveRoutingRuleEdit | PutRoutingFactEdit | RemoveRoutingFactEdit | AuditPolicyUnitEdit
Submission: TypeAlias = ProvideFactSubmission | ConsumerDispositionSubmission | ImpactDispositionSubmission | CoverageAttestationSubmission
Timestamp: TypeAlias = int | float
WorkflowContext: TypeAlias = ProposalRevisionHandle | AnalysisHandle | ReadinessHandle
WorkflowOutcome: TypeAlias = CreateProposalResult | ReviseProposalResult | PendingResult | CompleteResult | ReviewProposalResult | ApplyProposalResult | ApplicationRecoveryRequiredResult | RecoverApplicationResult | RejectedResult

MODEL_TYPES = MappingProxyType({
    'ActiveSnapshotSummary': ActiveSnapshotSummary,
    'AgentRouteResult': AgentRouteResult,
    'AllExpression': AllExpression,
    'AlwaysExpression': AlwaysExpression,
    'AnalysisChildHandle': AnalysisChildHandle,
    'AnalysisChildInspectionResult': AnalysisChildInspectionResult,
    'AnalysisContext': AnalysisContext,
    'AnalysisExecutionContractView': AnalysisExecutionContractView,
    'AnalysisHandle': AnalysisHandle,
    'AnalysisInspectionResult': AnalysisInspectionResult,
    'AnalysisRequest': AnalysisRequest,
    'AnalysisState': AnalysisState,
    'AnalyzeCall': AnalyzeCall,
    'AnalyzeProposalCall': AnalyzeProposalCall,
    'AnyExpression': AnyExpression,
    'ApplicationHandle': ApplicationHandle,
    'ApplicationRecoveryRequiredResult': ApplicationRecoveryRequiredResult,
    'ApplyCall': ApplyCall,
    'ApplyProposalCall': ApplyProposalCall,
    'ApplyProposalResult': ApplyProposalResult,
    'AuditPolicyUnitEdit': AuditPolicyUnitEdit,
    'AuthoredRoutingFact': AuthoredRoutingFact,
    'AuthoredRoutingRule': AuthoredRoutingRule,
    'AuthoringTargetHandle': AuthoringTargetHandle,
    'AuthorizationRecord': AuthorizationRecord,
    'AuthorizationReference': AuthorizationReference,
    'CanonicalModuleDeclaration': CanonicalModuleDeclaration,
    'ChangeDescriptor': ChangeDescriptor,
    'ChangePolicySemantics': ChangePolicySemantics,
    'ChangedPolicyUnit': ChangedPolicyUnit,
    'CompactReadResult': CompactReadResult,
    'CompleteResult': CompleteResult,
    'CompletionProof': CompletionProof,
    'ConsumerDispositionSubmission': ConsumerDispositionSubmission,
    'ConsumerReviewContract': ConsumerReviewContract,
    'ConsumerReviewObligationReadingReason': ConsumerReviewObligationReadingReason,
    'ContainsExpression': ContainsExpression,
    'CoverageAttestation': CoverageAttestation,
    'CoverageAttestationClaim': CoverageAttestationClaim,
    'CoverageAttestationSubmission': CoverageAttestationSubmission,
    'CoverageAuditAuthority': CoverageAuditAuthority,
    'CoverageCertificate': CoverageCertificate,
    'CoverageRequirement': CoverageRequirement,
    'CreateProposalCall': CreateProposalCall,
    'CreateProposalResult': CreateProposalResult,
    'CreateSnapshotCall': CreateSnapshotCall,
    'CreateSnapshotResult': CreateSnapshotResult,
    'CreateStandardEdit': CreateStandardEdit,
    'DecisionDependency': DecisionDependency,
    'DecisionFingerprint': DecisionFingerprint,
    'DeleteSnapshotCall': DeleteSnapshotCall,
    'DeleteSnapshotResult': DeleteSnapshotResult,
    'DispositionRecord': DispositionRecord,
    'DomainContractReference': DomainContractReference,
    'EqualsExpression': EqualsExpression,
    'EvidenceCheckRetirement': EvidenceCheckRetirement,
    'EvidenceConsumerRegistration': EvidenceConsumerRegistration,
    'EvidenceMaintenancePlan': EvidenceMaintenancePlan,
    'EvidenceReference': EvidenceReference,
    'EvidenceRelationshipUpdate': EvidenceRelationshipUpdate,
    'EvidenceSuiteDescription': EvidenceSuiteDescription,
    'ExistsExpression': ExistsExpression,
    'FactObservation': FactObservation,
    'FactRequirement': FactRequirement,
    'FactRequirementWork': FactRequirementWork,
    'FactValueContract': FactValueContract,
    'FindProposalsCall': FindProposalsCall,
    'FindProposalsResult': FindProposalsResult,
    'FindSnapshotsCall': FindSnapshotsCall,
    'FindSnapshotsResult': FindSnapshotsResult,
    'GeneralSelectionReason': GeneralSelectionReason,
    'ImpactDispositionSubmission': ImpactDispositionSubmission,
    'ImpactTraceReference': ImpactTraceReference,
    'InExpression': InExpression,
    'InspectCall': InspectCall,
    'InspectNextOperation': InspectNextOperation,
    'MaintainEvidenceCall': MaintainEvidenceCall,
    'MaintainEvidenceResult': MaintainEvidenceResult,
    'ModuleRelationshipKey': ModuleRelationshipKey,
    'MovePolicyUnitEdit': MovePolicyUnitEdit,
    'NewPolicyUnit': NewPolicyUnit,
    'NotExpression': NotExpression,
    'Obligation': Obligation,
    'PendingResult': PendingResult,
    'PolicyCoverageStatus': PolicyCoverageStatus,
    'PolicyImpactSelectionReason': PolicyImpactSelectionReason,
    'PolicyInspectionResult': PolicyInspectionResult,
    'PolicyRelationship': PolicyRelationship,
    'PolicyRelationshipInspection': PolicyRelationshipInspection,
    'PolicyRelationshipKey': PolicyRelationshipKey,
    'PolicySummary': PolicySummary,
    'PolicyUnitDeclaration': PolicyUnitDeclaration,
    'PolicyUnitMapping': PolicyUnitMapping,
    'PrepareCall': PrepareCall,
    'PreservePolicySemantics': PreservePolicySemantics,
    'ProposalHandle': ProposalHandle,
    'ProposalPolicySummary': ProposalPolicySummary,
    'ProposalReadResult': ProposalReadResult,
    'ProposalRelatedResult': ProposalRelatedResult,
    'ProposalRelationshipSummary': ProposalRelationshipSummary,
    'ProposalRevisionHandle': ProposalRevisionHandle,
    'ProposalRouteResult': ProposalRouteResult,
    'ProposalSummary': ProposalSummary,
    'ProposeCall': ProposeCall,
    'ProvenanceRecord': ProvenanceRecord,
    'ProvideFactSubmission': ProvideFactSubmission,
    'ProviderReference': ProviderReference,
    'PutPolicyRelationshipEdit': PutPolicyRelationshipEdit,
    'PutRoutingFactEdit': PutRoutingFactEdit,
    'PutRoutingRuleEdit': PutRoutingRuleEdit,
    'QuarantinedSnapshotSummary': QuarantinedSnapshotSummary,
    'QueryCall': QueryCall,
    'QueryNextOperation': QueryNextOperation,
    'QueryProposalCall': QueryProposalCall,
    'QueryProposalNextOperation': QueryProposalNextOperation,
    'Question': Question,
    'ReadCall': ReadCall,
    'ReadCoverage': ReadCoverage,
    'ReadRequest': ReadRequest,
    'ReadResult': ReadResult,
    'ReadinessHandle': ReadinessHandle,
    'ReadingPlanEntry': ReadingPlanEntry,
    'RecoverApplicationCall': RecoverApplicationCall,
    'RecoverApplicationResult': RecoverApplicationResult,
    'RecoverCall': RecoverCall,
    'RejectedResult': RejectedResult,
    'RelatedCall': RelatedCall,
    'RelatedRequest': RelatedRequest,
    'RelatedResult': RelatedResult,
    'RelationshipDisposition': RelationshipDisposition,
    'RelationshipInspectionResult': RelationshipInspectionResult,
    'RelationshipSummary': RelationshipSummary,
    'RemovePolicyRelationshipEdit': RemovePolicyRelationshipEdit,
    'RemoveRoutingFactEdit': RemoveRoutingFactEdit,
    'RemoveRoutingRuleEdit': RemoveRoutingRuleEdit,
    'ReplaceStandardRelationshipsEdit': ReplaceStandardRelationshipsEdit,
    'RequiresReadingReason': RequiresReadingReason,
    'ResolveCall': ResolveCall,
    'ResolveNextOperation': ResolveNextOperation,
    'ResolveWorkflowCall': ResolveWorkflowCall,
    'ResumeCall': ResumeCall,
    'RetirePolicyUnitEdit': RetirePolicyUnitEdit,
    'RetireStandardEdit': RetireStandardEdit,
    'ReviewCall': ReviewCall,
    'ReviewDecision': ReviewDecision,
    'ReviewProposalCall': ReviewProposalCall,
    'ReviewProposalResult': ReviewProposalResult,
    'ReviseCall': ReviseCall,
    'RevisePolicyUnitEdit': RevisePolicyUnitEdit,
    'ReviseProposalCall': ReviseProposalCall,
    'ReviseProposalResult': ReviseProposalResult,
    'ReviseStandardEdit': ReviseStandardEdit,
    'RouteCall': RouteCall,
    'RouteRequest': RouteRequest,
    'RouteResult': RouteResult,
    'RoutingBaseReadingReason': RoutingBaseReadingReason,
    'RoutingConfiguration': RoutingConfiguration,
    'RoutingFactsCall': RoutingFactsCall,
    'RoutingFactsResult': RoutingFactsResult,
    'RoutingQuestion': RoutingQuestion,
    'RoutingRuleExplanation': RoutingRuleExplanation,
    'RoutingRuleReadingReason': RoutingRuleReadingReason,
    'SemanticProposal': SemanticProposal,
    'SnapshotChildHandle': SnapshotChildHandle,
    'SnapshotHandle': SnapshotHandle,
    'SnapshotInspectionResult': SnapshotInspectionResult,
    'SpecializesReadingReason': SpecializesReadingReason,
    'StandardContent': StandardContent,
    'StandardsChangePurpose': StandardsChangePurpose,
    'StandardsChangeSet': StandardsChangeSet,
    'StructuredScope': StructuredScope,
    'UndeleteSnapshotCall': UndeleteSnapshotCall,
    'UndeleteSnapshotResult': UndeleteSnapshotResult,
    'VerificationFailure': VerificationFailure,
    'VerificationReport': VerificationReport,
    'VerifyProposalCall': VerifyProposalCall,
    'VerifyProposalResult': VerifyProposalResult,
    'VerifyRepositoryCall': VerifyRepositoryCall,
    'VerifyRepositoryResult': VerifyRepositoryResult,
    'WholeArtifactScope': WholeArtifactScope,
    'WorkflowContinuation': WorkflowContinuation,
    'WorkflowResult': WorkflowResult,
    'WorkflowStatusCall': WorkflowStatusCall,
})
_RUNTIME = ContractRuntime(_SCHEMA, MODEL_TYPES)

def decode_contract(definition: str, value: object) -> object:
    return _RUNTIME.decode(definition, value)

__all__ = (
    'ActiveSnapshotSummary',
    'AgentRouteResult',
    'AllExpression',
    'AlwaysExpression',
    'AnalysisChildArtifact',
    'AnalysisChildHandle',
    'AnalysisChildInspectionResult',
    'AnalysisContext',
    'AnalysisExecutionContractView',
    'AnalysisHandle',
    'AnalysisId',
    'AnalysisInspectionResult',
    'AnalysisMaterialHandle',
    'AnalysisRequest',
    'AnalysisState',
    'AnalyzeCall',
    'AnalyzeProposalCall',
    'AnyExpression',
    'ApplicabilityExpression',
    'ApplicationHandle',
    'ApplicationId',
    'ApplicationRecoveryRequiredResult',
    'ApplyCall',
    'ApplyProposalCall',
    'ApplyProposalResult',
    'AuditPolicyUnitEdit',
    'AuthoredRoutingFact',
    'AuthoredRoutingRule',
    'AuthoringTargetHandle',
    'AuthorizationId',
    'AuthorizationRecord',
    'AuthorizationReference',
    'CanonicalId',
    'CanonicalModuleDeclaration',
    'ChangeDescriptor',
    'ChangePolicySemantics',
    'ChangedPolicyUnit',
    'ChildId',
    'CompactReadResult',
    'CompleteResult',
    'CompletionProof',
    'ConsumerDispositionSubmission',
    'ConsumerReviewContract',
    'ConsumerReviewObligationReadingReason',
    'ContainsExpression',
    'CoverageAttestation',
    'CoverageAttestationClaim',
    'CoverageAttestationSubmission',
    'CoverageAuditAuthority',
    'CoverageCertificate',
    'CoverageRequirement',
    'CreateProposalCall',
    'CreateProposalResult',
    'CreateSnapshotCall',
    'CreateSnapshotResult',
    'CreateStandardEdit',
    'DecisionDependency',
    'DecisionFingerprint',
    'DeleteSnapshotCall',
    'DeleteSnapshotResult',
    'Digest',
    'DispositionRecord',
    'DomainContractReference',
    'EdgeId',
    'EqualsExpression',
    'EvidenceCheckRetirement',
    'EvidenceConsumerRegistration',
    'EvidenceMaintenancePlan',
    'EvidenceReference',
    'EvidenceRelationshipUpdate',
    'EvidenceSuiteDescription',
    'ExistsExpression',
    'FactObservation',
    'FactRequirement',
    'FactRequirementId',
    'FactRequirementWork',
    'FactSet',
    'FactValue',
    'FactValueContract',
    'FindProposalsCall',
    'FindProposalsResult',
    'FindSnapshotsCall',
    'FindSnapshotsResult',
    'GeneralSelectionReason',
    'ImpactDispositionSubmission',
    'ImpactTraceId',
    'ImpactTraceReference',
    'InExpression',
    'InspectCall',
    'InspectNextOperation',
    'InspectableHandle',
    'InspectionResult',
    'MaintainEvidenceCall',
    'MaintainEvidenceResult',
    'ModuleRelationshipKey',
    'MovePolicyUnitEdit',
    'NewPolicyUnit',
    'NextOperation',
    'NonEmptyString',
    'NotExpression',
    'Obligation',
    'ObligationId',
    'PendingResult',
    'PolicyCoverageStatus',
    'PolicyImpactSelectionReason',
    'PolicyInspectionResult',
    'PolicyRelationship',
    'PolicyRelationshipInspection',
    'PolicyRelationshipKey',
    'PolicySemanticIntent',
    'PolicySummary',
    'PolicyUnitDeclaration',
    'PolicyUnitMapping',
    'PrepareCall',
    'PreservePolicySemantics',
    'ProposalHandle',
    'ProposalId',
    'ProposalPolicySummary',
    'ProposalReadResult',
    'ProposalRelatedResult',
    'ProposalRelationshipSummary',
    'ProposalRevisionHandle',
    'ProposalRevisionId',
    'ProposalRouteResult',
    'ProposalSummary',
    'ProposeCall',
    'ProvenanceRecord',
    'ProvideFactSubmission',
    'ProviderReference',
    'PutPolicyRelationshipEdit',
    'PutRoutingFactEdit',
    'PutRoutingRuleEdit',
    'QuarantinedSnapshotSummary',
    'QueryCall',
    'QueryNextOperation',
    'QueryProposalCall',
    'QueryProposalNextOperation',
    'QueryProposalResult',
    'QueryRequest',
    'QueryResult',
    'Question',
    'ReadCall',
    'ReadCoverage',
    'ReadRequest',
    'ReadResult',
    'ReadinessHandle',
    'ReadinessId',
    'ReadingPlanEntry',
    'ReadingPlanReason',
    'RecoverApplicationCall',
    'RecoverApplicationResult',
    'RecoverCall',
    'RejectedResult',
    'RelatedCall',
    'RelatedRequest',
    'RelatedResult',
    'RelationshipConsumer',
    'RelationshipDisposition',
    'RelationshipInspectionResult',
    'RelationshipKey',
    'RelationshipSummary',
    'RemovePolicyRelationshipEdit',
    'RemoveRoutingFactEdit',
    'RemoveRoutingRuleEdit',
    'ReplaceStandardRelationshipsEdit',
    'RepositoryPath',
    'RequiresReadingReason',
    'ResolveCall',
    'ResolveNextOperation',
    'ResolveWorkflowCall',
    'ResumeCall',
    'RetirePolicyUnitEdit',
    'RetireStandardEdit',
    'ReviewCall',
    'ReviewDecision',
    'ReviewProposalCall',
    'ReviewProposalResult',
    'ReviewScope',
    'ReviseCall',
    'RevisePolicyUnitEdit',
    'ReviseProposalCall',
    'ReviseProposalResult',
    'ReviseStandardEdit',
    'RouteCall',
    'RouteRequest',
    'RouteResult',
    'RoutingBaseReadingReason',
    'RoutingConfiguration',
    'RoutingFactsCall',
    'RoutingFactsResult',
    'RoutingQuestion',
    'RoutingRuleExplanation',
    'RoutingRuleReadingReason',
    'ScalarValue',
    'SelectionReason',
    'SemanticProposal',
    'SnapshotChildHandle',
    'SnapshotHandle',
    'SnapshotId',
    'SnapshotInspectionResult',
    'SnapshotSummary',
    'SpecializesReadingReason',
    'StandardContent',
    'StandardEdit',
    'StandardsChangePurpose',
    'StandardsChangeSet',
    'StructuredScope',
    'Submission',
    'Timestamp',
    'UndeleteSnapshotCall',
    'UndeleteSnapshotResult',
    'VerificationFailure',
    'VerificationReport',
    'VerifyProposalCall',
    'VerifyProposalResult',
    'VerifyRepositoryCall',
    'VerifyRepositoryResult',
    'WholeArtifactScope',
    'WorkflowContext',
    'WorkflowContinuation',
    'WorkflowOutcome',
    'WorkflowResult',
    'WorkflowStatusCall',
    'DEFINITION_METADATA',
    'decode_contract',
)
