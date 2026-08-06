# Rust Standards Migration Index

This file is non-normative migration navigation. It owns no Rust policy and
does not establish applicability, precedence, or a default mechanism.

## Canonical Route

Use the [canonical Rust profile](../../profiles/languages/rust/README.md) for
Rust applicability, baseline verification, and routing to specialized owners.
The profile selects only owners supported by established project facts.

Missing owner or applicability facts return a typed `unavailable` diagnostic,
contradictory routing facts return typed `invalid`, and unsupported mechanisms
return typed `unsupported` through their selected owner. Do not treat this
index or its former documents as fallback authority.
