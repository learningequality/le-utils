# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from le_utils.constants import languages



# first_native_name  -- split native_name and return first part
################################################################################

def test_first_native_name():

    # basic native name
    lang_obj = languages.getlang('en')
    assert lang_obj is not None, 'English not found'
    assert lang_obj.name == "English", 'Wrong name'
    assert lang_obj.native_name == "English", 'Wrong native_name'
    assert lang_obj.first_native_name == "English", 'Wrong first_native_name'

    # native name with brackets
    lang_obj = languages.getlang('pt-BR')
    assert lang_obj is not None, 'Brazilian Portuguese not found'
    assert lang_obj.name == "Portuguese, Brazil", 'Wrong name'
    assert lang_obj.native_name == "Português (Brasil)", 'Wrong native_name'
    assert lang_obj.first_native_name == "Português (Brasil)", 'Wrong native_name'

    # native name with comma
    lang_obj = languages.getlang('tt')
    assert lang_obj is not None, 'Tatar not found'
    assert lang_obj.name == "Tatar", 'Wrong name'
    assert lang_obj.native_name == "татарча, tatarça, تاتارچا‎", 'Wrong native_name'
    assert lang_obj.first_native_name == "татарча", 'Wrong first_native_name'

    # native name with comma and brackets
    lang_obj = languages.getlang('zh')
    assert lang_obj is not None, 'Chinese not found'
    assert lang_obj.name == "Chinese", 'Wrong name'
    assert lang_obj.native_name == "中文, 汉语, 漢語", 'Wrong native_name'
    assert lang_obj.first_native_name == "中文", 'Wrong first_native_name'
