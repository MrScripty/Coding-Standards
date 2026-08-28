from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

from tools.standards_authority.standards_authority import (
    AuthorityReference,
    CodecContext,
    CodecSet,
    ExecutionClosure,
    invalid,
    unsupported,
)
from tools.standards_identity.standards_identity import (
    IdentityArray,
    IdentityObject,
    IdentityValue,
    hash_identity,
)

Operation = Literal["route", "read", "related", "analysis"]


@dataclass(frozen=True, slots=True, order=True)
class RoleRequirement:
    role: str
    object_kind: str
    minimum_cardinality: int
    maximum_cardinality: int | None

    def __post_init__(self) -> None:
        _nonempty(self.role, "role")
        _nonempty(self.object_kind, "object_kind")
        if type(self.minimum_cardinality) is not int or self.minimum_cardinality < 0:
            raise invalid(
                "ENGINE.INVALID_CARDINALITY",
                "minimum cardinality must be a nonnegative exact integer",
            )
        maximum = self.maximum_cardinality
        if maximum is not None and (
            type(maximum) is not int or maximum < self.minimum_cardinality
        ):
            raise invalid(
                "ENGINE.INVALID_CARDINALITY",
                "maximum cardinality must be null or at least the minimum",
            )


@dataclass(frozen=True, slots=True, init=False)
class OperationAuthorityContract:
    operation: Operation
    compatibility_revision: int
    required_view_roles: tuple[RoleRequirement, ...]
    allowed_dynamic_roles: tuple[RoleRequirement, ...]

    def __init__(
        self,
        operation: Operation,
        compatibility_revision: int,
        required_view_roles: Iterable[RoleRequirement],
        allowed_dynamic_roles: Iterable[RoleRequirement],
    ) -> None:
        if operation not in {"route", "read", "related", "analysis"}:
            raise invalid("ENGINE.INVALID_OPERATION", repr(operation))
        if type(compatibility_revision) is not int or compatibility_revision < 1:
            raise invalid(
                "ENGINE.INVALID_COMPATIBILITY_REVISION",
                "compatibility revision must be a positive exact integer",
            )
        required = _requirements(required_view_roles, "required view")
        dynamic = _requirements(allowed_dynamic_roles, "dynamic")
        if set(item.role for item in required) & set(item.role for item in dynamic):
            raise invalid(
                "ENGINE.OVERLAPPING_AUTHORITY_ROLE",
                "required and dynamic role sets must be disjoint",
            )
        object.__setattr__(self, "operation", operation)
        object.__setattr__(self, "compatibility_revision", compatibility_revision)
        object.__setattr__(self, "required_view_roles", required)
        object.__setattr__(self, "allowed_dynamic_roles", dynamic)

    @property
    def compatibility_key(self) -> tuple[Operation, int]:
        return self.operation, self.compatibility_revision


@dataclass(frozen=True, slots=True, order=True)
class OperationAuthoritySelection:
    operation: Operation
    authority: AuthorityReference

    def __post_init__(self) -> None:
        if self.operation not in {"route", "read", "related", "analysis"}:
            raise invalid("ENGINE.INVALID_OPERATION", repr(self.operation))
        if self.authority.object_kind != "operation-authority-contract":
            raise invalid(
                "ENGINE.INVALID_OPERATION_AUTHORITY_KIND",
                "operation selection must reference an operation authority contract",
            )


@dataclass(frozen=True, slots=True, order=True)
class SemanticAuthoritySelection:
    role: str
    authority: AuthorityReference

    def __post_init__(self) -> None:
        _nonempty(self.role, "role")


