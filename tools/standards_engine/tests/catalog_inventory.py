"""Read-only catalog accounting; raw catalog bytes are not model tokens.

Run as a module. With --catalog, accept a tool array, tools/list result, or its
JSON-RPC envelope. Otherwise inspect the installed purpose and output delivery without opening
an Engine store. No host configuration, tool invocation or model turn is made.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _encoded(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True).encode('utf-8')


def measure_catalog(value: object) -> dict:
    if isinstance(value, dict):
        value = value.get('result', value)
        value = value.get('tools') if isinstance(value, dict) else None
    if not isinstance(value, list):
        raise ValueError('Supply a tool array, tools/list result or its JSON-RPC envelope.')
    rows, names = [], set()
    for tool in value:
        if not isinstance(tool, dict) or not isinstance(tool.get('name'), str):
            raise ValueError('Every catalog entry must be a named tool object.')
        name = tool['name']
        description = tool.get('description', '')
        if name in names or not isinstance(description, str) or not isinstance(tool.get('inputSchema'), dict):
            raise ValueError('Tool names must be unique, descriptions text, and inputSchema an object.')
        if 'outputSchema' in tool and not isinstance(tool['outputSchema'], dict):
            raise ValueError('An outputSchema must be an object when present.')
        names.add(name)
        rows.append({'name': name, 'description_characters': len(description),
                     'description_utf8_bytes': len(description.encode('utf-8')),
                     'input_schema_json_bytes': len(_encoded(tool['inputSchema'])),
                     'output_schema_json_bytes': len(_encoded(tool['outputSchema'])) if 'outputSchema' in tool else 0,
                     'metadata_json_bytes': len(_encoded(tool['_meta'])) if '_meta' in tool else 0})
    encoded = _encoded(value)
    return {'tool_count': len(rows),
            **{key: sum(row[key] for row in rows) for key in
               ('description_characters', 'description_utf8_bytes', 'input_schema_json_bytes', 'output_schema_json_bytes', 'metadata_json_bytes')},
            'serialized_catalog_json_bytes': len(encoded),
            'measurement_sha256': hashlib.sha256(encoded).hexdigest(),
            'tools': rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, help='Measure the supplied raw catalog rather than an installation.')
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--purpose', choices=('application', 'authoring'), default='application')
    parser.add_argument('--output-schemas', choices=('eager', 'on-demand'), default='eager')
    parser.add_argument('--advanced', action='store_true')
    args = parser.parse_args()
    try:
        if args.catalog:
            report = measure_catalog(json.loads(args.catalog.read_text(encoding='utf-8')))
            report['source'] = {'kind': 'provided-catalog'}
        else:
            from tools.standards_engine.standards_engine.tools import AgentToolFacade
            from tools.standards_engine.standards_engine.mcp_catalog import tool_catalog
            interface = AgentToolFacade.load_interface(args.repo_root)
            report = measure_catalog(tool_catalog(interface, purpose=args.purpose, advanced=args.advanced, output_schemas=args.output_schemas))
            report['source'] = {'kind': 'installed', 'interface_version': interface.interface.interface_schema_version,
                                'purpose': args.purpose, 'schema_mode': 'native', 'output_schemas': args.output_schemas, 'advanced': args.advanced}
    except (OSError, ValueError) as error:
        parser.exit(2, f'Catalog inventory unavailable: {error}\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
