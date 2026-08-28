from __future__ import annotations

import importlib.metadata
import re
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = ROOT / "tools" / "standards_contracts"

EXPECTED = {
    "attrs": (
        "26.1.0",
        "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309",
    ),
    "jsonschema": (
        "4.26.0",
        "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
    ),
    "jsonschema-specifications": (
        "2025.9.1",
        "98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe",
    ),
    "referencing": (
        "0.37.0",
        "381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231",
    ),
    "typing-extensions": (
        "4.16.0",
        "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8",
    ),
}
RPDS_HASHES = {
    "3.11": "9c1255b302953c86a486b81d330d5ee1d5bd937691ce271b6be0ef0e299eaab7",
    "3.12": "ecabd69db66de867690f9797f2f8fa27ba501bbc24540cbdbdc649cd15888ba6",
}


class DependencyResolutionTest(unittest.TestCase):
    def test_manifest_declares_only_the_two_direct_dependencies(self) -> None:
        manifest = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text())
        self.assertEqual(manifest["project"]["requires-python"], ">=3.11,<3.13")
        self.assertEqual(
            manifest["project"]["dependencies"],
            ["jsonschema==4.26.0", "referencing==0.37.0"],
        )

    def test_lock_contains_only_the_reviewed_exact_artifacts(self) -> None:
        lock = (PACKAGE_ROOT / "requirements.lock").read_text()
        entries = re.findall(
            r"(?m)^([a-z][a-z0-9-]*)==([^ ;\\]+)(?: ; ([^\\\n]+))? \\\n"
            r"    --hash=sha256:([0-9a-f]{64})$",
            lock,
        )
        ordinary = {
            name: (version, digest)
            for name, version, marker, digest in entries
            if not marker
        }
        rpds = {
            re.fullmatch(r'python_version == "(3\.1[12])"', marker).group(1): digest
            for name, version, marker, digest in entries
            if name == "rpds-py" and version == "2026.6.3"
        }
        self.assertEqual(ordinary, EXPECTED)
        self.assertEqual(rpds, RPDS_HASHES)
        self.assertEqual(len(entries), 7)

    def test_isolated_environment_uses_the_exact_selected_runtime(self) -> None:
        if sys.version_info[:2] not in {(3, 11), (3, 12)}:
            self.skipTest("dependency lock admits CPython 3.11 and 3.12 only")
        expected_versions = {name: version for name, (version, _) in EXPECTED.items()}
        expected_versions["rpds-py"] = "2026.6.3"
        for distribution, expected in expected_versions.items():
            with self.subTest(distribution=distribution):
                self.assertEqual(importlib.metadata.version(distribution), expected)

        from jsonschema import Draft202012Validator
        from referencing import Registry

        self.assertEqual(
            Draft202012Validator.META_SCHEMA["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(len(Registry()), 0)


if __name__ == "__main__":
    unittest.main()
