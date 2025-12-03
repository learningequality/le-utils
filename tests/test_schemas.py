# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import contextlib
import uuid

import pytest

from le_utils.constants import completion_criteria
from le_utils.constants import embed_content_request
from le_utils.constants import embed_topics_request
from le_utils.constants import mastery_criteria

try:
    # the jsonschema package for python 3.4 is too old, so if not present, we'll just skip
    import jsonschema
except ImportError:
    jsonschema = None


# create a common decorator to skip tests if jsonschema is not available
skip_if_jsonschema_unavailable = pytest.mark.skipif(
    jsonschema is None, reason="jsonschema package is unavailable"
)


resolver = None
if jsonschema is not None:
    # this is an example of how to include the mastery criteria schema, which is referenced by the
    # completion criteria schema, in the schema resolver so that it validates
    resolver = jsonschema.RefResolver.from_schema(mastery_criteria.SCHEMA)
    resolver.store.update(
        jsonschema.RefResolver.from_schema(completion_criteria.SCHEMA).store
    )


def _validate_embed_content_request(data):
    """
    :param data: Dictionary of data to validate
    :raises: jsonschema.ValidationError: When invalid
    """
    jsonschema.validate(instance=data, schema=embed_content_request.SCHEMA)


def _validate_embed_topics_request(data):
    """
    :param data: Dictionary of data to validate
    :raises: jsonschema.ValidationError: When invalid
    """
    jsonschema.validate(instance=data, schema=embed_topics_request.SCHEMA)


def _validate_completion_criteria(data):
    """
    :param data: Dictionary of data to validate
    :raises: jsonschema.ValidationError: When invalid
    """
    jsonschema.validate(
        instance=data, schema=completion_criteria.SCHEMA, resolver=resolver
    )


@contextlib.contextmanager
def _assert_not_raises(not_expected):
    try:
        yield
        assert True
    except Exception as e:
        if isinstance(e, not_expected):
            assert e is None
        else:
            raise e


@skip_if_jsonschema_unavailable
def test_completion_criteria__time_model__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {"model": "time", "threshold": 2, "learner_managed": False}
        )
        _validate_completion_criteria(
            {
                "model": "time",
                "threshold": 1200123,
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__time_model__invalid():
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "time",
                "threshold": {"mastery_model": "not_real"},
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "time",
                "threshold": -1,
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__approx_time_model__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {"model": "approx_time", "threshold": 2, "learner_managed": False}
        )
        _validate_completion_criteria(
            {
                "model": "approx_time",
                "threshold": 1200123,
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__approx_time_model__invalid():
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "approx_time",
                "threshold": {"mastery_model": "not_real"},
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "approx_time",
                "threshold": -1,
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__pages_model__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {"model": "pages", "threshold": 2, "learner_managed": False}
        )
        _validate_completion_criteria(
            {
                "model": "pages",
                "threshold": 1200123,
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__pages_model__percentage__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "pages",
                "threshold": "99%",
            }
        )
        _validate_completion_criteria(
            {
                "model": "pages",
                "threshold": "1%",
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__pages_model__invalid():
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "pages",
                "threshold": {"mastery_model": "not_real"},
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "pages",
                "threshold": -1,
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__pages_model__percentage__invalid():
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "pages",
                "threshold": "0%",
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "pages",
                "threshold": "101%",
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__mastery_model__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {"mastery_model": "do_all"},
                "learner_managed": False,
            }
        )
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {"mastery_model": "m_of_n", "m": 1, "n": 2},
            }
        )
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {
                    "mastery_model": "pre_post_test",
                    "pre_post_test": {
                        "assessment_item_ids": [str(uuid.uuid4())],  # v4 UUID
                        "version_a_item_ids": [str(uuid.uuid4())],  # v4 UUID
                        "version_b_item_ids": [
                            str(uuid.uuid5(uuid.NAMESPACE_DNS, "test"))
                        ],  # v5 UUID
                    },
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__mastery_model__invalid():
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {"mastery_model": "m_of_n"},
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {"mastery_model": "do_all", "m": 1},
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {"mastery_model": "not_real"},
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": -1,
            }
        )
    # Missing version_b_item_ids
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {
                    "mastery_model": "pre_post_test",
                    "pre_post_test": {
                        "assessment_item_ids": [str(uuid.uuid4())],  # v4 UUID
                        "version_a_item_ids": [str(uuid.uuid4())],  # v4 UUID
                    },
                },
                "learner_managed": False,
            }
        )
    # Invalid UUIDs
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "mastery",
                "threshold": {
                    "mastery_model": "pre_post_test",
                    "pre_post_test": {
                        "assessment_item_ids": ["not-a-uuid"],
                        "version_a_item_ids": ["not-a-uuid"],
                        "version_b_item_ids": ["not-a-uuid"],
                    },
                },
                "learner_managed": False,
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__reference__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_completion_criteria({"model": "reference", "learner_managed": False})
        _validate_completion_criteria(
            {
                "model": "reference",
            }
        )


