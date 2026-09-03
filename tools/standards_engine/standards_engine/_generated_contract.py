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

_SCHEMA = json.loads('{"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"https://coding-standards.local/contracts/standards-engine/a2-v19","title":"Standards Engine A2 contract","description":"Canonical typed contract for snapshot lifecycle, controlled authoring, navigation, inspection, and immutable standards-change analysis.","oneOf":[{"$ref":"#/$defs/CreateSnapshotCall"},{"$ref":"#/$defs/CreateSnapshotResult"},{"$ref":"#/$defs/FindSnapshotsCall"},{"$ref":"#/$defs/FindSnapshotsResult"},{"$ref":"#/$defs/CreateProposalCall"},{"$ref":"#/$defs/CreateProposalResult"},{"$ref":"#/$defs/FindProposalsCall"},{"$ref":"#/$defs/FindProposalsResult"},{"$ref":"#/$defs/ReviseProposalCall"},{"$ref":"#/$defs/ReviseProposalResult"},{"$ref":"#/$defs/QueryProposalCall"},{"$ref":"#/$defs/QueryProposalResult"},{"$ref":"#/$defs/AnalyzeProposalCall"},{"$ref":"#/$defs/ReviewProposalCall"},{"$ref":"#/$defs/ReviewProposalResult"},{"$ref":"#/$defs/ApplyProposalCall"},{"$ref":"#/$defs/ApplyProposalResult"},{"$ref":"#/$defs/ApplicationRecoveryRequiredResult"},{"$ref":"#/$defs/RecoverApplicationCall"},{"$ref":"#/$defs/RecoverApplicationResult"},{"$ref":"#/$defs/DeleteSnapshotCall"},{"$ref":"#/$defs/DeleteSnapshotResult"},{"$ref":"#/$defs/UndeleteSnapshotCall"},{"$ref":"#/$defs/UndeleteSnapshotResult"},{"$ref":"#/$defs/QueryCall"},{"$ref":"#/$defs/QueryResult"},{"$ref":"#/$defs/PrepareCall"},{"$ref":"#/$defs/PendingResult"},{"$ref":"#/$defs/CompleteResult"},{"$ref":"#/$defs/ResolveCall"},{"$ref":"#/$defs/InspectCall"},{"$ref":"#/$defs/InspectionResult"},{"$ref":"#/$defs/RejectedResult"}],"$defs":{"NonEmptyString":{"type":"string","minLength":1},"CanonicalId":{"type":"string","pattern":"^[A-Za-z0-9][A-Za-z0-9._:/-]*$"},"EdgeId":{"type":"string","minLength":1},"Digest":{"type":"string","pattern":"^sha256:[0-9a-f]{64}$"},"ObligationId":{"type":"string","pattern":"^obligation:sha256:[0-9a-f]{64}$"},"ImpactTraceId":{"type":"string","pattern":"^impact-trace:sha256:[0-9a-f]{64}$"},"FactRequirementId":{"type":"string","pattern":"^fact-requirement:sha256:[0-9a-f]{64}$"},"ScalarValue":{"oneOf":[{"type":"boolean"},{"type":"integer"},{"type":"string"},{"type":"null"}]},"FactValue":{"oneOf":[{"type":"object","required":["type","state","value"],"properties":{"type":{"const":"boolean"},"state":{"const":"known"},"value":{"type":"boolean"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"state":{"const":"known"},"value":{"type":"null"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["enum","string","canonical-id"]},"state":{"const":"known"},"value":{"type":"string"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["string-set","enum-set"]},"state":{"const":"known"},"value":{"type":"array","items":{"type":"string"},"uniqueItems":true}},"additionalProperties":false},{"type":"object","required":["type","state"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"state":{"enum":["known-absent","unknown"]}},"additionalProperties":false}]},"FactSet":{"type":"object","additionalProperties":{"$ref":"#/$defs/FactValue"}},"StructuredScope":{"type":"object","required":["kind","heading_path"],"properties":{"kind":{"const":"structured"},"heading_path":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/NonEmptyString"}}},"additionalProperties":false},"WholeArtifactScope":{"type":"object","required":["kind"],"properties":{"kind":{"const":"whole-artifact"}},"additionalProperties":false},"ReviewScope":{"oneOf":[{"$ref":"#/$defs/StructuredScope"},{"$ref":"#/$defs/WholeArtifactScope"}]},"AllExpression":{"type":"object","required":["operator","expressions"],"properties":{"operator":{"const":"all"},"expressions":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ApplicabilityExpression"}}},"additionalProperties":false},"AnyExpression":{"type":"object","required":["operator","expressions"],"properties":{"operator":{"const":"any"},"expressions":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ApplicabilityExpression"}}},"additionalProperties":false},"NotExpression":{"type":"object","required":["operator","expression"],"properties":{"operator":{"const":"not"},"expression":{"$ref":"#/$defs/ApplicabilityExpression"}},"additionalProperties":false},"EqualsExpression":{"type":"object","required":["operator","fact","value"],"properties":{"operator":{"const":"equals"},"fact":{"$ref":"#/$defs/CanonicalId"},"value":{"$ref":"#/$defs/ScalarValue"}},"additionalProperties":false},"InExpression":{"type":"object","required":["operator","fact","values"],"properties":{"operator":{"const":"in"},"fact":{"$ref":"#/$defs/CanonicalId"},"values":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ScalarValue"}}},"additionalProperties":false},"ContainsExpression":{"type":"object","required":["operator","fact","value"],"properties":{"operator":{"const":"contains"},"fact":{"$ref":"#/$defs/CanonicalId"},"value":{"$ref":"#/$defs/ScalarValue"}},"additionalProperties":false},"ExistsExpression":{"type":"object","required":["operator","fact"],"properties":{"operator":{"const":"exists"},"fact":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"AlwaysExpression":{"type":"object","required":["operator"],"properties":{"operator":{"const":"always"}},"additionalProperties":false},"ApplicabilityExpression":{"oneOf":[{"$ref":"#/$defs/AlwaysExpression"},{"$ref":"#/$defs/AllExpression"},{"$ref":"#/$defs/AnyExpression"},{"$ref":"#/$defs/NotExpression"},{"$ref":"#/$defs/EqualsExpression"},{"$ref":"#/$defs/InExpression"},{"$ref":"#/$defs/ContainsExpression"},{"$ref":"#/$defs/ExistsExpression"}]},"GeneralSelectionReason":{"type":"object","required":["kind"],"properties":{"kind":{"enum":["routing-fact","requires","specializes","changed-policy","question","audit-coverage","unmapped-normative-change","structured-scope-analysis-unsupported"]},"source":{"$ref":"#/$defs/CanonicalId"},"fact":{"$ref":"#/$defs/CanonicalId"},"edge":{"$ref":"#/$defs/EdgeId"},"question":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"PolicyImpactSelectionReason":{"type":"object","required":["kind","source","edge","relation","evidence_owner","traces"],"properties":{"kind":{"const":"policy-impact-edge"},"source":{"$ref":"#/$defs/CanonicalId"},"edge":{"$ref":"#/$defs/EdgeId"},"relation":{"$ref":"#/$defs/CanonicalId"},"evidence_owner":{"$ref":"#/$defs/CanonicalId"},"traces":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ImpactTraceReference"}}},"additionalProperties":false},"SelectionReason":{"oneOf":[{"$ref":"#/$defs/GeneralSelectionReason"},{"$ref":"#/$defs/PolicyImpactSelectionReason"}]},"ImpactTraceReference":{"type":"object","required":["id","graph","applicability"],"properties":{"id":{"$ref":"#/$defs/ImpactTraceId"},"graph":{"enum":["accepted","proposed"]},"applicability":{"enum":["true","false","unknown"]}},"additionalProperties":false},"ConsumerReviewObligationReadingReason":{"type":"object","required":["kind","obligation"],"properties":{"kind":{"const":"consumer-review-obligation"},"obligation":{"$ref":"#/$defs/ObligationId"}},"additionalProperties":false},"RoutingBaseReadingReason":{"type":"object","required":["kind","projection"],"properties":{"kind":{"const":"routing-base"},"projection":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"RoutingRuleReadingReason":{"type":"object","required":["kind","rule","facts"],"properties":{"kind":{"const":"routing-rule"},"rule":{"$ref":"#/$defs/CanonicalId"},"facts":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"RequiresReadingReason":{"type":"object","required":["kind","edge","source"],"properties":{"kind":{"const":"requires"},"edge":{"$ref":"#/$defs/EdgeId"},"source":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"SpecializesReadingReason":{"type":"object","required":["kind","edge","source"],"properties":{"kind":{"const":"specializes"},"edge":{"$ref":"#/$defs/EdgeId"},"source":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"ReadingPlanReason":{"oneOf":[{"$ref":"#/$defs/ConsumerReviewObligationReadingReason"},{"$ref":"#/$defs/RoutingBaseReadingReason"},{"$ref":"#/$defs/RoutingRuleReadingReason"},{"$ref":"#/$defs/RequiresReadingReason"},{"$ref":"#/$defs/SpecializesReadingReason"}]},"ReadingPlanEntry":{"type":"object","required":["target","scope","authority","reasons","state"],"properties":{"target":{"$ref":"#/$defs/CanonicalId"},"scope":{"$ref":"#/$defs/ReviewScope"},"authority":{"enum":["normative","projection","contextual","evidence"]},"reasons":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ReadingPlanReason"}},"state":{"enum":["selected","conditional","unresolved"]}},"additionalProperties":false},"RouteRequest":{"type":"object","required":["kind","facts"],"properties":{"kind":{"const":"route"},"facts":{"$ref":"#/$defs/FactSet"}},"additionalProperties":false},"ReadRequest":{"type":"object","required":["kind","target"],"properties":{"kind":{"const":"read"},"target":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"RelatedRequest":{"type":"object","required":["kind","target","groups","direction","transitive"],"properties":{"kind":{"const":"related"},"target":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"direction":{"enum":["incoming","outgoing","both"]},"transitive":{"type":"boolean","default":false}},"additionalProperties":false},"QueryRequest":{"oneOf":[{"$ref":"#/$defs/RouteRequest"},{"$ref":"#/$defs/ReadRequest"},{"$ref":"#/$defs/RelatedRequest"}]},"PolicyUnitDeclaration":{"type":"object","required":["kind","id","module","heading_path","semantic_revision","lifecycle"],"properties":{"kind":{"const":"policy-unit"},"id":{"$ref":"#/$defs/CanonicalId"},"module":{"$ref":"#/$defs/CanonicalId"},"heading_path":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/NonEmptyString"}},"semantic_revision":{"type":"integer","minimum":1},"lifecycle":{"const":"active"},"aliases":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"predecessors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"successors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"CanonicalModuleDeclaration":{"type":"object","required":["kind","id","role","level","applies_when","does_not_apply_when","requires","specializes","verification"],"properties":{"kind":{"const":"canonical-module"},"id":{"$ref":"#/$defs/CanonicalId"},"role":{"enum":["core","router","workflow","profile","topic","reference"]},"level":{"enum":["MUST","SHOULD","PROFILE","REFERENCE"]},"applies_when":{"$ref":"#/$defs/NonEmptyString"},"does_not_apply_when":{"$ref":"#/$defs/NonEmptyString"},"requires":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"specializes":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"verification":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PolicyRelationshipInspection":{"type":"object","required":["relationship_kind","applicability","source_scope","consumer_scope","propagation","evidence_owner","rationale"],"properties":{"relationship_kind":{"enum":["normative-consumer","router-projection","prompt-projection","template-projection","reference-projection","fixture-projection","enforcement-suite-projection","documentation-projection","implementation-projection"]},"applicability":{"$ref":"#/$defs/ApplicabilityExpression"},"source_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"consumer_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"propagation":{"const":"source-to-consumer"},"evidence_owner":{"$ref":"#/$defs/CanonicalId"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"SemanticProposal":{"type":"object","required":["policy","accepted_semantic_revision","proposed_semantic_revision","intent","structural_digest"],"properties":{"policy":{"$ref":"#/$defs/CanonicalId"},"accepted_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"proposed_semantic_revision":{"type":"integer","minimum":1},"intent":{"$ref":"#/$defs/NonEmptyString"},"structural_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"ChangeDescriptor":{"type":"object","required":["kind","accepted_ids","proposed_ids","scope"],"properties":{"kind":{"enum":["modification","addition","removal","move","split","merge"]},"accepted_ids":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"proposed_ids":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"scope":{"$ref":"#/$defs/ReviewScope"},"accepted_module":{"$ref":"#/$defs/CanonicalId"},"proposed_module":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"ChangedPolicyUnit":{"type":"object","required":["policy","change_kind","classification","accepted_representation_digest","proposed_representation_digest","accepted_structural_digest","proposed_structural_digest","accepted_semantic_revision","proposed_semantic_revision","semantic_state","scope"],"properties":{"policy":{"$ref":"#/$defs/CanonicalId"},"change_kind":{"enum":["modification","addition","removal","move","split-predecessor","split-successor","merge-predecessor","merge-successor"]},"classification":{"enum":["unchanged","representation-only-candidate","possibly-semantically-changed","semantically-changed","unresolved"]},"accepted_representation_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"proposed_representation_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"accepted_structural_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"proposed_structural_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"accepted_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"proposed_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"semantic_state":{"enum":["accepted-unchanged","proposed","removed","unresolved"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"Question":{"type":"object","required":["id","kind","prompt","state","permitted_answers"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"kind":{"enum":["applicability-fact","normative-classification","identity-resolution","scope-resolution"]},"prompt":{"$ref":"#/$defs/NonEmptyString"},"state":{"enum":["required","answered","blocked"]},"permitted_answers":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/NonEmptyString"}}},"additionalProperties":false},"ConsumerReviewContract":{"type":"object","required":["kind","id","version","permitted_dispositions","evidence_contract","authorization_capability","semantics"],"properties":{"kind":{"const":"consumer-review-contract"},"id":{"$ref":"#/$defs/CanonicalId"},"version":{"type":"integer","minimum":1},"permitted_dispositions":{"type":"array","minItems":1,"uniqueItems":true,"items":{"enum":["updated","reviewed-no-change","not-applicable","blocked"]}},"evidence_contract":{"$ref":"#/$defs/CanonicalId"},"authorization_capability":{"$ref":"#/$defs/CanonicalId"},"semantics":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"DecisionDependency":{"type":"object","required":["class","identity","digest"],"properties":{"class":{"enum":["policy-unit","semantic-revision","structure","representation","module-locator","applicability-fact","relationship","audit","exception","evidence","provider-contract","applicability-contract","analysis-contract"]},"identity":{"$ref":"#/$defs/NonEmptyString"},"digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"DecisionFingerprint":{"type":"object","required":["decision_kind","decision_contract","schema_version","dependencies"],"properties":{"decision_kind":{"$ref":"#/$defs/CanonicalId"},"decision_contract":{"$ref":"#/$defs/CanonicalId"},"schema_version":{"const":1},"dependencies":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/DecisionDependency"}}},"additionalProperties":false},"FactValueContract":{"type":"object","required":["type","states","nullable"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"states":{"const":["known","known-absent"]},"nullable":{"type":"boolean"},"values":{"type":"array","minItems":1,"uniqueItems":true,"items":{"type":"string"}}},"additionalProperties":false},"EvidenceReference":{"type":"object","required":["id","digest","provider_contract","provider_contract_version"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"digest":{"$ref":"#/$defs/Digest"},"provider_contract":{"$ref":"#/$defs/CanonicalId"},"provider_contract_version":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"CompletionProof":{"type":"object","required":["required_coverage_subjects","certificate_subjects","reached_consumer_obligations","disposition_obligations","required_fact_requirements","observed_fact_requirements","non_consumer_obligations_resolved","applicability_resolved","authorization_valid","evidence_valid"],"properties":{"required_coverage_subjects":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"certificate_subjects":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"reached_consumer_obligations":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/ObligationId"}},"disposition_obligations":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/ObligationId"}},"required_fact_requirements":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/FactRequirementId"}},"observed_fact_requirements":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/FactRequirementId"}},"non_consumer_obligations_resolved":{"const":true},"applicability_resolved":{"const":true},"authorization_valid":{"const":true},"evidence_valid":{"const":true}},"additionalProperties":false},"Timestamp":{"type":"integer","minimum":0},"SnapshotId":{"type":"string","pattern":"^snapshot:v1:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"},"AnalysisId":{"type":"string","pattern":"^analysis:sha256:[0-9a-f]{64}$"},"ProposalId":{"type":"string","pattern":"^proposal:v1:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"},"ProposalRevisionId":{"type":"string","pattern":"^proposal-revision:sha256:[0-9a-f]{64}$"},"ReadinessId":{"type":"string","pattern":"^readiness:sha256:[0-9a-f]{64}$"},"ApplicationId":{"type":"string","pattern":"^application:sha256:[0-9a-f]{64}$"},"ChildId":{"type":"string","pattern":"^sha256:[0-9a-f]{64}$"},"AuthorizationId":{"type":"string","pattern":"^authorization:sha256:[0-9a-f]{64}$"},"SnapshotHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"snapshot-handle"},"id":{"$ref":"#/$defs/SnapshotId"},"schema_version":{"const":5}},"additionalProperties":false},"AnalysisHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"analysis-handle"},"id":{"$ref":"#/$defs/AnalysisId"},"schema_version":{"const":6}},"additionalProperties":false},"ProposalHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"proposal-handle"},"id":{"$ref":"#/$defs/ProposalId"},"schema_version":{"const":1}},"additionalProperties":false},"ProposalRevisionHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"proposal-revision-handle"},"id":{"$ref":"#/$defs/ProposalRevisionId"},"schema_version":{"const":1}},"additionalProperties":false},"ReadinessHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"readiness-handle"},"id":{"$ref":"#/$defs/ReadinessId"},"schema_version":{"const":1}},"additionalProperties":false},"ApplicationHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"application-handle"},"id":{"$ref":"#/$defs/ApplicationId"},"schema_version":{"const":1}},"additionalProperties":false},"SnapshotChildHandle":{"type":"object","required":["kind","snapshot","child_kind","child_id","schema_version"],"properties":{"kind":{"const":"snapshot-child-handle"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"child_kind":{"enum":["policy","relationship"]},"child_id":{"$ref":"#/$defs/NonEmptyString"},"schema_version":{"const":5}},"additionalProperties":false},"AnalysisChildHandle":{"type":"object","required":["kind","analysis","child_kind","child_id","schema_version"],"properties":{"kind":{"const":"analysis-child-handle"},"analysis":{"$ref":"#/$defs/AnalysisHandle"},"child_kind":{"enum":["context","fact-requirement","fact-observation","obligation","coverage-requirement","coverage-certificate"]},"child_id":{"$ref":"#/$defs/ChildId"},"schema_version":{"const":6}},"additionalProperties":false},"AnalysisMaterialHandle":{"oneOf":[{"$ref":"#/$defs/SnapshotHandle"},{"$ref":"#/$defs/ProposalRevisionHandle"}]},"InspectableHandle":{"oneOf":[{"$ref":"#/$defs/SnapshotHandle"},{"$ref":"#/$defs/AnalysisHandle"},{"$ref":"#/$defs/SnapshotChildHandle"},{"$ref":"#/$defs/AnalysisChildHandle"}]},"ActiveSnapshotSummary":{"type":"object","required":["snapshot","lifecycle","source_revision","created_at"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"lifecycle":{"const":"active"},"source_revision":{"$ref":"#/$defs/NonEmptyString"},"created_at":{"$ref":"#/$defs/Timestamp"}},"additionalProperties":false},"QuarantinedSnapshotSummary":{"type":"object","required":["snapshot","lifecycle","source_revision","created_at","purge_deadline"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"lifecycle":{"const":"quarantined"},"source_revision":{"$ref":"#/$defs/NonEmptyString"},"created_at":{"$ref":"#/$defs/Timestamp"},"purge_deadline":{"$ref":"#/$defs/Timestamp"}},"additionalProperties":false},"SnapshotSummary":{"oneOf":[{"$ref":"#/$defs/ActiveSnapshotSummary"},{"$ref":"#/$defs/QuarantinedSnapshotSummary"}]},"CreateSnapshotCall":{"type":"object","required":["kind"],"properties":{"kind":{"const":"create-snapshot"}},"additionalProperties":false},"CreateSnapshotResult":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"create-snapshot-result"},"snapshot":{"$ref":"#/$defs/ActiveSnapshotSummary"}},"additionalProperties":false},"FindSnapshotsCall":{"type":"object","required":["kind"],"properties":{"kind":{"const":"find-snapshots"},"lifecycle":{"enum":["active","quarantined"],"default":"active"},"after":{"$ref":"#/$defs/SnapshotHandle"},"limit":{"type":"integer","minimum":1,"default":50}},"additionalProperties":false},"FindSnapshotsResult":{"type":"object","required":["kind","snapshots"],"properties":{"kind":{"const":"find-snapshots-result"},"snapshots":{"type":"array","items":{"$ref":"#/$defs/SnapshotSummary"}},"continuation":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"ReplacementMutation":{"type":"object","required":["op","path","value"],"properties":{"op":{"const":"replace"},"path":{"$ref":"#/$defs/NonEmptyString"},"value":{"type":"string"}},"additionalProperties":false},"ProposalSummary":{"type":"object","required":["proposal","head_revision"],"properties":{"proposal":{"$ref":"#/$defs/ProposalHandle"},"head_revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"CreateProposalCall":{"type":"object","required":["kind","base_snapshot","mutations","semantic_proposals"],"properties":{"kind":{"const":"create-proposal"},"base_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"mutations":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ReplacementMutation"}},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"}}},"additionalProperties":false},"CreateProposalResult":{"type":"object","required":["kind","proposal","revision"],"properties":{"kind":{"const":"create-proposal-result"},"proposal":{"$ref":"#/$defs/ProposalHandle"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"FindProposalsCall":{"type":"object","required":["kind"],"properties":{"kind":{"const":"find-proposals"},"after":{"$ref":"#/$defs/ProposalHandle"},"limit":{"type":"integer","minimum":1,"default":50}},"additionalProperties":false},"FindProposalsResult":{"type":"object","required":["kind","proposals"],"properties":{"kind":{"const":"find-proposals-result"},"proposals":{"type":"array","items":{"$ref":"#/$defs/ProposalSummary"}},"continuation":{"$ref":"#/$defs/ProposalHandle"}},"additionalProperties":false},"ReviseProposalCall":{"type":"object","required":["kind","expected_revision","mutations","semantic_proposals"],"properties":{"kind":{"const":"revise-proposal"},"expected_revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"mutations":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ReplacementMutation"}},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"}}},"additionalProperties":false},"ReviseProposalResult":{"type":"object","required":["kind","proposal","revision"],"properties":{"kind":{"const":"revise-proposal-result"},"proposal":{"$ref":"#/$defs/ProposalHandle"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"DeleteSnapshotCall":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"delete-snapshot"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"DeleteSnapshotResult":{"type":"object","required":["kind","snapshot","purge_deadline"],"properties":{"kind":{"const":"delete-snapshot-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"purge_deadline":{"$ref":"#/$defs/Timestamp"}},"additionalProperties":false},"UndeleteSnapshotCall":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"undelete-snapshot"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"UndeleteSnapshotResult":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"undelete-snapshot-result"},"snapshot":{"$ref":"#/$defs/ActiveSnapshotSummary"}},"additionalProperties":false},"QueryNextOperation":{"type":"object","required":["operation","request_kind","snapshot"],"properties":{"operation":{"const":"query"},"request_kind":{"enum":["route","read","related"]},"target":{"$ref":"#/$defs/CanonicalId"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"}},"additionalProperties":false},"QueryProposalNextOperation":{"type":"object","required":["operation","request_kind","revision"],"properties":{"operation":{"const":"query_proposal"},"request_kind":{"enum":["route","read","related"]},"target":{"$ref":"#/$defs/CanonicalId"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"ResolveNextOperation":{"type":"object","required":["operation","request_kind","analysis"],"properties":{"operation":{"const":"resolve"},"request_kind":{"enum":["provide-fact","consumer-disposition","impact-disposition","coverage-attestation"]},"target":{"$ref":"#/$defs/CanonicalId"},"work":{"$ref":"#/$defs/AnalysisChildHandle"},"analysis":{"$ref":"#/$defs/AnalysisHandle"}},"additionalProperties":false},"InspectNextOperation":{"type":"object","required":["operation","request_kind","handle"],"properties":{"operation":{"const":"inspect"},"request_kind":{"const":"inspect"},"handle":{"$ref":"#/$defs/InspectableHandle"}},"additionalProperties":false},"NextOperation":{"oneOf":[{"$ref":"#/$defs/QueryNextOperation"},{"$ref":"#/$defs/ResolveNextOperation"},{"$ref":"#/$defs/InspectNextOperation"}]},"QueryCall":{"type":"object","required":["snapshot","request"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"request":{"$ref":"#/$defs/QueryRequest"}},"additionalProperties":false},"QueryProposalCall":{"type":"object","required":["revision","request"],"properties":{"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"request":{"$ref":"#/$defs/QueryRequest"}},"additionalProperties":false},"AnalyzeProposalCall":{"type":"object","required":["revision"],"properties":{"revision":{"$ref":"#/$defs/ProposalRevisionHandle"}},"additionalProperties":false},"ReviewDecision":{"type":"object","required":["owner","decision","rationale","evidence"],"properties":{"owner":{"enum":["consumer","impact","audit"]},"decision":{"const":"accept"},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}}},"additionalProperties":false},"ReviewProposalCall":{"type":"object","required":["kind","analysis","decisions"],"properties":{"kind":{"const":"review-proposal"},"analysis":{"$ref":"#/$defs/AnalysisHandle"},"decisions":{"type":"array","minItems":3,"maxItems":3,"uniqueItems":true,"items":{"$ref":"#/$defs/ReviewDecision"}},"prior_readiness":{"$ref":"#/$defs/ReadinessHandle"}},"additionalProperties":false},"ReviewProposalResult":{"type":"object","required":["kind","readiness","revision","status"],"properties":{"kind":{"const":"review-proposal-result"},"readiness":{"$ref":"#/$defs/ReadinessHandle"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"status":{"const":"ready"}},"additionalProperties":false},"ApplyProposalCall":{"type":"object","required":["kind","readiness"],"properties":{"kind":{"const":"apply-proposal"},"readiness":{"$ref":"#/$defs/ReadinessHandle"}},"additionalProperties":false},"ApplyProposalResult":{"type":"object","required":["kind","application","status"],"properties":{"kind":{"const":"apply-proposal-result"},"application":{"$ref":"#/$defs/ApplicationHandle"},"status":{"const":"applied"}},"additionalProperties":false},"RecoverApplicationCall":{"type":"object","required":["kind","readiness"],"properties":{"kind":{"const":"recover-application"},"readiness":{"$ref":"#/$defs/ReadinessHandle"}},"additionalProperties":false},"RecoverApplicationResult":{"type":"object","required":["kind","application","status"],"properties":{"kind":{"const":"recover-application-result"},"application":{"$ref":"#/$defs/ApplicationHandle"},"status":{"const":"applied"}},"additionalProperties":false},"ApplicationRecoveryRequiredResult":{"type":"object","required":["kind","application","status","code","outcome","message"],"properties":{"kind":{"const":"application-recovery-required-result"},"application":{"$ref":"#/$defs/ApplicationHandle"},"status":{"const":"recovery-required"},"code":{"enum":["APPLICATION.PUBLICATION_UNAVAILABLE","APPLICATION.OBSERVATION_UNAVAILABLE","APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE","APPLICATION.RECOVERY_TARGET_UNCERTAIN","APPLICATION.RECOVERY_TARGET_DIVERGED"]},"outcome":{"const":"unavailable"},"message":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PolicySummary":{"type":"object","required":["handle","authority","scope"],"properties":{"handle":{"$ref":"#/$defs/SnapshotChildHandle"},"authority":{"enum":["normative","projection","contextual","evidence"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"RelationshipSummary":{"type":"object","required":["handle","source","target","relation","groups","direction","traversal_eligible","applicability"],"properties":{"handle":{"$ref":"#/$defs/SnapshotChildHandle"},"source":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"},"relation":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"minItems":1,"uniqueItems":true},"direction":{"enum":["incoming","outgoing"]},"traversal_eligible":{"type":"boolean"},"applicability":{"enum":["true","false","unknown","not-declared"]}},"additionalProperties":false},"ProposalPolicySummary":{"type":"object","required":["id","authority","scope"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"authority":{"enum":["normative","projection","contextual","evidence"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"ProposalRelationshipSummary":{"type":"object","required":["source","target","relation","groups","direction","traversal_eligible","applicability"],"properties":{"source":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"},"relation":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"minItems":1,"uniqueItems":true},"direction":{"enum":["incoming","outgoing"]},"traversal_eligible":{"type":"boolean"},"applicability":{"enum":["true","false","unknown","not-declared"]}},"additionalProperties":false},"RouteResult":{"type":"object","required":["kind","snapshot","reading_plan","unresolved_questions","next_operations"],"properties":{"kind":{"const":"route-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"unresolved_questions":{"type":"array","items":{"$ref":"#/$defs/Question"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"ReadResult":{"type":"object","required":["kind","snapshot","policy","content","requires","specializes","related","next_operations"],"properties":{"kind":{"const":"read-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"policy":{"$ref":"#/$defs/PolicySummary"},"content":{"type":"string"},"requires":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"specializes":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"related":{"type":"array","items":{"$ref":"#/$defs/RelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"PolicyUnitMapping":{"type":"object","required":["state","policy_units"],"properties":{"state":{"enum":["exact-policy-unit","policy-units-present","incomplete"]},"reason":{"const":"no-policy-units"},"policy_units":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true}},"additionalProperties":false},"RelatedResult":{"type":"object","required":["kind","snapshot","target","policy_unit_mapping","relationships","next_operations"],"properties":{"kind":{"const":"related-result"},"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"target":{"$ref":"#/$defs/CanonicalId"},"policy_unit_mapping":{"$ref":"#/$defs/PolicyUnitMapping"},"relationships":{"type":"array","items":{"$ref":"#/$defs/RelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"QueryResult":{"oneOf":[{"$ref":"#/$defs/RouteResult"},{"$ref":"#/$defs/ReadResult"},{"$ref":"#/$defs/RelatedResult"}]},"ProposalRouteResult":{"type":"object","required":["kind","revision","reading_plan","unresolved_questions","next_operations"],"properties":{"kind":{"const":"proposal-route-result"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"unresolved_questions":{"type":"array","items":{"$ref":"#/$defs/Question"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/QueryProposalNextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"ProposalReadResult":{"type":"object","required":["kind","revision","policy","content","requires","specializes","related","next_operations"],"properties":{"kind":{"const":"proposal-read-result"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"policy":{"$ref":"#/$defs/ProposalPolicySummary"},"content":{"type":"string"},"requires":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"specializes":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"related":{"type":"array","items":{"$ref":"#/$defs/ProposalRelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/QueryProposalNextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"ProposalRelatedResult":{"type":"object","required":["kind","revision","target","policy_unit_mapping","relationships","next_operations"],"properties":{"kind":{"const":"proposal-related-result"},"revision":{"$ref":"#/$defs/ProposalRevisionHandle"},"target":{"$ref":"#/$defs/CanonicalId"},"policy_unit_mapping":{"$ref":"#/$defs/PolicyUnitMapping"},"relationships":{"type":"array","items":{"$ref":"#/$defs/ProposalRelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/QueryProposalNextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"QueryProposalResult":{"oneOf":[{"$ref":"#/$defs/ProposalRouteResult"},{"$ref":"#/$defs/ProposalReadResult"},{"$ref":"#/$defs/ProposalRelatedResult"}]},"AnalysisRequest":{"type":"object","required":["kind","base_snapshot","proposed_snapshot","changes","semantic_proposals","contract_version"],"properties":{"kind":{"const":"analysis-request"},"base_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"proposed_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"},"minItems":1},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"},"uniqueItems":true},"prior_analysis":{"$ref":"#/$defs/AnalysisHandle"},"contract_version":{"const":4}},"additionalProperties":false},"PrepareCall":{"type":"object","required":["request"],"properties":{"request":{"$ref":"#/$defs/AnalysisRequest"}},"additionalProperties":false},"AnalysisContext":{"type":"object","required":["kind","handle","subjects","changes","semantic_proposals"],"properties":{"kind":{"const":"analysis-context"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"subjects":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"},"minItems":1,"uniqueItems":true},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"},"minItems":1,"uniqueItems":true},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"},"uniqueItems":true}},"additionalProperties":false},"AuthorizationReference":{"type":"object","required":["id","issuer","capability","authority_digest"],"properties":{"id":{"$ref":"#/$defs/AuthorizationId"},"issuer":{"$ref":"#/$defs/CanonicalId"},"capability":{"$ref":"#/$defs/CanonicalId"},"authority_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"ProviderReference":{"type":"object","required":["id","contract","contract_version","input_digest"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"contract":{"$ref":"#/$defs/CanonicalId"},"contract_version":{"$ref":"#/$defs/NonEmptyString"},"input_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"AuthorizationRecord":{"type":"object","required":["reference","issuer_semantic_revision","principal","action","subject_kind","subject_id","authorization_evidence","revocation_authority","revocation_authority_semantic_revision","revocation_evidence"],"properties":{"reference":{"$ref":"#/$defs/AuthorizationReference"},"issuer_semantic_revision":{"type":"integer","minimum":1},"principal":{"$ref":"#/$defs/CanonicalId"},"action":{"$ref":"#/$defs/CanonicalId"},"subject_kind":{"$ref":"#/$defs/CanonicalId"},"subject_id":{"$ref":"#/$defs/NonEmptyString"},"authorization_evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true},"revocation_authority":{"$ref":"#/$defs/CanonicalId"},"revocation_authority_semantic_revision":{"type":"integer","minimum":1},"revocation_evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true}},"additionalProperties":false},"DomainContractReference":{"type":"object","required":["id","version"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"version":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"AnalysisExecutionContractView":{"type":"object","required":["authorization_authority_digest","providers"],"properties":{"authorization_authority_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"providers":{"type":"array","items":{"$ref":"#/$defs/ProviderReference"},"uniqueItems":true}},"additionalProperties":false},"FactRequirement":{"type":"object","required":["kind","handle","fact","fact_semantic_revision","fact_contract_digest","context","value_contract","answer_contract","evidence_contract","authorization_capability"],"properties":{"kind":{"const":"fact-requirement"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"fact":{"$ref":"#/$defs/CanonicalId"},"fact_semantic_revision":{"type":"integer","minimum":1},"fact_contract_digest":{"$ref":"#/$defs/Digest"},"context":{"$ref":"#/$defs/AnalysisChildHandle"},"value_contract":{"$ref":"#/$defs/FactValueContract"},"answer_contract":{"$ref":"#/$defs/CanonicalId"},"evidence_contract":{"$ref":"#/$defs/CanonicalId"},"authorization_capability":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"FactRequirementWork":{"type":"object","required":["requirement","prompt","dependent_programs"],"properties":{"requirement":{"$ref":"#/$defs/FactRequirement"},"prompt":{"$ref":"#/$defs/NonEmptyString"},"dependent_programs":{"type":"array","items":{"$ref":"#/$defs/NonEmptyString"},"minItems":1,"uniqueItems":true}},"additionalProperties":false},"FactObservation":{"type":"object","required":["kind","handle","requirement","value","evidence","authorization"],"properties":{"kind":{"const":"fact-observation"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"value":{"$ref":"#/$defs/FactValue"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true},"authorization":{"$ref":"#/$defs/AuthorizationReference"},"provider":{"$ref":"#/$defs/ProviderReference"}},"additionalProperties":false},"Obligation":{"type":"object","required":["handle","kind","target","scope","reasons","state","permitted_submissions","fingerprint"],"properties":{"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"kind":{"enum":["consumer-review","impact-review","lifecycle-impact-review","audit-coverage","unmapped-normative-change"]},"target":{"$ref":"#/$defs/CanonicalId"},"scope":{"$ref":"#/$defs/ReviewScope"},"reasons":{"type":"array","items":{"$ref":"#/$defs/SelectionReason"},"minItems":1,"uniqueItems":true},"state":{"enum":["required","resolved","blocked"]},"applicability":{"enum":["true","false","unknown","not-declared"]},"permitted_submissions":{"type":"array","items":{"enum":["consumer-disposition","impact-disposition","coverage-attestation"]},"minItems":1,"uniqueItems":true},"review_contract":{"$ref":"#/$defs/ConsumerReviewContract"},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"ProvideFactSubmission":{"type":"object","required":["kind","requirement","value","evidence"],"properties":{"kind":{"const":"provide-fact"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"value":{"$ref":"#/$defs/FactValue"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true}},"additionalProperties":false},"ConsumerDispositionSubmission":{"type":"object","required":["kind","obligation","result","rationale","evidence","fingerprint"],"properties":{"kind":{"const":"consumer-disposition"},"obligation":{"$ref":"#/$defs/AnalysisChildHandle"},"result":{"enum":["updated","reviewed-no-change","not-applicable","blocked"]},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"ImpactDispositionSubmission":{"type":"object","required":["kind","obligation","result","rationale","evidence","fingerprint"],"properties":{"kind":{"const":"impact-disposition"},"obligation":{"$ref":"#/$defs/AnalysisChildHandle"},"result":{"enum":["confirmed","resolved-no-impact","requires-change","blocked"]},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"CoverageAttestationClaim":{"type":"object","required":["requirement","conclusion","evidence","explicit_exclusions","rationale","auditor_provenance"],"properties":{"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"conclusion":{"const":"complete"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1,"uniqueItems":true},"explicit_exclusions":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"uniqueItems":true},"rationale":{"$ref":"#/$defs/NonEmptyString"},"auditor_provenance":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"CoverageAttestationSubmission":{"type":"object","required":["kind","claim"],"properties":{"kind":{"const":"coverage-attestation"},"claim":{"$ref":"#/$defs/CoverageAttestationClaim"}},"additionalProperties":false},"Submission":{"oneOf":[{"$ref":"#/$defs/ProvideFactSubmission"},{"$ref":"#/$defs/ConsumerDispositionSubmission"},{"$ref":"#/$defs/ImpactDispositionSubmission"},{"$ref":"#/$defs/CoverageAttestationSubmission"}]},"ResolveCall":{"type":"object","required":["analysis","submission"],"properties":{"analysis":{"$ref":"#/$defs/AnalysisHandle"},"submission":{"$ref":"#/$defs/Submission"}},"additionalProperties":false},"CoverageRequirement":{"type":"object","required":["kind","handle","subject","owner","semantic_revision","relationship_kinds","horizon","required_evidence_contract"],"properties":{"kind":{"const":"coverage-requirement"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"subject":{"$ref":"#/$defs/CanonicalId"},"owner":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"relationship_kinds":{"type":"array","items":{"$ref":"#/$defs/CanonicalId"},"uniqueItems":true},"horizon":{"$ref":"#/$defs/CanonicalId"},"required_evidence_contract":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"CoverageAttestation":{"type":"object","required":["kind","requirement","conclusion","evidence","explicit_exclusions","rationale","auditor_provenance","schema_version","authorization"],"properties":{"kind":{"const":"coverage-attestation"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"conclusion":{"const":"complete"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"},"minItems":1},"explicit_exclusions":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"}},"rationale":{"$ref":"#/$defs/NonEmptyString"},"auditor_provenance":{"$ref":"#/$defs/NonEmptyString"},"schema_version":{"const":4},"authorization":{"$ref":"#/$defs/AuthorizationReference"}},"additionalProperties":false},"CoverageCertificate":{"type":"object","required":["kind","handle","requirement","subject","owner","semantic_revision","horizon_digest","relationship_digest","evidence_digests","fact_schema_digest"],"properties":{"kind":{"const":"coverage-certificate"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"requirement":{"$ref":"#/$defs/AnalysisChildHandle"},"subject":{"$ref":"#/$defs/CanonicalId"},"owner":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"horizon_digest":{"$ref":"#/$defs/Digest"},"relationship_digest":{"$ref":"#/$defs/Digest"},"evidence_digests":{"type":"array","items":{"$ref":"#/$defs/Digest"},"uniqueItems":true},"fact_schema_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"DispositionRecord":{"type":"object","required":["obligation","kind","result","rationale","evidence","authorization","fingerprint"],"properties":{"obligation":{"$ref":"#/$defs/AnalysisChildHandle"},"kind":{"enum":["consumer-disposition","impact-disposition"]},"result":{"$ref":"#/$defs/NonEmptyString"},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"}},"authorization":{"$ref":"#/$defs/AuthorizationReference"},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"AnalysisState":{"type":"object","required":["kind","handle","base_snapshot","proposed_reference","changes","semantic_proposals","fact_observations","dispositions","coverage_attestations","authorization_records","domain_contracts","execution_contracts","contract_version"],"properties":{"kind":{"const":"analysis-state"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"base_snapshot":{"$ref":"#/$defs/SnapshotHandle"},"proposed_reference":{"$ref":"#/$defs/AnalysisMaterialHandle"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"},"minItems":1,"uniqueItems":true},"semantic_proposals":{"type":"array","items":{"$ref":"#/$defs/SemanticProposal"},"uniqueItems":true},"fact_observations":{"type":"array","items":{"$ref":"#/$defs/FactObservation"},"uniqueItems":true},"dispositions":{"type":"array","items":{"$ref":"#/$defs/DispositionRecord"},"uniqueItems":true},"coverage_attestations":{"type":"array","items":{"$ref":"#/$defs/CoverageAttestation"},"uniqueItems":true},"authorization_records":{"type":"array","items":{"$ref":"#/$defs/AuthorizationRecord"},"uniqueItems":true},"domain_contracts":{"type":"array","items":{"$ref":"#/$defs/DomainContractReference"},"minItems":1,"uniqueItems":true},"execution_contracts":{"$ref":"#/$defs/AnalysisExecutionContractView"},"contract_version":{"const":5}},"additionalProperties":false},"PendingResult":{"type":"object","required":["kind","handle","status","context","changes","changed_units","obligations","fact_requirements","reading_plan","next_operations"],"properties":{"kind":{"const":"pending-result"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"status":{"const":"needs-action"},"context":{"$ref":"#/$defs/AnalysisContext"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"}},"changed_units":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"}},"obligations":{"type":"array","items":{"$ref":"#/$defs/Obligation"}},"fact_requirements":{"type":"array","items":{"$ref":"#/$defs/FactRequirementWork"}},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"CompleteResult":{"type":"object","required":["kind","handle","status","context","changes","changed_units","coverage_certificates","fact_observations","dispositions","reading_plan","completion"],"properties":{"kind":{"const":"complete-result"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"status":{"const":"complete"},"context":{"$ref":"#/$defs/AnalysisContext"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"}},"changed_units":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"}},"coverage_certificates":{"type":"array","items":{"$ref":"#/$defs/CoverageCertificate"},"uniqueItems":true},"fact_observations":{"type":"array","items":{"$ref":"#/$defs/FactObservation"},"uniqueItems":true},"dispositions":{"type":"array","items":{"$ref":"#/$defs/DispositionRecord"}},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"completion":{"$ref":"#/$defs/CompletionProof"},"summary":{"type":"string"}},"additionalProperties":false},"RepositoryPath":{"type":"array","items":{"$ref":"#/$defs/NonEmptyString"},"minItems":1},"ProvenanceRecord":{"type":"object","required":["snapshot","path"],"properties":{"snapshot":{"$ref":"#/$defs/SnapshotHandle"},"path":{"$ref":"#/$defs/RepositoryPath"}},"additionalProperties":false},"SnapshotInspectionResult":{"type":"object","required":["kind","snapshot"],"properties":{"kind":{"const":"snapshot-inspection-result"},"snapshot":{"$ref":"#/$defs/SnapshotSummary"}},"additionalProperties":false},"PolicyInspectionResult":{"type":"object","required":["kind","policy","declaration","representation_digest","structural_digest","provenance"],"properties":{"kind":{"const":"policy-inspection-result"},"policy":{"$ref":"#/$defs/SnapshotChildHandle"},"declaration":{"oneOf":[{"$ref":"#/$defs/CanonicalModuleDeclaration"},{"$ref":"#/$defs/PolicyUnitDeclaration"}]},"representation_digest":{"$ref":"#/$defs/Digest"},"structural_digest":{"$ref":"#/$defs/Digest"},"provenance":{"$ref":"#/$defs/ProvenanceRecord"}},"additionalProperties":false},"RelationshipInspectionResult":{"type":"object","required":["kind","relationship","policy_semantics","provenance"],"properties":{"kind":{"const":"relationship-inspection-result"},"relationship":{"$ref":"#/$defs/RelationshipSummary"},"policy_semantics":{"oneOf":[{"$ref":"#/$defs/PolicyRelationshipInspection"},{"type":"null"}]},"provenance":{"$ref":"#/$defs/ProvenanceRecord"}},"additionalProperties":false},"AnalysisInspectionResult":{"type":"object","required":["kind","state"],"properties":{"kind":{"const":"analysis-inspection-result"},"state":{"$ref":"#/$defs/AnalysisState"}},"additionalProperties":false},"AnalysisChildArtifact":{"oneOf":[{"$ref":"#/$defs/AnalysisContext"},{"$ref":"#/$defs/FactRequirement"},{"$ref":"#/$defs/FactObservation"},{"$ref":"#/$defs/Obligation"},{"$ref":"#/$defs/CoverageRequirement"},{"$ref":"#/$defs/CoverageCertificate"}]},"AnalysisChildInspectionResult":{"type":"object","required":["kind","handle","artifact"],"properties":{"kind":{"const":"analysis-child-inspection-result"},"handle":{"$ref":"#/$defs/AnalysisChildHandle"},"artifact":{"$ref":"#/$defs/AnalysisChildArtifact"}},"additionalProperties":false},"InspectionResult":{"oneOf":[{"$ref":"#/$defs/SnapshotInspectionResult"},{"$ref":"#/$defs/PolicyInspectionResult"},{"$ref":"#/$defs/RelationshipInspectionResult"},{"$ref":"#/$defs/AnalysisInspectionResult"},{"$ref":"#/$defs/AnalysisChildInspectionResult"}]},"InspectCall":{"type":"object","required":["handle"],"properties":{"handle":{"$ref":"#/$defs/InspectableHandle"}},"additionalProperties":false},"RejectedResult":{"type":"object","required":["kind","code","outcome","message","details","next_operations"],"properties":{"kind":{"const":"rejected-result"},"code":{"$ref":"#/$defs/CanonicalId"},"outcome":{"enum":["invalid","unavailable","unsupported","unauthorized"]},"target":{"$ref":"#/$defs/NonEmptyString"},"message":{"$ref":"#/$defs/NonEmptyString"},"details":{"type":"object","additionalProperties":{"$ref":"#/$defs/ScalarValue"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}}},"additionalProperties":false}}}')
DEFINITION_METADATA = freeze_json({'ActiveSnapshotSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'created_at': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AllExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expressions': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AlwaysExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisChildArtifact': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisChildHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisChildInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'artifact': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisContext': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisExecutionContractView': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'authorization_authority_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'providers': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisMaterialHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'base_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prior_analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisState': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'base_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_reference': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_observations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_attestations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_records': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'domain_contracts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'execution_contracts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalyzeProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnyExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expressions': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplicabilityExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ApplicationHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplicationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ApplicationRecoveryRequiredResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'application': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'code': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'outcome': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'message': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplyProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplyProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'application': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthorizationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AuthorizationRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'reference': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'issuer_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'principal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'action': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revocation_authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revocation_authority_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revocation_evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthorizationReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'issuer': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'capability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CanonicalId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CanonicalModuleDeclaration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'role': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'level': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applies_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'does_not_apply_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'verification': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChangeDescriptor': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_ids': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_ids': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_module': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_module': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChangedPolicyUnit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'change_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'classification': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChildId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CompleteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changed_units': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_certificates': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_observations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'completion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CompletionProof': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'required_coverage_subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'certificate_subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reached_consumer_obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'disposition_obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'required_fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'observed_fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'non_consumer_obligations_resolved': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability_resolved': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_valid': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_valid': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerDispositionSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerReviewContract': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_capability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerReviewObligationReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ContainsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'conclusion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'explicit_exclusions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'auditor_provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationClaim': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'conclusion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'explicit_exclusions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'auditor_provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'claim': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageCertificate': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'horizon_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_digests': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_schema_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageRequirement': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_kinds': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'horizon': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'required_evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'base_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'mutations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateSnapshotCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CreateSnapshotResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DecisionDependency': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'class': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'identity': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DecisionFingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'decision_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decision_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dependencies': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DeleteSnapshotCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DeleteSnapshotResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'purge_deadline': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Digest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'DispositionRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DomainContractReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EdgeId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'EqualsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EvidenceReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider_contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ExistsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactObservation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirement': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_contract_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'answer_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_capability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirementId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactRequirementWork': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dependent_programs': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactSet': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactValue': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactValueContract': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'type': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'states': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'nullable': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'values': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FindProposalsCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'after': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'limit': {'title': None, 'description': None, 'has_default': True, 'default': 50}}}, 'FindProposalsResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'continuation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FindSnapshotsCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': True, 'default': 'active'}, 'after': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'limit': {'title': None, 'description': None, 'has_default': True, 'default': 50}}}, 'FindSnapshotsResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshots': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'continuation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'GeneralSelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'question': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ImpactDispositionSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ImpactTraceId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ImpactTraceReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'graph': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'values': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectableHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'InspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NonEmptyString': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NotExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expression': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Obligation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reasons': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_submissions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'review_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ObligationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'PendingResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changed_units': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyImpactSelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traces': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'declaration': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyRelationshipInspection': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'relationship_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'propagation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicySummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyUnitDeclaration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'module': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'heading_path': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'aliases': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'predecessors': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'successors': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyUnitMapping': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reason': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_units': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PrepareCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ProposalPolicySummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalReadResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'related': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRelatedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_unit_mapping': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationships': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRelationshipSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traversal_eligible': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRevisionHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalRevisionId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ProposalRouteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'unresolved_questions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProposalSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'proposal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'head_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProvenanceRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'path': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProvideFactSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProviderReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'input_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QuarantinedSnapshotSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'created_at': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'purge_deadline': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryProposalNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'QueryRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'QueryResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'Question': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_answers': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'related': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadinessHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadinessId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ReadingPlanEntry': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reasons': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadingPlanReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RecoverApplicationCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RecoverApplicationResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'application': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RejectedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'code': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'outcome': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'message': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'details': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelatedRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'transitive': {'title': None, 'description': None, 'has_default': True, 'default': False}}}, 'RelatedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_unit_mapping': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationships': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traversal_eligible': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReplacementMutation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'op': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'path': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RepositoryPath': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RequiresReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResolveCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'submission': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResolveNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'work': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewDecision': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decisions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prior_readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'readiness': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ReviseProposalCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expected_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'mutations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviseProposalResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposal': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'revision': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RouteRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RouteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'unresolved_questions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingBaseReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'projection': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingRuleReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rule': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ScalarValue': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SemanticProposal': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'intent': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotChildHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'child_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SnapshotInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SnapshotSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SpecializesReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StructuredScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'heading_path': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Submission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'Timestamp': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'UndeleteSnapshotCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'UndeleteSnapshotResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'WholeArtifactScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}}}})

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
    kind: Literal['modification', 'addition', 'removal', 'move', 'split', 'merge']
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
        'mutations': 'mutations',
        'semantic_proposals': 'semantic_proposals',
    })
    kind: Literal['create-proposal']
    base_snapshot: SnapshotHandle
    mutations: tuple[ReplacementMutation, ...]
    semantic_proposals: tuple[SemanticProposal, ...]

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
class ReadRequest:
    ''
    __definition__: ClassVar[str] = 'ReadRequest'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'target': 'target',
    })
    kind: Literal['read']
    target: CanonicalId

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
class ReplacementMutation:
    ''
    __definition__: ClassVar[str] = 'ReplacementMutation'
    __contract_fields__: ClassVar = MappingProxyType({
        'op': 'op',
        'path': 'path',
        'value': 'value',
    })
    op: Literal['replace']
    path: NonEmptyString
    value: str

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ReplacementMutation:
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
class ReviseProposalCall:
    ''
    __definition__: ClassVar[str] = 'ReviseProposalCall'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'expected_revision': 'expected_revision',
        'mutations': 'mutations',
        'semantic_proposals': 'semantic_proposals',
    })
    kind: Literal['revise-proposal']
    expected_revision: ProposalRevisionHandle
    mutations: tuple[ReplacementMutation, ...]
    semantic_proposals: tuple[SemanticProposal, ...]

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
ProposalId: TypeAlias = str
ProposalRevisionId: TypeAlias = str
QueryProposalResult: TypeAlias = ProposalRouteResult | ProposalReadResult | ProposalRelatedResult
QueryRequest: TypeAlias = RouteRequest | ReadRequest | RelatedRequest
QueryResult: TypeAlias = RouteResult | ReadResult | RelatedResult
ReadinessId: TypeAlias = str
ReadingPlanReason: TypeAlias = ConsumerReviewObligationReadingReason | RoutingBaseReadingReason | RoutingRuleReadingReason | RequiresReadingReason | SpecializesReadingReason
RepositoryPath: TypeAlias = tuple[NonEmptyString, ...]
ReviewScope: TypeAlias = StructuredScope | WholeArtifactScope
ScalarValue: TypeAlias = bool | int | float | str | None
SelectionReason: TypeAlias = GeneralSelectionReason | PolicyImpactSelectionReason
SnapshotId: TypeAlias = str
SnapshotSummary: TypeAlias = ActiveSnapshotSummary | QuarantinedSnapshotSummary
Submission: TypeAlias = ProvideFactSubmission | ConsumerDispositionSubmission | ImpactDispositionSubmission | CoverageAttestationSubmission
Timestamp: TypeAlias = int | float

