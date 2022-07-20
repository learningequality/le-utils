import json
import pkgutil
from collections import namedtuple

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
H5P = "h5p"
ZIM = "zim"
QUIZ = "quiz"

choices = (
    (TOPIC, "Topic"),
    (VIDEO, "Video"),
    (AUDIO, "Audio"),
    (EXERCISE, "Exercise"),
    (DOCUMENT, "Document"),
    (HTML5, "HTML5 App"),
    (SLIDESHOW, "Slideshow"),
    (H5P, "H5P"),
    (ZIM, "Zim"),
    (QUIZ, "Quiz"),
)
MAX_CHOICE_LENGTH = max([len(choice[0]) for choice in choices])

""" File Format (extension) to Content Kind Mapping """
MAPPING = {
    file_formats.MP4: VIDEO,
    file_formats.WEBM: VIDEO,
    file_formats.MP3: AUDIO,
    file_formats.PDF: DOCUMENT,
    file_formats.EPUB: DOCUMENT,
    file_formats.PERSEUS: EXERCISE,
    file_formats.HTML5: HTML5,
    file_formats.H5P: H5P,
    file_formats.ZIM: ZIM,
}


class Kind(namedtuple("Kind", ["id", "name"])):
    pass


def generate_list(constantlist):
    for id, kind in constantlist.items():
        yield Kind(id=id, **kind)


def _initialize_kind_list():
    constantlist = json.loads(
        pkgutil.get_data("le_utils", "resources/kindlookup.json").decode("utf-8")
    )

    return generate_list(constantlist)


KINDLIST = list(_initialize_kind_list())
