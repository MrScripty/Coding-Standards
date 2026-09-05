"""Run the real-client workflow walkthrough in a separate MCP SDK environment.

Invoke from the repository root with PYTHONPATH=. and the client environment's
Python. The Engine subprocess uses --engine-python and its locked dependencies.
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

from tools.standards_engine.tests.test_agent_workflow import (
    ROOT,
    decisions,
    evidence,
    prepare_repository,
    reference_change,
)


async def walkthrough(engine_python, pending_only=False):
    with tempfile.TemporaryDirectory(
        prefix="standards-mcp-workflow-client-"
    ) as temporary:
        repo = Path(temporary) / "repository"
        prepare_repository(repo)
        interrupted_server = Path(temporary) / "interrupted_server.py"
        interrupted_server.write_text("""from unittest.mock import patch
from tools.standards_engine.standards_engine.authoring import AuthoringModule
from tools.standards_engine.standards_engine.mcp import main
from tools.standards_snapshots.standards_snapshots import SnapshotError, SnapshotFailure
error = SnapshotError(SnapshotFailure("unavailable", "SNAPSHOT_STORE.FIXTURE_INTERRUPTION", "Fixture interrupted outcome recording after publication"))
with patch.object(AuthoringModule, "record_applied", side_effect=error):
    raise SystemExit(main())
