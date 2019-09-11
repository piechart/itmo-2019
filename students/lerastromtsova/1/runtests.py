import glob
import subprocess

PREFIX_TESTS = 'test_'
FILE_TYPE_TESTS = '.py'
SAMPLES_PATH = '/Users/gingy/ITMO/4_course/testing/itmo-2019' \
               '/students/lerastromtsova/1/samples/'


class TestRunner(object):
    """
        Class for running tests in any given directory.

        Test filenames should start with PREFIX defined above
        and have an extension FILE_TYPE_TESTS defined above
    """

    tests = []
    passed = []
    failed = []

    def collect_tests(self, path):
        """ Collects the tests from a given path. """
        self.tests.extend(glob.glob(f'{path}/{PREFIX_TESTS}*{FILE_TYPE_TESTS}'))

    def run_tests(self):
        """
            Runs the tests from self.tests.

            Adds them to either passed or failed.
        """
        for test in self.tests:
            try:
                subprocess.check_call(f'python {test}', shell=True)
                self.passed.append(test)
                print(f'{test} - ok')
            except subprocess.CalledProcessError:
                print(f'{test} - fail')
                self.failed.append(test)


if __name__ == '__main__':
    test_runner = TestRunner()
    test_runner.collect_tests(SAMPLES_PATH)
    test_runner.run_tests()
