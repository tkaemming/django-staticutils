from django.conf import settings

STATIC_HASH_LENGTH = getattr(settings, 'STATIC_HASH_LENGTH', 12)
