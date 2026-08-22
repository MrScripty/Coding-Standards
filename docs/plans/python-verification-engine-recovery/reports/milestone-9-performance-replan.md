# Milestone 9 Performance Re-Plan

## Trigger

Milestone 9 began from clean accepted revision
`689e6a37ef7a1c3868e0247bd3f634f8900c7822`. One discarded warm-up and seven
serial current samples produced:

| Workload | Median seconds | Range seconds | Provisional limit | Result |
| --- | ---: | ---: | ---: | --- |
| list | 0.138470 | 0.136239–0.142827 | 0.250 | within limit |
| focused | 0.186642 | 0.179059–0.191389 | 0.250 | within limit |
| all declarative | 1.536975 | 1.514586–1.589918 | 1.500 | re-plan required |
| generated evidence | 1.059976 | 1.016715–1.073427 | 1.500 | within limit |

Every all-suite sample exceeded its provisional historical limit. Complete
sampling stopped before execution so the limit could not be silently revised or
the implementation fitted to an unexplained number.

## Accepted Consumer Requirement

The Python-engine recovery plan owns a `2.000` second local all-declarative
integration-feedback requirement on the representative environment. This is a
maintainer-selected consumer limit: running every registered declarative suite
must remain a sub-two-second feedback operation. It is not derived from suite
count, the current median, or an implementation detail.

The current median consumes approximately 77 percent of that requirement. No
consumer impact or fault-isolation evidence justifies adding caching, parallel
execution, partial validation, or another performance mechanism. The list,
focused, generated-evidence, and complete limits remain unchanged.

## Authorized Continuation

Milestone 9 may continue with:

1. three serial complete-workload samples;
2. median and range comparison against the existing `150.000` second local
   wave-checkpoint requirement;
3. current performance and recovery acceptance evidence; and
4. all remaining broad recovery gates.

Re-plan again if any complete sample exceeds its limit, a workload fails, the
repository changes during sampling, or final evidence requires implementation
work rather than measurement and plan projection.
