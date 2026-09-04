# Milestone 4 Unique Proposal Review

## Scope

The review covers the exact 12 `codex/m6-u*-proposal` branches retained after
mapped-ref cleanup. Each branch has one unique commit. This slice inspected
their contents and accepted successors without deleting or rewriting refs.

## Findings

Every proposal has the same bounded shape:

- add one declarative verifier suite;
- remove that suite's legacy Bash checker; and
- prepare, but not integrate, a migration proposal.

For every proposal, current accepted `main` has exactly one later commit that
touches the same suite and checker as an accepted migration. Current repository
state confirms that the suite exists, the suite registry includes it, the Bash
checker is absent, and the accepted transition commit is an ancestor of
`main`.

The [exact disposition table](../inventories/unique-proposal-dispositions.tsv)
records each source branch and commit, proposed artifacts, superseding commit,
current artifact state, terminal classification, and cleanup disposition.

## Terminal Classification

All 12 branches are `superseded`. Their objectives were satisfied by later
accepted implementations, but their exact patches differ from accepted
history. They are not integrated or patch-equivalent replacements, and this
review does not relabel them as such.

No branch has an upstream, matching `origin` ref, active checkout, or declared
long-lived purpose. Retaining them solely as historical evidence conflicts with
the branch lifecycle policy because durable review evidence now records their
purpose and supersession.

## Re-Plan Trigger

Each branch is the last ref reaching one unique, unaccepted commit. Deleting a
branch would therefore permanently retire that proposal from ordinary ref
reachability. Canonical Commit policy requires separate explicit destructive
authority naming the branch and unique commit, confirming it is not accepted,
shared, or required, and recording recovery or permanent retirement.

That authority is not inferred from age, branch naming, supersession, or the
user's earlier mapped-ref decision. All 12 refs remain protected until a new
decision explicitly chooses one of these outcomes.

## Verification

- unique branches reviewed: 12;
- unique commits reviewed: 12;
- exact accepted transition commits: 12;
- current suites present and registered: 12;
- legacy Bash checkers absent: 12;
- ambiguous superseding transitions: 0;
- ref mutations during review: 0.
