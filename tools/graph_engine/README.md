# Repository Graph Engine

`tools/graph_engine/` owns repository-neutral directed-edge mechanics. It has
no dependency on standards policy, suite configuration, migration lifecycle,
planning, or Bash-checker retirement.

The engine builds one immutable index from explicitly registered sources. A
source declares canonical nodes, aliases, stable edges, named groups, and
provenance. Domain adapters may validate opaque metadata, but the engine does
not interpret it. Derived incoming, outgoing, incident, edge-to-group, and
group-to-edge indexes are never declaration authority.

Run tests:

```bash
python3 -m unittest discover -s tools/graph_engine/tests
```

Query a registered repository graph:

```bash
python3 tools/query_edges.py --node workflow.planning
python3 tools/query_edges.py \
  --node workflows/planning.md --direction outgoing --group policy-impact
python3 tools/query_edges.py --edge policy.planning.router
python3 tools/query_edges.py \
  --node workflow.planning --group policy-impact \
  --direction outgoing --traverse
python3 tools/query_edges.py --list-groups
```

The repository composition registers reviewed manifests and named deterministic
providers, then injects them into this neutral engine. Queries do not scan for
declarations or infer edges from text, links, paths, ownership, or another
graph. Transitive traversal is rejected unless the selected group explicitly
permits it.
