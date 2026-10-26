# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from le_utils.constants import file_formats


def test_FORMATLIST_exists():
    assert file_formats.FORMATLIST, "FORMATLIST did not genereate properly"


def test_ARCHIVE_FORMATS_does_not_change():
    assert set(file_formats.ARCHIVE_FORMATS) == {"zip", "h5p", "epub", "kpub", "bloompub", "bloomd"}
