from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import threading
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator, Literal, Sequence

from .errors import GitRepositoryError, invalid, unavailable, unsupported
from .model import (
    CapturedFile,
    GitCommandResult,
    GitlinkRepository,
    MaterializedCandidate,
    RepositoryCapture,
    RepositoryPath,
    RepositoryRevision,
)

DEFAULT_OUTPUT_LIMIT = 64 * 1024 * 1024
ERROR_OUTPUT_LIMIT = 1024 * 1024
COMMAND_TIMEOUT_SECONDS = 30
CANDIDATE_COMMIT_MESSAGE = "feat(standards): apply approved proposal\n"


def sanitized_git_environment() -> dict[str, str]:
    selected = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith("GIT_")
    }
    selected.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
            "LANG": "C",
        }
    )
    return selected


def git_command(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    max_output_bytes: int = DEFAULT_OUTPUT_LIMIT,
) -> GitCommandResult:
    if not isinstance(root, Path) or not root.is_absolute():
        raise invalid(
            "REPOSITORY_GIT.INVALID_ROOT",
            "repository root must be an absolute Path",
        )
    if (
        type(max_output_bytes) is not int
        or max_output_bytes < 1
        or isinstance(arguments, (str, bytes))
        or any(
            type(argument) is not str or not argument or "\0" in argument
            for argument in arguments
        )
        or (input_bytes is not None and type(input_bytes) is not bytes)
    ):
        raise invalid(
            "REPOSITORY_GIT.INVALID_COMMAND",
            "Git command arguments or bound are invalid",
        )
    return _run_bounded(
        ("git", "-C", str(root), *arguments),
        input_bytes=input_bytes,
        stdout_limit=max_output_bytes,
        stderr_limit=ERROR_OUTPUT_LIMIT,
        environment=sanitized_git_environment(),
    )