@dataclass(frozen=True, slots=True, init=False)
class StandardsAuthorityView:
    content: AuthorityReference
    operation_contracts: tuple[OperationAuthoritySelection, ...]
    authorities: tuple[SemanticAuthoritySelection, ...]

    def __init__(
        self,
        content: AuthorityReference,
        operation_contracts: Iterable[OperationAuthoritySelection],
        authorities: Iterable[SemanticAuthoritySelection],
    ) -> None:
        if content.object_kind != "content-snapshot":
            raise invalid(
                "ENGINE.INVALID_CONTENT_AUTHORITY",
                "a standards authority view requires a content snapshot",
            )
        operations = tuple(sorted(operation_contracts))
        semantic = tuple(sorted(authorities))
        if tuple(item.operation for item in operations) != (
            "analysis",
            "read",
            "related",
            "route",
        ):
            raise invalid(
                "ENGINE.OPERATION_CONTRACT_CLOSURE",
                "the view must select each operation exactly once",
            )
        roles = tuple(item.role for item in semantic)
        if len(set(roles)) != len(roles):
            raise invalid(
                "ENGINE.DUPLICATE_AUTHORITY_ROLE",
                "semantic authority roles must be unique",
            )
        object.__setattr__(self, "content", content)
        object.__setattr__(self, "operation_contracts", operations)
        object.__setattr__(self, "authorities", semantic)


@dataclass(frozen=True, slots=True)
class NavigationAuthority:
    operation: Literal["route", "read", "related"]
    request: IdentityValue
    semantic_result: IdentityValue
    authority: AuthorityReference

    def __post_init__(self) -> None:
        if self.operation not in {"route", "read", "related"}:
            raise invalid("ENGINE.INVALID_NAVIGATION_OPERATION", repr(self.operation))
        if self.authority.object_kind != "execution-closure":
            raise invalid(
                "ENGINE.INVALID_NAVIGATION_AUTHORITY",
                "navigation results require an execution closure",
            )


@dataclass(frozen=True, slots=True)
class PolicyInspectionAuthority:
    target: str
    projection: IdentityValue
    authority: AuthorityReference
    metadata: AuthorityReference

    def __post_init__(self) -> None:
        _nonempty(self.target, "target")
        _require_kind(self.authority, "execution-closure")
        _require_kind(self.metadata, "canonical-standards-corpus")


@dataclass(frozen=True, slots=True)
class RelationshipInspectionAuthority:
    target: str
    projection: IdentityValue
    authority: AuthorityReference
    graph: AuthorityReference
    policy_impact: AuthorityReference

    def __post_init__(self) -> None:
        _nonempty(self.target, "target")
        _require_kind(self.authority, "execution-closure")
        _require_kind(self.graph, "standards-graph")
        _require_kind(self.policy_impact, "compiled-policy-impact")


class OperationAuthorityContractCodec:
    object_kind = "operation-authority-contract"
    payload_contract = "operation-authority-contract.v2"
    allowed_dependency_kinds = frozenset[str]()

    def encode(self, value: OperationAuthorityContract) -> IdentityValue:
        return _operation_contract_value(value)

    def decode(
        self, payload: IdentityValue, context: CodecContext
    ) -> OperationAuthorityContract:
        del context
        members = _members(
            payload,
            {
                "operation",
                "compatibility_revision",
                "required_view_roles",
                "allowed_dynamic_roles",
            },
            "operation authority contract",
        )
        operation = _operation(members["operation"])
        revision = _integer(members["compatibility_revision"], "revision", minimum=1)
        return OperationAuthorityContract(
            operation,
            revision,
            _decode_requirements(members["required_view_roles"]),
            _decode_requirements(members["allowed_dynamic_roles"]),
        )

    def semantic_id(
        self, value: OperationAuthorityContract, context: CodecContext
    ) -> str:
        del context
        return hash_identity(
            "coding-standards:operation-authority-contract-identity:v1",
            "operation-authority-contract",
            _operation_contract_value(value),
        )

    def direct_dependencies(
        self, value: OperationAuthorityContract
    ) -> tuple[AuthorityReference, ...]:
        del value
        return ()


