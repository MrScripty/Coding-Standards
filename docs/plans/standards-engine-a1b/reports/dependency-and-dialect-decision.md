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
open-ended `>=3.11` to `>=3.11,<3.13` and declares one source-tree public import
root and repository entrypoints in this exact table:

```toml
[tool.standards-package]
schema-version = 1
public-import-root = "tools.example.example"
repository-entrypoints = []
```

| Module | Public import root | Repository entrypoints | Direct internal requirements | Direct external requirements |
| --- | --- | --- | --- | --- |
| `repository-graph-engine` | `tools.graph_engine.graph_engine` | none | none | none |
| `standards-applicability` | `tools.standards_applicability.standards_applicability` | none | none | none |
| `standards-identity` | `tools.standards_identity.standards_identity` | none | none | none |
| `standards-contracts` | `tools.standards_contracts.standards_contracts` | none | none | `jsonschema==4.26.0`, `referencing==0.37.0` |
| `standards-authority` | `tools.standards_authority.standards_authority` | none | `standards-identity` | none |
| `standards-metadata` | `tools.standards_metadata.standards_metadata` | none | `standards-authority`, `standards-identity` | none |
| `standards-policy-impact` | `tools.standards_policy_impact.standards_policy_impact` | none | `repository-graph-engine`, `standards-applicability`, `standards-authority`, `standards-identity`, `standards-metadata` | none |
| `standards-graph` | `tools.standards_graph.standards_graph` | none | `repository-graph-engine`, `standards-authority`, `standards-identity`, `standards-metadata`, `standards-policy-impact` | none |
| `standards-analysis` | `tools.standards_analysis.standards_analysis` | none | `repository-graph-engine`, `standards-applicability`, `standards-authority`, `standards-identity`, `standards-metadata`, `standards-policy-impact` | none |
| `standards-engine` | `tools.standards_engine.standards_engine` | none | `repository-graph-engine`, `standards-applicability`, `standards-analysis`, `standards-authority`, `standards-contracts`, `standards-graph`, `standards-identity`, `standards-metadata`, `standards-policy-impact` | none |
| `standards-verifier` | `tools.standards_verifier.standards_verifier` | `tools/query_edges.py`, `tools/verify_git_reachability.py`, `tools/standards_verifier/verify.py`, `tools/standards_verifier/generate_inventory.py`, `tools/standards_verifier/generate_numeric_audit.py`, `tools/standards_verifier/generate_numeric_retirements.py` | `repository-graph-engine`, `standards-applicability`, `standards-analysis`, `standards-contracts`, `standards-graph`, `standards-metadata`, `standards-policy-impact` | none |

Authority and Contracts deliberately have no dependency in either direction.
Authority owns its small internal envelope smart constructor and receives owner
codec sets through Engine composition. Contracts owns only public wire
validation and generation. The domain Modules above declare Authority and
Identity directly when their production paths construct authority-bound values
and owner-scoped semantic IDs. Applicability and the repository-neutral Graph
Engine remain free of repository authority mechanics.

The cutover gate parses production Python with `ast`, derives direct imports,
and requires exact equality with this manifest graph. For each cross-Module
import, `import dependency_root` is valid, while `import dependency_root.child`
and `from dependency_root.child import name` are invalid. For
`from dependency_root import name`, `name` must occur in the root's statically
resolved `__all__`; this prevents Python from implicitly loading an unexported
child module despite the syntactic root import. Cross-Module star imports and
literal or nonliteral `importlib`/`__import__` bypasses are invalid. Relative and
absolute imports within the owning Module remain valid only for files beneath
that Module's package root. A repository entrypoint is an external adapter to
its owning package and must import owner functionality through the manifest's
canonical public root; an alternate top-level package spelling is invalid even
when script-directory insertion would make it importable.

Each public-root `__init__.py` owns exports through exactly one `__all__`
assignment. The closed export-expression profile permits a tuple of unique
string literals and starred `<local-module-alias>.__all__` references, where
the alias comes from one relative import and the referenced local `__all__`
resolves through the same profile. Cycles, duplicate names, missing exports,
computed values, mutation after assignment, and imports outside the owning
package reject. This supports the generated contract algebra without copying
its evolving names into the facade initializer. The clean-environment smoke
loads every resolved name with `getattr(root, name)` so static declaration and
runtime binding are distinct, jointly required claims.

