"""Build and inspect bounded, local review packets."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import quote

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from tools.repository_git.repository_git import (
    GitRepository, GitRepositoryError, RepositoryPath, RepositoryRevision, git_output,
)

FORMAT = 1
MEMBER_LIMIT = 64 * 1024 * 1024
TOTAL_LIMIT = 256 * 1024 * 1024
COUNT_LIMIT = 4096
REQUEST_LIMIT = 1024 * 1024
OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
SHA = re.compile(r"sha256:[0-9a-f]{64}\Z")


class PacketError(Exception):
    def __init__(self, kind: str, message: str):
        self.kind = kind
        super().__init__(message)


def fail(message: str, kind: str = "invalid") -> None:
    raise PacketError(kind, message)


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def markdown(value: str) -> str:
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", value)


def safe_name(name: str) -> str:
    path = RepositoryPath.parse(name)
    for component in path.components:
        if component.endswith((" ", ".")) or any(ord(c) < 32 or ord(c) == 127 for c in component):
            fail("unsafe portable member name", "unsupported")
        if component.split(".")[0].casefold() in {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}:
            fail("unsafe portable member name", "unsupported")
    return str(path)


def check_names(names: list[str]) -> None:
    folded: set[str] = set()
    for name in names:
        safe_name(name)
        key = name.casefold()
        if key in folded:
            fail("duplicate or case-colliding packet member")
        folded.add(key)


def no_symlink_ancestors(path: Path) -> None:
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        if current.is_symlink():
            fail("filesystem path traverses a symlink", "unsupported")


def load_request(path: Path) -> tuple[dict, bytes]:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > REQUEST_LIMIT:
        fail("request unavailable or over limit", "unavailable")
    raw = path.read_bytes()
    if len(raw) > REQUEST_LIMIT:
        fail("request exceeds limit", "unsupported")
    try:
        request = json.loads(raw)
        schema = json.loads(Path(__file__).with_name("request-schema.json").read_bytes())
        Draft202012Validator(schema).validate(request)
    except (ValueError, UnicodeError):
        fail("invalid request JSON")
    except ValidationError:
        fail("request does not match version 1 schema")
    revisions = request["revisions"]
    if len(set(revisions.values())) != len(revisions):
        fail("revision aliases must identify distinct commits")
    if request["plan"]["revision"] not in revisions:
        fail("plan revision alias is unknown")
    safe_name(request["plan"]["path"])
    for path_name in request["context"]:
        safe_name(path_name)
    artifact_ids: set[str] = set()
    for artifact in request["artifacts"]:
        if artifact["id"] in artifact_ids:
            fail("duplicate artifact ID")
        artifact_ids.add(artifact["id"])
        if "subject" in artifact and artifact["subject"] not in revisions:
            fail("unknown evidence subject")
        origin = artifact["origin"]
        if origin["kind"] != "reference":
            safe_name(origin["path"])
        if origin["kind"] == "git-file" and origin["revision"] not in revisions:
            fail("unknown evidence revision")
    claim_ids: set[str] = set()
    for claim in request["claims"]:
        if claim["id"] in claim_ids:
            fail("duplicate claim ID")
        claim_ids.add(claim["id"])
        if any(item not in artifact_ids for item in claim["artifacts"]):
            fail("claim names unknown evidence")
    compared: set[str] = set()
    for item in request["comparisons"]:
        alias = item["revision"]
        if alias not in revisions or alias in {"baseline", "candidate"} or alias in compared:
            fail("invalid comparison revision")
        compared.add(alias)
        for scope in item["scopes"]:
            safe_name(scope)
    return request, raw


def safe_file(root: Path, relative: str) -> bytes | None:
    """Read one regular local file beneath a directory without following links."""
    components = RepositoryPath.parse(relative).components
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in components[:-1]:
            try:
                next_descriptor = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            except FileNotFoundError:
                return None
            os.close(descriptor)
            descriptor = next_descriptor
        try:
            leaf = os.open(components[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor)
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
            if len(data) > MEMBER_LIMIT or (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns) or len(data) != after.st_size:
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
    info.external_attr = (0o100600 << 16)
    return info


def _validate_staged(path: Path) -> dict:
    """Check this builder's completed staging file before publication."""
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(infos) > COUNT_LIMIT + 1:
                fail("packet member count exceeds limit", "unsupported")
            check_names(names)
            if "manifest.json" not in names:
                fail("packet manifest is missing")
            if any(info.is_dir() or (info.external_attr >> 16) & 0o170000 != 0o100000 for info in infos):
                fail("packet contains a nonregular member")
            total = sum(info.file_size for info in infos)
            if total > TOTAL_LIMIT or any(info.file_size > MEMBER_LIMIT for info in infos):
                fail("packet exceeds size limit", "unsupported")
            raw_manifest = archive.read("manifest.json")
            if len(raw_manifest) > MEMBER_LIMIT:
                fail("manifest exceeds member limit", "unsupported")
            actual_digest = digest(raw_manifest)
            manifest = json.loads(raw_manifest)
            if encoded(manifest) != raw_manifest or type(manifest) is not dict or set(manifest) != {"format_version", "request_sha256", "repository_label", "label", "review_question", "revisions", "plan", "primary", "context", "comparisons", "artifacts", "claims", "members", "material_gaps"} or manifest["format_version"] != FORMAT:
                fail("invalid packet manifest")
            members = manifest["members"]
            if type(members) is not list or len(members) != len(infos) - 1:
                fail("invalid member inventory")
            if {entry["name"] for entry in members} != set(names) - {"manifest.json"}:
                fail("member inventory differs from archive")
            for entry in members:
                if set(entry) != {"name", "size", "sha256"} or type(entry["size"]) is not int or entry["size"] < 0 or not SHA.fullmatch(entry["sha256"]):
                    fail("invalid member record")
                with archive.open(entry["name"]) as stream:
                    data = stream.read(MEMBER_LIMIT + 1)
                if len(data) != entry["size"] or digest(data) != entry["sha256"]:
                    fail("packet member changed")
            gaps = manifest["material_gaps"]
            if type(gaps) is not list or any(type(gap) is not dict or set(gap) != {"artifact_id", "availability"} or gap["availability"] not in {"missing", "referenced"} for gap in gaps):
                fail("invalid gap inventory")
            declared = [{"artifact_id": item["id"], "availability": item["availability"]} for item in manifest["artifacts"] if item["availability"] != "included"]
            if gaps != declared:
                fail("gap inventory differs from artifacts")
            return {"status": "built-with-gaps" if gaps else "built", "packet": str(path), "manifest_sha256": actual_digest, "material_gaps": gaps}
    except (OSError, zipfile.BadZipFile, UnicodeError, ValueError, KeyError, TypeError, EOFError):
        fail("packet is unavailable or malformed", "invalid")


