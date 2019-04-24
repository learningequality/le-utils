import json
import pkgutil
from collections import namedtuple
from gettext import gettext as _

""" Format Preset Constants"""

# IMPORTANT: Keep these constants in sync with presetlookup.json

VIDEO_HIGH_RES = "high_res_video"
VIDEO_HIGH_RES_READABLE = "High Resolution"
VIDEO_LOW_RES = "low_res_video"
VIDEO_LOW_RES_READABLE = "Low Resolution"
VIDEO_VECTOR = "vector_video"
VIDEO_VECTOR_READABLE = "Vectorized"
VIDEO_THUMBNAIL = "video_thumbnail"
VIDEO_THUMBNAIL_READABLE = "Thumbnail"
VIDEO_SUBTITLE = "video_subtitle"
VIDEO_SUBTITLE_READABLE = "Subtitle"
VIDEO_DEPENDENCY = "video_dependency"
VIDEO_DEPENDENCY_READABLE = "Video (dependency)"

AUDIO = "audio"
AUDIO_READABLE = "Audio"
AUDIO_THUMBNAIL = "audio_thumbnail"
AUDIO_THUMBNAIL_READABLE = "Thumbnail"

DOCUMENT = "document"
DOCUMENT_READABLE = "Document"  # TODO(ivan): Change to "PDF Document"  str translations?
EPUB = "epub"
EPUB_READABLE = "ePub Document"
DOCUMENT_THUMBNAIL = "document_thumbnail"
DOCUMENT_THUMBNAIL_READABLE = "Thumbnail"

EXERCISE = "exercise"
EXERCISE_READABLE = "Exercise"
EXERCISE_THUMBNAIL = "exercise_thumbnail"
EXERCISE_THUMBNAIL_READABLE = "Thumbnail"
EXERCISE_IMAGE = "exercise_image"
EXERCISE_IMAGE_READABLE = "Exercise Image"
EXERCISE_GRAPHIE = "exercise_graphie"
EXERCISE_GRAPHIE_READABLE = "Exercise Graphie"

CHANNEL_THUMBNAIL = "channel_thumbnail"
CHANNEL_THUMBNAIL_READABLE = "Channel Thumbnail"
TOPIC_THUMBNAIL = "topic_thumbnail"
TOPIC_THUMBNAIL_READABLE = "Thumbnail"

HTML5_ZIP = "html5_zip"
HTML5_ZIP_READABLE = "HTML5 Zip"
HTML5_THUMBNAIL = "html5_thumbnail"
HTML5_THUMBNAIL_READABLE = "HTML5 Thumbnail"

HTML5_DEPENDENCY_ZIP = "html5_dependency"
HTML5_DEPENDENCY_ZIP_READABLE = "HTML5 Dependency (Zip format)"

SLIDESHOW_IMAGE = "slideshow_image"
SLIDESHOW_IMAGE_READABLE = "Slideshow Image"

SLIDESHOW_THUMBNAIL = "slideshow_thumbnail"
SLIDESHOW_THUMBNAIL_READABLE = "Slideshow Thumbnail"

SLIDESHOW_MANIFEST = "slideshow_manifest"
SLIDESHOW_MANIFEST_READABLE = "Slideshow Manifest"


choices = (
    (VIDEO_HIGH_RES, _(VIDEO_HIGH_RES_READABLE)),
    (VIDEO_LOW_RES, _(VIDEO_LOW_RES_READABLE)),
    # (VIDEO_VECTOR, _(VIDEO_VECTOR_READABLE)),  # doesn't exist yet so took out
    (VIDEO_THUMBNAIL, _(VIDEO_THUMBNAIL_READABLE)),
    (VIDEO_SUBTITLE, _(VIDEO_SUBTITLE_READABLE)),
    (VIDEO_DEPENDENCY, _(VIDEO_DEPENDENCY_READABLE)),

    (AUDIO, _(AUDIO_READABLE)),
    (AUDIO_THUMBNAIL, _(AUDIO_THUMBNAIL_READABLE)),

    (DOCUMENT, _(DOCUMENT_READABLE)),
    (EPUB, _(EPUB_READABLE)),
    (DOCUMENT_THUMBNAIL, _(DOCUMENT_THUMBNAIL_READABLE)),

    (EXERCISE, _(EXERCISE_READABLE)),
    (EXERCISE_THUMBNAIL, _(EXERCISE_THUMBNAIL_READABLE)),
    (EXERCISE_IMAGE, _(EXERCISE_IMAGE_READABLE)),
    (EXERCISE_GRAPHIE, _(EXERCISE_GRAPHIE_READABLE)),

    (CHANNEL_THUMBNAIL, _(CHANNEL_THUMBNAIL_READABLE)),
    (TOPIC_THUMBNAIL, _(TOPIC_THUMBNAIL_READABLE)),

    (HTML5_ZIP, _(HTML5_ZIP_READABLE)),
    (HTML5_DEPENDENCY_ZIP, _(HTML5_DEPENDENCY_ZIP_READABLE)),
    (HTML5_THUMBNAIL, _(HTML5_THUMBNAIL_READABLE)),

    (SLIDESHOW_IMAGE, _(SLIDESHOW_IMAGE_READABLE)),
    (SLIDESHOW_THUMBNAIL, _(SLIDESHOW_THUMBNAIL_READABLE)),
    (SLIDESHOW_MANIFEST, _(SLIDESHOW_MANIFEST_READABLE)),
)


class Preset(
    namedtuple("Preset", [
            "id",
            "readable_name",
            "multi_language",
            "supplementary",
            "thumbnail",
            "subtitle",
            "display",
            "order",
            "kind",
            "allowed_formats",
            "convertible_formats"
        ])):
    pass

def generate_list(constantlist):
    for id, preset in constantlist.items():
        yield Preset(id=id, **preset)

def _initialize_preset_list():
    constantlist = json.loads(pkgutil.get_data('le_utils', 'resources/presetlookup.json').decode('utf-8'))

    return generate_list(constantlist)

PRESETLIST = list(_initialize_preset_list())
