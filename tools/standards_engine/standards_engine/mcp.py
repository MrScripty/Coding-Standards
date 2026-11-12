"""Synchronous MCP stdio transport for the generated Engine interface.

Only lifecycle, ping, and tools are supported. Requests execute serially;
durable Engine handles, rather than transport sessions, carry domain state.
One server process has one Engine: it is opened by the first store-backed tool
call, serves every later call, and is closed with the server. Its store
connection is opened for each call and closed when the call ends.
"""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import traceback
from typing import Callable, TextIO

from .tools import AgentToolFacade
from .agent_navigation import (
    ROUTE_CONTENT_RESULT_BYTES, ROUTE_PAGE_BYTES, ROUTE_PAGE_MIN_BYTES, admit_route_page_bytes,
)
from .runtime_identity import RuntimeIdentity
from .contract_discovery import ContractDiscovery
from .context_projection import Purpose
from .mcp_catalog import OutputSchemaDelivery, tool_catalog
from .interaction_observer import (
    DEFAULT_DEPLOYMENT, DEFAULT_MAX_AGE_SECONDS, DEFAULT_MAX_BYTES, DEFAULT_MAX_CALLS,
    InteractionRecorder, RecorderConfig, serialized_bytes,
)


PROTOCOL_VERSION = "2025-11-25"
# Every application client receives this text at initialize; keep it short and plain.
APPLICATION_INSTRUCTIONS = (
    "This server returns the engineering standards that apply to the task you are doing. "
    "Get them before you plan or change code, then follow them.\n"
    "1. Call routing_facts once. It lists every fact name and its allowed values; use them exactly as written.\n"
    "2. Call route with the facts that are true of your task and content={{}}. Leave out a fact you do not know. "
    "Do not remove a true fact to make a call succeed.\n"
    "3. reading_plan lists every module that applies. content.items holds the full text of this page. "
    "While content.next is present, call route again with exactly those arguments.\n"
    "4. Keep the returned snapshot and pass it in every later call. A module you already hold at that snapshot "
    "has not changed; do not read it again.\n"
    "Each module has a review_state: current (this exact text was approved for application use), "
    "changed-since-review (edited after it was approved) or not-reviewed (never approved). "
    "All three are delivered and all apply; the label only tells you how settled the wording is.\n"
    "read and read_many fetch modules by ID; ask for two or three per call so your client can show the whole result. "
    "describe_input gives exact argument shapes when your client abbreviates them.\n"
    "Installed interface {interface}; purpose application."
)


