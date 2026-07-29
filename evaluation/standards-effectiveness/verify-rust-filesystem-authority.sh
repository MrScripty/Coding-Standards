#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE="$SCRIPT_DIR/fixtures/rust/filesystem-authority-decisions.tsv"
readonly INVENTORY="$SCRIPT_DIR/generated/section-inventory.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/security.md"
readonly RUST_INDEX="$REPO_ROOT/profiles/languages/rust/README.md"
readonly SECURITY="$REPO_ROOT/topics/security.md"
readonly CROSS_PLATFORM="$REPO_ROOT/topics/cross-platform.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-SECURITY-STANDARDS.md"
readonly FINDINGS="$SCRIPT_DIR/findings.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

while IFS=$'\t' read -r case_id target containment mutation use_authority \
  fallback expected extra; do
  [[ "$case_id" == 'case' ]] && continue
  [[ "$target" =~ ^(existing|create)$ ]]
  [[ "$containment" =~ ^(proven|escaped|unproven|unknown)$ ]]
  [[ "$mutation" =~ ^(excluded|concurrent|unknown)$ ]]
  [[ "$use_authority" =~ ^(held-file|handle-relative|revalidated-path|plain-path|unavailable)$ ]]
  [[ "$fallback" =~ ^(none|plain-path|revalidate|lexical|alternate-root|unanchored-create)$ ]]
  [[ "$expected" =~ ^(allow|typed-invalid|typed-unavailable|typed-unsupported)$ ]]
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != 'none' ||
        "$containment" =~ ^(escaped|unproven)$ ]]; then
    actual='typed-invalid'
  elif [[ "$containment" == 'unknown' || "$mutation" == 'unknown' ]]; then
    actual='typed-unavailable'
  elif [[ "$mutation" == 'concurrent' &&
          "$use_authority" == 'unavailable' ]]; then
    actual='typed-unsupported'
  elif [[ "$mutation" == 'concurrent' &&
          ! "$use_authority" =~ ^(held-file|handle-relative)$ ]]; then
    actual='typed-invalid'
  elif [[ "$mutation" == 'excluded' &&
          ! "$use_authority" =~ ^(held-file|handle-relative|revalidated-path)$ ]]; then
    actual='typed-invalid'
  else
    actual='allow'
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$FIXTURE"

[[ "$(awk -F '\t' '$1 == "STD-0822" { count += 1 } END { print count + 0 }' \
  "$INVENTORY")" -eq 1 ]]
[[ "$(awk -F '\t' 'NR > 1 && $1 == "STD-0822" { count += 1 } END { print count + 0 }' \
  "$DISPOSITIONS")" -eq 1 ]]
awk -F '\t' '
  NR > 1 && $1 == "STD-0822" {
    if ($2 != "languages/rust/RUST-SECURITY-STANDARDS.md" ||
        $3 != "profiles/languages/rust/security.md" ||
        $4 != "refine" || $5 == "" || NF != 5) {
      exit 1
    }
    found = 1
  }
  END { exit !found }
' "$DISPOSITIONS"

"$SCRIPT_DIR/check-metadata.sh" \
  "$REPO_ROOT" "$REPO_ROOT/CORE-STANDARDS.md" \
  "$REPO_ROOT/workflows/verification.md" \
  "$SECURITY" "$CROSS_PLATFORM" "$RUST_INDEX" "$PROFILE"

required_profile=(
  '## Filesystem Authority Through Use'
  'A canonicalized `PathBuf` records'
  'directory capability and use a handle-relative operation'
  'handle-relative operation'
  'Immediate revalidation is sufficient only'
  'typed `invalid`, `unsupported`, or `unavailable`'
  '## No Fallback'
  '## Verification'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done
rg -F -q '## Validation And Use' "$SECURITY"
rg -F -q 'handle-relative, capability-based' "$SECURITY"

legacy_path="$(
  sed -n '/^## Path Validation$/,/^## Checked Arithmetic At Boundaries$/p' \
    "$LEGACY"
)"
rg -F -q 'security.md#filesystem-authority-through-use' <<< "$legacy_path"
for text in 'validate_within_root' '.canonicalize()' \
  'starts_with(&root)' 'Option<PathBuf>' 'Parse once into a validated type'; do
  if rg -F -q "$text" <<< "$legacy_path"; then
    printf 'legacy pathname-authority guidance remains: %s\n' "$text" >&2
    exit 1
  fi
done

for heading in '## Checked Arithmetic At Boundaries' '## Bounded Queues' \
  '## Network Listener Limits' '## Panic Policy'; do
  rg -F -q "$heading" "$LEGACY"
done

rg -F -q '| F026 | Partially resolved in Milestone 7.4b5e |' "$FINDINGS"
rg -F -q '`7.4b5e` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-filesystem-containment-policy.sh"
"$SCRIPT_DIR/verify-milestone-7-f025-f026-decomposition.sh"

printf 'Rust filesystem authority policy passed: %s decisions, 1 exact disposition\n' \
  "$(( $(wc -l < "$FIXTURE") - 1 ))"
