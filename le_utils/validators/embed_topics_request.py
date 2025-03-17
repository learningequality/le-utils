import jsonschema

from le_utils.constants.embed_topics_request import SCHEMA
from le_utils.validators.common import get_embed_schema_resolver


def validate(data):
    """
    :param data: Dictionary of data to validate
    :raises: jsonschema.ValidationError: When invalid
    """
    jsonschema.validate(
        instance=data, schema=SCHEMA, resolver=get_embed_schema_resolver(SCHEMA)
    )
