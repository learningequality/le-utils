# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pkgutil

from le_utils.constants import format_presets


def test_format_presets_are_synced():
    presetlookup = json.loads(
        pkgutil.get_data("le_utils", "resources/presetlookup.json").decode("utf-8")
    )
    presets_json = set(dict(presetlookup).keys())
    presets_python = set(dict(format_presets.choices).keys())
    assert presets_json == presets_python


def test_PRESETLIST_exists():
    assert format_presets.PRESETLIST, "PRESETLIST did not genereate properly"
