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

from .tools import AgentToolFacade
from .compiled_cache import CompiledSnapshotCache
from .runtime_identity import RuntimeIdentity
from .input_discovery import InputContractDiscovery
from .context_projection import Purpose
from .mcp_catalog import SchemaMode, tool_catalog


PROTOCOL_VERSION = "2025-11-25"


class ProtocolError(Exception):
    def __init__(self, code: int, message: str, data: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


class MCPServer:
    def __init__(self, root: Path, *, purpose: Purpose | str, advanced: bool = False,
                 schema_mode: SchemaMode | str = SchemaMode.COMPATIBILITY) -> None:
        self.root = root.resolve()
        self._purpose = Purpose(purpose)
        self.advanced = advanced
        self.schema_mode = SchemaMode(schema_mode)
        self._interface = AgentToolFacade.load_interface(self.root)
        self.tools = tool_catalog(
            self._interface, purpose=self.purpose, advanced=advanced,
            schema_mode=self.schema_mode,
        )
        self.names = {tool["name"] for tool in self.tools}
        self._runtime_identity = RuntimeIdentity(self.root, self.purpose, self._interface, self.tools)
        self._input_discovery = InputContractDiscovery(
            self._interface, purpose=self.purpose, operation_names=self.names,
            catalog_digest=self._runtime_identity.metadata()["catalog_digest"],
        )
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
        self._input_discovery = None
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
                "instructions": f"Installed interface {self._interface.interface.interface_schema_version}; purpose {self.purpose.value}. "
                "Use describe_input for missing or abbreviated input shapes; retain its catalog-bound selections. " + (
                    "Use route with content={} to obtain applicable exact guidance; follow content.next for more. Reuse returned snapshots for consistent observations."
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
        if name == "describe_input":
            return self._tool_result(self._input_discovery.invoke(arguments))
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
            "isError": value.get("kind") in {"rejected-result", "application-rejected-result", "candidate-application-rejected-result", "input-contract-rejected-result"}
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
    parser.add_argument(
        "--schema-mode", choices=[mode.value for mode in SchemaMode],
        default=SchemaMode.COMPATIBILITY.value,
        help="Use compatibility rendering (default), or native reference schemas for a qualified client.",
    )
    arguments = parser.parse_args()
    serve(
        MCPServer(arguments.repo_root, purpose=arguments.purpose, advanced=arguments.advanced,
                  schema_mode=arguments.schema_mode),
        sys.stdin,
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
