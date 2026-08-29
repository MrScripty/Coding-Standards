from __future__ import annotations

import errno
import fcntl
import hashlib
import os
import stat
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .errors import AuthorityError, invalid, unavailable, unsupported
from .git_index import sanitized_git_environment
from .snapshot import CaptureRequest, ContentSnapshot, RepositoryPath, SnapshotFile

_FS_IOC_GETFLAGS = 0x80086601
_EXT4_CASEFOLD_FL = 0x40000000


class CaptureSource(Protocol):
    def capture(self, request: CaptureRequest) -> ContentSnapshot: ...


@dataclass(frozen=True, slots=True)
class GitlinkSource:
    prefix: RepositoryPath
    object_database: Path


class GitCaptureSource:
    def __init__(
        self,
        repository: Path,
        revision: str,
        gitlinks: tuple[GitlinkSource, ...] = (),
    ) -> None:
        self._repository = repository
        self._revision = revision
        self._gitlinks = {
            item.prefix.components: item.object_database for item in gitlinks
        }

    def capture(self, request: CaptureRequest) -> ContentSnapshot:
        commit_oid = self._run_text(
            self._repository,
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{self._revision}^{{commit}}",
        ).strip()
        algorithm = _algorithm(commit_oid)
        commit = self._object(self._repository, commit_oid, "commit", algorithm)
        tree_oid = _commit_tree(commit)
        files = [
            self._capture_file(path, tree_oid, algorithm) for path in request.files
        ]
        return ContentSnapshot(files)

    def _capture_file(
        self, path: RepositoryPath, initial_tree: str, initial_algorithm: str
    ) -> SnapshotFile:
        repository = self._repository
        algorithm = initial_algorithm
        tree_oid = initial_tree
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
                    "CAPTURE.GIT_OBJECT_UNAVAILABLE",
                    f"{path!s} is absent from the selected Git tree",
                ) from error
            traversed.append(component)
            final = index == len(path.components) - 1
            if mode in {"100644", "100755"}:
                if not final:
                    raise unsupported(
                        "CAPTURE.GIT_NON_DIRECTORY",
                        f"{component!r} is a file before the requested leaf",
                    )
                content = self._object(repository, oid, "blob", algorithm)
                return SnapshotFile(path, content)
            if mode == "40000" or mode == "040000":
                if final:
                    raise unsupported(
                        "CAPTURE.GIT_NON_FILE",
                        "capture requests must name regular files",
                    )
                tree_oid = oid
                index += 1
                continue
            if mode == "160000":
                nested = self._gitlinks.get(tuple(traversed))
                if nested is None:
                    raise unsupported(
                        "CAPTURE.GITLINK_UNMAPPED",
                        f"gitlink {'/'.join(traversed)!r} has no explicit object database",
                    )
                if final:
                    raise unsupported(
                        "CAPTURE.GIT_NON_FILE",
                        "capture requests must name regular files",
                    )
                repository = nested
                algorithm = _algorithm(oid)
                commit = self._object(repository, oid, "commit", algorithm)
                tree_oid = _commit_tree(commit)
                index += 1
                continue
            raise unsupported(
                "CAPTURE.GIT_OBJECT_TYPE",
                f"Git mode {mode!r} is unsupported for selected content",
            )
        raise AssertionError("nonempty path traversal did not return a file")

    def _object(
        self, repository: Path, oid: str, expected_type: str, algorithm: str
    ) -> bytes:
        try:
            result = subprocess.run(
                ("git", "-C", str(repository), "cat-file", "--batch"),
                input=f"{oid}\n".encode("ascii"),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=sanitized_git_environment(),
            )
        except FileNotFoundError as error:
            raise unavailable(
                "CAPTURE.GIT_UNAVAILABLE", "git executable unavailable"
            ) from error
        except subprocess.CalledProcessError as error:
            detail = error.stderr.decode("utf-8", "replace").strip()
            raise invalid("CAPTURE.GIT_INVALID_OBJECT", detail) from error
        header, separator, remainder = result.stdout.partition(b"\n")
        if not separator:
            raise invalid("CAPTURE.GIT_INVALID_OBJECT", "batch header is incomplete")
        if header == f"{oid} missing".encode("ascii"):
            diagnostic = result.stderr.decode("utf-8", "replace").strip()
            if any(
                marker in diagnostic.lower()
                for marker in ("corrupt", "inflate", "hash mismatch")
            ):
                raise invalid("CAPTURE.GIT_INVALID_OBJECT", diagnostic)
            raise unavailable(
                "CAPTURE.GIT_OBJECT_UNAVAILABLE", f"Git object {oid} is unavailable"
            )
        fields = header.split(b" ")
        if len(fields) != 3 or fields[0] != oid.encode("ascii"):
            raise invalid("CAPTURE.GIT_INVALID_OBJECT", "batch header is contradictory")
        try:
            observed_type = fields[1].decode("ascii")
            size = int(fields[2])
        except (UnicodeDecodeError, ValueError) as error:
            raise invalid("CAPTURE.GIT_INVALID_OBJECT", str(error)) from error
        if observed_type != expected_type:
            raise invalid(
                "CAPTURE.GIT_TYPE_MISMATCH",
                f"expected {expected_type}, observed {observed_type}",
            )
        if size < 0 or len(remainder) != size + 1 or remainder[-1:] != b"\n":
            raise invalid("CAPTURE.GIT_INVALID_OBJECT", "batch body length is invalid")
        content = remainder[:-1]
        header = f"{expected_type} {len(content)}\0".encode("ascii")
        digest = hashlib.new(algorithm, header + content).hexdigest()
        if digest != oid:
            raise invalid(
                "CAPTURE.GIT_HASH_MISMATCH",
                f"Git object {oid} failed hash verification",
            )
        return content

    @staticmethod
    def _run(repository: Path, *arguments: str) -> bytes:
        try:
            return subprocess.run(
                ("git", "-C", str(repository), *arguments),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=sanitized_git_environment(),
            ).stdout
        except FileNotFoundError as error:
            raise unavailable(
                "CAPTURE.GIT_UNAVAILABLE", "git executable unavailable"
            ) from error
        except subprocess.CalledProcessError as error:
            detail = error.stderr.decode("utf-8", "replace").strip()
            if any(
                marker in detail.lower()
                for marker in ("corrupt", "inflate", "hash mismatch")
            ):
                raise invalid("CAPTURE.GIT_INVALID_OBJECT", detail) from error
            raise unavailable("CAPTURE.GIT_UNAVAILABLE", detail) from error

    @classmethod
    def _run_text(cls, repository: Path, *arguments: str) -> str:
        try:
            return cls._run(repository, *arguments).decode("ascii")
        except UnicodeDecodeError as error:
            raise invalid("CAPTURE.GIT_INVALID_OUTPUT", str(error)) from error


