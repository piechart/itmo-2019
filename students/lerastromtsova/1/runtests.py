import glob
import subprocess

PREFIX_TESTS = 'test_'
FILE_TYPE_TESTS = '.py'
SAMPLES_PATH = '/Users/gingy/ITMO/4_course/testing/itmo-2019/students/lerastromtsova/1/samples/'

class TestRunner:

    tests = []
    passed = []
    failed = []

    def collect_tests(self, path):
        self.tests = glob.glob(f'{path}/{PREFIX_TESTS}*{FILE_TYPE_TESTS}')

    def run_tests(self):
        for test in self.tests:
            try:
                subprocess.check_call(f'python {test}', shell=True)
                self.passed.append(test)
                print(f'{test} - ok')
            except subprocess.CalledProcessError:
                print(f'{test} - fail')
                self.failed.append(test)


if __name__ == "__main__":
    test_runner = TestRunner()
    test_runner.collect_tests(SAMPLES_PATH)
    test_runner.run_tests()
