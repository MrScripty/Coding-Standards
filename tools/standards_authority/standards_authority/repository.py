from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


from .envelope import decode_envelope, encode_envelope, encode_storage_key
from .errors import AuthorityError, invalid, unsupported
from .model import (
    AuthorityCodec,
    AuthorityEnvelope,
    AuthorityHandle,
    AuthorityReference,
    CodecContext,
    CodecSet,
    PutResult,
)
from .store import ObjectStore


@dataclass(frozen=True, slots=True)
class ResolvedAuthority:
    handle: AuthorityHandle
    value: object
    envelope: AuthorityEnvelope


class AuthorityRepository:
    def __init__(self, store: ObjectStore, codec_sets: Iterable[CodecSet]) -> None:
        self._store = store
        codecs: dict[str, AuthorityCodec[object]] = {}
        for codec_set in tuple(codec_sets):
            for codec in codec_set.codecs:
                if codec.object_kind in codecs:
                    raise invalid(
                        "AUTHORITY.DUPLICATE_CODEC_KIND",
                        f"duplicate injected codec for {codec.object_kind!r}",
                    )
                codecs[codec.object_kind] = codec
        self._codecs = codecs

    def publish(self, codec: AuthorityCodec[object], value: object) -> PutResult:
        selected = self._codecs.get(codec.object_kind)
        if selected is not codec:
            raise unsupported(
                "AUTHORITY.UNINJECTED_CODEC",
                f"codec for {codec.object_kind!r} was not injected",
            )
        context = _RepositoryContext(self, {})
        payload = codec.encode(value)
        semantic_id = codec.semantic_id(value, context)
        dependencies = codec.direct_dependencies(value)
        envelope = AuthorityEnvelope(
            object_kind=codec.object_kind,
            semantic_id=semantic_id,
            direct_dependencies=dependencies,
            payload_contract=codec.payload_contract,
            payload=payload,
        )
        self._validate_codec_dependencies(codec, envelope.direct_dependencies)
        handle = envelope.handle
        for dependency in envelope.direct_dependencies:
            if dependency == handle.reference:
                raise invalid(
                    "AUTHORITY.DEPENDENCY_CYCLE", "object directly depends on itself"
                )
            self._resolve_graph((dependency,))
        encoded = encode_envelope(envelope)
        result = self._store.put_if_absent(handle, encoded)
        resolved = self.resolve(handle)
        if resolved.envelope != envelope:
            raise invalid(
                "AUTHORITY.PUBLICATION_CONTRADICTION",
                "published object does not reproduce the submitted envelope",
            )
        return result

    def resolve(self, handle: AuthorityHandle) -> ResolvedAuthority:
        return self._resolve_graph((handle.reference,))[handle.reference]

    def resolve_reference(self, reference: AuthorityReference) -> ResolvedAuthority:
        return self._resolve_graph((reference,))[reference]

    def transitive_dependencies(
        self, roots: Iterable[AuthorityReference]
    ) -> tuple[AuthorityReference, ...]:
        return tuple(sorted(self._resolve_graph(tuple(set(roots)))))

    def _resolve_graph(
        self, roots: Iterable[AuthorityReference]
    ) -> dict[AuthorityReference, ResolvedAuthority]:
        ordered_roots = tuple(sorted(set(roots)))
        resolved: dict[AuthorityReference, ResolvedAuthority] = {}
        pending: dict[
            AuthorityReference, tuple[AuthorityEnvelope, AuthorityCodec[object]]
        ] = {}
        active: set[AuthorityReference] = set()
        stack = [(reference, False) for reference in reversed(ordered_roots)]
        while stack:
            reference, exiting = stack.pop()
            if exiting:
                envelope, codec = pending[reference]
                context = _RepositoryContext(self, resolved)
                try:
                    value = codec.decode(envelope.payload, context)
                    recomputed = codec.semantic_id(value, context)
                    dependencies = codec.direct_dependencies(value)
                except AuthorityError:
                    raise
                except (KeyError, TypeError, ValueError) as error:
                    raise invalid("AUTHORITY.OWNER_INVALID", str(error)) from error
                if recomputed != envelope.semantic_id:
                    raise invalid(
                        "AUTHORITY.IDENTITY_MISMATCH",
                        "owner-recomputed semantic identity differs from the envelope",
                    )
                if dependencies != envelope.direct_dependencies:
                    raise invalid(
                        "AUTHORITY.DEPENDENCY_MISMATCH",
                        "owner-extracted dependencies differ from the envelope",
                    )
                resolved[reference] = ResolvedAuthority(
                    envelope.handle, value, envelope
                )
                active.remove(reference)
                continue
            if reference in resolved:
                continue
            if reference in active:
                raise invalid(
                    "AUTHORITY.DEPENDENCY_CYCLE",
                    f"dependency cycle includes {reference!r}",
                )
            envelope, codec = self._load_node(reference)
            pending[reference] = (envelope, codec)
            active.add(reference)
            stack.append((reference, True))
            stack.extend(
                (dependency, False)
                for dependency in reversed(envelope.direct_dependencies)
            )
        return resolved

    def _load_node(
        self, reference: AuthorityReference
    ) -> tuple[AuthorityEnvelope, AuthorityCodec[object]]:
        handle = AuthorityHandle(reference.object_kind, reference.semantic_id)
        envelope = decode_envelope(self._store.get(handle))
        if envelope.handle != handle:
            raise invalid(
                "AUTHORITY.HANDLE_MISMATCH",
                "stored envelope does not agree with the requested handle",
            )
        codec = self._codecs.get(envelope.object_kind)
        if codec is None:
            raise unsupported(
                "AUTHORITY.UNSUPPORTED_OBJECT_KIND",
                f"no codec was injected for {envelope.object_kind!r}",
            )
        if envelope.payload_contract != codec.payload_contract:
            raise unsupported(
                "AUTHORITY.UNSUPPORTED_PAYLOAD_CONTRACT",
                f"unsupported payload contract {envelope.payload_contract!r}",
            )
        self._validate_codec_dependencies(codec, envelope.direct_dependencies)
        return envelope, codec

    @staticmethod
    def _validate_codec_dependencies(
        codec: AuthorityCodec[object],
        dependencies: tuple[AuthorityReference, ...],
    ) -> None:
        if dependencies != tuple(sorted(dependencies)) or len(set(dependencies)) != len(
            dependencies
        ):
            raise invalid(
                "AUTHORITY.INVALID_OWNER_DEPENDENCIES",
                "owner dependencies must be sorted and unique",
            )
        disallowed = [
            item.object_kind
            for item in dependencies
            if item.object_kind not in codec.allowed_dependency_kinds
        ]
        if disallowed:
            raise invalid(
                "AUTHORITY.DISALLOWED_DEPENDENCY_KIND",
                f"{codec.object_kind!r} does not admit {disallowed[0]!r}",
            )

    def _verify_all_stored(self) -> None:
        rows = getattr(self._store, "_all_rows", None)
        if rows is None:
            raise unsupported(
                "STORE.COMPLETE_VERIFICATION_UNSUPPORTED",
                "store does not expose internal complete verification",
            )
        for storage_key, encoded in rows():
            envelope = decode_envelope(encoded)
            if encode_storage_key(envelope.handle) != storage_key:
                raise invalid(
                    "STORE.HANDLE_KEY_MISMATCH",
                    "stored primary key differs from its canonical typed handle",
                )
            self.resolve(envelope.handle)


class _RepositoryContext(CodecContext):
    def __init__(
        self,
        repository: AuthorityRepository,
        resolved: dict[AuthorityReference, ResolvedAuthority],
    ) -> None:
        self._repository = repository
        self._resolved = resolved

    def resolve(self, reference: AuthorityReference) -> object:
        resolved = self._resolved.get(reference)
        if resolved is None:
            resolved = self._repository.resolve_reference(reference)
        return resolved.value

    def transitive_dependencies(
        self, roots: Iterable[AuthorityReference]
    ) -> tuple[AuthorityReference, ...]:
        return self._repository.transitive_dependencies(roots)


__all__ = ("AuthorityRepository", "ResolvedAuthority")
