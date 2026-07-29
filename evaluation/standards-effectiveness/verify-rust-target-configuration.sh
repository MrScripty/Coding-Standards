#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/target-configuration-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/cross-platform.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly ROUTER="$REPO_ROOT/STANDARDS-ROUTER.md"
readonly README="$REPO_ROOT/README.md"
readonly GENERIC="$REPO_ROOT/topics/cross-platform.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-CROSS-PLATFORM-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id targets target_contract rust_target \
  artifact_claim mechanism mechanism_basis mechanism_owner precedence boundary \
  cfg_placement evidence environment fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$targets" =~ ^(single|multiple|unknown|default)$ ]]
  [[ "$target_contract" =~ ^(declared|missing|contradictory)$ ]]
  [[ "$rust_target" =~ ^(selected|unsupported|unknown|fixed-default)$ ]]
  [[ "$artifact_claim" =~ ^(compile|link|package|integration|runtime|unknown)$ ]]
  [[ "$mechanism" =~ ^(cfg|build-script|feature|composition|dispatch|combined|unknown|default)$ ]]
  [[ "$mechanism_basis" =~ ^(declared|missing|target-substitute|unjustified)$ ]]
  [[ "$mechanism_owner" =~ ^(explicit|missing)$ ]]
  [[ "$precedence" =~ ^(explicit|not-applicable|ambiguous|missing)$ ]]
  [[ "$boundary" =~ ^(cohesive|domain-inline|universal-trait|universal-module|missing)$ ]]
  [[ "$cfg_placement" =~ ^(inline|module|build-selected|not-applicable|numeric-threshold)$ ]]
  [[ "$evidence" =~ ^(matched|compile-only|simulated|missing)$ ]]
  [[ "$environment" =~ ^(real-target|toolchain|declared-simulator|substitute-tool|unknown)$ ]]
  [[ "$fallback" =~ ^(none|default-triples|best-effort|universal-layout|numeric-threshold|named-tool|simulated-substitute|alternate-target|weaker-evidence)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unsupported|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$targets" == 'default' ||
        "$target_contract" == 'contradictory' ||
        "$rust_target" == 'fixed-default' ||
        "$mechanism" == 'default' ||
        "$mechanism_basis" =~ ^(target-substitute|unjustified)$ ||
        "$precedence" == 'ambiguous' ||
        ( "$mechanism" == 'combined' && "$precedence" == 'not-applicable' ) ||
        "$boundary" =~ ^(domain-inline|universal-trait|universal-module)$ ||
        "$cfg_placement" == 'numeric-threshold' ||
        "$evidence" =~ ^(compile-only|simulated)$ ||
        "$environment" == 'substitute-tool' ]]; then
    actual='typed-invalid'
  elif [[ "$rust_target" == 'unsupported' ]]; then
    actual='typed-unsupported'
  elif [[ "$targets" == 'unknown' ||
          "$target_contract" == 'missing' ||
          "$rust_target" == 'unknown' ||
          "$artifact_claim" == 'unknown' ||
          "$mechanism" == 'unknown' ||
          "$mechanism_basis" == 'missing' ||
          "$mechanism_owner" == 'missing' ||
          "$precedence" == 'missing' ||
          "$boundary" == 'missing' ||
          "$evidence" == 'missing' ||
          "$environment" == 'unknown' ]]; then
    actual='typed-unavailable'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

expected_ids=(STD-0726 STD-0727 STD-0728 STD-0729 STD-0730)
mapfile -t inventory_ids < <(
  awk -F '\t' '$1 >= "STD-0726" && $1 <= "STD-0730" { print $1 }' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' 'NR > 1 && $1 >= "STD-0726" && $1 <= "STD-0730" { print $1 }' \
    "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in STD-072[6-9]|STD-0730) ;; *) continue ;; esac
  [[ "$source" == 'languages/rust/RUST-CROSS-PLATFORM-STANDARDS.md' ]]
  [[ "$target" == 'profiles/languages/rust/cross-platform.md' ]]
  if [[ "$id" == 'STD-0726' ]]; then
    [[ "$disposition" == 'move' ]]
  else
    [[ "$disposition" == 'refine' ]]
  fi
  [[ -n "$rationale" && -z "${extra:-}" ]]
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" \
  "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$GENERIC" \
  "$RUST_INDEX" \
  "$PROFILE"

required_profile=(
  '## Rust Target Contract'
  'project, product, or release target'
  '## Configuration And Placement'
  '`cfg`'
  'build scripts, features, composition, and dispatch'
  'smallest'
  'No shared trait,'
  'Inline `cfg`'
  '## Evidence By Claim'
  'Target compilation does not prove linking'
  'typed `invalid`, `unsupported`, or `unavailable`'
  '## No Fallback'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

rg -F -q 'Rust target selection, configuration placement' "$RUST_INDEX"
rg -F -q '[Rust Cross-Platform profile](cross-platform.md)' "$RUST_INDEX"
rg -F -q '[Rust Cross-Platform profile](profiles/languages/rust/cross-platform.md)' \
  "$ROUTER"
rg -F -q '| [profiles/languages/rust/cross-platform.md](profiles/languages/rust/cross-platform.md) |' \
  "$README"

for pattern in 'RUST-CROSS-PLATFORM-STANDARDS.md' \
  'x86_64-unknown-linux-gnu' 'x86_64-pc-windows-msvc' \
  'aarch64-apple-darwin' 'Best-effort' 'five lines or fewer' \
  'three or more parameters' 'two inline `cfg()` blocks' \
  'Use `cross`' 'containerized builds' 'hosted CI runners'; do
  if rg -F -q "$pattern" "$PROFILE" "$RUST_INDEX" "$ROUTER" "$README"; then
    printf 'fixed Rust target/configuration guidance remains: %s\n' \
      "$pattern" >&2
    exit 1
  fi
done

diff -u <(
  printf '%s\n' \
    '# Rust Cross-Platform Standards' \
    '' \
    'Canonical Rust target selection, configuration placement, and evidence policy' \
    'moved to the' \
    '[Rust Cross-Platform profile](../../profiles/languages/rust/cross-platform.md).' \
    'Generic target support and semantic-fidelity policy remains in' \
    '[Cross-Platform](../../topics/cross-platform.md).'
) "$LEGACY"
for pattern in 'x86_64-unknown-linux-gnu' 'x86_64-pc-windows-msvc' \
  'aarch64-apple-darwin' 'Best-effort' 'shared trait' \
  'five lines or fewer' 'three or more parameters' \
  'two inline `cfg()` blocks' 'cargo check' 'Use `cross`' \
  'containerized builds' 'hosted CI runners'; do
  if rg -F -q "$pattern" "$LEGACY"; then
    printf 'legacy Rust target/configuration guidance remains: %s\n' \
      "$pattern" >&2
    exit 1
  fi
done

rg -F -q '| F047 | Resolved in Milestone 7.4b7e |' "$FINDINGS"
rg -F -q '`7.4b7e` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-platform-target-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-independent-trust-replan.sh"

printf 'Rust target/configuration policy passed: %s decisions, 5 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
