from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from tools.standards_verifier.standards_verifier.python_packages import (
    audit_python_packages,
    execute_python_package_contract,
)


class PythonPackageContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        subprocess.run(("git", "init", "-q"), cwd=self.root, check=True)
        self.write_package(
            "b",
            "b-package",
            (),
            """
            value = 7
            __all__ = ("value",)
            """,
        )
        self.write_package(
            "a",
            "a-package",
            ("b-package",),
            """
            from tools.b.b import value
            run = value
            __all__ = ("run",)
            """,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

    def write_package(
        self,
        directory: str,
        project: str,
        dependencies: tuple[str, ...],
        source: str,
    ) -> None:
        dependency_values = ", ".join(f'"{item}"' for item in dependencies)
        self.write(
            f"tools/{directory}/pyproject.toml",
            f"""
            [project]
            name = "{project}"
            version = "0.1.0"
            requires-python = ">=3.11,<3.13"
            dependencies = [{dependency_values}]

            [tool.standards-package]
            schema-version = 1
            public-import-root = "tools.{directory}.{directory}"
            repository-entrypoints = []
            """,
        )
        self.write(f"tools/{directory}/{directory}/__init__.py", source)

    def stage(self) -> None:
        subprocess.run(("git", "add", "-A"), cwd=self.root, check=True)

    def codes(self) -> tuple[str, ...]:
        self.stage()
        return tuple(item.code for item in audit_python_packages(self.root))

    def test_exact_public_import_and_dependency_closure_pass(self) -> None:
        self.assertEqual(self.codes(), ())
        self.assertEqual(execute_python_package_contract(self.root), ())

    def test_public_execution_failure_is_distinct(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            "raise RuntimeError('public import failed')\nrun = 1\n__all__ = ('run',)\n",
        )
        self.stage()
        self.assertEqual(
            tuple(item.code for item in execute_python_package_contract(self.root)),
            ("PYTHON_PACKAGE.PUBLIC_EXECUTION",),
        )

    def test_private_child_and_unexported_root_name_are_distinct(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            from tools.b.b.private import value
            __all__ = ("value",)
            """,
        )
        self.assertIn("PYTHON_PACKAGE.PRIVATE_IMPORT", self.codes())

        self.write(
            "tools/a/a/__init__.py",
            """
            from tools.b.b import missing
            __all__ = ("missing",)
            """,
        )
        self.assertIn("PYTHON_PACKAGE.UNEXPORTED_IMPORT", self.codes())

    def test_star_and_dynamic_import_bypasses_are_rejected(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            from tools.b.b import *
            __all__ = ("value",)
            """,
        )
        self.assertIn("PYTHON_PACKAGE.STAR_IMPORT", self.codes())

        self.write(
            "tools/a/a/__init__.py",
            """
            loaded = __import__("tools.b.b")
            __all__ = ("loaded",)
            """,
        )
        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

        variants = (
            """
            from importlib import import_module as load
            loaded = load("tools.b.b")
            __all__ = ("loaded",)
            """,
            """
            import importlib as machinery
            loaded = machinery.import_module("tools.b.b")
            __all__ = ("loaded",)
            """,
            """
            from builtins import __import__ as load
            loaded = load("tools.b.b")
            __all__ = ("loaded",)
            """,
            """
            load = __import__
            loaded = load("tools.b.b")
            __all__ = ("loaded",)
            """,
            """
            loaded = eval("__import__('tools.b.b')")
            __all__ = ("loaded",)
            """,
        )
        for source in variants:
            with self.subTest(source=source.strip().splitlines()[0]):
                self.write("tools/a/a/__init__.py", source)
                self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_dependency_and_source_ownership_are_exact(self) -> None:
        self.write_package(
            "a",
            "a-package",
            (),
            """
            from tools.b.b import value
            run = value
            __all__ = ("run",)
            """,
        )
        self.assertIn("PYTHON_PACKAGE.DEPENDENCY_CLOSURE", self.codes())

        self.write("tools/unowned.py", "__all__ = ('value',)\nvalue = 1\n")
        self.assertIn("PYTHON_PACKAGE.UNOWNED_SOURCE", self.codes())


if __name__ == "__main__":
    unittest.main()
