# Milestone 4 Horizon V2 Coverage Audit

## Authority

- Base commit: `50043a5bd2b2c7b1ea15c8a54e2eef34873cfbe9`
- Review capability: `standards.review.audit`
- Reviewer provenance:
  `user-authorized:horizon-v2-reading-authority-classification`
- Conclusion: `complete`

The reviewer directed one final attestation renewal after the complete proposed
horizon was frozen. This report is the referenced audit evidence for that
renewal.

## Horizon Comparison

| State | Provider version | Digest |
| --- | ---: | --- |
| Accepted base | 1 | `sha256:e735b6b6f37b8107058eae2924660ba0d5695266282117a076033c0ec96d0c46` |
| Coarse full-manifest intermediate | 1 | `sha256:25d152f20cfc205eb87e521e5a68d432a3ef303e227cb7d59729c83852771de9` |
| Final typed projection | 2 | `sha256:35ed5271ffb9573eb1ae4dd6949debd9f6aad011bb9d0b43dbbfba9eb5b077e9` |

The final horizon contains 856 members. The complete node catalog remains an
`AnalysisSnapshot` input. Horizon version 2 removes only
`nodes[].metadata.authority` from the catalog's coverage fingerprint and
retains every other current or future field.

## Structural Disposition

- Catalog node count: 27 before and after.
- Node IDs, aliases, and repository paths: unchanged.
- Classification additions: five `projection`, 22 `evidence`.
- Catalog groups and edges: unchanged.
- Compiled policy-impact relationships: 126 before and after.
- Compiled relationship semantics: unchanged.
- Policy semantic revisions: unchanged.

