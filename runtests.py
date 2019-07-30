#! /usr/bin/env python
# Adopted from Django REST Framework:
# https://github.com/tomchristie/django-rest-framework/blob/master/runtests.py
from __future__ import print_function

import os
import subprocess
import sys

import pytest

PACKAGE_NAME = 'dj'
TESTS = 'tests'
PYTEST_ARGS = {
    'default': [
        TESTS, '-s', '--tb=short', '-rw'
    ],
    'fast': [
        TESTS, '-s', '--tb=short', '-q', '-rw'
    ],
}

PACKAGES = [PACKAGE_NAME, TESTS]

sys.path.append(os.path.dirname(__file__))


def exit_on_failure(ret, message=None):
    if ret:
        sys.exit(ret)


def lint_main(cmd, args):
    print('Linting code')
    ret = subprocess.call(cmd + args)
    print('Lint failed' if ret else 'Lint passed')
    return ret


def split_class_and_function(string):
    class_string, function_string = string.split('.', 1)
    return "%s and %s" % (class_string, function_string)


def is_function(string):
    # `True` if it looks like a test function is included in the string.
    return string.startswith('test_') or '.test_' in string


def is_class(string):
    # `True` if first character is uppercase - assume it's a class name.
    return string[0] == string[0].upper()


if __name__ == "__main__":
    linter = ['flake8']

    try:
        sys.argv.remove('--nolint')
    except ValueError:
        run_lint = True
    else:
        run_lint = False

    try:
        sys.argv.remove('--lintonly')
    except ValueError:
        run_tests = True
    else:
        run_tests = False

    try:
        sys.argv.remove('--fast')
    except ValueError:
        style = 'default'
    else:
        style = 'fast'
        run_lint = False

    if len(sys.argv) > 1:
        pytest_args = sys.argv[1:]
        first_arg = pytest_args[0]

        try:
            pytest_args.remove('--coverage')
        except ValueError:
            pass
        else:
            pytest_args = [
                '--cov-report',
                'xml',
                '--cov',
                PACKAGE_NAME
            ] + pytest_args

        if first_arg.startswith('-'):
            # `runtests.py [flags]`
            pytest_args = [TESTS] + pytest_args
        elif is_class(first_arg) and is_function(first_arg):
            # `runtests.py TestCase.test_function [flags]`
            expression = split_class_and_function(first_arg)
            pytest_args = [TESTS, '-k', expression] + pytest_args[1:]
        elif is_class(first_arg) or is_function(first_arg):
            # `runtests.py TestCase [flags]`
            # `runtests.py test_function [flags]`
            pytest_args = [TESTS, '-k', pytest_args[0]] + pytest_args[1:]
    else:
        pytest_args = PYTEST_ARGS[style]

    if run_tests:
        exit_on_failure(pytest.main(pytest_args))

    if run_lint:
        exit_on_failure(lint_main(linter, PACKAGES))
