# Standards implementation status — 2026-09-04

This is a nonnormative implementation record. The proposed standards changes below are not applied or accepted.

The audit and evidence were committed as `a72105c8`. A snapshot path-ordering defect was reproduced, fixed, and committed as `7cf8a884`; all 23 snapshot tests pass. Reopening a store and capturing identical nested paths under a different source revision now succeeds in the regression test.

## Saved proposal

The Engine accepted the following proposal against the audit snapshot. Its base predates the two commits above, so this proposal is reviewable draft work, not publishable against current main.

```json
{
  "kind": "create-proposal-result",
  "proposal": {
    "id": "proposal:v1:d52fe315-169c-47b7-bc66-e08afdc6540b",
    "kind": "proposal-handle",
    "schema_version": 1
  },
  "revision": {
    "id": "proposal-revision:sha256:03463ad8e1eed41e6468396632f598de8850cf3a0da3e37a351e7ae41bdd7752",
    "kind": "proposal-revision-handle",
    "schema_version": 1
  }
}
```

## Blocking authoring limitations

1. Creating a current snapshot returns `SUITE_INPUT.STALE_FILE` with no next operations. The snapshot fix changes two registered file digests; the audit commit also changes the repository index. The repository generator can compute the correct projection, but the Engine cannot bootstrap past its stale-input check to refresh it through a proposal. No generated projection was changed directly.
2. The public change-set edit variants have no routing fact/rule operation. Changing Requires or policy-impact relationships does not implement conditional Router selection. F01 and the selective-reading part of F03 need an Engine operation or an explicit authoring exception.
3. The saved draft has a `pending-result` from Analysis and still needs consumer-impact review, current-base recreation, full verification, and application. This record does not accept outstanding downstream pilots.

The authoring constraint is in [.agents/skills/standards-engine/SKILL.md](../../.agents/skills/standards-engine/SKILL.md): “The Engine is the sole writer of standards Markdown, metadata, supplementary projections, SQLite state, and local Git publication.”

## Initial changes

### topic.dependencies

Requires: `core`, `workflow.verification`.

Dependency selection and maintenance apply without publication. Select Release only when the task changes publication or acquisition behavior (audit F02).

### workflow.tooling

Requires: `core`, `workflow.implementation`, `workflow.verification`.

Tool selection and configuration apply without history mutation. Select Commit for commit and history operations (audit F02).

### profile.language.rust.security

```diff
--- accepted/profile.language.rust.security
+++ proposed/profile.language.rust.security
@@ -1,6 +1,6 @@
 ## Panic And Recoverable Error Boundary
 
-Apply the [Rust API error policy](../../../languages/rust/RUST-API-STANDARDS.md#result-option-panic)
+Apply the [Rust API error policy](api.md#failure-expression-mechanisms)
 to public and internal fallible Rust operations. This profile specializes that
 policy for production request paths, lifecycle code, background services, and
 network handlers: recoverable errors must remain typed results and must not be

```

### core

```diff
--- accepted/core
+++ proposed/core
@@ -1,5 +1,37 @@
 These are the universal invariants. Load additional guidance through
 [STANDARDS-ROUTER.md](STANDARDS-ROUTER.md), not by reading the entire library.
+
+## Reading And Applying These Standards
+
+Read Core, then use the Router to select the workflows, topics, and profiles
+that match the task. Requires means an unconditional prerequisite; Specializes
+identifies a refinement of a broader concept. A related link is a route to
+additional guidance when its stated condition applies, not a request to read
+all descendants.
+
+MUST states an obligation within its applicability. SHOULD is the recommended
+starting point; depart when a concrete project constraint justifies it.
+Profiles refine shared obligations for a technology or boundary. References
+provide examples and explanation rather than additional requirements.
+
+Apply governing external requirements and explicit project public contracts,
+persisted contracts, and accepted architectural decisions first, then Core,
+applicable profile mechanisms, and selected workflows and topics. A profile
+cannot silently weaken the generic obligation it specializes. Identify an
+actual conflict and obtain an explicit, owned, justified exception; do not
+claim that an overridden obligation was satisfied.
+
+When a standard asks for a contract or decision, start from the existing code,
+accepted design, tool configuration, and consumer requirements. For routine
+reversible choices, use a suitable established convention and explain a
+material departure. Record reasoning in proportion to the consequence; an
+ordinary local choice does not require a separate approval or design document.
+
+A developer who lacks material facts should state the missing fact and its
+consequence in ordinary prose and continue independent work. References to
+invalid, unsupported, or unavailable do not require production error variants
+for development uncertainty. Machine interfaces use their declared diagnostic
+contract; production behavior uses the owning domain's failure contract.
 
 ## Objective And Scope
 
@@ -173,8 +205,10 @@
 
 ## Verification
 
-- Add the smallest test that fails for the defect or missing behavior before or
-  with its implementation.
+- For a behavior change or defect, add a focused regression test before or
+  with the implementation when existing evidence does not already prove the
+  property. A construction proof or existing test can suffice when it covers
+  the actual risk; explain material limits.
 - Run focused checks for the changed behavior and affected static/toolchain
   contracts.
 - Use integration, contract, system, user-workflow, environment-gated, and

```

### topic.security

