# -*- coding: utf-8 -*-

import os
import unittest

import pytest

from itmo.second import cats_composition


class TestCatsComposition(unittest.TestCase):
    """cats_composition tester."""

    def setUp(self):
        """Setup."""
        self.temp_dir = 'temp'
        self.test_file_amount = 1

    @pytest.mark.remote_data
    def test_main(self):
        """Tests main."""
        self.assertTrue(os.path.exists(self.temp_dir))

        fact_file = '{0}/cat_{1}_fact.txt'.format(
            self.temp_dir,
            self.test_file_amount,
        )
        if os.path.exists(fact_file):
            os.remove(fact_file)

        cat_processor = cats_composition.CatProcessor(
            cats_composition.fetch_cat_fact,
            cats_composition.fetch_cat_image,
            cats_composition.save_cat,
        )
        cats_composition.main(
            self.test_file_amount,
            process_cat=cat_processor,
            show_information=print,  # noqa: T002
        )

        self.assertTrue(os.path.exists(fact_file))
        self.assertGreater(os.stat(fact_file).st_size, 0)


if __name__ == '__main__':
    unittest.main()
