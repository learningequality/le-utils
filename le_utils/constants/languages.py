import json
import logging
import pkgutil
import re
from collections import defaultdict
from collections import namedtuple

try:
    import pycountry
except ImportError:
    pycountry = None

logger = logging.getLogger("le_utils")
logger.setLevel(logging.INFO)


LTR_LANGUAGE = "ltr"
RTL_LANGUAGE = "rtl"
LANGUAGE_DIRECTIONS = (
    (LTR_LANGUAGE, "Left to Right"),
    (RTL_LANGUAGE, "Right to Left"),
)

RTL_LANG_CODES = [
    "ar",  # Arabic
    "arq",  # Algerian
    "dv",  # Divehi; Dhivehi; Maldivian
    "he",  # Hebrew (modern)
    "fa",  # Persian
    "ps",  # Pashto; Pushto
    "ur",  # Urdu
    "yi",  # Yiddish
]


class Language(
    namedtuple(
        "Language", ["native_name", "primary_code", "subcode", "name", "ka_name"]
    )
):
    @property
    def code(self):
        if self.subcode:
            return "{primary_code}-{subcode}".format(
                primary_code=self.primary_code, subcode=self.subcode
            )
        else:
            return self.primary_code

    @property
    def id(self):
        return self.code

    @property
    def first_native_name(self):
        """
        Return the first native name in the comma-seprated list of `native_name`.
        """
        return self.native_name.split(",")[0]


def _parse_out_iso_639_code(code):
    code_regex = r"(?P<primary_code>\w{2,3})(-(?P<subcode>\w{2,4}))?"

    match = re.match(code_regex, code)
    if match:
        return defaultdict(lambda: None, **match.groupdict())
    else:
        return None


def generate_list(constantlist):
    for code, lang in constantlist.items():
        values = _parse_out_iso_639_code(code)
        values.update(lang)

        # add a default value to ka_name
        if "ka_name" not in values:
            values["ka_name"] = None

        yield Language(**values)


def _initialize_language_list():
    langlist = json.loads(
        pkgutil.get_data("le_utils", "resources/languagelookup.json").decode("utf-8")
    )

    return generate_list(langlist)


def _iget(key, lookup_dict):
    """
    Case-insensitive search for `key` within keys of `lookup_dict`.
    """
    for k, v in lookup_dict.items():
        if k.lower() == key.lower():
            return v
    return None


LANGUAGELIST = list(_initialize_language_list())

_LANGLOOKUP = {l.code: l for l in LANGUAGELIST}


def getlang(code, default=None):
    """
    Try to lookup a Language object for `code` in internal representation defined
    in resources/languagelookup.json.
    Returns None if lookup by internal representation fails.
    """
    return _LANGLOOKUP.get(code) or None
    # should this be   return _LANGLOOKUP.get(code) or _LANGLOOKUP[default]  ???


# NOTES ON INTERNAL REPRESENTATION FOR LANGUAGE CODES
################################################################################
# The language code lookup table in `resources/languagelookup.json` is complex:
# 1.   "<code>":{
# 2.     "name":"EnglishName, variant; AlternativeName",
# 3.     "native_name":"NativeName, AlternativeNativeName",
#       }
#
# 1. <code> can be two letter code, three letter code, or <code>-<locale> string
# 2. `name` attr. contains ";"-separated list of alternative names for the language,
#     some names have a ","-separated variant, e.g.,  "Spanish, Spain"
# 3. `native_name` contains ","-separated list of strings for language name in that language
#
# The following lookup tables and lookup functions perform the necessary logic
# to deal with the ";" and "," separators used in `resources/languagelookup.json`
################################################################################

_LANGUAGE_NAME_LOOKUP = {l.name: l for l in LANGUAGELIST}

# Enrich _LANGUAGE_NAME_LOOKUP with aliases for list-names, and simplified names
new_items = {}
for lang_name, lang_obj in _LANGUAGE_NAME_LOOKUP.items():
    # Add language names that are separated by semicolons, e.g. "Catalan; Valencian"
    if ";" in lang_name:
        new_names = [n.strip() for n in lang_name.split(";")]
        for new_name in new_names:
            if new_name in _LANGUAGE_NAME_LOOKUP.keys() or new_name in new_items:
                logger.debug("Skip " + new_name + " because it already exisits")
            else:
                new_items[new_name] = lang_obj
    # Add base names without modifies in brackets or country/region after comma
    elif "(" in lang_name or "," in lang_name:
        simple_name = lang_name.split(",")[0]  # take part before comma
        simple_name = simple_name.split("(")[0].strip()  # and before any bracket
        if simple_name in _LANGUAGE_NAME_LOOKUP.keys() or simple_name in new_items:
            logger.debug("Skip " + simple_name + " because it already exisits")
        else:
            new_items[simple_name] = lang_obj