@dataclass(frozen=True, slots=True)
class _Binding:
    mount_id: int
    device: int
    inode: int
    mode: int
    size: int
    mtime_ns: int
    ctime_ns: int


class NativeCaptureSource:
    def __init__(self, root: Path) -> None:
        if not root.is_absolute():
            raise invalid(
                "CAPTURE.RELATIVE_ROOT", "native capture root must be absolute"
            )
        self._root = root

    def capture(self, request: CaptureRequest) -> ContentSnapshot:
        retained: list[int] = []
        try:
            root_fd = self._open_absolute_root(retained)
            root_mount = _mount_id(root_fd)
            _require_ext4(root_mount)
            _require_case_sensitive(root_fd)
            directories = {(): _binding(root_fd)}
            first: dict[RepositoryPath, tuple[_Binding, bytes]] = {}
            for path in request.files:
                file_fd = self._open_relative_file(
                    root_fd, path, retained, root_mount, directories
                )
                binding = _binding(file_fd)
                first_bytes = _read_all(file_fd)
                second_bytes = _read_all(file_fd)
                if first_bytes != second_bytes or binding != _binding(file_fd):
                    raise unavailable(
                        "CAPTURE.SOURCE_CHANGED",
                        f"{path!s} changed during held-descriptor capture",
                    )
                first[path] = (binding, first_bytes)
            self._after_first_pass()
            second, second_directories = self._rewalk(request, root_mount)
            if first != second or directories != second_directories:
                raise unavailable(
                    "CAPTURE.SOURCE_CHANGED",
                    "native source bindings or bytes changed during endpoint revalidation",
                )
            return ContentSnapshot(
                SnapshotFile(path, first[path][1]) for path in request.files
            )
        finally:
            for descriptor in reversed(retained):
                os.close(descriptor)

    def _after_first_pass(self) -> None:
        """Test seam between retained-descriptor capture and independent rewalk."""

    def _rewalk(
        self, request: CaptureRequest, root_mount: int
    ) -> tuple[
        dict[RepositoryPath, tuple[_Binding, bytes]],
        dict[tuple[str, ...], _Binding],
    ]:
        retained: list[int] = []
        try:
            root_fd = self._open_absolute_root(retained)
            if _mount_id(root_fd) != root_mount:
                raise unavailable("CAPTURE.SOURCE_CHANGED", "root mount changed")
            _require_case_sensitive(root_fd)
            directories = {(): _binding(root_fd)}
            result: dict[RepositoryPath, tuple[_Binding, bytes]] = {}
            for path in request.files:
                descriptor = self._open_relative_file(
                    root_fd, path, retained, root_mount, directories
                )
                binding = _binding(descriptor)
                content = _read_all(descriptor)
                if content != _read_all(descriptor) or binding != _binding(descriptor):
                    raise unavailable("CAPTURE.SOURCE_CHANGED", f"{path!s} changed")
                result[path] = (binding, content)
            return result, directories
        finally:
            for descriptor in reversed(retained):
                os.close(descriptor)

    def _open_absolute_root(self, retained: list[int]) -> int:
        descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
        retained.append(descriptor)
        for component in self._root.parts[1:]:
            descriptor = _open_directory(descriptor, component)
            retained.append(descriptor)
        return descriptor

    @staticmethod
    def _open_relative_file(
        root_fd: int,
        path: RepositoryPath,
        retained: list[int],
        root_mount: int,
        directory_bindings: dict[tuple[str, ...], _Binding],
    ) -> int:
        directory = root_fd
        prefix: list[str] = []
        for component in path.components[:-1]:
            directory = _open_directory(directory, component)
            retained.append(directory)
            if _mount_id(directory) != root_mount:
                raise unsupported("CAPTURE.CROSS_MOUNT", f"{path!s} crosses a mount")
            prefix.append(component)
            key = tuple(prefix)
            observed = _binding(directory)
            existing = directory_bindings.setdefault(key, observed)
            if existing != observed:
                raise unavailable(
                    "CAPTURE.SOURCE_CHANGED", f"directory {'/'.join(key)!r} changed"
                )
        try:
            descriptor = os.open(
                path.components[-1],
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
                dir_fd=directory,
            )
        except OSError as error:
            raise _adapt_open_error(error, path) from error
        retained.append(descriptor)
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise unsupported("CAPTURE.NON_REGULAR", f"{path!s} is not a regular file")
        if _mount_id(descriptor) != root_mount:
            raise unsupported("CAPTURE.CROSS_MOUNT", f"{path!s} crosses a mount")
        return descriptor


