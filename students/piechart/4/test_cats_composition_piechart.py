# -*- coding: utf-8 -*-

# type: ignore  # noqa E800

import os
import shutil
import unittest

from pytest.mark import remote_data

import cats_composition_piechart


class TestCatsComposition(unittest.TestCase):
    """cats_composition tester."""

    def setUp(self):
        """Setup."""
        self.temp_dir = 'students/piechart/4/temp'
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        self.test_file_amount = 1

    def tearDown(self):
        """Tear down."""
        shutil.rmtree(self.temp_dir)

    @remote_data
    def test_main(self):
        """Tests main."""
        assert os.path.exists(self.temp_dir)

        fact_file = '{0}/cat_{1}_fact.txt'.format(
            self.temp_dir,
            self.test_file_amount,
        )
        if os.path.exists(fact_file):
            os.remove(fact_file)

        cat_processor = cats_composition_piechart.CatProcessor(
            cats_composition_piechart.fetch_cat_fact,
            cats_composition_piechart.fetch_cat_image,
            cats_composition_piechart.save_cat,
        )
        cats_composition_piechart.main(
            self.test_file_amount,
            process_cat=cat_processor,
            show_information=print,  # noqa: T002
        )

        assert os.stat(fact_file).st_size > 0


if __name__ == '__main__':
    unittest.main()
