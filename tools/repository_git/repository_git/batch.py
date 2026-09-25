"""Single-owner Git batch exchange with bounded frames and deterministic cleanup."""
from __future__ import annotations

import hashlib
import os
import queue
import signal
import subprocess
import threading
from dataclasses import dataclass, field
from typing import Callable

from .errors import GitRepositoryError, invalid, unavailable, unsupported

HEADER_LIMIT = 256


def object_size(header: bytes, oid: str, expected_type: str, limit: int) -> int:
    if not header.endswith(b"\n") or len(header) > HEADER_LIMIT:
        raise invalid("REPOSITORY_GIT.INVALID_OBJECT", "batch header is incomplete or oversized")
    header = header[:-1]
    if header == f"{oid} missing".encode("ascii"):
        raise unavailable("REPOSITORY_GIT.OBJECT_UNAVAILABLE", f"Git object {oid} is unavailable")
    fields = header.split(b" ")
    if len(fields) != 3 or fields[0] != oid.encode("ascii"):
        raise invalid("REPOSITORY_GIT.INVALID_OBJECT", "batch header is contradictory")
    try:
        observed_type = fields[1].decode("ascii")
        size = int(fields[2])
    except (UnicodeDecodeError, ValueError) as error:
        raise invalid("REPOSITORY_GIT.INVALID_OBJECT", "batch size or type is invalid") from error
    if observed_type != expected_type:
        raise invalid("REPOSITORY_GIT.TYPE_MISMATCH", f"expected {expected_type}, observed {observed_type}")
    if size < 0 or size > limit:
        raise unsupported("REPOSITORY_GIT.OBJECT_LIMIT", f"Git object exceeds {limit} bytes")
    return size


def verified_body(body: bytes, size: int, oid: str, expected_type: str, algorithm: str) -> bytes:
    if len(body) != size + 1 or body[-1:] != b"\n":
        raise invalid("REPOSITORY_GIT.INVALID_OBJECT", "batch body length is invalid")
    content = body[:-1]
    header = f"{expected_type} {size}\0".encode("ascii")
    if hashlib.new(algorithm, header + content).hexdigest() != oid:
        raise invalid("REPOSITORY_GIT.HASH_MISMATCH", f"Git object {oid} failed verification")
    return content


def command_failure(returncode: int | None, stderr: bytes) -> GitRepositoryError:
    detail = stderr.decode("utf-8", "replace").strip()
    if any(marker in detail.lower() for marker in ("corrupt", "inflate", "hash mismatch")):
        return invalid("REPOSITORY_GIT.INVALID_OBJECT", f"Git exited with {returncode}: {detail}")
    return unavailable("REPOSITORY_GIT.COMMAND_UNAVAILABLE", f"Git exited with {returncode}: {detail}")


@dataclass
class _Exchange:
    action: Callable[[], bytes]
    done: threading.Event = field(default_factory=threading.Event)
    result: bytes = b""
    error: BaseException | None = None


