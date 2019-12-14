# -*- coding: utf-8 -*-

# type: ignore  # noqa E800

import os
import shutil
import subprocess
import unittest

from pytest import mark

from cats_direct_piechart import (
    create_parser,
    fetch_cat_fact,
    fetch_cat_image,
    save_cat,
)


class TestCatsDirect(unittest.TestCase):  # noqa WPS230
    """cats_direct tester."""

    def setUp(self):
        """Sets up reused data."""
        self.test_file_data = {
            'index': 1010,
            'extension': 'jpg',
        }
        self.test_cat_fact = 'Test cat fact'

        self.store_dirname = 'students/piechart/4/temp'
        if (not os.path.exists(self.store_dirname)):
            os.mkdir(self.store_dirname)

        self.test_fact_path = '{0}/cat_{1}_fact.txt'.format(
            self.store_dirname,
            self.test_file_data['index'],
        )
        self.test_image_path = '{0}.{1}'.format(
            'test_image',
            self.test_file_data['extension'],
        )
        self.test_result_image_path = '{0}/cat_{1}_image.{2}'.format(
            self.store_dirname,
            self.test_file_data['index'],
            self.test_file_data['extension'],
        )
        self.http_exception_text = 'HTTP exception raised'

    def tearDown(self):
        """Cleanup."""
        shutil.rmtree(self.store_dirname)

    def test_parser(self):
        """Tests arguments parsing."""
        test_args = ['--count', '3']
        parsed = create_parser().parse_args(test_args)
        assert parsed.count == int(test_args[-1])

    @mark.remote_data
    def test_fetch_cat_fact(self):
        """Tests cat fact fetched result."""
        try:
            fact = fetch_cat_fact()
        except Exception:
            self.fail(self.http_exception_text)

        assert fact != ''

    @mark.remote_data
    def test_fetch_cat_image(self):
        """Tests cat image fetched result."""
        try:
            fetched = fetch_cat_image()
        except Exception:
            self.fail(self.http_exception_text)

        assert len(fetched) == 2
        assert fetched[0]

        content_length = fetched[1].headers['Content-length']

        try:
            int_content_length = int(content_length)
        except Exception:
            self.fail('Unexpected non-int data in Content-length header:')

        assert int_content_length > 0

    def test_save_cat(self):
        """Performs save_cat with test data and compares the result."""
        assert os.path.isfile(self.test_image_path)

        with open(self.test_image_path, 'rb') as test_image:
            save_cat(
                index=self.test_file_data['index'],
                fact=self.test_cat_fact,
                image=(self.test_file_data['extension'], test_image),
            )

    def test_integration(self):
        """Integration."""
        command_str = 'python students/piechart/4/cats_direct_piechart.py --count=1'  # noqa: E501
        assert subprocess.call(command_str, shell=True) == 0  # noqa: S602


if __name__ == '__main__':
    unittest.main()
