from django.conf import settings

# Versioning

STATIC_VERSION_GENERATOR = getattr(settings, 'STATIC_VERSION_GENERATOR',
    'staticutils.hashing.get_file_hash')

STATIC_VERSION_PATH_GENERATOR = getattr(settings,
    'STATIC_VERSION_PATH_GENERATOR', 'staticutils.utils.get_versioned_path')

STATIC_VERSION_HASH_LENGTH = getattr(settings, 'STATIC_VERSION_HASH_LENGTH', 12)

STATIC_VERSION_IGNORE_HIDDEN_FILES = getattr(settings,
    'STATIC_VERSION_IGNORE_HIDDEN_FILES', False)

# Packaging

STATIC_PACKAGES = getattr(settings, 'STATIC_PACKAGES', {})

STATIC_PACKAGE_STORAGE = getattr(settings, 'STATIC_PACKAGE_STORAGE',
    'staticutils.storages.OverwritableFileSystemStorage')

STATIC_PACKAGE_STORAGE_OPTIONS = getattr(settings,
    'STATIC_PACKAGE_STORAGE_OPTIONS', {})

STATIC_PACKAGE_PREPROCESSORS = getattr(settings,
    'STATIC_PACKAGE_PREPROCESSORS', ())

STATIC_PACKAGE_POSTPROCESSORS = getattr(settings,
    'STATIC_PACKAGE_POSTPROCESSORS', ())
