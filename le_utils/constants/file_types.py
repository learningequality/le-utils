from gettext import gettext as _
from le_utils.constants import file_formats

""" File Type Constants """
# constants for different File types
VIDEO = "video"
AUDIO = "audio"
DOCUMENT = "document"
HTML5 = "html5"
THUMBNAIL = "thumbnail"
SUBTITLES = "subtitles"


""" File Format (extension) to File Type Mapping """
MAPPING = {
    # ThumbnailFile formats
    file_formats.JPG: THUMBNAIL,
    file_formats.JPEG: THUMBNAIL,
    file_formats.PNG: THUMBNAIL,
    file_formats.GIF: THUMBNAIL,
    #
    # AudioFile formats
    file_formats.MP3: AUDIO,
    #
    # DocumentFile formats
    file_formats.PDF: DOCUMENT,
    #
    # formats HTMLZipFile
    file_formats.HTML5: HTML5,
    #
    # formats VideoFile
    file_formats.MP4: VIDEO,
    #
    # formats SubtitleFile
    file_formats.VTT: SUBTITLES,
    file_formats.SRT: SUBTITLES,
}
