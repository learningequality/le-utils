# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
import json
import pkgutil

from le_utils.constants import file_formats
def test_file_format_extensions_are_synced():
    formatlookup = json.loads(pkgutil.get_data('le_utils', 'resources/formatlookup.json').decode('utf-8'))

    exts_formatlookup = set(dict(formatlookup).keys())
    exts_file_formats = set(dict(file_formats.choices).keys())

    assert exts_formatlookup == exts_file_formats

