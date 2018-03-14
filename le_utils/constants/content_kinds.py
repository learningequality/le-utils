from gettext import gettext as _
from le_utils.constants import file_formats

""" Content Kind Constants """
# constants for ContentKind
TOPIC = "topic"
VIDEO = "video"
AUDIO = "audio"
EXERCISE = "exercise"
DOCUMENT = "document"
HTML5 = "html5"

choices = (
    (TOPIC, _("Topic")),
    (VIDEO, _("Video")),
    (AUDIO, _("Audio")),
    (EXERCISE, _("Exercise")),
    (DOCUMENT, _("Document")),
    (HTML5, _("HTML5 App")),
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
