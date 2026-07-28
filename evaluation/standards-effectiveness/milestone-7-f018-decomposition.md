# Milestone 7 F018 Decomposition

## Purpose

This report decomposes critical finding `F018` before normative guidance moves.
It is planning evidence, not a standards owner. The accepted sequence keeps
runtime proof, IPC specialization, and security trust-boundary policy distinct
while removing all assertion-based validation examples without fallback.

## Trigger And Evidence

The legacy corpus currently presents three unsafe forms:

- the executable-contract example casts `unknown` to a request type;
- the IPC example switches on an action and casts its payload to the expected
  action payload; and
- the Security example checks only generic envelope fields before casting the
  complete value to `ValidatedMessage`.

These forms can produce a validated type without proving the fields required by
the selected operation. Frozen sections `STD-0053`, `STD-0067`, and `STD-0593`
contain the direct defects. Their parent sections are included only where
needed to establish one canonical owner and remove competing legacy guidance.

## Binding Ownership

| Owner | Authority |
| --- | --- |
| `topics/contracts.md` | Defines what runtime evidence is sufficient to construct a validated value from unknown boundary input. |
| `profiles/boundaries/ipc.md` | Specializes contract decoding for IPC envelope, category/action discriminants, action-specific payloads, correlation fields, and unsupported actions. |
| `topics/security.md` | Requires untrusted boundary input to pass the applicable complete decoder before authority or side effects; it does not own contract schemas or IPC dispatch. |

Contracts must be accepted before the IPC profile can specialize them. Security
links to those owners and adds trust-boundary consequences without duplicating
their decoder rules. A type assertion, deserializer success, generic object
check, envelope-only check, or static producer type is not runtime proof of an
action-specific payload.

## Slice Map

[milestone-7-f018-slices.tsv](milestone-7-f018-slices.tsv) records the exact
frozen identifiers, target owners, proposed final dispositions, and execution
order.

| Slice | Frozen IDs | Outcome |
| --- | --- | --- |
| `7.4b2b` | `STD-0051`-`STD-0054` | Canonical generic runtime-decoding proof in Contracts. |
| `7.4b2c` | `STD-0063`-`STD-0068`, `STD-0592`-`STD-0595` | Canonical action-specific IPC decoding and Security trust-boundary linkage. |

The slices are serial. No other trust-boundary or consolidation slice may run
between them while unsafe IPC guidance remains active.

## Planning Correction 7.4b2a1: Lifecycle Handoff

The decomposition checker is an allowed adjacent file for both implementation
slices. It may change only to preserve the approved identifier, owner,
disposition, lifecycle, and next-slice contracts as dispositions are accepted.
It cannot weaken semantic gates, remove fixture requirements, or admit partial
disposition states.

The valid checked states are:

1. both slices `Planned`, no F018 dispositions, next slice `7.4b2b`;
2. `7.4b2b` `Accepted`, its four dispositions complete, `7.4b2c` `Planned`,
   next slice `7.4b2c`; or
3. both slices `Accepted`, all fourteen dispositions complete, and neither
   completed slice remains next.

The correction slice may touch only this report, the F018 decomposition
checker, the active plan, and execution ledger. It changes no normative owner,
frozen-ID proposal, fixture contract, objective, or implementation order.

## Slice 7.4b2b: Runtime-Decoding Proof

**Allowed write set:**

- `topics/contracts.md`;
- `ARCHITECTURE-PATTERNS.md`;
- `evaluation/standards-effectiveness/fixtures/contracts/runtime-decoding-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-runtime-decoding-policy.sh`;
- `evaluation/standards-effectiveness/verify-milestone-7-f018-decomposition.sh`
  for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No IPC profile, Security source, router, language profile, reference recipe,
generated inventory, template, or downstream repository belongs to this slice.

**Required semantics:**

- unknown boundary input becomes a validated value only through an executable
  decoder or smart constructor that checks every invariant required by that
  value;
- successful parsing, deserialization, shape inspection, or type assertion
  alone does not establish validity;
