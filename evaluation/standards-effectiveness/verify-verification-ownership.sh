#!/usr/bin/env bash
set -euo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly WORKFLOW="$ROOT/workflows/verification.md"
readonly TESTING="$ROOT/TESTING-STANDARDS.md"
readonly TOOLING="$ROOT/TOOLING-STANDARDS.md"
readonly LAUNCHER="$ROOT/LAUNCHER-STANDARDS.md"
readonly RELEASE="$ROOT/RELEASE-STANDARDS.md"
readonly RELEASE_WORKFLOW="$ROOT/workflows/release.md"

for heading in \
  "## Acceptance Is A Set Of Claims" \
  "## Evidence Kinds" \
  "## Environment Qualification" \
  "## Execution Mode" \
  "## Smoke Checks" \
  "## Scheduling And Duration"; do
  grep -qFx "$heading" "$WORKFLOW"
done

for file in "$TESTING" "$TOOLING" "$LAUNCHER"; do
  if [[ "$(grep -c 'workflows/verification.md' "$file")" -lt 1 ]]; then
    printf '%s: missing canonical verification link\n' \
      "${file#"$ROOT"/}" >&2
    exit 1
  fi
done

grep -q 'workflows/release.md' "$RELEASE"
grep -q '(verification.md)' "$RELEASE_WORKFLOW"

if rg -q '< 10ms|< 1s|< 30s|CI only|^## Verification Layers$|^### Targets$' \
  "$TESTING"; then
  printf 'TESTING-STANDARDS.md retains universal timing or acceptance taxonomy\n' >&2
  exit 1
fi

if rg -q '^\| Tests \| Affected only \| Full suite \|$' "$TOOLING"; then
  printf 'TOOLING-STANDARDS.md retains a universal local/CI test schedule\n' >&2
  exit 1
fi

grep -q 'Startup alone is usually' "$WORKFLOW"
grep -q 'evidence and never substitutes' "$WORKFLOW"
grep -q 'does not prove changed feature behavior' "$RELEASE_WORKFLOW"

printf 'Verification ownership checks passed\n'
