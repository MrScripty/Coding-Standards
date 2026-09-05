"""Synchronous MCP stdio transport for the generated Engine interface.

Only lifecycle, ping, and tools are supported. Requests execute serially;
durable Engine handles, rather than transport sessions, carry domain state.
"""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import sys
import traceback
from typing import TextIO

from .tools import AgentToolFacade


PROTOCOL_VERSION = "2025-11-25"
CONTRACT_PATH = "tools/standards_engine/contracts/generated/agent-tools.json"
READ_ONLY_OPERATIONS = frozenset(
    {
        "find_snapshots",
        "find_proposals",
        "query",
        "query_proposal",
        "inspect",
    }
)
DESCRIPTIONS = {
    "routing_facts": "Discover snapshot-bound registered routing facts, meanings, types, allowed values, nullability and aliases. Supply known facts to route; missing facts remain unknown. Omit snapshot to capture new accepted authority.",
    "route": "Route explicit registered facts to applicable standards and required closure. Omit snapshot to capture new accepted authority; reuse the returned snapshot for subsequent calls. Preserve unresolved questions.",
    "read": "Read exact authoritative policy by canonical ID. Compact detail preserves text and essential authority; full detail includes all relationship rows. Omit snapshot to capture new authority or supply an exact returned snapshot.",
    "related": "Traverse explicit permitted relationship groups against a supplied snapshot, or capture one when omitted. Preserve returned authoring-target handles.",
    "create_snapshot": "Capture canonical accepted standards for stable subsequent reads. Reuse the returned snapshot handle.",
    "find_snapshots": "Find durable snapshots to resume a standards workflow.",
    "delete_snapshot": "Delete a snapshot only for an explicitly requested lifecycle change.",
    "undelete_snapshot": "Restore an explicitly selected deleted snapshot.",
    "query": "Route explicit engineering facts to applicable standards and required closure, read authoritative policy by canonical ID, or traverse related policies within one snapshot. Read the router with include_routing to discover registered facts; do not infer missing facts.",
    "inspect": "Inspect a returned opaque handle for authoritative detail.",
    "prepare": "Analyze explicit changes between two accepted snapshots. For proposal authoring use analyze_proposal instead.",
    "resolve": "Submit actual evidence or an authorized owner decision for the current pending Analysis state. Follow returned next_operations.",
    "create_proposal": "Propose an atomic standards change with explicit domain intent and evidence against a snapshot.",
    "find_proposals": "Find durable proposals and their current revision handles.",
    "revise_proposal": "Append an atomic change to the exact expected proposal revision; stale revisions are rejected.",
    "query_proposal": "Read, route, or traverse standards within an exact immutable proposal revision.",
    "analyze_proposal": "Analyze an exact proposal revision and return unresolved consequences or complete analysis.",
    "review_proposal": "Accept complete current proposal analysis with explicit evidence-backed review decisions; return content-bound readiness. Requires user authorization for review.",
    "verify_proposal": "Verify the exact proposal candidate. Coverage audits require readiness. Verification does not supply review decisions or publish.",
    "apply_proposal": "Verify and publish the exact accepted readiness to the local canonical ref. Requires user authorization for application. On recovery-required use recover_application with the same readiness; never retry apply. Does not push a remote.",
    "recover_application": "Observe the durable application selected by readiness after recovery-required. Does not retry or publish; preserve the same readiness handle.",
    "verify_repository": "Verify the working tree. Refreshing generated verification inputs is a mutation; inspect verification.passed.",
    "maintain_evidence": "Preview or apply explicit evidence catalog maintenance with exact review evidence. Does not change normative standards or issue attestations.",
}


def schema_closure(root: dict, definitions: dict) -> dict:
    """Make a standalone schema containing only reachable local definitions."""
    selected: dict = {}

    def visit(value: object) -> None:
        if isinstance(value, dict):
            reference = value.get("$ref")
            if isinstance(reference, str) and reference.startswith("#/$defs/"):
                name = reference.removeprefix("#/$defs/")
                if name not in selected:
                    selected[name] = definitions[name]
                    visit(selected[name])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(root)
    return {**root, "$defs": selected}


