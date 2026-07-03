# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from le_utils.constants import exercises


def test_QTI_is_in_question_choices():
    assert exercises.QTI == "QTI"
    assert (exercises.QTI, "QTI") in exercises.question_choices
