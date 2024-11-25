import hashlib


def sha256(checksum, path):
    """Does the file match the checksum according to SHA256?"""
    return (checksum is None) or (_hash(hashlib.sha256(), path) == checksum)


def md5(checksum, path):
    """Does the file match the checksum according to MD5?"""
    return (checksum is None) or (_hash(hashlib.md5(), path) == checksum)


def _hash(hasher, path):
    try:
        with open(path, "rb") as f:
            while True:
                data = f.read(2**16)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
