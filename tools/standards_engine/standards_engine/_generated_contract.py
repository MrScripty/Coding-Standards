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

_SCHEMA = json.loads('{"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"https://coding-standards.local/contracts/standards-engine/a1/v11","title":"Standards Engine A1b contract","description":"Canonical typed contract for authority-view-bound navigation and read-only standards-change analysis.","oneOf":[{"$ref":"#/$defs/QueryCall"},{"$ref":"#/$defs/PrepareCall"},{"$ref":"#/$defs/ResolveCall"},{"$ref":"#/$defs/InspectCall"},{"$ref":"#/$defs/NavigationResult"},{"$ref":"#/$defs/PendingResult"},{"$ref":"#/$defs/CompleteResult"},{"$ref":"#/$defs/RejectedResult"},{"$ref":"#/$defs/InspectionResult"}],"$defs":{"NonEmptyString":{"type":"string","minLength":1},"CanonicalId":{"type":"string","pattern":"^[A-Za-z0-9][A-Za-z0-9._:/-]*$"},"EdgeId":{"type":"string","minLength":1},"Digest":{"type":"string","pattern":"^sha256:[0-9a-f]{64}$"},"ContentSnapshotId":{"type":"string","pattern":"^content-snapshot:sha256:[0-9a-f]{64}$"},"AuthorityObjectId":{"type":"string","pattern":"^[a-z][a-z0-9.-]*:sha256:[0-9a-f]{64}$"},"StandardsAuthorityViewId":{"type":"string","pattern":"^standards-authority-view:sha256:[0-9a-f]{64}$"},"ExecutionClosureId":{"type":"string","pattern":"^execution-closure:sha256:[0-9a-f]{64}$"},"NavigationId":{"type":"string","pattern":"^navigation-result:sha256:[0-9a-f]{64}$"},"AnalysisId":{"type":"string","pattern":"^analysis-root:sha256:[0-9a-f]{64}$"},"ObligationId":{"type":"string","pattern":"^obligation:sha256:[0-9a-f]{64}$"},"ImpactTraceId":{"type":"string","pattern":"^impact-trace:sha256:[0-9a-f]{64}$"},"CertificateId":{"type":"string","pattern":"^coverage-certificate:sha256:[0-9a-f]{64}$"},"CoverageAuthorityViewId":{"type":"string","pattern":"^coverage-view:sha256:[0-9a-f]{64}$"},"CoverageRequirementId":{"type":"string","pattern":"^coverage-requirement:sha256:[0-9a-f]{64}$"},"CoverageAttestationId":{"type":"string","pattern":"^coverage-attestation:sha256:[0-9a-f]{64}$"},"AnalysisContextId":{"type":"string","pattern":"^analysis-context:sha256:[0-9a-f]{64}$"},"FactRequirementId":{"type":"string","pattern":"^fact-requirement:sha256:[0-9a-f]{64}$"},"FactObservationId":{"type":"string","pattern":"^fact-observation:sha256:[0-9a-f]{64}$"},"ContentSnapshotHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"content-snapshot-handle"},"id":{"$ref":"#/$defs/ContentSnapshotId"},"schema_version":{"const":4}},"additionalProperties":false},"StandardsAuthorityViewHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"standards-authority-view-handle"},"id":{"$ref":"#/$defs/StandardsAuthorityViewId"},"schema_version":{"const":4}},"additionalProperties":false},"ExecutionClosureHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"execution-closure-handle"},"id":{"$ref":"#/$defs/ExecutionClosureId"},"schema_version":{"const":4}},"additionalProperties":false},"NavigationHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"navigation-handle"},"id":{"$ref":"#/$defs/NavigationId"},"schema_version":{"const":4}},"additionalProperties":false},"AnalysisHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"analysis-handle"},"id":{"$ref":"#/$defs/AnalysisId"},"schema_version":{"const":4}},"additionalProperties":false},"PolicyHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"policy-handle"},"id":{"$ref":"#/$defs/PolicyId"},"schema_version":{"const":4}},"additionalProperties":false},"RelationshipHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"relationship-handle"},"id":{"$ref":"#/$defs/RelationshipInspectionId"},"schema_version":{"const":4}},"additionalProperties":false},"CertificateHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"certificate-handle"},"id":{"$ref":"#/$defs/CertificateId"},"schema_version":{"const":4}},"additionalProperties":false},"CoverageAuthorityViewHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"coverage-authority-view-handle"},"id":{"$ref":"#/$defs/CoverageAuthorityViewId"},"schema_version":{"const":4}},"additionalProperties":false},"CoverageRequirementHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"coverage-requirement-handle"},"id":{"$ref":"#/$defs/CoverageRequirementId"},"schema_version":{"const":4}},"additionalProperties":false},"CoverageAttestationHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"coverage-attestation-handle"},"id":{"$ref":"#/$defs/CoverageAttestationId"},"schema_version":{"const":4}},"additionalProperties":false},"AnalysisContextHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"analysis-context-handle"},"id":{"$ref":"#/$defs/AnalysisContextId"},"schema_version":{"const":4}},"additionalProperties":false},"FactRequirementHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"fact-requirement-handle"},"id":{"$ref":"#/$defs/FactRequirementId"},"schema_version":{"const":4}},"additionalProperties":false},"FactObservationHandle":{"type":"object","required":["kind","id","schema_version"],"properties":{"kind":{"const":"fact-observation-handle"},"id":{"$ref":"#/$defs/FactObservationId"},"schema_version":{"const":4}},"additionalProperties":false},"InspectableHandle":{"oneOf":[{"$ref":"#/$defs/ContentSnapshotHandle"},{"$ref":"#/$defs/StandardsAuthorityViewHandle"},{"$ref":"#/$defs/ExecutionClosureHandle"},{"$ref":"#/$defs/NavigationHandle"},{"$ref":"#/$defs/AnalysisHandle"},{"$ref":"#/$defs/PolicyHandle"},{"$ref":"#/$defs/RelationshipHandle"},{"$ref":"#/$defs/CertificateHandle"},{"$ref":"#/$defs/CoverageAuthorityViewHandle"},{"$ref":"#/$defs/CoverageRequirementHandle"},{"$ref":"#/$defs/CoverageAttestationHandle"},{"$ref":"#/$defs/AnalysisContextHandle"},{"$ref":"#/$defs/FactRequirementHandle"},{"$ref":"#/$defs/FactObservationHandle"}]},"ScalarValue":{"oneOf":[{"type":"boolean"},{"type":"integer"},{"type":"string"},{"type":"null"}]},"FactValue":{"oneOf":[{"type":"object","required":["type","state","value"],"properties":{"type":{"const":"boolean"},"state":{"const":"known"},"value":{"type":"boolean"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"state":{"const":"known"},"value":{"type":"null"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["enum","string","canonical-id"]},"state":{"const":"known"},"value":{"type":"string"}},"additionalProperties":false},{"type":"object","required":["type","state","value"],"properties":{"type":{"enum":["string-set","enum-set"]},"state":{"const":"known"},"value":{"type":"array","items":{"type":"string"},"uniqueItems":true}},"additionalProperties":false},{"type":"object","required":["type","state"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"state":{"enum":["known-absent","unknown"]}},"additionalProperties":false}]},"FactSet":{"type":"object","additionalProperties":{"$ref":"#/$defs/FactValue"}},"AllExpression":{"type":"object","required":["operator","expressions"],"properties":{"operator":{"const":"all"},"expressions":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ApplicabilityExpression"}}},"additionalProperties":false},"AnyExpression":{"type":"object","required":["operator","expressions"],"properties":{"operator":{"const":"any"},"expressions":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ApplicabilityExpression"}}},"additionalProperties":false},"NotExpression":{"type":"object","required":["operator","expression"],"properties":{"operator":{"const":"not"},"expression":{"$ref":"#/$defs/ApplicabilityExpression"}},"additionalProperties":false},"EqualsExpression":{"type":"object","required":["operator","fact","value"],"properties":{"operator":{"const":"equals"},"fact":{"$ref":"#/$defs/CanonicalId"},"value":{"$ref":"#/$defs/ScalarValue"}},"additionalProperties":false},"InExpression":{"type":"object","required":["operator","fact","values"],"properties":{"operator":{"const":"in"},"fact":{"$ref":"#/$defs/CanonicalId"},"values":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ScalarValue"}}},"additionalProperties":false},"ContainsExpression":{"type":"object","required":["operator","fact","value"],"properties":{"operator":{"const":"contains"},"fact":{"$ref":"#/$defs/CanonicalId"},"value":{"$ref":"#/$defs/ScalarValue"}},"additionalProperties":false},"ExistsExpression":{"type":"object","required":["operator","fact"],"properties":{"operator":{"const":"exists"},"fact":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"AlwaysExpression":{"type":"object","required":["operator"],"properties":{"operator":{"const":"always"}},"additionalProperties":false},"ApplicabilityExpression":{"oneOf":[{"$ref":"#/$defs/AlwaysExpression"},{"$ref":"#/$defs/AllExpression"},{"$ref":"#/$defs/AnyExpression"},{"$ref":"#/$defs/NotExpression"},{"$ref":"#/$defs/EqualsExpression"},{"$ref":"#/$defs/InExpression"},{"$ref":"#/$defs/ContainsExpression"},{"$ref":"#/$defs/ExistsExpression"}]},"StructuredScope":{"type":"object","required":["kind","heading_path"],"properties":{"kind":{"const":"structured"},"heading_path":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/NonEmptyString"}}},"additionalProperties":false},"WholeArtifactScope":{"type":"object","required":["kind"],"properties":{"kind":{"const":"whole-artifact"}},"additionalProperties":false},"ReviewScope":{"oneOf":[{"$ref":"#/$defs/StructuredScope"},{"$ref":"#/$defs/WholeArtifactScope"}]},"SelectionReason":{"oneOf":[{"$ref":"#/$defs/GeneralSelectionReason"},{"$ref":"#/$defs/PolicyImpactSelectionReason"}]},"GeneralSelectionReason":{"type":"object","required":["kind"],"properties":{"kind":{"enum":["routing-fact","requires","specializes","changed-policy","question","audit-coverage","unmapped-normative-change","structured-scope-analysis-unsupported"]},"source":{"$ref":"#/$defs/CanonicalId"},"fact":{"$ref":"#/$defs/CanonicalId"},"edge":{"$ref":"#/$defs/EdgeId"},"question":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"PolicyImpactSelectionReason":{"type":"object","required":["kind","source","edge","relation","evidence_owner","traces"],"properties":{"kind":{"const":"policy-impact-edge"},"source":{"$ref":"#/$defs/CanonicalId"},"edge":{"$ref":"#/$defs/EdgeId"},"relation":{"$ref":"#/$defs/CanonicalId"},"evidence_owner":{"$ref":"#/$defs/CanonicalId"},"traces":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ImpactTraceReference"}}},"additionalProperties":false},"ImpactTraceReference":{"type":"object","required":["id","graph","applicability"],"properties":{"id":{"$ref":"#/$defs/ImpactTraceId"},"graph":{"enum":["accepted","proposed"]},"applicability":{"enum":["true","false","unknown"]}},"additionalProperties":false},"ConsumerReviewObligationReadingReason":{"type":"object","required":["kind","obligation"],"properties":{"kind":{"const":"consumer-review-obligation"},"obligation":{"$ref":"#/$defs/ObligationId"}},"additionalProperties":false},"RoutingBaseReadingReason":{"type":"object","required":["kind","projection"],"properties":{"kind":{"const":"routing-base"},"projection":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"RoutingRuleReadingReason":{"type":"object","required":["kind","rule","facts"],"properties":{"kind":{"const":"routing-rule"},"rule":{"$ref":"#/$defs/CanonicalId"},"facts":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"RequiresReadingReason":{"type":"object","required":["kind","edge","source"],"properties":{"kind":{"const":"requires"},"edge":{"$ref":"#/$defs/EdgeId"},"source":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"SpecializesReadingReason":{"type":"object","required":["kind","edge","source"],"properties":{"kind":{"const":"specializes"},"edge":{"$ref":"#/$defs/EdgeId"},"source":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"ReadingPlanReason":{"oneOf":[{"$ref":"#/$defs/ConsumerReviewObligationReadingReason"},{"$ref":"#/$defs/RoutingBaseReadingReason"},{"$ref":"#/$defs/RoutingRuleReadingReason"},{"$ref":"#/$defs/RequiresReadingReason"},{"$ref":"#/$defs/SpecializesReadingReason"}]},"ReadingPlanEntry":{"type":"object","required":["target","scope","authority","reasons","state"],"properties":{"target":{"$ref":"#/$defs/CanonicalId"},"scope":{"$ref":"#/$defs/ReviewScope"},"authority":{"enum":["normative","projection","contextual","evidence"]},"reasons":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ReadingPlanReason"}},"state":{"enum":["selected","conditional","unresolved"]}},"additionalProperties":false},"QueryNextOperation":{"type":"object","required":["operation","request_kind","view"],"properties":{"operation":{"const":"query"},"request_kind":{"enum":["route","read","related"]},"target":{"$ref":"#/$defs/CanonicalId"},"view":{"$ref":"#/$defs/StandardsAuthorityViewHandle"}},"additionalProperties":false},"ResolveNextOperation":{"type":"object","required":["operation","request_kind","analysis"],"properties":{"operation":{"const":"resolve"},"request_kind":{"enum":["provide-fact","consumer-disposition","impact-disposition","coverage-attestation"]},"target":{"$ref":"#/$defs/CanonicalId"},"obligation_id":{"$ref":"#/$defs/ObligationId"},"requirement_id":{"$ref":"#/$defs/FactRequirementId"},"analysis":{"$ref":"#/$defs/AnalysisHandle"}},"additionalProperties":false},"InspectNextOperation":{"type":"object","required":["operation","request_kind","target","view"],"properties":{"operation":{"const":"inspect"},"request_kind":{"const":"inspect"},"target":{"$ref":"#/$defs/CanonicalId"},"view":{"$ref":"#/$defs/StandardsAuthorityViewHandle"}},"additionalProperties":false},"NextOperation":{"oneOf":[{"$ref":"#/$defs/QueryNextOperation"},{"$ref":"#/$defs/ResolveNextOperation"},{"$ref":"#/$defs/InspectNextOperation"}]},"RouteRequest":{"type":"object","required":["kind","facts"],"properties":{"kind":{"const":"route"},"facts":{"$ref":"#/$defs/FactSet"}},"additionalProperties":false},"ReadRequest":{"type":"object","required":["kind","target"],"properties":{"kind":{"const":"read"},"target":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"RelatedRequest":{"type":"object","required":["kind","target","groups","direction","transitive"],"properties":{"kind":{"const":"related"},"target":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"direction":{"enum":["incoming","outgoing","both"]},"transitive":{"type":"boolean","default":false}},"additionalProperties":false},"QueryRequest":{"oneOf":[{"$ref":"#/$defs/RouteRequest"},{"$ref":"#/$defs/ReadRequest"},{"$ref":"#/$defs/RelatedRequest"}]},"QueryCall":{"type":"object","required":["view","request"],"properties":{"view":{"$ref":"#/$defs/StandardsAuthorityViewHandle"},"request":{"$ref":"#/$defs/QueryRequest"}},"additionalProperties":false},"PolicyUnitDeclaration":{"type":"object","required":["kind","id","module","heading_path","semantic_revision","lifecycle"],"properties":{"kind":{"const":"policy-unit"},"id":{"$ref":"#/$defs/CanonicalId"},"module":{"$ref":"#/$defs/CanonicalId"},"heading_path":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/NonEmptyString"}},"semantic_revision":{"type":"integer","minimum":1},"lifecycle":{"const":"active"},"aliases":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"predecessors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"successors":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"CanonicalModuleDeclaration":{"type":"object","required":["kind","id","role","level","applies_when","does_not_apply_when","requires","specializes","verification"],"properties":{"kind":{"const":"canonical-module"},"id":{"$ref":"#/$defs/CanonicalId"},"role":{"enum":["core","router","workflow","profile","topic","reference"]},"level":{"enum":["MUST","SHOULD","PROFILE","REFERENCE"]},"applies_when":{"$ref":"#/$defs/NonEmptyString"},"does_not_apply_when":{"$ref":"#/$defs/NonEmptyString"},"requires":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"specializes":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"verification":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"PolicyRelationshipInspection":{"type":"object","required":["relationship_kind","applicability","source_scope","consumer_scope","propagation","evidence_owner","rationale"],"properties":{"relationship_kind":{"enum":["normative-consumer","router-projection","prompt-projection","template-projection","reference-projection","fixture-projection","enforcement-suite-projection","documentation-projection","implementation-projection"]},"applicability":{"$ref":"#/$defs/ApplicabilityExpression"},"source_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"consumer_scope":{"oneOf":[{"$ref":"#/$defs/ReviewScope"},{"type":"null"}]},"propagation":{"const":"source-to-consumer"},"evidence_owner":{"$ref":"#/$defs/CanonicalId"},"rationale":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"SemanticProposal":{"type":"object","required":["policy","accepted_semantic_revision","proposed_semantic_revision","intent","structural_digest"],"properties":{"policy":{"$ref":"#/$defs/CanonicalId"},"accepted_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"proposed_semantic_revision":{"type":"integer","minimum":1},"intent":{"$ref":"#/$defs/NonEmptyString"},"structural_digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"ChangeDescriptor":{"type":"object","required":["kind","accepted_ids","proposed_ids","scope"],"properties":{"kind":{"enum":["modification","addition","removal","move","split","merge"]},"accepted_ids":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"proposed_ids":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"scope":{"$ref":"#/$defs/ReviewScope"},"accepted_module":{"$ref":"#/$defs/CanonicalId"},"proposed_module":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"ChangedPolicyUnit":{"type":"object","required":["policy","change_kind","classification","accepted_representation_digest","proposed_representation_digest","accepted_structural_digest","proposed_structural_digest","accepted_semantic_revision","proposed_semantic_revision","semantic_state","scope"],"properties":{"policy":{"$ref":"#/$defs/CanonicalId"},"change_kind":{"enum":["modification","addition","removal","move","split-predecessor","split-successor","merge-predecessor","merge-successor"]},"classification":{"enum":["unchanged","representation-only-candidate","possibly-semantically-changed","semantically-changed","unresolved"]},"accepted_representation_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"proposed_representation_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"accepted_structural_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"proposed_structural_digest":{"oneOf":[{"$ref":"#/$defs/Digest"},{"type":"null"}]},"accepted_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"proposed_semantic_revision":{"oneOf":[{"type":"integer","minimum":1},{"type":"null"}]},"semantic_state":{"enum":["accepted-unchanged","proposed","removed","unresolved"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"AnalysisRequest":{"type":"object","required":["kind","base_view","proposed_view","changes","semantic_proposals","contract_version"],"properties":{"kind":{"const":"analysis-request"},"base_view":{"$ref":"#/$defs/StandardsAuthorityViewHandle"},"proposed_view":{"$ref":"#/$defs/StandardsAuthorityViewHandle"},"changes":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/ChangeDescriptor"}},"semantic_proposals":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/SemanticProposal"}},"prior_analysis":{"$ref":"#/$defs/AnalysisHandle"},"contract_version":{"const":3}},"additionalProperties":false},"PrepareCall":{"type":"object","required":["request"],"properties":{"request":{"$ref":"#/$defs/AnalysisRequest"}},"additionalProperties":false},"PolicySummary":{"type":"object","required":["handle","authority","scope"],"properties":{"handle":{"$ref":"#/$defs/PolicyHandle"},"authority":{"enum":["normative","projection","contextual","evidence"]},"scope":{"$ref":"#/$defs/ReviewScope"}},"additionalProperties":false},"RelationshipSummary":{"type":"object","required":["handle","source","target","relation","groups","direction","traversal_eligible","applicability"],"properties":{"handle":{"$ref":"#/$defs/RelationshipHandle"},"source":{"$ref":"#/$defs/CanonicalId"},"target":{"$ref":"#/$defs/CanonicalId"},"relation":{"$ref":"#/$defs/CanonicalId"},"groups":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"direction":{"enum":["incoming","outgoing"]},"traversal_eligible":{"type":"boolean"},"applicability":{"enum":["true","false","unknown","not-declared"]}},"additionalProperties":false},"RouteResult":{"type":"object","required":["kind","handle","authority","reading_plan","unresolved_questions","next_operations"],"properties":{"kind":{"const":"route-result"},"handle":{"$ref":"#/$defs/NavigationHandle"},"authority":{"$ref":"#/$defs/ExecutionClosureHandle"},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"unresolved_questions":{"type":"array","items":{"$ref":"#/$defs/Question"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"ReadResult":{"type":"object","required":["kind","handle","authority","policy","content","requires","specializes","related","next_operations"],"properties":{"kind":{"const":"read-result"},"handle":{"$ref":"#/$defs/NavigationHandle"},"authority":{"$ref":"#/$defs/ExecutionClosureHandle"},"policy":{"$ref":"#/$defs/PolicySummary"},"content":{"type":"string"},"requires":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"specializes":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"related":{"type":"array","items":{"$ref":"#/$defs/RelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"RelatedResult":{"type":"object","required":["kind","handle","authority","target","policy_unit_mapping","relationships","next_operations"],"properties":{"kind":{"const":"related-result"},"handle":{"$ref":"#/$defs/NavigationHandle"},"authority":{"$ref":"#/$defs/ExecutionClosureHandle"},"target":{"$ref":"#/$defs/CanonicalId"},"policy_unit_mapping":{"type":"object","required":["state","policy_units"],"properties":{"state":{"enum":["exact-policy-unit","policy-units-present","incomplete"]},"reason":{"const":"no-policy-units"},"policy_units":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}}},"additionalProperties":false},"relationships":{"type":"array","items":{"$ref":"#/$defs/RelationshipSummary"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"summary":{"type":"string"}},"additionalProperties":false},"NavigationResult":{"oneOf":[{"$ref":"#/$defs/RouteResult"},{"$ref":"#/$defs/ReadResult"},{"$ref":"#/$defs/RelatedResult"}]},"Question":{"type":"object","required":["id","kind","prompt","state","permitted_answers"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"kind":{"enum":["applicability-fact","normative-classification","identity-resolution","scope-resolution"]},"prompt":{"$ref":"#/$defs/NonEmptyString"},"state":{"enum":["required","answered","blocked"]},"permitted_answers":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/NonEmptyString"}}},"additionalProperties":false},"Obligation":{"type":"object","required":["id","kind","target","scope","reasons","state","permitted_submissions","fingerprint"],"properties":{"id":{"$ref":"#/$defs/ObligationId"},"kind":{"enum":["consumer-review","impact-review","lifecycle-impact-review","audit-coverage","unmapped-normative-change"]},"target":{"$ref":"#/$defs/CanonicalId"},"scope":{"$ref":"#/$defs/ReviewScope"},"reasons":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/SelectionReason"}},"state":{"enum":["required","resolved","blocked"]},"applicability":{"enum":["true","false","unknown","not-declared"]},"permitted_submissions":{"type":"array","minItems":1,"uniqueItems":true,"items":{"enum":["consumer-disposition","impact-disposition","coverage-attestation"]}},"review_contract":{"$ref":"#/$defs/ConsumerReviewContract"},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"ConsumerReviewContract":{"type":"object","required":["kind","id","version","permitted_dispositions","evidence_contract","authorization_capability","semantics"],"properties":{"kind":{"const":"consumer-review-contract"},"id":{"$ref":"#/$defs/CanonicalId"},"version":{"type":"integer","minimum":1},"permitted_dispositions":{"type":"array","minItems":1,"uniqueItems":true,"items":{"enum":["updated","reviewed-no-change","not-applicable","blocked"]}},"evidence_contract":{"$ref":"#/$defs/CanonicalId"},"authorization_capability":{"$ref":"#/$defs/CanonicalId"},"semantics":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"DecisionDependency":{"type":"object","required":["class","identity","digest"],"properties":{"class":{"enum":["policy-unit","semantic-revision","structure","representation","module-locator","applicability-fact","relationship","audit","exception","evidence","provider-contract","applicability-contract","analysis-contract"]},"identity":{"$ref":"#/$defs/NonEmptyString"},"digest":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"DecisionFingerprint":{"type":"object","required":["decision_kind","decision_contract","schema_version","dependencies"],"properties":{"decision_kind":{"$ref":"#/$defs/CanonicalId"},"decision_contract":{"$ref":"#/$defs/CanonicalId"},"schema_version":{"const":1},"dependencies":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/DecisionDependency"}}},"additionalProperties":false},"AuthorityObjectReference":{"type":"object","required":["object_kind","id"],"properties":{"object_kind":{"$ref":"#/$defs/CanonicalId"},"id":{"$ref":"#/$defs/AuthorityObjectId"}},"additionalProperties":false},"SemanticAuthoritySelection":{"type":"object","required":["role","authority"],"properties":{"role":{"$ref":"#/$defs/CanonicalId"},"authority":{"$ref":"#/$defs/AuthorityObjectReference"}},"additionalProperties":false},"OperationAuthoritySelection":{"type":"object","required":["operation","authority"],"properties":{"operation":{"enum":["route","read","related","analysis"]},"authority":{"$ref":"#/$defs/AuthorityObjectReference"}},"additionalProperties":false},"StandardsAuthorityView":{"type":"object","required":["kind","handle","content","operation_contracts","authorities"],"properties":{"kind":{"const":"standards-authority-view"},"handle":{"$ref":"#/$defs/StandardsAuthorityViewHandle"},"content":{"$ref":"#/$defs/ContentSnapshotHandle"},"operation_contracts":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/OperationAuthoritySelection"},"minItems":1},"authorities":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/SemanticAuthoritySelection"},"minItems":1}},"additionalProperties":false},"ExecutionClosure":{"type":"object","required":["kind","handle","closure_contract","operation","roots"],"properties":{"kind":{"const":"execution-closure"},"handle":{"$ref":"#/$defs/ExecutionClosureHandle"},"closure_contract":{"const":"execution-closure.v2"},"operation":{"enum":["route","read","related","analysis"]},"roots":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/ExecutionAuthorityRoot"},"minItems":1}},"additionalProperties":false},"ExecutionAuthorityRoot":{"type":"object","required":["side","role","authority"],"properties":{"side":{"enum":["current","accepted","proposed","transition"]},"role":{"$ref":"#/$defs/CanonicalId"},"authority":{"$ref":"#/$defs/AuthorityObjectReference"}},"additionalProperties":false},"AnalysisContext":{"type":"object","required":["kind","handle","subjects","changes","semantic_proposals"],"properties":{"kind":{"const":"analysis-context"},"handle":{"$ref":"#/$defs/AnalysisContextHandle"},"subjects":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ChangedPolicyUnit"}},"semantic_proposals":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/SemanticProposal"}},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"},"minItems":1,"uniqueItems":true}},"additionalProperties":false},"FactValueContract":{"type":"object","required":["type","states","nullable"],"properties":{"type":{"enum":["boolean","enum","string","string-set","enum-set","canonical-id"]},"states":{"const":["known","known-absent"]},"nullable":{"type":"boolean"},"values":{"type":"array","minItems":1,"uniqueItems":true,"items":{"type":"string"}}},"additionalProperties":false},"FactRequirement":{"type":"object","required":["kind","handle","fact","fact_semantic_revision","fact_contract_digest","context","value_contract","answer_contract","evidence_contract","authority_dependencies","authorization_capability"],"properties":{"kind":{"const":"fact-requirement"},"handle":{"$ref":"#/$defs/FactRequirementHandle"},"fact":{"$ref":"#/$defs/CanonicalId"},"fact_semantic_revision":{"type":"integer","minimum":1},"fact_contract_digest":{"$ref":"#/$defs/Digest"},"context":{"$ref":"#/$defs/AnalysisContextHandle"},"value_contract":{"$ref":"#/$defs/FactValueContract"},"answer_contract":{"$ref":"#/$defs/CanonicalId"},"evidence_contract":{"$ref":"#/$defs/CanonicalId"},"authorization_capability":{"$ref":"#/$defs/CanonicalId"},"authority_dependencies":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/AuthorityObjectReference"},"minItems":1}},"additionalProperties":false},"PendingResult":{"type":"object","required":["kind","handle","status","context","changes","changed_units","obligations","fact_requirements","reading_plan","next_operations","authority"],"properties":{"kind":{"const":"pending-result"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"status":{"const":"needs-action"},"context":{"$ref":"#/$defs/AnalysisContext"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"}},"changed_units":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"}},"obligations":{"type":"array","items":{"$ref":"#/$defs/Obligation"}},"fact_requirements":{"type":"array","items":{"$ref":"#/$defs/FactRequirementWork"}},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}},"authority":{"$ref":"#/$defs/ExecutionClosureHandle"},"summary":{"type":"string"}},"additionalProperties":false},"EvidenceReference":{"type":"object","required":["id","digest","provider_contract","provider_contract_version"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"digest":{"$ref":"#/$defs/Digest"},"provider_contract":{"$ref":"#/$defs/CanonicalId"},"provider_contract_version":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"AuthorizationGrantReference":{"type":"object","required":["object_kind","id"],"properties":{"object_kind":{"const":"authorization-grant"},"id":{"$ref":"#/$defs/AuthorityObjectId"}},"additionalProperties":false},"ProviderAuthorityReference":{"type":"object","required":["object_kind","id"],"properties":{"object_kind":{"const":"provider-authority"},"id":{"$ref":"#/$defs/AuthorityObjectId"}},"additionalProperties":false},"FactObservation":{"type":"object","required":["kind","handle","requirement","value","evidence","authorization"],"properties":{"kind":{"const":"fact-observation"},"handle":{"$ref":"#/$defs/FactObservationHandle"},"requirement":{"$ref":"#/$defs/FactRequirementHandle"},"value":{"$ref":"#/$defs/FactValue"},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}},"authorization":{"$ref":"#/$defs/AuthorizationGrantReference"},"provider_authority":{"$ref":"#/$defs/ProviderAuthorityReference"}},"additionalProperties":false},"ProvideFactSubmission":{"type":"object","required":["kind","requirement","value","evidence"],"properties":{"kind":{"const":"provide-fact"},"requirement":{"$ref":"#/$defs/FactRequirementHandle"},"value":{"$ref":"#/$defs/FactValue"},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}}},"additionalProperties":false},"ConsumerDispositionSubmission":{"type":"object","required":["kind","obligation_id","result","rationale","evidence","fingerprint"],"properties":{"kind":{"const":"consumer-disposition"},"obligation_id":{"$ref":"#/$defs/ObligationId"},"result":{"enum":["updated","reviewed-no-change","not-applicable","blocked"]},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/EvidenceReference"}},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"ImpactDispositionSubmission":{"type":"object","required":["kind","obligation_id","result","rationale","evidence","fingerprint"],"properties":{"kind":{"const":"impact-disposition"},"obligation_id":{"$ref":"#/$defs/ObligationId"},"result":{"enum":["confirmed","resolved-no-impact","requires-change","blocked"]},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/EvidenceReference"}},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"CoverageAttestationClaim":{"type":"object","required":["requirement","conclusion","evidence","explicit_exclusions","rationale","auditor_provenance"],"properties":{"requirement":{"$ref":"#/$defs/CoverageRequirementHandle"},"conclusion":{"const":"complete"},"evidence":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}},"explicit_exclusions":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/EvidenceReference"}},"rationale":{"$ref":"#/$defs/NonEmptyString"},"auditor_provenance":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"CoverageAttestationSubmission":{"type":"object","required":["kind","obligation_id","claim"],"properties":{"kind":{"const":"coverage-attestation"},"obligation_id":{"$ref":"#/$defs/ObligationId"},"claim":{"$ref":"#/$defs/CoverageAttestationClaim"}},"additionalProperties":false},"Submission":{"oneOf":[{"$ref":"#/$defs/ProvideFactSubmission"},{"$ref":"#/$defs/ConsumerDispositionSubmission"},{"$ref":"#/$defs/ImpactDispositionSubmission"},{"$ref":"#/$defs/CoverageAttestationSubmission"}]},"ResolveCall":{"type":"object","required":["analysis","submission"],"properties":{"analysis":{"$ref":"#/$defs/AnalysisHandle"},"submission":{"$ref":"#/$defs/Submission"}},"additionalProperties":false},"CoverageHorizonMember":{"type":"object","required":["id","roles","fingerprint"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"roles":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"fingerprint":{"$ref":"#/$defs/Digest"}},"additionalProperties":false},"CoverageAuthorityView":{"type":"object","required":["kind","handle","subject","owner","semantic_revision","representation_digest","structural_digest","relationship_kinds","relationship_fingerprints","applicability_program_digests","fact_schema_digest","horizon","authority_dependencies"],"properties":{"kind":{"const":"coverage-authority-view"},"handle":{"$ref":"#/$defs/CoverageAuthorityViewHandle"},"subject":{"$ref":"#/$defs/CanonicalId"},"owner":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"representation_digest":{"$ref":"#/$defs/Digest"},"structural_digest":{"$ref":"#/$defs/Digest"},"relationship_kinds":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"relationship_fingerprints":{"type":"array","uniqueItems":true,"items":{"type":"object","required":["edge","fingerprint"],"properties":{"edge":{"$ref":"#/$defs/EdgeId"},"fingerprint":{"$ref":"#/$defs/Digest"}},"additionalProperties":false}},"applicability_program_digests":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/Digest"}},"fact_schema_digest":{"$ref":"#/$defs/Digest"},"horizon":{"type":"object","required":["id","provider","version","digest","members"],"properties":{"id":{"$ref":"#/$defs/CanonicalId"},"provider":{"$ref":"#/$defs/CanonicalId"},"version":{"type":"integer","minimum":1},"digest":{"$ref":"#/$defs/Digest"},"members":{"type":"array","items":{"$ref":"#/$defs/CoverageHorizonMember"}}},"additionalProperties":false},"authority_dependencies":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/AuthorityObjectReference"},"minItems":1}},"additionalProperties":false},"CoverageAuditRequirement":{"type":"object","required":["kind","handle","coverage_view","subject","owner","semantic_revision","relationship_kinds","horizon","required_evidence_contract"],"properties":{"kind":{"const":"coverage-audit-requirement"},"handle":{"$ref":"#/$defs/CoverageRequirementHandle"},"coverage_view":{"$ref":"#/$defs/CoverageAuthorityViewHandle"},"subject":{"$ref":"#/$defs/CanonicalId"},"owner":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"relationship_kinds":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"horizon":{"$ref":"#/$defs/CanonicalId"},"derived_from_view":{"$ref":"#/$defs/StandardsAuthorityViewHandle"},"required_evidence_contract":{"$ref":"#/$defs/CanonicalId"}},"additionalProperties":false},"CoverageAttestation":{"type":"object","required":["kind","handle","requirement","conclusion","evidence","explicit_exclusions","rationale","auditor_provenance","schema_version","authorization"],"properties":{"kind":{"const":"coverage-attestation"},"handle":{"$ref":"#/$defs/CoverageAttestationHandle"},"requirement":{"$ref":"#/$defs/CoverageRequirementHandle"},"conclusion":{"const":"complete"},"evidence":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/EvidenceReference"}},"explicit_exclusions":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"}},"rationale":{"$ref":"#/$defs/NonEmptyString"},"auditor_provenance":{"$ref":"#/$defs/NonEmptyString"},"schema_version":{"const":3},"authorization":{"$ref":"#/$defs/AuthorizationGrantReference"}},"additionalProperties":false},"ConsumerCoverageCertificate":{"type":"object","required":["kind","handle","coverage_view","requirement","attestation","subject","owner","semantic_revision","horizon_digest","relationship_digest","evidence_digests","fact_schema_digest","provenance","authority_dependencies"],"properties":{"kind":{"const":"consumer-coverage-certificate"},"handle":{"$ref":"#/$defs/CertificateHandle"},"coverage_view":{"$ref":"#/$defs/CoverageAuthorityViewHandle"},"requirement":{"$ref":"#/$defs/CoverageRequirementHandle"},"attestation":{"$ref":"#/$defs/CoverageAttestationHandle"},"subject":{"$ref":"#/$defs/CanonicalId"},"owner":{"$ref":"#/$defs/CanonicalId"},"semantic_revision":{"type":"integer","minimum":1},"horizon_digest":{"$ref":"#/$defs/Digest"},"relationship_digest":{"$ref":"#/$defs/Digest"},"evidence_digests":{"type":"array","items":{"$ref":"#/$defs/Digest"}},"provenance":{"$ref":"#/$defs/CertificateProvenance"},"fact_schema_digest":{"$ref":"#/$defs/Digest"},"authority_dependencies":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/AuthorityObjectReference"},"minItems":1}},"additionalProperties":false},"CertificateProvenance":{"type":"object","required":["generator"],"properties":{"generator":{"$ref":"#/$defs/NonEmptyString"}},"additionalProperties":false},"DispositionRecord":{"type":"object","required":["obligation_id","kind","result","rationale","evidence","authorization","fingerprint"],"properties":{"obligation_id":{"$ref":"#/$defs/ObligationId"},"kind":{"enum":["consumer-disposition","impact-disposition"]},"result":{"$ref":"#/$defs/NonEmptyString"},"rationale":{"$ref":"#/$defs/NonEmptyString"},"evidence":{"type":"array","items":{"$ref":"#/$defs/EvidenceReference"}},"authorization":{"$ref":"#/$defs/AuthorizationGrantReference"},"fingerprint":{"$ref":"#/$defs/DecisionFingerprint"}},"additionalProperties":false},"AnalysisState":{"type":"object","required":["kind","handle","context","authority","fact_observations","dispositions","coverage_attestations"],"properties":{"kind":{"const":"analysis-state"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"context":{"$ref":"#/$defs/AnalysisContext"},"fact_observations":{"type":"array","items":{"$ref":"#/$defs/FactObservation"},"uniqueItems":true},"dispositions":{"type":"array","items":{"$ref":"#/$defs/DispositionRecord"},"uniqueItems":true},"coverage_attestations":{"type":"array","items":{"$ref":"#/$defs/CoverageAttestation"},"uniqueItems":true},"authority":{"$ref":"#/$defs/ExecutionClosureHandle"}},"additionalProperties":false},"CompletionProof":{"type":"object","required":["required_coverage_subjects","certificate_subjects","reached_consumer_obligations","disposition_obligations","required_fact_requirements","observed_fact_requirements","non_consumer_obligations_resolved","applicability_resolved","authorization_valid","evidence_valid"],"properties":{"required_coverage_subjects":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"certificate_subjects":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CanonicalId"}},"reached_consumer_obligations":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/ObligationId"}},"disposition_obligations":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/ObligationId"}},"required_fact_requirements":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/FactRequirementId"}},"observed_fact_requirements":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/FactRequirementId"}},"non_consumer_obligations_resolved":{"const":true},"applicability_resolved":{"const":true},"authorization_valid":{"const":true},"evidence_valid":{"const":true}},"additionalProperties":false},"CompleteResult":{"type":"object","required":["kind","handle","status","context","changes","changed_units","coverage_certificates","fact_observations","dispositions","reading_plan","completion","authority"],"properties":{"kind":{"const":"complete-result"},"handle":{"$ref":"#/$defs/AnalysisHandle"},"status":{"const":"complete"},"context":{"$ref":"#/$defs/AnalysisContext"},"changes":{"type":"array","items":{"$ref":"#/$defs/ChangeDescriptor"}},"changed_units":{"type":"array","items":{"$ref":"#/$defs/ChangedPolicyUnit"}},"coverage_certificates":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/CertificateHandle"}},"fact_observations":{"type":"array","uniqueItems":true,"items":{"$ref":"#/$defs/FactObservation"}},"dispositions":{"type":"array","items":{"$ref":"#/$defs/DispositionRecord"}},"reading_plan":{"type":"array","items":{"$ref":"#/$defs/ReadingPlanEntry"}},"completion":{"$ref":"#/$defs/CompletionProof"},"authority":{"$ref":"#/$defs/ExecutionClosureHandle"},"summary":{"type":"string"}},"additionalProperties":false},"RejectedResult":{"type":"object","required":["kind","code","outcome","message","details","next_operations"],"properties":{"kind":{"const":"rejected-result"},"code":{"$ref":"#/$defs/CanonicalId"},"outcome":{"enum":["invalid","unavailable","unsupported","unauthorized"]},"target":{"$ref":"#/$defs/CanonicalId"},"message":{"$ref":"#/$defs/NonEmptyString"},"details":{"type":"object","additionalProperties":{"$ref":"#/$defs/ScalarValue"}},"next_operations":{"type":"array","items":{"$ref":"#/$defs/NextOperation"}}},"additionalProperties":false},"RepositoryPath":{"type":"object","required":["components"],"properties":{"components":{"type":"array","minItems":1,"items":{"type":"string","minLength":1}}},"additionalProperties":false},"ContentSnapshotFileEntry":{"type":"object","required":["path","content_digest","content_base64","byte_length"],"properties":{"path":{"$ref":"#/$defs/RepositoryPath"},"content_digest":{"$ref":"#/$defs/Digest"},"content_base64":{"type":"string"},"byte_length":{"type":"integer","minimum":0}},"additionalProperties":false},"ContentSnapshot":{"type":"object","required":["kind","handle","payload_contract","files"],"properties":{"kind":{"const":"content-snapshot"},"handle":{"$ref":"#/$defs/ContentSnapshotHandle"},"payload_contract":{"const":"content-snapshot.v2"},"files":{"type":"array","minItems":1,"uniqueItems":true,"items":{"$ref":"#/$defs/ContentSnapshotFileEntry"}}},"additionalProperties":false},"ProvenanceRecord":{"type":"object","required":["source_id","source_kind","locator","content_snapshot"],"properties":{"source_id":{"$ref":"#/$defs/CanonicalId"},"source_kind":{"enum":["manifest","generator","provider","canonical-document","sidecar"]},"locator":{"$ref":"#/$defs/NonEmptyString"},"content_snapshot":{"$ref":"#/$defs/ContentSnapshotHandle"}},"additionalProperties":false},"ContentSnapshotInspectionResult":{"type":"object","required":["kind","content_snapshot"],"properties":{"kind":{"const":"content-snapshot-inspection-result"},"content_snapshot":{"$ref":"#/$defs/ContentSnapshot"}},"additionalProperties":false},"PolicyInspectionResult":{"type":"object","required":["kind","policy","declaration","representation_digest","structural_digest","provenance"],"properties":{"kind":{"const":"policy-inspection-result"},"policy":{"$ref":"#/$defs/PolicyHandle"},"declaration":{"oneOf":[{"$ref":"#/$defs/CanonicalModuleDeclaration"},{"$ref":"#/$defs/PolicyUnitDeclaration"}]},"representation_digest":{"$ref":"#/$defs/Digest"},"structural_digest":{"$ref":"#/$defs/Digest"},"provenance":{"$ref":"#/$defs/ProvenanceRecord"}},"additionalProperties":false},"RelationshipInspectionResult":{"type":"object","required":["kind","relationship","policy_semantics","provenance"],"properties":{"kind":{"const":"relationship-inspection-result"},"relationship":{"$ref":"#/$defs/RelationshipSummary"},"policy_semantics":{"oneOf":[{"$ref":"#/$defs/PolicyRelationshipInspection"},{"type":"null"}]},"provenance":{"$ref":"#/$defs/ProvenanceRecord"}},"additionalProperties":false},"NavigationInspectionResult":{"type":"object","required":["kind","navigation"],"properties":{"kind":{"const":"navigation-inspection-result"},"navigation":{"$ref":"#/$defs/NavigationResult"}},"additionalProperties":false},"CertificateInspectionResult":{"type":"object","required":["kind","certificate"],"properties":{"kind":{"const":"certificate-inspection-result"},"certificate":{"$ref":"#/$defs/ConsumerCoverageCertificate"}},"additionalProperties":false},"CoverageAuthorityViewInspectionResult":{"type":"object","required":["kind","coverage_view"],"properties":{"kind":{"const":"coverage-authority-view-inspection-result"},"coverage_view":{"$ref":"#/$defs/CoverageAuthorityView"}},"additionalProperties":false},"CoverageRequirementInspectionResult":{"type":"object","required":["kind","requirement"],"properties":{"kind":{"const":"coverage-requirement-inspection-result"},"requirement":{"$ref":"#/$defs/CoverageAuditRequirement"}},"additionalProperties":false},"CoverageAttestationInspectionResult":{"type":"object","required":["kind","attestation"],"properties":{"kind":{"const":"coverage-attestation-inspection-result"},"attestation":{"$ref":"#/$defs/CoverageAttestation"}},"additionalProperties":false},"AnalysisContextInspectionResult":{"type":"object","required":["kind","context"],"properties":{"kind":{"const":"analysis-context-inspection-result"},"context":{"$ref":"#/$defs/AnalysisContext"}},"additionalProperties":false},"FactRequirementInspectionResult":{"type":"object","required":["kind","requirement"],"properties":{"kind":{"const":"fact-requirement-inspection-result"},"requirement":{"$ref":"#/$defs/FactRequirement"}},"additionalProperties":false},"FactObservationInspectionResult":{"type":"object","required":["kind","observation"],"properties":{"kind":{"const":"fact-observation-inspection-result"},"observation":{"$ref":"#/$defs/FactObservation"}},"additionalProperties":false},"InspectionResult":{"oneOf":[{"$ref":"#/$defs/ContentSnapshotInspectionResult"},{"$ref":"#/$defs/PolicyInspectionResult"},{"$ref":"#/$defs/RelationshipInspectionResult"},{"$ref":"#/$defs/NavigationInspectionResult"},{"$ref":"#/$defs/CertificateInspectionResult"},{"$ref":"#/$defs/CoverageAuthorityViewInspectionResult"},{"$ref":"#/$defs/CoverageRequirementInspectionResult"},{"$ref":"#/$defs/CoverageAttestationInspectionResult"},{"$ref":"#/$defs/AnalysisContextInspectionResult"},{"$ref":"#/$defs/FactRequirementInspectionResult"},{"$ref":"#/$defs/FactObservationInspectionResult"},{"$ref":"#/$defs/AnalysisState"},{"$ref":"#/$defs/StandardsAuthorityView"},{"$ref":"#/$defs/ExecutionClosure"}]},"InspectCall":{"type":"object","required":["handle"],"properties":{"handle":{"$ref":"#/$defs/InspectableHandle"}},"additionalProperties":false},"PolicyId":{"type":"string","pattern":"^policy-inspection:sha256:[0-9a-f]{64}$"},"RelationshipInspectionId":{"type":"string","pattern":"^relationship-inspection:sha256:[0-9a-f]{64}$"},"FactRequirementWork":{"type":"object","required":["requirement","prompt","dependent_programs"],"properties":{"requirement":{"$ref":"#/$defs/FactRequirement"},"prompt":{"$ref":"#/$defs/NonEmptyString"},"dependent_programs":{"type":"array","items":{"$ref":"#/$defs/NonEmptyString"},"minItems":1,"uniqueItems":true}},"additionalProperties":false}}}')
DEFINITION_METADATA = freeze_json({'AllExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expressions': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AlwaysExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisContext': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisContextHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisContextId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisContextInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AnalysisRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'base_view': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_view': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_proposals': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prior_analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnalysisState': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_observations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_attestations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AnyExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expressions': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ApplicabilityExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AuthorityObjectId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'AuthorityObjectReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'object_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'AuthorizationGrantReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'object_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CanonicalId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CanonicalModuleDeclaration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'role': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'level': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applies_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'does_not_apply_when': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'verification': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CertificateHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CertificateId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CertificateInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'certificate': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CertificateProvenance': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'generator': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChangeDescriptor': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_ids': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_ids': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_module': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_module': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ChangedPolicyUnit': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'change_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'classification': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CompleteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changed_units': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_certificates': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_observations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'completion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CompletionProof': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'required_coverage_subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'certificate_subjects': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reached_consumer_obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'disposition_obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'required_fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'observed_fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'non_consumer_obligations_resolved': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability_resolved': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_valid': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_valid': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerCoverageCertificate': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_view': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'attestation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'horizon_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_digests': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_schema_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority_dependencies': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerDispositionSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerReviewContract': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_dispositions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_capability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ConsumerReviewObligationReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ContainsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ContentSnapshot': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'payload_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'files': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ContentSnapshotFileEntry': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'path': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content_base64': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'byte_length': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ContentSnapshotHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ContentSnapshotId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ContentSnapshotInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'conclusion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'explicit_exclusions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'auditor_provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationClaim': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'conclusion': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'explicit_exclusions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'auditor_provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CoverageAttestationInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'attestation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAttestationSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'claim': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAuditRequirement': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_view': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_kinds': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'horizon': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'derived_from_view': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'required_evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAuthorityView': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'subject': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_kinds': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship_fingerprints': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability_program_digests': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_schema_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'horizon': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority_dependencies': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAuthorityViewHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageAuthorityViewId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CoverageAuthorityViewInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'coverage_view': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageHorizonMember': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'roles': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageRequirementHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'CoverageRequirementId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'CoverageRequirementInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DecisionDependency': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'class': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'identity': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'DecisionFingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'decision_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'decision_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dependencies': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Digest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'DispositionRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'obligation_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EdgeId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'EqualsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'EvidenceReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider_contract_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ExecutionAuthorityRoot': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'side': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'role': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ExecutionClosure': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'closure_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'roots': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ExecutionClosureHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ExecutionClosureId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ExistsExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactObservation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provider_authority': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactObservationHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactObservationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactObservationInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'observation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirement': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_contract_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'answer_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorization_capability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority_dependencies': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirementHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirementId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactRequirementInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactRequirementWork': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'dependent_programs': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'FactSet': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactValue': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'FactValueContract': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'type': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'states': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'nullable': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'values': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'GeneralSelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'question': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ImpactDispositionSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'result': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ImpactTraceId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'ImpactTraceReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'graph': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'values': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'view': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'InspectableHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'InspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NavigationHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'NavigationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NavigationInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'navigation': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'NavigationResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NonEmptyString': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'NotExpression': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'expression': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Obligation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reasons': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_submissions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'review_contract': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fingerprint': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ObligationId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'OperationAuthoritySelection': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PendingResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'status': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'context': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'changed_units': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'fact_requirements': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'PolicyImpactSelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traces': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'declaration': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'representation_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyRelationshipInspection': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'relationship_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'consumer_scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'propagation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence_owner': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rationale': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicySummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PolicyUnitDeclaration': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'module': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'heading_path': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'lifecycle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'aliases': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'predecessors': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'successors': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'PrepareCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProvenanceRecord': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'source_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'locator': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content_snapshot': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProvideFactSubmission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'value': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'evidence': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ProviderAuthorityReference': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'object_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'view': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'view': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'QueryRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'Question': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'prompt': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'permitted_answers': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requires': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'specializes': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'related': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadingPlanEntry': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'scope': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reasons': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'state': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReadingPlanReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RejectedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'code': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'outcome': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'message': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'details': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelatedRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'transitive': {'title': None, 'description': None, 'has_default': True, 'default': False}}}, 'RelatedResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_unit_mapping': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationships': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipInspectionId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RelationshipInspectionResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relationship': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'policy_semantics': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'provenance': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RelationshipSummary': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'relation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'groups': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'direction': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'traversal_eligible': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'applicability': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RepositoryPath': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'components': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RequiresReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResolveCall': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'submission': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ResolveNextOperation': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'operation': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'request_kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'target': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'obligation_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'requirement_id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'analysis': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ReviewScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'RouteRequest': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RouteResult': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'reading_plan': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'unresolved_questions': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'next_operations': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'summary': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingBaseReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'projection': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'RoutingRuleReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'rule': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'facts': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'ScalarValue': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SelectionReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'SemanticAuthoritySelection': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'role': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authority': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SemanticProposal': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'policy': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'accepted_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'proposed_semantic_revision': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'intent': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'structural_digest': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'SpecializesReadingReason': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'edge': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'source': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StandardsAuthorityView': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'handle': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'content': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'operation_contracts': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'authorities': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StandardsAuthorityViewHandle': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'id': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'schema_version': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'StandardsAuthorityViewId': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'StructuredScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}, 'heading_path': {'title': None, 'description': None, 'has_default': False, 'default': None}}}, 'Submission': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {}}, 'WholeArtifactScope': {'title': None, 'description': None, 'has_default': False, 'default': None, 'properties': {'kind': {'title': None, 'description': None, 'has_default': False, 'default': None}}}})

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
class AnalysisContext:
    ''
    __definition__: ClassVar[str] = 'AnalysisContext'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'subjects': 'subjects',
        'semantic_proposals': 'semantic_proposals',
        'changes': 'changes',
    })
    kind: Literal['analysis-context']
    handle: AnalysisContextHandle
    subjects: tuple[ChangedPolicyUnit, ...]
    semantic_proposals: tuple[SemanticProposal, ...]
    changes: tuple[ChangeDescriptor, ...]

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
class AnalysisContextHandle:
    ''
    __definition__: ClassVar[str] = 'AnalysisContextHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['analysis-context-handle']
    id: AnalysisContextId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisContextHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AnalysisContextInspectionResult:
    ''
    __definition__: ClassVar[str] = 'AnalysisContextInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'context': 'context',
    })
    kind: Literal['analysis-context-inspection-result']
    context: AnalysisContext

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AnalysisContextInspectionResult:
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
class AnalysisRequest:
    ''
    __definition__: ClassVar[str] = 'AnalysisRequest'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'base_view': 'base_view',
        'proposed_view': 'proposed_view',
        'changes': 'changes',
        'semantic_proposals': 'semantic_proposals',
        'prior_analysis': 'prior_analysis',
        'contract_version': 'contract_version',
    })
    kind: Literal['analysis-request']
    base_view: StandardsAuthorityViewHandle
    proposed_view: StandardsAuthorityViewHandle
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
        'context': 'context',
        'fact_observations': 'fact_observations',
        'dispositions': 'dispositions',
        'coverage_attestations': 'coverage_attestations',
        'authority': 'authority',
    })
    kind: Literal['analysis-state']
    handle: AnalysisHandle
    context: AnalysisContext
    fact_observations: tuple[FactObservation, ...]
    dispositions: tuple[DispositionRecord, ...]
    coverage_attestations: tuple[CoverageAttestation, ...]
    authority: ExecutionClosureHandle

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
class AuthorityObjectReference:
    ''
    __definition__: ClassVar[str] = 'AuthorityObjectReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'object_kind': 'object_kind',
        'id': 'id',
    })
    object_kind: CanonicalId
    id: AuthorityObjectId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuthorityObjectReference:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class AuthorizationGrantReference:
    ''
    __definition__: ClassVar[str] = 'AuthorizationGrantReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'object_kind': 'object_kind',
        'id': 'id',
    })
    object_kind: Literal['authorization-grant']
    id: AuthorityObjectId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> AuthorizationGrantReference:
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
class CertificateHandle:
    ''
    __definition__: ClassVar[str] = 'CertificateHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['certificate-handle']
    id: CertificateId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CertificateHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CertificateInspectionResult:
    ''
    __definition__: ClassVar[str] = 'CertificateInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'certificate': 'certificate',
    })
    kind: Literal['certificate-inspection-result']
    certificate: ConsumerCoverageCertificate

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CertificateInspectionResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CertificateProvenance:
    ''
    __definition__: ClassVar[str] = 'CertificateProvenance'
    __contract_fields__: ClassVar = MappingProxyType({
        'generator': 'generator',
    })
    generator: NonEmptyString

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CertificateProvenance:
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
        'authority': 'authority',
        'summary': 'summary',
    })
    kind: Literal['complete-result']
    handle: AnalysisHandle
    status: Literal['complete']
    context: AnalysisContext
    changes: tuple[ChangeDescriptor, ...]
    changed_units: tuple[ChangedPolicyUnit, ...]
    coverage_certificates: tuple[CertificateHandle, ...]
    fact_observations: tuple[FactObservation, ...]
    dispositions: tuple[DispositionRecord, ...]
    reading_plan: tuple[ReadingPlanEntry, ...]
    completion: CompletionProof
    authority: ExecutionClosureHandle
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
class ConsumerCoverageCertificate:
    ''
    __definition__: ClassVar[str] = 'ConsumerCoverageCertificate'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'coverage_view': 'coverage_view',
        'requirement': 'requirement',
        'attestation': 'attestation',
        'subject': 'subject',
        'owner': 'owner',
        'semantic_revision': 'semantic_revision',
        'horizon_digest': 'horizon_digest',
        'relationship_digest': 'relationship_digest',
        'evidence_digests': 'evidence_digests',
        'provenance': 'provenance',
        'fact_schema_digest': 'fact_schema_digest',
        'authority_dependencies': 'authority_dependencies',
    })
    kind: Literal['consumer-coverage-certificate']
    handle: CertificateHandle
    coverage_view: CoverageAuthorityViewHandle
    requirement: CoverageRequirementHandle
    attestation: CoverageAttestationHandle
    subject: CanonicalId
    owner: CanonicalId
    semantic_revision: int | float
    horizon_digest: Digest
    relationship_digest: Digest
    evidence_digests: tuple[Digest, ...]
    provenance: CertificateProvenance
    fact_schema_digest: Digest
    authority_dependencies: tuple[AuthorityObjectReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ConsumerCoverageCertificate:
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
        'obligation_id': 'obligation_id',
        'result': 'result',
        'rationale': 'rationale',
        'evidence': 'evidence',
        'fingerprint': 'fingerprint',
    })
    kind: Literal['consumer-disposition']
    obligation_id: ObligationId
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
class ContentSnapshot:
    ''
    __definition__: ClassVar[str] = 'ContentSnapshot'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'payload_contract': 'payload_contract',
        'files': 'files',
    })
    kind: Literal['content-snapshot']
    handle: ContentSnapshotHandle
    payload_contract: Literal['content-snapshot.v2']
    files: tuple[ContentSnapshotFileEntry, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ContentSnapshot:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ContentSnapshotFileEntry:
    ''
    __definition__: ClassVar[str] = 'ContentSnapshotFileEntry'
    __contract_fields__: ClassVar = MappingProxyType({
        'path': 'path',
        'content_digest': 'content_digest',
        'content_base64': 'content_base64',
        'byte_length': 'byte_length',
    })
    path: RepositoryPath
    content_digest: Digest
    content_base64: str
    byte_length: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ContentSnapshotFileEntry:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ContentSnapshotHandle:
    ''
    __definition__: ClassVar[str] = 'ContentSnapshotHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['content-snapshot-handle']
    id: ContentSnapshotId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ContentSnapshotHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ContentSnapshotInspectionResult:
    ''
    __definition__: ClassVar[str] = 'ContentSnapshotInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'content_snapshot': 'content_snapshot',
    })
    kind: Literal['content-snapshot-inspection-result']
    content_snapshot: ContentSnapshot

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ContentSnapshotInspectionResult:
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
        'handle': 'handle',
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
    handle: CoverageAttestationHandle
    requirement: CoverageRequirementHandle
    conclusion: Literal['complete']
    evidence: tuple[EvidenceReference, ...]
    explicit_exclusions: tuple[EvidenceReference, ...]
    rationale: NonEmptyString
    auditor_provenance: NonEmptyString
    schema_version: int | float
    authorization: AuthorizationGrantReference

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
    requirement: CoverageRequirementHandle
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
class CoverageAttestationHandle:
    ''
    __definition__: ClassVar[str] = 'CoverageAttestationHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['coverage-attestation-handle']
    id: CoverageAttestationId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAttestationHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAttestationInspectionResult:
    ''
    __definition__: ClassVar[str] = 'CoverageAttestationInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'attestation': 'attestation',
    })
    kind: Literal['coverage-attestation-inspection-result']
    attestation: CoverageAttestation

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAttestationInspectionResult:
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
        'obligation_id': 'obligation_id',
        'claim': 'claim',
    })
    kind: Literal['coverage-attestation']
    obligation_id: ObligationId
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
class CoverageAuditRequirement:
    ''
    __definition__: ClassVar[str] = 'CoverageAuditRequirement'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'coverage_view': 'coverage_view',
        'subject': 'subject',
        'owner': 'owner',
        'semantic_revision': 'semantic_revision',
        'relationship_kinds': 'relationship_kinds',
        'horizon': 'horizon',
        'derived_from_view': 'derived_from_view',
        'required_evidence_contract': 'required_evidence_contract',
    })
    kind: Literal['coverage-audit-requirement']
    handle: CoverageRequirementHandle
    coverage_view: CoverageAuthorityViewHandle
    subject: CanonicalId
    owner: CanonicalId
    semantic_revision: int | float
    relationship_kinds: tuple[CanonicalId, ...]
    horizon: CanonicalId
    required_evidence_contract: CanonicalId
    derived_from_view: StandardsAuthorityViewHandle | MissingValue = MISSING

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAuditRequirement:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAuthorityView:
    ''
    __definition__: ClassVar[str] = 'CoverageAuthorityView'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'subject': 'subject',
        'owner': 'owner',
        'semantic_revision': 'semantic_revision',
        'representation_digest': 'representation_digest',
        'structural_digest': 'structural_digest',
        'relationship_kinds': 'relationship_kinds',
        'relationship_fingerprints': 'relationship_fingerprints',
        'applicability_program_digests': 'applicability_program_digests',
        'fact_schema_digest': 'fact_schema_digest',
        'horizon': 'horizon',
        'authority_dependencies': 'authority_dependencies',
    })
    kind: Literal['coverage-authority-view']
    handle: CoverageAuthorityViewHandle
    subject: CanonicalId
    owner: CanonicalId
    semantic_revision: int | float
    representation_digest: Digest
    structural_digest: Digest
    relationship_kinds: tuple[CanonicalId, ...]
    relationship_fingerprints: tuple[FrozenMap[str, object], ...]
    applicability_program_digests: tuple[Digest, ...]
    fact_schema_digest: Digest
    horizon: FrozenMap[str, object]
    authority_dependencies: tuple[AuthorityObjectReference, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAuthorityView:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAuthorityViewHandle:
    ''
    __definition__: ClassVar[str] = 'CoverageAuthorityViewHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['coverage-authority-view-handle']
    id: CoverageAuthorityViewId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAuthorityViewHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageAuthorityViewInspectionResult:
    ''
    __definition__: ClassVar[str] = 'CoverageAuthorityViewInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'coverage_view': 'coverage_view',
    })
    kind: Literal['coverage-authority-view-inspection-result']
    coverage_view: CoverageAuthorityView

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageAuthorityViewInspectionResult:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageHorizonMember:
    ''
    __definition__: ClassVar[str] = 'CoverageHorizonMember'
    __contract_fields__: ClassVar = MappingProxyType({
        'id': 'id',
        'roles': 'roles',
        'fingerprint': 'fingerprint',
    })
    id: CanonicalId
    roles: tuple[CanonicalId, ...]
    fingerprint: Digest

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageHorizonMember:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageRequirementHandle:
    ''
    __definition__: ClassVar[str] = 'CoverageRequirementHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['coverage-requirement-handle']
    id: CoverageRequirementId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageRequirementHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class CoverageRequirementInspectionResult:
    ''
    __definition__: ClassVar[str] = 'CoverageRequirementInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'requirement': 'requirement',
    })
    kind: Literal['coverage-requirement-inspection-result']
    requirement: CoverageAuditRequirement

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> CoverageRequirementInspectionResult:
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
class DispositionRecord:
    ''
    __definition__: ClassVar[str] = 'DispositionRecord'
    __contract_fields__: ClassVar = MappingProxyType({
        'obligation_id': 'obligation_id',
        'kind': 'kind',
        'result': 'result',
        'rationale': 'rationale',
        'evidence': 'evidence',
        'authorization': 'authorization',
        'fingerprint': 'fingerprint',
    })
    obligation_id: ObligationId
    kind: Literal['consumer-disposition', 'impact-disposition']
    result: NonEmptyString
    rationale: NonEmptyString
    evidence: tuple[EvidenceReference, ...]
    authorization: AuthorizationGrantReference
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
class ExecutionAuthorityRoot:
    ''
    __definition__: ClassVar[str] = 'ExecutionAuthorityRoot'
    __contract_fields__: ClassVar = MappingProxyType({
        'side': 'side',
        'role': 'role',
        'authority': 'authority',
    })
    side: Literal['current', 'accepted', 'proposed', 'transition']
    role: CanonicalId
    authority: AuthorityObjectReference

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ExecutionAuthorityRoot:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ExecutionClosure:
    ''
    __definition__: ClassVar[str] = 'ExecutionClosure'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'closure_contract': 'closure_contract',
        'operation': 'operation',
        'roots': 'roots',
    })
    kind: Literal['execution-closure']
    handle: ExecutionClosureHandle
    closure_contract: Literal['execution-closure.v2']
    operation: Literal['route', 'read', 'related', 'analysis']
    roots: tuple[ExecutionAuthorityRoot, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ExecutionClosure:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class ExecutionClosureHandle:
    ''
    __definition__: ClassVar[str] = 'ExecutionClosureHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['execution-closure-handle']
    id: ExecutionClosureId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ExecutionClosureHandle:
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
        'provider_authority': 'provider_authority',
    })
    kind: Literal['fact-observation']
    handle: FactObservationHandle
    requirement: FactRequirementHandle
    value: FactValue
    evidence: tuple[EvidenceReference, ...]
    authorization: AuthorizationGrantReference
    provider_authority: ProviderAuthorityReference | MissingValue = MISSING

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
class FactObservationHandle:
    ''
    __definition__: ClassVar[str] = 'FactObservationHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['fact-observation-handle']
    id: FactObservationId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactObservationHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FactObservationInspectionResult:
    ''
    __definition__: ClassVar[str] = 'FactObservationInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'observation': 'observation',
    })
    kind: Literal['fact-observation-inspection-result']
    observation: FactObservation

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactObservationInspectionResult:
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
        'authority_dependencies': 'authority_dependencies',
    })
    kind: Literal['fact-requirement']
    handle: FactRequirementHandle
    fact: CanonicalId
    fact_semantic_revision: int | float
    fact_contract_digest: Digest
    context: AnalysisContextHandle
    value_contract: FactValueContract
    answer_contract: CanonicalId
    evidence_contract: CanonicalId
    authorization_capability: CanonicalId
    authority_dependencies: tuple[AuthorityObjectReference, ...]

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
class FactRequirementHandle:
    ''
    __definition__: ClassVar[str] = 'FactRequirementHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['fact-requirement-handle']
    id: FactRequirementId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactRequirementHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class FactRequirementInspectionResult:
    ''
    __definition__: ClassVar[str] = 'FactRequirementInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'requirement': 'requirement',
    })
    kind: Literal['fact-requirement-inspection-result']
    requirement: FactRequirement

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> FactRequirementInspectionResult:
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
        'obligation_id': 'obligation_id',
        'result': 'result',
        'rationale': 'rationale',
        'evidence': 'evidence',
        'fingerprint': 'fingerprint',
    })
    kind: Literal['impact-disposition']
    obligation_id: ObligationId
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
        'target': 'target',
        'view': 'view',
    })
    operation: Literal['inspect']
    request_kind: Literal['inspect']
    target: CanonicalId
    view: StandardsAuthorityViewHandle

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
class NavigationHandle:
    ''
    __definition__: ClassVar[str] = 'NavigationHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['navigation-handle']
    id: NavigationId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> NavigationHandle:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class NavigationInspectionResult:
    ''
    __definition__: ClassVar[str] = 'NavigationInspectionResult'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'navigation': 'navigation',
    })
    kind: Literal['navigation-inspection-result']
    navigation: NavigationResult

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> NavigationInspectionResult:
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
        'id': 'id',
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
    id: ObligationId
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
class OperationAuthoritySelection:
    ''
    __definition__: ClassVar[str] = 'OperationAuthoritySelection'
    __contract_fields__: ClassVar = MappingProxyType({
        'operation': 'operation',
        'authority': 'authority',
    })
    operation: Literal['route', 'read', 'related', 'analysis']
    authority: AuthorityObjectReference

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> OperationAuthoritySelection:
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
        'authority': 'authority',
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
    authority: ExecutionClosureHandle
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
class PolicyHandle:
    ''
    __definition__: ClassVar[str] = 'PolicyHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['policy-handle']
    id: PolicyId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> PolicyHandle:
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
    policy: PolicyHandle
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
    handle: PolicyHandle
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
class ProvenanceRecord:
    ''
    __definition__: ClassVar[str] = 'ProvenanceRecord'
    __contract_fields__: ClassVar = MappingProxyType({
        'source_id': 'source_id',
        'source_kind': 'source_kind',
        'locator': 'locator',
        'content_snapshot': 'content_snapshot',
    })
    source_id: CanonicalId
    source_kind: Literal['manifest', 'generator', 'provider', 'canonical-document', 'sidecar']
    locator: NonEmptyString
    content_snapshot: ContentSnapshotHandle

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
    requirement: FactRequirementHandle
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
class ProviderAuthorityReference:
    ''
    __definition__: ClassVar[str] = 'ProviderAuthorityReference'
    __contract_fields__: ClassVar = MappingProxyType({
        'object_kind': 'object_kind',
        'id': 'id',
    })
    object_kind: Literal['provider-authority']
    id: AuthorityObjectId

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> ProviderAuthorityReference:
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
        'view': 'view',
        'request': 'request',
    })
    view: StandardsAuthorityViewHandle
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
        'view': 'view',
    })
    operation: Literal['query']
    request_kind: Literal['route', 'read', 'related']
    view: StandardsAuthorityViewHandle
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
        'handle': 'handle',
        'authority': 'authority',
        'policy': 'policy',
        'content': 'content',
        'requires': 'requires',
        'specializes': 'specializes',
        'related': 'related',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['read-result']
    handle: NavigationHandle
    authority: ExecutionClosureHandle
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
    target: CanonicalId | MissingValue = MISSING

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
        'handle': 'handle',
        'authority': 'authority',
        'target': 'target',
        'policy_unit_mapping': 'policy_unit_mapping',
        'relationships': 'relationships',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['related-result']
    handle: NavigationHandle
    authority: ExecutionClosureHandle
    target: CanonicalId
    policy_unit_mapping: FrozenMap[str, object]
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
class RelationshipHandle:
    ''
    __definition__: ClassVar[str] = 'RelationshipHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['relationship-handle']
    id: RelationshipInspectionId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RelationshipHandle:
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
    handle: RelationshipHandle
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
class RepositoryPath:
    ''
    __definition__: ClassVar[str] = 'RepositoryPath'
    __contract_fields__: ClassVar = MappingProxyType({
        'components': 'components',
    })
    components: tuple[str, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> RepositoryPath:
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
        'obligation_id': 'obligation_id',
        'requirement_id': 'requirement_id',
        'analysis': 'analysis',
    })
    operation: Literal['resolve']
    request_kind: Literal['provide-fact', 'consumer-disposition', 'impact-disposition', 'coverage-attestation']
    analysis: AnalysisHandle
    target: CanonicalId | MissingValue = MISSING
    obligation_id: ObligationId | MissingValue = MISSING
    requirement_id: FactRequirementId | MissingValue = MISSING

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
        'handle': 'handle',
        'authority': 'authority',
        'reading_plan': 'reading_plan',
        'unresolved_questions': 'unresolved_questions',
        'next_operations': 'next_operations',
        'summary': 'summary',
    })
    kind: Literal['route-result']
    handle: NavigationHandle
    authority: ExecutionClosureHandle
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
class SemanticAuthoritySelection:
    ''
    __definition__: ClassVar[str] = 'SemanticAuthoritySelection'
    __contract_fields__: ClassVar = MappingProxyType({
        'role': 'role',
        'authority': 'authority',
    })
    role: CanonicalId
    authority: AuthorityObjectReference

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> SemanticAuthoritySelection:
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
class StandardsAuthorityView:
    ''
    __definition__: ClassVar[str] = 'StandardsAuthorityView'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'handle': 'handle',
        'content': 'content',
        'operation_contracts': 'operation_contracts',
        'authorities': 'authorities',
    })
    kind: Literal['standards-authority-view']
    handle: StandardsAuthorityViewHandle
    content: ContentSnapshotHandle
    operation_contracts: tuple[OperationAuthoritySelection, ...]
    authorities: tuple[SemanticAuthoritySelection, ...]

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> StandardsAuthorityView:
        selected = _RUNTIME.decode(cls.__definition__, value)
        if not isinstance(selected, cls):
            raise TypeError('decoded value has the wrong generated type')
        return selected

    def as_contract(self) -> dict[str, object]:
        return model_as_contract(self)

