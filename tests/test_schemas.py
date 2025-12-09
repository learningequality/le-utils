# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import contextlib
import uuid

import pytest

from le_utils.constants import completion_criteria
from le_utils.constants import embed_content_request
from le_utils.constants import embed_topics_request
from le_utils.constants import learning_objectives
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


def _validate_learning_objectives(data):
    """
    :param data: Dictionary of data to validate
    :raises: jsonschema.ValidationError: When invalid
    """
    jsonschema.validate(instance=data, schema=learning_objectives.SCHEMA)


@skip_if_jsonschema_unavailable
def test_learning_objectives__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [
                    {
                        "id": str(uuid.uuid4()),
                        "text": "Learning Objective 1",
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "text": "Learning Objective 2",
                        "metadata": {"key": "value"},
                    },
                ],
                "assessment_objectives": {
                    str(uuid.uuid4()): [str(uuid.uuid4())],
                    str(uuid.uuid4()): [
                        str(uuid.uuid4()),
                        str(uuid.uuid4()),
                    ],
                },
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())],
                    "abcdef1234567890abcdef1234567891": [str(uuid.uuid4())],
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__valid_uuid_v5():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [
                    {
                        "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "test")),
                        "text": "Learning Objective 1",
                    },
                    {
                        "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "test2")),
                        "text": "Learning Objective 2",
                        "metadata": {"key": "value"},
                    },
                ],
                "assessment_objectives": {
                    str(uuid.uuid5(uuid.NAMESPACE_DNS, "test")): [
                        str(uuid.uuid5(uuid.NAMESPACE_DNS, "test3"))
                    ],
                    str(uuid.uuid5(uuid.NAMESPACE_DNS, "test2")): [
                        str(uuid.uuid5(uuid.NAMESPACE_DNS, "test4")),
                        str(uuid.uuid5(uuid.NAMESPACE_DNS, "test5")),
                    ],
                },
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [
                        str(uuid.uuid5(uuid.NAMESPACE_DNS, "test6"))
                    ],
                    "abcdef1234567890abcdef1234567891": [
                        str(uuid.uuid5(uuid.NAMESPACE_DNS, "test7"))
                    ],
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_lo_structure():
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [
                    {"id": str(uuid.uuid4())},  # Missing text
                ],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_assessment_mapping():
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {
                    str(uuid.uuid4()): str(uuid.uuid4()),  # Should be an array
                },
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_lesson_mapping():
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": str(
                        uuid.uuid4()
                    ),  # Should be an array
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__missing_required_fields():
    # Missing learning_objectives
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )

    # Missing lesson_objectives
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
            }
        )

    # Missing lesson_objectives
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__empty_structures():
    # Empty learning_objectives
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )

    # Empty assessment_objectives
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )

    # Empty lesson_objectives
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {},
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_uuid_format_in_learning_objectives():
    # Invalid UUID format for learning objective ID
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": "invalid-uuid", "text": "LO1"}],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_uuid_format_in_references():
    # Invalid UUID format in assessment and lesson objective references
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {str(uuid.uuid4()): ["invalid-uuid"]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_question_id_pattern():
    # Invalid question ID pattern (not a valid UUID v4)
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {
                    "invalid-uuid-format": [str(uuid.uuid4())]
                },  # Invalid UUID format
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_lesson_id_pattern():
    # Invalid lesson ID pattern (has extra characters)
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [{"id": str(uuid.uuid4()), "text": "LO1"}],
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890:extra": [str(uuid.uuid4())]
                },  # Has extra characters
            }
        )


@skip_if_jsonschema_unavailable
def test_learning_objectives__invalid_text_patterns():
    # Empty text after trimming whitespace
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [
                    {"id": str(uuid.uuid4()), "text": "   "}
                ],  # Only whitespace
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )

    # Empty text
    with pytest.raises(jsonschema.ValidationError):
        _validate_learning_objectives(
            {
                "learning_objectives": [
                    {"id": str(uuid.uuid4()), "text": ""}
                ],  # Empty string
                "assessment_objectives": {str(uuid.uuid4()): [str(uuid.uuid4())]},
                "lesson_objectives": {
                    "abcdef1234567890abcdef1234567890": [str(uuid.uuid4())]
                },
            }
        )
