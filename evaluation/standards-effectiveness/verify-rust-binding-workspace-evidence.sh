#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly FIXTURE_DIR="$SCRIPT_DIR/fixtures/rust"
readonly SCHEMA="$FIXTURE_DIR/binding-workspace-evidence-schema.tsv"
readonly DECISIONS="$FIXTURE_DIR/binding-workspace-evidence-decisions.tsv"
readonly OBSERVED="$FIXTURE_DIR/binding-workspace-evidence-observed.tsv"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PROFILE="$REPO_ROOT/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$REPO_ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly PLAN="$REPO_ROOT/plans/standards-library-effectiveness-restructure-plan.md"

"$SCRIPT_DIR/check-decision-table.sh" "$SCHEMA" "$DECISIONS" "$OBSERVED"

while IFS=$'\t' read -r case_id package_facts dependency_direction \
  adapter_required core_evidence adapter_evidence capability fallback expected \
  extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]

  if [[ "$fallback" != none ||
        "$package_facts" == contradictory ||
        "$dependency_direction" == reversed ||
        "$adapter_evidence" == native-only ]]; then
    actual=typed-invalid
  elif [[ "$package_facts" == missing ||
          "$core_evidence" == missing ||
          "$capability" == unavailable ||
          ( "$adapter_required" == yes &&
            "$adapter_evidence" == missing ) ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, derived %s\n' \
      "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$DECISIONS"

awk -F '\t' '
  NR > 1 && ($1 == "STD-0761" || $1 == "STD-0762") {
    count += 1
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        $3 != "profiles/languages/rust/language-bindings.md" ||
        $4 != "refine" || $5 == "" || NF != 5) exit 1
  }
  END { exit count != 2 }
' "$DISPOSITIONS"

required_profile=(
  'Select crate, package, workspace-member, feature, generated-output, and script'
  'code may use separate packages or remain in one package'
  'not evidence waivers'
  'real host evidence remains part of acceptance'
  'typed `unavailable`'
  'typed `invalid`'
  'Do not prescribe a crate tree'
  'substitute native-only tests'
  'select another framework'
  'report default success'
)
for text in "${required_profile[@]}"; do
  rg -F -q "$text" "$PROFILE"
done

legacy_section="$(sed -n '/^### Workspace Layout$/,/^---$/p' "$LEGACY")"
rg -F -q 'language-bindings.md#package-and-workspace-placement' \
  <<< "$legacy_section"
rg -F -q 'No crate tree' <<< "$legacy_section"
for removed in \
  '[workspace]' \
  'default-members' \
  'mylib-uniffi' \
  'generate-bindings.sh'; do
  ! rg -F -q "$removed" <<< "$legacy_section"
done

rg -F -q '`7.4b8x` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-rust-binding-core-adapter-testability.sh"
"$SCRIPT_DIR/verify-milestone-7-row-7-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Rust binding workspace/evidence passed: %s decisions, 2 exact dispositions\n' \
  "$(( $(wc -l < "$DECISIONS") - 1 ))"