class StandardsAuthorityViewCodec:
    object_kind = "standards-authority-view"
    payload_contract = "standards-authority-view.v1"
    allowed_dependency_kinds = frozenset(
        {
            "content-snapshot",
            "operation-authority-contract",
            "canonical-standards-corpus",
            "routing-projection",
            "standards-graph",
            "compiled-policy-impact",
            "coverage-horizon",
        }
    )

    def encode(self, value: StandardsAuthorityView) -> IdentityValue:
        return _view_value(value)

    def decode(
        self, payload: IdentityValue, context: CodecContext
    ) -> StandardsAuthorityView:
        members = _members(
            payload, {"content", "operation_contracts", "authorities"}, "view"
        )
        view = StandardsAuthorityView(
            _decode_reference(members["content"]),
            _decode_operation_selections(members["operation_contracts"]),
            _decode_semantic_selections(members["authorities"]),
        )
        validate_standards_authority_view(view, context, None)
        return view

    def semantic_id(self, value: StandardsAuthorityView, context: CodecContext) -> str:
        validate_standards_authority_view(value, context, None)
        return hash_identity(
            "coding-standards:standards-authority-view:v1",
            "standards-authority-view",
            _view_value(value),
        )

    def direct_dependencies(
        self, value: StandardsAuthorityView
    ) -> tuple[AuthorityReference, ...]:
        return tuple(
            sorted(
                {
                    value.content,
                    *(item.authority for item in value.operation_contracts),
                    *(item.authority for item in value.authorities),
                }
            )
        )


class _ProjectionCodec:
    allowed_dependency_kinds: frozenset[str]
    value_type: type[object]
    identity_domain: str
    identity_label: str

    def encode(self, value: object) -> IdentityValue:
        return self._value(value)

    def decode(self, payload: IdentityValue, context: CodecContext) -> object:
        del context
        return self._decode(payload)

    def semantic_id(self, value: object, context: CodecContext) -> str:
        del context
        return hash_identity(self.identity_domain, self.identity_label, self._value(value))

    def direct_dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        return tuple(sorted(set(self._dependencies(value))))

    def _value(self, value: object) -> IdentityValue:
        raise NotImplementedError

    def _decode(self, payload: IdentityValue) -> object:
        raise NotImplementedError

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        raise NotImplementedError


class NavigationAuthorityCodec(_ProjectionCodec):
    object_kind = "navigation-result"
    payload_contract = "navigation-result.v1"
    allowed_dependency_kinds = frozenset({"execution-closure"})
    identity_domain = "coding-standards:navigation-result:v1"
    identity_label = "navigation-result"

    def _value(self, value: object) -> IdentityValue:
        if not isinstance(value, NavigationAuthority):
            raise invalid("ENGINE.INVALID_NAVIGATION_VALUE", repr(type(value)))
        return IdentityObject(
            (
                ("operation", value.operation),
                ("request", value.request),
                ("semantic_result", value.semantic_result),
                ("authority", _reference_value(value.authority)),
            )
        )

    def _decode(self, payload: IdentityValue) -> NavigationAuthority:
        members = _members(
            payload,
            {"operation", "request", "semantic_result", "authority"},
            "navigation result",
        )
        operation = _string(members["operation"], "operation")
        return NavigationAuthority(
            operation,  # type: ignore[arg-type]
            members["request"],
            members["semantic_result"],
            _decode_reference(members["authority"]),
        )

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, NavigationAuthority)
        return (value.authority,)


class PolicyInspectionAuthorityCodec(_ProjectionCodec):
    object_kind = "policy-inspection"
    payload_contract = "policy-inspection.v1"
    allowed_dependency_kinds = frozenset(
        {"execution-closure", "canonical-standards-corpus"}
    )
    identity_domain = "coding-standards:policy-inspection:v2"
    identity_label = "policy-inspection"

    def _value(self, value: object) -> IdentityValue:
        if not isinstance(value, PolicyInspectionAuthority):
            raise invalid("ENGINE.INVALID_POLICY_INSPECTION", repr(type(value)))
        return IdentityObject(
            (
                ("target", value.target),
                ("projection", value.projection),
                ("authority", _reference_value(value.authority)),
                ("metadata", _reference_value(value.metadata)),
            )
        )

    def _decode(self, payload: IdentityValue) -> PolicyInspectionAuthority:
        members = _members(
            payload,
            {"target", "projection", "authority", "metadata"},
            "policy inspection",
        )
        return PolicyInspectionAuthority(
            _string(members["target"], "target"),
            members["projection"],
            _decode_reference(members["authority"]),
            _decode_reference(members["metadata"]),
        )

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, PolicyInspectionAuthority)
        return value.authority, value.metadata


