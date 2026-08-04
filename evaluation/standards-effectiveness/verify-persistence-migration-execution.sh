#!/usr/bin/env bash
set -euo pipefail
S="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"&&pwd)";R="$(cd -- "$S/../.."&&pwd)";F="$S/fixtures/persistence/migration-execution-decisions.tsv";D="$R/profiles/boundaries/persistence.md";A="$R/ARCHITECTURE-PATTERNS.md"
count=0
while IFS=$'\t' read -r case_id selection source destination artifact identity integrity order ledger coordination reentry interruption overlap trigger capability fallback expected extra;do
 [[ "$case_id" == case ]]&&continue;[[ -z "${extra:-}" ]];((count+=1))
 if [[ "$fallback" != none || "$identity" == mismatched || "$integrity" == failed || "$order" == guessed || "$ledger" == contradictory || "$reentry" == repeated-unproven || "$interruption" == unknown-partial || "$overlap" == speculative || "$trigger" == implicit-startup ]];then actual=typed-invalid
 elif [[ "$source" == unsupported || "$destination" == unsupported || "$capability" == unsupported ]];then actual=typed-unsupported
 elif [[ "$selection" == selected && ( "$artifact" == missing || "$identity" == missing || "$integrity" == missing || "$order" == missing || "$ledger" == missing || "$coordination" == missing || "$capability" == missing ) ]];then actual=typed-unavailable
 else actual=allow;fi
 [[ "$actual" == "$expected" ]]||{ printf '%s: expected %s got %s\n' "$case_id" "$expected" "$actual" >&2;exit 1;}
done < "$F"
for text in '## Migration Execution Contract' 'source and destination states selected' 'migration identity and integrity' 'deterministic dependency' 'ledger consistent' 'does not authorize repeated application' 'startup is one possible trigger' 'none is a compatibility default';do rg -F -q "$text" "$D";done
for text in '## Illustrative Migration Adapters' 'These filenames, fields, SQL types' 'explicitly selected startup adapter' 'not discover pending work by guess';do rg -F -q "$text" "$R/reference/recipes/persistence.md";done
section="$(awk '/^## Schema Versioning and Migration/{capture=1} /^## Infrastructure Failure Recovery Index/{capture=0} capture{print}' "$A")"
for text in '[Persistence boundary profile]' '[Contracts]' '[Persistence Mechanism Recipes]';do [[ "$section" == *"$text"* ]];done
for text in '### The Pattern' '001_initial_schema.sql' 'schema_migrations' 'apply_pending_migrations' 'Add column' 'Two-phase removal' 'destructive replacement does not require a speculative';do [[ "$section" != *"$text"* ]];done
expected=(STD-{0113..0118});mapfile -t disposed < <(awk -F '\t' '$1>="STD-0113"&&$1<="STD-0118"{print $1}' "$S/consolidation-dispositions.tsv");[[ "${disposed[*]}" == "${expected[*]}" ]]
printf 'Persistence migration execution passed: %s decisions, 6 exact dispositions\n' "$count"
