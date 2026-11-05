# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from le_utils.constants import file_formats
from le_utils.constants import format_presets


def test_PRESETLIST_allowed_formats_are_file_format_ids():
    format_ids = {file_format.id for file_format in file_formats.FORMATLIST}
    for preset in format_presets.PRESETLIST:
        assert set(preset.allowed_formats) <= format_ids, preset.id


def test_RENDERABLE_PRESETS_ORDER_matches_PRESETLIST_ids():
    preset_ids = {preset.id for preset in format_presets.PRESETLIST if not preset.supplementary}
    assert set(format_presets.RENDERABLE_PRESETS_ORDER) == preset_ids


def test_RENDERABLE_PRESETS_ORDER_excludes_supplementary_presets():
    assert "video_thumbnail" not in format_presets.RENDERABLE_PRESETS_ORDER
    assert "qti_thumbnail" not in format_presets.RENDERABLE_PRESETS_ORDER


def test_RENDERABLE_PRESETS_ORDER_index_is_stable():
    # Pin known bit positions: reordering silently breaks Studio/Kolibri's
    # already-persisted File.included_presets bitmask values.
    assert format_presets.RENDERABLE_PRESETS_ORDER.index("high_res_video") == 0
    assert format_presets.RENDERABLE_PRESETS_ORDER.index("low_res_video") == 1
    assert format_presets.RENDERABLE_PRESETS_ORDER.index("video_dependency") == 2
    assert format_presets.RENDERABLE_PRESETS_ORDER.index("qti") == 13
    assert format_presets.RENDERABLE_PRESETS_ORDER.index("kpub") == 17
