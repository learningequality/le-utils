from le_utils.constants import file_formats

""" File Type Constants """
# constants for different File types
# TODO: Remove these and put them into ricecooker directly where needed.
VIDEO = "video"
AUDIO = "audio"
DOCUMENT = "document"
EPUB = "epub"
HTML5 = "html5"
H5P = "h5p"
ZIM = "zim"
THUMBNAIL = "thumbnail"
SUBTITLES = "subtitles"
SLIDESHOW_IMAGE = "slideshow_image"
BLOOMPUB = "bloompub"


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
    file_formats.EPUB: EPUB,
    file_formats.BLOOMPUB: BLOOMPUB,
    file_formats.BLOOMD: BLOOMPUB,
    #
    # formats HTMLZipFile
    file_formats.HTML5: HTML5,
    # formats H5PFile
    file_formats.H5P: H5P,
    #
    # formats ZimFile
    file_formats.ZIM: ZIM,
    #
    # formats VideoFile
    file_formats.MP4: VIDEO,
    file_formats.WEBM: VIDEO,
    #
    # formats SubtitleFile
    file_formats.VTT: SUBTITLES,
}
