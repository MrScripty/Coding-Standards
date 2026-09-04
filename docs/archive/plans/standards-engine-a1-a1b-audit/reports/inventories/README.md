# Architecture Inventory Method

The audit compares four immutable source trees:

| Label | Commit | Purpose |
| --- | --- | --- |
| `a1-v9-accepted` | `2359a98740b6035a0414bfaf5427ceaa1301a1c8` | Exact implementation accepted as original A1 |
| `a1-v10-accepted` | `7bc8bd070f882eb9779dc678139777d05a6ce7c7` | Exact accepted policy-impact-v2 runtime amendment |
| `a1b-plan-base` | `36dd75790b2f08a6e66624ccae4f8530bc111a92` | Accepted A1b planning/standards base before A1b runtime work |
| `a1b-accepted` | `84412f22fa9fe082f089eaa347c30c23f185ffee` | Exact implementation later accepted as A1b |

The two A1 runtime observations prevent policy-impact-v2 changes made after A1
acceptance from being counted as A1b design growth. The separate planning base
captures later standards, policy-graph, suite, and test posture without calling
that repository state another independently accepted A1 runtime.

To reproduce, export each commit into a separate temporary directory with
`git archive`, then run:

```text
python3 architecture_metrics.py \
  a1-v9-accepted /path/to/a1-v9-accepted \
  a1-v10-accepted /path/to/a1-v10-accepted \
  a1b-plan-base /path/to/a1b-plan-base \
  a1b-accepted /path/to/a1b-accepted
```

The script counts physical Python lines and files, AST function/class/test
definitions, package-root `__all__` exports, unique production import edges
between the selected packages, canonical schema lines/definitions, registered
declarative suites, and retained `verify-*.sh` files. Generated contract code
is included in production totals and also reported separately.

These measures are diagnostic observations, not verdicts. In particular:

- an import edge records dependency direction but not its semantic cost;
- a public export records Interface breadth but not how often it is used;
- a test-function count does not show necessity, overlap, or oracle quality;
- AST test-function counts omit dynamically generated cases and therefore do
  not supersede the accepted reports' executed-run totals;
- a line count mixes generated and handwritten code unless the separate
  generated-contract observation is considered; and
- the three revisions do not promise identical behavior or guarantees.

The architecture report combines this inventory with source inspection and
representative change-history analysis before drawing conclusions about Depth,
Leverage, Locality, or deletion opportunities.
