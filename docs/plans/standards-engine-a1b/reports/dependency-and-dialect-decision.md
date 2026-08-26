# A1b Dependency And Dialect Decision

**Status:** Proposed planning evidence

**Planning comparison base:** commit
`c4408363752b10060f631247f3e2f1fa26eae003`, tree
`84477150bd368a168dd04da3770de55c23bbb817`

**Resolution observed:** 2026-08-26

## Requirement

A1b needs one executable owner for the standard behavior used by its canonical
contract. The owner must:

- implement JSON Schema Draft 2020-12 instance validation;
- support the A1b schema and local-reference profile;
- expose errors that can be adapted to stable project diagnostics;
- run on Linux x86-64 with glibc 2.17 or newer under CPython 3.11 and 3.12;
- permit repository and installed-tool use under accepted terms;
- avoid runtime network retrieval; and
- let generated models remain representations rather than validators.

A1b does not need to implement JSON, implement JSON Schema, or re-certify a
third-party Draft implementation.

## Candidate Comparison

| Candidate | Draft owner | Project maintenance | Result |
| --- | --- | --- | --- |
| Current local validator plus generated decoder | Two incomplete repository interpreters | Permanent ownership of standardized semantics | Rejected |
| Code-first Python model library | Library model semantics plus a remaining schema projection | Two authorities still require reconciliation | Rejected |
| Scattered `jsonschema` calls | Dependency | Reference, profile, and diagnostic rules duplicated | Rejected |
| `standards_contracts` over `jsonschema` and `referencing` | Dependency | One adapter, projection compiler, and diagnostic contract | Selected |

## Selected Runtime

`jsonschema.Draft202012Validator` from `jsonschema==4.26.0` is the sole
Draft 2020-12 validator. `referencing==0.37.0` is a direct dependency because
`standards_contracts` constructs its immutable resource registry. The
repository does not override validator keywords, type checking, or equality.

The A1b lock uses pip requirements syntax with exact `==` versions and
`--hash` entries. Installation and verification use `--require-hashes`.
Package manifests declare the two direct dependencies; the lock records this
complete resolution:

| Package | Version | Role | License expression |
| --- | --- | --- | --- |
| `jsonschema` | 4.26.0 | Draft validator | MIT |
| `referencing` | 0.37.0 | Immutable resource registry | MIT |
| `attrs` | 26.1.0 | Transitive data-model dependency | MIT |
| `jsonschema-specifications` | 2025.9.1 | Transitive specification resources | MIT |
| `rpds-py` | 2026.6.3 | Transitive persistent collections | MIT |
| `typing-extensions` | 4.16.0 | Transitive typing compatibility | PSF-2.0 |

## Artifact Resolution

The resolver selected these package-index wheel artifacts and SHA-256 hashes:

| Exact artifact filename | SHA-256 |
| --- | --- |
| `attrs-26.1.0-py3-none-any.whl` | `c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309` |
| `jsonschema-4.26.0-py3-none-any.whl` | `d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce` |
| `jsonschema_specifications-2025.9.1-py3-none-any.whl` | `98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe` |
| `referencing-0.37.0-py3-none-any.whl` | `381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231` |
| `rpds_py-2026.6.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | `9c1255b302953c86a486b81d330d5ee1d5bd937691ce271b6be0ef0e299eaab7` |
| `rpds_py-2026.6.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | `ecabd69db66de867690f9797f2f8fa27ba501bbc24540cbdbdc649cd15888ba6` |
| `typing_extensions-4.16.0-py3-none-any.whl` | `481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8` |

Milestone 0 mechanically produces the lock from this reviewed resolution and
must reproduce these exact names, versions, target artifacts, and hashes.
Resolution drift is a re-plan trigger rather than authority to silently update
the planning record.

`rpds-py` is native. The two exact selected wheels require Linux x86-64 with
glibc 2.17 or newer and cover only CPython 3.11 and 3.12. A source build, musl,
another architecture, or another Python version is not part of this decision
and requires a new supported-target review.

Every Engine Module manifest changes `requires-python` from the former
open-ended `>=3.11` to `>=3.11,<3.13`. The exact direct internal dependency
graph is:

