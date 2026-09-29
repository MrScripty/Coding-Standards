"""Canonical fact records preserve bindings independently of agent presentation."""
from __future__ import annotations

import ast
from dataclasses import replace
from importlib.util import resolve_name
import json
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

from tools.standards_analysis.standards_analysis import load_router_projection
from tools.standards_engine.standards_engine import AgentToolFacade, StandardsEngine
from tools.standards_engine.standards_engine import agent_navigation, supporting
from tools.standards_engine.standards_engine._generated_contract import SnapshotHandle
from tools.standards_metadata.standards_metadata import FrozenContentSource, content_digest

ROOT = Path(__file__).resolve().parents[3]


def _presentation_imports(source: str) -> tuple[str, ...]:
    """Guard this material owner's static dependencies, not a general import graph.

    Resolve relative spellings with Python's owner so aliases do not conceal a
    navigation dependency. Dynamic loading and attribute access are out of scope.
    """
    package = supporting.__package__
    forbidden = {'agent_navigation', 'context_projection'}
    forbidden.update(f'{package}.{name}' for name in tuple(forbidden))
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names = [item.name for item in node.names]
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            if node.level:
                module = resolve_name('.' * node.level + module, package)
            names = [module, *(f'{module}.{item.name}' for item in node.names)]
        else:
            continue
        found.update(name for name in names if any(
            name == boundary or name.startswith(boundary + '.')
            for boundary in forbidden
        ))
    return tuple(sorted(found))


class FactOwnershipImportGuardTest(unittest.TestCase):
    def test_guard_rejects_equivalent_static_navigation_dependencies(self):
        package = supporting.__package__
        for name in ('agent_navigation', 'context_projection'):
            spellings = (
                f'import {name}',
                f'import {name} as view',
                f'import json, {package}.{name} as view',
                f'from {name} import route as select',
                f'from {package}.{name} import route',
                f'from .{name} import route as select',
                f'from .{name} import *',
                f'from . import {name}',
                f'from . import {name} as view',
                f'from {package} import {name} as view',
                f'from ..standards_engine import {name} as view',
                f'from ..standards_engine.{name} import route',
            )
            for statement in spellings:
                with self.subTest(statement=statement):
                    self.assertTrue(_presentation_imports(statement))

    def test_guard_allows_unrelated_modules_aliases_and_non_import_text(self):
        source = """import json as agent_navigation
from tools.standards_analysis.standards_analysis import RouterProjection
from . import authoring as context_projection
from .authoring import ProposalRevision
from unrelated import agent_navigation
from unrelated.context_projection import value
from tools.standards_engine.standards_engine import agent_navigation_helpers
from .context_projection_helpers import value
text = 'import agent_navigation'
# from . import context_projection
"""
        self.assertEqual(_presentation_imports(source), ())


class FactMaterialOwnershipTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='fact-material-owner-')
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.engine = StandardsEngine.open_repository(ROOT,purpose='authoring',
                          store_path=Path(cls.temporary.name)/'snapshots.sqlite3')
        cls.addClassCleanup(cls.engine.close)
        cls.facade = AgentToolFacade(cls.engine,AgentToolFacade.load_interface(ROOT))
        created = cls.facade.create_snapshot({'kind':'create-snapshot'})
        assert created['kind']=='create-snapshot-result',created
        cls.snapshot = created['snapshot']['snapshot']
        cls.compiled = cls.engine._compiled_snapshot(cls.engine._snapshot_id(SnapshotHandle.from_value(cls.snapshot)))

    def materials(self, *, router=None, source=None):
        c = self.compiled
        return supporting.build_materials(source or c.source,c.corpus,c.policy_impact,
                                          router or c.router,c.supporting)

    def test_exact_record_serialization_preserves_existing_material_identity(self):
        c = self.compiled
        raw = tomllib.loads(c.source.read_bytes('evaluation/standards-effectiveness/router-projection.toml').decode())
        fields = ('id','semantic_revision','type','nullable','values','aliases','meaning','prompt')
        facts = [{name: sorted(fact[name]) if name in ('values','aliases') else fact[name]
                  for name in fields} for fact in sorted(raw['facts'],key=lambda f:f['id'])]
        self.assertEqual(json.dumps(c.router.fact_definitions()),json.dumps(facts))
        module = c.corpus.resolve_module('router')
        expected = {'id':module.module_id,'role':module.role,'level':module.level,
                    'content':c.source.read_bytes(module.path).decode(),
                    'policy_units':[u.as_declaration() for u in c.corpus.policy_unit_corpus.for_module('router')],
                    'routing':{'facts':facts,'base_modules':list(c.router.base_modules),
                               'rules':[{'id':rule.id,'target':rule.target,'when':rule.program.as_expression()}
                                        for rule in c.router.rules]}}
        self.assertEqual(c.materials['router'].binding,content_digest(expected))
        self.assertEqual(replace(c,materials=self.materials()).semantic_signature(),c.semantic_signature())

    def test_presentation_reordering_and_mutation_cannot_redefine_binding(self):
        canonical = self.compiled.router.fact_definitions()
        original = agent_navigation.routing_facts
        def presented(engine, call):
            result = original(engine,call)
            value = result.as_contract()
            value['facts'].reverse()
            value['facts'][0]['prompt'] = 'Presentation-only prompt.'
            value['facts'][0]['aliases'].append('presentation.alias')
            return type(result).from_value(value)
        with patch.object(agent_navigation,'routing_facts',side_effect=presented):
            response = self.facade.routing_facts({'snapshot':self.snapshot})
            self.assertNotEqual(response['facts'],canonical)
            rebound = self.materials()
        self.assertEqual(rebound,self.compiled.materials)
        self.assertEqual(self.compiled.router.fact_definitions(),canonical)
        self.assertEqual(replace(self.compiled,materials=rebound).semantic_signature(),self.compiled.semantic_signature())

    def test_real_fact_change_still_changes_router_binding_not_unrelated_material(self):
        c = self.compiled
        path = 'evaluation/standards-effectiveness/router-projection.toml'
        first = c.router.facts[0]
        original = c.source.read_bytes(path)
        changed = original.replace(first.prompt.encode(),(first.prompt+' Revised canonical prompt.').encode(),1)
        self.assertNotEqual(original,changed)
        source = FrozenContentSource([(name,changed if name==path else data) for name,data in c.source.files])
        router = load_router_projection(source,c.corpus.module_corpus)
        rebound = self.materials(router=router,source=source)
        self.assertEqual(rebound['router'].content,c.materials['router'].content)
        self.assertNotEqual(rebound['router'].binding,c.materials['router'].binding)
        self.assertEqual({k:v for k,v in rebound.items() if k!='router'},
                         {k:v for k,v in c.materials.items() if k!='router'})

    def test_navigation_and_domain_consumers_use_the_canonical_owner(self):
        self.assertFalse(hasattr(agent_navigation,'fact_definitions'))
        # This bound dependency regression enforces the specific review finding,
        # not a generic package-layout convention or a file-size threshold.
        self.assertEqual(_presentation_imports(Path(supporting.__file__).read_text()), ())
        canonical = self.compiled.router.fact_definitions()
        facts = self.facade.routing_facts({'snapshot':self.snapshot})
        self.assertEqual(facts['facts'],canonical)
        read = self.facade.read({'snapshot':self.snapshot,'target':'router','detail':'full','include_routing':True})
        self.assertEqual(read['routing']['facts'],canonical)
        route = self.facade.route({'snapshot':self.snapshot,'facts':{}})
        self.assertEqual([q['fact'] for q in route['unresolved_questions']],canonical)
