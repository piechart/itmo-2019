# -*- coding: utf-8 -*-

import unittest

from runtests import TestRunner

SAMPLES_PATH = '/Users/gingy/ITMO/4_course/testing/itmo-2019/students/lerastromtsova/1/samples/'  # noqa: E501
NON_EXISTING_PATH = '/Users/gingy/sometests/'
NO_TESTS_PATH = '/Users/gingy/ITMO/4_course/testing'
FACTORIAL_TEST = '{0}test_factorial.py'.format(SAMPLES_PATH)
GCD_TEST = '{0}test_gcd.py'.format(SAMPLES_PATH)


class Test(unittest.TestCase):
    """Class for performing unit tests on my testing framework."""

    def test_collect_tests_nonexistent(self):
        """Test the 'collect_tests' method, path does not exist."""
        test_runner = TestRunner()
        test_runner.collect_tests(NON_EXISTING_PATH)
        self.assertRaises(FileNotFoundError)

    def test_collect_tests_no_tests(self):
        """Test the 'collect_tests' method, there are no test files."""
        test_runner = TestRunner()
        tests = test_runner.collect_tests(NO_TESTS_PATH)
        self.assertEqual(tests, [])

    def test_collect_tests_happy(self):
        """Test the 'collect_tests' method, happy path."""
        test_runner = TestRunner()
        tests = test_runner.collect_tests(SAMPLES_PATH)

        self.assertEqual(tests, [FACTORIAL_TEST, GCD_TEST])

    def test_run_tests(self):
        """Test the 'run_tests' method."""
        test_runner = TestRunner()
        tests = test_runner.collect_tests(SAMPLES_PATH)
        test_runner.run_tests(tests)
        self.assertEqual(test_runner.passed, [FACTORIAL_TEST])
        self.assertEqual(test_runner.failed, [GCD_TEST])


if __name__ == '__main__':
    unittest.main()