@dataclass(frozen=True, slots=True)
class StandardsAuthorityViewHandle:
    ''
    __definition__: ClassVar[str] = 'StandardsAuthorityViewHandle'
    __contract_fields__: ClassVar = MappingProxyType({
        'kind': 'kind',
        'id': 'id',
        'schema_version': 'schema_version',
    })
    kind: Literal['standards-authority-view-handle']
    id: StandardsAuthorityViewId
    schema_version: int | float

    def __post_init__(self) -> None:
        _RUNTIME.normalize_model(self)

    @classmethod
    def from_value(cls, value: object) -> StandardsAuthorityViewHandle:
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

AnalysisContextId: TypeAlias = str
AnalysisId: TypeAlias = str
ApplicabilityExpression: TypeAlias = AlwaysExpression | AllExpression | AnyExpression | NotExpression | EqualsExpression | InExpression | ContainsExpression | ExistsExpression
AuthorityObjectId: TypeAlias = str
CanonicalId: TypeAlias = str
CertificateId: TypeAlias = str
ContentSnapshotId: TypeAlias = str
CoverageAttestationId: TypeAlias = str
CoverageAuthorityViewId: TypeAlias = str
CoverageRequirementId: TypeAlias = str
Digest: TypeAlias = str
EdgeId: TypeAlias = str
ExecutionClosureId: TypeAlias = str
FactObservationId: TypeAlias = str
FactRequirementId: TypeAlias = str
FactValue: TypeAlias = FrozenMap[str, object]
FactSet: TypeAlias = FrozenMap[str, FactValue]
ImpactTraceId: TypeAlias = str
InspectableHandle: TypeAlias = ContentSnapshotHandle | StandardsAuthorityViewHandle | ExecutionClosureHandle | NavigationHandle | AnalysisHandle | PolicyHandle | RelationshipHandle | CertificateHandle | CoverageAuthorityViewHandle | CoverageRequirementHandle | CoverageAttestationHandle | AnalysisContextHandle | FactRequirementHandle | FactObservationHandle
InspectionResult: TypeAlias = ContentSnapshotInspectionResult | PolicyInspectionResult | RelationshipInspectionResult | NavigationInspectionResult | CertificateInspectionResult | CoverageAuthorityViewInspectionResult | CoverageRequirementInspectionResult | CoverageAttestationInspectionResult | AnalysisContextInspectionResult | FactRequirementInspectionResult | FactObservationInspectionResult | AnalysisState | StandardsAuthorityView | ExecutionClosure
NavigationId: TypeAlias = str
NavigationResult: TypeAlias = RouteResult | ReadResult | RelatedResult
NextOperation: TypeAlias = QueryNextOperation | ResolveNextOperation | InspectNextOperation
NonEmptyString: TypeAlias = str
ObligationId: TypeAlias = str
PolicyId: TypeAlias = str
QueryRequest: TypeAlias = RouteRequest | ReadRequest | RelatedRequest
ReadingPlanReason: TypeAlias = ConsumerReviewObligationReadingReason | RoutingBaseReadingReason | RoutingRuleReadingReason | RequiresReadingReason | SpecializesReadingReason
RelationshipInspectionId: TypeAlias = str
ReviewScope: TypeAlias = StructuredScope | WholeArtifactScope
ScalarValue: TypeAlias = bool | int | float | str | None
SelectionReason: TypeAlias = GeneralSelectionReason | PolicyImpactSelectionReason
StandardsAuthorityViewId: TypeAlias = str
Submission: TypeAlias = ProvideFactSubmission | ConsumerDispositionSubmission | ImpactDispositionSubmission | CoverageAttestationSubmission

