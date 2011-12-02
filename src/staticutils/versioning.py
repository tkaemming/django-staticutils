from django.utils.importlib import import_module
from staticutils.settings import STATIC_VERSION_GENERATOR, STATIC_VERSION_PATH_GENERATOR

module, method = STATIC_VERSION_GENERATOR.rsplit('.', 1)
get_file_version = getattr(import_module(module), method)

module, method = STATIC_VERSION_PATH_GENERATOR.rsplit('.', 1)
get_versioned_path = getattr(import_module(module), method)
