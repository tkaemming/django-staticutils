import hashlib
from django.contrib.staticfiles.finders import get_finders
from django.core.exceptions import MiddlewareNotUsed
from staticutils.settings import STATIC_HASH_LENGTH

asset_hashes = {}

class CacheBusterMiddleware(object):
    """
    Middleware that runs through all static assets on server startup to 
    calculate their hashed value for cache-busting. To recalculate the hashes, 
    the server must be restarted. The middleware is set up this way to avoid 
    having to do a disk read (and associated seek) as well as the hash 
    computation for each request.
    """
    def __init__(self):
        for finder in get_finders():
            for path, storage in finder.list([]):
                hash = hashlib.md5()
                hash.update(storage.open(path, 'rb').read())
                version = '%s' % hash.hexdigest()
                asset_hashes[path] = version[0:STATIC_HASH_LENGTH]
        raise MiddlewareNotUsed
