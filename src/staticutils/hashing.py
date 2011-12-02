import hashlib
from staticutils.settings import STATIC_VERSION_HASH_LENGTH

def get_file_hash(path, storage, hash_length=STATIC_VERSION_HASH_LENGTH):
    h = hashlib.md5()
    h.update(storage.open(path, 'rb').read())
    return h.hexdigest()[:hash_length]
