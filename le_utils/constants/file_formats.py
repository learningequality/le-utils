from gettext import gettext as _

""" File Format Constants """
# constants for Video format
MP4 = "mp4"
MP4_MIMETYPE = "video/mp4"

# constants for Subtitle format
VTT = "vtt"
VTT_MIMETYPE = "text/vtt"
SRT = "srt"
SRT_MIMETYPE = "text/srt"

# constants for Audio format
MP3 = "mp3"
MP3_MIMETYPE = "audio/mp3"
WAV = "wav"
WAV_MIMETYPE = "audio/wav"

# constants for Document format
PDF = "pdf"
PDF_MIMETYPE = "application/pdf"

# constants for Thumbnail format
JPG = "jpg"
JPG_MIMETYPE = "image/jpeg"
JPEG = "jpeg"
PNG = "png"
PNG_MIMETYPE = "image/png"

JSON = "json"
JSON_MIMETYPE = "application/json"
SVG = "svg"
SVG_MIMETYPE = "image/svg"

# constants for Exercise format
PERSEUS = "perseus"
PERSEUS_MIMETYPE = ".perseus"

choices = (
    (MP4, _("mp4")),

    (VTT, _("vtt")),
    (SRT, _("srt")),

    (MP3, _("mp3")),
    (WAV, _("wav")),

    (PDF, _("pdf")),

    (JPG, _("jpg")),
    (JPEG, _("jpeg")),
    (PNG, _("png")),
    (JSON, _("json")),
    (SVG, _("svg")),

    (PERSEUS, _("perseus")),
)
