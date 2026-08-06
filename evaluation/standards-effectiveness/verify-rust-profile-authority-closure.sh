#!/usr/bin/env bash
set -euo pipefail

S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
R="$(cd -- "$S/../.." && pwd)"
PROFILE="$R/profiles/languages/rust/README.md"

for metadata in 'ID: `profile.language.rust`' 'Requires: `core`' \
  'Canonical owner: `profiles/languages/rust/README.md`'; do
  rg -F -q "$metadata" "$PROFILE"
done

for route in '(api.md)' '(dependencies.md)' '(release.md)' '(tooling.md)' \
  '(async.md)' '(cross-platform.md)' '(unsafe.md)' '(interop.md)' \
  '(security.md)' '(language-bindings.md)'; do
  rg -F -q "$route" "$PROFILE"
done

for text in '## Canonical Routing And No Legacy Authority' \
  'non-normative migration indexes' 'they do not own Rust policy' \
  'typed `unavailable`' 'typed `invalid`' 'typed `unsupported`' \
  'Do not fall back to a legacy Rust file' 'default runtime, tool, target' \
  'feature matrix, benchmark adapter, unsafe'; do
  rg -F -q "$text" "$PROFILE"
done
for text in '## Detailed Guidance During Migration' \
  '../../../languages/rust/' 'remain canonical for specialized rules' \
  'legacy Rust rule conflicts' 'Criterion is required'; do
  ! rg -F -q "$text" "$PROFILE"
done

"$S/verify-rust-api-owner-contract.sh"
"$S/verify-rust-async-boundary.sh"
"$S/verify-rust-unsafe-contracts.sh"
"$S/verify-rust-tooling-criterion.sh"
"$S/verify-language-profile-routing.sh"
"$S/verify-root-readme-consumer-audit.sh"
"$S/verify-milestone-7-row-46-decomposition.sh"
printf 'Rust profile authority closure passed: canonical specialized routes, typed diagnostics, no legacy authority\n'
