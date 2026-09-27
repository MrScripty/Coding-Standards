"""Snapshot-bound relationship group discovery and invalid-group recovery.

The graph is the vocabulary authority; the application view supplies its permitted
subgraph. This module owns only whole-record presentation and its explicit bounds.
"""
from __future__ import annotations

import json

from . import _generated_contract as c

GROUP_PAGE_BYTES = 16 * 1024
GROUP_PAGE_DEFAULT_ITEMS = 8


def _reject(engine, code: str, outcome: str, message: str):
    from .context_projection import Purpose, application_rejection
    if engine.purpose is Purpose.APPLICATION:
        public = 'APPLICATION.INPUT_INVALID' if outcome == 'invalid' else 'APPLICATION.RESULT_LIMIT'
        return application_rejection(public, outcome)
    return engine._reject(code, outcome, message)


def validate_selection(engine, values: dict):
    if values.get('offset', 0) and 'snapshot' not in values:
        return _reject(engine, 'GROUPS.SELECTION', 'invalid',
                       'A nonzero offset requires the exact returned snapshot.')
    return None


def group_page(engine, snapshot, graph, *, offset: int = 0, limit: int = GROUP_PAGE_DEFAULT_ITEMS):
    """Return registered groups, including groups with no edges for a target.

    Every item preserves the registered purpose and traversal policy. Neither
    source locators, validators nor graph extension metadata enter this view.
    """
    offset, limit = int(offset), int(limit)
    groups = sorted(graph.groups.values(), key=lambda group: group.id)
    if offset > len(groups):
        return _reject(engine, 'GROUPS.SELECTION', 'invalid',
                       'The offset exceeds the registered relationship groups.')
    snapshot_id = engine._snapshot_id(snapshot)
    engine._snapshots.snapshot(snapshot_id)
    value = {
        'kind': 'relationship-groups-result', 'purpose': engine.purpose.value,
        'snapshot': snapshot.as_contract(), 'offset': offset, 'total': len(groups),
        'items': [],
    }

    def continuation():
        end = offset + len(value['items'])
        if end < len(groups):
            value['next'] = {'snapshot': snapshot.as_contract(), 'offset': end, 'limit': limit}
        else:
            value.pop('next', None)

    for group in groups[offset:offset + limit]:
        value['items'].append({
            'id': group.id, 'description': group.purpose,
            'traversal_directions': sorted(direction.value for direction in group.traversal.directions),
            'transitive': group.traversal.transitive,
        })
        continuation()
        if len(json.dumps(value).encode('utf-8')) > GROUP_PAGE_BYTES:
            value['items'].pop()
            if not value['items']:
                return _reject(engine, 'GROUPS.RESULT_LIMIT', 'unsupported',
                               'One whole group record exceeds the 16 KiB discovery limit.')
            break
    continuation()
    if len(json.dumps(value).encode('utf-8')) > GROUP_PAGE_BYTES:
        return _reject(engine, 'GROUPS.RESULT_LIMIT', 'unsupported',
                       'The group discovery envelope exceeds its 16 KiB limit.')
    engine._snapshots.snapshot(snapshot_id)
    return c.RelationshipGroupsResult.from_value(value)


def relationship_groups(engine, call):
    values = call.as_contract()
    rejected = validate_selection(engine, values)
    if rejected is not None:
        return rejected
    try:
        snapshot = values.get('snapshot')
        if snapshot is None:
            captured = engine.create_snapshot(c.CreateSnapshotCall(kind='create-snapshot'))
            if isinstance(captured, c.RejectedResult):
                return captured
            snapshot = captured.as_contract()['snapshot']['snapshot']
        handle = c.SnapshotHandle.from_value(snapshot)
        compiled = engine._compiled_snapshot(engine._snapshot_id(handle))
        return group_page(engine, handle, compiled.graph,
                          offset=values.get('offset', 0), limit=values.get('limit', GROUP_PAGE_DEFAULT_ITEMS))
    except engine._domain_errors() as error:
        return engine._domain_rejection(error)


def unknown_group_result(engine, snapshot, graph):
    """Keep rejection semantics while offering the same bounded discovery page."""
    from .context_projection import Purpose, application_rejection
    page = group_page(engine, snapshot, graph)
    if not isinstance(page, c.RelationshipGroupsResult):
        return page
    if engine.purpose is Purpose.APPLICATION:
        result = application_rejection('APPLICATION.UNKNOWN_GROUP', 'invalid')
    else:
        result = engine._reject('GRAPH.UNKNOWN_GROUP', 'invalid',
                                'Choose a registered group from relationship_groups; no group was inferred.')
    value = result.as_contract()
    value['relationship_groups'] = page.as_contract()
    return type(result).from_value(value)