MODEL_TYPES = MappingProxyType({
    'ActiveSnapshotSummary': ActiveSnapshotSummary,
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
    'AnalyzeProposalCall': AnalyzeProposalCall,
    'AnyExpression': AnyExpression,
    'ApplicationHandle': ApplicationHandle,
    'ApplicationRecoveryRequiredResult': ApplicationRecoveryRequiredResult,
    'ApplyProposalCall': ApplyProposalCall,
    'ApplyProposalResult': ApplyProposalResult,
    'AuthorizationRecord': AuthorizationRecord,
    'AuthorizationReference': AuthorizationReference,
    'CanonicalModuleDeclaration': CanonicalModuleDeclaration,
    'ChangeDescriptor': ChangeDescriptor,
    'ChangedPolicyUnit': ChangedPolicyUnit,
    'CompleteResult': CompleteResult,
    'CompletionProof': CompletionProof,
    'ConsumerDispositionSubmission': ConsumerDispositionSubmission,
    'ConsumerReviewContract': ConsumerReviewContract,
    'ConsumerReviewObligationReadingReason': ConsumerReviewObligationReadingReason,
    'ContainsExpression': ContainsExpression,
    'CoverageAttestation': CoverageAttestation,
    'CoverageAttestationClaim': CoverageAttestationClaim,
    'CoverageAttestationSubmission': CoverageAttestationSubmission,
    'CoverageCertificate': CoverageCertificate,
    'CoverageRequirement': CoverageRequirement,
    'CreateProposalCall': CreateProposalCall,
    'CreateProposalResult': CreateProposalResult,
    'CreateSnapshotCall': CreateSnapshotCall,
    'CreateSnapshotResult': CreateSnapshotResult,
    'DecisionDependency': DecisionDependency,
    'DecisionFingerprint': DecisionFingerprint,
    'DeleteSnapshotCall': DeleteSnapshotCall,
    'DeleteSnapshotResult': DeleteSnapshotResult,
    'DispositionRecord': DispositionRecord,
    'DomainContractReference': DomainContractReference,
    'EqualsExpression': EqualsExpression,
    'EvidenceReference': EvidenceReference,
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
    'NotExpression': NotExpression,
    'Obligation': Obligation,
    'PendingResult': PendingResult,
    'PolicyImpactSelectionReason': PolicyImpactSelectionReason,
    'PolicyInspectionResult': PolicyInspectionResult,
    'PolicyRelationshipInspection': PolicyRelationshipInspection,
    'PolicySummary': PolicySummary,
    'PolicyUnitDeclaration': PolicyUnitDeclaration,
    'PolicyUnitMapping': PolicyUnitMapping,
    'PrepareCall': PrepareCall,
    'ProposalHandle': ProposalHandle,
    'ProposalPolicySummary': ProposalPolicySummary,
    'ProposalReadResult': ProposalReadResult,
    'ProposalRelatedResult': ProposalRelatedResult,
    'ProposalRelationshipSummary': ProposalRelationshipSummary,
    'ProposalRevisionHandle': ProposalRevisionHandle,
    'ProposalRouteResult': ProposalRouteResult,
    'ProposalSummary': ProposalSummary,
    'ProvenanceRecord': ProvenanceRecord,
    'ProvideFactSubmission': ProvideFactSubmission,
    'ProviderReference': ProviderReference,
    'QuarantinedSnapshotSummary': QuarantinedSnapshotSummary,
    'QueryCall': QueryCall,
    'QueryNextOperation': QueryNextOperation,
    'QueryProposalCall': QueryProposalCall,
    'QueryProposalNextOperation': QueryProposalNextOperation,
    'Question': Question,
    'ReadRequest': ReadRequest,
    'ReadResult': ReadResult,
    'ReadinessHandle': ReadinessHandle,
    'ReadingPlanEntry': ReadingPlanEntry,
    'RecoverApplicationCall': RecoverApplicationCall,
    'RecoverApplicationResult': RecoverApplicationResult,
    'RejectedResult': RejectedResult,
    'RelatedRequest': RelatedRequest,
    'RelatedResult': RelatedResult,
    'RelationshipInspectionResult': RelationshipInspectionResult,
    'RelationshipSummary': RelationshipSummary,
    'ReplacementMutation': ReplacementMutation,
    'RequiresReadingReason': RequiresReadingReason,
    'ResolveCall': ResolveCall,
    'ResolveNextOperation': ResolveNextOperation,
    'ReviewDecision': ReviewDecision,
    'ReviewProposalCall': ReviewProposalCall,
    'ReviewProposalResult': ReviewProposalResult,
    'ReviseProposalCall': ReviseProposalCall,
    'ReviseProposalResult': ReviseProposalResult,
    'RouteRequest': RouteRequest,
    'RouteResult': RouteResult,
    'RoutingBaseReadingReason': RoutingBaseReadingReason,
    'RoutingRuleReadingReason': RoutingRuleReadingReason,
    'SemanticProposal': SemanticProposal,
    'SnapshotChildHandle': SnapshotChildHandle,
    'SnapshotHandle': SnapshotHandle,
    'SnapshotInspectionResult': SnapshotInspectionResult,
    'SpecializesReadingReason': SpecializesReadingReason,
    'StructuredScope': StructuredScope,
    'UndeleteSnapshotCall': UndeleteSnapshotCall,
    'UndeleteSnapshotResult': UndeleteSnapshotResult,
    'WholeArtifactScope': WholeArtifactScope,
})
_RUNTIME = ContractRuntime(_SCHEMA, MODEL_TYPES)

