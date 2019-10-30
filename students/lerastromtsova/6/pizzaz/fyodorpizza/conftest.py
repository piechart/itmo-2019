# -*- coding: utf-8 -*-

import os

import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizzaz.settings')


def pytest_configure():
    """`Pytest` automatically calls this function once when tests are run."""
    settings.DEBUG = False
    django.setup()
