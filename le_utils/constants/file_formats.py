import json
import pkgutil
from collections import namedtuple
from gettext import gettext as _

""" File Format Constants """

# IMPORTANT: Keep these constants in sync with formatlookup.json and presetlookup.json

# constants for Video format
MP4 = "mp4"
MP4_MIMETYPE = "video/mp4"
WEBM = "webm"
WEBM_MIMETYPE = "video/webm"
# constants for video formats converitble to mp4
AVI = "avi"
MOV = "mov"
MPG = "mpg"
WMV = "wmv"
MKV = "mkv"
FLV = "flv"
OGV = "ogv"
M4V = "m4v"

# constants for Subtitle format
VTT = "vtt"
VTT_MIMETYPE = ".vtt"
# constants for formats convertible to VTT
SRT = "srt"
TTML = "ttml"
SAMI = "sami"
SCC = "scc"
DFXP = "dfxp"

# constants for Audio format
MP3 = "mp3"
MP3_MIMETYPE = ".mp3"

# constants for Document format
PDF = "pdf"
PDF_MIMETYPE = "application/pdf"

# constants for Thumbnail format
JPG = "jpg"
JPG_MIMETYPE = "image/jpeg"
JPEG = "jpeg"
PNG = "png"
PNG_MIMETYPE = "image/png"
GIF = "gif"
GIF_MIMETYPE = "image/gif"


JSON = "json"
JSON_MIMETYPE = "application/json"
SVG = "svg"
SVG_MIMETYPE = "image/svg"
GRAPHIE = "graphie"
GRAPHIE_MIMETYPE = ".graphie"

# constants for Exercise format
PERSEUS = "perseus"
PERSEUS_MIMETYPE = "application/perseus+zip"

# constants for HTML5 zip format
HTML5 = "zip"
HTML5_MIMETYPE = ".zip"

# constants for H5P format
H5P = "h5p"
H5P_MIMETYPE = ".h5p"

# constants for ePub format
EPUB = "epub"
EPUB_MIMETYPE = "application/epub+zip"

choices = (
    (MP4, _("MP4 Video")),
    (WEBM, _("WEBM Video")),

    (VTT, _("VTT Subtitle")),

    (MP3, _("MP3 Audio")),

    (PDF, _("PDF Document")),

    (JPG, _("JPG Image")),
    (JPEG, _("JPEG Image")),
    (PNG, _("PNG Image")),
    (GIF, _("GIF Image")),
    (JSON, _("JSON")),
    (SVG, _("SVG Image")),

    (PERSEUS, _("Perseus Exercise")),

    (GRAPHIE, _("Graphie Exercise")),

    (HTML5, _("HTML5 Zip")),

    (H5P, _("H5P")),

    (EPUB, _("ePub Document")),
)

class Format(namedtuple("Format", ["id", "mimetype"])):
    pass

def generate_list(constantlist):
    for id, format in constantlist.items():
        yield Format(id=id, **format)

def _initialize_format_list():
    constantlist = json.loads(pkgutil.get_data('le_utils', 'resources/formatlookup.json').decode('utf-8'))
    return generate_list(constantlist)

FORMATLIST = list(_initialize_format_list())

_FORMATLOOKUP = {f.id: f for f in FORMATLIST}

def getformat(id, default=None):
    """
    Try to lookup a file format object for its `id` in internal representation defined
    in resources/formatlookup.json.
    Returns None if lookup by internal representation fails.
    """
    return _FORMATLOOKUP.get(id) or None