The verifier consumes manifests and package initializers directly and does not
duplicate package or symbol allowlists. Governed production sources are the
tracked Python files beneath each manifest root plus its exact
`repository-entrypoints`. A Git-index completeness pass rejects any tracked
non-test Python under `tools/` that belongs to neither set. Package test roots
remain test inputs and do not contribute production requirements.

Clean-environment execution covers every repository entrypoint as well as every
root/export. Each exact script is invoked with safe-path mode from outside the
checkout, with the reviewed checkout root as the sole `PYTHONPATH`; mutating
commands operate only on an isolated repository fixture. This proves that an
entrypoint does not depend on its script directory, ambient installation, or an
alternate package spelling. A root/export-only smoke is insufficient.

The Verifier root exports this exact repository-entrypoint Interface. Each
script imports one named adapter from
`tools.standards_verifier.standards_verifier` and does no package-path mutation,
private import, argument parsing, diagnostic adaptation, or domain dispatch of
its own:

| Repository entrypoint | Canonical root export | Clean execution |
| --- | --- | --- |
| `tools/query_edges.py` | `repository_graph_main` | list registered groups from the reviewed checkout |
| `tools/verify_git_reachability.py` | `git_reachability_main` | verify an explicit manifest in an isolated Git fixture |
| `tools/standards_verifier/verify.py` | `verifier_main` | list registered suite IDs from the reviewed checkout |
| `tools/standards_verifier/generate_inventory.py` | `generated_artifacts_main` | check generated artifacts in the reviewed checkout |
| `tools/standards_verifier/generate_numeric_audit.py` | `numeric_audit_main` | write the snapshot in an isolated repository fixture |
| `tools/standards_verifier/generate_numeric_retirements.py` | `numeric_retirements_main` | check retirements in the reviewed checkout |

Each adapter owns its parser, typed diagnostics, default-root injection, and
exit status. The script wrapper supplies only its derived default repository
root and process arguments. Adapter names are resolved from the root's
authoritative `__all__`; no entrypoint-name allowlist is copied into the
verifier check.

A transitive import does not satisfy a missing direct declaration, and an
unused declaration is invalid. Test-only imports are suite inputs, not
production requirements. Discovering a required edge, production source,
entrypoint, or public root outside this closed table is a re-plan trigger.

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
admitted Python version derives the roots above from package manifests and
performs public import smoke from outside the checkout with safe-path mode and
the exact checkout root as its sole `PYTHONPATH`. The following expansion is
illustrative evidence, not a second root authority:

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
selecting a build backend. The same clean environments execute every exact
manifest entrypoint against isolated inputs. Importability and execution do not
prove boundary compliance; the AST verifier owns that distinct claim. An
otherwise-valid generated-output
fixture and an otherwise-valid handwritten-facade fixture each cover both a
below-root private import and a root-form unexported child import and must reach
the exact typed package-boundary diagnostic. Additional fixtures cover a valid
export, cross-Module star import, dynamic import, malformed or cyclic export
closure, and an unowned production source. Focused projection tests also inspect
the generated import prelude, but they are not the independent acceptance
oracle.
A future separately installed or published internal distribution requires its
own build, dependency, release, and installation decision.

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
- every case in the feature-driven contract-semantic matrix agrees between the
  direct selected validator and the production Adapter, including the known A1
  regressions, without a repository keyword implementation;
- one schema mutation per admitted projection semantic changes the compiled
  model and affected public behavior;
- dependency errors are converted to stable project diagnostics;
- public operation closure and generated projections are complete; and
- unsupported projection constructs reject at compilation.

Generated freshness, adapter behavior, projection completeness, domain
invariants, and facade integration are separate claims. Agreement between two
project entry points is not presented as independent Draft conformance.

### SQLite interruption oracle

Milestone 2 selects the host `strace` executable only as a required-real Linux
test oracle. The production Authority package continues to depend only on the
standard library and `standards_identity`. The harness must capability-probe
`--inject`, signal delivery, and interception of `fsync` and `fdatasync`, then
prove from the trace that `SIGKILL` was injected at the selected synchronization
syscall after the child's pre-commit barrier. It does not accept a timeout,
sleep, repeated probabilistic kill, or ordinary process failure.

