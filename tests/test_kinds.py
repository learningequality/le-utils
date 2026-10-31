# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from le_utils.constants import content_kinds
from le_utils.constants import file_formats


def test_MAPPING_keys_are_file_format_ids():
    format_ids = {fmt.id for fmt in file_formats.FORMATLIST}
    assert set(content_kinds.MAPPING) <= format_ids
