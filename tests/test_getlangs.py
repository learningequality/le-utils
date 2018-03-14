# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from le_utils.constants import languages



# getlang ==> Internal representation code lookup
################################################################################

def test_known_codes():
    lang_obj = languages.getlang('en')
    assert lang_obj is not None, 'English not found'
    assert lang_obj.name == "English", 'Wrong name'
    assert lang_obj.native_name == "English", 'Wrong native_name'

    lang_obj = languages.getlang('pt-BR')
    assert lang_obj is not None, 'Brazilian Portuguese not found'
    assert lang_obj.name == "Portuguese, Brazil", 'Wrong name'
    assert lang_obj.native_name == "Português (Brasil)", 'Wrong native_name'

    lang_obj = languages.getlang('zul')
    assert lang_obj is not None, 'Zulu not found'
    assert lang_obj.name == "Zulu", 'Wrong name'
    assert lang_obj.native_name == "isiZulu", 'Wrong native_name'


def test_unknown_code():
    lang_obj = languages.getlang('unknownd-code')
    assert lang_obj is None, 'Unknown lang code returned non-None'



# getlang_by_name ==> Lookup by Language object by name
################################################################################

def test_known_names():
    lang_obj = languages.getlang_by_name('English')
    assert lang_obj is not None, 'English not found'
    assert lang_obj.code == "en", 'Wrong code'
    assert lang_obj.name == "English", 'Wrong name'
    assert lang_obj.native_name == "English", 'Wrong native_name'

    lang_obj = languages.getlang_by_name('Zulu')
    assert lang_obj is not None, 'Zulu not found'
    assert lang_obj.code == "zul", 'Wrong internal repr. code'
    assert lang_obj.name == "Zulu", 'Wrong name'
    assert lang_obj.native_name == "isiZulu", 'Wrong native_name'

    # NOTE: Currently only support full-name matching so would have to lookup by
    #       "name, country" to get local language version
    lang_obj = languages.getlang_by_name('Portuguese, Brazil')
    assert lang_obj is not None, 'Brazilian Portuguese not found'
    assert lang_obj.code == "pt-BR", 'Wrong internal repr. code'
    assert lang_obj.name == "Portuguese, Brazil", 'Wrong name'
    assert lang_obj.native_name == "Português (Brasil)", 'Wrong native_name'

    # NOTE: Currently only support full match lookups where multiple language
    #       specified spearated by semicolons, e.g. "Scottish Gaelic; Gaelic"
    lang_obj = languages.getlang_by_name('Scottish Gaelic; Gaelic')
    assert lang_obj is not None, 'Scottish Gaelic; Gaelic not found'
    assert lang_obj.code == "gd", 'Wrong internal repr. code'
    assert lang_obj.name == "Scottish Gaelic; Gaelic", 'Wrong name'
    assert lang_obj.native_name == "Gàidhlig", 'Wrong native_name'


def test_unknown_name():
    lang_obj = languages.getlang_by_name('UnknoenLanguage')
    assert lang_obj is None, 'UnknoenLanguage name returned non-None'

def test_language_names_with_modifier_in_bracket():
    # try to match based on language name (stuff before subcode in brackets)
    lang_obj = languages.getlang_by_name('Swahili (macrolanguage)')
    assert lang_obj is not None, 'Swahili not found'
    assert lang_obj.code == "sw", 'Wrong internal repr. code'
    assert lang_obj.name == "Swahili", 'Wrong name'
    assert lang_obj.native_name == "Kiswahili", 'Wrong native_name'
    #
    lang_obj = languages.getlang_by_name('Sanskrit (Saṁskṛta)')
    assert lang_obj is not None, 'Sanskrit not found'
    assert lang_obj.code == "sa", 'Wrong internal repr. code'
    assert lang_obj.name == "Sanskrit (Saṁskṛta)", 'Wrong name'
    assert lang_obj.native_name == "संस्कृतम्", 'Wrong native_name'

def test_language_names_with_modifier_after_comma():
    # try to match based on language name (stuff before the comma)
    lang_obj = languages.getlang_by_name('Arabic, Tunisian')
    assert lang_obj is not None, 'Arabic fallback not found'
    assert lang_obj.code == "ar", 'Wrong internal repr. code'
    assert lang_obj.name == "Arabic", 'Wrong name'


def test_list_like_language_names():
    lang_obj = languages.getlang_by_name('Scottish Gaelic')
    assert lang_obj is not None, 'Scottish Gaelic; Gaelic not found'
    assert lang_obj.code == "gd", 'Wrong internal repr. code'
    assert lang_obj.name == "Scottish Gaelic; Gaelic", 'Wrong name'
    assert lang_obj.native_name == "Gàidhlig", 'Wrong native_name'

    lang_obj = languages.getlang_by_name('Gaelic')
    assert lang_obj is not None, 'Scottish Gaelic; Gaelic not found'
    assert lang_obj.code == "gd", 'Wrong internal repr. code'
    assert lang_obj.name == "Scottish Gaelic; Gaelic", 'Wrong name'
    assert lang_obj.native_name == "Gàidhlig", 'Wrong native_name'



