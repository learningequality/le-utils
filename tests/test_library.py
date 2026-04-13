# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from le_utils.constants import library


def test_library_constants_exist():
    assert library.KOLIBRI == "KOLIBRI"
    assert library.COMMUNITY == "COMMUNITY"


def test_library_choices():
    choices_dict = dict(library.choices)
    assert library.KOLIBRI in choices_dict
    assert library.COMMUNITY in choices_dict
    assert choices_dict[library.KOLIBRI] == "Kolibri"
    assert choices_dict[library.COMMUNITY] == "Community"


def test_LIBRARYLIST_exists():
    assert library.LIBRARYLIST, "LIBRARYLIST did not generate properly"
