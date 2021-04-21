# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from le_utils.constants import file_formats

# assert that if something is .mp4 or .webm, then it is a video file; and so on for audio, doc, etc.


def test_known_formats():
    format_obj = file_formats.getformat("webm")
    assert format_obj is not None, "webm not found"
    assert format_obj.id == "webm", "Wrong id"
    assert format_obj.mimetype == "video/webm", "Wrong mimetype"

    format_obj = file_formats.getformat("graphie")
    assert format_obj is not None, "graphie not found"
    assert format_obj.id == "graphie", "Wrong id"
    assert format_obj.mimetype == ".graphie", "Wrong mimetype"

    format_obj = file_formats.getformat("gif")
    assert format_obj is not None, "gif not found"
    assert format_obj.id == "gif", "Wrong id"
    assert format_obj.mimetype == "image/gif", "Wrong mimetype"


def test_unknown_formats():
    format_obj = file_formats.getformat("unknown-id")
    assert format_obj is None, "Unknown format code returned non-None"
