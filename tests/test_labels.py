# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
from glob import glob


def handle_array(labels):
    output = labels
    return output


def handle_object(element):
    output = []
    for key, value in element.items():
        handler = handle_object if isinstance(value, dict) else handle_array
        output.append(key)
        output.extend(handler(value))
    return output


def read_labels_specs():
    labels_spec_files = glob(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "spec",
            "labels-*.json",
        )
    )
    for labels_spec_file in labels_spec_files:
        with open(labels_spec_file) as json_labels_spec_file:
            yield json.load(json_labels_spec_file)


def test_labels_unique():
    labels_specs = read_labels_specs()

    label_outputs = {}

    for labels_spec in labels_specs:
        for label_type, labels in labels_spec.items():
            handler = handle_object if isinstance(labels, dict) else handle_array
            if label_type not in label_outputs:
                label_outputs[label_type] = []
            spec_labels = handler(labels)
            assert len(spec_labels) == len(set(spec_labels))
            label_outputs[label_type].extend(spec_labels)

    for label_type, labels in label_outputs.items():
        label_outputs[label_type] = sorted(set(labels))

    all_labels = [label for labels in label_outputs.values() for label in labels]
    assert len(all_labels) == len(set(all_labels))
