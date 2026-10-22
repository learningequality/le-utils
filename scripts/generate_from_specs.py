"""
generate_from_specs
Builds or rebuilds the labels py files assigning ids to the labels
"""

from __future__ import unicode_literals

import json
import os
import re
import string
import subprocess
import sys
from collections import OrderedDict
from glob import glob
from hashlib import md5
from uuid import UUID
from uuid import uuid3

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

py_labels_output_dir = os.path.join(py_output_dir, "labels")


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
            if isinstance(constants_spec, dict):
                constants_outputs[key] = constants_spec
            else:
                # assume it's a list and convert to an OrderedDict
                constants_outputs[key] = OrderedDict([(a.upper(), a) for a in sorted(constants_spec)])
    return constants_outputs


def read_schema_specs():
    schema_spec_files = glob(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "spec",
            "schema-*.json",
        )
    )
    schema_outputs = {}
    constants_outputs = {}
    for schema_spec_file in schema_spec_files:
        with open(schema_spec_file) as json_schema_spec_file:
            key = snake_to_pascal(schema_spec_file.split("-")[-1].split(".")[0])
            schema_outputs[key] = json_schema_spec_file.read()

        json_schema = json.loads(schema_outputs[key])
        # find definitions that should be exported as constants
        for json_schema_def in json_schema.get("definitions", {}).values():
            export_name = json_schema_def.get("$exportConstants")
            if export_name is not None and "enum" in json_schema_def:
                constants_outputs.update({snake_to_pascal(export_name): OrderedDict([(a.upper(), a) for a in sorted(json_schema_def.get("enum"))])})

    return schema_outputs, constants_outputs


def write_python_header(f):
    f.write("# -*- coding: utf-8 -*-\n")
    f.write("# Generated by scripts/generate_from_specs.py\n")
    f.write("from __future__ import unicode_literals\n")
    f.write("\n")


def write_python_file(output_file, name, ordered_output, schema=None):
    with open(output_file, "w") as f:
        write_python_header(f)
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
        if schema:
            f.write("\n")
            f.write("SCHEMA = {}\n".format(repr(json.loads(schema))))


def write_js_header(f):
    f.write("// -*- coding: utf-8 -*-\n")
    f.write("// Generated by scripts/generate_from_specs.py\n")


def write_js_file(output_file, name, ordered_output, schema=None):
    with open(output_file, "w") as f:
        write_js_header(f)
        f.write("// {}\n".format(name))
        f.write("\n")
        if ordered_output:
            f.write("export default {\n")
            for key, value in ordered_output.items():
                f.write('    {key}: "{value}",\n'.format(key=key, value=value))
            f.write("};\n")
        if schema:
            f.write("\n")
            f.write("export const SCHEMA = {};\n".format(schema))


def define_constant(constants, constant, value):
    if constant in constants:
        raise ValueError("Constant {} is defined twice".format(constant))
    constants[constant] = value


def namedtuple_constants(spec):
    constants = OrderedDict()
    ids = set()
    for record in spec["records"]:
        for field in spec["namedtuple"]["fields"]:
            if field not in record:
                raise ValueError("Record {} has no field {}".format(record["constant"], field))
        if record["id"] in ids:
            raise ValueError("Record id {} is defined twice".format(record["id"]))
        ids.add(record["id"])
        define_constant(constants, record["constant"], record["id"])
        for field in record.get("field_constants", []):
            define_constant(constants, "{}_{}".format(record["constant"], field.upper()), record[field])
    for constant, value in spec.get("constants", {}).items():
        define_constant(constants, constant, value)
    return constants


def namedtuple_tuples(spec, constants):
    tuples = spec.get("tuples", {})
    for tuple_name, members in tuples.items():
        if len(set(members)) != len(members):
            raise ValueError("Tuple {} repeats a constant".format(tuple_name))
        for member in members:
            if member not in constants:
                raise ValueError("Tuple {} references undefined constant {}".format(tuple_name, member))
    return tuples


def namedtuple_choices(spec):
    if "choices_order" not in spec:
        return None
    labels = {record["constant"]: record["label"] for record in spec["records"]}
    if len(set(spec["choices_order"])) != len(spec["choices_order"]):
        raise ValueError("choices_order repeats a record")
    for constant in spec["choices_order"]:
        if constant not in labels:
            raise ValueError("choices_order references undefined record {}".format(constant))
    for constant in labels:
        if constant not in spec["choices_order"]:
            raise ValueError("choices_order omits record {}".format(constant))
    return [(constant, labels[constant]) for constant in spec["choices_order"]]


def write_python_choices(f, choices):
    f.write("choices = (\n")
    for constant, label in choices:
        f.write("    ({}, {!r}),\n".format(constant, label))
    f.write(")\n")


