import json
import pkgutil

from jsonschema import RefResolver


def get_embed_schema_resolver(schema):
    """
    Returns a properly configured JSON schema resolver for embed schemas.

    :param schema: The schema to use as the base schema
    :return: A configured RefResolver
    """
    common_definitions = json.loads(
        pkgutil.get_data("le_utils", "resources/definitions-embed_common.json").decode(
            "utf-8"
        )
    )

    schema_store = {"/schemas/common_embed_definitions": common_definitions}

    return RefResolver.from_schema(schema, store=schema_store)
