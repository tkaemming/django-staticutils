from django.conf import settings
from django.template import Library
from staticutils.middleware import asset_versions
from staticutils.versioning import get_versioned_path

register = Library()

@register.simple_tag
def versionedstatic(path):
    versioned_path = path
    if not settings.DEBUG:
        version = asset_versions.get(path)
        if version:
            versioned_path = get_versioned_path(path, version)

    return ''.join((settings.STATIC_URL, versioned_path))
