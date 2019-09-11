import unittest
from runtests import TestRunner

SAMPLES_PATH = '/Users/gingy/ITMO/4_course/testing/itmo-2019/students/lerastromtsova/1/samples/'


class Test(unittest.TestCase):

    def test_collect_tests(self):
        test_runner = TestRunner()
        test_runner.collect_tests(SAMPLES_PATH)
        self.assertEqual(test_runner.tests, [SAMPLES_PATH+'test_factorial.py', SAMPLES_PATH+'test_gcd.py'])

    def test_run_tests(self):
        test_runner = TestRunner()
        test_runner.collect_tests(SAMPLES_PATH)
        test_runner.run_tests()
        self.assertEqual(test_runner.passed, [SAMPLES_PATH+'test_factorial.py'])
        self.assertEqual(test_runner.failed, [SAMPLES_PATH+'test_gcd.py'])


if __name__ == '__main__':
    unittest.main()
