#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/binding-architecture-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly GENERIC="$REPO_ROOT/profiles/boundaries/language-bindings.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id scope annotation framework_dependency \
  host_behavior dependency_direction generated_state core_verification \
  capability fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$scope" =~ ^(core|adapter|generated)$ ]]
  [[ "$annotation" =~ ^(none|independent|coupled)$ ]]
  [[ "$framework_dependency" =~ ^(absent|present)$ ]]
  [[ "$host_behavior" =~ ^(absent|present)$ ]]
  [[ "$dependency_direction" =~ ^(none|adapter-to-core|core-to-adapter|generated-to-adapter)$ ]]
  [[ "$generated_state" =~ ^(generated|hand-edited|not-applicable)$ ]]
  [[ "$core_verification" =~ ^(pass|missing|not-applicable)$ ]]
  [[ "$capability" =~ ^(available|unavailable|not-required)$ ]]
  [[ "$fallback" =~ ^(none|merge-layers|skip-core-test|alternate-framework)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable)$ ]]
  [[ -z "${extra:-}" ]]

  invalid_architecture=0
  if [[ "$scope" == 'core' ]] &&
     [[ "$annotation" == 'coupled' || "$framework_dependency" == 'present' ||
        "$host_behavior" == 'present' ||
        "$dependency_direction" == 'core-to-adapter' ||
        "$core_verification" != 'pass' ]]; then
    invalid_architecture=1
  elif [[ "$scope" == 'adapter' &&
          "$dependency_direction" != 'adapter-to-core' ]]; then
    invalid_architecture=1
  elif [[ "$scope" == 'generated' ]] &&
       [[ "$dependency_direction" != 'generated-to-adapter' ||
          "$generated_state" != 'generated' ]]; then
    invalid_architecture=1
  fi

  if [[ "$fallback" != 'none' || "$invalid_architecture" -eq 1 ]]; then
    actual='typed-invalid'
  elif [[ "$capability" == 'unavailable' ]]; then
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

expected_ids=(STD-0759 STD-0760 STD-0790 STD-0791)
mapfile -t inventory_ids < <(
  awk -F '\t' '
    $1 == "STD-0759" || $1 == "STD-0760" ||
    $1 == "STD-0790" || $1 == "STD-0791" { print $1 }
  ' "$INVENTORY"
)
mapfile -t disposition_ids < <(
  awk -F '\t' '
    NR > 1 && ($1 == "STD-0759" || $1 == "STD-0760" ||
               $1 == "STD-0790" || $1 == "STD-0791") { print $1 }
  ' "$DISPOSITIONS"
)
[[ "${inventory_ids[*]}" == "${expected_ids[*]}" ]]
[[ "${disposition_ids[*]}" == "${expected_ids[*]}" ]]

while IFS=$'\t' read -r id source target disposition rationale extra; do
  case "$id" in
    STD-0759|STD-0760|STD-0790|STD-0791)
      [[ "$source:$target:$disposition" == \
        'languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md:profiles/languages/rust/language-bindings.md:refine' ]]
      [[ -n "$rationale" && -z "${extra:-}" ]]
      ;;
  esac
done < <(tail -n +2 "$DISPOSITIONS")

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$REPO_ROOT/topics/contracts.md" "$REPO_ROOT/topics/security.md" \
  "$REPO_ROOT/profiles/boundaries/interop.md" "$GENERIC" \
  "$RUST_INDEX" "$PROFILE"

required_profile=(
  '## Core And Adapter Boundary'
  'usable without a binding'
  'Adapters depend on core contracts'
  'adds no binding-'
  'A disabled-by-default'
  '## Verification'
  'core build and tests without binding features'
  'dependency and feature inspection'
  '## No Fallback'
  'cannot add a'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

rg -F -q '(language-bindings.md)' "$RUST_INDEX"
rg -F -q 'profiles/languages/rust/language-bindings.md' \
  "$REPO_ROOT/README.md" "$LEGACY"
rg -F -q '## Layer Ownership' "$GENERIC"

legacy_architecture="$(
  sed -n '/^## Three-Layer Architecture$/,/^### Workspace Layout$/p' "$LEGACY"
)"
for text in 'Layer 3:' 'optional `cfg_attr` annotations' \
  'Multiple binding crates can coexist' '### Rules'; do
  if rg -F -q "$text" <<< "$legacy_architecture"; then
    printf 'legacy Rust binding architecture remains active: %s\n' \
      "$text" >&2
    exit 1
  fi
done
rg -F -q 'language-bindings.md#core-and-adapter-boundary' \
  <<< "$legacy_architecture"

legacy_features="$(
  sed -n '/^### Feature Flags for Optional Binding Support$/,/^### cdylib Configuration$/p' "$LEGACY"
)"
for text in 'Core types that can be annotated directly' '# mylib-core/Cargo.toml' \
  '[features]' 'dep:uniffi'; do
  if rg -F -q "$text" <<< "$legacy_features"; then
    printf 'legacy Rust core binding dependency remains active: %s\n' \
      "$text" >&2
    exit 1
  fi
done
rg -F -q 'language-bindings.md#core-and-adapter-boundary' \
  <<< "$legacy_features"

for heading in '### Workspace Layout' '## Memory Ownership Model' \
  '## Async Bridging'; do
  rg -F -q "$heading" "$LEGACY"
done

rg -F -q '`7.4b5b` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-milestone-7-f025-f026-decomposition.sh"

printf 'Rust binding architecture policy passed: %s decisions, 4 exact dispositions\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