def write_python_records(f, spec):
    type_name = spec["namedtuple"]["name"]
    fields = spec["namedtuple"]["fields"]
    f.write("class {name}(namedtuple({name!r}, {fields!r})):\n".format(name=type_name, fields=fields))
    f.write("    pass\n")
    f.write("\n")
    f.write("\n")
    f.write("def generate_list(constantlist):\n")
    f.write("    for id, record in constantlist.items():\n")
    f.write("        yield {}(id=id, **record)\n".format(type_name))
    f.write("\n")
    f.write("\n")
    f.write("{}LIST = [\n".format(type_name.upper()))
    for record in spec["records"]:
        arguments = ", ".join("{}={!r}".format(field, record[field]) for field in fields)
        f.write("    {}({}),\n".format(type_name, arguments))
    f.write("]\n")


def write_python_getter(f, spec):
    upper = spec["namedtuple"]["name"].upper()
    f.write("\n")
    f.write("_{name}LOOKUP = {{r.id: r for r in {name}LIST}}\n".format(name=upper))
    f.write("\n")
    f.write("\n")
    f.write("def {}(id, default=None):\n".format(spec["namedtuple"]["getter"]))
    f.write("    return _{}LOOKUP.get(id) or None\n".format(upper))


def write_namedtuple_python_file(output_file, name, spec):
    constants = namedtuple_constants(spec)
    tuples = namedtuple_tuples(spec, constants)
    choices = namedtuple_choices(spec)
    with open(output_file, "w") as f:
        write_python_header(f)
        f.write("from collections import namedtuple\n")
        f.write("\n")
        f.write("# {}\n".format(name))
        f.write("\n")
        for constant, value in constants.items():
            f.write("{} = {!r}\n".format(constant, value))
        for tuple_name, members in tuples.items():
            f.write("\n")
            f.write("{} = ({},)\n".format(tuple_name, ", ".join(members)))
        f.write("\n")
        if choices is not None:
            write_python_choices(f, choices)
            f.write("\n")
            f.write("\n")
        write_python_records(f, spec)
        if "getter" in spec["namedtuple"]:
            write_python_getter(f, spec)


def js_object(pairs):
    return "{{ {} }}".format(", ".join("{}: {}".format(key, json.dumps(value)) for key, value in pairs))


def write_namedtuple_js_file(output_file, name, spec):
    fields = spec["namedtuple"]["fields"]
    with open(output_file, "w") as f:
        write_js_header(f)
        f.write("// {}\n".format(name))
        f.write("\n")
        f.write("export default {\n")
        for constant, value in namedtuple_constants(spec).items():
            f.write("    {}: {},\n".format(constant, json.dumps(value)))
        f.write("};\n")
        f.write("\n")
        f.write("export const {}LIST = [\n".format(spec["namedtuple"]["name"].upper()))
        for record in spec["records"]:
            f.write("    {},\n".format(js_object((field, record[field]) for field in fields)))
        f.write("];\n")


def write_labels_src_files(label_outputs):
    output_files = []
    for label_type, ordered_output in label_outputs.items():
        py_output_file = os.path.join(py_labels_output_dir, "{}.py".format(pascal_to_snake(label_type)))
        write_python_file(py_output_file, label_type, ordered_output)
        output_files.append(py_output_file)

        js_output_file = os.path.join(js_labels_output_dir, "{}.js".format(label_type))
        write_js_file(js_output_file, label_type, ordered_output)
        output_files.append(js_output_file)
    return output_files


def write_constants_src_files(constants_outputs, schemas):
    output_files = []
    keys = set(list(constants_outputs.keys()) + list(schemas.keys()))

    for key in keys:
        constant_outputs = constants_outputs.get(key, {})
        schema = schemas.get(key, None)

        py_output_file = os.path.join(py_output_dir, "{}.py".format(pascal_to_snake(key)))
        js_output_file = os.path.join(js_output_dir, "{}.js".format(key))
        if "namedtuple" in constant_outputs:
            write_namedtuple_python_file(py_output_file, key, constant_outputs)
            write_namedtuple_js_file(js_output_file, key, constant_outputs)
        else:
            write_python_file(py_output_file, key, constant_outputs, schema=schema)
            write_js_file(js_output_file, key, constant_outputs, schema=schema)
        output_files += [py_output_file, js_output_file]
    return output_files


if __name__ == "__main__":
    labels_to_write = read_labels_specs()

    constants_to_write = read_constants_specs()

    schemas_to_write, schema_constants_to_write = read_schema_specs()
    constants_to_write.update(schema_constants_to_write)

    output_files = []

    output_files += write_labels_src_files(labels_to_write)

    output_files += write_constants_src_files(constants_to_write, schemas_to_write)

    py_files = [f for f in output_files if f.endswith(".py")]
    subprocess.call(["ruff", "check", "--fix"] + py_files)
    subprocess.call(["ruff", "format"] + py_files)
