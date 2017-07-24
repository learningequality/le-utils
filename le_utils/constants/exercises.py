# coding=utf-8

from gettext import gettext as _

""" Mastery Models """
DO_ALL = "do_all"
NUM_CORRECT_IN_A_ROW_10 = "num_correct_in_a_row_10"
NUM_CORRECT_IN_A_ROW_2 = "num_correct_in_a_row_2"
NUM_CORRECT_IN_A_ROW_3 = "num_correct_in_a_row_3"
NUM_CORRECT_IN_A_ROW_5 = "num_correct_in_a_row_5"
SKILL_CHECK = "skill_check"
M_OF_N = "m_of_n"

MASTERY_MODELS = (
    (DO_ALL, _("Do all")),
    (NUM_CORRECT_IN_A_ROW_2, _("2 in a row")),
    (NUM_CORRECT_IN_A_ROW_10, _("10 in a row")),
    (NUM_CORRECT_IN_A_ROW_3, _("3 in a row")),
    (NUM_CORRECT_IN_A_ROW_5, _("5 in a row")),
    (SKILL_CHECK, _("Skill check")),
    (M_OF_N, _("M out of N")),
)

IMG_PLACEHOLDER = "{☣ LOCALPATH}"
IMG_FORMAT = "${" + IMG_PLACEHOLDER + "}/{0}"
IMG_REGEX = r'\$\{☣ LOCALPATH\}\/(.+)'

CONTENT_STORAGE_PLACEHOLDER = "{☣ CONTENTSTORAGE}"
CONTENT_STORAGE_FORMAT = "${" + CONTENT_STORAGE_PLACEHOLDER + "}/{0}"
CONTENT_STORAGE_REGEX = r'\(\$\{☣ CONTENTSTORAGE\}\/(.+)\)'

GRAPHIE_DELIMITER = '$$$GRAPHIE_BREAK$$$'

""" Question Types """
INPUT_QUESTION = "input_question"
MULTIPLE_SELECTION = "multiple_selection"
SINGLE_SELECTION = "single_selection"
FREE_RESPONSE = "free_response"
PERSEUS_QUESTION = "perseus_question"

question_choices = (
    (INPUT_QUESTION, _("Input Question")),
    (MULTIPLE_SELECTION, _("Multiple Selection")),
    (SINGLE_SELECTION, _("Single Selection")),
    (FREE_RESPONSE, _("Free Response")),
    (PERSEUS_QUESTION, _("Perseus Question")),
)