```diff
--- accepted/topic.security
+++ proposed/topic.security
@@ -1,3 +1,40 @@
+## Identity And Permission
+
+At a protected operation, distinguish valid input, authenticated identity, and
+permission to perform the requested action on the requested resource. A valid
+identifier or an authenticated caller does not prove authorization. Enforce
+permission at the trusted boundary before disclosing data or performing the
+effect, including tenant and ownership constraints. Deny access unless the
+applicable policy permits it; do not rely on a hidden UI control or an earlier
+unrelated authorization check. Test forbidden actions, cross-owner and
+cross-tenant access where relevant, and revoked or expired authority.
+
+## Sensitive Data And Credentials
+
+Identify sensitive fields and the owners allowed to receive them. Minimize
+collection, retention, and disclosure across responses, logs, traces, caches,
+and diagnostic artifacts. Redact before exporting diagnostics; return bounded
+public failure information while preserving useful restricted diagnostics.
+Keep secrets out of source control and ordinary logs. Supply credentials
+through the deployment's secret mechanism with the narrowest required access,
+and define rotation and revocation for long-lived credentials.
+
+For network paths carrying sensitive data or credentials, use an established
+secure transport with peer verification. Use maintained cryptographic
+implementations and the platform's secure randomness and key storage rather
+than custom cryptography. Select algorithms and configuration against the
+actual threat model and supported platform requirements.
+
+## Dependency And Build Trust
+
+Treat downloaded packages, build tools, generated artifacts, and CI extensions
+as executable trust decisions. Select their source and identity explicitly,
+verify the integrity or provenance required by the distribution contract, and
+restrict the credentials and authority available to them. Keep untrusted
+contribution jobs away from publication secrets. Own vulnerability triage and
+remediation across the supported lifecycle; a clean scan alone does not prove
+trustworthiness. Dependencies and Build own the corresponding procedures.
+
 ## Untrusted Structured Input
 
 Decode untrusted structured input through the complete contract required by the

```

Proposed applicability: A change affects untrusted input, protected resources, identity, authorization, sensitive data, credentials, cryptography, secure transport, executable dependency trust, or network listeners.

Proposed exclusion: No trust boundary, protected operation, sensitive data, credential, cryptographic, dependency trust, or listener behavior is affected.

### topic.architecture.immutable-authority-closure

Semantic revision 2 → 3. Scope immutable closure to promised immutable results and replay; permit explicit live inspection and preserve current access revocation independently of historical result identity (audit F09).

```diff
--- accepted/topic.architecture.immutable-authority-closure
+++ proposed/topic.architecture.immutable-authority-closure
@@ -1,7 +1,8 @@
-An immutable, replayable, or inspectable handle binds the complete transitive
-authority closure required to reproduce every result advertised from that
-handle. The closure includes each authority, contract, provider input, and
-authorization view whose value can affect the result, referenced through an
+A handle that promises an immutable result or replay binds the complete
+transitive authority closure needed to reproduce that promised result. A live
+inspection handle may observe current state when its contract says so;
+inspectability alone does not promise replay. The closure includes each authority, contract, provider input, and
+historical authorization input whose value determines the captured result, referenced through an
 exact immutable identity.
 
 Derive that closure from the handle's advertised operations, result semantics,
@@ -19,11 +20,16 @@
 ability to name a field or serialize a record is not evidence that another
 authority object is required.
 
-Resolution cannot depend on ambient mutable state, an instance-local cache,
-the originating process, undeclared providers, fresh authorization, or a live
-filesystem or service read that is not itself bound into the closure. Derived
+Reconstruction of the promised result cannot depend on ambient mutable state,
+an instance-local cache, the originating process, undeclared providers, or a
+live filesystem or service read that is not itself bound into the closure. Derived
 results may be cached, but cache availability and process history cannot change
 their meaning.
+
+Current permission to access or disclose a captured result remains a separate
+security decision. Check it when the access contract requires it, and deny
+revoked access without changing the captured content or substituting a newer
+result. Historical permission is an input to replay, not a continuing grant.
 
 Persistence owns reopening through real store adapters, and Contracts owns
 handle representation and version behavior. If any required authority cannot

```

## Prepared verification refresh

Computed with the repository generator into a temporary file; not written to the canonical projection. The index digest must be recomputed if additional files are committed.

```diff
--- evaluation/standards-effectiveness/generated/suite-inputs.json
+++ candidate
@@ -20441,7 +20441,7 @@
       ]
     },
     {
-      "digest": "sha256:7644f46f89796980698c5c06e397bd7f8adbbea720e453fd3dfef6e2dd62a4ca",
+      "digest": "sha256:9fb28637faadcc55f8842efaa367c9488c5470f076de265bbdf0e08446b56521",
       "path": "tools/standards_snapshots/standards_snapshots/store.py",
       "state": "present",
       "uses": [
@@ -20463,7 +20463,7 @@
       ]
     },
     {
-      "digest": "sha256:ea1de9c24115379fd616490d9d705c6aa570495c668071e23aeb1b6a93501ef3",
+      "digest": "sha256:1e584da33a550a390a1a255171f1c8a2a3cca3a151b389b66a8b78f580d0634b",
       "path": "tools/standards_snapshots/tests/test_module.py",
       "state": "present",
       "uses": [
@@ -24624,7 +24624,7 @@
     "path": "evaluation/standards-effectiveness/suite-registry.toml"
   },
   "repository_index": {
-    "digest": "sha256:9da22b7e2ac54d98c1549170036cf3e0cadd2a0b6337132f49095a67490d9baa",
+    "digest": "sha256:0d3853e1349016344e729b261a6f9c1fc0176e496bfed615ed4ce0f7999fa2f0",
     "uses": [
       {
         "check": "python-package-contract",

```

## Analysis state

```json
{
  "kind": "pending-result",
  "handle": {
    "id": "analysis:sha256:1c48ce81306c12316e139cd4d6340a607d253be660715b64a851e9ba973f3b9f",
    "kind": "analysis-handle",
    "schema_version": 6
  },
  "pending_work": {
    "impact-disposition": 5,
    "consumer-disposition": 30,
    "coverage-attestation": 1
  }
}
```

No pending review obligation has been represented as resolved. Resume using the exact Engine handles above.
