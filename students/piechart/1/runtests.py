import os
import glob
import imp

PY_EXTENSION = ".py"
TEST_PREFIX = "test_"


def find_files(directory, pattern):
    return glob.glob(f"{directory}/{pattern}", recursive=True)


def import_module(target_file):
    global PY_EXTENSION
    name = os.path.basename(target_file).replace(PY_EXTENSION, "")

    if len(name) == 0 or (not os.path.exists(target_file)):
        return None

    module = imp.load_source(name, target_file)
    return module


def extract_tests(module):
    global TEST_PREFIX
    if module is None:
        return None
    return dict(filter(lambda elem: elem[0].startswith(TEST_PREFIX), vars(module).items()))


def perform_testing(target_dir=""):
    if len(target_dir) == 0:
        target_dir = os.getcwd()

    test_files = find_files(target_dir, f"{TEST_PREFIX}*{PY_EXTENSION}")

    for test_file in test_files:
        module = import_module(test_file)

        if module is None:
            continue

        tests = extract_tests(module)

        for test in tests.items():
            try:
                test[1]()
                test_result = "ok"
            except AssertionError:
                test_result = "fail"

            print(f"{test_file} - {test[0]} - {test_result}")


if __name__ == '__main__':
    perform_testing(input("Input target dir (Enter for current): "))
