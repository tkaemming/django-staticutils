import errno
import os
from django.conf import settings
from django.core.files import locks
from django.core.files.move import file_move_safe
from django.core.files.storage import FileSystemStorage
from django.utils._os import abspathu


class OverwritableFileSystemStorage(FileSystemStorage):
    """
    A subclass of FileSystemStorage that allows files to be overwritten.
    """
    def __init__(self, location, base_url=None):
        self.base_location = location
        self.location = abspathu(self.base_location)
        if base_url is not None:
            self.base_url = base_url

    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        # ghetto port of FileSystemStorage._save, allows overwriting files
        full_path = self.path(name)

        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        try:
            if hasattr(content, 'temporary_file_path'):
                file_move_safe(content.temporary_file_path(), full_path)
                content.close()

            else:
                fd = os.open(full_path, os.O_WRONLY | os.O_CREAT |
                    getattr(os, 'O_BINARY', 0))
                try:
                    locks.lock(fd, locks.LOCK_EX)
                    for chunk in content.chunks():
                        os.write(fd, chunk)
                finally:
                    locks.unlock(fd)
                    os.close(fd)
        except OSError, e:
            raise

        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name
