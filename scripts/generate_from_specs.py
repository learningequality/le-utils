"""
generate_from_specs
Builds or rebuilds the labels py files assigning ids to the labels
"""
from __future__ import unicode_literals

import json
import os
import re
import string
import sys
from collections import OrderedDict
from glob import glob
from hashlib import md5
from uuid import UUID
from uuid import uuid3

from pkg_resources import get_distribution

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


root_label = md5()
root_label.update("Kolibri labels".encode("utf-8"))

root_namespace = UUID(hex=root_label.hexdigest())

pascal_case_pattern = re.compile(r"(?<!^)(?=[A-Z])")

js_output_dir = os.path.join(os.path.dirname(__file__), "..", "js")

js_labels_output_dir = os.path.join(js_output_dir, "labels")

py_output_dir = os.path.join(os.path.dirname(__file__), "..", "le_utils", "constants")

py_labels_output_dir = os.path.join(
    os.path.dirname(__file__), "..", "le_utils", "constants", "labels"
)


def pascal_to_snake(name):
    return pascal_case_pattern.sub("_", name).lower()


def snake_to_pascal(name):
    return "".join(a.title() for a in name.split("_"))


CHARACTERS = string.ascii_letters + string.digits + "#" + "&"


def _from_uuid(uuid):
    """
    :params uuid: UUID
    :returns: character string that represents the UUID
    """
    # With a length of 12 for the hex number, we would need approximately
    # 24000 labels to have a 1 in a million chance of a collision.
    # Numbers derived using the formula for the generalized birthday problem:
    # https://en.wikipedia.org/wiki/Birthday_problem#The_generalized_birthday_problem
    # n=sqrt(2*d*ln(1/(1-p))
    # where d is the number of combinations of d digits, p is the probability
    # So for 12 digits, d = 16^12
    # p = 0.000001 for one in a million
    data = int(uuid.hex[:12], 16)
    res = []
    while data > 0 or not res:
        res += CHARACTERS[(data & 0x3F)]
        data >>= 6
    res.reverse()
    return "".join(res)


def generate_identifier(namespace, label):
    if sys.version_info[0] < 3:
        label = label.encode("utf-8")
    return uuid3(namespace, label)


def generate_key(identifier, previous=None):
    key = _from_uuid(identifier)
    if previous is None:
        return key
    return "{}.{}".format(previous, key)


def handle_array(labels, namespace, previous=None):
    output = {}
    for label in sorted(labels):
        identifier = generate_identifier(namespace, label)
        output[label] = generate_key(identifier, previous)
    return output


def handle_object(element, namespace, previous=None):
    output = {}
    for key, value in sorted(element.items(), key=lambda t: t[0]):
        handler = handle_object if isinstance(value, dict) else handle_array
        identifier = generate_identifier(namespace, key)
        new_key = generate_key(identifier, previous)
        output[key] = new_key
        new = handler(value, namespace, new_key)
        for k, v in new.items():
            if k not in output:
                output[k] = v
            else:
                raise ValueError("Duplicate label {}".format(k))
    return output


def read_labels_specs():  # noqa C901
    labels_spec_files = glob(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "spec",
            "labels-*.json",
        )
    )
    label_outputs = OrderedDict()
    for labels_spec_file in labels_spec_files:
        with open(labels_spec_file) as json_labels_spec_file:
            labels_spec = json.load(json_labels_spec_file)
            for label_type, labels in sorted(labels_spec.items(), key=lambda t: t[0]):
                handler = handle_object if isinstance(labels, dict) else handle_array
                namespace = generate_identifier(root_namespace, label_type)
                output = handler(labels, namespace)
                if label_type not in label_outputs:
                    label_outputs[label_type] = OrderedDict()
                for key, value in sorted(output.items(), key=lambda t: t[0]):
                    if key not in label_outputs[label_type]:
                        label_outputs[label_type][key] = value
    return label_outputs


def read_constants_specs():
    constants_spec_files = glob(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "spec",
            "constants-*.json",
        )
    )
    constants_outputs = {}
    for constants_spec_file in constants_spec_files:
        with open(constants_spec_file) as json_constants_spec_file:
            constants_spec = json.load(json_constants_spec_file)
            key = snake_to_pascal(constants_spec_file.split("-")[-1].split(".")[0])
            constants_outputs[key] = OrderedDict(
                [(a.upper(), a) for a in sorted(constants_spec)]
            )
    return constants_outputs


def write_python_file(output_file, name, ordered_output):
    with open(output_file, "w") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# Generated by scripts/generate_from_specs.py\n")
        f.write("from __future__ import unicode_literals\n")
        f.write("\n")
        f.write("# {}\n".format(name))
        f.write("\n")
        for key, value in ordered_output.items():
            f.write('{} = "{}"\n'.format(key, value))
        f.write("\n")
        f.write("choices = (\n")
        for key in ordered_output.keys():
            f.write('    ({}, "{}"),\n'.format(key, key.replace("_", " ").title()))
        f.write(")\n")
        f.write("\n")
        f.write("{}LIST = [\n".format(name.upper()))
        for key in ordered_output.keys():
            f.write("    {},\n".format(key))
        f.write("]\n")


def write_js_header(f):
    f.write("// -*- coding: utf-8 -*-\n")
    f.write("// Generated by scripts/generate_from_specs.py\n")


def write_js_file(output_file, name, ordered_output):
    with open(output_file, "w") as f:
        write_js_header(f)
        f.write("// {}\n".format(name))
        f.write("\n")
        f.write("export default {\n")
        for key, value in ordered_output.items():
            f.write('    {key}: "{value}",\n'.format(key=key, value=value))
        f.write("};\n")


def write_labels_src_files(label_outputs):
    for label_type, ordered_output in label_outputs.items():
        py_output_file = os.path.join(
            py_labels_output_dir, "{}.py".format(pascal_to_snake(label_type))
        )
        write_python_file(py_output_file, label_type, ordered_output)

        js_output_file = os.path.join(js_labels_output_dir, "{}.js".format(label_type))
        write_js_file(js_output_file, label_type, ordered_output)


def write_constants_src_files(constants_outputs):
    for constant_type, ordered_output in constants_outputs.items():
        py_output_file = os.path.join(
            py_output_dir, "{}.py".format(pascal_to_snake(constant_type))
        )
        write_python_file(py_output_file, constant_type, ordered_output)

        js_output_file = os.path.join(js_output_dir, "{}.js".format(constant_type))
        write_js_file(js_output_file, constant_type, ordered_output)


def set_package_json_version():
    python_version = get_distribution("le-utils").version

    package_json = os.path.join(js_output_dir, "package.json")

    with open(package_json, "r") as f:
        package = json.load(f)

    package["version"] = python_version

    with open(package_json, "w") as f:
        output = json.dumps(package, indent=2, sort_keys=True)
        firstline = True
        for line in output.split("\n"):
            if firstline:
                firstline = False
            else:
                f.write("\n")
            f.write(line.rstrip())


if __name__ == "__main__":
    labels_to_write = read_labels_specs()

    constants_to_write = read_constants_specs()

    write_labels_src_files(labels_to_write)

    write_constants_src_files(constants_to_write)

    set_package_json_version()