@skip_if_jsonschema_unavailable
def test_completion_criteria__reference__invalid():
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "reference",
                "threshold": 1,
                "learner_managed": False,
            }
        )
    with pytest.raises(jsonschema.ValidationError):
        _validate_completion_criteria(
            {
                "model": "reference",
                "threshold": {"mastery_model": "do_all"},
                "learner_managed": False,
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__topics__without_ancestors__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_embed_topics_request(
            {
                "topics": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Target topic",
                        "description": "Target description",
                        "language": "en",
                    }
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__topics__with_ancestors__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_embed_topics_request(
            {
                "topics": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Target topic",
                        "description": "Target description",
                        "language": "en",
                        "ancestors": [
                            {
                                "id": str(uuid.uuid4()),
                                "title": "Parent topic",
                                "description": "Parent description",
                                "level": 1,
                            }
                        ],
                    }
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__topics__invalid_id():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_topics_request(
            {
                "topics": [
                    {
                        "id": "123",
                        "channel_id": str(uuid.uuid4()),
                        "title": "Target topic",
                        "description": "Target description",
                        "language": "en",
                    }
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__topics__missing_language():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_topics_request(
            {
                "topics": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Target topic",
                        "description": "Target description",
                    }
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__topics__invalid_channel_id():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_topics_request(
            {
                "topics": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": "123",
                        "title": "Target topic",
                        "description": "Target description",
                        "language": "en",
                    }
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__topics__missing_channel_id():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_topics_request(
            {
                "topics": [
                    {
                        "id": str(uuid.uuid4()),
                        "title": "Target topic",
                        "description": "Target description",
                        "language": "en",
                    }
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__content__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_embed_content_request(
            {
                "resources": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                        "content_id": str(uuid.uuid4()),
                    },
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__content__valid_with_files():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_embed_content_request(
            {
                "resources": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                        "content_id": str(uuid.uuid4()),
                        "files": [
                            {
                                "url": "http://localhost:8000/media/1234.jpg",
                                "preset": "video_thumbnail",
                            },
                            {
                                "url": "https://storage.cloud.google.com/test.appspot.com/test/test.mp4",
                                "preset": "high_res_video",
                                "language": "en",
                            },
                            {
                                "url": "http://storage.cloud.google.com/test.appspot.com/test/test.mp4",
                                "preset": "high_res_video",
                                "language": "es",
                            },
                        ],
                    },
                ],
                "metadata": {
                    "channel_id": "000",
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__content__invalid_id():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_content_request(
            {
                "resources": [
                    {
                        "id": "123",
                        "channel_id": str(uuid.uuid4()),
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                        "content_id": str(uuid.uuid4()),
                    },
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__content__invalid_channel_id():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_content_request(
            {
                "resources": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": "123",
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                        "content_id": str(uuid.uuid4()),
                    },
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__content__invalid_content_id():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_content_request(
            {
                "resources": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                        "content_id": "non-uuid",
                    },
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__content__invalid_url_files():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_content_request(
            {
                "resources": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                        "content_id": str(uuid.uuid4()),
                        "files": [
                            {
                                "url": "https://example.com/media/1234.jpg",
                                "preset": "video_thumbnail",
                            },
                        ],
                    },
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_embed__content__invalid_preset_files():
    with pytest.raises(jsonschema.ValidationError):
        _validate_embed_content_request(
            {
                "resources": [
                    {
                        "id": str(uuid.uuid4()),
                        "channel_id": str(uuid.uuid4()),
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                        "content_id": str(uuid.uuid4()),
                        "files": [
                            {
                                "url": "http://localhost:8080/media/1234.jpg",
                                "preset": "invalid_preset",
                            },
                        ],
                    },
                ],
                "metadata": {
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )
