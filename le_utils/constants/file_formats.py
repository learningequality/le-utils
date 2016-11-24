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
PERSEUS_MIMETYPE = "application/perseus+zip"

# constants for HTML5 zip format
HTML5 = "zip"
HTML5_MIMETYPE = "application/zip"


choices = (
    (MP4, _("MP4 Video")),

    (VTT, _("VTT Subtitle")),
    (SRT, _("SRT Subtitle")),

    (MP3, _("MP3 Audio")),
    (WAV, _("WAV Audio")),

    (PDF, _("PDF Document")),

    (JPG, _("JPG Image")),
    (JPEG, _("JPEG Image")),
    (PNG, _("PNG Image")),
    (JSON, _("JSON")),
    (SVG, _("SVG Image")),

    (PERSEUS, _("Perseus Exercise")),
    (HTML5, _("HTML5 Zip")),
)
