from gettext import gettext as _

""" Mastery Models """
DO_ALL = "do_all"
NUM_CORRECT_IN_A_ROW_10 = "num_correct_in_a_row_10"
NUM_CORRECT_IN_A_ROW_3 = "num_correct_in_a_row_3"
NUM_CORRECT_IN_A_ROW_5 = "num_correct_in_a_row_5"
SKILL_CHECK = "skill_check"

MASTERY_MODELS = (
    (DO_ALL, _("Do all")),
    (NUM_CORRECT_IN_A_ROW_10, _("10 in a row")),
    (NUM_CORRECT_IN_A_ROW_3, _("3 in a row")),
    (NUM_CORRECT_IN_A_ROW_5, _("5 in a row")),
    (SKILL_CHECK, _("Skill check")),
)

""" Question Types """
INPUT = "input_question"
MULTI_SELECT = "multiple_selection"
SINGLE_SELECT = "singles_election"
FREE_RESPONSE = "free_response"

question_choices = (
    (INPUT, _("Input Question")),
    (MULTI_SELECT, _("Multiple Selection")),
    (SINGLE_SELECT, _("Single Selection")),
    (FREE_RESPONSE, _("Free Response")),
)