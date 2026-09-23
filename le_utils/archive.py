import hashlib
import zipfile

_CHUNK_SIZE = 64 * 1024


def _member_sha256(zf, info):
    digest = hashlib.sha256()
    with zf.open(info) as member:
        for chunk in iter(lambda: member.read(_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contents_sha256(fileobj):
    """
    Identity hash of a zip archive's member paths and bytes, independent of compression and metadata.
    FROZEN: ricecooker and Studio's upload Cloud Function index archives by this digest.
    :param fileobj: A seekable binary file object of a zip archive
    :return: A hex SHA-256 digest
    """
    with zipfile.ZipFile(fileobj) as zf:
        members = {}
        for info in zf.infolist():
            # Not .filename: Windows rewrites "\\" in it and Python >= 3.12 overrides it from 0x7075 extra fields.
            path = info.orig_filename
            # Before the directory skip: zipfile reads "x\0/" as file "x".
            if "\0" in path:
                raise ValueError(f"NUL in member path {path!r}")
            if path.endswith("/"):
                continue
            if path in members:
                raise ValueError(f"Duplicate member path {path!r}")
            members[path] = info
        digest = hashlib.sha256()
        for path in sorted(members):
            digest.update(f"{path}\0{_member_sha256(zf, members[path])}\n".encode("utf-8"))
    return digest.hexdigest()