def git_output(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    max_output_bytes: int = DEFAULT_OUTPUT_LIMIT,
) -> bytes:
    result = git_command(
        root,
        arguments,
        input_bytes=input_bytes,
        max_output_bytes=max_output_bytes,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise unavailable(
            "REPOSITORY_GIT.COMMAND_UNAVAILABLE",
            f"Git exited with {result.returncode}: {detail}",
        )
    return result.stdout


def indexed_paths(root: Path) -> tuple[str, ...]:
    return tuple(
        sorted(
            _nul_fields(
                git_output(root, ("ls-files", "-z", "--full-name")),
                "Git index path output",
            )
        )
    )


def staged_name_status(
    root: Path, base: str, pathspecs: Sequence[str]
) -> tuple[str, ...]:
    if type(base) is not str or not base:
        raise invalid("REPOSITORY_GIT.INVALID_BASE", "diff base must be nonempty")
    return _nul_fields(
        git_output(
            root,
            (
                "diff",
                "--cached",
                "--name-status",
                "-z",
                "--find-renames",
                "--find-copies",
                base,
                "--",
                *pathspecs,
            ),
        ),
        "Git staged name-status output",
    )


def materialize_index(root: Path, destination: Path) -> None:
    if not isinstance(destination, Path) or not destination.is_absolute():
        raise invalid(
            "REPOSITORY_GIT.INVALID_DESTINATION",
            "index destination must be an absolute Path",
        )
    prefix = str(destination.resolve()) + os.sep
    git_output(root, ("checkout-index", "--all", "--force", f"--prefix={prefix}"))


class GitRepository:
    def __init__(
        self,
        repository: Path,
        gitlinks: Iterable[GitlinkRepository] = (),
        *,
        max_object_bytes: int = DEFAULT_OUTPUT_LIMIT,
    ) -> None:
        if not isinstance(repository, Path) or not repository.is_absolute():
            raise invalid(
                "REPOSITORY_GIT.INVALID_ROOT",
                "repository root must be an absolute Path",
            )
        if type(max_object_bytes) is not int or max_object_bytes < 1:
            raise invalid(
                "REPOSITORY_GIT.INVALID_BOUND", "object bound must be positive"
            )
        selected = tuple(gitlinks)
        prefixes = tuple(item.prefix.components for item in selected)
        if len(set(prefixes)) != len(prefixes):
            raise invalid(
                "REPOSITORY_GIT.DUPLICATE_GITLINK", "gitlink prefixes must be unique"
            )
        self._repository = repository
        self._gitlinks = {item.prefix.components: item.repository for item in selected}
        self._max_object_bytes = max_object_bytes
        self._active_candidates: set[int] = set()

    def current_revision(self) -> RepositoryRevision:
        return self._revision("HEAD^{commit}")

    def branch_revision(self, branch: str) -> RepositoryRevision:
        if (
            type(branch) is not str
            or not branch
            or "\0" in branch
            or any(0xD800 <= ord(character) <= 0xDFFF for character in branch)
        ):
            raise invalid(
                "REPOSITORY_GIT.INVALID_BRANCH",
                "branch name must be a nonempty Unicode scalar string without NUL",
            )
        checked = git_command(
            self._repository,
            ("check-ref-format", "--branch", branch),
            max_output_bytes=256,
        )
        if checked.returncode != 0 or checked.stdout.decode(
            "utf-8", "replace"
        ).strip() != branch:
            raise invalid(
                "REPOSITORY_GIT.INVALID_BRANCH",
                "branch name is not canonical",
            )
        return self._revision(f"refs/heads/{branch}^{{commit}}")

    @contextmanager
    def materialize_candidate(
        self,
        expected: RepositoryRevision,
        replacements: Iterable[CapturedFile],
    ) -> Iterator[MaterializedCandidate]:
        if type(expected) is not RepositoryRevision:
            raise invalid(
                "REPOSITORY_GIT.INVALID_CANDIDATE",
                "candidate base must be an exact RepositoryRevision",
            )
        supplied = tuple(replacements)
        if any(type(item) is not CapturedFile for item in supplied):
            raise invalid(
                "REPOSITORY_GIT.INVALID_CANDIDATE",
                "candidate replacements must be exact CapturedFile values",
            )
        selected = tuple(sorted(supplied, key=lambda item: item.path))
        paths = tuple(item.path for item in selected)
        if not selected or len(set(paths)) != len(paths):
            raise invalid(
                "REPOSITORY_GIT.INVALID_CANDIDATE",
                "candidate replacements must be nonempty and path-unique",
            )
        self._object(self._repository, expected.oid, "commit", _algorithm(expected.oid))

        with tempfile.TemporaryDirectory(prefix="coding-standards-candidate-") as scratch:
            candidate_root = Path(scratch).resolve() / "repository"
            git_output(
                self._repository,
                (
                    "clone",
                    "--no-checkout",
                    "--local",
                    "--no-hardlinks",
                    "--quiet",
                    "--",
                    str(self._repository),
                    str(candidate_root),
                ),
            )
            git_output(candidate_root, ("remote", "remove", "origin"))
            self._copy_verification_refs(candidate_root)
            git_output(
                candidate_root,
                ("checkout", "--detach", "--force", expected.oid),
            )
            entries = _index_entries(candidate_root)
            for replacement in selected:
                path = str(replacement.path)
                try:
                    mode, _oid = entries[path]
                except KeyError as error:
                    raise unavailable(
                        "REPOSITORY_GIT.CANDIDATE_PATH_UNAVAILABLE",
                        f"replacement target {path!r} is absent from the candidate base",
                    ) from error
                if mode not in {"100644", "100755"}:
                    raise unsupported(
                        "REPOSITORY_GIT.CANDIDATE_PATH_UNSUPPORTED",
                        f"replacement target {path!r} is not a regular file",
                    )
                self._write_candidate_file(candidate_root, replacement)

            git_output(
                candidate_root,
                (
                    "--literal-pathspecs",
                    "add",
                    "--all",
                    "--",
                    *(str(path) for path in paths),
                ),
            )
            tree = _ascii_oid(
                git_output(candidate_root, ("write-tree",), max_output_bytes=256),
                "candidate tree",
            )
            environment = sanitized_git_environment()
            environment.update(
                {
                    "GIT_AUTHOR_DATE": "2000-01-01T00:00:00+00:00",
                    "GIT_AUTHOR_EMAIL": "standards-engine@example.invalid",
                    "GIT_AUTHOR_NAME": "Standards Engine",
                    "GIT_COMMITTER_DATE": "2000-01-01T00:00:00+00:00",
                    "GIT_COMMITTER_EMAIL": "standards-engine@example.invalid",
                    "GIT_COMMITTER_NAME": "Standards Engine",
                }
            )
            candidate_revision = RepositoryRevision(
                _ascii_oid(
                    _git_output_with_environment(
                        candidate_root,
                        ("commit-tree", tree, "-p", expected.oid),
                        environment,
                        input_bytes=CANDIDATE_COMMIT_MESSAGE.encode("utf-8"),
                        max_output_bytes=256,
                    ),
                    "candidate commit",
                )
            )
            git_output(
                candidate_root,
                ("update-ref", "refs/heads/main", candidate_revision.oid),
            )
            git_output(
                candidate_root,
                ("checkout", "--detach", "--force", candidate_revision.oid),
            )
            candidate = MaterializedCandidate(
                candidate_root,
                expected,
                candidate_revision,
            )
            self._validate_candidate(candidate)
            identity = id(candidate)
            self._active_candidates.add(identity)
            try:
                yield candidate
            finally:
                self._active_candidates.discard(identity)

    def publish_candidate(
        self,
        candidate: MaterializedCandidate,
        expected: RepositoryRevision,
    ) -> Literal["updated", "stale"]:
        if (
            type(candidate) is not MaterializedCandidate
            or type(expected) is not RepositoryRevision
            or candidate.expected != expected
            or id(candidate) not in self._active_candidates
        ):
            raise invalid(
                "REPOSITORY_GIT.INVALID_CANDIDATE",
                "publication requires one active materialized candidate and its exact base",
            )
        branch = "main"
        observed_before = self.branch_revision(branch)
        if observed_before != expected:
            return "stale"
        target = f"refs/heads/{branch}"
        self._validate_candidate(candidate)
        git_output(
            self._repository,
            (
                "fetch",
                "--no-tags",
                "--no-write-fetch-head",
                "--quiet",
                "--",
                str(candidate.root),
                "refs/heads/main",
            ),
        )
        self._object(
            self._repository,
            candidate.revision.oid,
            "commit",
            _algorithm(candidate.revision.oid),
        )
        try:
            updated = git_command(
                self._repository,
                ("update-ref", target, candidate.revision.oid, expected.oid),
                max_output_bytes=256,
            )
        except GitRepositoryError as error:
            return self._resolve_uncertain_publication(
                branch,
                expected,
                candidate.revision,
                prior_error=error,
            )
        if updated.returncode == 0:
            return "updated"
        return self._resolve_uncertain_publication(
            branch,
            expected,
            candidate.revision,
        )

    def _resolve_uncertain_publication(
        self,
        branch: str,
        expected: RepositoryRevision,
        candidate: RepositoryRevision,
        *,
        prior_error: GitRepositoryError | None = None,
    ) -> Literal["updated", "stale"]:
        try:
            observed = self.branch_revision(branch)
        except GitRepositoryError as error:
            raise unavailable(
                "REPOSITORY_GIT.PUBLICATION_OUTCOME_UNAVAILABLE",
                "the expected-target update completed without an observable terminal state",
            ) from error
        if observed == candidate:
            return "updated"
        if prior_error is not None:
            raise unavailable(
                "REPOSITORY_GIT.PUBLICATION_OUTCOME_UNAVAILABLE",
                "the expected-target update completed without an observable terminal state",
            ) from prior_error
        if observed != expected:
            return "stale"
        raise unavailable(
            "REPOSITORY_GIT.PUBLICATION_UNAVAILABLE",
            "Git rejected the expected-target update while the target remained unchanged",
        )

    def _copy_verification_refs(self, candidate_root: Path) -> None:
        output = git_output(
            self._repository,
            ("show-ref",),
        )
        for raw_line in output.splitlines():
            try:
                raw_oid, raw_ref = raw_line.split(b" ", 1)
                oid = raw_oid.decode("ascii")
                reference = raw_ref.decode("utf-8")
            except (UnicodeDecodeError, ValueError) as error:
                raise invalid(
                    "REPOSITORY_GIT.INVALID_OUTPUT",
                    "Git reference output is malformed",
                ) from error
            if reference == "refs/heads/main" or reference.endswith("^{}"):
                continue
            git_output(candidate_root, ("update-ref", reference, oid))

    @staticmethod
    def _write_candidate_file(root: Path, replacement: CapturedFile) -> None:
        destination = root.joinpath(*replacement.path.components)
        try:
            if destination.is_symlink() or not destination.is_file():
                raise OSError("replacement target is not a regular file")
            resolved = destination.resolve(strict=True)
            if not resolved.is_relative_to(root):
                raise OSError("replacement target escapes the candidate root")
            flags = os.O_WRONLY | os.O_TRUNC
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            descriptor = os.open(destination, flags)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(replacement.content)
        except OSError as error:
            raise unavailable(
                "REPOSITORY_GIT.CANDIDATE_WRITE_UNAVAILABLE",
                f"candidate replacement could not be written: {error}",
            ) from error

    def _validate_candidate(self, candidate: MaterializedCandidate) -> None:
        if not candidate.root.is_dir():
            raise unavailable(
                "REPOSITORY_GIT.CANDIDATE_UNAVAILABLE",
                "materialized candidate is no longer available",
            )
        candidate_repository = GitRepository(candidate.root)
        if candidate_repository.current_revision() != candidate.revision:
            raise invalid(
                "REPOSITORY_GIT.CANDIDATE_DIVERGED",
                "candidate HEAD no longer identifies the verified revision",
            )
        index_status = git_command(
            candidate.root,
            ("diff", "--cached", "--quiet", candidate.revision.oid, "--"),
            max_output_bytes=256,
        )
        if index_status.returncode != 0:
            raise invalid(
                "REPOSITORY_GIT.CANDIDATE_DIVERGED",
                "candidate index differs from its revision",
            )
        entries = _index_entries(candidate.root)
        files: dict[str, Path] = {}
        for directory, names, filenames in os.walk(candidate.root):
            current = Path(directory)
            if current == candidate.root and ".git" in names:
                names.remove(".git")
            for name in names:
                nested = current / name
                if nested.is_symlink():
                    raise invalid(
                        "REPOSITORY_GIT.CANDIDATE_DIVERGED",
                        "candidate contains a symlinked directory",
                    )
            for name in filenames:
                path = current / name
                relative = path.relative_to(candidate.root).as_posix()
                try:
                    observed = path.lstat()
                except OSError as error:
                    raise unavailable(
                        "REPOSITORY_GIT.CANDIDATE_UNAVAILABLE",
                        f"candidate path {relative!r} could not be observed: {error}",
                    ) from error
                if not stat.S_ISREG(observed.st_mode):
                    raise invalid(
                        "REPOSITORY_GIT.CANDIDATE_DIVERGED",
                        f"candidate path {relative!r} is not a regular file",
                    )
                files[relative] = path
        if set(files) != set(entries):
            raise invalid(
                "REPOSITORY_GIT.CANDIDATE_DIVERGED",
                "candidate filesystem paths differ from its index",
            )
        algorithm = _algorithm(candidate.revision.oid)
        for path, (mode, oid) in entries.items():
            if mode not in {"100644", "100755"}:
                raise unsupported(
                    "REPOSITORY_GIT.CANDIDATE_PATH_UNSUPPORTED",
                    f"candidate path {path!r} is not a regular file",
                )
            try:
                content = files[path].read_bytes()
                executable = bool(files[path].stat().st_mode & 0o111)
            except OSError as error:
                raise unavailable(
                    "REPOSITORY_GIT.CANDIDATE_UNAVAILABLE",
                    f"candidate path {path!r} could not be observed: {error}",
                ) from error
            header = f"blob {len(content)}\0".encode("ascii")
            if hashlib.new(algorithm, header + content).hexdigest() != oid or (
                executable != (mode == "100755")
            ):
                raise invalid(
                    "REPOSITORY_GIT.CANDIDATE_DIVERGED",
                    f"candidate path {path!r} differs from its object",
                )

    def _revision(self, revision: str) -> RepositoryRevision:
        output = git_output(
            self._repository,
            ("rev-parse", "--verify", "--end-of-options", revision),
            max_output_bytes=256,
        )
        try:
            oid = output.decode("ascii").strip()
        except UnicodeDecodeError as error:
            raise invalid("REPOSITORY_GIT.INVALID_OUTPUT", str(error)) from error
        return RepositoryRevision(oid)

    def capture_current(self, paths: Iterable[RepositoryPath]) -> RepositoryCapture:
        selected = tuple(sorted(paths))
        if not selected or len(set(selected)) != len(selected):
            raise invalid(
                "REPOSITORY_GIT.INVALID_CAPTURE",
                "capture paths must be nonempty and unique",
            )
        revision = self.current_revision()
        return RepositoryCapture(
            revision,
            (CapturedFile(path, self.read_file(revision, path)) for path in selected),
        )

    def read_file(self, revision: RepositoryRevision, path: RepositoryPath) -> bytes:
        algorithm = _algorithm(revision.oid)
        commit = self._object(self._repository, revision.oid, "commit", algorithm)
        tree_oid = _commit_tree(commit, algorithm)
        repository = self._repository
        traversed: list[str] = []
        index = 0
        while index < len(path.components):
            tree = self._object(repository, tree_oid, "tree", algorithm)
            entries = _tree_entries(tree, algorithm)
            component = path.components[index]
            try:
                mode, oid = entries[component]
            except KeyError as error:
                raise unavailable(
                    "REPOSITORY_GIT.OBJECT_UNAVAILABLE",
                    f"{path!s} is absent from revision {revision.oid}",
                ) from error
            traversed.append(component)
            final = index == len(path.components) - 1
            if mode in {"100644", "100755"}:
                if not final:
                    raise unsupported(
                        "REPOSITORY_GIT.NON_DIRECTORY",
                        f"{component!r} is a file before the requested leaf",
                    )
                return self._object(repository, oid, "blob", algorithm)
            if mode in {"40000", "040000"}:
                if final:
                    raise unsupported(
                        "REPOSITORY_GIT.NON_REGULAR_FILE",
                        "requested path identifies a tree",
                    )
                tree_oid = oid
                index += 1
                continue
            if mode == "160000":
                nested = self._gitlinks.get(tuple(traversed))
                if nested is None:
                    raise unsupported(
                        "REPOSITORY_GIT.GITLINK_UNMAPPED",
                        f"gitlink {'/'.join(traversed)!r} has no repository mapping",
                    )
                if final:
                    raise unsupported(
                        "REPOSITORY_GIT.NON_REGULAR_FILE",
                        "requested path identifies a gitlink",
                    )
                repository = nested
                algorithm = _algorithm(oid)
                nested_commit = self._object(repository, oid, "commit", algorithm)
                tree_oid = _commit_tree(nested_commit, algorithm)
                index += 1
                continue
            raise unsupported(
                "REPOSITORY_GIT.NON_REGULAR_FILE",
                f"Git mode {mode!r} is not a regular file",
            )
        raise AssertionError("nonempty path traversal did not return a file")

    def _object(
        self, repository: Path, oid: str, expected_type: str, algorithm: str
    ) -> bytes:
        try:
            output = git_output(
                repository,
                ("cat-file", "--batch"),
                input_bytes=f"{oid}\n".encode("ascii"),
                max_output_bytes=self._max_object_bytes + 256,
            )
        except GitRepositoryError as error:
            if error.failure.code == "REPOSITORY_GIT.COMMAND_UNAVAILABLE":
                detail = error.failure.message.lower()
                if any(
                    marker in detail
                    for marker in ("corrupt", "inflate", "hash mismatch")
                ):
                    raise invalid(
                        "REPOSITORY_GIT.INVALID_OBJECT", error.failure.message
                    ) from error
            raise
        header, separator, remainder = output.partition(b"\n")
        if not separator:
            raise invalid("REPOSITORY_GIT.INVALID_OBJECT", "batch header is incomplete")
        if header == f"{oid} missing".encode("ascii"):
            raise unavailable(
                "REPOSITORY_GIT.OBJECT_UNAVAILABLE", f"Git object {oid} is unavailable"
            )
        fields = header.split(b" ")
        if len(fields) != 3 or fields[0] != oid.encode("ascii"):
            raise invalid(
                "REPOSITORY_GIT.INVALID_OBJECT", "batch header is contradictory"
            )
        try:
            observed_type = fields[1].decode("ascii")
            size = int(fields[2])
        except (UnicodeDecodeError, ValueError) as error:
            raise invalid("REPOSITORY_GIT.INVALID_OBJECT", str(error)) from error
        if observed_type != expected_type:
            raise invalid(
                "REPOSITORY_GIT.TYPE_MISMATCH",
                f"expected {expected_type}, observed {observed_type}",
            )
        if size < 0 or size > self._max_object_bytes:
            raise unsupported(
                "REPOSITORY_GIT.OBJECT_LIMIT",
                f"Git object exceeds {self._max_object_bytes} bytes",
            )
        if len(remainder) != size + 1 or remainder[-1:] != b"\n":
            raise invalid(
                "REPOSITORY_GIT.INVALID_OBJECT", "batch body length is invalid"
            )
        content = remainder[:-1]
        object_header = f"{expected_type} {len(content)}\0".encode("ascii")
        if hashlib.new(algorithm, object_header + content).hexdigest() != oid:
            raise invalid(
                "REPOSITORY_GIT.HASH_MISMATCH", f"Git object {oid} failed verification"
            )
        return content


def _run_bounded(
    command: tuple[str, ...],
    *,
    input_bytes: bytes | None,
    stdout_limit: int,
    stderr_limit: int,
    environment: dict[str, str],
) -> GitCommandResult:
    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
        )
    except OSError as error:
        raise unavailable(
            "REPOSITORY_GIT.EXECUTABLE_UNAVAILABLE", f"Git execution failed: {error}"
        ) from error

    assert process.stdout is not None and process.stderr is not None
    outputs: dict[str, bytes] = {}
    overflow: list[str] = []

    def read(name: str, stream: object, limit: int) -> None:
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = stream.read(64 * 1024)  # type: ignore[attr-defined]
            if not chunk:
                break
            total += len(chunk)
            if total > limit:
                overflow.append(name)
                process.kill()
                break
            chunks.append(chunk)
        outputs[name] = b"".join(chunks)

    stdout_thread = threading.Thread(
        target=read, args=("stdout", process.stdout, stdout_limit)
    )
    stderr_thread = threading.Thread(
        target=read, args=("stderr", process.stderr, stderr_limit)
    )
    stdout_thread.start()
    stderr_thread.start()
    if input_bytes is not None:
        assert process.stdin is not None
        try:
            process.stdin.write(input_bytes)
            process.stdin.close()
        except BrokenPipeError:
            pass
    try:
        returncode = process.wait(timeout=COMMAND_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as error:
        process.kill()
        process.wait()
        raise unavailable(
            "REPOSITORY_GIT.COMMAND_TIMEOUT",
            f"Git command exceeded {COMMAND_TIMEOUT_SECONDS} seconds",
        ) from error
    finally:
        stdout_thread.join()
        stderr_thread.join()
        process.stdout.close()
        process.stderr.close()
        if process.stdin is not None and not process.stdin.closed:
            process.stdin.close()
    if overflow:
        raise unsupported(
            "REPOSITORY_GIT.OUTPUT_LIMIT",
            f"Git {overflow[0]} exceeded its configured byte bound",
        )
    return GitCommandResult(returncode, outputs["stdout"], outputs["stderr"])


def _nul_fields(output: bytes, description: str) -> tuple[str, ...]:
    if not output:
        return ()
    if not output.endswith(b"\0"):
        raise invalid(
            "REPOSITORY_GIT.INVALID_OUTPUT", f"{description} is not NUL terminated"
        )
    try:
        fields = output[:-1].decode("utf-8").split("\0")
    except UnicodeDecodeError as error:
        raise unsupported(
            "REPOSITORY_GIT.PATH_ENCODING", f"{description} is not UTF-8"
        ) from error
    if any(not field for field in fields):
        raise invalid(
            "REPOSITORY_GIT.INVALID_OUTPUT", f"{description} contains an empty field"
        )
    return tuple(fields)


def _git_output_with_environment(
    root: Path,
    arguments: Sequence[str],
    environment: dict[str, str],
    *,
    input_bytes: bytes | None = None,
    max_output_bytes: int = DEFAULT_OUTPUT_LIMIT,
) -> bytes:
    result = _run_bounded(
        ("git", "-C", str(root), *arguments),
        input_bytes=input_bytes,
        stdout_limit=max_output_bytes,
        stderr_limit=ERROR_OUTPUT_LIMIT,
        environment=environment,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise unavailable(
            "REPOSITORY_GIT.COMMAND_UNAVAILABLE",
            f"Git exited with {result.returncode}: {detail}",
        )
    return result.stdout


def _ascii_oid(output: bytes, description: str) -> str:
    try:
        oid = output.decode("ascii").strip()
        RepositoryRevision(oid)
    except (UnicodeDecodeError, GitRepositoryError) as error:
        raise invalid(
            "REPOSITORY_GIT.INVALID_OUTPUT",
            f"Git {description} output is not one canonical object ID",
        ) from error
    return oid


def _index_entries(root: Path) -> dict[str, tuple[str, str]]:
    fields = git_output(root, ("ls-files", "-s", "-z"))
    entries: dict[str, tuple[str, str]] = {}
    for raw in fields.split(b"\0"):
        if not raw:
            continue
        header, separator, raw_path = raw.partition(b"\t")
        parts = header.split(b" ")
        if not separator or len(parts) != 3 or parts[2] != b"0":
            raise invalid(
                "REPOSITORY_GIT.INVALID_OUTPUT",
                "Git index output is malformed or contains an unmerged entry",
            )
        try:
            mode = parts[0].decode("ascii")
            oid = parts[1].decode("ascii")
            path = raw_path.decode("utf-8")
            RepositoryRevision(oid)
            RepositoryPath.parse(path)
        except (UnicodeDecodeError, GitRepositoryError) as error:
            raise unsupported(
                "REPOSITORY_GIT.PATH_ENCODING",
                "Git index entry is not a supported canonical path or object",
            ) from error
        if path in entries:
            raise invalid(
                "REPOSITORY_GIT.INVALID_OUTPUT",
                f"Git index repeats path {path!r}",
            )
        entries[path] = (mode, oid)
    return entries


def _algorithm(oid: str) -> str:
    return "sha1" if len(oid) == 40 else "sha256"


def _commit_tree(commit: bytes, algorithm: str) -> str:
    first = commit.splitlines()[0]
    if not first.startswith(b"tree "):
        raise invalid("REPOSITORY_GIT.INVALID_COMMIT", "commit omits leading tree")
    try:
        revision = RepositoryRevision(first[5:].decode("ascii"))
    except UnicodeDecodeError as error:
        raise invalid("REPOSITORY_GIT.INVALID_COMMIT", str(error)) from error
    if _algorithm(revision.oid) != algorithm:
        raise invalid(
            "REPOSITORY_GIT.INVALID_COMMIT",
            "commit and tree object IDs use different algorithms",
        )
    return revision.oid


def _tree_entries(tree: bytes, algorithm: str) -> dict[str, tuple[str, str]]:
    oid_size = hashlib.new(algorithm).digest_size
    offset = 0
    entries: dict[str, tuple[str, str]] = {}
    while offset < len(tree):
        space = tree.find(b" ", offset)
        nul = tree.find(b"\0", space + 1)
        if space < 0 or nul < 0 or nul + 1 + oid_size > len(tree):
            raise invalid("REPOSITORY_GIT.INVALID_TREE", "malformed Git tree object")
        try:
            mode = tree[offset:space].decode("ascii")
            name = tree[space + 1 : nul].decode("utf-8")
            RepositoryPath((name,))
        except (UnicodeDecodeError, GitRepositoryError) as error:
            raise unsupported("REPOSITORY_GIT.PATH_ENCODING", str(error)) from error
        oid = tree[nul + 1 : nul + 1 + oid_size].hex()
        if name in entries:
            raise invalid(
                "REPOSITORY_GIT.DUPLICATE_TREE_NAME", f"duplicate tree name {name!r}"
            )
        entries[name] = (mode, oid)
        offset = nul + 1 + oid_size
    return entries


__all__ = (
    "COMMAND_TIMEOUT_SECONDS",
    "DEFAULT_OUTPUT_LIMIT",
    "GitRepository",
    "git_command",
    "git_output",
    "indexed_paths",
    "materialize_index",
    "sanitized_git_environment",
    "staged_name_status",
)
