# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pkgutil

from le_utils.constants import content_kinds


def test_content_kind_extensions_are_synced():
    kindlookup = json.loads(
        pkgutil.get_data("le_utils", "resources/kindlookup.json").decode("utf-8")
    )
    kinds_json = set(dict(kindlookup).keys())
    kinds_py = set(dict(content_kinds.choices).keys())
    assert kinds_json == kinds_py


def test_KINDLIST_exists():
    assert content_kinds.KINDLIST, "KINDLIST did not genereate properly"