# getlang_by_alpha2 ==> Lookup by two-letter Language code
################################################################################

def test_known_alpha2_codes():
    lang_obj = languages.getlang_by_alpha2('en')
    assert lang_obj is not None, 'English not found'
    assert lang_obj.code == "en", 'Wrong code'
    assert lang_obj.name == "English", 'Wrong name'
    assert lang_obj.native_name == "English", 'Wrong native_name'

    lang_obj = languages.getlang_by_alpha2('zu')
    assert lang_obj is not None, 'Zulu not found'
    assert lang_obj.code == "zul", 'Wrong internal repr. code'
    assert lang_obj.name == "Zulu", 'Wrong name'
    assert lang_obj.native_name == "isiZulu", 'Wrong native_name'

    lang_obj = languages.getlang_by_alpha2('pt')
    assert lang_obj is not None, 'Portuguese not found'
    assert lang_obj.code == "pt", 'Wrong code'
    assert lang_obj.name == "Portuguese", 'Wrong name'
    assert lang_obj.native_name == "Português", 'Wrong native_name'

def test_unknown_alpha2_code():
    lang_obj = languages.getlang_by_alpha2('zz')
    assert lang_obj is None, 'Uknown code zz returned non-None'



@pytest.fixture
def simplified_chinese_codes():
    return ['zh-Hans', 'zh-Hans-CN', 'zh-Hans-TW']

@pytest.fixture
def traditional_chinese_codes():
    return ['zh-Hant', 'zh-Hant-TW', 'zh-Hant-HK', 'zh-HK']


def test_youtube_edgecases_alpha2_codes(simplified_chinese_codes, traditional_chinese_codes):
    # check old language code for Hebrew works `iw`
    lang_obj = languages.getlang_by_alpha2('iw')
    assert lang_obj is not None, 'Hebrew not found'
    assert lang_obj.code == "he", 'Wrong code'
    assert lang_obj.name == "Hebrew (modern)", 'Wrong name'
    assert lang_obj.native_name == "עברית", 'Wrong native_name'

    # Check all Simplified Chinese codes are resolved correctly to zh-CN
    for lang_code in simplified_chinese_codes:
        lang_obj = languages.getlang_by_alpha2(lang_code)
        assert lang_obj is not None, 'Simplified Chinese not found'
        assert lang_obj.code == "zh-CN", 'Wrong internal repr. code'
        assert lang_obj.name == "Chinese, Simplified", 'Wrong name'
        assert lang_obj.native_name == "中国大陆", 'Wrong native_name'

    # Check all Traditional Chinese codes are resolved correctly to zh-TW
    for lang_code in traditional_chinese_codes:
        lang_obj = languages.getlang_by_alpha2(lang_code)
        assert lang_obj is not None, 'Traditional Chinese not found'
        assert lang_obj.code == "zh-TW", 'Wrong internal repr. code'
        assert lang_obj.name == "Chinese, Traditional", 'Wrong name'
        assert lang_obj.native_name == "正體字/繁體字", 'Wrong native_name'



# getlang_by_native_name ==> Lookup by Language object by native_name
################################################################################

def test_known_native_names():
    lang_obj = languages.getlang_by_native_name('English')
    assert lang_obj is not None, 'English not found'
    assert lang_obj.code == "en", 'Wrong code'
    assert lang_obj.name == "English", 'Wrong name'
    assert lang_obj.native_name == "English", 'Wrong native_name'

    lang_obj = languages.getlang_by_native_name('isiZulu')
    assert lang_obj is not None, 'Zulu not found'
    assert lang_obj.code == "zul", 'Wrong internal repr. code'
    assert lang_obj.name == "Zulu", 'Wrong name'
    assert lang_obj.native_name == "isiZulu", 'Wrong native_name'

    # NOTE: Currently only support full-name matching so would have to lookup by
    #       "name, country" to get local language version
    lang_obj = languages.getlang_by_native_name('Português')
    assert lang_obj is not None, 'Portuguese not found'
    assert lang_obj.code == "pt", 'Wrong internal repr. code'
    assert lang_obj.name == "Portuguese", 'Wrong name'
    assert lang_obj.native_name == "Português", 'Wrong native_name'

    # NOTE: Currently only support full match lookups where multiple language
    #       specified spearated by semicolons, e.g. "Scottish Gaelic; Gaelic"
    lang_obj = languages.getlang_by_native_name('Gàidhlig')
    assert lang_obj is not None, 'Scottish Gaelic; Gaelic not found'
    assert lang_obj.code == "gd", 'Wrong internal repr. code'
    assert lang_obj.name == "Scottish Gaelic; Gaelic", 'Wrong name'
    assert lang_obj.native_name == "Gàidhlig", 'Wrong native_name'


