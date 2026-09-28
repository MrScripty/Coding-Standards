"""Closed version-one request decoding and semantic links."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from .common import REQUEST_LIMIT, fail, safe_name


def load_request(path: Path) -> tuple[dict, bytes]:
    if path.is_symlink():
        fail("request path is a symlink", "unsupported")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            fail("request is not a regular file", "unsupported")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            raw = stream.read(REQUEST_LIMIT + 1)
    finally:
        os.close(descriptor)
    if len(raw) > REQUEST_LIMIT:
        fail("request exceeds limit", "unsupported")

    def unique_pairs(pairs: list[tuple[str, object]]) -> dict:
        value: dict = {}
        for key, item in pairs:
            if key in value:
                fail("request contains duplicate JSON keys")
            value[key] = item
        return value

    def reject_constant(_: str) -> None:
        fail("request contains a nonfinite number")

    try:
        request = json.loads(
            raw, object_pairs_hook=unique_pairs, parse_constant=reject_constant
        )
        schema = json.loads(
            Path(__file__).with_name("request-schema.json").read_bytes()
        )
        Draft202012Validator(schema).validate(request)
    except (ValueError, UnicodeError):
        fail("invalid request JSON")
    except ValidationError:
        fail("request does not match version 1 schema")

    def require_scalar(value: object) -> None:
        if type(value) is str:
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                fail("request contains unsupported Unicode", "unsupported")
        elif type(value) is list:
            for item in value:
                require_scalar(item)
        elif type(value) is dict:
            for key, item in value.items():
                require_scalar(key)
                require_scalar(item)

    require_scalar(request)
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
        if (
            "reported_subject_revision" in artifact
            and "reported_repository" not in artifact
        ):
            fail("reported subject requires a repository label")
        if "subject" in artifact and "reported_subject_revision" in artifact:
            fail("evidence has contradictory subject identities")
        origin = artifact["origin"]
        if origin["kind"] == "git-file" and "reported_repository" in artifact:
            fail("local Git evidence cannot claim a foreign repository")
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
        if (
            alias not in revisions
            or alias in {"baseline", "candidate"}
            or alias in compared
        ):
            fail("invalid comparison revision")
        compared.add(alias)
        for scope in item["scopes"]:
            safe_name(scope)
    return request, raw