""")

        def parameters(interrupted=False):
            launch = (
                [str(interrupted_server)]
                if interrupted
                else ["-m", "tools.standards_engine.standards_engine.mcp"]
            )
            return StdioServerParameters(
                command=engine_python,
                args=["-P", *launch, "--repo-root", str(repo)],
                env={**os.environ, "PYTHONPATH": str(ROOT)},
            )

        calls = []

        async def call(client, name, arguments, *, error=False):
            result = await client.call_tool(name, arguments)
            calls.append(name)
            assert bool(result.isError) == error, result
            assert result.structuredContent is not None, result
            return result.structuredContent

        async with stdio_client(parameters(True)) as streams:
            async with ClientSession(
                *streams, read_timeout_seconds=timedelta(seconds=600)
            ) as client:
                await client.initialize()
                tools = await client.list_tools()
                names = {t.name for t in tools.tools}
                assert "query" not in names and "apply" in names
                if pending_only:
                    change = reference_change(repo, "client-pending")
                    change["edits"][0]["standard"].update(
                        id="topic.agent-client-fixture", role="topic", level="MUST"
                    )
                    pending = await call(client, "propose", {"change_set": change})
                    assert pending["status"] == "needs-action", pending
                    obligation = pending["outcome"]["obligations"][0]
                    await call(
                        client,
                        "review",
                        {"context": pending["context"], "decisions": decisions(repo)},
                        error=True,
                    )
                    submission = {
                        "kind": "impact-disposition",
                        "obligation": obligation["handle"],
                        "fingerprint": obligation["fingerprint"],
                        "result": "confirmed",
                        "rationale": "The isolated standalone fixture module's new normative scope is explicitly acknowledged by the test owner.",
                        "evidence": [evidence(repo)],
                    }
                    resolved = await call(
                        client,
                        "resolve_workflow",
                        {"context": pending["context"], "submission": submission},
                    )
                    assert resolved["status"] == "complete", resolved
                    assert resolved["context"] != pending["context"]
                    return {
                        "scenario": "pending decision",
                        "calls": calls,
                        "explicit_resolution": True,
                        "incomplete_review_refused": True,
                    }
                proposed = await call(
                    client,
                    "propose",
                    {"change_set": reference_change(repo, "client-published")},
                )
                assert proposed["status"] == "complete"
                assert proposed["context"]["kind"] == "analysis-handle"
                initial_context = proposed["context"]
                ready = await call(
                    client,
                    "review",
                    {"context": initial_context, "decisions": decisions(repo)},
                )
                assert ready["status"] == "ready"
                context = ready["context"]
                assert context["kind"] == "readiness-handle"
                before = (
                    subprocess.check_output(
                        ["git", "-C", str(repo), "rev-parse", "main"]
                    )
                    .decode()
                    .strip()
                )
                applied = await call(client, "apply", {"context": context})
                assert applied["status"] == "recovery-required", applied
                assert (
                    applied["outcome"]["code"]
                    == "APPLICATION.OUTCOME_PERSISTENCE_UNAVAILABLE"
                ), applied
                assert [n["operation"] for n in applied["next_operations"]] == [
                    "recover"
                ]
                refused = await call(client, "apply", {"context": context}, error=True)
                assert refused["code"] == "WORKFLOW.OPERATION_NOT_AVAILABLE"
                selected = (
                    subprocess.check_output(
                        ["git", "-C", str(repo), "rev-parse", "main"]
                    )
                    .decode()
                    .strip()
                )
                assert selected != before
        async with stdio_client(parameters()) as streams:
            async with ClientSession(
                *streams, read_timeout_seconds=timedelta(seconds=600)
            ) as client:
                await client.initialize()
                observed = await call(client, "workflow_status", {"context": context})
                assert observed["status"] == "recovery-required"
                assert observed["context"] == context
                recovered = await call(client, "recover", {"context": context})
                assert recovered["status"] == "applied", recovered
                assert recovered["next_operations"] == []
                assert (
                    subprocess.check_output(
                        ["git", "-C", str(repo), "rev-parse", "main"]
                    )
                    .decode()
                    .strip()
                    == selected
                )
                result = await call(
                    client, "read", {"target": "reference.testing.client-published"}
                )
                assert (
                    "This is an isolated workflow test reference." in result["content"]
                )
                # A fresh proposal and an interleaved revision prove that resuming
                # old contexts cannot silently retarget their reviewed subject.
                old = await call(
                    client,
                    "propose",
                    {"change_set": reference_change(repo, "client-stale")},
                )
                revised = await call(
                    client,
                    "revise",
                    {
                        "context": old["context"],
                        "change_set": reference_change(
                            repo, "client-stale", revision=True
                        ),
                    },
                )
                stale = await call(
                    client, "workflow_status", {"context": old["context"]}
                )
                assert stale["status"] == "stale"
                assert stale["revision"] == old["revision"]
                await call(
                    client,
                    "review",
                    {"context": old["context"], "decisions": decisions(repo)},
                    error=True,
                )
                resumed = await call(client, "resume", {"context": old["context"]})
                assert (
                    resumed["revision"] == revised["revision"]
                    and resumed["status"] == "draft"
                )
                analyzed = await call(
                    client, "analyze", {"context": resumed["context"]}
                )
                assert analyzed["context"] == revised["context"]
                ready_again = await call(
                    client,
                    "review",
                    {"context": analyzed["context"], "decisions": decisions(repo)},
                )
                normal = await call(
                    client, "apply", {"context": ready_again["context"]}
                )
                assert normal["status"] == "applied", normal
                assert normal["outcome"]["kind"] == "apply-proposal-result"
                readback = await call(
                    client, "read", {"target": "reference.testing.client-stale"}
                )
                assert "Revised fixture text." in readback["content"]

        return {
            "client": "official MCP Python SDK",
            "focused_tools": len(names),
            "calls": calls,
            "context_identities": 1,
            "proposal_and_analysis_calls": 1,
            "explicit_review": True,
            "verified_local_publication": True,
            "normal_apply_success": True,
            "interrupted_outcome": True,
            "retry_refused": True,
            "cold_process_recovery": True,
            "recovery_did_not_publish": True,
            "accepted_text_readback": True,
            "stale_context_rejected": True,
            "resume_explicit": True,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-python", required=True)
    parser.add_argument("--pending-only", action="store_true")
    arguments = parser.parse_args()
    print(
        json.dumps(
            asyncio.run(walkthrough(arguments.engine_python, arguments.pending_only)),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