def test_unknown_name():
    lang_obj = languages.getlang_by_native_name('UnknoenNativeLanguage')
    assert lang_obj is None, 'query for natove_name UnknoenNativeLanguage returned non-None'

def test_language_names_with_modifier_in_bracket():
    # try to match based on language name (stuff before subcode in brackets)
    lang_obj = languages.getlang_by_native_name('中文')
    assert lang_obj is not None, 'Chinese 1 not found'
    assert lang_obj.code == "zh", 'Wrong internal repr. code'
    assert lang_obj.name == "Chinese", 'Wrong name'
    assert lang_obj.native_name == "中文 (Zhōngwén), 汉语, 漢語", 'Wrong native_name'
    #
    lang_obj = languages.getlang_by_native_name('汉语')
    assert lang_obj is not None, 'Chinese 2 not found'
    assert lang_obj.code == "zh", 'Wrong internal repr. code'
    assert lang_obj.name == "Chinese", 'Wrong name'
    assert lang_obj.native_name == "中文 (Zhōngwén), 汉语, 漢語", 'Wrong native_name'
    #
    lang_obj = languages.getlang_by_native_name('漢語')
    assert lang_obj is not None, 'Chinese 3 not found'
    assert lang_obj.code == "zh", 'Wrong internal repr. code'
    assert lang_obj.name == "Chinese", 'Wrong name'
    assert lang_obj.native_name == "中文 (Zhōngwén), 汉语, 漢語", 'Wrong native_name'
    #
    lang_obj = languages.getlang_by_native_name('日本語')
    assert lang_obj is not None, 'Japanese not found'
    assert lang_obj.code == "ja", 'Wrong internal repr. code'
    assert lang_obj.name == "Japanese", 'Wrong name'
    assert lang_obj.native_name == "日本語 (にほんご／にっぽんご)", 'Wrong native_name'
    #
    lang_obj = languages.getlang_by_native_name('한국어')
    assert lang_obj is not None, 'Korean not found'
    assert lang_obj.code == "ko", 'Wrong internal repr. code'
    assert lang_obj.name == "Korean", 'Wrong name'
    assert lang_obj.native_name == "한국어 (韓國語), 조선말 (朝鮮語)", 'Wrong native_name'
    #
    lang_obj = languages.getlang_by_native_name('조선말')
    assert lang_obj is not None, 'Korean not found'
    assert lang_obj.code == "ko", 'Wrong internal repr. code'
    assert lang_obj.name == "Korean", 'Wrong name'
    assert lang_obj.native_name == "한국어 (韓國語), 조선말 (朝鮮語)", 'Wrong native_name'


def test_list_like_language_native_names():
    lang_obj = languages.getlang_by_native_name('Iñupiaq')
    assert lang_obj is not None, 'Inupiaq not found'
    assert lang_obj.code == "ik", 'Wrong internal repr. code'
    assert lang_obj.name == "Inupiaq", 'Wrong name'
    assert lang_obj.native_name == "Iñupiaq, Iñupiatun", 'Wrong native_name'
    #
    lang_obj = languages.getlang_by_native_name('Iñupiatun')
    assert lang_obj is not None, 'Inupiaq not found'
    assert lang_obj.code == "ik", 'Wrong internal repr. code'
    assert lang_obj.name == "Inupiaq", 'Wrong name'
    assert lang_obj.native_name == "Iñupiaq, Iñupiatun", 'Wrong native_name'



@pytest.fixture
def african_languages_list():
    return ['Sesotho', 'isiXhosa', 'isiZulu', 'isiNdebele', 'Setswana', 'Siswati',
            'Xitsonga', 'Sepedi', 'Tshivenda']

def test_african_languages(african_languages_list):
    missing_names = []
    for native_name in african_languages_list:
        lang_obj = languages.getlang_by_native_name(native_name)
        if lang_obj is None:
            missing_names.append(native_name)
    assert missing_names == [], 'Languages with native_names missing: ' + str(missing_names)


# check RTL_LANG_CODES contains Arabic, Hebrew, and Urdu
################################################################################
def test_rtl_languagess():
    minimum_list = ['ar', 'he', 'ur']
    for lang_code in minimum_list:
        assert lang_code in languages.RTL_LANG_CODES, 'Known RTL missing from RTL_LANG_CODES list'

