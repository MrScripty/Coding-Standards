"""Bounded, value-free explanations of already rejected validator input.

jsonschema remains the validity oracle. A proven disjoint string discriminator
can filter irrelevant error causes; it never accepts a branch or an instance.
Literal values and arbitrary object keys are not copied into public feedback.
"""
from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import asdict
import json

from jsonschema.exceptions import ValidationError

from .errors import InputIssue
from .union_selection import StringDiscriminant

MAX_INPUT_ISSUES = 8
MAX_FEEDBACK_BYTES = 8 * 1024
MAX_DIAGNOSTIC_ERRORS = 128
MAX_POINTER_CHARS = 512
MAX_MESSAGE_CHARS = 384


def _pointer(parts: Iterable[str | int]) -> str:
    return ''.join('/' + str(p).replace('~', '~0').replace('/', '~1') for p in parts)


def _location(error: ValidationError, missing_field: str | None = None) -> tuple[str, bool]:
    path = tuple(error.absolute_schema_path)
    declared = {path[i + 1] for i, item in enumerate(path[:-1]) if item == 'properties'}
    parts = []
    exact = True
    for part in error.absolute_path:
        if isinstance(part, str) and part not in declared:
            parts.append('*')
            exact = False
        else:
            parts.append(part)
    if missing_field is not None:
        parts.append(missing_field)  # The name comes from required, not the instance.
    pointer = _pointer(parts)
    if len(pointer) > MAX_POINTER_CHARS:
        return '', False
    return pointer, exact


def _issues(error: ValidationError) -> Iterator[InputIssue]:
    keyword = str(error.validator or 'contract')
    constraint = error.validator_value
    if keyword == 'required' and isinstance(error.instance, Mapping):
        # One validator error may represent one of several missing required fields.
        # Emit the complete declared missing set, then deduplicate other errors.
        for name in constraint:
            if name not in error.instance:
                pointer, exact = _location(error, name)
                yield InputIssue(pointer, exact, keyword, 'Supply this required field.')
        return
    pointer, exact = _location(error)
    messages = {
        'additionalProperties': 'Remove fields not declared by this object.',
        'oneOf': 'Supply exactly one supported variant; discover its fields before retrying.',
        'enum': 'Use one of the values declared for this field.',
        'const': 'Use the exact value declared for this field.',
        'pattern': 'Use the string format declared for this field.',
        'uniqueItems': 'Supply distinct items in this array.',
    }
    message = messages.get(keyword, 'Satisfy the declared constraint for this field.')
    if keyword == 'type' and isinstance(constraint, str):
        message = f'Supply a value of type {constraint}.'
    elif keyword in {'minItems', 'maxItems', 'minLength', 'maxLength',
                     'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum',
                     'minProperties', 'maxProperties'}:
        message = f'Satisfy {keyword} = {constraint}.'
    yield InputIssue(pointer, exact, keyword[:64], message[:MAX_MESSAGE_CHARS])


def validation_feedback(
    errors: Iterable[ValidationError], selectors: Mapping[int, StringDiscriminant],
) -> tuple[tuple[InputIssue, ...], bool]:
    """Observe a bounded prefix of errors; keep ambiguous unions as one issue.

    The original complete first-error tree is retained separately by the runtime.
    `truncated` means more detail exists or the diagnostic work/size bound was hit.
    This is not a promise to enumerate every possible constraint violation.
    """
    pending = [iter(errors)]
    selected: list[InputIssue] = []
    seen: set[InputIssue] = set()
    visited = 0
    while pending:
        error = next(pending[-1], None)
        if error is None:
            pending.pop()
            continue
        visited += 1
        if visited > MAX_DIAGNOSTIC_ERRORS:
            return tuple(selected), True
        selector = selectors.get(id(error.schema)) if error.validator == 'oneOf' else None
        branch = selector.select(error.instance) if selector is not None else None
        if branch is not None and error.context:
            index = next(i for i, candidate in enumerate(error.validator_value) if candidate is branch)
            causes = [e for e in error.context if e.schema_path and e.schema_path[0] == index]
            if causes:
                pending.append(iter(causes))
                continue
        for issue in _issues(error):
            if issue in seen:
                continue
            seen.add(issue)
            candidate = [*selected, issue]
            if len(candidate) > MAX_INPUT_ISSUES or len(json.dumps(
                [asdict(item) for item in candidate], ensure_ascii=True,
            ).encode('utf-8')) > MAX_FEEDBACK_BYTES:
                return tuple(selected), True
            selected.append(issue)
    return tuple(selected), False