_LANGUAGE_NAME_LOOKUP.update(new_items)


def getlang_by_name(name):
    """
    Try to lookup a Language object by name, e.g. 'English', in internal language list.
    Returns None if lookup by language name fails in resources/languagelookup.json.
    """
    direct_match = _iget(name, _LANGUAGE_NAME_LOOKUP)
    if direct_match:
        return direct_match
    else:
        simple_name = name.split(",")[0]  # take part before comma
        simple_name = simple_name.split("(")[0].strip()  # and before any bracket
        return _LANGUAGE_NAME_LOOKUP.get(simple_name, None)


_LANGUAGE_NATIVE_NAME_LOOKUP = {l.native_name: l for l in LANGUAGELIST}

# Enrich _LANGUAGE_NATIVE_NAME_LOOKUP with aliases for list-like names
new_items = {}
for lang_native_name, lang_obj in _LANGUAGE_NATIVE_NAME_LOOKUP.items():
    # Add base native names without modifies in brackets or after comma
    if "," in lang_native_name:
        new_native_names = [n.strip() for n in lang_native_name.split(",")]
        for new_native_name in new_native_names:
            simple_native_name = new_native_name.split("(")[
                0
            ].strip()  # text before any bracket
            if (
                simple_native_name in _LANGUAGE_NATIVE_NAME_LOOKUP.keys()
                or new_native_name in new_items
            ):
                logger.debug(
                    "Skip " + simple_native_name + " because it already exisits"
                )
            else:
                new_items[simple_native_name] = lang_obj
    elif "(" in lang_native_name:
        simple_native_name = lang_native_name.split("(")[
            0
        ].strip()  # text before any bracket
        if (
            simple_native_name in _LANGUAGE_NATIVE_NAME_LOOKUP.keys()
            or simple_native_name in new_items
        ):
            logger.debug("Skip " + simple_native_name + " because it already exisits")
        else:
            new_items[simple_native_name] = lang_obj
_LANGUAGE_NATIVE_NAME_LOOKUP.update(new_items)


def getlang_by_native_name(native_name):
    """
    Try to lookup a Language object by native_name, e.g. 'English', in internal language list.
    Returns None if lookup by language name fails in resources/languagelookup.json.
    """
    direct_match = _iget(native_name, _LANGUAGE_NATIVE_NAME_LOOKUP)
    if direct_match:
        return direct_match
    else:
        simple_native_name = native_name.split(",")[0]  # take part before comma
        simple_native_name = simple_native_name.split("(")[
            0
        ].strip()  # and before any bracket
        return _LANGUAGE_NATIVE_NAME_LOOKUP.get(simple_native_name, None)


def getlang_by_alpha2(code):  # noqa: C901
    """
    Lookup a Language object for language code `code` based on these strategies:
      - Special case rules for Hebrew and Chinese Hans/Hant scripts
      - Using `alpha_2` lookup in `pycountry.languages` followed by lookup for a
        language with the same `name` in the internal representaion
    Returns `None` if no matching language is found.
    """
    if pycountry is None:
        logger.warn("pycountry is not installed, cannot lookup language by alpha2")
        return None

    # First try exact match to a language code in the internal representaion
    exact_match = getlang(code)
    if exact_match:
        return exact_match

    # Handle special cases for language codes returned by YouTube API
    if code == "iw":  # handle old Hebrew code 'iw' and return modern code 'he'
        return getlang("he")
    elif "zh-Hans" in code:  # use code `zh-CN` for all simplified Chinese
        return getlang("zh-CN")
    elif re.match("zh(.*)?-TW", code):  # matches all Taiwan chinese codes
        return getlang("zh-TW")
    elif re.match("zh(.*)?-HK", code):  # use code `zh-Hant` for Hong Kong
        return getlang("zh-Hant")

    # extract prefix only if specified with subcode: e.g. zh-Hans --> zh
    first_part = code.split("-")[0]

    # See if pycountry can find this language
    try:
        pyc_lang = pycountry.languages.get(alpha_2=first_part)
        if pyc_lang:
            if hasattr(pyc_lang, "inverted_name"):
                lang_name = pyc_lang.inverted_name
            else:
                lang_name = pyc_lang.name
            return getlang_by_name(lang_name)
        else:
            return None
    except KeyError:
        return None


def getlang_direction(code):
    if code in RTL_LANG_CODES:
        return RTL_LANGUAGE
    else:
        return LTR_LANGUAGE