def decode_contract(definition: str, value: object) -> object:
    return _RUNTIME.decode(definition, value)

__all__ = (
    'ActiveSnapshotSummary',
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
    'AnalyzeProposalCall',
    'AnyExpression',
    'ApplicabilityExpression',
    'ApplicationHandle',
    'ApplicationId',
    'ApplicationRecoveryRequiredResult',
    'ApplyProposalCall',
    'ApplyProposalResult',
    'AuthorizationId',
    'AuthorizationRecord',
    'AuthorizationReference',
    'CanonicalId',
    'CanonicalModuleDeclaration',
    'ChangeDescriptor',
    'ChangedPolicyUnit',
    'ChildId',
    'CompleteResult',
    'CompletionProof',
    'ConsumerDispositionSubmission',
    'ConsumerReviewContract',
    'ConsumerReviewObligationReadingReason',
    'ContainsExpression',
    'CoverageAttestation',
    'CoverageAttestationClaim',
    'CoverageAttestationSubmission',
    'CoverageCertificate',
    'CoverageRequirement',
    'CreateProposalCall',
    'CreateProposalResult',
    'CreateSnapshotCall',
    'CreateSnapshotResult',
    'DecisionDependency',
    'DecisionFingerprint',
    'DeleteSnapshotCall',
    'DeleteSnapshotResult',
    'Digest',
    'DispositionRecord',
    'DomainContractReference',
    'EdgeId',
    'EqualsExpression',
    'EvidenceReference',
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
    'NextOperation',
    'NonEmptyString',
    'NotExpression',
    'Obligation',
    'ObligationId',
    'PendingResult',
    'PolicyImpactSelectionReason',
    'PolicyInspectionResult',
    'PolicyRelationshipInspection',
    'PolicySummary',
    'PolicyUnitDeclaration',
    'PolicyUnitMapping',
    'PrepareCall',
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
    'ProvenanceRecord',
    'ProvideFactSubmission',
    'ProviderReference',
    'QuarantinedSnapshotSummary',
    'QueryCall',
    'QueryNextOperation',
    'QueryProposalCall',
    'QueryProposalNextOperation',
    'QueryProposalResult',
    'QueryRequest',
    'QueryResult',
    'Question',
    'ReadRequest',
    'ReadResult',
    'ReadinessHandle',
    'ReadinessId',
    'ReadingPlanEntry',
    'ReadingPlanReason',
    'RecoverApplicationCall',
    'RecoverApplicationResult',
    'RejectedResult',
    'RelatedRequest',
    'RelatedResult',
    'RelationshipInspectionResult',
    'RelationshipSummary',
    'ReplacementMutation',
    'RepositoryPath',
    'RequiresReadingReason',
    'ResolveCall',
    'ResolveNextOperation',
    'ReviewDecision',
    'ReviewProposalCall',
    'ReviewProposalResult',
    'ReviewScope',
    'ReviseProposalCall',
    'ReviseProposalResult',
    'RouteRequest',
    'RouteResult',
    'RoutingBaseReadingReason',
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
    'StructuredScope',
    'Submission',
    'Timestamp',
    'UndeleteSnapshotCall',
    'UndeleteSnapshotResult',
    'WholeArtifactScope',
    'DEFINITION_METADATA',
    'decode_contract',
)
