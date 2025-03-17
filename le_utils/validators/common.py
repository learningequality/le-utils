import json
import os

from jsonschema import RefResolver


def get_embed_schema_resolver(schema):
    """
    Returns a properly configured JSON schema resolver for embed schemas.

    :param schema: The schema to use as the base schema
    :return: A configured RefResolver
    """
    schema_dir = os.path.join(os.path.dirname(__file__), "..", "..", "spec")
    with open(os.path.join(schema_dir, "definitions-embed_common.json")) as f:
        common_definitions = json.load(f)

    schema_store = {"/schemas/common_embed_definitions": common_definitions}

    return RefResolver.from_schema(schema, store=schema_store)