| Node | Classification | Disposition |
| --- | --- | --- |
| `prompts/full-codebase-standards-refactor.md` | `projection` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `prompts/implement-plan.md` | `projection` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `prompts/planning.md` | `projection` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `templates/PLAN-TEMPLATE.md` | `projection` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/commit/authority.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/commit/hook-bypass.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/commit/branch-lifecycle.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/commit/task-worktree-terminal.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/verification-guide.md` | `projection` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/implementation/plan-entrypoint-decisions.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/planning/admission-decisions.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/planning/concurrent-integration-applicability.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/planning/concurrent-integration-outcomes.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/planning/consolidation-decisions.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/planning/full-review-prompt-decisions.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/planning/template-projection-decisions.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `evaluation/standards-effectiveness/fixtures/planning/work-slice-proportionality.tsv` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `concurrent-plan-integration` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `full-review-prompt-entrypoint` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `plan-implementation-entrypoint` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `plan-template-projection` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `planning-admission` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `planning-consolidation` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `policy-semantic-impact` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `s1-routing` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `commit-consolidation-dispositions` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |
| `release-maintenance-policy` | `evidence` | Existing identity, aliases, path, and graph incidence unchanged; reading classification added. |

## Exact Requirements

### Commit

| Policy unit | Requirement |
| --- | --- |
| `workflow.commit.per-commit-boundary` | `coverage-requirement:sha256:dcc8df7ec9ca3a2852c78e81992d5541dde5bb0c60878f38f857eeec7cfa0766` |
| `workflow.commit.isolation-applicability` | `coverage-requirement:sha256:17073b2008f31da2d1b25c415476bd7d83e4422fb7f79d83944c8f8d82bbcf75` |
| `workflow.commit.branch-context` | `coverage-requirement:sha256:ffac4de725a11b04e83b8e3902fe654f0604070da163b590013582818afbd117` |
| `workflow.commit.integration-mechanisms` | `coverage-requirement:sha256:af329caa341a0c81ea1c30d0bf0e0c91cf9a78cd43a5dfea367050433100284d` |
| `workflow.commit.cherry-pick-lineage` | `coverage-requirement:sha256:8a82aa19bbed266f0e620b1a41a5d010f389becbf24c4a6e710023436367a542` |
| `workflow.commit.terminal-branch-lifecycle` | `coverage-requirement:sha256:cd01cf37137ae72048bd9ea6769ea1bb295467e6bfd4966926c2bf0eae52a372` |
| `workflow.commit.worktree-lifecycle` | `coverage-requirement:sha256:6329316eba862b145adf40f0de394f64e992ee7ce4854660c2165a0d6d1ee761` |
| `workflow.commit.branch-history-review` | `coverage-requirement:sha256:bfb77c291e2fa476ee936826af34226fa1e630a242619e15d8eab38668e87a95` |
| `workflow.commit.hook-bypass-authority` | `coverage-requirement:sha256:dbe9759a59bec26ea9129e84aeb1e271b231c8f26547025b6478080c219c871d` |
| `workflow.commit.rewrite-authority` | `coverage-requirement:sha256:0973dd50ff218f143a09b66ed247f943d38886ec0ce297cc9eba77accf9b6778` |
| `workflow.commit.topology` | `coverage-requirement:sha256:e90c69831d9bcd94d747c20ef0dc239805aa698f02a1be0903981754e3d74daa` |
| `workflow.commit.commit-message` | `coverage-requirement:sha256:cba9b2e2c7efa5fa9b19813154bbb654e674ee64f8f0309cb37a49f373b4ff9c` |
| `workflow.commit.invalid-outcomes` | `coverage-requirement:sha256:67c4a1d1ae958be74309b5a2b04389b612d27d014ea1cf58f6b8fe193fe95c76` |

### Planning

| Policy unit | Requirement |
| --- | --- |
| `workflow.planning.written-plan-applicability` | `coverage-requirement:sha256:5c2b01c95c98cee8e87c8aec30d497f4ab1ea78d9fbf11420a128f2893f667ce` |
| `workflow.planning.artifact-model` | `coverage-requirement:sha256:cb53bb0a99d8702b202d47d8f5d396c6fecce3388430ac78b8ea5146e8af3c47` |
| `workflow.planning.active-plan-fields` | `coverage-requirement:sha256:05ef4b1d1e0ac33078b19b085c9e9f1e08dd893ca6bd335c3d4117d934745363` |
| `workflow.planning.lifecycle` | `coverage-requirement:sha256:8f24e30804adadfdddc56154fe240f78c3bc33654ffc083a872c6e5b8994dc79` |
| `workflow.planning.plan-admission` | `coverage-requirement:sha256:32b8bb619fa8db00f206f95b2e98d73e3becec3b96259d68bb19644bc539891c` |
| `workflow.planning.concurrent-integration-routing` | `coverage-requirement:sha256:2497a0d4eddcc8da4327656e5f55119b04ceb058dc7926b31e1603a0272aca0c` |
| `workflow.planning.repository-isolation` | `coverage-requirement:sha256:e9e2b4c204e3ad6bb2b51fcff1cd191d9202a2ed6af616096252053e380805fa` |
| `workflow.planning.projection-completeness` | `coverage-requirement:sha256:757280755de382a471111f6eb355dc8f1d94033d903281edb3fe60d6634da73a` |
| `workflow.planning.acceptance-claims` | `coverage-requirement:sha256:c25c9107721a3af5bec22254f7ea872ea58af937356fb06aea930d9841708244` |
| `workflow.planning.milestones-and-slices` | `coverage-requirement:sha256:741b0af7768d9ebec4a0e8a066f088ce0c1f9307d2d8483ae355c3f35943db7d` |
| `workflow.planning.current-state` | `coverage-requirement:sha256:221ef10d09916ad01cc67479c7626372fef3b104f9ebe5bedc1eed6477ca300e` |
| `workflow.planning.replanning` | `coverage-requirement:sha256:653c30208749f2a7ff0f447c87fee48c0c0d7ace642a351650ffe7ff30dd5983` |
| `workflow.planning.findings` | `coverage-requirement:sha256:96d5d208a0136aa9c312dde71e39a4120f7b2a209cc787b7412cc78fc24c0137` |
| `workflow.planning.concurrent-work` | `coverage-requirement:sha256:e65477fd68662fc92af741852061f92f296c0e8a69362beb480e1461e1d562fb` |
| `workflow.planning.completion` | `coverage-requirement:sha256:51ef94620130eec55db2a69f9edb66261c2d745684f0265fb8f0f1fe792cc884` |

## Disposition

The final provider-v2 horizon was reviewed as complete for all 28 listed
subjects. No additional consumer relationship was identified. The exact
requirements may receive renewed `complete` attestations citing this report.
