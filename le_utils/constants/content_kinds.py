import json
import pkgutil
from collections import namedtuple
from gettext import gettext as _
from le_utils.constants import file_formats

""" Content Kind Constants """

# IMPORTANT: Keep these constants in sync with kindlookup.json and presetlookup.json

TOPIC = "topic"
VIDEO = "video"
AUDIO = "audio"
EXERCISE = "exercise"
DOCUMENT = "document"
HTML5 = "html5"
SLIDESHOW = "slideshow"

choices = (
    (TOPIC, _("Topic")),
    (VIDEO, _("Video")),
    (AUDIO, _("Audio")),
    (EXERCISE, _("Exercise")),
    (DOCUMENT, _("Document")),
    (HTML5, _("HTML5 App")),
    (SLIDESHOW, _("Slideshow")),
)

""" File Format (extension) to Content Kind Mapping """
MAPPING = {
    file_formats.MP4: VIDEO,
    file_formats.MP3: AUDIO,
    file_formats.PDF: DOCUMENT,
    file_formats.EPUB: DOCUMENT,
    file_formats.PERSEUS: EXERCISE,
    file_formats.HTML5: HTML5,
}


class Kind(namedtuple("Kind", ["id", "name"])):
    pass

def generate_list(constantlist):
    for id, kind in constantlist.items():
        yield Kind(id=id, **kind)

def _initialize_kind_list():
    constantlist = json.loads(pkgutil.get_data('le_utils', 'resources/kindlookup.json').decode('utf-8'))

    return generate_list(constantlist)

KINDLIST = list(_initialize_kind_list())
