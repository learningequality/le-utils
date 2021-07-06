import json
import pkgutil
from collections import namedtuple

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
AUDIO_DEPENDENCY = "audio_dependency"
AUDIO_DEPENDENCY_READABLE = "audio (dependency)"

DOCUMENT = "document"
DOCUMENT_READABLE = (
    "Document"  # TODO(ivan): Change to "PDF Document"  str translations?
)
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

H5P_ZIP = "h5p"
H5P_ZIP_READABLE = "H5P Zip"
H5P_THUMBNAIL = "h5p_thumbnail"
H5P_THUMBNAIL_READABLE = "H5P Thumbnail"

ZIM = "zim"
ZIM_READABLE = "Zim"
ZIM_THUMBNAIL = "zim_thumbnail"
ZIM_THUMBNAIL_READABLE = "Zim Thumbnail"

QTI_ZIP = "qti"
QTI_ZIP_READABLE = "QTI Zip"
QTI_THUMBNAIL = "qti_thumbnail"
QTI_THUMBNAIL_READABLE = "QTI Thumbnail"


SLIDESHOW_IMAGE = "slideshow_image"
SLIDESHOW_IMAGE_READABLE = "Slideshow Image"

SLIDESHOW_THUMBNAIL = "slideshow_thumbnail"
SLIDESHOW_THUMBNAIL_READABLE = "Slideshow Thumbnail"

SLIDESHOW_MANIFEST = "slideshow_manifest"
SLIDESHOW_MANIFEST_READABLE = "Slideshow Manifest"


choices = (
    (VIDEO_HIGH_RES, VIDEO_HIGH_RES_READABLE),
    (VIDEO_LOW_RES, VIDEO_LOW_RES_READABLE),
    # (VIDEO_VECTOR, VIDEO_VECTOR_READABLE),  # doesn't exist yet so took out
    (VIDEO_THUMBNAIL, VIDEO_THUMBNAIL_READABLE),
    (VIDEO_SUBTITLE, VIDEO_SUBTITLE_READABLE),
    (VIDEO_DEPENDENCY, VIDEO_DEPENDENCY_READABLE),
    (AUDIO, AUDIO_READABLE),
    (AUDIO_THUMBNAIL, AUDIO_THUMBNAIL_READABLE),
    (AUDIO_DEPENDENCY, AUDIO_DEPENDENCY_READABLE),
    (DOCUMENT, DOCUMENT_READABLE),
    (EPUB, EPUB_READABLE),
    (DOCUMENT_THUMBNAIL, DOCUMENT_THUMBNAIL_READABLE),
    (EXERCISE, EXERCISE_READABLE),
    (EXERCISE_THUMBNAIL, EXERCISE_THUMBNAIL_READABLE),
    (EXERCISE_IMAGE, EXERCISE_IMAGE_READABLE),
    (EXERCISE_GRAPHIE, EXERCISE_GRAPHIE_READABLE),
    (CHANNEL_THUMBNAIL, CHANNEL_THUMBNAIL_READABLE),
    (TOPIC_THUMBNAIL, TOPIC_THUMBNAIL_READABLE),
    (HTML5_ZIP, HTML5_ZIP_READABLE),
    (HTML5_DEPENDENCY_ZIP, HTML5_DEPENDENCY_ZIP_READABLE),
    (HTML5_THUMBNAIL, HTML5_THUMBNAIL_READABLE),
    (H5P_ZIP, H5P_ZIP_READABLE),
    (H5P_THUMBNAIL, H5P_THUMBNAIL_READABLE),
    (ZIM, ZIM_READABLE),
    (ZIM_THUMBNAIL, ZIM_THUMBNAIL_READABLE),
    (QTI_ZIP, QTI_ZIP_READABLE),
    (QTI_THUMBNAIL, QTI_THUMBNAIL_READABLE),
    (SLIDESHOW_IMAGE, SLIDESHOW_IMAGE_READABLE),
    (SLIDESHOW_THUMBNAIL, SLIDESHOW_THUMBNAIL_READABLE),
    (SLIDESHOW_MANIFEST, SLIDESHOW_MANIFEST_READABLE),
)


class Preset(
    namedtuple(
        "Preset",
        [
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
            "convertible_formats",
        ],
    )
):
    pass


def generate_list(constantlist):
    for id, preset in constantlist.items():
        yield Preset(id=id, **preset)


def _initialize_preset_list():
    constantlist = json.loads(
        pkgutil.get_data("le_utils", "resources/presetlookup.json").decode("utf-8")
    )

    return generate_list(constantlist)


PRESETLIST = list(_initialize_preset_list())
