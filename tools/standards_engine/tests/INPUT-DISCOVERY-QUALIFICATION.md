# Input discovery qualification

There are separate evidence boundaries. Keep their results distinct.

## Automated contract and workflow evidence

Run in the supported locked environment from the repository root:

```sh
PYTHONPATH=. python -m unittest tools.standards_engine.tests.test_input_discovery tools.standards_engine.tests.test_discovered_workflow tools.standards_engine.tests.test_model_discovery_qualification
PYTHONPATH=. python -m tools.standards_contracts.standards_contracts.projection --check
```

The first suite reconstructs every published input closure through the actual tool
and validates it independently. The second uses discovered schemas to validate real
fixture authoring requests and proves shared/inline decisions preserve authority.
The third tests the fail-closed qualification checker with synthetic events; those
events are **not** client/model acceptance evidence. Existing raw-Codex navigation
checks now exercise discovery too, but still have no model turn.

## Real model-visible qualification

Use the operator's supported locked Python environment and authenticated Codex.
Select the actual model and client execution surface. This opt-in command uses the
configured model service and may incur usage. It makes a private fixture clone,
registers a uniquely named local MCP server only for that app-server process, and
starts an ephemeral model thread in an empty directory. It does not change user
Codex configuration or authorize changes in the source repository.

```sh
PYTHONPATH=. /path/to/locked/python -m tools.standards_engine.tests.codex_discovery_client \
  --allow-model-turn \
  --model YOUR_SUPPORTED_MODEL \
  --surface YOUR_ACTUAL_CLIENT_SURFACE \
  --schema-mode native \
  --evidence-dir /new/private/path/discovery-qualification
```

Use `--codex-config KEY=VALUE` only for explicit supported client settings needed
to select the intended execution surface or disable other MCP servers. The harness
refuses to start the model turn while another MCP server exposes tools; run-owned
fixture settings take precedence over supplied overrides. The surface label is recorded as an
operator request, not inferred from a raw catalog. Record the actual effective
surface and capture the model-visible declaration when the client exposes it;
attach that observation to acceptance. The harness uses the ordinary app-server
thread and MCP tools path, not a manually posted authoring request.

The task supplies semantic intent and a real fixture evidence reference. It does
not supply argument-schema examples or generated call payloads. The model must
use describe_input for all five authoring operations, create and revise a test
proposal, resolve one decision and then a multiple-decision batch, reuse evidence,
and explicitly review to readiness. The harness validates observed model-authored
arguments/results, requires every used definition to have been retrieved before
its action (unrelated union choices need not be read), checks exact sequence and failures, reads back the requested
fixture content independently, and confirms main was not published. It rejects
filesystem, web, unrelated tools, missing or unknown event surfaces, schema-repair
calls and agent self-reported success as substitutes for observed behavior.

Events and results are preserved in `events.jsonl`, `qualification.json`, task.txt,
readback JSON and stderr.log. These are private operator artifacts; review them for
sensitive context before sharing. The fixture repository is retained for inspection;
its disposal is an explicit operator action. Preserve active production stores.
An unsupported app-server/event format or missing executable yields unavailable
qualification rather than a pass. There is no elapsed-time deadline for active work;
shutdown escalation applies only after completion, failure or operator cancellation.

## Acceptance record

Record client version, requested and observed execution surface, model, Engine
interface and runtime/catalog identity, trace location, exact readback, tool counts,
argument-repair failures and request/result byte measurements. Repeat representative
ordinary navigation when the client surface changes. Record model token measurements
only when the client actually exposes them; JSON bytes are not billing savings.

A status of passed in qualification.json is behavioral evidence for that one
fixture/client run. It is not editorial review, a universal client certification,
or proof that TypeScript declarations no longer contain unknown. Operator review
must confirm the requested exposure surface and absence of outside schema sources.
Compatibility removal requires an accepted direct or discovery path for every
supported deployment (or explicit retirement of that deployment), plus integration
review. Full schemas reaching the client are insufficient on their own.