class RelationshipInspectionAuthorityCodec(_ProjectionCodec):
    object_kind = "relationship-inspection"
    payload_contract = "relationship-inspection.v1"
    allowed_dependency_kinds = frozenset(
        {"execution-closure", "standards-graph", "compiled-policy-impact"}
    )
    identity_domain = "coding-standards:relationship-inspection:v2"
    identity_label = "relationship-inspection"

    def _value(self, value: object) -> IdentityValue:
        if not isinstance(value, RelationshipInspectionAuthority):
            raise invalid("ENGINE.INVALID_RELATIONSHIP_INSPECTION", repr(type(value)))
        return IdentityObject(
            (
                ("target", value.target),
                ("projection", value.projection),
                ("authority", _reference_value(value.authority)),
                ("graph", _reference_value(value.graph)),
                ("policy_impact", _reference_value(value.policy_impact)),
            )
        )

    def _decode(self, payload: IdentityValue) -> RelationshipInspectionAuthority:
        members = _members(
            payload,
            {"target", "projection", "authority", "graph", "policy_impact"},
            "relationship inspection",
        )
        return RelationshipInspectionAuthority(
            _string(members["target"], "target"),
            members["projection"],
            _decode_reference(members["authority"]),
            _decode_reference(members["graph"]),
            _decode_reference(members["policy_impact"]),
        )

    def _dependencies(self, value: object) -> tuple[AuthorityReference, ...]:
        assert isinstance(value, RelationshipInspectionAuthority)
        return value.authority, value.graph, value.policy_impact


def validate_standards_authority_view(
    view: StandardsAuthorityView,
    context: CodecContext,
    supported_keys: frozenset[tuple[Operation, int]] | None,
) -> None:
    required: dict[str, str] = {}
    for selection in view.operation_contracts:
        selected = context.resolve(selection.authority)
        if not isinstance(selected, OperationAuthorityContract):
            raise invalid(
                "ENGINE.OPERATION_CONTRACT_TYPE",
                "operation authority did not decode to its owner type",
            )
        if selected.operation != selection.operation:
            raise invalid(
                "ENGINE.OPERATION_CONTRACT_MISMATCH",
                "operation selection and contract operation differ",
            )
        if supported_keys is not None and selected.compatibility_key not in supported_keys:
            raise unsupported(
                "ENGINE.UNSUPPORTED_OPERATION_COMPATIBILITY",
                repr(selected.compatibility_key),
            )
        for requirement in selected.required_view_roles:
            existing = required.setdefault(requirement.role, requirement.object_kind)
            if existing != requirement.object_kind:
                raise invalid(
                    "ENGINE.CONFLICTING_ROLE_KIND",
                    f"role {requirement.role!r} selects unequal object kinds",
                )
            if (
                requirement.minimum_cardinality != 1
                or requirement.maximum_cardinality != 1
            ):
                raise invalid(
                    "ENGINE.INVALID_VIEW_CARDINALITY",
                    "required view roles must have cardinality 1..1",
                )
    actual = {item.role: item.authority.object_kind for item in view.authorities}
    if actual != required:
        raise invalid(
            "ENGINE.VIEW_ROLE_CLOSURE",
            "view semantic authorities must exactly match required roles and kinds",
        )


