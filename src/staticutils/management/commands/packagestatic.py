import fnmatch
from django.contrib.staticfiles.finders import get_finders
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.core.management.base import NoArgsCommand
from django.utils.importlib import import_module
from staticutils import settings

def process(name, content, processors):
    for location in processors:
        module, callable = location.rsplit('.', 1)
        processor = getattr(import_module(module), callable)
        content = processor(name, content)
    return content

class Command(NoArgsCommand):
    can_import_settings = True

    def handle_noargs(self, *args, **kwargs):
        storage = get_storage_class(settings.STATIC_PACKAGE_STORAGE)
        destination = storage(**settings.STATIC_PACKAGE_STORAGE_OPTIONS)

        files = {}
        for finder in get_finders():
            files.update(dict(finder.list(ignore_patterns='') or []))

        for package, patterns in settings.STATIC_PACKAGES.items():
            names = []
            for pattern in patterns:
                if hasattr(pattern, 'search'):
                    matches = [name for name in files.keys()
                        if pattern.search(name) is not None]
                else:
                    matches = fnmatch.filter(files.keys(), pattern)
                names.extend(matches)

            contents = []
            for name in names:
                contents.append(process(name, files[name].open(name).read(),
                    settings.STATIC_PACKAGE_PREPROCESSORS))

            destination.save(package, ContentFile(process(package,
                "\n".join(contents), settings.STATIC_PACKAGE_POSTPROCESSORS)))
