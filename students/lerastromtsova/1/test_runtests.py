import unittest
from runtests import TestRunner

SAMPLES_PATH = '/Users/gingy/ITMO/4_course/testing/itmo-2019/students/lerastromtsova/1/samples/'
NON_EXISTING_PATH = '/Users/gingy/sometests'
NO_TESTS_PATH = '/Users/gingy/ITMO/4_course/testing'


class Test(unittest.TestCase):

    def test_collect_tests(self):

        # test happy path
        test_runner = TestRunner()
        test_runner.collect_tests(SAMPLES_PATH)
        self.assertEqual(test_runner.tests, [SAMPLES_PATH+'test_factorial.py', SAMPLES_PATH+'test_gcd.py'])

        # test if path does not exist
        test_runner = TestRunner()
        test_runner.collect_tests(NON_EXISTING_PATH)
        self.assertRaises(FileNotFoundError)

        # test is there are no tests
        test_runner = TestRunner()
        test_runner.collect_tests(NO_TESTS_PATH)
        self.assertEqual(test_runner.tests, [])
        
    def test_run_tests(self):
        test_runner = TestRunner()
        test_runner.collect_tests(SAMPLES_PATH)
        test_runner.run_tests()
        self.assertEqual(test_runner.passed, [SAMPLES_PATH+'test_factorial.py'])
        self.assertEqual(test_runner.failed, [SAMPLES_PATH+'test_gcd.py'])


if __name__ == '__main__':
    unittest.main()