def validate_execution_authority(
    closure: ExecutionClosure,
    contract_reference: AuthorityReference,
    contract: OperationAuthorityContract,
    view_sides: Iterable[str],
) -> None:
    sides = tuple(sorted(set(view_sides)))
    if not sides or any(not side for side in sides):
        raise invalid("ENGINE.INVALID_EXECUTION_SIDES", "execution sides are invalid")
    if closure.operation != contract.operation:
        raise invalid(
            "ENGINE.EXECUTION_OPERATION_MISMATCH",
            "execution closure and operation contract differ",
        )
    selected_operation = tuple(
        item
        for item in closure.roots
        if item.side == "current" and item.role == "operation-contract"
    )
    if (
        len(selected_operation) != 1
        or selected_operation[0].reference != contract_reference
    ):
        raise invalid(
            "ENGINE.EXECUTION_CONTRACT_CLOSURE",
            "execution closure must select its exact operation contract once",
        )
    required = {item.role: item for item in contract.required_view_roles}
    dynamic = {item.role: item for item in contract.allowed_dynamic_roles}
    for side in sides:
        actual = {
            item.role: item.reference
            for item in closure.roots
            if item.side == side and item.role in required
        }
        if set(actual) != set(required):
            raise invalid(
                "ENGINE.EXECUTION_VIEW_ROLE_CLOSURE",
                f"execution side {side!r} has an incomplete view role set",
            )
        if any(
            actual[role].object_kind != requirement.object_kind
            for role, requirement in required.items()
        ):
            raise invalid(
                "ENGINE.EXECUTION_VIEW_ROLE_KIND",
                "execution view role selects the wrong authority kind",
            )
    dynamic_roots = tuple(
        item
        for item in closure.roots
        if item.side == "current" and item.role in dynamic
    )
    for role, requirement in dynamic.items():
        selected = tuple(item for item in dynamic_roots if item.role == role)
        if len(selected) < requirement.minimum_cardinality or (
            requirement.maximum_cardinality is not None
            and len(selected) > requirement.maximum_cardinality
        ):
            raise invalid(
                "ENGINE.EXECUTION_DYNAMIC_CARDINALITY",
                f"dynamic role {role!r} violates its cardinality",
            )
        if any(item.reference.object_kind != requirement.object_kind for item in selected):
            raise invalid(
                "ENGINE.EXECUTION_DYNAMIC_ROLE_KIND",
                f"dynamic role {role!r} selects the wrong authority kind",
            )
    admitted = {
        (side, role)
        for side in sides
        for role in required
    } | {("current", role) for role in dynamic} | {
        ("current", "operation-contract")
    }
    unknown = tuple(
        item for item in closure.roots if (item.side, item.role) not in admitted
    )
    if unknown:
        raise invalid(
            "ENGINE.EXECUTION_UNKNOWN_ROLE",
            "execution closure contains an unadmitted side or role",
        )


def operation_contracts() -> tuple[OperationAuthorityContract, ...]:
    def exact(role: str, kind: str) -> RoleRequirement:
        return RoleRequirement(role, kind, 1, 1)

    def many(role: str, kind: str) -> RoleRequirement:
        return RoleRequirement(role, kind, 0, None)

    common = {
        "metadata": "canonical-standards-corpus",
        "graph": "standards-graph",
    }
    analysis_dynamic = (
        exact("context", "analysis-context"),
        many("requirement", "fact-requirement"),
        many("observation", "fact-observation"),
        many("coverage-view", "coverage-view"),
        many("coverage-requirement", "coverage-requirement"),
        many("coverage-attestation", "coverage-attestation"),
        many("coverage-certificate", "coverage-certificate"),
        many("provider-authority", "provider-authority"),
        many("authorization-grant", "authorization-grant"),
    )
    return (
        OperationAuthorityContract(
            "route",
            2,
            (exact("metadata", common["metadata"]), exact("routing", "routing-projection"), exact("graph", common["graph"])),
            (),
        ),
        OperationAuthorityContract(
            "read",
            2,
            (exact("metadata", common["metadata"]), exact("graph", common["graph"])),
            (),
        ),
        OperationAuthorityContract(
            "related",
            2,
            (exact("metadata", common["metadata"]), exact("graph", common["graph"])),
            (),
        ),
        OperationAuthorityContract(
            "analysis",
            2,
            (
                exact("metadata", common["metadata"]),
                exact("graph", common["graph"]),
                exact("policy-impact", "compiled-policy-impact"),
                exact("coverage", "coverage-horizon"),
            ),
            analysis_dynamic,
        ),
    )