def render_index(request: dict, primary: list[dict], artifacts: list[dict], gaps: list[dict], members: dict[str, bytes]) -> bytes:
    lines = ["# Review material packet", "", "This packet inventories selected material. It does not decide whether claims or CI results are valid.", "", "## Revisions", ""]
    for role, oid in request["revisions"].items():
        lines.append(f"- {markdown(role)}: `{oid}`")
    lines += ["", "## Primary files", ""]
    for item in primary:
        path = item["path"]
        for role in ("baseline", "candidate"):
            member = item.get(role, {}).get("member")
            if member:
                lines.append(f"- {role} {markdown(path)}: [complete file]({quote(member, safe='/')})")
            else:
                lines.append(f"- {role} {markdown(path)}: absent")
    lines += ["", "## Evidence", ""]
    for item in artifacts:
        member = item.get("member")
        suffix = f" [local bytes]({quote(member, safe='/')})" if member else ""
        lines.append(f"- {item['id']}: {item['availability']}{suffix}")
    lines += ["", "## Caller supplied claim associations", ""]
    for claim in request["claims"]:
        lines.append(f"- {markdown(claim['id'])}: {', '.join(claim['artifacts']) or 'unassociated'}")
    lines += ["", f"Primary patch: [complete patch]({quote('changes/baseline-candidate.patch')})", "", f"Declared gaps: {len(gaps)}", ""]
    return "\n".join(lines).encode("utf-8")


