from gettext import gettext as _
from le_utils.constants import file_formats

""" Content Kind Constants """
# constants for ContentKind
TOPIC = "topic"
VIDEO = "video"
AUDIO = "audio"
EXERCISE = "exercise"
DOCUMENT = "document"

choices = (
    (TOPIC, _("Topic")),
    (VIDEO, _("Video")),
    (AUDIO, _("Audio")),
    (EXERCISE, _("Exercise")),
    (DOCUMENT, _("Document")),
)

""" Format and Content Kind Mapping """
MAPPING = {
    file_formats.MP4: VIDEO,
    file_formats.MP3: AUDIO,
    file_formats.WAV: AUDIO,
    file_formats.PDF: DOCUMENT,
    file_formats.PERSEUS: EXERCISE,
}