| Module | Direct internal requirements | Direct external requirements |
| --- | --- | --- |
| `repository-graph-engine` | none | none |
| `standards-applicability` | none | none |
| `standards-identity` | none | none |
| `standards-contracts` | none | `jsonschema==4.26.0`, `referencing==0.37.0` |
| `standards-metadata` | `standards-identity` | none |
| `standards-authority` | `standards-identity` | none |
| `standards-policy-impact` | `repository-graph-engine`, `standards-applicability`, `standards-metadata` | none |
| `standards-graph` | `repository-graph-engine`, `standards-metadata`, `standards-policy-impact` | none |
| `standards-analysis` | `repository-graph-engine`, `standards-applicability`, `standards-identity`, `standards-metadata`, `standards-policy-impact` | none |
| `standards-engine` | `repository-graph-engine`, `standards-applicability`, `standards-analysis`, `standards-authority`, `standards-contracts`, `standards-graph`, `standards-metadata`, `standards-policy-impact` | none |
| `standards-verifier` | `repository-graph-engine`, `standards-applicability`, `standards-analysis`, `standards-contracts`, `standards-graph`, `standards-metadata`, `standards-policy-impact` | none |

The cutover gate derives production direct imports and requires exact equality
with this manifest graph. A transitive import does not satisfy a missing direct
declaration, and an unused declaration is invalid. Test-only imports are suite
inputs, not production requirements. Discovering a required edge outside this
closed table is a re-plan trigger.

This internal source-tree closure is A1B-A6I and remains pending until the
atomic cutover. It is deliberately separate from A1B-A6: Milestone 0 proves the
external lock, artifacts, target environments, security disposition, and
isolated dependency imports without claiming that not-yet-updated internal
manifests already pass.

The accepted install operation is exactly:

```sh
python -m pip install \
  --require-hashes \
  --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

The lock lists every package above explicitly. The two `rpds-py` entries use
mutually exclusive `python_version == "3.11"` and `python_version == "3.12"`
markers and their corresponding single admitted wheel hash. Universal entries
carry only the reviewed universal-wheel hash. A resolver selecting an sdist,
another wheel, another transitive version, or an unlisted dependency fails.

The internal Modules execute from the repository source tree and are not
published as separate distributions in A1b. After the external install, each
admitted Python version performs the public import smoke from outside the
checkout with safe-path mode and the exact checkout root as its sole
`PYTHONPATH`:

```sh
cd "$isolated_directory"
PYTHONPATH="$reviewed_checkout_root" python -P -c '
from tools.graph_engine import graph_engine
from tools.standards_applicability import standards_applicability
from tools.standards_identity import standards_identity
from tools.standards_contracts import standards_contracts
from tools.standards_metadata import standards_metadata
from tools.standards_authority import standards_authority
from tools.standards_policy_impact import standards_policy_impact
from tools.standards_graph import standards_graph
from tools.standards_analysis import standards_analysis
from tools.standards_engine import standards_engine
from tools.standards_verifier import standards_verifier
'
```

This proves the repository's actual local execution boundary without silently
selecting a build backend. A future separately installed or published internal
distribution requires its own build, dependency, release, and installation
decision.

## Dialect And Projection Profile

The public schema declares
`https://json-schema.org/draft/2020-12/schema`. The exact required vocabulary
closure and unused selected vocabularies are recorded in the
[schema/domain audit](schema-and-domain-contract-audit.md). No custom
vocabulary or format-assertion vocabulary is enabled.

The current operation-reachable projection surface is:

```text
$schema, $id, $ref, $defs,
title, description, default,
type, const, enum, oneOf,
required, properties, additionalProperties,
items, minItems, uniqueItems,
minLength, pattern, minimum
```

This list limits what A1b can project into generated Python and agent-tool
representations. It is not a local validation subset. The selected validator
continues to own validation.

Only same-resource `#/$defs/...` references are admitted. Runtime retrieval,
remote resources, custom vocabularies, format assertion, keyword overrides,
and dynamic references are excluded. Patterns are limited to the audited
ASCII-compatible projection profile. A newly reachable unsupported projection
construct blocks compilation and triggers re-planning.

The v11 schema removes every `x-standards-engine-*` annotation. A separate
closed interface contract owns operation roots and capability selection;
domain Modules own identity, invariants, authorization, transitions, and
policy behavior.

## Evidence Boundary

Upstream `jsonschema` owns Draft conformance. A1b neither copies nor runs the
complete official JSON Schema Test Suite and makes no independent claim that it
has re-certified Draft 2020-12.

Repository acceptance instead proves:

- the exact dependency and `Draft202012Validator` class are selected;
- `check_schema` accepts the canonical schema;
- the registry contains only declared immutable local resources and has no
  retrieval path;
- known A1 Boolean/integer, Unicode, `pattern`, and `uniqueItems` cases pass
  through the production adapter;
- dependency errors are converted to stable project diagnostics;
- public operation closure and generated projections are complete; and
- unsupported projection constructs reject at compilation.

