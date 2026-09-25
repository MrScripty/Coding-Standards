"""Qualify registration using the actual MCP SDK and a disposable Git repository.

Run after committing the candidate and refreshing its verification inputs:
  PYTHONPATH=. CLIENT_PYTHON tools/standards_engine/tests/mcp_policy_registration_client.py \
    --engine-python /path/to/locked-engine-python --output /tmp/registration-result.json

The client environment uses the repository's existing MCP SDK qualification
setup. Fixture review decisions authorize only this temporary repository; the
user's installed store and blocked proposal are not opened by this harness.
"""
from __future__ import annotations

import argparse
import asyncio
from datetime import timedelta
import json
import os
from pathlib import Path
import subprocess
import tempfile

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tools.standards_engine.tests.test_agent_workflow import ROOT, evidence, prepare_repository


MODULE = "topic.registration-client"
FIRST = MODULE + ".first"
SECOND = MODULE + ".second"
CONSUMER = "reference.testing.registration-client"
PROVENANCE = "provenance.registration-client"
PRIVATE = "REGISTRATION_PRIVATE_REASON_83721"


def require(condition: bool, observed: object) -> None:
    if not condition:
        raise AssertionError(observed)


def owner(identity: str, *, reference: bool = False) -> dict[str, object]:
    return {"id": identity, "title": "Registration Client Fixture",
            "role": "reference" if reference else "topic",
            "level": "REFERENCE" if reference else "MUST",
            "applies_when": "The isolated registration fixture is selected.",
            "does_not_apply_when": "The fixture is outside the selected task.",
            "verification": "The actual MCP registration walkthrough observes publication.",
            "body": "## First Scope\n\nRetain the selected result.\n\n## Second Scope\n\nReview the next result.\n"}


def registration(identity: str, heading: str) -> dict[str, object]:
    return {"kind": "register-policy-unit", "standard": MODULE,
            "policy_unit": {"id": identity, "heading_chain": [heading],
                            "semantic_revision": 1, "intent": "Give the existing fixture scope a stable identity.",
                            "aliases": [], "predecessors": [], "successors": []}}


