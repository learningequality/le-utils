import uuid

from le_utils.constants.uuid import KOLIBRI_ECOSYSTEM_UUID_NAMESPACE

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def generate_ecosystem_namespaced_uuid(hostname_or_url):
    """
    Generate a UUID for a given URL, namespaced by the Kolibri ecosystem UUID namespace.
    :param hostname_or_url: A URL to generate a UUID-- only the netloc/host is used
    :return: A namespaced UUID
    """
    _url = urlparse(hostname_or_url)

    return uuid.uuid5(uuid.UUID(KOLIBRI_ECOSYSTEM_UUID_NAMESPACE), _url.netloc)
