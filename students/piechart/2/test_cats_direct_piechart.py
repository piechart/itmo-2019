# -*- coding: utf-8 -*-

import os
import shutil
import unittest

import pytest
import urllib3

from itmo.second.cats_direct import (
    create_parser,
    fetch_cat_fact,
    fetch_cat_image,
    save_cat,
)

INDEX_STR = 'index'
EXTENSION_STR = 'extension'

class TestCatsDirect(unittest.TestCase):  # noqa WPS230
    """cats_direct tester."""

    def setUp(self):
        """Sets up reused data."""
        self.test_file_data = {
            INDEX_STR: 1010,
            EXTENSION_STR: 'jpg',
        }
        self.test_cat_fact = 'Test cat fact'

        self.store_dirname = 'students/piechart/2/temp'
        if (not os.path.exists(self.store_dirname)):
            os.mkdir(self.store_dirname)

        self.test_fact_path = '{0}/cat_{1}_fact.txt'.format(
            self.store_dirname,
            self.test_file_data[INDEX_STR],
        )
        self.test_image_path = '{0}.{1}'.format(
            'students/piechart/2/test_image',
            self.test_file_data[EXTENSION_STR],
        )
        self.test_result_image_path = '{0}/cat_{1}_image.{2}'.format(
            self.store_dirname,
            self.test_file_data[INDEX_STR],
            self.test_file_data[EXTENSION_STR],
        )
        self.http_exception_text = 'HTTP exception raised'

    def tearDown(self):
        """Cleanup."""
        shutil.rmtree(self.store_dirname)

    def test_parser(self):
        """Tests arguments parsing."""
        test_args = ['--count', '3']
        parsed = create_parser().parse_args(test_args)
        self.assertEqual(parsed.count, int(test_args[-1]))

    @pytest.mark.remote_data
    def test_fetch_cat_fact(self):
        """Tests cat fact fetched result."""
        try:
            fact = fetch_cat_fact()
        except Exception:
            self.fail(self.http_exception_text)

        self.assertIs(type(fact), str)
        self.assertNotEqual(fact, '')

    @pytest.mark.remote_data
    def test_fetch_cat_image(self):
        """Tests cat image fetched result."""
        try:
            fetched = fetch_cat_image()
        except Exception:
            self.fail(self.http_exception_text)

        self.assertEqual(len(fetched), 2)

        self.assertIs(type(fetched[0]), str)
        self.assertNotEqual(len(fetched[0]), 0)

        self.assertIs(type(fetched[1]), urllib3.response.HTTPResponse)
        content_length = fetched[1].headers['Content-length']
        self.assertNotEqual(content_length, '')

        try:
            int_content_length = int(content_length)
        except Exception:
            self.fail('Unexpected non-int data in Content-length header:')

        self.assertGreater(int_content_length, 0)

    def test_save_cat(self):
        """Performs save_cat with test data and compares the result."""
        self.assertTrue(os.path.isfile(self.test_image_path))

        with open(self.test_image_path, 'rb') as test_image:
            save_cat(
                index=self.test_file_data[INDEX_STR],
                fact=self.test_cat_fact,
                image=(self.test_file_data[EXTENSION_STR], test_image),
            )


if __name__ == '__main__':
    unittest.main()
