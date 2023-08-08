import uuid

from le_utils.constants.uuid import KOLIBRI_ECOSYSTEM_UUID_NAMESPACE
from le_utils.uuid import generate_ecosystem_namespaced_uuid


def test_namespace_does_not_change():
    assert KOLIBRI_ECOSYSTEM_UUID_NAMESPACE == "237627f4-3601-11ee-a67c-595de72bede7"


def test_generate_ecosystem_namespaced_uuid():
    assert generate_ecosystem_namespaced_uuid(
        "https://studio.learningequality.org"
    ) == uuid.UUID("2d04ed86-aa8c-519f-ae78-a250e03d8482")
