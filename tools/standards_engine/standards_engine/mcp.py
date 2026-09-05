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
        "workflow_status",
        "resume",
        "find_snapshots",
        "find_proposals",
        "query",
        "query_proposal",
        "inspect",
    }
)
FOCUSED_OPERATIONS = frozenset(
    {
        "route",
        "read",
        "related",
        "routing_facts",
        "inspect",
        "query_proposal",
        "propose",
        "revise",
        "analyze",
        "resolve_workflow",
        "review",
        "apply",
        "recover",
        "workflow_status",
        "resume",
    }
)
# These inputs contain nested authoring variants that supported clients may
# abbreviate as `unknown` even after reference expansion. Preserve the exact
# input contract in description text, which is visible independently of their
# type renderer. This is generated documentation, never a second validator.
INPUT_CONTRACT_DESCRIPTIONS = frozenset({"propose", "revise", "resolve_workflow"})
DESCRIPTIONS = {
    "propose": "Create a proposal from explicit change intent and immediately analyze it. Reuse returned context. Omit snapshot to capture accepted authority. Stops at missing evidence or decisions; never reviews or applies automatically.",
    "revise": "Revise the exact proposal referenced by context and analyze the new revision. Supply an atomic change set. Stale contexts cannot select a newer head implicitly.",
    "analyze": "Analyze the exact draft context and return pending requirements or complete analysis with a new context.",
    "resolve_workflow": "Supply one actual evidence or owner-decision submission for pending workflow context. Return the new immutable context and Engine-derived continuations.",
    "review": "Explicitly accept complete analysis using three evidence-backed review decisions. Requires user authorization. Returns readiness as context, without applying.",
    "apply": "Explicitly verify and locally publish the exact accepted workflow context. Requires user authorization. Recovery-required continues only through recover; never retry an interrupted apply.",
    "recover": "Explicitly observe the application bound to readiness context after recovery-required. Requires current recovery authority. Never verifies, publishes, retries, or rolls back.",
    "workflow_status": "Reconstruct the exact workflow context and legal continuations from durable Engine records. Does not select newer revisions or perform mutation.",
    "resume": "Explicitly select the current revision of the proposal identified by context. Returns a draft context; analysis is a separate next action. Recovery-required must be recovered first.",
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


def tool_catalog(root: Path, *, advanced: bool = False) -> list[dict]:
    contract = json.loads((root / CONTRACT_PATH).read_text(encoding="utf-8"))
    definitions = contract["$defs"]
    result = []
    for operation in contract["operations"]:
        name = operation["id"]
        if not advanced and name not in FOCUSED_OPERATIONS:
            continue
        description = DESCRIPTIONS[name]
        if name in INPUT_CONTRACT_DESCRIPTIONS:
            schema = schema_closure(
                definitions[operation["input_definition"]], definitions
            )
            description += (
                "\n\nExact input contract (JSON Schema Draft 2020-12). "
                "Named definitions include all edit/evidence fields and recursive variants; "
                "use these fields when the client abbreviates its type declaration.\n"
                "```json\n"
                + json.dumps(schema, separators=(",", ":"), sort_keys=True)
                + "\n```"
            )
        result.append(
            {
                "name": name,
                "description": description,
                "annotations": {"readOnlyHint": name in READ_ONLY_OPERATIONS},
                "inputSchema": input_schema(
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


def input_schema(root: dict, definitions: dict) -> dict:
    """Expose input structure inline, retaining references only at recursion.

    Inline containing objects so client reference rendering is only needed at
    recursive expression fields. Validation keywords and the remaining reference
    closure retain their canonical semantics.
    """

    def expand(value, active=()):
        if isinstance(value, list):
            return [expand(item, active) for item in value]
        if not isinstance(value, dict):
            return value
        if "$ref" in value:
            reference = value["$ref"]
            if not reference.startswith("#/$defs/"):
                raise ValueError(f"Unsupported input schema reference: {reference}")
            name = reference.removeprefix("#/$defs/")
            if name in active:
                return value
            resolved = expand(definitions[name], (*active, name))
            siblings = {key: item for key, item in value.items() if key != "$ref"}
            if siblings:
                return {"allOf": [resolved, expand(siblings, active)]}
            return resolved
        return {key: expand(item, active) for key, item in value.items()}

    return schema_closure(expand(root), definitions)


class ProtocolError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


class MCPServer:
    def __init__(self, root: Path, *, advanced: bool = False) -> None:
        self.root = root.resolve()
        self.advanced = advanced
        self.tools = tool_catalog(self.root, advanced=advanced)
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
                "instructions": (
                    "Use explicit routing facts and preserve opaque handles. Follow typed Engine outcomes and next_operations. Standards mutations belong to the Engine. Recovery-required continues through recover with the same context, never an apply retry."
                    + (
                        " Native advanced operations use recover_application with readiness."
                        if self.advanced
                        else ""
                    )
                ),
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
                        "text": (
                            "Engine invocation failed; inspect server stderr. Outcome is unknown: do not automatically retry a mutation. "
                            + (
                                "For interrupted native application, use recover_application with the original readiness."
                                if name in ("apply_proposal", "recover_application")
                                else "For interrupted focused application, use workflow_status with the original context and follow its recovery continuation."
                            )
                        ),
                    }
                ],
            }
        return {
            "structuredContent": value,
            "content": [{"type": "text", "text": json.dumps(value)}],
            "isError": value.get("kind") == "rejected-result"
            or value.get("status") == "rejected",
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
    parser.add_argument(
        "--advanced",
        action="store_true",
        help="Expose the complete native and focused catalog.",
    )
    arguments = parser.parse_args()
    serve(
        MCPServer(arguments.repo_root, advanced=arguments.advanced),
        sys.stdin,
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
