# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import inspect
import io
import json
import os

from le_utils.constants import content_kinds
from le_utils.constants import file_formats
from le_utils.constants import format_presets
from le_utils.constants import languages
from le_utils.constants import licenses

IMPORTS = {"json", "logging", "pkgutil", "namedtuple", "unicode_literals"}

EXCLUDED = {
    "content_kinds": {"file_formats"},
    "languages": {
        "logger",
        "lang_name",
        "lang_obj",
        "new_items",
        "new_name",
        "new_names",
        "simple_name",
        "lang_native_name",
        "new_native_name",
        "new_native_names",
        "simple_native_name",
    },
}

PINNED_PATH = os.path.join(os.path.dirname(__file__), "pinned_api.json")

with io.open(PINNED_PATH, encoding="utf-8") as f:
    PINNED = json.load(f)


def encode(value):
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, tuple) and hasattr(value, "_fields"):
        cls = type(value)
        properties = sorted(name for name, attr in vars(cls).items() if isinstance(attr, property))
        return {
            "namedtuple": cls.__name__,
            "fields": [[field, encode(getattr(value, field))] for field in value._fields],
            "properties": {name: encode(getattr(value, name)) for name in properties},
        }
    if isinstance(value, tuple):
        return {"tuple": [encode(item) for item in value]}
    if isinstance(value, list):
        return {"list": [encode(item) for item in value]}
    if isinstance(value, dict):
        return {"dict": {key: encode(item) for key, item in value.items()}}
    if inspect.isclass(value) and hasattr(value, "_fields"):
        return {"namedtuple_class": value.__name__, "fields": list(value._fields)}
    if inspect.isfunction(value):
        return {"function": str(inspect.signature(value))}
    raise TypeError("Cannot encode {!r}".format(value))


def encode_module(module):
    excluded = IMPORTS | EXCLUDED.get(module.__name__.rsplit(".", 1)[-1], set())
    return {key: encode(value) for key, value in vars(module).items() if not key.startswith("_") and key not in excluded}


def test_file_formats_api_is_pinned():
    assert encode_module(file_formats) == PINNED["file_formats"]


def test_licenses_api_is_pinned():
    assert encode_module(licenses) == PINNED["licenses"]


def test_content_kinds_api_is_pinned():
    assert encode_module(content_kinds) == PINNED["content_kinds"]


def test_format_presets_api_is_pinned():
    assert encode_module(format_presets) == PINNED["format_presets"]


def test_languages_api_is_pinned():
    assert encode_module(languages) == PINNED["languages"]
