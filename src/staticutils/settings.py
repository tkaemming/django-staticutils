from django.conf import settings

STATIC_VERSION_GENERATOR = getattr(settings, 'STATIC_VERSION_GENERATOR',
    'staticutils.hashing.get_file_hash')

STATIC_VERSION_PATH_GENERATOR = getattr(settings,
    'STATIC_VERSION_PATH_GENERATOR', 'staticutils.utils.get_versioned_path')

STATIC_VERSION_HASH_LENGTH = getattr(settings, 'STATIC_VERSION_HASH_LENGTH', 12)

STATIC_VERSION_IGNORE_HIDDEN_FILES = getattr(settings,
    'STATIC_VERSION_IGNORE_HIDDEN_FILES', False)
