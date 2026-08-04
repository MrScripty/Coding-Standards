# Milestone 7 Row 32 Persistence Decomposition

## Owner Contract

Create `profiles/boundaries/persistence.md` for durable read/write, transaction,
publication, migration application, version-ledger, and store mutation
mechanisms. Contracts selects supported states and evolution; Resilience owns
recovery; Concurrency owns overlapping access; Security owns authorization;
Build owns generated artifacts; Diagnostics owns reporting; Verification owns
evidence.

Persistence does not own every in-memory mutation or mandate a database,
transaction, migration format, startup execution, version table, rollback
mechanism, compatibility window, or implementation phase sequence.

## Exact Ownership

- `STD-0106` is an index created with the owner.
- `STD-0107`, `STD-0108`, `STD-0110`, and `STD-0111` refine durable mutation;
  `STD-0109` is an index; `STD-0112` splits policy from reference mechanisms.
- `STD-0113` is an index; `STD-0114`, `STD-0115`, and `STD-0118` refine
  migration execution; `STD-0116` and `STD-0117` split policy from SQL, naming,
  ledger-schema, and startup-loop examples.

## Ordered Children

1. `32.1`: create and route the useful Persistence profile, recipe boundary,
   owner evidence, and `STD-0106` index.
2. `32.2`: migrate `STD-0107` through `STD-0112` durable mutation and extract
   fixed phases and pseudocode without placeholder or debug-only defaults.
3. `32.3`: migrate `STD-0113` through `STD-0118` migration execution, extract
   SQL/file/startup mechanisms, replace duplicate Architecture policy with
   indexes, and close row 32.

Shared routing, metadata, dispositions, plan, and ledger remain serial. Each
child may additionally touch only its owner/reference section, legacy section,
focused fixtures/checker, decomposition validation, and cursor assertions.

## Typed Outcomes And No Fallback

Missing authority, source/destination state, durable invariant, store
capability, ledger, coordination, or evidence is `unavailable`; partial
authoritative publication, contradictory ledger/state, corrupt state, or
incomplete proof is `invalid`; unsupported versions or required mechanisms are
`unsupported`.

Do not fall back to partial writes, temporary invalid authoritative state,
debug-only validation, deletion, rebuild, guessed migration order, repeated
application, startup execution, default rollback, additive-is-safe, or
speculative coexistence.

## Re-plan Triggers

Stop if implementation requires generic in-memory ownership, a fixed store or
migration framework, recovery or compatibility authority transfer, multiple
dispositions per identifier, a fourth semantic child, or files outside the
approved write set.