MODEL_TYPES = MappingProxyType({
    'AllExpression': AllExpression,
    'AlwaysExpression': AlwaysExpression,
    'AnalysisContext': AnalysisContext,
    'AnalysisContextHandle': AnalysisContextHandle,
    'AnalysisContextInspectionResult': AnalysisContextInspectionResult,
    'AnalysisHandle': AnalysisHandle,
    'AnalysisRequest': AnalysisRequest,
    'AnalysisState': AnalysisState,
    'AnyExpression': AnyExpression,
    'AuthorityObjectReference': AuthorityObjectReference,
    'AuthorizationGrantReference': AuthorizationGrantReference,
    'CanonicalModuleDeclaration': CanonicalModuleDeclaration,
    'CertificateHandle': CertificateHandle,
    'CertificateInspectionResult': CertificateInspectionResult,
    'CertificateProvenance': CertificateProvenance,
    'ChangeDescriptor': ChangeDescriptor,
    'ChangedPolicyUnit': ChangedPolicyUnit,
    'CompleteResult': CompleteResult,
    'CompletionProof': CompletionProof,
    'ConsumerCoverageCertificate': ConsumerCoverageCertificate,
    'ConsumerDispositionSubmission': ConsumerDispositionSubmission,
    'ConsumerReviewContract': ConsumerReviewContract,
    'ConsumerReviewObligationReadingReason': ConsumerReviewObligationReadingReason,
    'ContainsExpression': ContainsExpression,
    'ContentSnapshot': ContentSnapshot,
    'ContentSnapshotFileEntry': ContentSnapshotFileEntry,
    'ContentSnapshotHandle': ContentSnapshotHandle,
    'ContentSnapshotInspectionResult': ContentSnapshotInspectionResult,
    'CoverageAttestation': CoverageAttestation,
    'CoverageAttestationClaim': CoverageAttestationClaim,
    'CoverageAttestationHandle': CoverageAttestationHandle,
    'CoverageAttestationInspectionResult': CoverageAttestationInspectionResult,
    'CoverageAttestationSubmission': CoverageAttestationSubmission,
    'CoverageAuditRequirement': CoverageAuditRequirement,
    'CoverageAuthorityView': CoverageAuthorityView,
    'CoverageAuthorityViewHandle': CoverageAuthorityViewHandle,
    'CoverageAuthorityViewInspectionResult': CoverageAuthorityViewInspectionResult,
    'CoverageHorizonMember': CoverageHorizonMember,
    'CoverageRequirementHandle': CoverageRequirementHandle,
    'CoverageRequirementInspectionResult': CoverageRequirementInspectionResult,
    'DecisionDependency': DecisionDependency,
    'DecisionFingerprint': DecisionFingerprint,
    'DispositionRecord': DispositionRecord,
    'EqualsExpression': EqualsExpression,
    'EvidenceReference': EvidenceReference,
    'ExecutionAuthorityRoot': ExecutionAuthorityRoot,
    'ExecutionClosure': ExecutionClosure,
    'ExecutionClosureHandle': ExecutionClosureHandle,
    'ExistsExpression': ExistsExpression,
    'FactObservation': FactObservation,
    'FactObservationHandle': FactObservationHandle,
    'FactObservationInspectionResult': FactObservationInspectionResult,
    'FactRequirement': FactRequirement,
    'FactRequirementHandle': FactRequirementHandle,
    'FactRequirementInspectionResult': FactRequirementInspectionResult,
    'FactRequirementWork': FactRequirementWork,
    'FactValueContract': FactValueContract,
    'GeneralSelectionReason': GeneralSelectionReason,
    'ImpactDispositionSubmission': ImpactDispositionSubmission,
    'ImpactTraceReference': ImpactTraceReference,
    'InExpression': InExpression,
    'InspectCall': InspectCall,
    'InspectNextOperation': InspectNextOperation,
    'NavigationHandle': NavigationHandle,
    'NavigationInspectionResult': NavigationInspectionResult,
    'NotExpression': NotExpression,
    'Obligation': Obligation,
    'OperationAuthoritySelection': OperationAuthoritySelection,
    'PendingResult': PendingResult,
    'PolicyHandle': PolicyHandle,
    'PolicyImpactSelectionReason': PolicyImpactSelectionReason,
    'PolicyInspectionResult': PolicyInspectionResult,
    'PolicyRelationshipInspection': PolicyRelationshipInspection,
    'PolicySummary': PolicySummary,
    'PolicyUnitDeclaration': PolicyUnitDeclaration,
    'PrepareCall': PrepareCall,
    'ProvenanceRecord': ProvenanceRecord,
    'ProvideFactSubmission': ProvideFactSubmission,
    'ProviderAuthorityReference': ProviderAuthorityReference,
    'QueryCall': QueryCall,
    'QueryNextOperation': QueryNextOperation,
    'Question': Question,
    'ReadRequest': ReadRequest,
    'ReadResult': ReadResult,
    'ReadingPlanEntry': ReadingPlanEntry,
    'RejectedResult': RejectedResult,
    'RelatedRequest': RelatedRequest,
    'RelatedResult': RelatedResult,
    'RelationshipHandle': RelationshipHandle,
    'RelationshipInspectionResult': RelationshipInspectionResult,
    'RelationshipSummary': RelationshipSummary,
    'RepositoryPath': RepositoryPath,
    'RequiresReadingReason': RequiresReadingReason,
    'ResolveCall': ResolveCall,
    'ResolveNextOperation': ResolveNextOperation,
    'RouteRequest': RouteRequest,
    'RouteResult': RouteResult,
    'RoutingBaseReadingReason': RoutingBaseReadingReason,
    'RoutingRuleReadingReason': RoutingRuleReadingReason,
    'SemanticAuthoritySelection': SemanticAuthoritySelection,
    'SemanticProposal': SemanticProposal,
    'SpecializesReadingReason': SpecializesReadingReason,
    'StandardsAuthorityView': StandardsAuthorityView,
    'StandardsAuthorityViewHandle': StandardsAuthorityViewHandle,
    'StructuredScope': StructuredScope,
    'WholeArtifactScope': WholeArtifactScope,
})
_RUNTIME = ContractRuntime(_SCHEMA, MODEL_TYPES)