async def walkthrough(engine_python: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="standards-registration-mcp-") as temporary:
        repo = Path(temporary) / "repository"
        prepare_repository(repo)
        calls = []
        resolutions = []

        def parameters(purpose="authoring"):
            return StdioServerParameters(
                command=engine_python,
                args=["-P", "-m", "tools.standards_engine.standards_engine.mcp",
                      "--purpose", purpose, "--repo-root", str(repo)],
                env={**os.environ, "PYTHONPATH": str(ROOT)},
            )

        def change(edits):
            return {"purpose": {
                "summary": "Qualify existing-standard policy registration.",
                "rationale": "Exercise the real publication path in this disposable fixture only.",
                "evidence": [evidence(repo)],
            }, "edits": edits}

        async def call(client, name, arguments, *, error=False):
            if name in {"propose", "revise", "analyze", "resolve_workflow", "workflow_status", "resume"}:
                arguments = {"detail": "full", **arguments}
            result = await client.call_tool(name, arguments)
            calls.append(name)
            require(bool(result.isError) == error, result)
            require(result.structuredContent is not None, result)
            return result.structuredContent

        async def complete(client, proposed):
            seen = set()
            while proposed.get("status") == "needs-action":
                identity = json.dumps(proposed["context"], sort_keys=True)
                require(identity not in seen, proposed)
                seen.add(identity)
                outcome = proposed["outcome"]
                require(not outcome.get("fact_requirements"), outcome)
                operations = [item for item in outcome["next_operations"]
                              if item.get("operation") == "resolve"]
                require(bool(operations), outcome)
                selected = next((item for item in operations
                                 if item["request_kind"] == "consumer-disposition"), operations[0])
                kind = selected["request_kind"]
                resolutions.append(kind)
                if kind == "coverage-attestation":
                    submission = {"kind": kind, "claim": {
                        "requirement": selected["work"], "conclusion": "complete",
                        "evidence": [evidence(repo)], "explicit_exclusions": [],
                        "rationale": "The fixture owns the explicitly declared synthetic consumer horizon.",
                        "auditor_provenance": "Registration MCP test fixture; not a production standards audit.",
                    }}
                else:
                    require(kind in {"consumer-disposition", "impact-disposition"}, selected)
                    obligation = next(item for item in outcome["obligations"]
                                      if item["handle"] == selected["work"])
                    submission = {
                        "kind": kind, "obligation": selected["work"],
                        "result": "reviewed-no-change" if kind == "consumer-disposition" else "confirmed",
                        "fingerprint": obligation["fingerprint"],
                        "rationale": "Explicit fixture decision for this exact synthetic registration and consumer.",
                        "evidence": [evidence(repo)],
                    }
                proposed = await call(client, "resolve_workflow", {
                    "context": proposed["context"], "submission": submission,
                })
            require(proposed.get("status") == "complete", proposed)
            return proposed

        async def publish(client, proposed):
            completed = await complete(client, proposed)
            ready = await call(client, "review", {"context": completed["context"], "decisions": [
                {"owner": selected, "decision": "accept", "evidence": [evidence(repo)],
                 "rationale": "Accept this exact isolated registration fixture after its explicit dispositions."}
                for selected in ("consumer", "impact", "audit")
            ]})
            require(ready.get("status") == "ready", ready)
            applied = await call(client, "apply", {"context": ready["context"]})
            require(applied.get("status") == "applied", applied)
            return applied

        async with stdio_client(parameters()) as streams:
            async with ClientSession(*streams, read_timeout_seconds=timedelta(seconds=600)) as client:
                await client.initialize()
                catalog = await client.list_tools()
                propose_tool = next(tool for tool in catalog.tools if tool.name == "propose")
                require("register-policy-unit" in json.dumps(propose_tool.inputSchema), propose_tool)
                initial = []
                for identity, reference in ((MODULE, False), (CONSUMER, True)):
                    initial.append({"kind": "create-standard", "standard": owner(identity, reference=reference),
                                    "requires": [], "specializes": [], "policy_units": []})
                await publish(client, await call(client, "propose", {"change_set": change(initial)}))
                before = await call(client, "read", {"target": MODULE, "detail": "full"})
                historical_snapshot = before["snapshot"]
                first = await call(client, "propose", {"change_set": change([registration(FIRST, "First Scope")])})
                # Retain a real pending/current workflow, then replace the server.
                first_context, first_revision = first["context"], first["revision"]

        async with stdio_client(parameters()) as streams:
            async with ClientSession(*streams, read_timeout_seconds=timedelta(seconds=600)) as client:
                await client.initialize()
                resumed = await call(client, "workflow_status", {"context": first_context})
                require(resumed["revision"] == first_revision, resumed)
                await publish(client, resumed)
                after = await call(client, "read", {"target": MODULE, "detail": "full"})
                require(after["content"] == before["content"], after)
                first_policy = await call(client, "read", {"target": FIRST})
                require(first_policy["policy"]["scope"]["heading_path"] == ["First Scope"], first_policy)

                revised_owner = owner(MODULE)
                revised_owner["body"] = revised_owner["body"].replace("Second Scope", "Revised Second Scope")
                rewrite = {"kind": "revise-standard", "standard": revised_owner,
                           "scope_updates": [{"policy": FIRST, "heading_path": ["First Scope"],
                                              "semantics": {"kind": "preserve", "semantic_revision": 1,
                                                            "intent": "Preserve the registered first scope."}}]}
                association = {"kind": "put-policy-relationship", "relationship": {
                    "source_policy": SECOND, "consumer": CONSUMER, "relation": "reference-projection",
                    "applicability": {"operator": "always"}, "source_scope": None, "consumer_scope": None,
                    "evidence_owner": "review:consumer", "rationale": "The synthetic reference consumes this scope.",
                }}
                reason = {"kind": "put-provenance", "record": {
                    "id": PROVENANCE, "subject": SECOND, "origin": "current-justification",
                    "rationale": PRIVATE, "evidence": [evidence(repo)],
                }}
                second = await call(client, "propose", {"change_set": change([
                    association, reason, registration(SECOND, "Revised Second Scope"), rewrite,
                    {"kind": "approve-application-content", "target": MODULE},
                ])})
                before_failure = subprocess.check_output(["git", "rev-parse", "main"], cwd=repo)
                invalid = registration(MODULE + ".unavailable", "Missing Scope")
                await call(client, "revise", {"context": second["context"],
                                              "change_set": change([invalid])}, error=True)
                require(subprocess.check_output(["git", "rev-parse", "main"], cwd=repo) == before_failure,
                        "Rejected revision changed accepted main")
                status = await call(client, "workflow_status", {"context": second["context"]})
                require(status["revision"] == second["revision"], status)
                await publish(client, status)
                latest_snapshot = (await call(client, "read", {"target": SECOND}))["snapshot"]

        async with stdio_client(parameters()) as streams:
            async with ClientSession(*streams, read_timeout_seconds=timedelta(seconds=600)) as client:
                await client.initialize()
                current = await call(client, "read", {"snapshot": latest_snapshot, "target": SECOND, "detail": "full"})
                require(current["policy"]["scope"]["heading_path"] == ["Revised Second Scope"], current)
                require(any(item["source"] == SECOND and item["target"] == CONSUMER
                            for item in current["related"]), current)
                reason = await call(client, "read", {"snapshot": latest_snapshot, "target": PROVENANCE})
                require(reason["record"]["rationale"] == PRIVATE, reason)
                old = await call(client, "read", {"snapshot": historical_snapshot, "target": MODULE})
                require(old["content"] == before["content"], old)

        async with stdio_client(parameters("application")) as streams:
            async with ClientSession(*streams, read_timeout_seconds=timedelta(seconds=600)) as client:
                await client.initialize()
                current = await call(client, "read", {"target": SECOND, "detail": "full"})
                require(current["kind"] == "application-read-result", current)
                require("Revised Second Scope" in current["content"], current)
                require(PRIVATE not in json.dumps(current), current)
                await call(client, "read", {"target": PROVENANCE}, error=True)

        return {"status": "passed", "client": "official MCP Python SDK", "calls": calls,
                "resolutions": resolutions, "existing_unmapped_owner": True,
                "existing_populated_owner": True, "same_candidate_rewrite_and_relationship": True,
                "cold_pending_workflow": True, "cold_snapshot_readback": True,
                "rejected_revision_preserved_candidate": True, "application_provenance_isolation": True,
                "fixture_only": True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-python", required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    # The output is written only after every required observation succeeds.
    result = asyncio.run(walkthrough(arguments.engine_python))
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
