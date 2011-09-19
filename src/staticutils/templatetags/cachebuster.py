import time
from django.conf import settings
from django.template import Library
from staticutils.middleware import asset_hashes

register = Library()

@register.simple_tag
def cachebust(url):
    # If we're in DEBUG mode, always return the latest asset version.
    if settings.DEBUG:
        asset_hash = int(time.time())
    else:
        asset_hash = asset_hashes.get(url, int(time.time()))
    return '%s%s?%s' % (settings.STATIC_URL, url, asset_hash)