class VerifiedBatchReader:
    """One serial caller, one pipe owner, and one bounded stderr drain.

    The per-exchange deadline retains the existing command timeout, including
    pipe writes. It never limits the lifetime of a valid multi-object capture.
    Exceptions close the protocol stream; a later explicit session read may
    create a fresh reader, but this reader never retries a failed request.
    """

    def __init__(self, command: tuple[str, ...], *, environment: dict[str, str],
                 object_limit: int, stderr_limit: int, timeout: float) -> None:
        self._limit, self._stderr_limit, self._timeout = object_limit, stderr_limit, timeout
        self._closed = False
        self._stderr = bytearray()
        self._overflow = threading.Event()
        self._stderr_error: OSError | None = None
        self._requests: queue.Queue[_Exchange | None] = queue.Queue(maxsize=1)
        self._busy = threading.Lock()
        try:
            self._process = subprocess.Popen(
                command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, env=environment,
                start_new_session=os.name == "posix",
            )
        except OSError as error:
            raise unavailable("REPOSITORY_GIT.EXECUTABLE_UNAVAILABLE", f"Git execution failed: {error}") from error
        self._worker = threading.Thread(target=self._work, name="git-batch-exchange")
        self._drainer = threading.Thread(target=self._drain, name="git-batch-stderr")
        try:
            self._worker.start()
            self._drainer.start()
        except BaseException:
            self.abort()
            raise

    def _kill(self) -> None:
        try:
            if os.name == "posix":
                os.killpg(self._process.pid, signal.SIGKILL)
            else:
                self._process.kill()
        except ProcessLookupError:
            pass

    def _drain(self) -> None:
        assert self._process.stderr is not None
        try:
            while chunk := os.read(self._process.stderr.fileno(), 64 * 1024):
                remaining = self._stderr_limit - len(self._stderr)
                self._stderr.extend(chunk[:remaining])
                if len(chunk) > remaining:
                    self._overflow.set()
                    self._kill()
                    return
        except OSError as error:
            self._stderr_error = error
            self._kill()

    def _work(self) -> None:
        while not self._closed:
            exchange = self._requests.get()
            if exchange is None:
                return
            try:
                exchange.result = exchange.action()
            except BaseException as error:
                exchange.error = error
            finally:
                exchange.done.set()

    def _perform(self, action: Callable[[], bytes]) -> bytes:
        if self._closed:
            raise invalid("REPOSITORY_GIT.READ_SESSION_CLOSED", "the batch reader is closed")
        if not self._busy.acquire(blocking=False):
            raise invalid("REPOSITORY_GIT.READ_SESSION_BUSY", "batch exchanges require one owner")
        try:
            exchange = _Exchange(action)
            self._requests.put_nowait(exchange)
            if not exchange.done.wait(self._timeout):
                raise unavailable("REPOSITORY_GIT.COMMAND_TIMEOUT", f"Git exchange exceeded {self._timeout} seconds")
            if self._overflow.is_set():
                raise unsupported("REPOSITORY_GIT.OUTPUT_LIMIT", "Git stderr exceeded its configured byte bound")
            if self._stderr_error is not None:
                raise unavailable("REPOSITORY_GIT.COMMAND_UNAVAILABLE", "Git stderr could not be observed") from self._stderr_error
            if exchange.error is not None:
                raise exchange.error
            return exchange.result
        except BaseException as error:
            self.abort()
            if self._overflow.is_set():
                raise unsupported("REPOSITORY_GIT.OUTPUT_LIMIT", "Git stderr exceeded its configured byte bound") from error
            if (isinstance(error, GitRepositoryError)
                and error.failure.code == "REPOSITORY_GIT.INVALID_OBJECT"
                and self._process.returncode is not None
                and self._process.returncode > 0):
                raise command_failure(self._process.returncode, bytes(self._stderr)) from error
            if isinstance(error, (BrokenPipeError, OSError)):
                raise command_failure(self._process.returncode, bytes(self._stderr)) from error
            # Corruption can arrive as an incomplete stdout frame plus stderr.
            if isinstance(error, GitRepositoryError) and any(
                word in bytes(self._stderr).lower() for word in (b"corrupt", b"inflate", b"hash mismatch")
            ):
                raise command_failure(self._process.returncode, bytes(self._stderr)) from error
            raise
        finally:
            self._busy.release()

    def read(self, oid: str, expected_type: str, algorithm: str) -> bytes:
        def exchange() -> bytes:
            assert self._process.stdin is not None and self._process.stdout is not None
            self._process.stdin.write(f"{oid}\n".encode("ascii"))
            self._process.stdin.flush()
            header = self._process.stdout.readline(HEADER_LIMIT + 1)
            size = object_size(header, oid, expected_type, self._limit)
            body = self._process.stdout.read(size + 1)
            return verified_body(body, size, oid, expected_type, algorithm)
        return self._perform(exchange)

    def _release(self, *, aborted: bool = False) -> None:
        self._closed = True
        try:
            self._requests.put_nowait(None)
        except queue.Full:
            pass
        if self._worker.ident is not None:
            self._worker.join()
        if self._drainer.ident is not None:
            self._drainer.join()
        close_error = None
        for stream in (self._process.stdin, self._process.stdout, self._process.stderr):
            if stream is not None:
                try:
                    stream.close()
                except OSError as error:
                    close_error = error
        # An aborted exchange deliberately discards pending stdin after reaping;
        # a broken pipe during that discard cannot replace the primary failure.
        if close_error is not None and not aborted:
            raise unavailable("REPOSITORY_GIT.COMMAND_UNAVAILABLE", "Git pipe cleanup failed") from close_error

    def abort(self) -> None:
        if self._closed:
            return
        self._kill()
        self._process.wait()
        self._release(aborted=True)

    def close(self) -> None:
        if self._closed:
            return
        def finish() -> bytes:
            assert self._process.stdin is not None and self._process.stdout is not None
            self._process.stdin.close()
            if self._process.stdout.read(1):
                raise invalid("REPOSITORY_GIT.INVALID_OBJECT", "unexpected trailing batch output")
            return b""
        try:
            self._perform(finish)
            try:
                code = self._process.wait(timeout=self._timeout)
            except subprocess.TimeoutExpired as error:
                raise unavailable("REPOSITORY_GIT.COMMAND_TIMEOUT", "Git batch shutdown exceeded the command timeout") from error
            self._release()
            if self._overflow.is_set():
                raise unsupported("REPOSITORY_GIT.OUTPUT_LIMIT", "Git stderr exceeded its configured byte bound")
            if self._stderr_error is not None or code != 0:
                raise command_failure(code, bytes(self._stderr))
        except BaseException:
            self.abort()
            raise
