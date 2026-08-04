#!/usr/bin/env bash
set -euo pipefail

readonly S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly R="$(cd -- "$S/../.." && pwd)"
readonly F="$S/fixtures/contracts/planning-boundary-decisions.tsv"
readonly C="$R/topics/contracts.md"
readonly A="$R/ARCHITECTURE-PATTERNS.md"

count=0
while IFS=$'\t' read -r case_id facts class deployment concurrent request expected extra; do
  [[ "$case_id" == case ]] && continue
  [[ -z "${extra:-}" ]]
  ((count += 1))

  if [[ "$facts" == missing ]]; then
    actual=typed-unavailable
  elif [[ "$request" != select ]]; then
    actual=typed-invalid
  elif [[ "$concurrent" == active ]]; then
    actual=freeze-temporary
  else
    case "$class:$deployment" in
      internal-coordinated:atomic) actual=replace ;;
      persisted:*) actual=migrate ;;
      public-versioned:*) actual=version ;;
      distributed-independent:independent) actual=negotiate ;;
      generated:*) actual=regenerate ;;
      *) actual=typed-invalid ;;
    esac
  fi

  [[ "$actual" == "$expected" ]] || {
    printf '%s: expected %s, got %s\n' "$case_id" "$expected" "$actual" >&2
    exit 1
  }
done < "$F"

rg -F -q 'Freeze the selected contract shape while parallel work depends on it.' "$A"
rg -F -q 'implementation-phase freeze into an indefinite compatibility promise.' "$A"
rg -F -q 'Unknown facts produce an unresolved-contract diagnostic.' "$C"
rg -F -q 'internal-coordinated' "$C"
rg -F -q 'distributed-independent' "$C"

if rg -q 'Define shared interfaces/types FIRST|Append-only changes|New types can be added, existing cannot change' "$A"; then
  printf 'Architecture Patterns retains rejected permanent-freeze or append-only policy\n' >&2
  exit 1
fi

expected_ids=(STD-{0046..0050})
mapfile -t disposed < <(awk -F '\t' '$1>="STD-0046"&&$1<="STD-0050"{print $1}' "$S/consolidation-dispositions.tsv")
[[ "${disposed[*]}" == "${expected_ids[*]}" ]]
[[ "$(awk -F '\t' '$1>="STD-0046"&&$1<="STD-0050"&&($2!="ARCHITECTURE-PATTERNS.md"||$3!="topics/contracts.md"||$4!="index"||NF!=5){n++}END{print n+0}' "$S/consolidation-dispositions.tsv")" -eq 0 ]]

printf 'Contract planning boundary passed: %s decisions, 5 exact dispositions\n' "$count"
