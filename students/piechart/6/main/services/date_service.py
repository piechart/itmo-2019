# -*- coding: utf-8 -*-

import datetime

DATE_FORMAT = '%Y-%m-%d'


def today():
    """Generates today date object."""
    return datetime.datetime.today().strftime(DATE_FORMAT)


def date_object(date):
    """Converts str to date object."""
    return datetime.datetime.strptime(date, DATE_FORMAT)
