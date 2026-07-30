# Cross-Platform Standards

Canonical target support, platform-behavior isolation, mechanism selection,
semantic fidelity, and typed unresolved outcomes moved to the
[Cross-Platform topic](topics/cross-platform.md#platform-support-contract).
Language-specific mechanisms are selected through the
[Standards Router](STANDARDS-ROUTER.md).

---

## File System Conventions

Canonical path construction, display/lexical/canonical identity, comparison,
alias, space, and filesystem-family verification policy moved to
[Cross-Platform](topics/cross-platform.md#filesystem-paths). Untrusted
filesystem authorization additionally follows
[Security containment](topics/security.md#filesystem-containment).

---

## Native Library Rules

Native artifact loading is governed by the canonical
[Cross-Platform loading contract](topics/cross-platform.md#native-artifact-loading).

### Loading Strategy

See the
[Cross-Platform loading contract](topics/cross-platform.md#native-artifact-loading).

### Library Naming

Native artifact identity is governed by the canonical
[Release artifact plan](workflows/release.md#artifact-plan).

### Installation Documentation

Native artifact acquisition, installation, and loading information is governed
by the canonical [Release artifact plan](workflows/release.md#artifact-plan).

---

## CI Matrix

Platform evidence coverage is governed by the canonical
[Verification workflow](workflows/verification.md#platform-evidence-coverage).

### When to Build

Evidence scheduling is governed by the canonical
[Verification workflow](workflows/verification.md#platform-evidence-coverage).
