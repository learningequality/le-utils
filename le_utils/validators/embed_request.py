import jsonschema

from le_utils.constants.embed_request import SCHEMA


def validate(data):
    """
    :param data: Dictionary of data to validate
    :raises: jsonschema.ValidationError: When invalid
    """
    jsonschema.validate(instance=data, schema=SCHEMA)
