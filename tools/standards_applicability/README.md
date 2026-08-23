# Standards Applicability

`standards_applicability` is the repository-neutral executable authority for
the bounded applicability language. It compiles one typed fact schema, compiles
many immutable programs against that schema, binds one immutable fact set per
request, and evaluates programs with exact three-valued outcomes.

```python
schema = compile_fact_schema(declaration)
program = schema.compile(expression)
facts = schema.bind(raw_facts)
result = program.evaluate(facts)
```

The Module uses only the Python standard library. It does not load repository
files, own public JSON shapes, generate questions, traverse graphs, or emit
consumer diagnostics. Adapters load authored data and translate
`ApplicabilityError` into their domain outcomes.
