"""Prepared manifest memory is owned and bounded with the compiled data graph."""
from dataclasses import replace
import unittest

from tools.standards_engine.standards_engine.compiled_cache import _retained_size
from tools.standards_metadata.tests.test_prepared_suite_dependencies import load_fixture


class CoveragePreparationAccountingTest(unittest.TestCase):
    def test_dependency_index_is_charged_before_any_cache_hit(self):
        prepared, _ = load_fixture()
        direct = replace(prepared)
        unprepared_size = _retained_size(direct, 32 * 1024 * 1024)
        prepared_size = _retained_size(prepared, 32 * 1024 * 1024)
        self.assertIsNotNone(prepared_size)
        self.assertIsNotNone(unprepared_size)
        self.assertGreater(prepared_size, unprepared_size)
        self.assertIsNone(_retained_size(prepared, prepared_size - 1))
        self.assertEqual(_retained_size(prepared, prepared_size), prepared_size)

    def test_dependency_lookups_do_not_grow_retained_memory(self):
        prepared, _ = load_fixture()
        size = _retained_size(prepared, 32 * 1024 * 1024)
        for _ in range(5):
            for suite in prepared.suites:
                prepared.dependency(suite.id)
        self.assertEqual(_retained_size(prepared, 32 * 1024 * 1024), size)


if __name__ == "__main__":
    unittest.main()
