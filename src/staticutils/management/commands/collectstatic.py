from optparse import make_option
from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic
from django.core.management.base import CommandError


class Command(collectstatic.Command):
    option_list = collectstatic.Command.option_list + (
        make_option('--only-versioned',
            action='store_true',
            dest='only_versioned',
            default=False,
            help='Only collect static assets from `VERSIONED_STATIC_ROOT`. '\
                 'Cannot be used with `--plain`.'),
        make_option('--plain',
            action='store_true',
            dest='plain',
            default=False,
            help='Ignore `VERSIONED_STATIC_ROOT`. (Original behavior.) '\
                 'Cannot be used with `--only-versioned`.'),
    )

    def handle_noargs(self, only_versioned=False, plain=False, **options):
        if only_versioned and plain:
            raise CommandError(
                "--hashed-only and --plain cannot be used together."
            )

        if not plain:
            versioned_finder = ['staticutils.finders.VersionedStaticRootFinder']
            if only_versioned:
                # Only use our VersionedStaticRootFinder and rather than the default finders.
                settings.STATICFILES_FINDERS = versioned_finder
            else:
                # Original behavior, wih the addition of VERSIONED_STATIC_ROOT. 
                # We cast STATICFILES_FINDERS to a list to avoid a TypeError by
                # trying to concatenate a list to a tuple.
                settings.STATICFILES_FINDERS = list(settings.STATICFILES_FINDERS) + versioned_finder

        return super(Command, self).handle_noargs(**options)