Generated freshness, adapter behavior, projection completeness, domain
invariants, and facade integration are separate claims. Agreement between two
project entry points is not presented as independent Draft conformance.

## Licensing And Provenance

No third-party source, wheel, or test corpus is copied into this repository.
The lock and provenance report record installed dependencies only. Current
repository outputs do not bundle those distributions; any future bundled
release requires a new Release and Licensing disposition.

The selected wheel license-file SHA-256 values are:

| Package | License file | SHA-256 |
| --- | --- | --- |
| `attrs` | `LICENSE` | `882115c95dfc2af1eeb6714f8ec6d5cbcabf667caff8729f42420da63f714e9f` |
| `jsonschema` | `COPYING` | `4f92a015a13c4d1a040bef018aa13430b4f1bc73b41b16bb846c346766de7439` |
| `jsonschema-specifications` | `COPYING` | `42dcd63495f87b4eb7c7757afa379bb55a53f94afd7a5f657d9adf57236e515c` |
| `referencing` | `COPYING` | `42dcd63495f87b4eb7c7757afa379bb55a53f94afd7a5f657d9adf57236e515c` |
| `rpds-py` | `LICENSE` | `314e4e91be3baa93c0fb4bccc9e4e97cd643eb839b065af921782c2175fe9909` |
| `typing-extensions` | `LICENSE` | `3b2f81fe21d181c499c59a256c8e1968455d6689d269aa85373bfb6af41da3bf` |

The exact release pages and wheel metadata identify these authorities:

| Package | Exact release authority | Upstream source | Copyright authority |
| --- | --- | --- | --- |
| `attrs==26.1.0` | [PyPI release](https://pypi.org/project/attrs/26.1.0/) | [python-attrs/attrs](https://github.com/python-attrs/attrs) | 2015 Hynek Schlawack and attrs contributors |
| `jsonschema==4.26.0` | [PyPI release](https://pypi.org/project/jsonschema/4.26.0/) | [python-jsonschema/jsonschema](https://github.com/python-jsonschema/jsonschema) | 2013 Julian Berman |
| `jsonschema-specifications==2025.9.1` | [PyPI release](https://pypi.org/project/jsonschema-specifications/2025.9.1/) | [python-jsonschema/jsonschema-specifications](https://github.com/python-jsonschema/jsonschema-specifications) | 2022 Julian Berman |
| `referencing==0.37.0` | [PyPI release](https://pypi.org/project/referencing/0.37.0/) | [python-jsonschema/referencing](https://github.com/python-jsonschema/referencing) | 2022 Julian Berman |
| `rpds-py==2026.6.3` | [PyPI release](https://pypi.org/project/rpds-py/2026.6.3/) | [crate-py/rpds](https://github.com/crate-py/rpds) | 2023 Julian Berman |
| `typing-extensions==4.16.0` | [PyPI release](https://pypi.org/project/typing-extensions/4.16.0/) | [python/typing_extensions](https://github.com/python/typing_extensions) | Python Software Foundation and historical licensors named by PSF-2.0 |

The exact wheel filenames and hashes above are the selected distribution
artifacts. Their embedded `METADATA` records the package name, version,
project URLs, `Requires-Python`, license expression, and license-file path.
Their embedded license bytes produce the recorded license hashes.

**Compatibility decision:** MIT and PSF-2.0 permit the planned installation,
import, internal execution, modification, and redistribution subject to their
notice and license conditions. A1b installs the wheels as dependencies and
does not copy or bundle their source or binary contents into a repository
artifact, so this repository change requires no new distributed notice file.
Installed wheels retain their own metadata and license files. Any future
bundled executable, vendored source, copied wheel, or redistributed dependency
closure must include the applicable notices/license texts and receive a new
Licensing and Release review.

A missing license file, changed copyright authority, incompatible term, changed
artifact hash, or new redistribution behavior blocks dependency acceptance.

## Security And Updates

OSV package-version queries on 2026-08-26 returned no known vulnerabilities for
the exact six-package resolution. This is planning evidence, not a permanent
claim. Milestone 0 repeats the accepted dependency audit and binds its result.

Updating any package requires rerunning resolution, hashes, target support,
provenance, license, vulnerability, adapter regressions, generated projection,
and public integration evidence.

## Sources

- [`jsonschema` project](https://github.com/python-jsonschema/jsonschema)
- [`jsonschema` 4.26.0 package metadata](https://pypi.org/project/jsonschema/4.26.0/)
- [`referencing` project](https://github.com/python-jsonschema/referencing)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)

## Decision

The dependency-backed contract compiler is selected. Implementation remains
unavailable until the replacement A1b plan and ADR receive independent
exact-tree admission.
