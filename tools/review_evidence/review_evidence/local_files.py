"""Operation-owned local directories, not authority from an old pathname check.

Walk every component without following symlinks, retain the selected directory,
and verify the requested name still denotes the same chain before accepting work.
All later effects and cleanup use that descriptor, never a re-resolved pathname.
"""
from __future__ import annotations

import errno
import os
import stat
from pathlib import Path
from types import TracebackType

from tools.repository_git.repository_git import RepositoryPath

from .common import fail


def _identity(observed: os.stat_result) -> tuple[int, int]:
    return observed.st_dev, observed.st_ino


def _open_directory(path: Path) -> tuple[int, tuple[tuple[int, int], ...]]:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    descriptor = os.open(path.anchor, flags)
    identities = [_identity(os.fstat(descriptor))]
    try:
        for component in path.parts[1:]:
            child = os.open(component, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
            identities.append(_identity(os.fstat(descriptor)))
        return descriptor, tuple(identities)
    except BaseException:
        os.close(descriptor)
        raise


class LocalDirectory:
    """One admitted directory chain; no global registry or process-wide state."""

    def __init__(self, path: Path) -> None:
        self.path = path.absolute()
        try:
            self.descriptor, self._identities = _open_directory(self.path)
        except OSError as error:
            kind = "unsupported" if error.errno in (errno.ELOOP, errno.ENOTDIR) else "unavailable"
            fail("local directory is unavailable or traverses a symlink", kind)
        self._closed = False

    def assert_current(self) -> None:
        if self._closed:
            fail("local directory lifetime is closed", "unavailable")
        try:
            checked, identities = _open_directory(self.path)
        except OSError:
            fail("selected directory name changed or became unavailable", "unavailable")
        try:
            if identities != self._identities:
                fail("selected directory name changed", "unavailable")
        finally:
            os.close(checked)

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            os.close(self.descriptor)

    def __enter__(self) -> LocalDirectory:
        return self

    def __exit__(self, _kind: object, _value: object, _trace: TracebackType | None) -> None:
        self.close()

    def matches_file(self, name: str, identity: tuple[int, int]) -> bool:
        try:
            observed = os.stat(name, dir_fd=self.descriptor, follow_symlinks=False)
        except FileNotFoundError:
            return False
        return stat.S_ISREG(observed.st_mode) and _identity(observed) == identity


def read_regular(directory: LocalDirectory, relative: str, limit: int) -> bytes | None:
    """Read one bounded, stable file under the retained root; missing stays a gap."""
    directory.assert_current()
    components = RepositoryPath.parse(relative).components
    descriptor = os.dup(directory.descriptor)
    leaf: int | None = None
    try:
        for component in components[:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        leaf = os.open(components[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                       dir_fd=descriptor)
        before = os.fstat(leaf)
        if not stat.S_ISREG(before.st_mode):
            fail("local evidence is not regular", "unsupported")
        if before.st_size > limit:
            fail("local evidence exceeds member limit", "unsupported")
        with os.fdopen(os.dup(leaf), "rb") as stream:
            data = stream.read(limit + 1)
        after = os.fstat(leaf)
        if (len(data) > limit or len(data) != after.st_size
            or (before.st_size, before.st_mtime_ns, before.st_ctime_ns)
            != (after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
            fail("local evidence changed or exceeds limit", "unavailable")
        return data
    except FileNotFoundError:
        return None
    finally:
        if leaf is not None:
            os.close(leaf)
        os.close(descriptor)
        # Even a missing file must not bless a replaced evidence root as a gap.
        directory.assert_current()