- a decoder returns a validated value or a typed `invalid`, `unsupported`, or
  `unavailable` diagnostic;
- normalization and defaulting are part of the decoder contract and cannot
  silently discard invalid input;
- trusted in-process values that never cross an applicable boundary do not
  acquire a redundant runtime-decoding requirement; and
- missing runtime proof cannot fall back to a cast, alternate unchecked shape,
  permissive default, or the original untrusted object.

**Focused evidence:**

`runtime-decoding-decisions.tsv` must cover trusted in-process values, valid
unknown input, malformed shape, assertion-only conversion, incomplete
validation, unsupported contract versions, unavailable decoders, normalization
failure, and successful construction of a validated value.

**Acceptance gate:** The generic Contracts owner states the runtime-proof
contract, `STD-0051`-`STD-0054` have exact final dispositions, the direct
request assertion is removed, the legacy section links to Contracts without
competing rules, and focused plus affected global regressions pass.

## Slice 7.4b2c: Action-Specific IPC Decoding

**Allowed write set:**

- `profiles/boundaries/ipc.md` (new canonical IPC profile);
- `topics/security.md`;
- `ARCHITECTURE-PATTERNS.md`;
- `SECURITY-STANDARDS.md`;
- `STANDARDS-ROUTER.md`;
- `README.md`;
- `evaluation/standards-effectiveness/fixtures/ipc/action-payload-decisions.tsv`;
- `evaluation/standards-effectiveness/verify-ipc-payload-validation.sh`;
- `evaluation/standards-effectiveness/verify-milestone-7-f018-decomposition.sh`
  for lifecycle/disposition handoff only;
- consolidation dispositions, evaluation README, findings, active plan, and
  execution ledger.

No language profile, transport implementation, schema-library recipe,
generated inventory, template, lockfile, or downstream repository belongs to
this slice.

**Required semantics:**

- decode the envelope and the category/action discriminant before dispatch;
- select the schema from the complete supported category/action pair;
- validate every action-specific payload field and applicable metadata before
  constructing that action's validated message type;
- unknown supported-shape actions return typed `unsupported`; malformed
  envelopes or recognized actions with invalid payloads return typed `invalid`;
- inability to obtain required decoding capability returns typed `unavailable`;
- dispatch accepts only validated variants and performs no payload assertions;
- producer-side typing never substitutes for consumer-side trust-boundary
  decoding; and
- no default action, fall-through handler, generic `ValidatedMessage` cast,
  payload cast, or alternate permissive decoder acts as fallback.

The profile may describe discriminated unions and decoder registries, but it
must not mandate a language, validation library, transport, or product message
catalog.

**Focused evidence:**

`action-payload-decisions.tsv` must cover valid actions from at least two
categories, malformed envelopes, unknown categories/actions, mismatched
category/action pairs, missing and wrong-type payload fields, extra-field
policy, invalid correlation metadata, producer-only typing, envelope-only
validation, unavailable schemas, and dispatch of validated variants.

**Acceptance gate:** Finding `F018` is resolved; all fourteen planned
identifiers have exact final dispositions; the IPC profile and Security topic
route deterministically with valid metadata; all unsafe message/request casts
are removed from active and legacy guidance; typed decision fixtures and all
affected regressions pass.

## No-Fallback And Legacy Rule

The implementation slices replace unsafe guidance in place. Legacy documents
may retain concise migration links, but not validated-type casts, unchecked
dispatch, duplicate decoder policy, compatibility schemas, permissive unknown
actions, or alternate execution paths. An unresolved decoder decision produces
a typed diagnostic.

## Re-Plan Triggers

- A validated-value constructor cannot be separated from a language-specific
  type-system mechanism without losing the generic contract.
- IPC applicability requires a new boundary role or precedence rule.
- A frozen section must split across owners in a way the disposition ledger
  cannot represent unambiguously.
- Removing the unsafe examples requires files outside the approved slice.
- Verification cannot distinguish full action-specific decoding from
  envelope-only checks or assertion-based proof.
- Existing canonical Security or Contracts guidance conflicts with the required
  typed outcomes.
