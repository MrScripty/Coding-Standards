# Release Maintenance And Recovery

**Standards metadata**

- ID: `workflow.release.operations`
- Role: `workflow`
- Level: `MUST`
- Applies when: A change selects maintenance channels, publication presentation, or release recovery procedures.
- Does not apply when: No maintenance channel, publication presentation, or release recovery procedure changes.
- Requires: `workflow.release`
- Specializes: `none`
- Verification: Focused decision fixtures and affected boundary evidence for the rules below.
- Canonical owner: `workflows/release/operations.md`

## Maintenance And Channels

For each release unit that promises post-publication support, define a
maintenance contract before making that promise:

- the supported release lines and their immutable source lineage;
- the fixes, compatibility obligations, and response classes in scope;
- who may start, extend, or end support;
- the support window or explicit end condition;
- how a fix reaches every affected supported line and relevant successor line;
  and
- the release channel through which consumers receive the result.

A standard release has no intrinsic branch, tag, maintenance duration, or
support class. Trunk-only maintenance, release branches, signed references,
registry revisions, and other source-selection mechanisms are project-owned
implementations of the maintenance contract.

When correcting a supported release, identify every affected release line,
select an accepted immutable source for each line, apply and verify the change
under that line's contract, and publish a new artifact identity. Reconcile the
fix into relevant successor lines or record an explicit reason why it does not
apply. Do not mutate published bytes or silently omit an affected supported
line.

Long-term support is an explicit support class, not a property inferred from a
branch name or release age. Its contract names scope, duration or end
condition, compatibility and security commitments, source lineage, delivery
channels, and responsible authority. If those facts are absent, return a typed
release-maintenance diagnostic rather than claiming maintenance or long-term
support.

A release channel is a consumer contract, not a branch, tag, version-like
string, or deployment environment. Define its audience, stability and
compatibility expectations, admission and promotion criteria, update and
discovery behavior, retention and support policy, withdrawal or rollback
behavior, and artifact identity rules.

Prerelease identifiers and channels are independent decisions. Promotion may
reuse accepted bytes only when the destination channel accepts the same
artifact identity and evidence; otherwise produce and verify a new planned
artifact. If the channel or promotion decision is unresolved, return a typed
release-channel diagnostic and do not silently publish to a default channel.

Feature flags and runtime activation controls do not define release channels.
When a product can deploy code separately from activating behavior, govern
that mechanism through an explicit project-owned configuration and lifecycle
policy rather than inferring it from the release process.
## Publication Presentation

A publication surface presents an accepted release to consumers. It does not
own versioning, channels, artifact identity, compatibility, or acceptance
decisions. Before publication, define:

- the destination and release channel;
- the responsible publication authority;
- any private, staged, review, public, or withdrawn visibility states;
- the accepted release notes and required disclosures;
- how planned artifacts and their relationships are presented; and
- how consumers discover, select, verify, and report problems with the release.

Enter a draft or review state only when the destination supports it and the
accepted publication procedure requires it. A provider feature or manual
review is not a universal release gate. Publication may proceed only from the
canonical pipeline handoff with the authority required for the selected
destination and visibility transition.

Derive prerelease presentation from the accepted version and channel
contracts. Major version zero does not by itself make a publication a
prerelease. Provider labels are projections of the canonical decision and
cannot redefine it.

Release notes derive from the accepted changelog, migration obligations,
support policy, and required security or operational disclosures. Generated
summaries may supplement that material when they are accurate, but cannot
replace required curated content or invent unaccepted claims.

Present the exact artifact identities and relationships from the artifact
plan. Give consumers enough target, format, and compatibility context to select
the correct artifact, and place each selected integrity, signature,
provenance, or dependency document where its relationship to the final bytes
is unambiguous. Provider layout and grouping may improve discovery but must not
create a second artifact identity scheme.

If destination, authority, visibility, notes, channel projection, or artifact
presentation is unresolved, return a typed release-publication diagnostic and
do not publish using a provider default.
## Recovery And Withdrawal

Plan recovery for each publication destination and channel before relying on a
generic rollback claim. Published artifacts may be immutable, cached,
installed, mirrored, or consumed offline, so reversal can require one or more
distinct actions:

- stop further distribution or promotion;
- mark, yank, withdraw, or deprecate an affected artifact when supported;
- notify affected consumers and operators;
- contain active harm through an authorized operational control;
- publish a corrected or superseding release; and
- restore or migrate affected state under its persistence contract.

Start recovery when accepted evidence or observed impact invalidates a required
release claim, creates unacceptable security or safety exposure, corrupts
artifacts or state, or violates the release's support and channel contracts.
Classify affected release units, versions, channels, consumers, artifacts, and
persisted state before selecting actions.

Use only transitions supported by the destination and contract. Do not describe
withdrawal as erasure when consumers may retain bytes, mutate a published
artifact in place, reuse an immutable version or artifact identity for
different bytes, or assume every registry supports unpublishing. When reversal
is unavailable, contain distribution where possible, communicate the status,
and publish a newly identified correction or superseding decision.

The recovery contract names normal and emergency authorities, required
approvals, credential scope, notification owners, and any actions permitted
before broader review. Urgency does not grant implicit authority. If immediate
action is necessary, record the acting authority, evidence, scope, and
follow-up obligations.

Verify each recovery action against its intended effect. A replacement release
must satisfy its own version, contract, artifact, behavior, and publication
claims; recovery status cannot waive normal acceptance. Reconcile corrections
across every affected supported release line.

Record the incident, consumer impact, actions, residual exposure, and prevention
decision in the durable artifact selected by documentation policy. A changelog
or release note is appropriate only when it communicates a consumer-relevant
change; it is not a universal post-incident record.

If affected scope, channel capability, authority, safe action, or replacement
evidence is unresolved, return a typed release-recovery diagnostic and preserve
the known incident state rather than claiming rollback success.
