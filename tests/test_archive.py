import io
import struct
import zipfile
import zlib

import pytest

from le_utils.archive import contents_sha256

MEMBERS = [
    ("README.txt", b"Kolibri\n"),
    ("index.html", b"<html><body><p>Kolibri</p></body></html>\n"),
    ("css/site/style.css", b"p { color: #333; }\n"),
    ("assets/data.bin", bytes(range(256)) * 400),
    ("données/été.txt", "café\n".encode("utf-8")),
    ("empty.txt", b""),
]
EXPECTED_DIGEST = "9ccc8c88bedb2106e59879ba70e7c84f38f098bf8fa4a7a2476dad63eab0ae15"


def _zip(members, compression=zipfile.ZIP_DEFLATED):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", compression) as zf:
        for name, data in members:
            zf.writestr(name, data)
    archive.seek(0)
    return archive


@pytest.mark.parametrize("compression", [zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED], ids=["stored", "deflated"])
def test_contents_sha256_is_pinned(compression):
    assert contents_sha256(_zip(MEMBERS, compression)) == EXPECTED_DIGEST


def test_contents_sha256_ignores_member_order():
    assert contents_sha256(_zip(reversed(MEMBERS))) == EXPECTED_DIGEST


def test_contents_sha256_ignores_directory_entries():
    directories = [("css/", b""), ("css/site/", b""), ("données/", b"")]
    assert contents_sha256(_zip(directories + MEMBERS)) == EXPECTED_DIGEST


def test_contents_sha256_depends_on_member_paths():
    moved = [("moved/" + name if name == "index.html" else name, data) for name, data in MEMBERS]
    assert contents_sha256(_zip(moved)) != EXPECTED_DIGEST


def _with_metadata(name):
    info = zipfile.ZipInfo(name, date_time=(2001, 2, 3, 4, 5, 6))
    info.external_attr = 0o100755 << 16
    info.comment = b"comment"
    # Python >= 3.12 replaces ZipInfo.filename with this Unicode Path field's name.
    renamed = ("renamed/" + name).encode("utf-8")
    info.extra = struct.pack("<HHBL", 0x7075, 5 + len(renamed), 1, zlib.crc32(name.encode("utf-8"))) + renamed
    return info


def test_contents_sha256_ignores_metadata():
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as zf:
        zf.comment = b"archive comment"
        for name, data in MEMBERS:
            zf.writestr(_with_metadata(name), data)
    assert contents_sha256(archive) == EXPECTED_DIGEST


def test_contents_sha256_is_independent_of_file_position():
    archive = _zip(MEMBERS)
    archive.read()
    assert contents_sha256(archive) == EXPECTED_DIGEST
    assert not archive.closed


def test_contents_sha256_rejects_duplicate_paths():
    with pytest.warns(UserWarning):
        archive = _zip(MEMBERS + [("index.html", b"other")])
    with pytest.raises(ValueError):
        contents_sha256(archive)


def test_contents_sha256_rejects_nul_in_path():
    # zipfile truncates names at NUL when writing, so patch the stored bytes.
    # Trailing "/": NUL must be rejected before directory entries are skipped.
    archive = io.BytesIO(_zip([("nul#name/", b"x")]).getvalue().replace(b"nul#name", b"nul\0name"))
    with pytest.raises(ValueError):
        contents_sha256(archive)
