"""Run a unittest suite across cores, one `python -m unittest` process per test module.

unittest still discovers and runs every test. This module only starts one
worker per test module, at most --jobs at a time, and adds up what they report.
It fails when a worker fails, and when the workers together ran a different
number of tests than one serial discovery finds, so no test can disappear.

    PYTHONPATH=. python3 -m tools.standards_engine.tests.parallel_unittest

The Engine suite is the default; -s selects another suite's test directory.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

# Runs in a child interpreter started like `python -m unittest`, so discovery
# imports test modules exactly as a worker will and never into this process.
DISCOVER = r'''
import json, os, sys, unittest
modules = {}
class Loader(unittest.TestLoader):
    def loadTestsFromModule(self, module, *args, **options):
        tests = super().loadTestsFromModule(module, *args, **options)
        name = os.path.basename(module.__file__)
        modules[name] = modules.get(name, 0) + tests.countTestCases()
        return tests
def cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item
suite = Loader().discover(sys.argv[1], pattern=sys.argv[2], top_level_dir=sys.argv[3] or None)
for case in cases(suite):
    # A module that cannot be imported is one failing test named after it.
    if type(case).__name__ == '_FailedTest':
        name = case._testMethodName.rsplit('.', 1)[-1] + '.py'
        modules[name] = modules.get(name, 0) + 1
print('DISCOVERED ' + json.dumps({'total': suite.countTestCases(), 'modules': modules}))
'''
RAN = re.compile(r'^Ran (\d+) tests? in ', re.MULTILINE)
DURATION = re.compile(r'^(\d+\.\d+)s\s+(\S.*)$')


def discover(arguments: argparse.Namespace) -> dict:
    """Count the tests of every module with one serial discovery in a child interpreter."""
    child = subprocess.run(
        [sys.executable, '-c', DISCOVER, arguments.start_directory, arguments.pattern,
         arguments.top_level_directory or ''],
        capture_output=True, text=True)
    lines = [line for line in child.stdout.splitlines() if line.startswith('DISCOVERED ')]
    if child.returncode != 0 or not lines:
        raise SystemExit(f'Test discovery failed.\n{child.stdout}{child.stderr}')
    return json.loads(lines[-1].removeprefix('DISCOVERED '))


def run_module(arguments: argparse.Namespace, module: str) -> dict:
    command = [sys.executable, '-m', 'unittest', 'discover', '-s', arguments.start_directory, '-p', module]
    if arguments.top_level_directory:
        command += ['-t', arguments.top_level_directory]
    if arguments.durations is not None:
        command += ['--durations', str(arguments.durations)]
    if arguments.verbose:
        command.append('-v')
    started = time.monotonic()
    worker = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace')
    ran = RAN.findall(worker.stdout)
    return {'module': module, 'status': worker.returncode, 'output': worker.stdout,
            'ran': int(ran[-1]) if ran else 0, 'seconds': time.monotonic() - started}


def durations(output: str) -> list[tuple[float, str]]:
    """The per-test times unittest printed under `Slowest test durations`."""
    rows, listing = [], False
    for line in output.splitlines():
        if line == 'Slowest test durations':
            listing = True
        elif listing and (match := DURATION.match(line)):
            rows.append((float(match[1]), match[2]))
        elif listing and line.startswith('Ran '):
            listing = False
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-s', '--start-directory', default=os.path.relpath(Path(__file__).resolve().parent),
                        help='Directory to discover tests in; default: the Engine tests beside this module.')
    parser.add_argument('-p', '--pattern', default='test*.py')
    parser.add_argument('-t', '--top-level-directory')
    parser.add_argument('-j', '--jobs', type=int,
                        help='Worker processes at a time; default: the cores this process may use.')
    parser.add_argument('--durations', type=int, metavar='N',
                        help='Show the N slowest tests of the whole suite (0 shows all); needs Python 3.12.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Run workers with -v and show every worker\'s output, not only failures.')
    arguments = parser.parse_args(argv)
    if arguments.durations is not None and sys.version_info < (3, 12):
        parser.error('--durations needs Python 3.12 or newer')
    available = len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else os.cpu_count() or 1
    jobs = arguments.jobs if arguments.jobs is not None else available
    if jobs < 1:
        parser.error('--jobs must be at least 1')

    started = time.monotonic()
    discovered = discover(arguments)
    modules = sorted(discovered['modules'])
    if not discovered['total']:
        print(f'No tests discovered in {arguments.start_directory}.')
        return 1
    print(f'Running {discovered["total"]} tests from {len(modules)} modules in {arguments.start_directory}, '
          f'{min(jobs, len(modules))} at a time.', flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for future in as_completed([pool.submit(run_module, arguments, module) for module in modules]):
            result = future.result()
            results.append(result)
            expected = discovered['modules'][result['module']]
            if result['status'] == 0 and result['ran'] != expected:
                result['status'] = f'ran {result["ran"]} of {expected} discovered tests'
            passed = result['status'] == 0
            print(f'{"ok" if passed else "FAILED":6} {result["module"]}: {result["ran"]} tests in '
                  f'{result["seconds"]:.1f}s', flush=True)
            if arguments.verbose or not passed:
                print(f'{"-" * 70}\n{result["output"].rstrip()}\n{"-" * 70}', flush=True)

    if arguments.durations is not None:
        rows = sorted((row for result in results for row in durations(result['output'])), reverse=True)
        print('\nSlowest test durations')
        for seconds, name in rows[:arguments.durations or None]:
            print(f'{seconds:.3f}s'.ljust(11) + name)
    failed = sorted(result['module'] for result in results if result['status'] != 0)
    ran = sum(result['ran'] for result in results)
    print(f'\nRan {ran} tests in {time.monotonic() - started:.1f}s ({len(modules)} modules, '
          f'{min(jobs, len(modules))} at a time); serial discovery found {discovered["total"]}.')
    if ran != discovered['total']:
        print(f'FAILED: {discovered["total"] - ran} discovered tests did not run.')
        return 1
    if failed:
        print(f'FAILED (modules={len(failed)}): {", ".join(failed)}')
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
