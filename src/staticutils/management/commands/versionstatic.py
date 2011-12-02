from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic
from django.core.files.storage import FileSystemStorage
from staticutils.versioning import get_file_version, get_versioned_path

class Command(collectstatic.Command):
    help = "Collects static files from apps and other locations into "\
           "`VERSIONED_STATIC_ROOT` with a versioned filename. (Used in "\
           "conjunction with the {% versionedstatic %} template tag.)"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        # Force storage to be a filesystem storage for VERSIONED_STATIC_ROOT.
        self.storage = FileSystemStorage(location=settings.VERSIONED_STATIC_ROOT)
        try:
            self.storage.path('')
        except NotImplementedError:
            self.local = False
        else:
            self.local = True

    def copy_file(self, path, prefixed_path, source_storage, **kwargs):
        version = get_file_version(path, source_storage)
        prefixed_path = get_versioned_path(prefixed_path, version)
        return super(Command, self).copy_file(path, prefixed_path,
            source_storage, **kwargs)

    def link_file(self, path, prefixed_path, source_storage, **kwargs):
        version = get_file_version(path, source_storage)
        prefixed_path = get_versioned_path(prefixed_path, version)
        return super(Command, self).link_file(path, prefixed_path,
            source_storage, **kwargs)
