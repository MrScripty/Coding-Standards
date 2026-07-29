#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
readonly BASE="$SCRIPT_DIR/fixtures/rust/binding-contract-discovery"
readonly PROFILE="$ROOT/profiles/languages/rust/language-bindings.md"
readonly LEGACY="$ROOT/languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md"
readonly DISPOSITIONS="$SCRIPT_DIR/consolidation-dispositions.tsv"
readonly PLAN="$ROOT/plans/standards-library-effectiveness-restructure-plan.md"

"$SCRIPT_DIR/check-decision-table.sh" \
  "$BASE-schema.tsv" "$BASE-decisions.tsv" "$BASE-observed.tsv"

while IFS=$'\t' read -r case_id contract mechanism value evidence fallback \
  expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  if [[ "$fallback" != none || "$mechanism" == alternate ||
        "$contract" == contradictory || "$value" == invalid ]]; then
    actual=typed-invalid
  elif [[ "$contract" == not-required ]]; then
    actual=no-discovery
  elif [[ "$value" == unsupported ]]; then
    actual=typed-unsupported
  elif [[ "$contract" == missing || "$mechanism" == none ||
          "$value" == unavailable || "$evidence" == missing ]]; then
    actual=typed-unavailable
  else
    actual=allow
  fi
  [[ "$actual" == "$expected" ]]
done < "$BASE-decisions.tsv"

awk -F '\t' '
  NR > 1 && $1 == "STD-0809" {
    count++
    if ($2 != "languages/rust/RUST-LANGUAGE-BINDINGS-STANDARDS.md" ||
        $3 != "profiles/languages/rust/language-bindings.md" ||
        $4 != "refine" || $5 == "" || NF != 5) exit 1
  }
  END { exit count != 1 }
' "$DISPOSITIONS"

for text in \
  '## Contract Discovery Adaptation' \
  'only when the selected Contracts-owned' \
  'exported operation, handshake field, package' \
  'not a universal' \
  'Return `invalid`' \
  '`unsupported`' \
  '`unavailable`' \
  'universal `version()`' \
  'alternate discovery' \
  'default success'; do
  rg -F -q "$text" "$PROFILE"
done

legacy_section="$(sed -n '/^### Version Export$/,$p' "$LEGACY")"
rg -F -q 'language-bindings.md#contract-discovery-adaptation' \
  <<< "$legacy_section"
! rg -F -q 'pub fn version()' <<< "$legacy_section"
! rg -F -q 'CARGO_PKG_VERSION' <<< "$legacy_section"

rg -F -q '`7.4b8r` (`Accepted`)' "$PLAN"
rg -F -q '`7.4b8s` (`Accepted`)' "$PLAN"
"$SCRIPT_DIR/verify-binding-contract-evolution.sh"
"$SCRIPT_DIR/verify-milestone-7-row-5-decomposition.sh"
"$SCRIPT_DIR/verify-milestone-7-execution-train.sh"

printf 'Rust binding contract discovery passed: %s decisions, 1 exact disposition\n' \
  "$(( $(wc -l < "$BASE-decisions.tsv") - 1 ))"
