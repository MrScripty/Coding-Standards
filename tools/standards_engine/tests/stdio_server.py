"""One real server process for as many calls as a test makes.

The process is the production module, started the way an MCP client starts it.
Requests and responses are newline-delimited JSON-RPC on its pipes, so every
call still crosses the real transport; only the process start is not repeated.
Recording is always off: no launch here can reach a developer's database.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[3]
MODULE = 'tools.standards_engine.standards_engine.mcp'


class StdioServer:
    """A started and initialized server; `close` ends it the way a client does."""

    def __init__(self, root, *, purpose, options=(), client='test', cwd=None, silent=True, timeout=300):
        self.silent = silent
        self._timeout = timeout
        self._identifier = 0
        # A file, not a pipe: a server that writes diagnostics can never block on it.
        self._errors = tempfile.TemporaryFile()
        try:
            self._process = subprocess.Popen(
                [sys.executable, '-P', '-m', MODULE, '--repo-root', str(root), '--purpose', purpose,
                 *options, '--no-observe'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self._errors, text=True, cwd=cwd,
                env={**os.environ, 'PYTHONPATH': str(ROOT)})
        except BaseException:
            self._errors.close()
            raise
        self._lines = queue.Queue()
        self._reader = threading.Thread(target=self._read, daemon=True)
        self._reader.start()
        try:
            self.initialized = self.exchange('initialize', {
                'protocolVersion': '2025-11-25', 'capabilities': {},
                'clientInfo': {'name': client, 'version': '1'}})
            self._send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        except BaseException:
            self._release()
            raise

    def _read(self):
        for line in self._process.stdout:
            self._lines.put(line)
        self._lines.put(None)

    def _send(self, message):
        try:
            self._process.stdin.write(json.dumps(message) + '\n')
            self._process.stdin.flush()
        except (BrokenPipeError, ValueError):
            raise AssertionError(f'The server is not running: {self.stderr()}') from None

    def exchange(self, method, params=None):
        """Send one request and return its JSON-RPC response."""
        self._identifier += 1
        self._send({'jsonrpc': '2.0', 'id': self._identifier, 'method': method, 'params': params or {}})
        try:
            line = self._lines.get(timeout=self._timeout)
        except queue.Empty:
            self._stop()
            raise AssertionError(f'No response to {method} within {self._timeout} seconds: {self.stderr()}') from None
        if line is None:
            self._stop()
            raise AssertionError(f'The server exited before answering {method}: {self.stderr()}')
        response = json.loads(line)
        if response.get('id') != self._identifier:
            raise AssertionError(f'Response {response.get("id")!r} does not answer request {self._identifier}.')
        if self.silent and self.stderr():
            raise AssertionError(f'The server wrote to stderr during {method}: {self.stderr()}')
        return response

    def call(self, name, arguments):
        """Call one tool and return its JSON-RPC response."""
        return self.exchange('tools/call', {'name': name, 'arguments': arguments})

    def stderr(self):
        """Everything the process has written to stderr so far."""
        self._errors.seek(0)
        return self._errors.read().decode(errors='replace')

    def _stop(self):
        if self._process.poll() is None:
            self._process.kill()
            self._process.wait()

    def _release(self):
        """Stop the process if it still runs and close every handle this object owns."""
        self._stop()
        self._reader.join()
        for stream in (self._process.stdin, self._process.stdout, self._errors):
            try:
                stream.close()
            except BrokenPipeError:
                pass

    def close(self):
        """End input, require a clean exit, and return what the process wrote to stderr."""
        if self._errors.closed:
            return ''
        try:
            try:
                self._process.stdin.close()
            except BrokenPipeError:
                pass
            try:
                code = self._process.wait(timeout=self._timeout)
            except subprocess.TimeoutExpired:
                self._stop()
                raise AssertionError(f'The server did not exit at end of input: {self.stderr()}') from None
            errors = self.stderr()
        finally:
            self._release()
        if code != 0:
            raise AssertionError(f'The server exited with status {code}: {errors}')
        if self.silent and errors:
            raise AssertionError(f'The server wrote to stderr: {errors}')
        return errors


class StdioServers:
    """The servers of one test or one class: one process for each distinct launch.

    A launch is its repository, purpose and options. Register `close` as a
    cleanup; it requires every process to have exited cleanly.
    """

    def __init__(self, *, client='test', cwd=None, silent=True):
        self._settings = {'client': client, 'cwd': cwd, 'silent': silent}
        self._servers = {}

    def server(self, root, purpose, *options):
        """The running server for this launch, started on first use."""
        key = (str(root), purpose, options)
        if key not in self._servers:
            self._servers[key] = StdioServer(root, purpose=purpose, options=options, **self._settings)
        return self._servers[key]

    def restart(self, root, purpose, *options):
        """End this launch's process so that its next call starts a new one."""
        server = self._servers.pop((str(root), purpose, options), None)
        if server is not None:
            server.close()

    def close(self):
        failures = []
        while self._servers:
            try:
                self._servers.popitem()[1].close()
            except AssertionError as error:
                failures.append(str(error))
        if failures:
            raise AssertionError('\n'.join(failures))
