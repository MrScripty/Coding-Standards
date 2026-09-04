# A1b Milestone 0 Dependency Provenance

**Recorded:** 2026-08-27

**Planning selection:**
[dependency-and-dialect-decision.md](dependency-and-dialect-decision.md)

## Exact Lock

`tools/standards_contracts/requirements.lock` contains the complete reviewed
resolution and only these wheel hashes:

| Package | Version | Selected wheel scope | SHA-256 |
| --- | --- | --- | --- |
| `attrs` | `26.1.0` | universal | `c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309` |
| `jsonschema` | `4.26.0` | universal | `d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce` |
| `jsonschema-specifications` | `2025.9.1` | universal | `98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe` |
| `referencing` | `0.37.0` | universal | `381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231` |
| `rpds-py` | `2026.6.3` | CPython 3.11, manylinux 2.17 x86-64 | `9c1255b302953c86a486b81d330d5ee1d5bd937691ce271b6be0ef0e299eaab7` |
| `rpds-py` | `2026.6.3` | CPython 3.12, manylinux 2.17 x86-64 | `ecabd69db66de867690f9797f2f8fa27ba501bbc24540cbdbdc649cd15888ba6` |
| `typing-extensions` | `4.16.0` | universal | `481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8` |

The accepted install command was executed independently in fresh CPython 3.11
and 3.12 virtual environments:

```sh
python -m pip install \
  --require-hashes \
  --only-binary=:all: \
  -r tools/standards_contracts/requirements.lock
```

Pip selected the exact platform wheel for each interpreter, rejected the other
marker, and reported the six expected installed distributions. `pip check`
reported `No broken requirements found` in both environments.

## Environment

| Claim | Observed value |
| --- | --- |
| Required architecture | `x86_64` |
| Required filesystem for later durable-store evidence | `ext4` |
| CPython 3.11 environment | `3.11.14` |
| CPython 3.12 environment | `3.12.3` |
| Host glibc | `2.39` |
| Minimum selected wheel ABI | manylinux glibc `2.17` |

Both environments imported `jsonschema.Draft202012Validator` and
`referencing.Registry` and passed the isolated dependency-resolution tests.
The repository source tree supplied the new stdlib-only `standards_identity`
package through `PYTHONPATH`; it was not installed as an external distribution.

## License And Notice Reproduction

Installed wheel metadata reported the admitted license expressions and exact
license paths. SHA-256 over those installed files reproduced all reviewed
values:

| Package | Expression | License hash |
| --- | --- | --- |
| `attrs` | MIT | `882115c95dfc2af1eeb6714f8ec6d5cbcabf667caff8729f42420da63f714e9f` |
| `jsonschema` | MIT | `4f92a015a13c4d1a040bef018aa13430b4f1bc73b41b16bb846c346766de7439` |
| `jsonschema-specifications` | MIT | `42dcd63495f87b4eb7c7757afa379bb55a53f94afd7a5f657d9adf57236e515c` |
| `referencing` | MIT | `42dcd63495f87b4eb7c7757afa379bb55a53f94afd7a5f657d9adf57236e515c` |
| `rpds-py` | MIT | `314e4e91be3baa93c0fb4bccc9e4e97cd643eb839b065af921782c2175fe9909` |
| `typing-extensions` | PSF-2.0 | `3b2f81fe21d181c499c59a256c8e1968455d6689d269aa85373bfb6af41da3bf` |

No wheel, source archive, license text, or third-party test corpus is copied
into the repository. The installed distributions retain their metadata and
license files. The reviewed non-bundling disposition remains unchanged.

## Security Result

An exact package-version batch query to the authoritative OSV API on
2026-08-27 returned six empty result objects, one for each locked distribution.
No known vulnerability was reported for the exact resolution at verification
time. This is time-bound evidence; a version update or later blocking advisory
reopens dependency acceptance.

## Disposition

The implemented lock reproduces the admitted package, artifact, target,
license, notice, and security selection. This evidence supports automated
A1B-A6. A1B-A6L remains a separate final independent claim and the required-real
`strace` interruption behavior remains Milestone 2 work.
