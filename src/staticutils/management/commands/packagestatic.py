import fnmatch
from optparse import make_option
from django.contrib.staticfiles.finders import get_finders
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.core.management.base import NoArgsCommand
from django.utils.encoding import smart_str
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
    option_list = NoArgsCommand.option_list + (
        make_option('-i', '--ignore', action='append', default=[],
            dest='ignore_patterns', metavar='PATTERN',
            help="Ignore files or directories matching this glob-style "
                "pattern. Use multiple times to ignore more."),
        make_option('--no-default-ignore', action='store_false',
            dest='use_default_ignore_patterns', default=True,
            help="Don't ignore the common private glob-style patterns 'CVS', "
                "'.*' and '*~'."),
        make_option('--no-preprocess',
            action='store_false', dest='preprocess', default=True,
            help="Do NOT preprocess package contents."),
        make_option('--no-postprocess',
            action='store_false', dest='postprocess', default=True,
            help="Do NOT postprocess package contents."),
    )

    def handle_noargs(self, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.preprocess = options['preprocess']
        self.postprocess = options['postprocess']
        ignore_patterns = options['ignore_patterns']
        if options['use_default_ignore_patterns']:
            ignore_patterns += ['CVS', '.*', '*~']
        self.ignore_patterns = list(set(ignore_patterns))

        storage = get_storage_class(settings.STATIC_PACKAGE_STORAGE)
        destination = storage(**settings.STATIC_PACKAGE_STORAGE_OPTIONS)

        files = {}
        for finder in get_finders():
            files.update(dict(finder.list(ignore_patterns=self.ignore_patterns) or []))

        for package, patterns in settings.STATIC_PACKAGES.items():
            names = []
            for pattern in patterns:
                if hasattr(pattern, 'search'):
                    matches = [name for name in files.keys()
                        if pattern.search(name) is not None]
                else:
                    matches = fnmatch.filter(files.keys(), pattern)
                names.extend(matches)

            names = set(names) # don't include the same file twice in the same package
            file_count = len(names)
            self.log('Creating static package: %s (%s %s)' % (package,
                file_count, file_count == 1 and "file" or "files"), level=1)

            contents = []
            for name in names:
                self.log("   - %s" % name, level=2)
                content = files[name].open(name).read()
                if self.preprocess:
                    content = process(name, content,
                        settings.STATIC_PACKAGE_PREPROCESSORS)
                contents.append(content)

            content = "\n".join(contents)
            if self.postprocess:
                content = process(package, content,
                    settings.STATIC_PACKAGE_POSTPROCESSORS)

            destination.save(package, ContentFile(content))

    def log(self, msg, level=2):
        msg = smart_str(msg)
        if not msg.endswith("\n"):
            msg += "\n"
        if self.verbosity >= level:
            self.stdout.write(msg)
