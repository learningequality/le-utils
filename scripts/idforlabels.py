"""
idforlabels
Builds or rebuilds the labelslooup.json assigning ids to the labels that do not have it
"""
from __future__ import unicode_literals

import json
import os
import string
from hashlib import md5
from uuid import UUID
from uuid import uuid3

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


root_label = md5()
root_label.update("Kolibri labels")

root_namespace = UUID(hex=root_label.hexdigest())


CHARACTERS = string.letters + string.digits + "#" + "&"


def _from_uuid(uuid):
    """
    :params uuid: UUID
    :returns: character string that represents the UUID
    """
    data = int(uuid.hex[:8], 16)
    res = []
    while data > 0 or not res:
        res += CHARACTERS[(data & 0x3F)]
        data >>= 6
    res.reverse()
    return "".join(res)


def generate_identifier(namespace, label):
    return uuid3(namespace, label.encode("utf-8"))


def generate_key(identifier, previous=None):
    key = _from_uuid(identifier)
    if previous is None:
        return key
    return "{}.{}".format(previous, key)


def handle_array(labels, namespace, previous=None):
    output = {}
    for label in labels:
        identifier = generate_identifier(namespace, label)
        output[label] = generate_key(identifier, previous)
    return output


def handle_object(element, namespace, previous=None):
    output = {}
    for key, value in element.items():
        handler = handle_object if isinstance(value, dict) else handle_array
        identifier = generate_identifier(namespace, key)
        new_key = generate_key(identifier, previous)
        output[key] = new_key
        output.update(handler(value, namespace, new_key))
    return output


if __name__ == "__main__":
    templates_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "le_utils",
        "resources",
        "labelstemplatelookup.json",
    )
    with open(templates_file) as json_templates_file:
        templates = json.load(json_templates_file)

    output_file = os.path.join(
        os.path.dirname(__file__), "..", "le_utils", "resources", "labelslookup.json"
    )

    output = {}

    for label_type, labels in templates.items():
        handler = handle_object if isinstance(labels, dict) else handle_array
        namespace = generate_identifier(root_namespace, label_type)
        output[label_type] = handler(labels, namespace)

    with open(output_file, "w") as json_labels_file:
        json.dump(output, json_labels_file, sort_keys=True, indent=2)