Support is capability-based rather than tied to one patch release; each
acceptance environment records its exact `strace` release, executable digest,
package artifact, source revision, and package source. The admitted planning
selection is Ubuntu Noble package `strace 6.8-0ubuntu2` on `amd64`. Missing
capability or different unresolved provenance makes the required-real
environment `unsupported` and blocks A1b acceptance rather than changing
production behavior or selecting a custom SQLite VFS.

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

The test-only `strace` oracle is likewise invoked from the host and is neither
copied nor bundled. Its exact admitted provenance is:

| Item | Exact authority and identity |
| --- | --- |
| Ubuntu binary package | Noble `amd64` package `strace_6.8-0ubuntu2_amd64.deb`; SHA-256 `d588810ae26b06fee6678dc81e5b54f6efcde8e718e4589adb4d11d254b9820b`; the [Ubuntu package page](https://packages.ubuntu.com/noble/strace) identifies source package `strace (6.8-0ubuntu2)`, Ubuntu Developers, and upstream `strace.io` |
| Source descriptor | [`strace_6.8-0ubuntu2.dsc`](https://archive.ubuntu.com/ubuntu/pool/main/s/strace/strace_6.8-0ubuntu2.dsc); SHA-256 `330679ec872f5d097809a28fe0bcd4fe3a0ba2a57e639feec53ffc3745aa831b`; signature key `92D618F668F22F8ED80BEEF5BA3E29338280B242`, identified by [Launchpad](https://launchpad.net/~paelzer) as Christian Ehrhardt; descriptor identifies source version `6.8-0ubuntu2`, Ubuntu Developers, and Debian VCS `https://salsa.debian.org/debian/strace.git` |
| Upstream source artifact | [`strace_6.8.orig.tar.xz`](https://archive.ubuntu.com/ubuntu/pool/main/s/strace/strace_6.8.orig.tar.xz); descriptor SHA-256 `ba6950a96824cdf93a584fa04f0a733896d2a6bc5f0ad9ffe505d9b41e970149` |
| Ubuntu/Debian packaging delta | [`strace_6.8-0ubuntu2.debian.tar.xz`](https://archive.ubuntu.com/ubuntu/pool/main/s/strace/strace_6.8-0ubuntu2.debian.tar.xz); descriptor SHA-256 `6efc6fde478f3beb37dbd246f1e9fe4f13e74eef794b5b66d7589f0933bc351b` |
| Tested executable | `/usr/bin/strace`; SHA-256 `28f957c227012de0b18d1bd7fff2d396cb693ea60ed8013be68de071e84b5001`; package version output `strace 6.8` and package-manager identity `6.8-0ubuntu2` |
| Copyright and notice authorities | [Ubuntu package copyright file](https://changelogs.ubuntu.com/changelogs/pool/main/s/strace/strace_6.8-0ubuntu2/copyright), installed as `/usr/share/doc/strace/copyright`; SHA-256 `40e4ca01654c733c06fabee65168da4c177117b1bd084f3a752bc8a989736e04`; identifies the named 1991-2001 contributors and The strace developers, 2001-2022. The exact tested executable additionally reports `Copyright (c) 1991-2024 The strace developers` in `strace --version`; both notices are retained as provenance rather than treating the older packaging summary as exhaustive. |
| License authority | The package copyright authority selects LGPL-2.1-or-later for the executable and points to the installed LGPL-2.1 text at `/usr/share/common-licenses/LGPL-2.1`; SHA-256 `dc626520dcd53a22f727af3ee42c770e56c97a64fe3adb063799d8ab032fe551` |

The package's separately licensed test suite is not copied or run. Invoking the
installed executable for internal verification creates no repository-
distribution notice obligation. The hashes above are evidence for this exact
selection, not a checked-in dependency lock or a promise that another host
package is equivalent. Vendoring, bundling, modifying, redistributing, or
selecting a differently sourced executable requires a new Licensing and
Release disposition.

The 2026-08-27 planning preflight downloaded the exact binary package, source
descriptor, upstream archive, and packaging delta from the authorities above
and reproduced every recorded artifact SHA-256. It also reproduced the
installed executable, copyright-file, and LGPL-2.1 hashes locally. Final
required-real acceptance repeats those checks and the capability probe.

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
