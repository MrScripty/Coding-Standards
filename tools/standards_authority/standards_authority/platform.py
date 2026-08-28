from __future__ import annotations

import fcntl
import errno
import os
import stat
import struct
from pathlib import Path

from .errors import invalid, unavailable, unsupported
from .recovery import default_store_path, verify_sqlite_capabilities
from .store import SQLiteObjectStore

_FS_IOC_GETFLAGS = 0x80086601
_EXT4_CASEFOLD_FL = 0x40000000


def open_default_store(repository_root: Path) -> SQLiteObjectStore:
    verify_sqlite_capabilities()
    path = default_store_path(repository_root)
    retained: list[int] = []
    try:
        repository_fd = _open_absolute_directory(repository_root, retained)
        try:
            os.mkdir(".standards-engine", 0o700, dir_fd=repository_fd)
        except FileExistsError:
            pass
        state_fd = os.open(
            ".standards-engine",
            os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW,
            dir_fd=repository_fd,
        )
        retained.append(state_fd)
        observed = os.fstat(state_fd)
        _verify_private_directory(observed)
        _require_local_ext4(state_fd)
        store = SQLiteObjectStore(path)
        try:
            os.chmod("authority.sqlite3", 0o600, dir_fd=state_fd)
            file_fd = os.open(
                "authority.sqlite3",
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
                dir_fd=state_fd,
            )
            retained.append(file_fd)
            descriptor_stat = os.fstat(file_fd)
            path_stat = path.lstat()
            if (descriptor_stat.st_dev, descriptor_stat.st_ino) != (
                path_stat.st_dev,
                path_stat.st_ino,
            ):
                raise invalid(
                    "STORE.PATH_IDENTITY_MISMATCH",
                    "configured path and retained descriptor identify different files",
                )
            _verify_private_file(descriptor_stat)
        except Exception:
            store.close()
            raise
        return store
    except OSError as error:
        raise unavailable("STORE.ROOT_UNAVAILABLE", str(error)) from error
    finally:
        for descriptor in reversed(retained):
            os.close(descriptor)


def _open_absolute_directory(path: Path, retained: list[int]) -> int:
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    retained.append(descriptor)
    for component in path.parts[1:]:
        try:
            descriptor = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW,
                dir_fd=descriptor,
            )
        except OSError as error:
            if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                raise unsupported(
                    "STORE.PATH_REDIRECTION",
                    "store root contains a symlink or non-directory component",
                ) from error
            raise
        retained.append(descriptor)
    return descriptor


def _verify_private_directory(observed: os.stat_result) -> None:
    if not stat.S_ISDIR(observed.st_mode):
        raise invalid("STORE.INVALID_ROOT", "store root must be a directory")
    if observed.st_uid != os.geteuid():
        raise unsupported(
            "STORE.ROOT_OWNER", "store root is not owned by this principal"
        )
    if stat.S_IMODE(observed.st_mode) != 0o700:
        raise unsupported("STORE.ROOT_MODE", "store root mode must be exactly 0700")


def _verify_private_file(observed: os.stat_result) -> None:
    if not stat.S_ISREG(observed.st_mode):
        raise invalid("STORE.INVALID_PATH", "store path must be a regular file")
    if observed.st_uid != os.geteuid() or stat.S_IMODE(observed.st_mode) != 0o600:
        raise unsupported(
            "STORE.FILE_AUTHORITY",
            "store file must be owner-owned with mode exactly 0600",
        )


def _require_local_ext4(descriptor: int) -> None:
    flags = struct.unpack("I", fcntl.ioctl(descriptor, _FS_IOC_GETFLAGS, b"\0" * 4))[0]
    if flags & _EXT4_CASEFOLD_FL:
        raise unsupported("STORE.CASEFOLD", "casefolded ext4 is unsupported")
    observed = os.fstat(descriptor)
    major_minor = f"{os.major(observed.st_dev)}:{os.minor(observed.st_dev)}"
    try:
        mountinfo = Path("/proc/self/mountinfo").read_text().splitlines()
    except OSError as error:
        raise unsupported("STORE.MOUNT_INFO_UNAVAILABLE", str(error)) from error
    matches = [line.split() for line in mountinfo if line.split()[2] == major_minor]
    if not matches:
        raise unsupported("STORE.MOUNT_INFO_UNAVAILABLE", major_minor)
    filesystems = {fields[fields.index("-") + 1] for fields in matches}
    if filesystems != {"ext4"}:
        raise unsupported(
            "STORE.UNSUPPORTED_FILESYSTEM",
            f"store requires local ext4, observed {sorted(filesystems)!r}",
        )


__all__ = ("open_default_store",)