def _open_directory(parent: int, component: str) -> int:
    try:
        descriptor = os.open(
            component,
            os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW,
            dir_fd=parent,
        )
    except OSError as error:
        raise _adapt_open_error(error, RepositoryPath((component,))) from error
    try:
        _require_case_sensitive(descriptor)
    except AuthorityError:
        os.close(descriptor)
        raise
    return descriptor


def _require_case_sensitive(descriptor: int) -> None:
    try:
        flags = struct.unpack(
            "I", fcntl.ioctl(descriptor, _FS_IOC_GETFLAGS, b"\0" * 4)
        )[0]
    except OSError as error:
        raise unsupported("CAPTURE.FILESYSTEM_FLAGS_UNAVAILABLE", str(error)) from error
    if flags & _EXT4_CASEFOLD_FL:
        raise unsupported(
            "CAPTURE.CASEFOLD", "casefolded ext4 directory is unsupported"
        )


def _binding(descriptor: int) -> _Binding:
    observed = os.fstat(descriptor)
    return _Binding(
        _mount_id(descriptor),
        observed.st_dev,
        observed.st_ino,
        stat.S_IFMT(observed.st_mode),
        observed.st_size,
        observed.st_mtime_ns,
        observed.st_ctime_ns,
    )


def _mount_id(descriptor: int) -> int:
    try:
        for line in Path(f"/proc/self/fdinfo/{descriptor}").read_text().splitlines():
            if line.startswith("mnt_id:\t"):
                return int(line.split("\t", 1)[1])
    except (OSError, ValueError) as error:
        raise unsupported("CAPTURE.MOUNT_ID_UNAVAILABLE", str(error)) from error
    raise unsupported("CAPTURE.MOUNT_ID_UNAVAILABLE", "fdinfo omitted mnt_id")


