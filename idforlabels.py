"""
idforlabels
Builds or rebuilds the labelslooup.json assigning ids to the labels that do not have it
"""
import json
import os

from uuid import uuid4

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def handle_array(templates, labels, previous=None):
    for template in templates:
        if labels.get(template, None) is None:
            if previous is not None:
                labels[template] = "{}.{}".format(previous, uuid4().hex)
            else:
                labels[template] = uuid4().hex
    return labels


def handle_object(element, label, previous=None):
    for key in element.keys():
        to_handle = element[key]
        handler = handle_object if isinstance(to_handle, dict) else handle_array
        new_key = (
            uuid4().hex if previous is None else "{}.{}".format(previous, uuid4().hex)
        )
        key_label = label.get(key, [new_key, dict()])
        label[key] = [key_label[0], handler(to_handle, key_label[1], key_label[0])]
    return label


if __name__ == "__main__":
    templates_file = os.path.join("le_utils", "resources", "labelstemplatelookup.json")
    with open(templates_file) as json_templates_file:
        templates = json.load(json_templates_file)

    labels_file = os.path.join("le_utils", "resources", "labelslookup.json")
    try:
        with open(labels_file) as json_labels_file:
            labels = json.load(json_labels_file)
    except FileNotFoundError:
        labels = {}

    for label_type in templates.keys():
        to_handle = templates[label_type]
        handler = handle_object if isinstance(to_handle, dict) else handle_array
        labels[label_type] = handler(to_handle, labels.get(label_type, dict()))

    with open(labels_file, "w") as json_labels_file:
        json.dump(labels, json_labels_file, sort_keys=True, indent=2)