class ProtocolError(Exception):
    def __init__(self, code: int, message: str, data: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


class MCPServer:
    def __init__(self, root: Path, *, purpose: Purpose | str, advanced: bool = False,
                 route_page_bytes: int | None = None,
                 output_schemas: OutputSchemaDelivery | str = OutputSchemaDelivery.EAGER,
                 observation: RecorderConfig | None = None) -> None:
        self.root = root.resolve()
        self._purpose = Purpose(purpose)
        self._route_page_bytes = admit_route_page_bytes(route_page_bytes)
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
        # Opened by the first store-backed tool call; see _invoke.
        self._facade: AgentToolFacade | None = None
        self._observer = (InteractionRecorder(observation, self._runtime_identity.metadata(), self.tools)
                          if observation is not None else None)
        self._closed = False
        self.initialized = False
        self.ready = False

    @property
    def purpose(self) -> Purpose:
        return self._purpose

    def close(self) -> None:
        """Close the process's Engine, with its cache, and its capture."""
        try:
            self._close_engine()
        finally:
            if self._observer is not None:
                self._observer.close()
            self._interface = None
            self._runtime_identity = None
            self._contract_discovery = None
            self.tools.clear()
            self.names.clear()
            self._closed = True

    def _close_engine(self) -> None:
        facade, self._facade = self._facade, None
        if facade is not None:
            facade.close()

    def _invoke(self, name: str, arguments: dict) -> dict:
        """Run one store-backed tool call on this process's Engine.

        The facade, its Engine and the compilation cache are opened by the
        first call that needs them and serve every later call. The store
        connection is not kept: each call opens one, running the admission a
        new open of the store runs, and closes it when the call ends. Between
        calls the process therefore holds no store connection, lock or open
        store file, and every call observes the store exactly as when each
        call opened its own Engine: another process's writes, a migration, a
        changed schema, due maintenance, and a store file that was replaced,
        removed or overwritten. A relocated root and a replaced or missing
        store file close the Engine so that a new one is opened and audited.
        An Engine that reports an unclassified failure is closed straight away.
        """
        facade = self._facade
        if facade is not None and not facade.readmit():
            self._close_engine()
            facade = None
        if facade is None:
            facade = self._facade = AgentToolFacade.open_repository(
                self.root, purpose=self.purpose, interface=self._interface,
                route_page_bytes=self._route_page_bytes,
            )
        value = getattr(facade, name)(arguments)
        # Closing rolls back a transaction the operation did not end, as it
        # always has. A raised failure closes the whole Engine instead.
        facade.release()
        if not facade.reusable:
            self._close_engine()
        return value

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
                "instructions": APPLICATION_INSTRUCTIONS.format(
                    interface=self._interface.interface.interface_schema_version)
                if self.purpose is Purpose.APPLICATION else
                f"Installed interface {self._interface.interface.interface_schema_version}; purpose {self.purpose.value}. Output schemas {self.output_schemas.value}. "
                "Use describe_input for missing or abbreviated input shapes; retain its catalog-bound selections. "
                "Use describe_output only when an exact result contract is needed; ordinary results remain structured and server-validated. " + (
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
        if name in {"describe_input", "describe_output"}:
            return self._tool_result(self._contract_discovery.invoke(
                arguments, direction="input" if name == "describe_input" else "output"))
        if name == "runtime_info":
            value = self._runtime_identity.invoke(arguments)
            return self._tool_result(value)
        try:
            with redirect_stdout(sys.stderr):
                value = self._invoke(name, arguments)
        except BaseException as error:
            # The outcome is unknown and so is the Engine's state. Close it; the
            # next call opens a new one. No operation retries.
            try:
                self._close_engine()
            except Exception as failure:
                print(f"Engine close failed: {type(failure).__name__}", file=sys.stderr)
            if not isinstance(error, Exception):
                raise
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
        "--route-page-bytes", type=int,
        help=f"Application purpose only: byte budget of one route content page, measured on one JSON "
             f"serialization of the result ({ROUTE_PAGE_MIN_BYTES} to {ROUTE_CONTENT_RESULT_BYTES}; default "
             f"{ROUTE_PAGE_BYTES}). A page always holds at least one whole item.",
    )
    parser.add_argument(
        "--output-schemas", choices=[choice.value for choice in OutputSchemaDelivery],
        default=OutputSchemaDelivery.EAGER.value,
        help="Advertise complete output schemas (eager, default), or retrieve exact contracts through describe_output (on-demand).",
    )
    parser.add_argument('--observe-database', type=Path,
                        help='Record operator-only observations in this SQLite file instead of the default location; its directory must exist.')
    parser.add_argument('--observe-deployment', default=DEFAULT_DEPLOYMENT,
                        help='Nonsensitive deployment label stored with each recorded session.')
    parser.add_argument('--no-observe', action='store_true',
                        help='Do not record this process. STANDARDS_ENGINE_OBSERVE=off does the same.')
    parser.add_argument('--observe-max-calls', type=int, default=DEFAULT_MAX_CALLS)
    parser.add_argument('--observe-max-age-seconds', type=int, default=DEFAULT_MAX_AGE_SECONDS)
    parser.add_argument('--observe-max-bytes', type=int, default=DEFAULT_MAX_BYTES)
    arguments = parser.parse_args()
    if arguments.route_page_bytes is not None:
        if arguments.purpose != Purpose.APPLICATION.value:
            parser.error("--route-page-bytes applies to the application purpose")
        try:
            admit_route_page_bytes(arguments.route_page_bytes)
        except ValueError as error:
            parser.error(str(error))
    # Recording is on for every server process. Only these two switches turn it
    # off; in-process MCPServer construction records only when given a configuration.
    observation = None
    if not arguments.no_observe and os.environ.get('STANDARDS_ENGINE_OBSERVE', '').strip().lower() != 'off':
        try:
            observation = RecorderConfig(arguments.observe_database, arguments.observe_deployment,
                                         arguments.observe_max_calls, arguments.observe_max_age_seconds,
                                         arguments.observe_max_bytes)
        except ValueError as error:
            parser.error(str(error))
    serve(
        MCPServer(arguments.repo_root, purpose=arguments.purpose, advanced=arguments.advanced,
                  route_page_bytes=arguments.route_page_bytes,
                  output_schemas=arguments.output_schemas, observation=observation),
        sys.stdin,
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
