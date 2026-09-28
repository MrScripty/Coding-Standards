"""Exact material acquisition and no-replace packet publication."""

from __future__ import annotations

import json
import os
import stat
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import quote

from tools.repository_git.repository_git import (
    GitRepository,
    RepositoryPath,
    RepositoryRevision,
    git_output,
)

from .common import (
    COUNT_LIMIT,
    FORMAT,
    MEMBER_LIMIT,
    SHA,
    TOTAL_LIMIT,
    VERSION,
    check_names,
    digest,
    encoded,
    fail,
    markdown,
    no_symlink_ancestors,
    safe_name,
)
from .request import load_request


def safe_file(root: Path, relative: str) -> bytes | None:
    """Read one regular local file beneath a directory without following links."""
    components = RepositoryPath.parse(relative).components
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in components[:-1]:
            try:
                next_descriptor = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
            except FileNotFoundError:
                return None
            os.close(descriptor)
            descriptor = next_descriptor
        try:
            leaf = os.open(
                components[-1],
                os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=descriptor,
            )
        except FileNotFoundError:
            return None
        try:
            before = os.fstat(leaf)
            if not stat.S_ISREG(before.st_mode):
                fail("local evidence is not regular", "unsupported")
            if before.st_size > MEMBER_LIMIT:
                fail("local evidence exceeds member limit", "unsupported")
            with os.fdopen(os.dup(leaf), "rb") as stream:
                data = stream.read(MEMBER_LIMIT + 1)
            after = os.fstat(leaf)
            if (
                len(data) > MEMBER_LIMIT
                or (before.st_size, before.st_mtime_ns, before.st_ctime_ns)
                != (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                or len(data) != after.st_size
            ):
                fail("local evidence changed or exceeds limit", "unavailable")
            return data
        finally:
            os.close(leaf)
    finally:
        os.close(descriptor)


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100600 << 16
    return info


def _validate_staged(path: Path) -> dict:
    """Check this builder's completed staging file before publication."""
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(infos) > COUNT_LIMIT:
                fail("packet member count exceeds limit", "unsupported")
            check_names(names)
            if "manifest.json" not in names:
                fail("packet manifest is missing")
            if any(
                info.is_dir() or (info.external_attr >> 16) & 0o170000 != 0o100000
                for info in infos
            ):
                fail("packet contains a nonregular member")
            total = sum(info.file_size for info in infos)
            if total > TOTAL_LIMIT or any(
                info.file_size > MEMBER_LIMIT for info in infos
            ):
                fail("packet exceeds size limit", "unsupported")
            with archive.open("manifest.json") as stream:
                raw_manifest = stream.read(MEMBER_LIMIT + 1)
            if len(raw_manifest) > MEMBER_LIMIT:
                fail("manifest exceeds member limit", "unsupported")
            actual_digest = digest(raw_manifest)
            manifest = json.loads(raw_manifest)
            if (
                encoded(manifest) != raw_manifest
                or type(manifest) is not dict
                or set(manifest)
                != {
                    "format_version",
                    "implementation",
                    "request_sha256",
                    "repository_label",
                    "label",
                    "review_question",
                    "revisions",
                    "plan",
                    "primary",
                    "context",
                    "comparisons",
                    "artifacts",
                    "claims",
                    "members",
                    "material_gaps",
                }
                or type(manifest["format_version"]) is not int
                or manifest["format_version"] != FORMAT
            ):
                fail("invalid packet manifest")
            members = manifest["members"]
            if type(members) is not list or len(members) != len(infos) - 1:
                fail("invalid member inventory")
            if {entry["name"] for entry in members} != set(names) - {"manifest.json"}:
                fail("member inventory differs from archive")
            for entry in members:
                if (
                    set(entry) != {"name", "size", "sha256"}
                    or type(entry["size"]) is not int
                    or entry["size"] < 0
                    or not SHA.fullmatch(entry["sha256"])
                ):
                    fail("invalid member record")
                with archive.open(entry["name"]) as stream:
                    data = stream.read(MEMBER_LIMIT + 1)
                if len(data) != entry["size"] or digest(data) != entry["sha256"]:
                    fail("packet member changed")
            gaps = manifest["material_gaps"]
            if type(gaps) is not list or any(
                type(gap) is not dict
                or set(gap) != {"artifact_id", "availability"}
                or gap["availability"] not in {"missing", "referenced"}
                for gap in gaps
            ):
                fail("invalid gap inventory")
            declared = [
                {"artifact_id": item["id"], "availability": item["availability"]}
                for item in manifest["artifacts"]
                if item["availability"] != "included"
            ]
            if gaps != declared:
                fail("gap inventory differs from artifacts")
            return {
                "status": "built-with-gaps" if gaps else "built",
                "packet": str(path),
                "manifest_sha256": actual_digest,
                "material_gaps": gaps,
            }
    except (
        OSError,
        zipfile.BadZipFile,
        UnicodeError,
        ValueError,
        KeyError,
        TypeError,
        EOFError,
    ):
        fail("packet is unavailable or malformed", "invalid")


def render_index(
    request: dict,
    identities: dict[str, dict[str, str]],
    primary: list[dict],
    artifacts: list[dict],
    gaps: list[dict],
    members: dict[str, bytes],
    plan_member: str,
    comparisons: list[dict],
) -> bytes:
    lines = [
        "# Review material packet",
        "",
        "This packet inventories selected material. It does not decide whether claims or CI results are valid.",
        "",
        "## Revisions",
        "",
    ]
    for role, identity in identities.items():
        lines.append(
            f"- {markdown(role)}: commit `{identity['commit']}`; tree `{identity['tree']}`"
        )
    lines += [
        "",
        "## Governing plan and change",
        "",
        f"- [Exact governing plan]({quote(plan_member, safe='/')})",
        "- [Complete baseline to candidate patch](changes/baseline-candidate.patch)",
        "",
        f"## Changed primary files ({sum(item['changed'] for item in primary)})",
        "",
    ]

    def append_versions(item: dict) -> None:
        path = item["path"]
        for role in ("baseline", "candidate"):
            member = item.get(role, {}).get("member")
            if member:
                lines.append(
                    f"- {role} {markdown(path)}: [complete file]({quote(member, safe='/')})"
                )
            else:
                lines.append(f"- {role} {markdown(path)}: absent")

    for item in primary:
        if item["changed"]:
            append_versions(item)
    lines += ["", f"## Explicit context files ({len(request['context'])})", ""]
    primary_by_path = {item["path"]: item for item in primary}
    for path in request["context"]:
        append_versions(primary_by_path[path])
    lines += ["", "## Evidence", ""]
    for item in artifacts:
        member = item.get("member")
        suffix = f" [local bytes]({quote(member, safe='/')})" if member else ""
        lines.append(f"- {item['id']}: {item['availability']}{suffix}")
    if comparisons:
        lines += ["", "## Supplemental comparisons", ""]
        for item in comparisons:
            role = item["revision"]
            lines.append(
                f"- {markdown(role)}: [complete path inventory]({quote(f'comparisons/{role}.json', safe='/')}); selected scopes equal: {str(item['equal_within_scopes']).lower()}"
            )
    lines += ["", "## Caller supplied claim associations", ""]
    for claim in request["claims"]:
        lines.append(
            f"- {markdown(claim['id'])}: {', '.join(claim['artifacts']) or 'unassociated'}"
        )
    lines += [
        "",
        f"ZIP file members, including index and manifest: {len(members) + 2}",
        f"Included payload bytes, excluding index and manifest: {sum(map(len, members.values()))}",
        f"Declared gaps: {len(gaps)}",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def build(
    repo_root: Path, request_path: Path, evidence_root: Path | None, output: Path
) -> dict:
    request, request_bytes = load_request(request_path)
    repo_root = repo_root.absolute()
    output = output.absolute()
    no_symlink_ancestors(repo_root)
    no_symlink_ancestors(output.parent)
    if (
        output.suffix.lower() != ".zip"
        or not output.parent.is_dir()
        or output.exists()
        or output.is_symlink()
    ):
        fail("output must be a new ZIP in an existing directory")
    if output.parent.is_symlink() or repo_root.is_symlink() or not repo_root.is_dir():
        fail("unsafe repository or output path")
    if evidence_root is not None:
        evidence_root = evidence_root.absolute()
        no_symlink_ancestors(evidence_root)
        if evidence_root.is_symlink() or not evidence_root.is_dir():
            fail("evidence root is unavailable or unsafe")
    elif any(item["origin"]["kind"] == "local-file" for item in request["artifacts"]):
        fail("local evidence requires an evidence root")
    git = GitRepository(repo_root)
    top_level = Path(
        git_output(
            repo_root,
            ("rev-parse", "--show-toplevel"),
            max_output_bytes=4096,
            local_only=True,
        )
        .decode("utf-8")
        .rstrip("\n")
    )
    if top_level.resolve() != repo_root.resolve():
        fail("repo-root must identify the Git worktree root")
    git_directory = Path(
        git_output(
            repo_root,
            ("rev-parse", "--absolute-git-dir"),
            max_output_bytes=4096,
            local_only=True,
        )
        .decode("utf-8")
        .rstrip("\n")
    )
    resolved_output = output.resolve(strict=False)
    for root in (repo_root, git_directory, evidence_root):
        if root is not None and (
            resolved_output == root.resolve()
            or root.resolve() in resolved_output.parents
            or resolved_output in root.resolve().parents
        ):
            fail("output overlaps an input root")
    revisions = {
        role: RepositoryRevision(oid) for role, oid in request["revisions"].items()
    }
    identities = {
        role: {
            "commit": revision.oid,
            "tree": git.revision_tree(revision, local_only=True),
        }
        for role, revision in revisions.items()
    }
    entries = {
        role: git.revision_entries(revision, local_only=True)
        for role, revision in revisions.items()
    }
    members: dict[str, bytes] = {}

    def add(name: str, data: bytes) -> None:
        safe_name(name)
        if (
            len(data) > MEMBER_LIMIT
            or len(members) >= COUNT_LIMIT - 1
            or sum(map(len, members.values())) + len(data) > TOTAL_LIMIT
        ):
            fail("packet material exceeds limit", "unsupported")
        if name in members:
            fail("duplicate packet member")
        members[name] = data

    def read(role: str, path: RepositoryPath) -> bytes:
        mode, _ = entries[role][path]
        if mode not in {"100644", "100755"}:
            fail("selected source is not a regular file", "unsupported")
        with git.read_session(revisions[role], local_only=True) as session:
            return session.read_file(path)

    baseline, candidate = entries["baseline"], entries["candidate"]
    changed = sorted(
        path
        for path in baseline.keys() | candidate.keys()
        if baseline.get(path) != candidate.get(path)
    )
    primary: list[dict] = []
    selected = sorted(
        set(changed) | {RepositoryPath.parse(path) for path in request["context"]}
    )
    for path in selected:
        if path not in baseline and path not in candidate:
            fail("selected context absent at both endpoints")
        item: dict = {"path": str(path), "changed": path in changed}
        for role, inventory in (("baseline", baseline), ("candidate", candidate)):
            if path in inventory:
                mode, oid = inventory[path]
                data = read(role, path)
                member = f"source/{role}/{path}"
                add(member, data)
                item[role] = {"mode": mode, "blob": oid, "member": member}
        primary.append(item)
    patch = git_output(
        repo_root,
        (
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--no-renames",
            "--binary",
            "--full-index",
            "--no-color",
            revisions["baseline"].oid,
            revisions["candidate"].oid,
            "--",
        ),
        max_output_bytes=MEMBER_LIMIT,
        local_only=True,
        attribute_source=revisions["candidate"],
    )
    add("changes/baseline-candidate.patch", patch)
    plan_role = request["plan"]["revision"]
    plan_path = RepositoryPath.parse(request["plan"]["path"])
    if plan_path not in entries[plan_role]:
        fail("governing plan is absent")
    plan_bytes = read(plan_role, plan_path)
    plan_member = f"records/governing-plan/{plan_path.components[-1]}"
    add(plan_member, plan_bytes)
    comparisons: list[dict] = []
    for comparison in request["comparisons"]:
        role = comparison["revision"]
        other = entries[role]
        differences = sorted(
            path
            for path in candidate.keys() | other.keys()
            if candidate.get(path) != other.get(path)
        )
        scopes = comparison["scopes"]

        def detail(path: RepositoryPath) -> dict:
            result = {"path": str(path)}
            for side, inventory in (("candidate", candidate), (role, other)):
                if path in inventory:
                    mode, oid = inventory[path]
                    result[side] = {"mode": mode, "blob": oid}
            return result

        within = [
            path
            for path in differences
            if any(
                str(path) == scope or str(path).startswith(scope + "/")
                for scope in scopes
            )
        ]
        report = {
            "revision": role,
            "scopes": scopes,
            "equal_within_scopes": not within,
            "differences_within_scopes": [detail(path) for path in within],
            "differences_outside_scopes": [
                detail(path) for path in differences if path not in within
            ],
        }
        add(f"comparisons/{role}.json", encoded(report))
        comparisons.append(report)
    artifacts: list[dict] = []
    gaps: list[dict] = []
    for artifact in request["artifacts"]:
        origin = artifact["origin"]
        item = {
            "id": artifact["id"],
            "role": artifact["role"],
            "subject": artifact.get("subject"),
            "reported_repository": artifact.get("reported_repository"),
            "reported_subject_revision": artifact.get("reported_subject_revision"),
            "origin": origin,
        }
        if origin["kind"] == "reference":
            item["availability"] = "referenced"
        elif origin["kind"] == "git-file":
            role = origin["revision"]
            path = RepositoryPath.parse(origin["path"])
            if path not in entries[role]:
                fail("selected Git evidence is absent", "unavailable")
            data = read(role, path)
            item["availability"] = "included"
            item["mode"], item["blob"] = entries[role][path]
        else:
            assert evidence_root is not None
            data = safe_file(evidence_root, origin["path"])
            item["availability"] = "included" if data is not None else "missing"
            if (
                data is not None
                and "expected_sha256" in origin
                and digest(data) != origin["expected_sha256"]
            ):
                fail("local evidence digest differs from expected")
            item["hash_basis"] = (
                "expected" if "expected_sha256" in origin else "recorded"
            )
        if item["availability"] == "included":
            prefix = "records" if origin["kind"] == "git-file" else "evidence"
            member = f"{prefix}/{item['id']}/{origin['path'].split('/')[-1]}"
            add(member, data)
            item["member"] = member
        else:
            gaps.append(
                {"artifact_id": item["id"], "availability": item["availability"]}
            )
        artifacts.append(item)
    add(
        "INDEX.md",
        render_index(
            request,
            identities,
            primary,
            artifacts,
            gaps,
            members,
            plan_member,
            comparisons,
        ),
    )
    check_names([*members, "manifest.json"])
    manifest = {
        "format_version": FORMAT,
        "implementation": {
            "name": "review-evidence",
            "version": VERSION,
            "source_sha256": digest(Path(__file__).read_bytes()),
        },
        "request_sha256": digest(request_bytes),
        "repository_label": request["repository_label"],
        "label": request["label"],
        "review_question": request["review_question"],
        "revisions": identities,
        "plan": {**request["plan"], "member": plan_member},
        "primary": primary,
        "context": request["context"],
        "comparisons": comparisons,
        "artifacts": artifacts,
        "claims": request["claims"],
        "members": [
            {"name": name, "size": len(data), "sha256": digest(data)}
            for name, data in sorted(members.items())
        ],
        "material_gaps": gaps,
    }
    raw_manifest = encoded(manifest)
    if (
        len(raw_manifest) > MEMBER_LIMIT
        or sum(map(len, members.values())) + len(raw_manifest) > TOTAL_LIMIT
    ):
        fail("manifest exceeds packet limit", "unsupported")
    descriptor, staged = tempfile.mkstemp(
        prefix=".review-evidence-", suffix=".zip", dir=output.parent
    )
    published = False
    try:
        with os.fdopen(descriptor, "wb") as stream:
            os.fchmod(stream.fileno(), 0o600)
            with zipfile.ZipFile(stream, "w") as archive:
                for name, data in sorted(members.items()):
                    archive.writestr(zip_info(name), data)
                archive.writestr(zip_info("manifest.json"), raw_manifest)
        result = _validate_staged(Path(staged))
        os.link(staged, output, follow_symlinks=False)
        published = True
        result["packet"] = str(output)
        return result
    finally:
        try:
            os.unlink(staged)
        except OSError:
            if published:
                result["cleanup_warning"] = "owned staging file cleanup failed"
            else:
                raise


__all__ = ("build",)
