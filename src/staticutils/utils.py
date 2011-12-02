import os
from staticutils.settings import STATIC_VERSION_IGNORE_HIDDEN_FILES

def get_versioned_path(path, version):
    """
    Returns a versioned path.

    If filename has an extension, the version hash comes before the extension:

        foo.css -> foo.a8d2bd908f64.css

    If the filename does not have an extension, the version hash comes after
    the base filename:

        foo/bar -> foo/bar.a8d2bd908f64
    """
    directory, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)

    if STATIC_VERSION_IGNORE_HIDDEN_FILES and basename.startswith('.'):
        return path

    bits = []
    if directory:
        bits.append('%s/%s' % (directory, basename))
    else:
        bits.append(basename)

    bits.append(version)
    if extension:
        bits.append(extension.lstrip('.'))

    return '.'.join(['%s' % bit for bit in bits])
