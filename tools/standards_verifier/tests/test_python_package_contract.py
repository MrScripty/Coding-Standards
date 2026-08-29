from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.standards_verifier.standards_verifier.checks.python_package_contract import (
    _audit_fixture,
)
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
            schema-version = 2
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

    def test_entrypoint_executes_declared_operation_instead_of_help(self) -> None:
        self.write(
            "tools/a/pyproject.toml",
            """
            [project]
            name = "a-package"
            version = "0.1.0"
            requires-python = ">=3.11,<3.13"
            dependencies = ["b-package"]

            [tool.standards-package]
            schema-version = 2
            public-import-root = "tools.a.a"
            repository-entrypoints = [
              { path = "tools/a_entrypoint.py", arguments = ["--run"], fixture = "reviewed-repository", remove = [] },
            ]
            """,
        )
        self.write(
            "tools/a_entrypoint.py",
            """
            import sys
            if sys.argv[1:] != ["--run"]:
                raise SystemExit(2)
            print("operation completed")
            """,
        )
        self.stage()
        self.assertEqual(execute_python_package_contract(self.root), ())

        self.write(
            "tools/a_entrypoint.py",
            """
            import sys
            if sys.argv[1:] == ["--help"]:
                print("help")
                raise SystemExit(0)
            raise SystemExit(3)
            """,
        )
        self.stage()
        self.assertEqual(
            tuple(item.code for item in execute_python_package_contract(self.root)),
            ("PYTHON_PACKAGE.ENTRYPOINT_EXECUTION",),
        )

    def test_indexed_copy_excludes_untracked_ambient_files(self) -> None:
        self.write(
            "tools/a/pyproject.toml",
            """
            [project]
            name = "a-package"
            version = "0.1.0"
            requires-python = ">=3.11,<3.13"
            dependencies = ["b-package"]

            [tool.standards-package]
            schema-version = 2
            public-import-root = "tools.a.a"
            repository-entrypoints = [
              { path = "tools/indexed_copy.py", arguments = ["{fixture}"], fixture = "isolated-indexed-copy", remove = [] },
            ]
            """,
        )
        self.write(
            "tools/indexed_copy.py",
            """
            import pathlib
            import sys
            fixture = pathlib.Path(sys.argv[1])
            if (fixture / "ambient.txt").exists():
                raise SystemExit(4)
            print("indexed copy is isolated")
            """,
        )
        self.stage()
        self.write("ambient.txt", "untracked\n")

        self.assertEqual(execute_python_package_contract(self.root), ())

    def test_indexed_copy_uses_staged_bytes_not_worktree_bytes(self) -> None:
        self.write(
            "tools/a/pyproject.toml",
            """
            [project]
            name = "a-package"
            version = "0.1.0"
            requires-python = ">=3.11,<3.13"
            dependencies = ["b-package"]

            [tool.standards-package]
            schema-version = 2
            public-import-root = "tools.a.a"
            repository-entrypoints = [
              { path = "tools/indexed_copy.py", arguments = ["{fixture}"], fixture = "isolated-indexed-copy", remove = [] },
            ]
            """,
        )
        self.write(
            "tools/indexed_copy.py",
            """
            import pathlib
            import sys
            observed = (pathlib.Path(sys.argv[1]) / "indexed.txt").read_text()
            if observed != "staged\\n":
                raise SystemExit(4)
            print("indexed bytes are exact")
            """,
        )
        self.write("indexed.txt", "staged\n")
        self.stage()
        self.write("indexed.txt", "working tree\n")

        self.assertEqual(execute_python_package_contract(self.root), ())

    def test_fixture_construction_failure_is_a_typed_finding(self) -> None:
        self.write(
            "tools/a/pyproject.toml",
            """
            [project]
            name = "a-package"
            version = "0.1.0"
            requires-python = ">=3.11,<3.13"
            dependencies = ["b-package"]

            [tool.standards-package]
            schema-version = 2
            public-import-root = "tools.a.a"
            repository-entrypoints = [
              { path = "tools/indexed_copy.py", arguments = ["{fixture}"], fixture = "isolated-indexed-copy", remove = ["missing.txt"] },
            ]
            """,
        )
        self.write("tools/indexed_copy.py", "print('unreachable')\n")
        self.stage()

        self.assertEqual(
            tuple(item.code for item in execute_python_package_contract(self.root)),
            ("PYTHON_PACKAGE.ENTRYPOINT_FIXTURE",),
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
            """
            from _frozen_importlib import __import__ as load
            loaded = load("tools.b.b")
            __all__ = ("loaded",)
            """,
            """
            import _imp as machinery
            loaded = machinery.load_dynamic("tools.b.b", "fixture")
            __all__ = ("loaded",)
            """,
        )
        for source in variants:
            with self.subTest(source=source.strip().splitlines()[0]):
                self.write("tools/a/a/__init__.py", source)
                self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_sys_modules_import_capability_bypass_is_rejected(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            import sys
            load = getattr(sys.modules["builtins"], "__import__")
            loaded = load("tools.b.b")
            __all__ = ("loaded",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_later_class_binding_does_not_hide_sys_modules_bypass(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            import sys
            class Fixture:
                load = getattr(sys.modules["builtins"], "__import__")
                sys = object()
            __all__ = ("Fixture",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_method_does_not_close_over_class_sys_binding(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            import sys
            class Fixture:
                sys = object()
                def load(self):
                    return sys.modules["builtins"]
            __all__ = ("Fixture",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_class_comprehension_does_not_close_over_class_sys_binding(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            import sys
            class Fixture:
                sys = object()
                modules = [sys.modules[name] for name in ("builtins",)]
            __all__ = ("Fixture",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_shadowed_capability_names_are_not_treated_as_import_machinery(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            def use(eval, exec, __import__):
                return eval(1), exec(2), __import__(3)
            run = use(lambda value: value, lambda value: value, lambda value: value)
            __all__ = ("run",)
            """,
        )

        self.assertNotIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_later_module_binding_does_not_hide_builtin_capability_access(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            run = eval("1")
            eval = lambda value: value
            __all__ = ("run",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_assignment_rhs_precedes_module_and_class_target_binding(self) -> None:
        variants = (
            """
            eval = eval("40 + 2")
            __all__ = ("eval",)
            """,
            """
            class Fixture:
                eval = eval("40 + 2")
            __all__ = ("Fixture",)
            """,
        )
        for source in variants:
            with self.subTest(source=source.strip().splitlines()[0]):
                self.write("tools/a/a/__init__.py", source)
                self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_conditional_binding_does_not_hide_builtin_capability(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            if False:
                eval = lambda value: value
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_complete_conditional_benign_binding_is_preserved(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            condition = True
            if condition:
                eval = lambda value: value
            else:
                eval = lambda value: value + 1
            run = eval(1)
            __all__ = ("run",)
            """,
        )

        self.assertNotIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_conditional_deletion_may_restore_builtin_capability(self) -> None:
        variants = (
            """
            eval = lambda value: value
            if condition:
                del eval
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
            """
            eval = lambda value: value
            if condition:
                del eval
            else:
                eval = lambda value: value + 1
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
        )
        for source in variants:
            with self.subTest(has_else="else:" in source):
                self.write("tools/a/a/__init__.py", source)
                self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_supported_branch_exits_preserve_possible_unbinding(self) -> None:
        variants = (
            """
            eval = lambda value: value
            while condition:
                del eval
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
            """
            eval = lambda value: value
            for value in values:
                del eval
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
            """
            eval = lambda value: value
            try:
                del eval
            except RuntimeError:
                pass
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
        )
        for source in variants:
            with self.subTest(statement=source.splitlines()[2].strip()):
                self.write("tools/a/a/__init__.py", source)
                self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_simple_sys_alias_retains_capability_provenance(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            import sys
            registry = sys
            run = registry.modules["builtins"].__import__
            __all__ = ("run",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_conditional_sys_alias_retains_possible_capability(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            import sys
            condition = True
            if condition:
                registry = sys
            else:
                registry = object()
            run = registry.modules["builtins"].__import__
            __all__ = ("run",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_conditional_sys_alias_retains_provenance_in_nested_scope(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            import sys
            if condition:
                registry = sys
            def load():
                return registry.modules["builtins"].__import__
            __all__ = ("load",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_assignment_targets_bind_from_left_to_right(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            values = {}
            eval = values[eval] = lambda value: value
            run = eval(1)
            __all__ = ("run",)
            """,
        )

        self.assertNotIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_augmented_assignment_loads_bound_target_before_store(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            class Value:
                def __add__(self, other):
                    return other
            eval = Value()
            eval += eval
            __all__ = ("eval",)
            """,
        )

        self.assertNotIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_deleted_module_binding_restores_builtin_capability(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            eval = lambda value: value
            del eval
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_loaded_name_inside_assignment_target_is_not_a_binding(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            values = {}
            values[getattr] = 1
            run = getattr(__builtins__, "__import__")
            __all__ = ("run",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_exception_alias_is_a_benign_binding_inside_its_handler(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            try:
                raise ValueError("fixture")
            except ValueError as eval:
                run = str(eval)
            __all__ = ("run",)
            """,
        )

        self.assertNotIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_exception_alias_is_unbound_after_its_handler(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            try:
                raise ValueError("fixture")
            except ValueError as eval:
                pass
            run = eval("40 + 2")
            __all__ = ("run",)
            """,
        )

        self.assertIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_arbitrary_attributes_do_not_imply_import_machinery(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            class Fixture:
                def import_module(self, value):
                    return value
            run = Fixture().import_module(7)
            __all__ = ("run",)
            """,
        )

        self.assertNotIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_comprehension_targets_are_benign_lexical_bindings(self) -> None:
        self.write(
            "tools/a/a/__init__.py",
            """
            values = (lambda value: value,)
            run = [eval(1) for eval in values]
            modules = [sys.modules for sys in ()]
            __all__ = ("modules", "run")
            """,
        )

        self.assertNotIn("PYTHON_PACKAGE.DYNAMIC_IMPORT", self.codes())

    def test_verifier_git_fixtures_ignore_ambient_repository_overrides(self) -> None:
        case = {
            "id": "ambient-git",
            "consumer_dependencies": ["b-package"],
            "consumer_source": (
                "from tools.b.b import value\n"
                "run = value\n"
                '__all__ = ("run",)\n'
            ),
            "expected_codes": [],
        }
        self.write(
            "tools/a/pyproject.toml",
            """
            [project]
            name = "a-package"
            version = "0.1.0"
            requires-python = ">=3.11,<3.13"
            dependencies = ["b-package"]

            [tool.standards-package]
            schema-version = 2
            public-import-root = "tools.a.a"
            repository-entrypoints = [
              { path = "tools/fixture_entrypoint.py", arguments = ["{fixture}"], fixture = "isolated-git-repository", remove = [] },
            ]
            """,
        )
        self.write("tools/fixture_entrypoint.py", "print('fixture completed')\n")
        self.stage()

        with patch.dict(
            os.environ,
            {"GIT_DIR": "/unavailable", "GIT_INDEX_FILE": "/unavailable/index"},
        ):
            self.assertEqual(_audit_fixture(case), ())
            self.assertEqual(execute_python_package_contract(self.root), ())

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
