"""Synchronous MCP stdio transport for the generated Engine interface.

Only lifecycle, ping, and tools are supported. Requests execute serially;
durable Engine handles, rather than transport sessions, carry domain state.
"""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from copy import deepcopy
import json
from pathlib import Path
import sys
import traceback
from typing import TextIO

from tools.standards_contracts.standards_contracts import CompiledContracts

from .tools import AgentToolFacade
from .compiled_cache import CompiledSnapshotCache
from .runtime_identity import RuntimeIdentity
from .context_projection import Purpose, qualified_operations


PROTOCOL_VERSION = "2025-11-25"
READ_ONLY_OPERATIONS = frozenset(
    {
        "read_many",
        "workflow_status",
        "workflow_details",
        "runtime_info",
        "resume",
        "find_snapshots",
        "find_proposals",
        "query",
        "query_proposal",
        "preview_application",
        "inspect",
    }
)
FOCUSED_OPERATIONS = frozenset(
    {
        "route",
        "read",
        "read_many",
        "related",
        "routing_facts",
        "inspect",
        "query_proposal",
        "preview_application",
        "propose",
        "revise",
        "analyze",
        "resolve_workflow",
        "resolve_many",
        "review",
        "apply",
        "recover",
        "workflow_status",
        "workflow_details",
        "runtime_info",
        "resume",
    }
)
# These inputs contain nested authoring variants that supported clients may
# abbreviate as `unknown` even after reference expansion. Preserve the exact
# input contract in description text, which is visible independently of their
# type renderer. This is generated documentation, never a second validator.
INPUT_CONTRACT_DESCRIPTIONS = frozenset({"propose", "revise", "resolve_workflow"})
DESCRIPTIONS = {
    "runtime_info": "Inspect this running interface, catalog and installation identity without opening the standards store. Supply expected_catalog to compare the client catalog. Restart and reconnect after implementation replacement; refresh tools when only the client catalog differs.",
    "resolve_many": "Record 1–128 explicit decisions bound to one exact Analysis context. Each decision retains its ordinary evidence and authorization checks; the final state is recorded atomically. A rejected batch records no decisions. Arguments are limited to 256 KiB. Compact results are default; use workflow_details for pending work.",
    "workflow_details": "Read a live Analysis section in pages of 1–16 records (default 8, up to 64 KiB per page). Follow the exact next arguments; observation bindings detect evidence changes between pages. Detail reads do not decide or publish.",
    "read_many": "Read 1–32 selected items from one explicit snapshot in request order. Each item accepts the single-read options. The complete JSON result is limited to 2 MiB; a failed item rejects the whole request. Use the snapshot returned by route or read.",
    "propose": "Create a proposal from explicit change intent and immediately analyze it. Reuse returned context. Omit snapshot to capture accepted authority. Stops at missing evidence or decisions; never reviews or applies automatically.",
    "revise": "Revise the exact proposal referenced by context and analyze the new revision. Supply an atomic change set. Stale contexts cannot select a newer head implicitly.",
    "analyze": "Analyze the exact draft context and return pending requirements or complete analysis with a new context.",
    "resolve_workflow": "Supply one actual evidence or owner-decision submission for pending workflow context. Return the new immutable context and Engine-derived continuations.",
    "review": "Explicitly accept complete analysis using three evidence-backed review decisions. Requires user authorization. Returns readiness as context, without applying.",
    "apply": "Explicitly verify and locally publish the exact accepted workflow context. Requires user authorization. Recovery-required continues only through recover; never retry an interrupted apply.",
    "recover": "Use observe to inspect the original admitted application, or explicitly select complete-publication to revalidate and publish that same candidate. Preserve the original readiness and current recovery authority.",
    "workflow_status": "Reconstruct the exact workflow context and legal continuations from durable Engine records. Does not select newer revisions or perform mutation.",
    "resume": "Explicitly select the current revision of the proposal identified by context. Returns a draft context; analysis is a separate next action. Recovery-required must be recovered first.",
    "routing_facts": "Discover snapshot-bound registered routing facts, meanings, types, allowed values, nullability and aliases. Supply known facts to route; missing facts remain unknown. Omit snapshot to capture new accepted authority.",
    "route": "Route explicit registered facts to applicable standards and required closure. Omit snapshot to capture new accepted authority; reuse the returned snapshot for subsequent calls. Preserve unresolved questions.",
    "read": "Read exact authoritative policy by canonical ID. Compact detail preserves text and essential authority; full detail includes all relationship rows. Omit snapshot to capture new authority or supply an exact returned snapshot. For navigation authoring, target navigation-indexes to discover registered entrypoint handles, then read a returned navigation ID for its exact content. Navigation results carry authority and are not normative policy.",
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
    "query_proposal": "Read, route, or traverse authoring content within an exact immutable proposal revision. Use preview_application to inspect its qualified application view.",
    "preview_application": "Inspect an exact unpublished revision through the ordinary application qualification and filtering rules. Supply one read, route, or related request. Results and continuations stay bound to the draft; this operation neither publishes content nor approves review or exposure.",
    "analyze_proposal": "Analyze an exact proposal revision and return unresolved consequences or complete analysis.",
    "review_proposal": "Accept complete current proposal analysis with explicit evidence-backed review decisions; return content-bound readiness. Requires user authorization for review.",
    "verify_proposal": "Verify the exact proposal candidate. Coverage audits require readiness. Verification does not supply review decisions or publish.",
    "apply_proposal": "Verify and publish the exact accepted readiness to the local canonical ref. Requires user authorization for application. On recovery-required use recover_application with the same readiness; never retry apply. Does not push a remote.",
    "recover_application": "Observe the original admitted application or explicitly authorize complete-publication after revalidation. Preserve the selected readiness and application identity.",
    "verify_repository": "Verify the working tree. Refreshing generated verification inputs is a mutation; inspect verification.passed.",
    "maintain_evidence": "Maintain the accepted repository evidence catalog at an exact revision. For draft-only consumers use register-consumer in propose/revise with separate policy relationships. This operation does not edit a proposal or certify coverage.",
}