def tool_catalog(root: Path) -> list[dict]:
    contract = json.loads((root / CONTRACT_PATH).read_text(encoding="utf-8"))
    definitions = contract["$defs"]
    result = []
    for operation in contract["operations"]:
        name = operation["id"]
        result.append(
            {
                "name": name,
                "description": DESCRIPTIONS[name],
                "annotations": {"readOnlyHint": name in READ_ONLY_OPERATIONS},
                "inputSchema": schema_closure(
                    definitions[operation["input_definition"]], definitions
                ),
                "outputSchema": schema_closure(
                    {
                        "type": "object",
                        "oneOf": [
                            {"$ref": f"#/$defs/{definition}"}
                            for definition in operation["result_definitions"]
                        ],
                    },
                    definitions,
                ),
            }
        )
    return result


class ProtocolError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


class MCPServer:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.tools = tool_catalog(self.root)
        self.names = {tool["name"] for tool in self.tools}
        self.initialized = False
        self.ready = False

    def dispatch(self, message: object) -> dict | None:
        identifier = None
        try:
            if not isinstance(message, dict):
                raise ProtocolError(-32600, "Expected a JSON-RPC request object.")
            identifier = message.get("id")
            if (
                message.get("jsonrpc") != "2.0"
                or not isinstance(message.get("method"), str)
                or (
                    "id" in message
                    and (
                        isinstance(identifier, bool)
                        or not isinstance(identifier, (str, int))
                    )
                )
            ):
                identifier = None
                raise ProtocolError(-32600, "Invalid JSON-RPC request.")
            method = message["method"]
            params = message.get("params", {})
            if "id" not in message:
                if method == "notifications/initialized" and self.initialized:
                    self.ready = True
                return None
            if not isinstance(params, dict):
                raise ProtocolError(-32602, "Parameters must be an object.")
            result = self._request(method, params)
            return {"jsonrpc": "2.0", "id": identifier, "result": result}
        except ProtocolError as error:
            return {
                "jsonrpc": "2.0",
                "id": identifier,
                "error": {"code": error.code, "message": str(error)},
            }

    def _request(self, method: str, params: dict) -> dict:
        if method == "ping":
            return {}
        if method == "initialize":
            if self.initialized:
                raise ProtocolError(-32600, "Session is already initialized.")
            if (
                not isinstance(params.get("protocolVersion"), str)
                or not isinstance(params.get("capabilities"), dict)
                or not isinstance(params.get("clientInfo"), dict)
            ):
                raise ProtocolError(-32602, "Missing initialization parameters.")
            self.initialized = True
            return {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "standards-engine", "version": "0.1.0"},
                "instructions": "Use explicit routing facts and preserve opaque handles. Follow typed Engine outcomes and next_operations. Standards mutations belong to the Engine. Recovery-required continues only through recover_application, never an apply retry.",
            }
        if not self.ready:
            raise ProtocolError(-32000, "Initialize the session before using tools.")
        if method == "tools/list":
            if "cursor" in params:
                raise ProtocolError(-32602, "This catalog has no continuation cursor.")
            return {"tools": self.tools}
        if method != "tools/call":
            raise ProtocolError(-32601, "Method not found.")
        name = params.get("name")
        if not isinstance(name, str) or name not in self.names:
            raise ProtocolError(-32602, "Unknown Standards Engine tool.")
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            raise ProtocolError(-32602, "Tool arguments must be an object.")
        try:
            # Opening per call matches the reference transport and avoids keeping
            # store state alive across idle client sessions. No operation retries.
            with redirect_stdout(sys.stderr):
                with AgentToolFacade.open_repository(self.root) as facade:
                    value = getattr(facade, name)(arguments)
        except Exception:
            traceback.print_exc(file=sys.stderr)
            return {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": "Engine invocation failed; inspect server stderr. Outcome is unknown: do not automatically retry a mutation. For interrupted application, use recover_application with the original readiness.",
                    }
                ],
            }
        return {
            "structuredContent": value,
            "content": [{"type": "text", "text": json.dumps(value)}],
            "isError": value.get("kind") == "rejected-result",
        }


def serve(server: MCPServer, source: TextIO, destination: TextIO) -> None:
    for line in source:
        try:
            message = json.loads(line)
        except (ValueError, RecursionError):
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Invalid JSON."},
            }
        else:
            response = server.dispatch(message)
        if response is not None:
            destination.write(json.dumps(response) + "\n")
            destination.flush()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Serve Standards Engine tools over MCP stdio."
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    serve(MCPServer(arguments.repo_root), sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
