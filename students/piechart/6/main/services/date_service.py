# -*- coding: utf-8 -*-

import datetime

DATE_FORMAT = '%Y-%m-%d'


def today() -> str:
    """Generates today str object."""
    return datetime.datetime.today().strftime(DATE_FORMAT)


def date_object(date) -> datetime:
    """Converts str to date object."""
    return datetime.datetime.strptime(date, DATE_FORMAT)