def _requirements(
    values: Iterable[RoleRequirement], description: str
) -> tuple[RoleRequirement, ...]:
    exact = tuple(sorted(values))
    roles = tuple(item.role for item in exact)
    if len(set(roles)) != len(roles):
        raise invalid(
            "ENGINE.DUPLICATE_ROLE_REQUIREMENT",
            f"{description} role requirements must be unique",
        )
    return exact


def _operation_contract_value(value: OperationAuthorityContract) -> IdentityObject:
    return IdentityObject(
        (
            ("operation", value.operation),
            ("compatibility_revision", value.compatibility_revision),
            (
                "required_view_roles",
                IdentityArray(_requirement_value(item) for item in value.required_view_roles),
            ),
            (
                "allowed_dynamic_roles",
                IdentityArray(_requirement_value(item) for item in value.allowed_dynamic_roles),
            ),
        )
    )


def _requirement_value(value: RoleRequirement) -> IdentityObject:
    return IdentityObject(
        (
            ("role", value.role),
            ("object_kind", value.object_kind),
            ("minimum_cardinality", value.minimum_cardinality),
            ("maximum_cardinality", value.maximum_cardinality),
        )
    )


def _view_value(value: StandardsAuthorityView) -> IdentityObject:
    return IdentityObject(
        (
            ("content", _reference_value(value.content)),
            (
                "operation_contracts",
                IdentityArray(
                    IdentityObject(
                        (
                            ("operation", item.operation),
                            ("authority", _reference_value(item.authority)),
                        )
                    )
                    for item in value.operation_contracts
                ),
            ),
            (
                "authorities",
                IdentityArray(
                    IdentityObject(
                        (("role", item.role), ("authority", _reference_value(item.authority)))
                    )
                    for item in value.authorities
                ),
            ),
        )
    )


def _reference_value(value: AuthorityReference) -> IdentityObject:
    return IdentityObject(
        (("object_kind", value.object_kind), ("semantic_id", value.semantic_id))
    )


def _decode_reference(value: IdentityValue) -> AuthorityReference:
    members = _members(value, {"object_kind", "semantic_id"}, "authority reference")
    return AuthorityReference(
        _string(members["object_kind"], "object_kind"),
        _string(members["semantic_id"], "semantic_id"),
    )


def _decode_requirements(value: IdentityValue) -> tuple[RoleRequirement, ...]:
    raw = _array(value, "role requirements")
    return tuple(
        RoleRequirement(
            _string(item["role"], "role"),
            _string(item["object_kind"], "object_kind"),
            _integer(item["minimum_cardinality"], "minimum_cardinality", minimum=0),
            None
            if item["maximum_cardinality"] is None
            else _integer(item["maximum_cardinality"], "maximum_cardinality", minimum=0),
        )
        for item in (
            _members(
                raw_item,
                {"role", "object_kind", "minimum_cardinality", "maximum_cardinality"},
                "role requirement",
            )
            for raw_item in raw
        )
    )


def _decode_operation_selections(
    value: IdentityValue,
) -> tuple[OperationAuthoritySelection, ...]:
    return tuple(
        OperationAuthoritySelection(
            _operation(item["operation"]), _decode_reference(item["authority"])
        )
        for item in (
            _members(raw, {"operation", "authority"}, "operation selection")
            for raw in _array(value, "operation selections")
        )
    )


