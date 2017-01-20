from collections import namedtuple, defaultdict
import os
import re
import json


class Language(namedtuple("Language", ["native_name",
                                       "primary_code",
                                       "subcode",
                                       "name",
                                       "ka_name"])):

    @property
    def code(self):
        return "{primary_code}-{subcode}".format(
            primary_code=self.primary_code,
            subcode=self.subcode
        )


    @property
    def id(self):
        return self.code

def _parse_out_iso_639_code(code) -> dict:
    code_regex = r'(?P<primary_code>\w{2,3})(-(?P<subcode>\w{2,3}))?'

    match = re.match(code_regex, code)
    if match:
        return defaultdict(lambda: None, **match.groupdict())
    else:
        return None


def _initialize_language_list():
    with open(os.path.dirname(__file__) + '/languagelookup.json') as f:
        langlist = json.load(f)

    for code, lang in langlist.items():
        values = _parse_out_iso_639_code(code)
        values.update(lang)

        # add a default value to ka_name
        if 'ka_name' not in values:
            values['ka_name'] = None

        yield Language(**values)


LANGUAGELIST = list(_initialize_language_list())

# LANGUAGELIST = [
#     Language(native_name=code, primary_code="pt", subcode="PT", standard_name="Portuguese"),
# ]

LANGUAGES = {l.code: l for l in LANGUAGELIST}
