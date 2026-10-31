# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from le_utils.constants import content_kinds
from le_utils.constants import file_formats
from le_utils.constants import format_presets


def test_MAPPING_keys_are_file_format_ids():
    format_ids = {fmt.id for fmt in file_formats.FORMATLIST}
    assert set(content_kinds.MAPPING) <= format_ids


def test_PRESETLIST_kinds_are_kind_ids():
    kind_ids = {kind.id for kind in content_kinds.KINDLIST}
    assert {preset.kind for preset in format_presets.PRESETLIST if preset.kind} <= kind_ids