def decode_contract(definition: str, value: object) -> object:
    return _RUNTIME.decode(definition, value)

__all__ = (
    'AllExpression',
    'AlwaysExpression',
    'AnalysisContext',
    'AnalysisContextHandle',
    'AnalysisContextId',
    'AnalysisContextInspectionResult',
    'AnalysisHandle',
    'AnalysisId',
    'AnalysisRequest',
    'AnalysisState',
    'AnyExpression',
    'ApplicabilityExpression',
    'AuthorityObjectId',
    'AuthorityObjectReference',
    'AuthorizationGrantReference',
    'CanonicalId',
    'CanonicalModuleDeclaration',
    'CertificateHandle',
    'CertificateId',
    'CertificateInspectionResult',
    'CertificateProvenance',
    'ChangeDescriptor',
    'ChangedPolicyUnit',
    'CompleteResult',
    'CompletionProof',
    'ConsumerCoverageCertificate',
    'ConsumerDispositionSubmission',
    'ConsumerReviewContract',
    'ConsumerReviewObligationReadingReason',
    'ContainsExpression',
    'ContentSnapshot',
    'ContentSnapshotFileEntry',
    'ContentSnapshotHandle',
    'ContentSnapshotId',
    'ContentSnapshotInspectionResult',
    'CoverageAttestation',
    'CoverageAttestationClaim',
    'CoverageAttestationHandle',
    'CoverageAttestationId',
    'CoverageAttestationInspectionResult',
    'CoverageAttestationSubmission',
    'CoverageAuditRequirement',
    'CoverageAuthorityView',
    'CoverageAuthorityViewHandle',
    'CoverageAuthorityViewId',
    'CoverageAuthorityViewInspectionResult',
    'CoverageHorizonMember',
    'CoverageRequirementHandle',
    'CoverageRequirementId',
    'CoverageRequirementInspectionResult',
    'DecisionDependency',
    'DecisionFingerprint',
    'Digest',
    'DispositionRecord',
    'EdgeId',
    'EqualsExpression',
    'EvidenceReference',
    'ExecutionAuthorityRoot',
    'ExecutionClosure',
    'ExecutionClosureHandle',
    'ExecutionClosureId',
    'ExistsExpression',
    'FactObservation',
    'FactObservationHandle',
    'FactObservationId',
    'FactObservationInspectionResult',
    'FactRequirement',
    'FactRequirementHandle',
    'FactRequirementId',
    'FactRequirementInspectionResult',
    'FactRequirementWork',
    'FactSet',
    'FactValue',
    'FactValueContract',
    'GeneralSelectionReason',
    'ImpactDispositionSubmission',
    'ImpactTraceId',
    'ImpactTraceReference',
    'InExpression',
    'InspectCall',
    'InspectNextOperation',
    'InspectableHandle',
    'InspectionResult',
    'NavigationHandle',
    'NavigationId',
    'NavigationInspectionResult',
    'NavigationResult',
    'NextOperation',
    'NonEmptyString',
    'NotExpression',
    'Obligation',
    'ObligationId',
    'OperationAuthoritySelection',
    'PendingResult',
    'PolicyHandle',
    'PolicyId',
    'PolicyImpactSelectionReason',
    'PolicyInspectionResult',
    'PolicyRelationshipInspection',
    'PolicySummary',
    'PolicyUnitDeclaration',
    'PrepareCall',
    'ProvenanceRecord',
    'ProvideFactSubmission',
    'ProviderAuthorityReference',
    'QueryCall',
    'QueryNextOperation',
    'QueryRequest',
    'Question',
    'ReadRequest',
    'ReadResult',
    'ReadingPlanEntry',
    'ReadingPlanReason',
    'RejectedResult',
    'RelatedRequest',
    'RelatedResult',
    'RelationshipHandle',
    'RelationshipInspectionId',
    'RelationshipInspectionResult',
    'RelationshipSummary',
    'RepositoryPath',
    'RequiresReadingReason',
    'ResolveCall',
    'ResolveNextOperation',
    'ReviewScope',
    'RouteRequest',
    'RouteResult',
    'RoutingBaseReadingReason',
    'RoutingRuleReadingReason',
    'ScalarValue',
    'SelectionReason',
    'SemanticAuthoritySelection',
    'SemanticProposal',
    'SpecializesReadingReason',
    'StandardsAuthorityView',
    'StandardsAuthorityViewHandle',
    'StandardsAuthorityViewId',
    'StructuredScope',
    'Submission',
    'WholeArtifactScope',
    'DEFINITION_METADATA',
    'decode_contract',
)
