# Milestone 4 Performance Claims And Baseline

## Measurement Contract

- Accepted revision: `de2289ad4c905c7bf9e0bba9a37da90955f4ce0a`.
- Runtime: CPython 3.12.3 on Linux 7.0.0-28-generic x86_64.
- Hardware: Intel Core Ultra 9 275HX, 24 cores, one thread per core.
- Repository state: clean canonical worktree with 207 registered declarative
  suites and 65 retained Bash checkers.
- Metric: subprocess wall-clock seconds measured with `time.perf_counter()`.
- Fast-workload sampling: one discarded warm-up followed by seven serial
  samples with output suppressed.
- Complete sampling: three serial samples with output suppressed.
- Variability rule: compare medians; reject a change when its median exceeds
  the workload budget or when an unexplained sample exceeds the budget.

## Claims And Baseline

| Workload | Consumer impact | Baseline seconds | Budget seconds | Decision |
| --- | --- | ---: | ---: | --- |
| `verify.py --list` | interactive suite discovery | median 0.191; range 0.188–0.199 | 0.250 | preserve registry validity; do not parse unrelated suite bodies |
| `verify.py --suite s1-routing` | focused developer feedback | median 0.198; range 0.196–0.202 | 0.250 | parse selected dependency closure only |
| `verify.py --all` | declarative integration gate | median 1.215; range 1.206–1.216 | 1.500 | retain complete strict suite validation |
| generated evidence check | migration artifact freshness | median 1.071; range 1.059–1.080 | 1.500 | retain current scans; no cache or snapshot layer |
| `verify.py --complete` | mixed wave/shared-contract checkpoint | median 128.647; range 128.244–131.777 | 150.000 | retained Bash dominates; do not attribute this claim to catalog loading |

The budgets are current local regression guards, not universal downstream
latency standards. A materially different repository scale or environment
requires a new claim-matched baseline.

## Post-Change Evidence

| Workload | Median seconds | Observed range | Baseline change | Result |
| --- | ---: | ---: | ---: | --- |
| list | 0.104 | 0.101–0.113 | -45.4% | within budget |
| focused | 0.111 | 0.110–0.119 | -43.8% | within budget |
| all declarative | 1.247 | 1.242–1.248 | +2.6% | within budget |
| generated evidence | 1.069 | 1.057–1.093 | -0.2% | within budget |
| complete checkpoint | approximately 116.5 | acceptance run | diagnostic comparison only | within budget |

All 353 verifier tests, 35 neutral graph tests, 207 declarative suites, generated
freshness checks, and the complete checkpoint with 65 retained Bash checkers
pass.

## Selected Implementation

Registry structure and dependency validity remain universal invocation
authority. Listing needs no suite bodies. Focused execution loads and validates
only selected suites and their dependency closure, so an unrelated malformed
suite cannot block focused feedback.

Checks that inspect assertion identities across suite boundaries must declare
that catalog-wide requirement. The engine then loads every suite body through
the same strict parser before executing that check. This preserves one catalog
authority without making catalog-wide validation the fallback for ordinary
focused execution.

## Rejected Optimizations

- A persistent cache adds invalidation and trust policy without a measured need.
- A shared repository snapshot adds orchestration complexity for a generated
  workload already below its accepted budget.
- Parallel complete execution would change retained-checker ordering and failure
  semantics while addressing temporary Bash work rather than the Python engine.

## 2026-08-21 Current Revalidation

The preceding baseline and post-change sections remain historical evidence for
their accepted revisions. Current revalidation used CPython 3.12.3 on Linux
7.0.0-28-generic x86_64 with an Intel Core Ultra 9 275HX, 24 cores, one thread
per core, 215 registered declarative suites, and 56 retained Bash checkers.

Fast workloads were measured at clean revision
`689e6a37ef7a1c3868e0247bd3f634f8900c7822` using one discarded warm-up and
seven serial samples. Complete workloads were measured after the docs-only
performance re-plan at clean revision
`48165cbab825262d67d508c8298e2eb87bdbb8a7`; verifier implementation authority
was unchanged.

| Workload | Samples | Median seconds | Range seconds | Owned limit | Result |
| --- | --- | ---: | ---: | ---: | --- |
| list | 0.138470, 0.138223, 0.141932, 0.136239, 0.142827, 0.137451, 0.139734 | 0.138470 | 0.136239–0.142827 | 0.250 | satisfied |
| focused | 0.179059, 0.189581, 0.183851, 0.179673, 0.191389, 0.186642, 0.187539 | 0.186642 | 0.179059–0.191389 | 0.250 | satisfied |
| all declarative | 1.514586, 1.577297, 1.548041, 1.589918, 1.536975, 1.520681, 1.518372 | 1.536975 | 1.514586–1.589918 | 2.000 | satisfied after accepted re-plan |
| generated evidence | 1.060778, 1.068213, 1.059976, 1.032949, 1.073427, 1.034856, 1.016715 | 1.059976 | 1.016715–1.073427 | 1.500 | satisfied |
| complete checkpoint | 133.538871, 133.469900, 130.958935 | 133.469900 | 130.958935–133.538871 | 150.000 | satisfied |

The plan owner selected the `2.000` second all-declarative limit as a local
sub-two-second integration-feedback requirement. It is not derived from the
current median or suite count. The other requirements retain their historical
consumer authority. No sample exceeds its owned limit, and the complete range
is stable. Current evidence does not justify caching, parallel execution,
partial validation, or another performance mechanism.
