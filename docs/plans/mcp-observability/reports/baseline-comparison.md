# Synthetic baseline/candidate comparison

Baseline: `188beda1fa477d21d576c233dd8c7f4c4c267d23`, extracted with `git archive` into an isolated temporary directory. Candidate: reviewed source hashes in [independent review](independent-review.md). Python3.12.14; SQLite3.53.1; locked dependency versions matched. No model/client session or real interaction log was collected.

Each cold process received initialize, initialized notification, tools/list, describe_input(runtime_info), an invalid runtime_info request, a valid runtime_info request and ping. Six requests, one notification, three tool calls, six replies;688 sent stdio bytes. The operator recorder created only temporary synthetic databases, removed after the comparison.

| Purpose | Output schemas | Baseline bytes | Candidate off | Candidate on | Replies equal |
| --- | --- | ---: | ---: | ---: | --- |
| authoring | eager | 753498 | 753498 | 753498 | yes |
| authoring | on-demand | 115030 | 115030 | 115030 | yes |
| application | eager | 89041 | 89041 | 89041 | yes |
| application | on-demand | 22115 | 22115 | 22115 | yes |

Comparison parsed every reply, including schema catalog, typed rejection, text content and runtime observations. Only process UUID and implementation digest were normalized: these must differ for distinct loaded sources/processes. Full JSON response byte totals matched without normalization. No tools, protocol messages, operation retries or domain results were added.

One sample per configuration is outcome/byte preservation evidence, not a latency benchmark. Observed cold process times ranged from882.27ms to1393.69ms with other tests active. No throughput/overhead, token or billing claim is made.

Reproduction: extract the named baseline with git archive; start the baseline MCP and candidate MCP with --purpose authoring/application and --output-schemas eager/on-demand. Send the seven listed JSON-RPC messages, compare parsed replies after replacing instance_id/implementation_digest (including JSON text blocks), and count UTF-8 bytes of the actual stdio streams. Repeat the candidate with --observe-database pointing at a fresh private temporary path and --observe-deployment synthetic-comparison.