def _require_ext4(mount_id: int) -> None:
    try:
        lines = Path("/proc/self/mountinfo").read_text().splitlines()
    except OSError as error:
        raise unsupported("CAPTURE.MOUNT_INFO_UNAVAILABLE", str(error)) from error
    for line in lines:
        fields = line.split()
        if int(fields[0]) == mount_id:
            separator = fields.index("-")
            if fields[separator + 1] != "ext4":
                raise unsupported(
                    "CAPTURE.UNSUPPORTED_FILESYSTEM",
                    f"capture requires ext4, observed {fields[separator + 1]}",
                )
            return
    raise unsupported("CAPTURE.MOUNT_INFO_UNAVAILABLE", f"mount {mount_id} absent")


def _read_all(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _algorithm(oid: str) -> str:
    if len(oid) == 40 and all(character in "0123456789abcdef" for character in oid):
        return "sha1"
    if len(oid) == 64 and all(character in "0123456789abcdef" for character in oid):
        return "sha256"
    raise invalid("CAPTURE.GIT_INVALID_OID", f"invalid Git object ID {oid!r}")


def _commit_tree(commit: bytes) -> str:
    first = commit.splitlines()[0]
    if not first.startswith(b"tree "):
        raise invalid("CAPTURE.GIT_INVALID_COMMIT", "commit omits leading tree")
    try:
        return first[5:].decode("ascii")
    except UnicodeDecodeError as error:
        raise invalid("CAPTURE.GIT_INVALID_COMMIT", str(error)) from error


def _tree_entries(tree: bytes, algorithm: str) -> dict[str, tuple[str, str]]:
    oid_size = hashlib.new(algorithm).digest_size
    offset = 0
    entries: dict[str, tuple[str, str]] = {}
    while offset < len(tree):
        space = tree.find(b" ", offset)
        nul = tree.find(b"\0", space + 1)
        if space < 0 or nul < 0 or nul + 1 + oid_size > len(tree):
            raise invalid("CAPTURE.GIT_INVALID_TREE", "malformed Git tree object")
        try:
            mode = tree[offset:space].decode("ascii")
            name = tree[space + 1 : nul].decode("utf-8")
            RepositoryPath((name,))
        except (UnicodeDecodeError, AuthorityError) as error:
            raise unsupported("CAPTURE.GIT_PATH_UNSUPPORTED", str(error)) from error
        oid = tree[nul + 1 : nul + 1 + oid_size].hex()
        if name in entries:
            raise invalid("CAPTURE.GIT_DUPLICATE_NAME", f"duplicate tree name {name!r}")
        entries[name] = (mode, oid)
        offset = nul + 1 + oid_size
    return entries


def _adapt_open_error(error: OSError, path: RepositoryPath) -> AuthorityError:
    if error.errno in {errno.ELOOP, errno.ENOTDIR}:
        return unsupported("CAPTURE.SYMLINK_OR_NON_DIRECTORY", f"{path!s}: {error}")
    if error.errno in {errno.ENOENT, errno.ESTALE}:
        return unavailable("CAPTURE.SOURCE_UNAVAILABLE", f"{path!s}: {error}")
    return unavailable("CAPTURE.SOURCE_UNAVAILABLE", f"{path!s}: {error}")


__all__ = (
    "CaptureSource",
    "GitCaptureSource",
    "GitlinkSource",
    "NativeCaptureSource",
)
