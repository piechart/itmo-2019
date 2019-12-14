
# -*- coding: utf-8 -*-

# type: ignore  # noqa E800

from typing import Callable, Tuple

from requests.packages import urllib3

from cats_direct_piechart import (
    create_parser,
    fetch_cat_fact,
    fetch_cat_image,
    save_cat,
)


class CatProcessor(object):
    """
    Knows exactly how to process cats.

    Only uses composition.
    """

    def __init__(
        self,
        fetch_text,
        fetch_image: Callable[[], Tuple[str, urllib3.HTTPResponse]],
        process_text_and_image: Callable[[int, str, Tuple[str, urllib3.HTTPResponse]], None]  # noqa E501
    ):
        """Saves dependencies into internal state."""
        self._fetch_text = fetch_text
        self._fetch_image = fetch_image
        self._process_text_and_image = process_text_and_image

    def __call__(self, index: int):
        """Runs the process of cat downloading."""
        return self._process_text_and_image(
            index,
            self._fetch_text(),
            self._fetch_image(),
        )


def main(
    cats_to_fetch: int,
    process_cat: Callable,
    show_information: Callable,
) -> None:
    """Fetches cats and saves the into temp folder."""
    if not cats_to_fetch:
        show_information('No cats :(')
        return

    for cat_index in range(1, cats_to_fetch + 1):
        process_cat(cat_index)
    show_information('Cats downloaded!')


if __name__ == '__main__':
    # Building dependencies:
    cat_processor = CatProcessor(fetch_cat_fact, fetch_cat_image, save_cat)

    # Building our main:
    main(
        create_parser().parse_args().count,
        process_cat=cat_processor,
        show_information=print,  # noqa: T002
    )
