#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly FIXTURE="$S/fixtures/rust/security-panic-boundary-decisions.tsv"
readonly PROFILE="$R/profiles/languages/rust/security.md"
readonly LEGACY="$R/languages/rust/RUST-SECURITY-STANDARDS.md"
readonly DISPOSITIONS="$S/consolidation-dispositions.tsv"
readonly PLAN="$R/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id context failure proof panic_form documentation fallback expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$proof" == missing && "$failure" == invariant ]]; then
    actual=typed-unavailable
  elif [[ "$fallback" != none ||
          ( "$failure" == recoverable && "$panic_form" != result ) ]]; then
    actual=typed-invalid
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]] || { printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2; exit 1; }
done < "$FIXTURE"

awk -F '\t' 'NR > 1 && $1 == "STD-0826" { print $2 ":" $3 ":" $4 }' "$DISPOSITIONS" |
  grep -Fx 'languages/rust/RUST-SECURITY-STANDARDS.md:profiles/languages/rust/security.md:refine'

for text in 'Panic And Recoverable Error Boundary' 'Rust API error policy' 'production request paths' 'typed `unavailable`' 'typed `invalid`' 'broad catch-all recovery'; do
  rg -F -q "$text" "$PROFILE"
done
legacy="$(sed -n '/^## Panic Policy$/,$p' "$LEGACY")"
rg -F -q 'security.md#panic-and-recoverable-error-boundary' <<< "$legacy"
for removed in 'Production request paths, lifecycle code' 'must not use `unwrap()` or `expect()`'; do
  ! rg -F -q "$removed" <<< "$legacy"
done

"$S/verify-rust-listener-lifecycle.sh"
"$S/verify-rust-filesystem-authority.sh"
rg -F -q '`7.4b8ah` (`Accepted`)' "$PLAN"
"$S/verify-milestone-7-execution-train.sh"
printf 'Rust security panic boundary passed: 11 decisions, 1 exact disposition\n'
