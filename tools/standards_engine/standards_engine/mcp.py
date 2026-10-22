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
from typing import Callable, TextIO

from .tools import AgentToolFacade
from .compiled_cache import CompiledSnapshotCache
from .runtime_identity import RuntimeIdentity
from .contract_discovery import ContractDiscovery
from .context_projection import Purpose
from .mcp_catalog import OutputSchemaDelivery, tool_catalog
from .interaction_observation import InertInteractionRecorder, SQLiteInteractionRecorder
from .interaction_observer import (
    DEFAULT_MAX_AGE_SECONDS, DEFAULT_MAX_BYTES, DEFAULT_MAX_CALLS,
    InteractionRecorder, RecorderConfig, serialized_bytes,
)


PROTOCOL_VERSION = "2025-11-25"


class ProtocolError(Exception):
    def __init__(self, code: int, message: str, data: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


class MCPServer:
    def __init__(self, root: Path, *, purpose: Purpose | str, advanced: bool = False,
                 output_schemas: OutputSchemaDelivery | str = OutputSchemaDelivery.EAGER,
                 observation_db: Path | None = None,
                 observation: RecorderConfig | None = None) -> None:
        self.root = root.resolve()
        self._purpose = Purpose(purpose)
        self.advanced = advanced
        self.output_schemas = OutputSchemaDelivery(output_schemas)
        self._interface = AgentToolFacade.load_interface(self.root)
        self.tools = tool_catalog(
            self._interface, purpose=self.purpose, advanced=advanced,
            output_schemas=self.output_schemas,
        )
        self.names = {tool["name"] for tool in self.tools}
        self._runtime_identity = RuntimeIdentity(self.root, self.purpose, self._interface, self.tools)
        self._contract_discovery = ContractDiscovery(
            self._interface, purpose=self.purpose, operation_names=self.names,
            catalog_digest=self._runtime_identity.metadata()["catalog_digest"],
        )
        self._compiled_cache = CompiledSnapshotCache(self.root, self.purpose)
        self._observer = (InteractionRecorder(observation, self._runtime_identity.metadata(), self.tools)
                          if observation is not None else None)
        self._closed = False
        self.initialized = False
        self.ready = False
        self._recorder = (InertInteractionRecorder() if observation_db is None
                          else SQLiteInteractionRecorder(observation_db))
        self._recorder.begin_session(self._runtime_identity.metadata())

    @property
    def purpose(self) -> Purpose:
        return self._purpose

    def close(self) -> None:
        """Close process-owned capture and cache; each tool call closes its domain store."""
        self._recorder.close()
        if self._observer is not None:
            self._observer.close()
        self._compiled_cache.close()
        self._interface = None
        self._runtime_identity = None
        self._contract_discovery = None
        self.tools.clear()
        self.names.clear()
        self._closed = True

    def dispatch(self, message: object) -> dict | None:
        return self._handle(message)

    def _handle(self, message: object, *, deliver: Callable[[dict], int | None] | None = None,
                request_bytes: int | None = None, parse_error: bool = False) -> dict | None:
        observer = self._observer
        ticket = None
        if observer is not None:
            # Measurement failures are diagnostics failures, never protocol failures.
            if request_bytes is None and deliver is None:
                try:
                    request_bytes = serialized_bytes(message)
                except Exception:
                    pass
            ticket = observer.begin(message, request_bytes=request_bytes,
                                    scope='stdio-flushed' if deliver else 'constructed',
                                    parse_error=parse_error)
        try:
            response = ({'jsonrpc': '2.0', 'id': None,
                         'error': {'code': -32700, 'message': 'Invalid JSON.'}}
                        if parse_error else self._dispatch(message))
            response_bytes = None
            if response is not None:
                if deliver is not None:
                    response_bytes = deliver(response)
                elif observer is not None:
                    try:
                        response_bytes = serialized_bytes(response)
                    except Exception:
                        pass
            if observer is not None:
                observer.finish(ticket, response, response_bytes=response_bytes)
            return response
        except BaseException:
            if observer is not None:
                observer.finish(ticket, incomplete=True)
            raise

    def _dispatch(self, message: object) -> dict | None:
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
                "instructions": f"Installed interface {self._interface.interface.interface_schema_version}; purpose {self.purpose.value}. Output schemas {self.output_schemas.value}. "
                "Use describe_input for missing or abbreviated input shapes; retain its catalog-bound selections. "
                "Use describe_output only when an exact result contract is needed; ordinary results remain structured and server-validated. " + (
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
        interaction = self._recorder.record_request(params)
        result = self._call_tool(params)
        value = result.get("structuredContent")
        if isinstance(value, dict):
            metadata = _response_metadata(value)
            if metadata:
                self._recorder.record_response_metadata(interaction, metadata)
        return result

    def _call_tool(self, params: dict) -> dict:
        name = params.get("name")
        if not isinstance(name, str) or name not in self.names:
            raise ProtocolError(-32602, "Tool unavailable in this running catalog; inspect runtime_info and refresh tools or restart/reconnect after an upgrade.",
                                self._runtime_identity.metadata())
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            raise ProtocolError(-32602, "Tool arguments must be an object.")
        if name in {"describe_input", "describe_output"}:
            return self._tool_result(self._contract_discovery.invoke(
                arguments, direction="input" if name == "describe_input" else "output"))
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
            "isError": value.get("kind") in {"rejected-result", "application-rejected-result", "candidate-application-rejected-result", "input-contract-rejected-result", "output-contract-rejected-result"}
            or value.get("status") == "rejected",
        }


def _response_metadata(value: dict) -> dict:
    """Interface-owned selection: identifiers only, never result bodies."""
    return {key: value[key] for key in ("kind", "code", "outcome", "status")
            if key in value and isinstance(value[key], str)}


def serve(server: MCPServer, source: TextIO, destination: TextIO) -> None:
    def deliver(response: dict) -> int | None:
        serialized = json.dumps(response) + "\n"
        destination.write(serialized)
        destination.flush()
        return len(serialized.encode('utf-8')) if server._observer is not None else None

    try:
        for line in source:
            try:
                message = json.loads(line)
                parse_error = False
            except (ValueError, RecursionError):
                message, parse_error = None, True
            request_bytes = None
            if server._observer is not None:
                try:
                    request_bytes = len(line.encode('utf-8'))
                except UnicodeError:
                    pass
            server._handle(message, deliver=deliver, request_bytes=request_bytes,
                           parse_error=parse_error)
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
        "--output-schemas", choices=[choice.value for choice in OutputSchemaDelivery],
        default=OutputSchemaDelivery.EAGER.value,
        help="Advertise complete output schemas (eager, default), or retrieve exact contracts through describe_output (on-demand).",
    )
    parser.add_argument(
        "--observation-db", type=Path,
        help="Record private local interaction evidence in this SQLite file (disabled when omitted).",
    )
    parser.add_argument('--observe-database', type=Path,
                        help='Opt in to operator-only local SQLite observations in a trusted directory.')
    parser.add_argument('--observe-deployment', help='Required nonsensitive deployment label when recording.')
    parser.add_argument('--observe-max-calls', type=int, default=DEFAULT_MAX_CALLS)
    parser.add_argument('--observe-max-age-seconds', type=int, default=DEFAULT_MAX_AGE_SECONDS)
    parser.add_argument('--observe-max-bytes', type=int, default=DEFAULT_MAX_BYTES)
    arguments = parser.parse_args()
    if (arguments.observe_database is None) != (arguments.observe_deployment is None):
        parser.error('--observe-database and --observe-deployment must be supplied together')
    observation = None
    if arguments.observe_database is not None:
        try:
            observation = RecorderConfig(arguments.observe_database, arguments.observe_deployment,
                                         arguments.observe_max_calls, arguments.observe_max_age_seconds,
                                         arguments.observe_max_bytes)
        except ValueError as error:
            parser.error(str(error))
    serve(
        MCPServer(arguments.repo_root, purpose=arguments.purpose, advanced=arguments.advanced,
                  output_schemas=arguments.output_schemas,
                  observation_db=arguments.observation_db, observation=observation),
        sys.stdin,
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
