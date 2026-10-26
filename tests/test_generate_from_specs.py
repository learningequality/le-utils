# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib.util
import json
import os
import shutil
import subprocess
from collections import OrderedDict

import pytest

_script = importlib.util.spec_from_file_location("generate_from_specs", os.path.join(os.path.dirname(__file__), "..", "scripts", "generate_from_specs.py"))
generate_from_specs = importlib.util.module_from_spec(_script)
_script.loader.exec_module(generate_from_specs)


def spec(**overrides):
    base = {
        "namedtuple": {"name": "Format", "fields": ["id", "mimetype"], "getter": "getformat"},
        "records": [
            {
                "constant": "MP4",
                "label": "MP4 Video",
                "field_constants": ["mimetype"],
                "id": "mp4",
                "mimetype": "video/mp4",
            },
        ],
        "choices_order": ["MP4"],
    }
    base.update(overrides)
    return base


def assert_spec_raises(tmp_path, invalid_spec):
    output_file = str(tmp_path / "formats.py")
    with pytest.raises(ValueError):
        generate_from_specs.write_namedtuple_python_file(output_file, "FileFormats", invalid_spec)
    assert not os.path.exists(output_file)


def mp4_record(**overrides):
    record = spec()["records"][0].copy()
    record.update(overrides)
    return record


def test_constant_shadowing_record_constant_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(constants={"MP4": "avi"}))


def test_constant_shadowing_field_constant_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(constants={"MP4_MIMETYPE": "video/avi"}))


def test_field_constant_shadowing_record_constant_raises(tmp_path):
    records = [
        mp4_record(constant="MP4_MIMETYPE", id="a", field_constants=[]),
        mp4_record(id="mp4"),
    ]
    assert_spec_raises(tmp_path, spec(records=records, choices_order=["MP4_MIMETYPE", "MP4"]))


def test_duplicate_record_constant_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(records=[mp4_record(), mp4_record(id="mp4b")]))


def test_duplicate_record_id_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(records=[mp4_record(), mp4_record(constant="MP4B")]))


def test_choices_order_with_undefined_record_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(choices_order=["MP4", "NOPE"]))


def test_choices_order_omitting_record_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(records=[mp4_record(), mp4_record(constant="WEBM", id="webm")]))


def test_choices_order_repeating_record_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(choices_order=["MP4", "MP4"]))


def test_tuple_with_undefined_constant_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(tuples={"VIDEO": ["MP4", "AVI"]}))


def test_tuple_repeating_constant_raises(tmp_path):
    assert_spec_raises(tmp_path, spec(tuples={"VIDEO": ["MP4", "MP4"]}))


def test_record_missing_field_raises(tmp_path):
    record = mp4_record()
    del record["mimetype"]
    assert_spec_raises(tmp_path, spec(records=[record]))


def write_and_exec(tmp_path, valid_spec):
    output_file = str(tmp_path / "formats.py")
    generate_from_specs.write_namedtuple_python_file(output_file, "FileFormats", valid_spec)
    namespace = {}
    with open(output_file) as f:
        exec(f.read(), namespace)
    return namespace


def test_tuple_with_defined_constants_is_written(tmp_path):
    namespace = write_and_exec(tmp_path, spec(constants={"AVI": "avi"}, tuples={"VIDEO": ["MP4", "AVI"]}))
    assert namespace["VIDEO"] == ("mp4", "avi")


def test_generate_list_yields_records(tmp_path):
    namespace = write_and_exec(tmp_path, spec())
    records = list(namespace["generate_list"]({"webm": {"mimetype": "video/webm"}}))
    assert records == [namespace["Format"](id="webm", mimetype="video/webm")]


def test_spec_without_choices_order_omits_choices(tmp_path):
    valid_spec = spec()
    del valid_spec["choices_order"]
    namespace = write_and_exec(tmp_path, valid_spec)
    assert "choices" not in namespace
    assert namespace["FORMATLIST"] == [namespace["Format"](id="mp4", mimetype="video/mp4")]


def test_spec_without_getter_omits_getter(tmp_path):
    valid_spec = spec(namedtuple={"name": "Format", "fields": ["id", "mimetype"]})
    namespace = write_and_exec(tmp_path, valid_spec)
    assert "getformat" not in namespace
    assert namespace["FORMATLIST"] == [namespace["Format"](id="mp4", mimetype="video/mp4")]


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_js_exports_constants_and_records(tmp_path):
    output_file = tmp_path / "Formats.mjs"
    generate_from_specs.write_namedtuple_js_file(str(output_file), "FileFormats", spec(constants={"AVI": "avi"}))
    script = "import constants, {{ FORMATLIST }} from {!r}; console.log(JSON.stringify([constants, FORMATLIST]));".format(output_file.as_uri())
    output = subprocess.check_output(["node", "--input-type=module", "-e", script])
    constants, records = json.loads(output.decode("utf-8"), object_pairs_hook=OrderedDict)
    assert list(constants.items()) == [("MP4", "mp4"), ("MP4_MIMETYPE", "video/mp4"), ("AVI", "avi")]
    assert records == [{"id": "mp4", "mimetype": "video/mp4"}]