def build(repo_root: Path, request_path: Path, evidence_root: Path | None, output: Path) -> dict:
    request, request_bytes = load_request(request_path)
    repo_root = repo_root.absolute()
    output = output.absolute()
    no_symlink_ancestors(repo_root)
    no_symlink_ancestors(output.parent)
    if output.suffix.lower() != ".zip" or not output.parent.is_dir() or output.exists() or output.is_symlink():
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
    resolved_output = output.resolve(strict=False)
    for root in (repo_root, evidence_root):
        if root is not None and (resolved_output == root.resolve() or root.resolve() in resolved_output.parents or resolved_output in root.resolve().parents):
            fail("output overlaps an input root")
    git = GitRepository(repo_root)
    revisions = {role: RepositoryRevision(oid) for role, oid in request["revisions"].items()}
    entries = {role: git.revision_entries(revision, local_only=True) for role, revision in revisions.items()}
    members: dict[str, bytes] = {}
    def add(name: str, data: bytes) -> None:
        safe_name(name)
        if len(data) > MEMBER_LIMIT or len(members) >= COUNT_LIMIT or sum(map(len, members.values())) + len(data) > TOTAL_LIMIT:
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
    changed = sorted(path for path in baseline.keys() | candidate.keys() if baseline.get(path) != candidate.get(path))
    primary: list[dict] = []
    selected = sorted(set(changed) | {RepositoryPath.parse(path) for path in request["context"]})
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
    patch = git_output(repo_root, ("diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--binary", "--full-index", "--no-color", revisions["baseline"].oid, revisions["candidate"].oid, "--"), max_output_bytes=MEMBER_LIMIT, local_only=True)
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
        differences = sorted(path for path in candidate.keys() | other.keys() if candidate.get(path) != other.get(path))
        scopes = comparison["scopes"]
        def detail(path: RepositoryPath) -> dict:
            result = {"path": str(path)}
            for side, inventory in (("candidate", candidate), (role, other)):
                if path in inventory:
                    mode, oid = inventory[path]
                    result[side] = {"mode": mode, "blob": oid}
            return result
        within = [path for path in differences if any(str(path) == scope or str(path).startswith(scope + "/") for scope in scopes)]
        report = {"revision": role, "scopes": scopes, "equal_within_scopes": not within, "differences_within_scopes": [detail(path) for path in within], "differences_outside_scopes": [detail(path) for path in differences if path not in within]}
        add(f"comparisons/{role}.json", encoded(report))
        comparisons.append(report)
    artifacts: list[dict] = []
    gaps: list[dict] = []
    for artifact in request["artifacts"]:
        origin = artifact["origin"]
        item = {"id": artifact["id"], "role": artifact["role"], "subject": artifact.get("subject"), "origin": origin}
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
            if data is not None and "expected_sha256" in origin and digest(data) != origin["expected_sha256"]:
                fail("local evidence digest differs from expected")
            item["hash_basis"] = "expected" if "expected_sha256" in origin else "recorded"
        if item["availability"] == "included":
            prefix = "records" if origin["kind"] == "git-file" else "evidence"
            member = f"{prefix}/{item['id']}/{origin['path'].split('/')[-1]}"
            add(member, data)
            item["member"] = member
        else:
            gaps.append({"artifact_id": item["id"], "availability": item["availability"]})
        artifacts.append(item)
    add("INDEX.md", render_index(request, primary, artifacts, gaps, members))
    check_names([*members, "manifest.json"])
    manifest = {"format_version": FORMAT, "request_sha256": digest(request_bytes), "repository_label": request["repository_label"], "label": request["label"], "review_question": request["review_question"], "revisions": request["revisions"], "plan": {**request["plan"], "member": plan_member}, "primary": primary, "context": request["context"], "comparisons": comparisons, "artifacts": artifacts, "claims": request["claims"], "members": [{"name": name, "size": len(data), "sha256": digest(data)} for name, data in sorted(members.items())], "material_gaps": gaps}
    raw_manifest = encoded(manifest)
    if len(raw_manifest) > MEMBER_LIMIT or sum(map(len, members.values())) + len(raw_manifest) > TOTAL_LIMIT:
        fail("manifest exceeds packet limit", "unsupported")
    descriptor, staged = tempfile.mkstemp(prefix=".review-evidence-", suffix=".zip", dir=output.parent)
    published = False
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="review-evidence")
    commands = parser.add_subparsers(dest="command", required=True)
    builder = commands.add_parser("build")
    builder.add_argument("--repo-root", type=Path, required=True)
    builder.add_argument("--request", type=Path, required=True)
    builder.add_argument("--evidence-root", type=Path)
    builder.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = build(args.repo_root, args.request, args.evidence_root, args.output)
        print(json.dumps(result, sort_keys=True))
        return 1 if result["material_gaps"] else 0
    except PacketError as error:
        print(json.dumps({"status": error.kind, "message": str(error)}, sort_keys=True))
        return 2
    except GitRepositoryError as error:
        print(json.dumps({"status": error.failure.kind, "message": "Git material unavailable or unsupported"}, sort_keys=True))
        return 2
    except (OSError, zipfile.BadZipFile):
        print(json.dumps({"status": "unavailable", "message": "local filesystem operation failed"}, sort_keys=True))
        return 2


__all__ = ("build", "main")
