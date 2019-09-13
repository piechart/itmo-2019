# -*- coding: utf-8 -*-

import glob
import subprocess  # noqa: S404

PREFIX_TESTS = 'test_'
FILE_TYPE_TESTS = '.py'


class TestRunner(object):
    """
    Class for running tests in any given directory.

    Test filenames should start with PREFIX_TESTS defined above
    and have an extension FILE_TYPE_TESTS defined above
    """

    passed = []
    failed = []

    def collect_tests(self, path):
        """Collects the tests from a given path."""
        name = '{0}/{1}*{2}'.format(path, PREFIX_TESTS, FILE_TYPE_TESTS)
        return glob.glob(name)

    def run_tests(self, tests):
        """
        Runs the tests with names from self.tests.

        Adds them to either passed or failed.
        """
        for test in tests:
            command = 'python {0}'.format(test)
            try:
                flag = subprocess.check_call(command, shell=True)  # noqa: S602
            except subprocess.CalledProcessError:
                flag = 1
            if flag:
                self.failed.append(test)
                print('{0} - fail'.format(test))  # noqa: T001
            else:
                self.passed.append(test)
                print('{0} - ok'.format(test))  # noqa: T001


if __name__ == '__main__':
    path = input('Enter path to directory with tests: ')  # noqa: S322, WPS421
    test_runner = TestRunner()
    tests = test_runner.collect_tests(path)
    test_runner.run_tests(tests)