APPLICATION_DESCRIPTIONS = {
    "runtime_info": DESCRIPTIONS["runtime_info"],
    "read_many": "Read 1–32 selected reviewed items from one explicit snapshot in order. Each item supplies target and optional detail. The complete JSON result is limited to 2 MiB; an unavailable item rejects the whole request.",
    "route": "Select applicable guidance from registered facts and a complete qualified dependency closure. Reuse the returned snapshot.",
    "read": "Read a reviewed standard, example, or operational aid by identity. Full detail adds permitted relationships.",
    "related": "Discover selected relationships among qualified guidance and examples in one snapshot.",
    "routing_facts": "Read the reviewed vocabulary for routing a task. Supply known facts and retain unresolved conditions.",
    "query": "Route, read, or traverse qualified guidance within the supplied snapshot.",
    "inspect": "Inspect a permitted policy or relationship handle within its captured snapshot.",
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


def tool_catalog(
    root: Path, *, purpose: Purpose | str, advanced: bool = False,
    interface: CompiledContracts | None = None,
) -> list[dict]:
    # Discovery and invocation share the same installed schema authority.
    selected = interface if interface is not None else AgentToolFacade.load_interface(root)
    contract = selected.project().agent_tools
    definitions = contract["$defs"]
    result = []
    purpose = Purpose(purpose)
    for operation in qualified_operations(contract, purpose):
        name = operation["id"]
        if not advanced and name not in FOCUSED_OPERATIONS:
            continue
        description = APPLICATION_DESCRIPTIONS[name] if purpose is Purpose.APPLICATION else DESCRIPTIONS[name]
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
                "annotations": {"readOnlyHint": purpose is Purpose.APPLICATION or name in READ_ONLY_OPERATIONS},
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
    def __init__(self, code: int, message: str, data: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


class MCPServer:
    def __init__(self, root: Path, *, purpose: Purpose | str, advanced: bool = False) -> None:
        self.root = root.resolve()
        self._purpose = Purpose(purpose)
        self.advanced = advanced
        self._interface = AgentToolFacade.load_interface(self.root)
        self.tools = tool_catalog(
            self.root, purpose=self.purpose, advanced=advanced, interface=self._interface
        )
        self.names = {tool["name"] for tool in self.tools}
        self._runtime_identity = RuntimeIdentity(self.root, self.purpose, self._interface, self.tools)
        self._compiled_cache = CompiledSnapshotCache(self.root, self.purpose)
        self._closed = False
        self.initialized = False
        self.ready = False

    @property
    def purpose(self) -> Purpose:
        return self._purpose

    def close(self) -> None:
        """Release only process-owned pure resources; each call closes its store."""
        self._compiled_cache.close()
        self._interface = None
        self._runtime_identity = None
        self.tools.clear()
        self.names.clear()
        self._closed = True

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
                "error": {"code": error.code, "message": str(error),
                          **({"data": error.data} if error.data is not None else {})},
            }

    def _request(self, method: str, params: dict) -> dict:
        if self._closed:
            raise ProtocolError(-32000, "The server is closed.")
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
                "serverInfo": {"name": "standards-engine", "version": self._runtime_identity.implementation_version},
                "_meta": {"standards-engine/runtime": self._runtime_identity.metadata()},
                "instructions": f"Installed interface {self._interface.interface.interface_schema_version}; purpose {self.purpose.value}. " + (
                    "Use route and read to obtain applicable guidance. Reuse returned snapshots for consistent observations."
                    if self.purpose is Purpose.APPLICATION else
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
            return {"tools": deepcopy(self.tools),
                    "_meta": {"standards-engine/runtime": self._runtime_identity.metadata()}}
        if method != "tools/call":
            raise ProtocolError(-32601, "Method not found.")
        name = params.get("name")
        if not isinstance(name, str) or name not in self.names:
            raise ProtocolError(-32602, "Tool unavailable in this running catalog; inspect runtime_info and refresh tools or restart/reconnect after an upgrade.",
                                self._runtime_identity.metadata())
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            raise ProtocolError(-32602, "Tool arguments must be an object.")
        if name == "runtime_info":
            value = self._runtime_identity.invoke(arguments)
            return self._tool_result(value)
        try:
            # Opening per call matches the reference transport and avoids keeping
            # store state alive across idle client sessions. No operation retries.
            with redirect_stdout(sys.stderr):
                with AgentToolFacade.open_repository(
                    self.root, purpose=self.purpose, interface=self._interface,
                    compiled_cache=self._compiled_cache,
                ) as facade:
                    value = getattr(facade, name)(arguments)
        except Exception as error:
            if self.purpose is Purpose.APPLICATION:
                print(
                    f"Application invocation failed: {type(error).__name__}",
                    file=sys.stderr,
                )
                return {"isError": True, "content": [{"type": "text", "text": "Application observation is unavailable; operator diagnostics retain the failure."}]}
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
        return self._tool_result(value)

    def _tool_result(self, value: dict) -> dict:
        return {
            "_meta": {"standards-engine/runtime": self._runtime_identity.metadata()},
            "structuredContent": value,
            "content": [{"type": "text", "text": json.dumps(value)}],
            "isError": value.get("kind") in {"rejected-result", "application-rejected-result", "candidate-application-rejected-result"}
            or value.get("status") == "rejected",
        }


def serve(server: MCPServer, source: TextIO, destination: TextIO) -> None:
    try:
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
    finally:
        server.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Serve Standards Engine tools over MCP stdio."
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--purpose", choices=[value.value for value in Purpose], required=True)
    parser.add_argument(
        "--advanced",
        action="store_true",
        help="Expose additional operations within the configured purpose.",
    )
    arguments = parser.parse_args()
    serve(
        MCPServer(arguments.repo_root, purpose=arguments.purpose, advanced=arguments.advanced),
        sys.stdin,
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
