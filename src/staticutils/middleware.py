from django.contrib.staticfiles.finders import get_finders
from django.core.exceptions import MiddlewareNotUsed
from staticutils.versioning import get_file_version

asset_versions = {}

class AssetVersioningMiddleware(object):
    """
    Middleware that runs through all static assets on server startup to 
    calculate their versioned value for cache-busting. To regenerate versions,
    the server must be restarted. The middleware is set up this way to avoid 
    having to do a disk read (and associated seek) as well as the version
    computation for each request.
    """
    def __init__(self):
        for finder in get_finders():
            for path, storage in finder.list([]):
                asset_versions[path] = get_file_version(path, storage)
        raise MiddlewareNotUsed