def _decode_semantic_selections(
    value: IdentityValue,
) -> tuple[SemanticAuthoritySelection, ...]:
    return tuple(
        SemanticAuthoritySelection(
            _string(item["role"], "role"), _decode_reference(item["authority"])
        )
        for item in (
            _members(raw, {"role", "authority"}, "semantic selection")
            for raw in _array(value, "semantic selections")
        )
    )


def _members(
    value: IdentityValue, expected: set[str], description: str
) -> dict[str, IdentityValue]:
    if type(value) is not IdentityObject:
        raise invalid("ENGINE.INVALID_PAYLOAD", f"{description} must be an object")
    members = dict(value.members)
    if set(members) != expected:
        raise invalid(
            "ENGINE.INVALID_PAYLOAD_FIELDS",
            f"{description} fields differ from the payload contract",
        )
    return members


def _array(value: IdentityValue, description: str) -> tuple[IdentityValue, ...]:
    if type(value) is not IdentityArray:
        raise invalid("ENGINE.INVALID_PAYLOAD", f"{description} must be an array")
    return value.values


def _string(value: IdentityValue, field: str) -> str:
    if type(value) is not str or not value:
        raise invalid("ENGINE.INVALID_PAYLOAD", f"{field} must be a nonempty string")
    return value


def _nonempty(value: object, field: str) -> str:
    if type(value) is not str or not value:
        raise invalid("ENGINE.INVALID_VALUE", f"{field} must be a nonempty string")
    return value


def _integer(value: IdentityValue, field: str, *, minimum: int) -> int:
    if type(value) is not int or value < minimum:
        raise invalid(
            "ENGINE.INVALID_PAYLOAD",
            f"{field} must be an exact integer >= {minimum}",
        )
    return value


def _operation(value: IdentityValue) -> Operation:
    selected = _string(value, "operation")
    if selected not in {"route", "read", "related", "analysis"}:
        raise invalid("ENGINE.INVALID_OPERATION", repr(selected))
    return selected  # type: ignore[return-value]


def _require_kind(reference: AuthorityReference, expected: str) -> None:
    if reference.object_kind != expected:
        raise invalid(
            "ENGINE.INVALID_AUTHORITY_KIND",
            f"expected {expected!r}, observed {reference.object_kind!r}",
        )


OPERATION_AUTHORITY_CODEC = OperationAuthorityContractCodec()
STANDARDS_AUTHORITY_VIEW_CODEC = StandardsAuthorityViewCodec()
NAVIGATION_AUTHORITY_CODEC = NavigationAuthorityCodec()
POLICY_INSPECTION_AUTHORITY_CODEC = PolicyInspectionAuthorityCodec()
RELATIONSHIP_INSPECTION_AUTHORITY_CODEC = RelationshipInspectionAuthorityCodec()

ENGINE_CODECS = CodecSet(
    "standards-engine",
    (
        OPERATION_AUTHORITY_CODEC,
        STANDARDS_AUTHORITY_VIEW_CODEC,
        NAVIGATION_AUTHORITY_CODEC,
        POLICY_INSPECTION_AUTHORITY_CODEC,
        RELATIONSHIP_INSPECTION_AUTHORITY_CODEC,
    ),
)

__all__ = (
    "ENGINE_CODECS",
    "NAVIGATION_AUTHORITY_CODEC",
    "OPERATION_AUTHORITY_CODEC",
    "POLICY_INSPECTION_AUTHORITY_CODEC",
    "RELATIONSHIP_INSPECTION_AUTHORITY_CODEC",
    "STANDARDS_AUTHORITY_VIEW_CODEC",
    "NavigationAuthority",
    "OperationAuthorityContract",
    "OperationAuthoritySelection",
    "PolicyInspectionAuthority",
    "RelationshipInspectionAuthority",
    "RoleRequirement",
    "SemanticAuthoritySelection",
    "StandardsAuthorityView",
    "operation_contracts",
    "validate_execution_authority",
    "validate_standards_authority_view",
)
