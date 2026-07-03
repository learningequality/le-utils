# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pkgutil

from le_utils.constants import format_presets


def test_format_presets_are_synced():
    presetlookup = json.loads(pkgutil.get_data("le_utils", "resources/presetlookup.json").decode("utf-8"))
    presets_json = set(dict(presetlookup).keys())
    presets_python = set(dict(format_presets.choices).keys())
    assert presets_json == presets_python


def test_PRESETLIST_exists():
    assert format_presets.PRESETLIST, "PRESETLIST did not genereate properly"


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
