# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import contextlib

import pytest

from le_utils.constants import completion_criteria
from le_utils.constants import mastery_criteria
from le_utils.validators.embed_request import (
    validate as validate_recommendations_request,
)


try:
    # the jsonschema package for python 3.4 is too old, so if not present, we'll just skip
    import jsonschema
except ImportError:
    jsonschema = None


resolver = None
if jsonschema is not None:
    # this is an example of how to include the mastery criteria schema, which is referenced by the
    # completion criteria schema, in the schema resolver so that it validates
    resolver = jsonschema.RefResolver.from_schema(mastery_criteria.SCHEMA)
    resolver.store.update(
        jsonschema.RefResolver.from_schema(completion_criteria.SCHEMA).store
    )


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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
def test_completion_criteria__reference__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        _validate_completion_criteria({"model": "reference", "learner_managed": False})
        _validate_completion_criteria(
            {
                "model": "reference",
            }
        )


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
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


@pytest.mark.skipif(jsonschema is None, reason="jsonschema package is unavailable")
def test_recommendations__topic__valid():
    with _assert_not_raises(jsonschema.ValidationError):
        validate_recommendations_request(
            {
                "topics": [
                    {
                        "id": "456",
                        "title": "Target topic",
                        "description": "Target description",
                        "language": "en",
                    }
                ],
                "resources": [
                    {
                        "id": "123",
                        "title": "Resource title",
                        "description": "Resource description",
                        "text": "Resource text",
                        "language": "en",
                    },
                ],
                "metadata": {
                    "channel_id": "000",
                    "channel_title": "Channel title",
                    "some_additional_field": "some_random_value",
                },
            }
        )
